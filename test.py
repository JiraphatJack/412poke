import sys
import psycopg2 
import psycopg2.extras
import pandas as pd
import matplotlib.pyplot as plt
param_dic = {
    "host"      : "localhost",
    "database"  : "postgres",
    "user"      : "postgres",
    "password"  : "qwer"
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

#height and weight scatter plot
col = ["name","capture_rate", "height", "weight"]
pokemon = postgresql_to_dataframe(conn, "select name,capture_rate,height,weight from pokemon", col)
print(pokemon)
plt.scatter(pokemon['height'],pokemon['weight'])
plt.xlabel("height")
plt.ylabel("weight")
plt.title("Scatter plot of Height VS Weight")
plt.show()

#capture rate and weight scatter plot
plt.scatter(pokemon['capture_rate'],pokemon['weight'])
plt.xlabel("capture rate")
plt.ylabel("weight")
plt.title("Scatter plot of capture rate VS Weight")
plt.show()

#capture rate and height scatter plot
plt.scatter(pokemon['capture_rate'],pokemon['height'])
plt.xlabel("capture rate")
plt.ylabel("height")
plt.title("Scatter plot of capture rate VS height")
plt.show()

#pokemon types bar plot
types = postgresql_to_dataframe(conn, '''SELECT types.type_name, x.num
                                            FROM (SELECT types.type_id as id,count(*) as num 
                                                FROM types, hastype
                                                WHERE types.type_id = hastype.type_id
                                                GROUP BY types.type_id) as x, types
                                            WHERE types.type_id = x.id
                                            ORDER BY types.type_id''', ["type_name","count"])

print(types)
fig = plt.figure(figsize = (20, 5))
plt.bar(types['type_name'],types['count'], width = 0.6)
plt.xlabel("type")
plt.ylabel("number of pokemon")
plt.title("number of pokemon in each type")
plt.show()

#move types bar plot
moves = postgresql_to_dataframe(conn, '''SELECT types.type_name, x.num
                                            FROM (SELECT types.type_id as id,count(*) as num 
                                                FROM moves, types
                                                WHERE types.type_id = moves.type_id
                                                GROUP BY types.type_id) as x, types
                                            WHERE types.type_id = x.id
                                            ORDER BY types.type_id''', ["type_name","count"])

print(moves)
fig = plt.figure(figsize = (20, 5))
plt.bar(moves['type_name'],moves['count'], width = 0.6)
plt.xlabel("type")
plt.ylabel("number of move")
plt.title("number of move in each type")
plt.show()

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

"""i = 0
while i < move_per_pokemon.shape[0]:
    s = i
    i += 30
    plt.bar(move_per_pokemon['pokedex_number'][s:i],move_per_pokemon['count'][s:i], width = 0.6)
    plt.show()"""

"""
fig, axs = plt.subplots(1, 1, figsize = (10,7), tight_layout = True)

axs.hist(pokemon['capture_rate'],bins = 30)

plt.show()
"""

conn.close()