import tkinter
from tkinter import *
import tkinter.messagebox

display = tkinter.Tk()
display.geometry('500x250')

background = tkinter.PhotoImage(file="pokemonLogo.gif") #give it a better color later
bgimg = Label(display, i=background)
bgimg.img_ref = background
bgimg.pack()

titleLabel = Label(display, text = 'Welcome to the Pokedex API! Click a button.', width = 100, height = 75)
titleLabel.pack()

def func(): tkinter.messagebox.showinfo("Button was clicked") #display graph here
enterButton = Button(display, text= "Enter", width = 12, height = 5, command=func)
enterButton.place(x=180, y= 125)

display.mainloop()