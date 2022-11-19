import sys
import psycopg2 
import psycopg2.extras
import pandas as pd
import json
import requests
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
pokemon_column_names = ["pokedex_number", "name", "capture_rate", "height", "weight", "region_name"]
col = ["name"]
moves_column_names = ["move_id", "move_name", "type_id"]
move_pool_column_names = ["movepool_id", "pokedex_number", "version_id","move_id","move_method_id","level_learned"]
# Execute the "SELECT *" query
pokemon = postgresql_to_dataframe(conn, "select name from pokemon where capture_rate < 50", col)
moves = postgresql_to_dataframe(conn, "SELECT * from moves", moves_column_names)

print(pokemon)




conn.close()