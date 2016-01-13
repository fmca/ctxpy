from datetime import datetime, time
import json
from time import mktime
import urllib
from ctx.toolkit import Generator

__author__ = 'fmca'


class CalendarGenerator(Generator):
    def __init__(self, calendar_id):
        super(CalendarGenerator, self).__init__("calendar", 1, 0.8)
        self.calendar_id = calendar_id
        self.date_fmt = '%Y-%m-%dT%H:%M:%S'

    def generate(self):
        response = urllib.request.urlopen(
            "https://www.googleapis.com/calendar/v3/calendars/" + self.calendar_id + "/events?key=AIzaSyAPwTbtA7jzilZebl124PaPkqThQ2Glnno")
        data = json.loads(response.read().decode("UTF-8"))
        events = []
        for event_json in data['items']:
            event = dict()
            start_str = event_json['start']['dateTime']
            end_str = event_json['end']['dateTime']

            def create_event(start_str, end_str):
                event['start'] = datetime.fromtimestamp(mktime(time.strptime(start_str, self.date_fmt)))
                event['end'] = datetime.fromtimestamp(mktime(time.strptime(end_str, self.date_fmt)))

            try:
                create_event(start_str, end_str)
            except ValueError:
                try:
                    create_event(start_str[:-6], end_str[:-6])
                except ValueError:
                    create_event(start_str[:-1], end_str[:-1])
            events.append(event)
        return {"value": events, "accuracy": 1}

