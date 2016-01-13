from datetime import datetime
from ctx.toolkit import Generator

__author__ = 'fmca'


class TimeGenerator(Generator):
    def __init__(self):
        super(TimeGenerator, self).__init__("time", 1, 0.8)

    def generate(self):
        now = datetime.now()
        return {"value": now, "accuracy": 1}
