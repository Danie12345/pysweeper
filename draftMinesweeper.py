# -*- coding: utf-8 -*-
"""
Created on Wed Oct 23 00:13:29 2019

@author: daniel
"""

# minesweeper

from tkinter import Button, Tk, Label, Frame, font, DISABLED, NORMAL, CENTER, LEFT, RIGHT
from PIL import ImageTk, Image
from random import randint as r
from screeninfo import get_monitors
from math import log10 as log
from math import ceil


IMG_SCALE = 14
STATS_HEIGHT = 30
BUTTONS_SIZE = 26

NUM_COLORS = {1:"Red", 2:"Orange", 3:"Green", 4:"Cyan", 5:"Blue", 6:"Magenta", 7:"Purple", 8:"Indigo"}
get_rgb = lambda rgb: "#%02x%02x%02x" % rgb

def nohover(event):
    pass

def right_click(event):
    label = Label(event.widget, image=RED_FLAG, anchor=CENTER)
    if event.widget.parent.clicks < 1:
        label.pack()
        event.pressedType = "FLAG"
        event.widget.parent.clicks += 1
        event.widget['state'] = DISABLED
    else:
        label.destroy()
        event.widget.parent.clicks -= 1
        event.pressedType = "None"
        event.widget['state'] = NORMAL
    event.widget.update()
    

def mouse_wheel_click(event):
    if event.pressedType == "None":
        label = Label(event.widget, image=RED_FLAG, anchor=CENTER)
        label.pack()
        event.pressedType = "FLAG"

class Botones:
    def __init__(self, buttons, caches):
        self.buttons = buttons
        self.caches = caches

class unBoton:
    def __init__(self, fils=1, cols=1, x=1, y=1, butt=None):
        self.fils = fils
        self.cols = cols
        self.clicks = 0
        self.x = x
        self.y = y
        self.pressedType = "None"
        self.bombs_around = 0
        self.shown = False
        
        self.mines = 0
        self.text = " {} ".format("   ")
        self.butt = butt
        self.butt.configure(text=self.text, command=self.hacer)
        self.butt.parent = self
        self.cache = {}
    
    def hacer(self):
        buttons = self.parent.buttons
        caches = self.parent.caches
        if self.clicks == 0:
            self.clicks += 1
            if self.mines:
                for row in buttons:
                    for button in row:
                        if button.mines:
                            if not button.shown:
                                button.shown = True
                                label = Label(button.butt, image=BOMB_BOOM, anchor=CENTER)
                                label.pack()
                        button.butt['state'] = DISABLED
            else:
                if self.bombs_around == 0:
                    self.discover()
                else:
                    self.text = f" {self.bombs_around} "
                    caches[-1][self.fils, self.cols] = buttons[self.fils][self.cols].bombs_around
                    label = Label(self.butt, text=self.text if self.text != " 0 " else "     ", font=FONT, bg=get_rgb((240,240,240)), fg=NUM_COLORS[self.bombs_around], anchor=CENTER)
                    label.pack(padx=0, pady=0)
                self.butt['state'] = DISABLED
            buttons[self.fils][self.cols] = self       
    
    def bombs_count(self):
        buttons = self.parent.buttons
        total = 0
        for row in range(-1,2):
            for col in range(-1,2):
                if (0 <= self.fils + row < len(buttons)) and (0 <= self.cols + col < len(buttons[0])):
                    total += buttons[self.fils + row][self.cols + col].mines
        self.bombs_around = total
    
    def discover(self):
        buttons = self.parent.buttons
        caches = self.parent.caches
        for row in range(-1,2):
            for col in range(-1,2):
                if (0 <= self.fils + row < len(buttons)) and (0 <= self.cols + col < len(buttons[0])):
                    caches[-1][self.fils + row, self.cols + col] = buttons[self.fils + row][self.cols + col].bombs_around
                    buttons[self.fils + row][self.cols + col].hacer()

def StartGame():
    global BOMB_TICK, BOMB_BOOM, RED_FLAG, FONT
    mines = Tk()
    cols = 16
    fils = 16
    difficulty = 1
    bombs = ceil(difficulty*10**(log(cols)*log(fils)))
    mines.geometry(f"{BUTTONS_SIZE*cols}x{BUTTONS_SIZE*fils + STATS_HEIGHT}+{(get_monitors()[0].width - BUTTONS_SIZE*cols)//2}+{(get_monitors()[0].height - (BUTTONS_SIZE*fils + STATS_HEIGHT))//2}")
    mines.resizable(True, True)

    stats = Frame(master=mines, height=STATS_HEIGHT)
    stats.grid(column=0, row=0)

    matrix = Frame(master=mines)
    matrix.grid(column=0, row=1)

    BOMB_TICK = ImageTk.PhotoImage(Image.open("bomb_tick.png").resize((IMG_SCALE,IMG_SCALE), Image.ANTIALIAS))
    BOMB_BOOM = ImageTk.PhotoImage(Image.open("bomb_boom.png").resize((IMG_SCALE,IMG_SCALE), Image.ANTIALIAS))
    RED_FLAG = ImageTk.PhotoImage(Image.open("red_flag.png").resize((IMG_SCALE,IMG_SCALE), Image.ANTIALIAS))
    FONT = font.Font(family="Helvetica", size=7, weight='bold')
    RESET_ALL = Button(stats, text="Reset Settings", command=lambda:print("Settings reset..."))
    RESET_ALL.pack(side=LEFT)
    RESET_GAME = Button(stats, text="Start New Game", command=lambda:print("Starting new game..."))
    RESET_GAME.pack(side=RIGHT)
    caches = [{}]
    buttons = [[unBoton(fils=fil, cols=col, x=cols, y=fils, butt=Button(master=matrix)) for col in range(cols)] for fil in range(fils)]
    Buttons = Botones(buttons, caches)

    for row in Buttons.buttons:
        for button in row:
            button.parent = Buttons
            button.butt.bind("<Button-3>", right_click)

    while bombs != 0:
        x,y = r(0,cols-1),r(0,fils-1)
        if Buttons.buttons[y][x].mines == 0:
            Buttons.buttons[y][x].mines = 1
            bombs -= 1

    for fil in range(fils):
        for col in range(cols):
            Buttons.buttons[fil][col].bombs_count()
            Buttons.buttons[fil][col].butt.grid(column=col, row=fil+1)

    mines.mainloop()

if __name__ == "__main__":
    StartGame()