import random
from tkinter import *
import math

# Create a window
win = Tk()
win.geometry("800x800")
win.title("Maze creater")

# Create a canvas
c = Canvas(win, width=800, height=800, bg="white")
c.pack()

walls = []
for i in range(50, 751, 50):
    for j in range(50, 750, 50):
        walls.append(c.create_line(i, j, i, j+50))
for i in range(50, 750, 50):
    for j in range(50, 751, 50):
        walls.append(c.create_line(i, j, i+50, j))

cells = []
for i in range(75, 726, 50):
    for j in range(75, 726, 50):
        connected_walls = []
        for x in walls:
            if c.coords(x)[0] == c.coords(x)[2] and (c.coords(x)[1] + c.coords(x)[3])/2 == j and abs(c.coords(x)[0] - i) <= 25:
                connected_walls.append(x)
            elif c.coords(x)[1] == c.coords(x)[3] and (c.coords(x)[0] + c.coords(x)[2])/2 == i and abs(c.coords(x)[1] - j) <= 25:
                connected_walls.append(x)
        cells.append([i, j, connected_walls])

cellx = int(input("Enter x coordinate of cell: "))
celly = int(input("Enter y coordinate of cell: "))

for i in cells:
    if i[0] == cellx and i[1] == celly:
        cell = i
for i in cell[2]:
    c.itemconfig(i, fill="red")

win.mainloop()