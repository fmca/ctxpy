from bottle import route, post, static_file, request, run
from tinydb import TinyDB

@post('/recipe')
def newRecipe():
	recipe = request.json.get("recipe");
	print(recipe);
	
# Static files
@route('/<filepath:path>')
def server_static(filepath):
    return static_file(filepath, root='./static')
	
run(host='localhost', port=8080, debug=True)