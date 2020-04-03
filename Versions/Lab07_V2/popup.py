#!/usr/bin/python3
from tkinter import *
from tkinter import messagebox as tkMessageBox

top = Tk()
def hello():
   tkMessageBox.showinfo("Say Hello", "Hello World")

B1 = Button(top, text = "Say Hello", command = hello)
B1.pack()

top.mainloop()
