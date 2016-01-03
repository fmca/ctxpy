from bottle import route, post, static_file, request, run
from tinydb import TinyDB
from time import sleep

@post('/recipe')
def newRecipe():
	contextRecipe = request.json.get("context");
	actionRecipe = request.json.get("action");
	sleep(2);
	print(contextRecipe);
	print(actionRecipe);
	
# Static files
@route('/<filepath:path>')
def server_static(filepath):
    return static_file(filepath, root='./static')
	
run(host='localhost', port=8080, debug=True)