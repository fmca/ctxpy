
from uiautomator import device as d
from subprocess import call
from threading import Thread

class Actuator:
	def executeInBackground(self, recipe):
		thread = Thread(target = self.execute, args = (recipe, ))
		thread.start()
	def execute(self, recipe):
		for action in recipe['action']:
			if action['id'] == 'Facebook':
				self.doFacebook(action, recipe['variables'])
			elif action['id'] == 'Calendar':
				self.doAgenda(action, recipe['variables'])
			elif action['id'] == 'Email':
				self.doEmail(action, recipe['variables'])

	def doEmail(self, action, variables):
		d.screen.on()
		d.press.home()
		Adb.start("com.google.android.gm/com.google.android.gm.ComposeActivityGmail")
		d(resourceId="com.google.android.gm:id/to").click()
		Adb.write(action['value'])
		d.press.enter()
		d(resourceId="com.google.android.gm:id/subject").click()
		Adb.write(self.getVar("$titulo", variables))
		d(resourceId="com.google.android.gm:id/body").click()
		Adb.write(self.getVar("$mensagem", variables))
		d(resourceId="com.google.android.gm:id/send").click()		
		
	def doAgenda(self, action, variables):
		pass
	def doFacebook(self, action, variables):
		contact = action["value"]
		d.screen.on()
		d.press.home()
		Adb.start("com.facebook.orca/.auth.StartScreenActivity")
		d(resourceId="com.facebook.orca:id/action_search").click()
		Adb.write(contact)
		d(className="android.widget.ListView").child(index=1).click()
		d(resourceId="com.facebook.orca:id/edit_text").click()
		Adb.write(self.getVar("$mensagem", variables))
		d(description="Enviar").click()
	def getVar(self, varname, variables):
		return next(filter(lambda var: var['name'] == varname, variables))['value']
        


class Adb:
    def write(text):
         call(["adb", "shell", "input", "text", "'" + text.replace(' ', '%s') + "'"])
    def start(activity):
        call(["adb", "shell", "am", "start", activity])
        
