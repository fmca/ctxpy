from threading import Timer

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
		
class Widget(Observable, Observer):
	def __init__(self, type, *generators):
		super(Widget, self).__init__()
		self.type = type
		self.generators = generators
		self.status = None
		for generator in generators:
			generator.register(self)
	def getproperty(self, type):
		for generator in self.generators:
			if generator.type == type:
				return generator.property
	
			
class Generator(Observable):
	def __init__(self, type):
		super().__init__()
		self.property = None
		self.type = type
	def generate(self):
		raise NotImplementedError("Not implemented")
	def start(self, delay):
		new_property = self.generate()
		if new_property != self.property:
			self.property = new_property
			event = Event(self.type, property=new_property)
			super().notify(event)
		timerTask = Timer(delay, lambda: self.start(delay), ())
		timerTask.start();