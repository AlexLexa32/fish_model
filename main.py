from tkinter import *
from настройки import *
import time


class Object:
    def __init__(self):
        self.v, self.m, self.h = V, M, H

    def info(self):
        otv = dict()
        otv['mg'] = self.m*g
        otv['Fa'] = self.v*g*ambient_density
        otv['P'] = self.h*g*ambient_density+100_000
        return otv

    def correction(self, parameter, new_value):
        if parameter == 'V':
            self.v = new_value
        elif parameter == 'M':
            self.m = new_value
        elif parameter == 'H':
            self.h = new_value


root = Tk()
root.geometry('400x400+200+50')

r = Canvas(root, bg='#142351', width=2000, height=2000)
r.pack()
obj = r.create_rectangle(1, 1, 50, 50, fill='#830a71')


root.mainloop()