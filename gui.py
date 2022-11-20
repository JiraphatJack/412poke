import tkinter
from tkinter import *
import tkinter.messagebox

display = tkinter.Tk()
display.geometry('500x250')

background = tkinter.PhotoImage(file="pokemonLogo.gif") #background
bgimg = Label(display, i=background)
bgimg.pack()

titleLabel = Label(display, text = 'Welcome to the Pokedex API! Click a button.', width = 35, height = 1)
titleLabel.place(x=250, y= 20)

def openHeightWeightScreen():
    screen = Toplevel(display)
    screen.title("Height-Weight Scatter Plot")
    screen.geometry('750x375')
    Label(screen, text = "Height-Weight Scatter Plot").pack()
    #insert graph or image of graph here
def openMoveTypeScreen():
    screen = Toplevel(display)
    screen.title("Move Type Bar Graph")
    screen.geometry('750x375')
    Label(screen, text = "Move Type Bar Graph").pack()
    #insert graph or image of graph here

def openPokemonTypeScreen():
    screen = Toplevel(display)
    screen.title("Pokemon Type Bar Graph")
    screen.geometry('750x375')
    Label(screen, text = "Pokemon Type Bar Graph").pack()
    #insert graph or image of graph here

def CaptureRateWeightTypeScreen():
    screen = Toplevel(display)
    screen.title("Capture Rate vs Weight Scatter Plot")
    screen.geometry('750x375')
    Label(screen, text = "Capture Rate vs Weight Scatter Plot").pack()
    #insert graph or image of graph here

def CaptureRateWeightScreen():
    screen = Toplevel(display)
    screen.title("Capture Rate vs Weight Scatter Plot")
    screen.geometry('750x375')
    Label(screen, text = "Capture Rate vs Weight Scatter Plot").pack()
    #insert graph or image of graph here

def NumMovesScreen():
    screen = Toplevel(display)
    screen.title("Number of Learnable Moves")
    screen.geometry('750x375')
    Label(screen, text = "Number of Learnable Moves").pack()
    #insert graph or image of graph here

def NumMovesScreen():
    screen = Toplevel(display)
    screen.title("Number of Learnable Moves")
    screen.geometry('750x375')
    Label(screen, text = "Number of Learnable Moves").pack()
    #insert graph or image of graph here

def CaptureRateHeightScreen():
    screen = Toplevel(display)
    screen.title("Capture Rate vs Height Scatter Plot")
    screen.geometry('750x375')
    Label(screen, text = "Capture Rate vs Height Scatter Plot").pack()
    #insert graph or image of graph here

heightWeightButton = Button(display, text="Height-Weight Comparison", command = openHeightWeightScreen)
heightWeightButton.place(x=20, y=50)

MoveTypeButton = Button(display, text="Move Type Analysis", command = openMoveTypeScreen)
MoveTypeButton.place(x=20, y=100)

PokemonTypeButton = Button(display, text="Pokemon Type Analysis", command = openPokemonTypeScreen)
PokemonTypeButton.place(x=20, y=150)

captureRateWeightButton = Button(display, text="Capture Rate vs Weight Scatter Plot", command = CaptureRateWeightScreen)
captureRateWeightButton.place(x=225, y=50)

captureRateHeightButton = Button(display, text="Capture Rate vs Height Scatter Plot", command = CaptureRateHeightScreen)
captureRateHeightButton.place(x=225, y=100)

NumMovesButton = Button(display, text="Number of Learnable Moves", command = NumMovesScreen)
NumMovesButton.place(x=225, y=150)

display.mainloop()
