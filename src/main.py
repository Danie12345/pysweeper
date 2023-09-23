# -*- coding: utf-8 -*-
"""
Created on Wed Oct 23 00:13:29 2019

@author: daniel
"""

# pysweeper

import os
import sys
from tkinter import Button, Tk, Label, Frame, font, LEFT, RIGHT
from PIL import ImageTk, Image
from random import randint as r
from screeninfo import get_monitors
from math import log10 as log
from math import ceil
from botones import Botones, unBoton
from events import nohover, right_click, mouse_wheel_click

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
        self.Buttons = None
        self.matrix.destroy()
        self.SetSettings(cols=self.cols, fils=self.fils, difficulty=self.difficulty, bombs=self.bombs, resizable=self.mines.resizable())
        self.GenerateButtonGrid()

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
        self.Buttons = Botones([[]], [])
        caches = [{}]
        buttons = [[
                unBoton(
                    fils=fil, cols=col, x=self.cols, y=self.fils, butt=Button(master=self.matrix),
                    PARAMS = {
                        'NUM_COLORS': NUM_COLORS, 
                        'get_rgb': get_rgb, 
                        'BOMB_TICK': self.BOMB_TICK,
                        'BOMB_BOOM': self.BOMB_BOOM,
                        'RED_FLAG': self.RED_FLAG,
                        'FONT': self.FONT,
                        'RESET_ALL': self.RESET_ALL,
                        'RESET_GAME': self.RESET_GAME
                    }
                ) for col in range(self.cols)
            ] for fil in range(self.fils)
        ]
        self.Buttons = Botones(buttons, caches)
        for row in self.Buttons.buttons:
            for button in row:
                button.parent = self.Buttons
                button.butt.bind("<Button-3>", lambda event: right_click(event, image=self.RED_FLAG))
                button.butt.bind("<Button-2>", lambda event: mouse_wheel_click(event, image=self.BOMB_TICK))
        while self.bombs != 0:
            x,y = r(0,self.cols-1),r(0,self.fils-1)
            if self.Buttons.buttons[y][x].mines == 0:
                self.Buttons.buttons[y][x].mines = 1
                self.bombs -= 1
        for fil in range(self.fils):
            for col in range(self.cols):
                self.Buttons.buttons[fil][col].bombs_count()
                self.Buttons.buttons[fil][col].butt.grid(column=col, row=fil+1)

    def SetSettings(self, cols=16, fils=16, difficulty=1, bombs=None, resizable=(False, False)):
        self.cols = 16
        self.fils = 16
        self.difficulty = 1
        self.bombs = ceil(self.difficulty*10**(log(self.cols)*log(self.fils))) if bombs == None else bombs
        self.mines.geometry(f"{BUTTONS_SIZE*self.cols}x{BUTTONS_SIZE*self.fils + STATS_HEIGHT}+{(get_monitors()[0].width - BUTTONS_SIZE*self.cols)//2}+{(get_monitors()[0].height - (BUTTONS_SIZE*self.fils + STATS_HEIGHT))//2}")
        self.mines.resizable(*resizable)

        self.stats = Frame(master=self.mines, height=STATS_HEIGHT)
        self.stats.grid(column=0, row=0)

        self.matrix = Frame(master=self.mines)
        self.matrix.grid(column=0, row=1)
        
        return self.GenerateCONSTANTS()
    
    def GenerateGame(self, ):
        self.SetSettings()
        self.GenerateButtonGrid()
        
    def StartGame(self, ):
        self.GenerateGame()
        self.mines.mainloop()





if __name__ == "__main__":
    game = Game()
    game.StartGame()