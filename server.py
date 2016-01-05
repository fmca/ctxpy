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
	
	
	
class Widget:
	def register():
		pass
	
class Generator:
	pass
	
class Interpreter:
	pass
	
run(host='localhost', port=8080, debug=True)