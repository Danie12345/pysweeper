from tkinter import *
from tkinter import font
from turtle import back

root = Tk()

text = Text(root)
text.insert(INSERT, "Hello, world!\n")
text.insert(END, "This is a phrase.\n")
text.insert(END, "Bye bye...")
text.pack(expand=1, fill=BOTH)

# adding a tag to a part of text specifying the indices
text.tag_add("recolor", "1.0")
text.tag_config("recolor",background="gray", foreground="yellow", font="Helvetica 14")

root.mainloop()



class MyApp():
    def __init__(self):
        self.root = Tk()
        l1 = Label(self.root, text="Hello")
        l2 = Label(self.root, text="World")
        l1.grid(row=0, column=0, padx=(0, 0))
        l2.grid(row=1, column=0, padx=(0, 0)) 

app = MyApp()
app.root.mainloop()