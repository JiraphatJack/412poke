import tkinter
from tkinter import *
import tkinter.messagebox

display = tkinter.Tk()
display.geometry('500x250')

background = tkinter.PhotoImage(file="pokemonLogo.gif") #background
bgimg = Label(display, i=background)
bgimg.pack()

titleLabel = Label(display, text = 'Welcome to the Pokedex API! Click a button.', width = 35, height = 1)
titleLabel.place(x=125, y= 50)

def func(): tkinter.messagebox.showinfo("Button was clicked") #display graph here
enterButton = Button(display, text= "Enter", width = 5, height = 2, command=func)
enterButton.place(x=228, y= 100)

display.mainloop()