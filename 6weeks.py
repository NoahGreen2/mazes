from tkinter import *
import random
import time

win = Tk()
win.geometry("450x450")
win.title("6 Week Project")
c = Canvas(win, width=450, height=450, bg="white")
c.pack()

squares = []
for i in range(25, 425, 50):
    for j in range(25, 425, 50):
        squares.append(c.create_rectangle(i, j, i+50, j+50, fill="white", outline="black"))

round = 1
lives = 3
sequence = []
prog = 0
sequence.append(random.randint(0, 63))

def find_possible_next_square(sequence):
    last = sequence[-1]
    possible = []
    if last % 8 != 7:
        possible.append(last + 1)
    if last % 8 != 0:
        possible.append(last - 1)
    if last > 7:
        possible.append(last - 8)
    if last < 56:
        possible.append(last + 8)
    return possible
def check_square(index):
    global prog
    if index != sequence[prog]:
        global lives
        lives -= 1
        print("Wrong! You now have " + str(lives) + " lives.")
        if lives == 0:
            print("You lost!")
            win.quit()
        else:
            prog = 0
            time.sleep(0.5)
            begin_round(round, lives, sequence)
    else:
        prog += 1
        if prog == len(sequence):
            prog = 0
            next = random.choice(find_possible_next_square(sequence))
            sequence.append(next)
            begin_round(round, lives, sequence)
def begin_round(round, lives, sequence):
    for i in sequence:
        c.itemconfig(squares[i], fill="red")
        win.update()
        time.sleep(1)
        c.itemconfig(squares[i], fill="white")
        win.update()
    index = 0
    for square in squares:
        c.tag_bind(square, "<Button-1>", lambda event, index=index: check_square(index))
        index += 1

win.update()
time.sleep(3)
begin_round(round, lives, sequence)

win.mainloop()