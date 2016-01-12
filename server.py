import json

from bottle import route, get, post, delete, static_file, response, request, run
from tinydb import TinyDB, where

db = TinyDB("db.json");
recipesTable = db.table("recipes");
widgets = []


@get('/recipe')
def get_recipes():
    response.content_type = "application/json";
    return json.dumps(recipesTable.all(), ensure_ascii=False).encode("utf-8");


@post('/recipe')
def new_recipe():
    recipesTable.insert(request.json);


@delete('/recipe/<name>')
def delete_recipe(name):
    recipesTable.remove(where('name') == name)


# Static files
@route('/<file_path:path>')
def server_static(file_path):
    return static_file(file_path, root='./static')


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

# actuator = Actuator()
# actuator.doFacebook({"value": "Raine Borba", "variables": {"messagem": "Hello"}})
gen_time = ctx.TimeGenerator()
gen_calendar = ctx.CalendarGenerator("tgkehbl0fecu2htgfai7qdkh7k@group.calendar.google.com")
gen_gps = ctx.GPSGenerator(100)

wgt_time = ctx.TimeWidget(gen_time)
wgt_agenda = ctx.AgendaWidget(gen_time, gen_calendar)
wgt_location = ctx.LocationWidget((-8.1075833, -35.0207727), gen_gps)

widgets = [wgt_time, wgt_agenda, wgt_location]
interpreter = ctx.Interpreter(recipesTable, widgets)

gen_calendar.start(15)
gen_time.start(2)
gen_gps.start(5)
interpreter.interpret(5)

run(host='localhost', port=8080, debug=True)
