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
    "password"  : ""
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

def whenClosed():
    conn.close()
    display.destroy()

display = tkinter.Tk()
display.geometry('500x250')

background = tkinter.PhotoImage(file="pokemonLogo.gif") #background
bgimg = Label(display, i=background)
bgimg.pack()

titleLabel = Label(display, text = 'Welcome to the Pokedex API! Click a button.', width = 35, height = 1)
titleLabel.place(x=125, y= 20)
col = ["name","capture_rate", "height", "weight"]
pokemon = postgresql_to_dataframe(conn, "select name,capture_rate,height,weight from pokemon", col)

def openHeightWeightScreen():
    #screen = Toplevel(display)
    #screen.title("Height-Weight Scatter Plot")
    #screen.geometry('750x375')
    #Label(screen, text = "Height-Weight Scatter Plot").pack()
    #insert graph or image of graph here
    plt.scatter(pokemon['height'],pokemon['weight'])
    plt.xlabel("height")
    plt.ylabel("weight")
    plt.title("Scatter plot of Height VS Weight")
    plt.show()

def openMoveTypeScreen():
    #screen = Toplevel(display)
    #screen.title("Move Type Bar Graph")
    #screen.geometry('750x375')
    #Label(screen, text = "Move Type Bar Graph").pack()
    #insert graph or image of graph here
    moves = postgresql_to_dataframe(conn, '''SELECT types.type_name, x.num
                                            FROM (SELECT types.type_id as id,count(*) as num 
                                                FROM moves, types
                                                WHERE types.type_id = moves.type_id
                                                GROUP BY types.type_id) as x, types
                                            WHERE types.type_id = x.id
                                            ORDER BY types.type_id''', ["type_name","count"])
    fig = plt.figure(figsize = (20, 5))
    plt.bar(moves['type_name'],moves['count'], width = 0.6)
    plt.xlabel("type")
    plt.ylabel("number of move")
    plt.title("number of move in each type")
    plt.show()

def openPokemonTypeScreen():
    #screen = Toplevel(display)
    #screen.title("Pokemon Type Bar Graph")
    #screen.geometry('750x375')
    #Label(screen, text = "Pokemon Type Bar Graph").pack()
    #insert graph or image of graph here
    types = postgresql_to_dataframe(conn, '''SELECT types.type_name, x.num
                                            FROM (SELECT types.type_id as id,count(*) as num 
                                                FROM types, hastype
                                                WHERE types.type_id = hastype.type_id
                                                GROUP BY types.type_id) as x, types
                                            WHERE types.type_id = x.id
                                            ORDER BY types.type_id''', ["type_name","count"])
    fig = plt.figure(figsize = (20, 5))
    plt.bar(types['type_name'],types['count'], width = 0.6)
    plt.xlabel("type")
    plt.ylabel("number of pokemon")
    plt.title("number of pokemon in each type")
    plt.show()

def CaptureRateWeightScreen():
    #screen = Toplevel(display)
    #screen.title("Capture Rate vs Weight Scatter Plot")
    #screen.geometry('750x375')
    #Label(screen, text = "Capture Rate vs Weight Scatter Plot").pack()
    #insert graph or image of graph here
    #capture rate and weight scatter plot
    plt.scatter(pokemon['capture_rate'],pokemon['weight'])
    plt.xlabel("capture rate")
    plt.ylabel("weight")
    plt.title("Scatter plot of capture rate VS Weight")
    plt.show()

def NumMovesScreen():
    #screen = Toplevel(display)
    #screen.title("Number of Learnable Moves")
    #screen.geometry('750x375')
    #Label(screen, text = "Number of Learnable Moves").pack()
    #insert graph or image of graph here
    move_per_pokemon = postgresql_to_dataframe(conn, '''SELECT pokemon.pokedex_number, x.num
                                                    FROM (SELECT pokemon.pokedex_number as id,count(*) as num 
                                                                FROM pokemon, (SELECT DISTINCT movepool.pokedex_number,
                                                                            movepool.move_id 
                                                                            FROM movepool) as m1
                                                                WHERE pokemon.pokedex_number = m1.pokedex_number
                                                                GROUP BY pokemon.pokedex_number) as x, pokemon
                                                            WHERE x.id = pokemon.pokedex_number
                                                            ORDER BY x.id''', ["pokedex_number","count"])

    #histogram for pokemon move
    fig, axs = plt.subplots(1, 1, figsize = (10,7), tight_layout = True)
    axs.hist(move_per_pokemon['count'],bins = 30)
    plt.xlabel("number of move")
    plt.ylabel("number of pokemon")
    plt.title("number of moves that pokemon can learn")
    plt.show()

def CaptureRateHeightScreen():
    #screen = Toplevel(display)
    #screen.title("Capture Rate vs Height Scatter Plot")
    #screen.geometry('750x375')
    #Label(screen, text = "Capture Rate vs Height Scatter Plot").pack()
    #insert graph or image of graph here
    plt.scatter(pokemon['capture_rate'],pokemon['height'])
    plt.xlabel("capture rate")
    plt.ylabel("height")
    plt.title("Scatter plot of capture rate VS height")
    plt.show()

heightWeightButton = Button(display, text="Height-Weight Comparison", command = openHeightWeightScreen, width = 25, height = 1)
heightWeightButton.place(x=15, y=50)

MoveTypeButton = Button(display, text="Move Type Analysis", command = openMoveTypeScreen, width = 25, height = 1)
MoveTypeButton.place(x=15, y=100)

PokemonTypeButton = Button(display, text="Pokemon Type Analysis", command = openPokemonTypeScreen, width = 25, height = 1)
PokemonTypeButton.place(x=15, y=150)

captureRateWeightButton = Button(display, text="Capture Rate vs Weight Plot", command = CaptureRateWeightScreen, width = 25, height = 1)
captureRateWeightButton.place(x=300, y=50)

captureRateHeightButton = Button(display, text="Capture Rate vs Height Plot", command = CaptureRateHeightScreen, width = 25, height = 1)
captureRateHeightButton.place(x=300, y=100)

NumMovesButton = Button(display, text="Number of Learnable Moves", command = NumMovesScreen, width = 25, height = 1)
NumMovesButton.place(x=300, y=150)

display.protocol("WM_DELETE_WINDOW", whenClosed)
display.mainloop()
