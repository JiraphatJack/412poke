import tkinter
from tkinter import *
import tkinter.messagebox
import sys
import psycopg2 
import psycopg2.extras
import pandas as pd
import matplotlib.pyplot as plt

param_dic = {
    "host"      : "localhost",
    "database"  : "postgres",
    "user"      : "postgres",
    "password"  : "WasNotNaka:("
}
port_id = 5432

#create a connection#

def connect(params_dic):
    conn = None
    try:
        print('Connecting to database')
        conn = psycopg2.connect(**params_dic)
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
        sys.exit(1)
    
    print('Successful')
    return conn

#convert result from query to pandas dataframe
def postgresql_to_dataframe(conn, select_querry, column_names):
    cur = conn.cursor()
    try:
        cur.execute(select_querry)
    except (Exception, psycopg2.DatabaseError) as error:
        print('Error: %s', error)
        cur.close()
        return 1
    
    tupples = cur.fetchall()
    cur.close()
    
    # We just need to turn it into a pandas dataframe
    df = pd.DataFrame(tupples, columns=column_names)
    return df


conn = connect(param_dic)
# Execute the "SELECT *" query

display = tkinter.Tk()
display.geometry('500x250')

#background = tkinter.PhotoImage(file="pokemonLogo.gif") #background
#bgimg = Label(display, i=background)
#bgimg.pack()

titleLabel = Label(display, text = 'Welcome to the Pokedex API! Click a button.', width = 35, height = 1)
titleLabel.place(x=250, y= 20)

def openHeightWeightScreen():
    screen = Toplevel(display)
    screen.title("Height-Weight Scatter Plot")
    screen.geometry('750x375')
    Label(screen, text = "Height-Weight Scatter Plot").pack()
    #insert graph or image of graph here
    col = ["name","capture_rate", "height", "weight"]
    pokemon = postgresql_to_dataframe(conn, "select name,capture_rate,height,weight from pokemon", col)
    print(pokemon)
    plt.scatter(pokemon['height'],pokemon['weight'])
    plt.xlabel("height")
    plt.ylabel("weight")
    plt.title("Scatter plot of Height VS Weight")
    plt.show()

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

def CaptureRateWeightScreen():
    screen = Toplevel(display)
    screen.title("Capture Rate vs Weight Scatter Plot")
    screen.geometry('750x375')
    Label(screen, text = "Capture Rate vs Weight Scatter Plot").pack()
    #insert graph or image of graph here
    #capture rate and weight scatter plot
    plt.scatter(pokemon['capture_rate'],pokemon['weight'])
    plt.xlabel("capture rate")
    plt.ylabel("weight")
    plt.title("Scatter plot of capture rate VS Weight")
    plt.show()

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
