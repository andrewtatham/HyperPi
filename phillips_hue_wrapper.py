import pprint
import random

import time
from phue import Bridge


class HueWrapper(object):
    def __init__(self):

        self.light_name = "Hue color lamp 1"
        self.bridge_ip = '192.168.0.20'
        self.b = None
        self.light = None

    def connect(self):
        self.b = Bridge(self.bridge_ip)
        self.b.connect()
        for l in self.b.lights:
            text = l.name
            if l.name == self.light_name:
                text += " *"
                self.light = l
            print(text)
        if self.light.reachable:
            print("connected")
        pprint.pprint(self.light.__dict__)

    def on(self):
        self.light.on = True

    def colour_temperature(self, temp):
        # (white only) 154 is the coolest, 500 is the warmest
        self.light.ct = temp

    def xy(self, x, y):
        #  co-ordinates in CIE 1931 space
        self.light.xy = (x, y)

    def random_colour(self):
        self.light.xy = [random.random(), random.random()]

    def hue(self, hue, sat):
        # hue' parameter has the range 0-65535 so represents approximately 182*degrees
        # sat is 0-255?
        self.light.hue = hue
        self.light.sat = sat

    def brightness(self, bright):
        # // brightness between 0-254 (NB 0 is not off!)
        self.light.bri = bright

    def colour_loop(self):
        self.light.effect = "colorloop"

    def flash_once(self):
        self.light.alert = "select"

    def flash_multiple(self):
        self.light.alert = "lselect"

    def flash_off(self):
        self.light.alert = None

    def off(self):
        self.light.on = False

    @property
    def is_on(self):
        return self.light.on

    def set_hsv(self, hsv):
        if not self.light.on:
            self.on()
        h = int(hsv[0] * 65535)
        s = int(hsv[1] * 255)
        v = int(hsv[2] * 255)
        print((h, s, v))
        self.hue(h, s)
        self.brightness(v)
        pass


if __name__ == '__main__':
    hue = HueWrapper()
    hue.connect()

    hue.on()
    hue.brightness(254)
    for _ in range(5):
        hue.random_colour()

    hue.colour_temperature(154)
    hue.colour_temperature(500)
    hue.colour_temperature(154)
    hue.colour_loop()
    hue.off()
