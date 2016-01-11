from ctx_toolkit import Generator, Widget
import os, urllib.request, time, json
from datetime import datetime
from time import mktime
from action import Actuator
from threading import Timer

class TimeWidget(Widget):
	def __init__(self, *generators):
		super(TimeWidget, self).__init__("Horario", "$horarioAgora", *generators)
	def update(self, event):
		now = self.getproperty("time").time()
		self.status = now
			
class AgendaWidget(Widget):
	def __init__(self, *generators):
		super(AgendaWidget, self).__init__("Ocupado", None, *generators)
	def update(self, event):
		now = self.getproperty("time")
		events = self.getproperty("calendar")
		occupied = False
		if events and now: 
			for event in events:
				if(now >= event['start'] and now < event['end']):
					occupied = True
		self.status = occupied
		
class TimeGerator(Generator):
	def __init__(self):
		super(TimeGerator, self).__init__("time")
	def generate(self):
		now = datetime.now()
		return now
		

class CalendarGenerator(Generator):
	def __init__(self, calendar_id):
		super(CalendarGenerator, self).__init__("calendar")
		self.calendar_id = calendar_id
		self.date_fmt = '%Y-%m-%dT%H:%M:%S'
	def generate(self):
		response = urllib.request.urlopen("https://www.googleapis.com/calendar/v3/calendars/"+self.calendar_id+"/events?key=AIzaSyAPwTbtA7jzilZebl124PaPkqThQ2Glnno")
		data = json.loads(response.read().decode("UTF-8"))
		events = [];
		for event_json in data['items']:
			event = dict()
			startstr = event_json['start']['dateTime']
			endstr = event_json['end']['dateTime']
			def createEvent(startstr, endstr):
				event['start'] = datetime.fromtimestamp(mktime(time.strptime(startstr, self.date_fmt)))
				event['end'] = datetime.fromtimestamp(mktime(time.strptime(endstr, self.date_fmt)))
			try:
				createEvent(startstr, endstr)
			except ValueError:
				try:
					createEvent(startstr[:-6], endstr[:-6])
				except ValueError:
					createEvent(startstr[:-1], endstr[:-1])
			events.append(event)
		return events


class Interpreter:
	def __init__(self, recipesTable, widgets):
		self.recipesTable = recipesTable;
		self.widgets = widgets
		self.statuses = dict()
		self.actuator = Actuator()
	def getwidget(self, type):
		for widget in self.widgets:
			if widget.type == type:
				return widget
	def getvariables(self):
		variables = []
		for w in self.widgets:
			variables.append({"name": w.status_name, "value": str(w.status)})
		return variables
	def updatevariables(self, variables, recipe):
		def replace(value):
			for v in variables:
				if v['name']:
					print("replacing, " + v['name'] + " in " + value)
					value = value.replace(v['name'], v['value'])
			return value
		for action in recipe['action']:
			action['value'] = replace(action['value'])
		for action_variable in recipe['variables']:
			action_variable['value'] = replace(action_variable['value'])
		return recipe
	def interpret(self, delay):
		recipes = self.recipesTable.all()
		for recipe in recipes:
			isReady = len(recipe['context']) > 0
			for ctx in recipe['context']:
				if ctx['id'] == 'Horario':
					isReady = isReady and self.checkTime(ctx)
				elif ctx['id'] == 'Ocupado':
					isReady = isReady and self.checkAgenda(ctx)
			if isReady and not self.statuses.get(recipe['name'], not isReady):
				print(recipe['name'] + " is ready")
				recipe = self.updatevariables(self.getvariables(), recipe)
				self.actuator.executeInBackground(recipe)
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
