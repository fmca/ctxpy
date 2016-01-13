from ctx.toolkit import Widget

__author__ = 'fmca'


class LocationWidget(Widget):
    def __init__(self, home_location, *generators, distance_ts=50):
        super(LocationWidget, self).__init__("Em Casa", "$emCasa", *generators)
        self.home_location = home_location
        self.distance_ts = distance_ts

    def update(self, event):
        gps_coord = self.get_property("gps")
        home_tuple = tuple(map(lambda x: float(x), StrUtils.split(self.home_location, ",", 1)))
        new_distance = distance(Point(home_tuple[1], home_tuple[0]), Point(gps_coord[1], gps_coord[0])).meters
        print("distance: " + str(new_distance) + " between: " + str(gps_coord) + " and " + str(self.home_location))
        self.status = new_distance < self.distance_ts
