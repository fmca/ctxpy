from bottle import route, get, post, static_file, response, request, run
from tinydb import TinyDB
from time import sleep
from json import dumps

db = TinyDB("db.json");
recipesTable = db.table("recipes");
widgets = []

@get('/recipe')
def getRecipes():
	response.content_type = "application/json";
	return dumps(recipesTable.all(), ensure_ascii=False).encode("iso-8859-1");
	
@post('/recipe')
def newRecipe():
	contextRecipe = request.json.get("context");
	actionRecipe = request.json.get("action");
	recipesTable.insert(request.json);
	
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
	answer = dict()
	for widget in widgets:
		answer[widget.type] = str(widget.status)
	return dumps(answer, ensure_ascii=False).encode("iso-8859-1")
	
import ctx

gen_time = ctx.TimeGerator()
wgt_time = ctx.TimeWidget(gen_time)
gen_calendar = ctx.CalendarGenerator("tgkehbl0fecu2htgfai7qdkh7k@group.calendar.google.com")
wgt_agenda = ctx.AgendaWidget(gen_time, gen_calendar)

widgets = [wgt_time, wgt_agenda]

gen_calendar.start(5)
gen_time.start(5)
	
run(host='localhost', port=8080, debug=True)