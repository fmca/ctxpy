from datetime import datetime
from threading import Timer

from samples.ifctt.action import Actuator


class Interpreter:
    def __init__(self, recipes_table, widgets):
        self.recipesTable = recipes_table;
        self.widgets = widgets
        self.statuses = dict()
        self.actuator = Actuator()

    def get_widget(self, type):
        for widget in self.widgets:
            if widget.type == type:
                return widget

    def get_variables(self):
        variables = []
        for w in self.widgets:
            variables.append({"name": w.status_name, "value": str(w.status)})
        return variables

    @staticmethod
    def update_variables(variables, recipe):
        def replace(value):
            for v in variables:
                if v['name']:
                    value = value.replace(v['name'], v['value'])
            return value

        for action in recipe['action']:
            action['value'] = replace(action['value'])
        for action_variable in recipe['variables']:
            action_variable['value'] = replace(action_variable['value'])
        return recipe

    def start(self, delay=5):
        recipes = self.recipesTable.all()
        for recipe in recipes:
            is_ready = len(recipe['context']) > 0
            for ctx in recipe['context']:
                if ctx['id'] == 'Horario':
                    is_ready = is_ready and self.check_time(ctx)
                elif ctx['id'] == 'Ocupado':
                    is_ready = is_ready and self.check_agenda(ctx)
                elif ctx['id'] == 'Localizacao':
                    is_ready = is_ready and self.check_location(ctx)
            if is_ready and not self.statuses.get(recipe['name'], not is_ready):
                print(recipe['name'] + " is ready")
                recipe = self.update_variables(self.get_variables(), recipe)
                self.actuator.execute_in_background(recipe)
            self.statuses[recipe['name']] = is_ready
        timer_task = Timer(delay, lambda: self.start(delay), ())
        timer_task.start()

    def check_agenda(self, ctx):
        occupied = self.get_widget("Ocupado").status
        if ctx['category'] == 'ocupado':
            return occupied
        else:
            return not occupied

    def check_time(self, ctx):
        wgt_time_status = self.get_widget("Horario").status
        if wgt_time_status:
            ctx_time = datetime.strptime(ctx['value'], '%H:%M').time()
            if ctx['category'] == '>':
                return wgt_time_status > ctx_time
            elif ctx['category'] == '<':
                return wgt_time_status < ctx_time
            else:
                return wgt_time_status == ctx_time

    def check_location(self, ctx):
        home = self.get_widget("Em Casa").status
        if ctx['category'] == 'em casa':
            return home
        else:
            return not home
