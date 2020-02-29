import random
import math
from tkinter import *
from tkinter import messagebox

random.seed()
init_pos_limit = 10.0
sheep_move_dist = 0.5
wolf_move_dist = 1.0
scale = 20.0
animal_dot = 10.0
sheep_alive = 0


def add_sheep(event):
    global world
    x, y = event.x, event.y
    sheep = Sheep(world, x, y)
    world.add_animal(sheep)
    update_alive()


def update_alive():
    global sheep_alive
    sheep_alive = world.alive_sheep()
    sheep_alive_label.configure(text="Sheep: %s" % sheep_alive)


def update_wolf_position(event):
    world.animals[0].update_position(event.x, event.y)


def reset():
    while len(world.animals) > 0:
        world.remove_animal(0)
    wolf = Wolf(world, 400, 400)
    world.add_animal(wolf)
    update_alive()


class Sheep():
    def __init__(self, world, pos_x, pos_y):
        self.world = world;
        self.pos_x = pos_x;
        self.pos_y = pos_y;
        self.shape = canvas.create_oval(pos_x - animal_dot, pos_y - animal_dot, pos_x + animal_dot, pos_y + animal_dot,
                                        fill="blue")

    def show_position(self, event):
        self.pos_x = event.x
        self.pos_y = event.y

    def sheep_move(self):
        x = random.randrange(4)
        if x == 0:
            self.pos_x += sheep_move_dist * scale
            canvas.move(self.shape, +sheep_move_dist * scale, 0)
        elif x == 1:
            self.pos_x -= sheep_move_dist * scale
            canvas.move(self.shape, -sheep_move_dist * scale , 0)
        elif x == 2:
            self.pos_y += sheep_move_dist * scale
            canvas.move(self.shape, 0, +sheep_move_dist * scale)
        elif x == 3:
            self.pos_y -= sheep_move_dist * scale
            canvas.move(self.shape, 0, -sheep_move_dist * scale)
        canvas.update()


class Wolf(object):
    def __init__(self, world, pos_x, pos_y):
        self.world = world;
        self.pos_x = pos_x;
        self.pos_y = pos_y;
        self.shape = canvas.create_oval(pos_x - animal_dot, pos_y - animal_dot, pos_x + animal_dot, pos_y + animal_dot,
                                        fill="red")

    def show_position(self):
        print('{}, {}'.format(self.pos_x,self.pos_y))

    def update_position(self, pos_x, pos_y):
        canvas.move(self.shape, pos_x - self.pos_x, pos_y - self.pos_y)
        self.pos_x = pos_x
        self.pos_y = pos_y

    def detect(self):
        basic_distance = 0.0
        number = 1
        for x, val in enumerate(self.world.animals):
            if isinstance(val, Sheep):
                distance = math.sqrt((val.pos_x - self.pos_x) ** 2 + (val.pos_y - self.pos_y) ** 2) / scale
                if basic_distance > distance or basic_distance == 0.0:
                    basic_distance = distance
                    number = x
        return number, basic_distance

    def wolf_move(self):
        number, distance = self.detect()
        self.show_position()
        if distance < wolf_move_dist:
            self.pos_x = self.world.animals[number].pos_x
            self.pos_y = self.world.animals[number].pos_y
            canvas.move(self.shape, -self.pos_x, -self.pos_y)
            canvas.move(self.shape, self.world.animals[number].pos_x, self.world.animals[number].pos_y)
            self.world.remove_animal(number)
        else:
            x_an = wolf_move_dist * ((self.world.animals[number].pos_x - self.pos_x)/distance)
            y_an = wolf_move_dist * ((self.world.animals[number].pos_y - self.pos_y)/distance)
            canvas.move(self.shape, -self.pos_x, -self.pos_y)
            self.pos_x = self.pos_x + (x_an)
            self.pos_y = self.pos_y + (y_an)
            canvas.move(self.shape, self.pos_x, self.pos_y)

class World:
    def __init__(self):
        self.animals = []

    def add_animal(self, animal):
        self.animals.append(animal)

    def remove_animal(self, index):
        canvas.delete(self.animals[index].shape)
        del self.animals[index]

    def alive_sheep(self):
        temp = 0
        for i in self.animals:
            if isinstance(i, Sheep):
                temp += 1
        return temp

    def tura(self):
        if sheep_alive > 0:
            for x in self.animals:
                if isinstance(x, Sheep):
                    x.sheep_move()
            self.animals[0].wolf_move()
        else:
            messagebox.showerror("Blad","Brak owiec, nie mozna przeprowadzic symulacji")
        update_alive()


root = Tk()
root.title("Chase")
root.resizable(False, False)
canvas = Canvas(root, width=4 * init_pos_limit * scale, height=4 * init_pos_limit * scale, background="green")
buttonFrame = Frame(root, width=0.5 * init_pos_limit * scale, height=4 * init_pos_limit * scale)

canvas.pack(side="bottom", expand=False)
buttonFrame.pack(side="top", expand=False)

sheep_alive_label = Label(buttonFrame, text="Sheep: %s" % sheep_alive)
sheep_alive_label.grid(column=0, row=0)

world = World()
wolf = Wolf(world, 400, 400)
world.add_animal(wolf)

button_step = Button(buttonFrame, text="Nastepny Krok", command=world.tura)
button_step.grid(column=1, row=0)
button_reset = Button(buttonFrame, text="Reset", command=reset)
button_reset.grid(column=2, row=0)

canvas.bind('<Button-1>', add_sheep)
canvas.bind('<Button-3>', update_wolf_position)
root.mainloop()

#   for x in range(1, total_rounds + 1):
#    sheep_move(owce)
#       detect(wilk, owce)
#     tura(owce)
