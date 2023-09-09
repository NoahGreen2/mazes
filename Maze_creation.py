import random
from tkinter import *
import time
from PIL import Image, ImageTk

win = Tk()
win.geometry("800x800")
win.title("Maze creater")

c = Canvas(win, width=800, height=800, bg="white")
c.pack()

img1 = Image.open("mouse.png").resize((50, 50), Image.ANTIALIAS)
mouse_image = ImageTk.PhotoImage(img1)

img2 = Image.open("cheese.png").resize((50, 50), Image.ANTIALIAS)
cheese_image = ImageTk.PhotoImage(img2)

wall_coords = []
active_walls = []
path_end = []

for i in range(50, 751, 50):
    for j in range(50, 750, 50):
        line = c.create_line(i, j, i, j+50)
        wall_coords.append(c.coords(line))
        active_walls.append(line)
for i in range(50, 750, 50):
    for j in range(50, 751, 50):
        line = c.create_line(i, j, i+50, j)
        wall_coords.append(c.coords(line))
        active_walls.append(line)

cells = []

for i in range(75, 726, 50):
    for j in range(75, 726, 50):
        connected_walls = []
        for x in active_walls:
            if c.coords(x)[0] == c.coords(x)[2] and (c.coords(x)[1] + c.coords(x)[3])/2 == j and abs(c.coords(x)[0] - i) <= 25:
                connected_walls.append(x)
            elif c.coords(x)[1] == c.coords(x)[3] and (c.coords(x)[0] + c.coords(x)[2])/2 == i and abs(c.coords(x)[1] - j) <= 25:
                connected_walls.append(x)
        cells.append([i, j, connected_walls, False])

cell = cells[0]
for i in cell[2]:
    c.itemconfig(i, fill="red", width=5)
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
        cell[2].remove(wall)
        next[2].remove(wall)
        active_walls.remove(wall)
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
        c.itemconfig(wall, fill="green", width=5)
    c.create_image(end[0], end[1], image=cheese_image)
    return end

recursion_sequence(cell)
win.update()



def find_possible_paths(cell, path):
    possible_paths = []
    possible_connected_walls = []
    missing_walls = []
    for x in wall_coords:
        if x[0] == x[2] and (x[1] + x[3])/2 == cell[1] and abs(x[0] - cell[0]) <= 25:
            possible_connected_walls.append(x)
        elif x[1] == x[3] and (x[0] + x[2])/2 == cell[0] and abs(x[1] - cell[1]) <= 25:
            possible_connected_walls.append(x)
    for wall in cell[2]:
        if c.coords(wall) in possible_connected_walls:
            possible_connected_walls.remove(c.coords(wall))
    missing_walls = possible_connected_walls
    for wall in missing_walls:
        if wall[0] == wall[2]:
            for x in cells:
                if abs(x[0]-wall[0]) == 25 and x[1] == (wall[1] + wall[3])/2 and x != cell and x not in path and x[3] == True:
                    possible_paths.append(x)
        elif wall[1] == wall[3]:
            for x in cells:
                if abs(x[1]-wall[1]) == 25 and x[0] == (wall[0] + wall[2])/2 and x != cell and x not in path and x[3] == True:
                    possible_paths.append(x)
    return possible_paths

def loop_solve(cell, path, end):
    for ball in path_end:
        c.delete(ball)
    path_end.append(c.create_image(cell[0], cell[1], image=mouse_image))
    win.update()
    time.sleep(0.1)
    cell[3] = False
    path.append(cell)
    if cell != end:
        possible_paths = find_possible_paths(cell, path)
        if possible_paths:
            loop_solve(possible_paths[0], path, end)
        else:
            loop_solve(path[-2], path[:-2], end)
    else:
        for x in range(len(path)-1):
            c.create_line(path[x][0], path[x][1], path[x+1][0], path[x+1][1], fill="blue", width=5)

def solve_maze(start, end):
    path = []
    loop_solve(start, path, end)

solve_maze(cell, choose_end(visited[:-1]))

win.mainloop()