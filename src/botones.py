from tkinter import Button, Tk, Label, Frame, font, DISABLED, NORMAL, CENTER, LEFT, RIGHT

class Botones:
    def __init__(self, buttons, caches):
        self.buttons = buttons
        self.caches = caches

class unBoton:
    def __init__(self, fils=1, cols=1, x=1, y=1, butt=None, PARAMS={}):
        self.fils = fils
        self.cols = cols
        self.clicks = 0
        self.x = x
        self.y = y
        self.pressedType = "None"
        self.bombs_around = 0
        self.shown = False
        self.params = PARAMS
        
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
                                label = Label(button.butt, image=self.params['BOMB_BOOM'], anchor=CENTER)
                                label.pack()
                        button.butt['state'] = DISABLED
            else:
                if self.bombs_around == 0:
                    self.discover()
                else:
                    self.text = f" {self.bombs_around} "
                    caches[-1][self.fils, self.cols] = buttons[self.fils][self.cols].bombs_around
                    label = Label(self.butt, text=self.text if self.text != " 0 " else "     ", font=self.params['FONT'], bg=self.params['get_rgb']((240,240,240)), fg=self.params['NUM_COLORS'][self.bombs_around], anchor=CENTER)
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