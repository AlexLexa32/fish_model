from tkinter import *
from настройки import *
import time


class Fish:
    def __init__(self, V, M, x, y, cnvs):
        self.v, self.m = V, M
        self.x, self.y = x, y
        self.cnvs = cnvs
        self.Speed = 0
        self.q = self.cnvs.create_text(self.x, self.y, text='🐠', justify=CENTER, font="Verdana 70")

    def info(self):
        otv = dict()
        otv['mg'] = self.m*g
        otv['Fa'] = self.v*g*ambient_density
        otv['P'] = self.h*g*ambient_density+Patm
        otv['F'] = abs(self.m*g-self.v*g*ambient_density)
        return otv

    def correction(self, parameter, new_value):
        if parameter == 'V':
            self.v = new_value
        elif parameter == 'M':
            self.m = new_value
        elif parameter == 'H':
            self.h = new_value

    def drow(self):
        q = self.cnvs.create_text(self.x, self.y, text='🐠', justify=CENTER, font="Verdana 70")

    def update(self, t):
        #if self.y > 0 and self.y < WIDTH_canvas:
        if  0 < self.y < WIDTH_canvas:
            self.y -= self.Speed*t
            self.Speed += (self.v*g*ambient_density-self.m*g)*t/self.m

            self.cnvs.move(self.q, 0, -self.Speed*t)
            print(self.y)



root = Tk()
root.geometry(f'{WIDTH}x{HEIGHT}+200+50')
root.title('fish_model')

r = Canvas(root, bg=BG_canvas, width=WIDTH_canvas, height=HEIGHT_canvas)
r.place(x=0, y=0)
# obj = r.create_rectangle(1, 1, 50, 50, fill='#830a71')
fish = Fish(V, M, X_fish, Y_fish, r)
#fish.drow()
while True:
    fish.update(0.02)
    #fish.drow()
    root.update()
    time.sleep(0.01)
#r.create_text(30, 30, text='🐠', justify=CENTER, font="Verdana 70")

root.mainloop()
