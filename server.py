from bottle import route, get, post, delete, static_file, response, request, run
from tinydb import TinyDB, where
from time import sleep
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

#actuator = Actuator()
#actuator.doFacebook({"value": "Raine Borba", "variables": {"messagem": "Hello"}})
gen_time = ctx.TimeGerator()
gen_calendar = ctx.CalendarGenerator("tgkehbl0fecu2htgfai7qdkh7k@group.calendar.google.com")

wgt_time = ctx.TimeWidget(gen_time)
wgt_agenda = ctx.AgendaWidget(gen_time, gen_calendar)

widgets = [wgt_time, wgt_agenda]
interpreter = ctx.Interpreter(recipesTable, widgets)

gen_calendar.start(15)
gen_time.start(5)
interpreter.interpret(5)
	
run(host='localhost', port=8080, debug=True)
