import random
from tkinter import *
import time

win = Tk()
win.geometry("800x800")
win.title("Maze creater")

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
        cells.append([i, j, connected_walls, False])

cell = cells[0]
for i in cell[2]:
    c.itemconfig(i, fill="red")
cell[3] = True

def find_touching_cells(i, j):
    touching_cells = []
    for x in cells:
        if x[0] == i and abs(x[1] - j) == 50 and x[3] == False:
            touching_cells.append(x)
        elif abs(x[0] - i) == 50 and x[1] == j and x[3] == False:
            touching_cells.append(x)
    return touching_cells

def find_touching_wall(i, j):
    for x in i[2]:
        for y in j[2]:
            if x == y:
                return x

def step_back(l):
    if find_touching_cells(visited[-l][0], visited[-l][1]):
        recursion_sequence(visited[-l])
    else:
        step_back(l+1)

def next_cell(touching_cells, cell):
    choices = []
    for x in touching_cells:
        if x[3] == False:
            choices.append(x)
    if len(choices) != 0:
        next = random.choice(choices)
        wall = find_touching_wall(cell, next)
        c.delete(wall)
        win.update()
        time.sleep(0.1)
        cell[2].remove(wall)
        next[2].remove(wall)
        next[3] = True
        return next
    else:
        step_back(1)

visited = []

def recursion_sequence(cell):
    if cell not in visited:
        visited.append(cell)
    if len(visited) < 196:
        recursion_sequence(next_cell(find_touching_cells(cell[0], cell[1]), cell))

def choose_end(visited):
    choices = []
    for cell in visited:
        if len(cell[2]) == 3:
            choices.append(cell)
    furthest = 0
    for cell in choices:
        if cell[0] + cell[1] > furthest:
            furthest = cell[0] + cell[1]
            end = cell
    for wall in end[2]:
        c.itemconfig(wall, fill="green")

recursion_sequence(cell)
win.update()

choose_end(visited[:-1])


win.mainloop()