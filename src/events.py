from tkinter import Button, Tk, Label, Frame, font, DISABLED, NORMAL, CENTER, LEFT, RIGHT
from typing import Any


class EventFunc:
    def __init__(self, func):
        self.func = func
    
    def __call__(self, *args: Any, **kwds: Any) -> Any:
        return self.func(*args, **kwds)


def nohoverEvent(event):
    pass

def right_clickEvent(event=None, image=''):
    label = Label(event.widget, image=image, anchor=CENTER)
    if event.widget.parent.clicks < 1:
        label.pack()
        event.pressedType = "FLAG"
        event.widget.parent.clicks += 1
        print ('flagged')
        event.widget['state'] = DISABLED
    else:
        for child in event.widget.winfo_children():
            child.destroy()
        # label.config(image='')
        event.widget.parent.clicks -= 1
        # event.pressedType = "None"
        event.widget['state'] = NORMAL
    event.widget.update()
    
def mouse_wheel_clickEvent(event=None, image=''):
    label = Label(event.widget, image=image, anchor=CENTER)
    label.pack()
    event.pressedType = "FLAG"
    event.widget['state'] = DISABLED
    event.widget.update()


nohover = EventFunc(nohoverEvent)
right_click = EventFunc(right_clickEvent)
mouse_wheel_click = EventFunc(mouse_wheel_clickEvent)