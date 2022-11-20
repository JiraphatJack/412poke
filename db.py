import psycopg2
import sys

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
        conn.autocommit = True
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
        sys.exit(1)
    
    print('Successful')
    return conn

def build_db(conn):
    cur = conn.cursor()
    try:
        cur.execute("DROP TABLE IF EXISTS pokemon CASCADE")
        cur.execute("DROP TABLE IF EXISTS pokemon_move_methods CASCADE")
        cur.execute("DROP TABLE IF EXISTS types CASCADE")
        cur.execute("DROP TABLE IF EXISTS hasType CASCADE")
        cur.execute("DROP TABLE IF EXISTS moves CASCADE")
        cur.execute("DROP TABLE IF EXISTS movepool CASCADE")
        cur.execute("DROP TABLE IF EXISTS versions CASCADE")
        cur.execute("DROP TABLE IF EXISTS pokemon_species CASCADE")



        cur.execute('''CREATE table pokemon(pokedex_number SERIAL UNIQUE NOT NULL,
                                                name varchar(45),
                                                capture_rate integer,
                                                height integer,
                                                weight integer,
                                                region_name varchar(10),
                                                PRIMARY KEY(pokedex_number))''')
        with open(r'pokemon.csv', 'r') as f:
            next(f)
            cur.copy_from(f, 'pokemon', sep=',')
        f.close()

        cur.execute('''CREATE table pokemon_move_methods(id SERIAL UNIQUE NOT NULL,
                                                            name varchar(25),
                                                            PRIMARY KEY(id));''')

        with open(r'pokemon_move_methods.csv', 'r') as f:
            next(f)
            cur.copy_from(f, 'pokemon_move_methods', sep=',')
        f.close()

        cur.execute('''CREATE table types(type_id integer,
                                            type_name varchar(15),
                                            PRIMARY KEY(type_id));''')

        with open(r'types.csv', 'r') as f:
            next(f)
            cur.copy_from(f, 'types', sep=',')
        f.close()

        cur.execute('''CREATE table hastype(
                                pokedex_number integer,
                                type_id integer,
                                slot integer,
                                PRIMARY KEY(pokedex_number, type_id),
                                FOREIGN KEY(pokedex_number) REFERENCES pokemon(pokedex_number),
                                FOREIGN KEY(type_id) REFERENCES types(type_id))''')

        with open(r'pokemon_types.csv', 'r') as f:
            next(f)
            cur.copy_from(f, 'hastype', sep=',')
        f.close()

        
        cur.execute('''CREATE table moves(
                        move_id SERIAL UNIQUE NOT NULL,
                        move_name varchar(75),
                        type_id integer,
                        PRIMARY KEY(move_id),
                        FOREIGN KEY(type_id) REFERENCES types(type_id));''')

        with open(r'moves.csv', 'r') as f:
            next(f)
            cur.copy_from(f, 'moves', sep=',')
        f.close()

        cur.execute('''CREATE table versions(
                            id SERIAL UNIQUE NOT NULL,
                            version_id integer,
                            version_name varchar(25),
                            PRIMARY KEY(id));''')

        with open(r'versions.csv', 'r') as f:
            next(f)
            cur.copy_from(f, 'versions', sep=',')
        f.close()

        cur.execute('''CREATE table movepool(
                        movepool_id SERIAL UNIQUE NOT NULL,
                        pokedex_number integer,
                        version_id integer,
                        move_id integer,
                        move_method_id integer,
                        level_learned integer,
                        PRIMARY KEY(movepool_id),
                        FOREIGN KEY(pokedex_number) REFERENCES pokemon(pokedex_number),
                        FOREIGN KEY(version_id) REFERENCES versions(id),
                        FOREIGN KEY(move_id) REFERENCES moves(move_id),
                        FOREIGN KEY(move_method_id) REFERENCES pokemon_move_methods(id));''')

        with open(r'pokemon_movepools.csv', 'r') as f:
            next(f)
            cur.copy_from(f, 'movepool', sep=',')
        f.close()
        
        cur.execute('''CREATE TABLE pokemon_species(
                            pokedex_number integer,
                            generation_id integer,
                            evolves_from_species_id integer,
                            evolution_chain_id integer,
                            color_id integer,
                            shape_id integer,
                            gender_rate integer,
                            base_happiness integer,
                            hatch_counter integer,
                            growth_rate_id integer,
                            is_legendary boolean,
                            is_mythical boolean
        )''')
        with open(r'pokemon_species.csv', 'r') as f:
            next(f)
            cur.copy_from(f, 'pokemon_species', sep=',')
        f.close()

        cur.close()


    except (Exception, psycopg2.DatabaseError) as error:
        print('Error: %s', error)
        cur.close()
        return 1

conn = connect(param_dic)
build_db(conn)
conn.close()