# -*- coding: utf-8 -*-
"""
Created on Wed Oct 23 00:13:29 2019

@author: daniel
"""

# pysweeper

import os
import sys
from tkinter import Button, Tk, Label, Frame, font, DISABLED, NORMAL, CENTER, LEFT, RIGHT
from PIL import ImageTk, Image
from random import randint as r
from screeninfo import get_monitors
from math import log10 as log
from math import ceil

def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)

try:
    import iconpath
    path = 'src\\assets\\fave.ico'
except:
    path = 'assets\\fave.ico'


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

class Game:
    def __init__(self):
        self.mines = self.GenerateWindow()

    def GenerateWindow(self, ):
        root = Tk()
        root.title('Pysweeper')
        root.resizable(False, False)
        self.im = Image.open(resource_path(path))
        self.photo = ImageTk.PhotoImage(self.im)
        root.wm_iconphoto(True, self.photo)
        self.WINDOW_HEIGHT = 350
        self.WINDOW_WIDTH = 500
        self.screen_width = root.winfo_screenwidth()
        self.screen_height = root.winfo_screenheight()
        self.x_cordinate = int((self.screen_width/2) - (self.WINDOW_WIDTH/2))
        self.y_cordinate = int((self.screen_height/2) - (self.WINDOW_HEIGHT/2))
        root.geometry("{}x{}+{}+{}".format(self.WINDOW_WIDTH, self.WINDOW_HEIGHT, self.x_cordinate, self.y_cordinate))
        self.PAD_X = 25
        self.PAD_Y = 25
        return root

    def RestartGame(self, ):
        pass

    def GenerateCONSTANTS(self,):
        self.BOMB_TICK = ImageTk.PhotoImage(Image.open("src\\assets\\bomb_tick.png").resize((IMG_SCALE,IMG_SCALE), Image.ANTIALIAS))
        self.BOMB_BOOM = ImageTk.PhotoImage(Image.open("src\\assets\\bomb_boom.png").resize((IMG_SCALE,IMG_SCALE), Image.ANTIALIAS))
        self.RED_FLAG = ImageTk.PhotoImage(Image.open("src\\assets\\red_flag.png").resize((IMG_SCALE,IMG_SCALE), Image.ANTIALIAS))
        self.FONT = font.Font(family="Helvetica", size=7, weight='bold')
        self.RESET_ALL = Button(self.stats, text="Reset Settings", command=lambda: print("Settings reset..."))
        self.RESET_ALL.pack(side=LEFT)
        self.RESET_GAME = Button(self.stats, text="Start New Game", command=lambda: self.RestartGame())
        self.RESET_GAME.pack(side=RIGHT)
        return self.BOMB_TICK, self.BOMB_BOOM, self.RED_FLAG, self.FONT, self.RESET_ALL, self.RESET_GAME

    def GenerateButtonGrid(self, ):
        caches = [{}]
        buttons = [[unBoton(fils=fil, cols=col, x=self.cols, y=self.fils, butt=Button(master=self.matrix)) for col in range(self.cols)] for fil in range(self.fils)]
        self.Buttons = Botones(buttons, caches)
        for row in self.Buttons.buttons:
            for button in row:
                button.parent = self.Buttons
                button.butt.bind("<Button-3>", right_click)
        while self.bombs != 0:
            x,y = r(0,self.cols-1),r(0,self.fils-1)
            if self.Buttons.buttons[y][x].mines == 0:
                self.Buttons.buttons[y][x].mines = 1
                self.bombs -= 1
        for fil in range(self.fils):
            for col in range(self.cols):
                self.Buttons.buttons[fil][col].bombs_count()
                self.Buttons.buttons[fil][col].butt.grid(column=col, row=fil+1)

    def SetSettings(self, cols=16, fils=16, difficulty=1, bombs=None, ):
        self.cols = 16
        self.fils = 16
        self.difficulty = 1
        self.bombs = ceil(self.difficulty*10**(log(self.cols)*log(self.fils))) if bombs == None else bombs
        self.mines.geometry(f"{BUTTONS_SIZE*self.cols}x{BUTTONS_SIZE*self.fils + STATS_HEIGHT}+{(get_monitors()[0].width - BUTTONS_SIZE*self.cols)//2}+{(get_monitors()[0].height - (BUTTONS_SIZE*self.fils + STATS_HEIGHT))//2}")
        self.mines.resizable(True, True)

        self.stats = Frame(master=self.mines, height=STATS_HEIGHT)
        self.stats.grid(column=0, row=0)

        self.matrix = Frame(master=self.mines)
        self.matrix.grid(column=0, row=1)
        
        return self.GenerateCONSTANTS()
        

    def StartGame(self, ):
        global BOMB_TICK, BOMB_BOOM, RED_FLAG, FONT, RESET_ALL, RESET_GAME
        
        BOMB_TICK, BOMB_BOOM, RED_FLAG, FONT, RESET_ALL, RESET_GAME = self.SetSettings()

        self.GenerateButtonGrid()

        self.mines.mainloop()





if __name__ == "__main__":
    game = Game()
    game.StartGame()