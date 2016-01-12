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
    def __init__(self, type, status_name, *generators):
        super(Widget, self).__init__()
        self.type = type
        self.generators = generators
        self.status = None
        self.status_name = status_name
        for generator in generators:
            generator.register(self)

    def getproperty(self, type):
        for generator in self.generators:
            if generator.type == type:
                return generator.property


class Generator(Observable):
    def __init__(self, type, relevance, threshold):
        super().__init__()
        self.property = None
        self.type = type
        self.relevance = relevance
        self.threshold

    def generate(self):
        # generate a dict, e.g.: {"value": 12, "certainity" : 0.9}
        raise NotImplementedError("Not implemented")

    def has_acceptable_certainity(self, new_property):
        return new_property.certainity + (self.relevance * new_property.certainity) < self.threshold

    def start(self, delay):
        new_property = self.generate()
        if new_property['value'] != self.property and self.has_acceptable_certainity(new_property):
            self.property = new_property['value']
            event = Event(self.type, property=new_property['value'])
            super().notify(event)
        timerTask = Timer(delay, lambda: self.start(delay), ())
        timerTask.start();
