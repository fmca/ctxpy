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

def time_handler(generators):
	print("handler")
	for gen in generators:
		print(gen._property)
	
wgt_time = Widget(type, time_handler)

def time_generator():
	from datetime import datetime
	now = datetime.now().time()
	return str(now.hour )+ ":" + str(now.minute) + ":" + str(now.second)
gen_time = Generator(wgt_time, "time", time_generator)

gen_time.start(1)

	
#run(host='localhost', port=8080, debug=True)