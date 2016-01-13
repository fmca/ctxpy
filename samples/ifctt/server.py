import sys
import os.path
# importing parent modules
sys.path.append(os.path.join(os.path.dirname(__file__), '../..'))

import json

from bottle import route, get, post, delete, static_file, response, request, run
from ctx.generators import TimeGenerator, CalendarGenerator, GPSGenerator
from ctx.widgets import TimeWidget, AgendaWidget, LocationWidget
from tinydb import TinyDB, where

db = TinyDB("db.json");
recipes_table = db.table("recipes")
configs_table = db.table("configs")
if len(configs_table.all()) == 0:
    configs_table.insert({"name": "calendar", "value": "tgkehbl0fecu2htgfai7qdkh7k@group.calendar.google.com"})
    configs_table.insert({"name": "location", "value": '-8.1075833, -35.0207727'})
widgets = []


@get('/recipe')
def get_recipes():
    response.content_type = "application/json";
    return json.dumps(recipes_table.all(), ensure_ascii=False).encode("utf-8")


@post('/recipe')
def new_recipe():
    recipes_table.insert(request.json);


@delete('/recipe/<name>')
def delete_recipe(name):
    recipes_table.remove(where('name') == name)


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


@get('/configs')
def configs():
    response.content_type = "application/json"
    answer = [configs_table.search(where('name') == 'calendar')[0],
              configs_table.search(where('name') == 'location')[0]]
    return json.dumps(answer, ensure_ascii=False).encode("iso-8859-1")


@post('/configs')
def save_config():
    for config in request.json:
        print(config)
        configs_table.remove(where('name') == config['name'])
        configs_table.insert(config)
        if config['name'] == 'calendar':
            gen_calendar.calendar_id == config['value']
        if config['name'] == 'location':
            wgt_location.home_location = config['value']
    answer = configs_table.all()
    return json.dumps(answer, ensure_ascii=False).encode("iso-8859-1")


from samples.ifctt import interpreter

gen_time = TimeGenerator()
gen_calendar = CalendarGenerator(configs_table.search(where('name') == 'calendar')[0]['value'])
gen_gps = GPSGenerator(100)

wgt_time = TimeWidget(gen_time)
wgt_agenda = AgendaWidget(gen_time, gen_calendar)
wgt_location = LocationWidget(configs_table.search(where('name') == 'location')[0]['value'], gen_gps)

widgets = [wgt_time, wgt_agenda, wgt_location]
interpreter = interpreter.Interpreter(recipes_table, widgets)

gen_calendar.start()
gen_time.start()
gen_gps.start()
interpreter.start()

run(host='localhost', port=8080, debug=True)
