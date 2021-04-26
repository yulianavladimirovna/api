import math


class MapParams:
    LAT_STEP = 0.008
    LON_STEP = 0.02

    def __init__(self):
        self.longitude = 37.530887
        self.latitude = 55.703118
        self.zoom = 15
        self.l = 'map'
        self.pt = []

    def up_zoom(self):
        self.zoom += 1

    def down_zoom(self):
        self.zoom -= 1

    def get_longitude(self):
        return self.longitude

    def get_latitude(self):
        return self.latitude

    def get_zoom(self):
        return self.zoom

    def left(self):
        self.longitude -= self.LON_STEP * math.pow(2, 15 - self.zoom)

    def right(self):
        self.longitude += self.LON_STEP * math.pow(2, 15 - self.zoom)

    def up(self):
        self.latitude += self.LAT_STEP * math.pow(2, 15 - self.zoom)

    def down(self):
        self.latitude -= self.LAT_STEP * math.pow(2, 15 - self.zoom)

    def get_pt(self):
        return '~'.join(self.pt)

    def new_pt(self, long, lat, m='pm2blm'):
        self.pt = [','.join([long, lat, m])]

    def new_l(self, l):
        self.l = l

    def get_l(self):
        return self.l

    def new_search(self, lon, lat):
        self.new_pt(str(lon), str(lat))
        self.longitude = lon
        self.latitude = lat