from ctx.toolkit import Widget

__author__ = 'fmca'


class AgendaWidget(Widget):
    def __init__(self, *generators):
        super(AgendaWidget, self).__init__("Ocupado", None, *generators)

    def update(self, event):
        now = self.get_property("time")
        events = self.get_property("calendar")
        occupied = False
        if events and now:
            for event in events:
                if event['start'] <= now < event['end']:
                    occupied = True
        self.status = occupied
