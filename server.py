from bottle import route, get, post, static_file, response, request, run
from tinydb import TinyDB
from time import sleep
from json import dumps

db = TinyDB("db.json");
recipesTable = db.table("recipes");

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
	
from ctx_toolkit import Generator, Widget
import os

class TimeWidget(Widget):
	def __init__(self, *generators):
		super(TimeWidget, self).__init__("time", *generators)
	def update(self, event):
		for generator in self.generators:
			print(generator.property)
			
class TimeGerator(Generator):
	def __init__(self):
		super(TimeGerator, self).__init__("time")
	def generate(self):
		from datetime import datetime
		now = datetime.now().time()
		return str(now.hour )+ ":" + str(now.minute) + ":" + str(now.second)
		
		
gen_time = TimeGerator()
wgt_time = TimeWidget(gen_time)

gen_time.start(1)

	
#run(host='localhost', port=8080, debug=True)