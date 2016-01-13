from ctx.toolkit import Widget

__author__ = 'fmca'


class TimeWidget(Widget):
    def __init__(self, *generators):
        super(TimeWidget, self).__init__("Horario", "$horarioAgora", *generators)

    def update(self, event):
        now = self.get_property("time").time()
        self.status = now
