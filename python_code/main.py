from tkinter import *
import time
import random
from settings import *


class Shark:
    def __init__(self, V, M, x, y, cnvs):
        self.v, self.m = V, M
        self.x, self.y = x, y
        self.cnvs = cnvs
        self.Speed = 0
        self.dx = 0
        self.q = self.cnvs.create_text(self.x, self.y, text='🦈', justify=CENTER, font="Verdana 70")

    def info(self):
        otv = dict()
        otv['mg'] = self.m*g
        otv['Fa'] = self.v*g*ambient_density
        otv['P'] = self.y*g*ambient_density+Patm
        otv['F'] = self.v*g*ambient_density-self.m*g
        otv['X'] = self.x
        otv['Y'] = (self.y-self.Speed * 0.02 +WIDTH_canvas) % WIDTH_canvas
        return otv

    def correction(self, parameter, value):
        if parameter == 'V':
            self.v += value
            self.m += value*Ro2
        elif parameter == 'M':
            self.m += value
        elif parameter == 'X':
            self.dx += value

    def drow(self):
        q = self.cnvs.create_text(self.x, self.y, text='🦈', justify=CENTER, font="Verdana 70")

    def update(self, t):
        # if (self.v * ambient_density - self.m > 0 and self.y > 0) or (self.v * ambient_density - self.m < 0 and self.y < WIDTH_canvas):
        #     self.y -= self.Speed * t
        # elif self.y < 0:
        #     self.Speed += (self.v * g * ambient_density - self.m * g) * t / self.m
        #     self.Speed = max(self.Speed, 0)
        # elif self.y > WIDTH_canvas:
        #     self.Speed += (self.v * g * ambient_density - self.m * g) * t / self.m
        #     self.Speed = min(self.Speed, WIDTH_canvas)
        # if 0 < self.y < WIDTH_canvas:
        self.Speed += (self.v * g * ambient_density - self.m * g) * t / self.m
        self.y = (self.y-self.Speed * t + WIDTH_canvas) % WIDTH_canvas
        self.cnvs.move(self.q, self.dx, (self.y-self.Speed * t + WIDTH_canvas) % WIDTH_canvas-self.y)
        #self.cnvs.move(self.q, self.dx, - self.Speed * t)

        self.x += self.dx
        self.dx = 0
        self.y = min(self.y, WIDTH_canvas)
        self.y = max(self.y, 0)


class Fish:
    def __init__(self, canvas):
        self.x = 0
        self.y = random.randint(30, HEIGHT_canvas - 30)
        self.cnvs = canvas
        self.image = self.cnvs.create_text(self.x, self.y, text='🐠', justify=CENTER, font="Verdana 30")

    def respawn(self):
        x_old, y_old = self.x, self.y
        self.x = random.choice([random.randint(30, max(self.x-20, 30)),
                                random.randint(min(self.x+20, WIDTH_canvas-30), WIDTH_canvas-30)])
        self.y = random.choice([random.randint(30, max(self.y - 20, 30)),
                                random.randint(min(self.y + 20, HEIGHT_canvas - 30), HEIGHT_canvas - 30)])
        self.cnvs.move(self.image, self.x-x_old, self.y-y_old)
        return self.x, self.y


root = Tk()
root.geometry(f'{WIDTH}x{HEIGHT}+200+50')
root.title('fish_model')

r = Canvas(root, bg=BG_canvas, width=WIDTH_canvas, height=HEIGHT_canvas)
r.place(x=0, y=0)

l1 = Label(root)
l1.place(x=WIDTH_canvas+5, y=0)
l2 = Label(root)
l2.place(x=WIDTH_canvas+5, y=40)
l3 = Label(root)
l3.place(x=WIDTH_canvas+5, y=80)
l4 = Label(root)
l4.place(x=WIDTH_canvas+5, y=120)

cnt_o2 = 0


def f1():
    global cnt_o2
    if cnt_o2 <= max_cnt_o2:
        shark.correction('V', Vo2)
        cnt_o2 += 1


def f2():
    global cnt_o2
    if cnt_o2 >= -max_cnt_o2:
        shark.correction('V', -Vo2)
        cnt_o2 -= 1


def movef(event):
    if event.keysym == 'Right':
        shark.correction('X', step)
    if event.keysym == 'Left':
        shark.correction('X', -step)
    if event.keysym == 'Up':
        f1()
    if event.keysym == 'Down':
        f2()


Button(root, text='набрать воздух', command=f1).place(x=WIDTH_canvas+5, y=160)
Button(root, text='выпустить воздух', command=f2).place(x=WIDTH_canvas+5, y=200)

root.bind("<KeyPress-Left>", movef)
root.bind("<KeyPress-Right>", movef)
root.bind("<KeyPress-Up>", movef)
root.bind("<KeyPress-Down>", movef)

shark = Shark(V, M, X_shark, Y_shark, r)
fish = Fish(r)
fish_x, fish_y = fish.respawn() #кастыль
cnt = 0
while True:
    shark.update(0.02)
    root.update()
    time.sleep(0.01)
    cnt += 1
    if cnt > 10:
        cnt = 0
        x = shark.info()
        if abs(x['X']-fish_x) < 42 and abs(x['Y']-fish_y) < 42:
            fish_x, fish_y = fish.respawn()
            shark.correction('M', M_fish)
        l1['text'] = f'mg: {round(x["mg"], 2)} Н'
        l2['text'] = f'Fa: {round(x["Fa"], 2)} Н'
        l3['text'] = f'P: {round(x["P"], 2)} Па'
        l4['text'] = f'F: {round(x["F"], 2)} Н'
        print(x["Y"])
