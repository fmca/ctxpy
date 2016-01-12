import urllib.request
import time
import json
from datetime import datetime
from time import mktime
from threading import Timer

from ctx_toolkit import Generator, Widget
from action import Actuator


class TimeWidget(Widget):
    def __init__(self, *generators):
        super(TimeWidget, self).__init__("Horario", "$horarioAgora", *generators)

    def update(self, event):
        now = self.getproperty("time").time()
        self.status = now


class AgendaWidget(Widget):
    def __init__(self, *generators):
        super(AgendaWidget, self).__init__("Ocupado", None, *generators)

    def update(self, event):
        now = self.getproperty("time")
        events = self.getproperty("calendar")
        occupied = False
        if events and now:
            for event in events:
                if (now >= event['start'] and now < event['end']):
                    occupied = True
        self.status = occupied


class TimeGerator(Generator):
    def __init__(self):
        super(TimeGerator, self).__init__("time", 1, 0.8)

    def generate(self):
        now = datetime.now()
        return {"value": now, "certainity": 1}


class CalendarGenerator(Generator):
    def __init__(self, calendar_id):
        super(CalendarGenerator, self).__init__("calendar", 1, 0.8)
        self.calendar_id = calendar_id
        self.date_fmt = '%Y-%m-%dT%H:%M:%S'

    def generate(self):
        response = urllib.request.urlopen(
            "https://www.googleapis.com/calendar/v3/calendars/" + self.calendar_id + "/events?key=AIzaSyAPwTbtA7jzilZebl124PaPkqThQ2Glnno")
        data = json.loads(response.read().decode("UTF-8"))
        events = [];
        for event_json in data['items']:
            event = dict()
            start_str = event_json['start']['dateTime']
            end_str = event_json['end']['dateTime']

            def create_event(start_str, end_str):
                event['start'] = datetime.fromtimestamp(mktime(time.strptime(start_str, self.date_fmt)))
                event['end'] = datetime.fromtimestamp(mktime(time.strptime(end_str, self.date_fmt)))

            try:
                create_event(start_str, end_str)
            except ValueError:
                try:
                    create_event(start_str[:-6], end_str[:-6])
                except ValueError:
                    create_event(start_str[:-1], end_str[:-1])
            events.append(event)
        return {"value": events, "certainty": 1}


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
                    print("replacing, " + v['name'] + " in " + value)
                    value = value.replace(v['name'], v['value'])
            return value

        for action in recipe['action']:
            action['value'] = replace(action['value'])
        for action_variable in recipe['variables']:
            action_variable['value'] = replace(action_variable['value'])
        return recipe

    def interpret(self, delay):
        recipes = self.recipesTable.all()
        for recipe in recipes:
            is_ready = len(recipe['context']) > 0
            for ctx in recipe['context']:
                if ctx['id'] == 'Horario':
                    is_ready = is_ready and self.check_time(ctx)
                elif ctx['id'] == 'Ocupado':
                    is_ready = is_ready and self.check_agenda(ctx)
            if is_ready and not self.statuses.get(recipe['name'], not is_ready):
                print(recipe['name'] + " is ready")
                recipe = self.update_variables(self.get_variables(), recipe)
                self.actuator.execute_in_background(recipe)
            self.statuses[recipe['name']] = is_ready
        timer_task = Timer(delay, lambda: self.interpret(delay), ())
        timer_task.start()

    def check_agenda(self, ctx):
        occupied = self.get_widget("Ocupado").status
        if ctx['category'] == 'ocupado':
            return occupied
        else:
            return not occupied

    def check_time(self, ctx):
        wgt_time_status = self.get_widget("Horario").status
        ctx_time = datetime.strptime(ctx['value'], '%H:%M').time()
        if ctx['category'] == '>':
            return wgt_time_status > ctx_time
        elif ctx['category'] == '<':
            return wgt_time_status < ctx_time
        else:
            return wgt_time_status == ctx_time
