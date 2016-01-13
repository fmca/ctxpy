from abc import abstractmethod
from threading import Timer
from ctx.uncertainty.measurers import clear_dobson_paddy


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
    @abstractmethod
    def update(self, event):
        pass

    def __init__(self, type, status_name, *generators):
        super(Widget, self).__init__()
        self.type = type
        self.generators = generators
        self.status = None
        self.status_name = status_name
        for generator in generators:
            generator.register(self)

    def get_property(self, type):
        for generator in self.generators:
            if generator.type == type:
                return generator.property


class Generator(Observable):
    def __init__(self, type, relevance, threshold, certainty_measurer=clear_dobson_paddy):
        super().__init__()
        self.certainty_measurer = certainty_measurer
        self.property = None
        self.type = type
        self.relevance = relevance
        self.threshold = threshold

    def generate(self):
        # generate a dict, e.g.: {"value": 12, "certainty" : 0.9}
        raise NotImplementedError("Not implemented")

    def has_acceptable_certainty(self, new_property):
        certainty_level = self.certainty_measurer(self.relevance, new_property['accuracy'])
        is_acceptable = certainty_level > self.threshold
        return is_acceptable

    def start(self, delay=5):
        new_property = self.generate()
        if new_property['value'] != self.property and self.has_acceptable_certainty(new_property):
            self.property = new_property['value']
            event = Event(self.type, property=new_property['value'])
            super().notify(event)
        timer_task = Timer(delay, lambda: self.start(delay), ())
        timer_task.start()


