import colorsys
import colour
from tkinter import *

from phillips_hue_wrapper import HueWrapper


class App:
    def __init__(self, master):
        self.light = None
        self.master = master
        self.fullscreen = False
        # w, h = self.master.winfo_screenwidth(), self.master.winfo_screenheight()
        # self.master.overrideredirect(1)
        # self.master.geometry("%dx%d+0+0" % (w, h))

        self.master.focus_set()
        self.master.bind("<F10>", self.toggle_fullscreen)
        self.master.bind("<Escape>", self.end_fullscreen)

        self.frame = Frame(self.master)
        self.frame.pack()

        self.canvas = Canvas(self.frame, height=60, width=360)
        self.canvas.pack()

        self.on = BooleanVar(self.frame)
        self.on_checkbox = Checkbutton(
            self.frame,
            text="on",
            variable=self.on,
            height=5,
            width=10,
            indicatoron=FALSE,
            borderwidth=6)
        self.on_checkbox.pack()
        self.on.trace("w", self.update_on)

        self.hue = DoubleVar(self.frame, 0.0)
        self.sat = DoubleVar(self.frame, 1.0)
        self.var = DoubleVar(self.frame, 1.0)

        self.hue_slider = Scale(
            self.frame,
            orient=HORIZONTAL,
            label="h",
            variable=self.hue,
            length=360,
            width=30,
            to=360,
            resolution=1)
        self.sat_slider = Scale(
            self.frame,
            orient=HORIZONTAL,
            label="s",
            variable=self.sat,
            length=360,
            width=30,
            to=1,
            resolution=0.01)
        self.var_slider = Scale(
            self.frame,
            orient=HORIZONTAL,
            label="v",
            variable=self.var,
            length=360,
            width=30,
            to=1,
            resolution=0.01)
        self.hue_slider.pack()
        self.sat_slider.pack()
        self.var_slider.pack()

        self.hue.trace("w", self.update_hsv)
        self.sat.trace("w", self.update_hsv)
        self.var.trace("w", self.update_hsv)

        self.quit_button = Button(
            self.frame, text="QUIT", fg="red", command=self.frame.quit
        )
        self.quit_button.pack(side=LEFT)

        self.fullscreen_button = Button(self.frame, text="Fullscreen", command=self.toggle_fullscreen)
        self.fullscreen_button.pack(side=LEFT)

        self.update_hsv()

    def toggle_fullscreen(self, event=None):
        self.fullscreen = not self.fullscreen  # Just toggling the boolean
        self.master.attributes("-fullscreen", self.fullscreen)
        return "break"

    def end_fullscreen(self, event=None):
        self.fullscreen = False
        self.master.attributes("-fullscreen", False)
        return "break"

    def update_on(self, *args):
        on = self.on.get()
        if on and not self.light.is_on:
            self.light.on()
        elif not on and self.light.is_on:
            self.light.off()

    def update_hsv(self, *args):
        h = self.hue.get() / 360.0
        s = self.sat.get()
        v = self.var.get()
        hsv = (h, s, v)
        print(hsv)
        rgb = colorsys.hsv_to_rgb(h, s, v)
        print(rgb)
        hex_colour = colour.rgb2hex(rgb, force_long=True)
        print(hex_colour)
        self.canvas.configure(background=hex_colour)

        self.init_light()

        self.light.set_hsv(hsv)

    def init_light(self):
        if not self.light:
            self.light = HueWrapper()
            self.light.connect()
        self.on.set(self.light.is_on)


if __name__ == '__main__':
    root = Tk()

    app = App(root)

    root.mainloop()

    # root.destroy()  # optional; see description below
