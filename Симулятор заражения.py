from tkinter import *
from random import *
import time
from time import time
import matplotlib.pyplot as plt


class Ball():
    def __init__(self, color='lightblue'):
        self.color = color
        self.last = False
        if self.color != 'red':
            self.infection = False
        else:
            self.infection = True

        self.radius = randint(1, 10)
        self.change_x = randint(-5, 5)
        self.change_y = randint(-5, 5)

        self.x = randint(self.radius+3, inf.width-self.radius-3)
        self.y = randint(inf.indent+3+self.radius, inf.height-self.radius-3)
        self.id = inf.canvas.create_oval(self.x - self.radius,
                                         self.y - self.radius,
                                         self.x + self.radius,
                                         self.y + self.radius, fill=self.color)


class Infection():

    def __init__(self):
        self.ar_balls = []
        self.indent = 100
        self.flag = False
        self.ar_rect = []

    def create_field(self, width, height):
        self.ar_graph_cnt = [1]
        self.f = True
        self.tic = 0
        self.height = height
        self.width = width
        self.win = Tk()
        self.win.title('Симулятор заражения')
        self.win.resizable(0, 0)
        self.canvas = Canvas(self.win, width=self.width, height=self.height)
        self.canvas.pack()
        self.scale = Scale(self.win, orient='horizontal', from_=5, to=500)
        self.scale.set('50')
        self.scale.place(x=100, y=5)

        self.label = Label(text='Количество:')
        self.label.place(x=30, y=5)

        self.count = 1
        self.ar_time = [0]

        self.cnt = 2

        self.btn2 = Button(text='Вывести График', command=self.graph)
        self.btn2.place(x=300, y=10)
        
        self.width_rect = self.width // (self.cnt * 2 + 1)
        self.height_rect = self.height // (self.cnt * 2 + 1)
        self.ar_balls.append(Ball(color='red'))

        self.btn1 = Button(text='Начать симуляцию', command=self.create_balls)
        self.btn1.place(x=400, y=10)
        self.canvas.mainloop()

    def create_balls(self):
        self.f = True
        if self.tic == 0:
            self.tic = time()
        if self.flag is False:
            self.flag = True
            self.cnt_balls = self.scale.get()
            for i in range(self.scale.get()-1):
                self.ar_balls.append(Ball())

            self.canvas.create_rectangle(3, self.indent,
                                         self.width,
                                         self.height)
            '''
            for i in range(1,self.cnt*2+1,2):
                for j in range(1,self.cnt*2+1,2):
                    self.ar_rect.append(self.canvas.create_rectangle(3+self.width_rect*j,
                                        self.indent+self.height_rect*i,
                                        3+self.width_rect*(j+1) ,
                                        self.indent+self.height_rect*(i+1) ))
            '''
            self.movement()

    def movement(self):
        while self.f:
            for cur_ball in self.ar_balls:
                if self.f:
                    self.check_collision(cur_ball)
                    self.canvas.move(cur_ball.id, cur_ball.change_x,
                                     cur_ball.change_y)
                    self.borders(cur_ball)

                    self.win.update()

    def borders(self, cur_ball):
        if (self.canvas.coords(cur_ball.id)[2] >= self.width) or self.canvas.coords(cur_ball.id)[0] <= 3:
            cur_ball.change_x = -cur_ball.change_x
        if self.canvas.coords(cur_ball.id)[3] >= self.height or self.canvas.coords(cur_ball.id)[1] <= self.indent:
            cur_ball.change_y = -cur_ball.change_y

    def check_collision(self, cur_ball):
        x1 = self.canvas.coords(cur_ball.id)[0]
        y1 = self.canvas.coords(cur_ball.id)[1]
        x2 = self.canvas.coords(cur_ball.id)[2]
        y2 = self.canvas.coords(cur_ball.id)[3]
        ar_overlap = list(self.canvas.find_overlapping(x1, y1, x2, y2))

        try:
            ar_overlap.pop(ar_overlap.index(self.ar_balls[-1].id + 1))

        except ValueError:
            None

        for i in range(2, len(self.ar_rect)+2, 1):
            try:
                ar_overlap.pop(ar_overlap.index(self.ar_balls[-1].id + i))
                print(ar_overlap.index(self.cnt_balls + i))
            except ValueError:
                None

        for i in ar_overlap:

            if self.ar_balls[i-1].infection:
                for j in ar_overlap:
                    if self.ar_balls[j-1].infection is False:
                        self.count += 1
                        self.tac = time()
                        self.ar_time.append(self.tac - self.tic)
                        self.ar_graph_cnt.append(self.count)

                    self.ar_balls[j-1].infection = True
                    self.ar_balls[j-1].last = True
                    self.canvas.itemconfig(self.ar_balls[j-1].id, fill='red')
                    #if self.count == self.cnt_balls:
                            #self.graph()
                            #self.count = 0

    def graph(self):
        figure = plt.figure()

        plt.title('График заражения')
        
        plt.plot(self.ar_time, self.ar_graph_cnt, 'r')
        plt.grid()
        plt.show()

width = 600
height = 600

inf = Infection()
inf.create_field(width, height)
