from threading import Thread

from uiautomator import device as d
from ctx.generators.util import Adb


class Actuator:
    def execute_in_background(self, recipe):
        thread = Thread(target=self.execute, args=(recipe,))
        thread.start()

    def execute(self, recipe):
        for action in recipe['action']:
            if action['id'] == 'Facebook':
                self.do_facebook(action, recipe['variables'])
            elif action['id'] == 'Calendar':
                self.do_agenda(action, recipe['variables'])
            elif action['id'] == 'Email':
                self.do_email(action, recipe['variables'])

    def do_email(self, action, variables):
        d.screen.on()
        d.press.home()
        Adb.start("com.google.android.gm/com.google.android.gm.ComposeActivityGmail")
        d(resourceId="com.google.android.gm:id/to").click()
        Adb.write(action['value'])
        d.press.enter()
        d(resourceId="com.google.android.gm:id/subject").click()
        Adb.write(self.get_var("$titulo", variables))
        d(resourceId="com.google.android.gm:id/body").click()
        Adb.write(self.get_var("$mensagem", variables))
        d(resourceId="com.google.android.gm:id/send").click()

    def do_agenda(self, action, variables):
        pass

    def do_facebook(self, action, variables):
        contact = action["value"]
        d.screen.on()
        d.press.home()
        Adb.start("com.facebook.orca/.auth.StartScreenActivity")
        d(resourceId="com.facebook.orca:id/action_search").click()
        Adb.write(contact)
        d(className="android.widget.ListView").child(index=1).click()
        d(resourceId="com.facebook.orca:id/edit_text").click()
        Adb.write(self.get_var("$mensagem", variables))
        d(description="Enviar").click()

    @staticmethod
    def get_var(var_name, variables):
        return next(filter(lambda var: var['name'] == var_name, variables))['value']
