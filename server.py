from bottle import route, get, post, delete, static_file, response, request, run
from tinydb import TinyDB, where
from time import sleep
from threading import Timer
from datetime import datetime
import json

db = TinyDB("db.json");
recipesTable = db.table("recipes");
widgets = []

@get('/recipe')
def getRecipes():
	response.content_type = "application/json";
	return json.dumps(recipesTable.all(), ensure_ascii=False).encode("utf-8");
	
@post('/recipe')
def newRecipe():
	recipesTable.insert(request.json);
	
@delete('/recipe/<name>')
def deleteRecipe(name):
	recipesTable.remove(where('name')==name)
	
# Static files
@route('/<filepath:path>')
def server_static(filepath):
    return static_file(filepath, root='./static')
	
# Static files
@get('/')
def home():
    return static_file("index.html", root='./static')
	
@get('/widgets')
def widgets():
	response.content_type = "application/json"
	answer = []
	for widget in widgets:
		answer.append({"type": widget.type, "status": str(widget.status)})
	return json.dumps(answer, ensure_ascii=False).encode("iso-8859-1")
	
import ctx

class Interpreter:
	def __init__(self, *widgets):
		self.widgets = widgets
		self.statuses = dict()
	def getwidget(self, type):
		for widget in widgets:
			if widget.type == type:
				return widget
	def interpret(self, delay):
		recipes = recipesTable.all()
		for recipe in recipes:
			isReady = len(recipe['context']) > 0
			for ctx in recipe['context']:
				if ctx['id'] == 'Horario':
					isReady = isReady and self.checkTime(ctx)
				elif ctx['id'] == 'Ocupado':
					isReady = isReady and self.checkAgenda(ctx)
			if isReady and not self.statuses.get(recipe['name'], not isReady):
				print(recipe['name'] + " is ready")
			self.statuses[recipe['name']] = isReady
		timerTask = Timer(delay, lambda: self.interpret(delay), ())
		timerTask.start()
		
	def checkAgenda(self, ctx):
		occupied = self.getwidget("Ocupado").status
		if ctx['category'] == 'ocupado':
			return occupied
		else:
			return not occupied
	
	def checkTime(self, ctx):
		time = self.getwidget("Horario").status
		ctx_time = datetime.strptime(ctx['value'], '%H:%M').time()
		if ctx['category'] == '>':
			return time > ctx_time
		elif ctx['category'] == '<':
			return time < ctx_time
		else:
			return time == ctx_time

from uiautomator import device as d
from subprocess import call

class Actuator:
    def doAgenda(self, action):
        pass
    def doFacebook(self, action):
        d.screen.on()
        d.press.home()
        call(["adb", "shell", "am", "start", "com.facebook.orca/.auth.StartScreenActivity"])
        d(resourceId="com.facebook.orca:id/action_search").click()
        
        

gen_time = ctx.TimeGerator()
wgt_time = ctx.TimeWidget(gen_time)
gen_calendar = ctx.CalendarGenerator("tgkehbl0fecu2htgfai7qdkh7k@group.calendar.google.com")
wgt_agenda = ctx.AgendaWidget(gen_time, gen_calendar)

widgets = [wgt_time, wgt_agenda]

interpreter = Interpreter(widgets)

gen_calendar.start(15)
gen_time.start(5)
interpreter.interpret(5)
	
run(host='localhost', port=8080, debug=True)
