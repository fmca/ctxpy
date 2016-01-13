import re
import traceback
from ctx.generators.util import Adb, StrUtils
from ctx.toolkit import Generator

__author__ = 'fmca'


class GPSGenerator(Generator):
    def __init__(self, acceptable_distance):
        super(GPSGenerator, self).__init__("gps", 1, 0.7)
        self.acceptable_distance = acceptable_distance

    def generate(self):
        result = Adb.shell("dumpsys", "location").replace("\n", "").replace("\r", "")
        m = re.match(".*Last Known Locations:.*gps: Location\[gps (.*?) acc=(.*?) et.*Last Known.*", result)
        coordinates = None
        accuracy = 0
        try:
            coordinates_tuple_str = tuple(StrUtils.split(m.group(1), ",", 2))
            print(coordinates_tuple_str)
            coordinates = tuple(map(lambda x: float(x.replace(",", ".")), coordinates_tuple_str))
            accuracy = 1 - (int(m.group(2)) / self.acceptable_distance)
        except AttributeError:
            traceback.print_exc()  # m can be None

        return {"value": coordinates, "accuracy": accuracy}