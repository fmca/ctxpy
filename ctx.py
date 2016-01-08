from ctx_toolkit import Generator, Widget
import os, urllib.request, time, json
from datetime import datetime
from time import mktime

class TimeWidget(Widget):
	def __init__(self, *generators):
		super(TimeWidget, self).__init__("Time", *generators)
	def update(self, event):
		now = self.getproperty("time").time()
		self.status = now
			
class AgendaWidget(Widget):
	def __init__(self, *generators):
		super(AgendaWidget, self).__init__("Agenda", *generators)
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