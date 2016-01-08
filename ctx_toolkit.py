class Event:
	def __init__(self, type, **kwargs):
		self.type = type
		self.properties = kwargs

class Observer:
	def update(self):
		raise NotImplementedError("Not implemented")

class Observable:
	def __init__(self):
		self._observers = []
	def register(self, observer):
		self._observers.append(observer)
	def notify(self, event):
		event.source = self
		for observer in self._observers:
			observer.update(event)
		
class Widget(Observer, Observable):
	def __init__(self, type, fn_change_handler):
		self._change_handler = fn_change_handler
	def update(self, obj):
		self._change_handler(Observable._observers)
			
from threading import Timer
class Generator(Observable):
	def __init__(self, widget, type, fn_generate):
		Observable.__init__(self)
		self._property = None
		self._generate = fn_generate
		self._type = type
	def start(self, delay):
		
		new_property = self._generate()
		print(new_property)
		if(new_property != self._property):
			self._property = new_property
			event = Event(self._type, property=new_property)
			self.notify(event)
		timerTask = Timer(delay, lambda: self.start(delay), ())
		timerTask.start();