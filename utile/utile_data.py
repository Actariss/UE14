import sqlite3

DB = "../cli_panoptes/data/cli_panoptes.sqlite"


def connect_db(db_filename=DB):
    sqlite_connection = None
    try:
        sqlite_connection = sqlite3.connect(db_filename, check_same_thread=False)
    except sqlite3.Error as error:
        print("Failed to connect database", db_filename, error)
    finally:
        if sqlite_connection:
            return sqlite_connection


def select_db(db_conn : sqlite3.Connection, query: str, parameters: tuple):
    curseur = db_conn.cursor()
    liste = []
    for iteration in curseur.execute(query, parameters):
        liste.append(iteration)
    return liste


def simple_insert_db(db_conn : sqlite3.Connection, query: str, parameters: tuple):
    cur = db_conn.cursor()
    try:
        cur.execute(query, parameters)
        db_conn.commit()

    except sqlite3.Error as error:
        print("Echec de l'insertion", error)
    else:
        print("Insertion réussie")


def alter_table_db(db_conn : sqlite3.Connection, query: str, parameters: tuple):
    curseur = db_conn.cursor()
    try:
        curseur.execute(query, parameters)
    except sqlite3.Error as error:
        print("Echec de la modification de table", error)
    else:
        print("Modification réussie")
        db_conn.commit()


def drop_table_db(db_conn : sqlite3.Connection, query: str, parameters: tuple):
    curseur = db_conn.cursor()
    try:
        curseur.execute(query, parameters)
    except sqlite3.Error as error:
        print("Echec de la supression de table", error)
    else:
        print("Supression réussie")
        db_conn.commit()


def update_db(db_conn : sqlite3.Connection, query: str, parameters: tuple):

    curseur = db_conn.cursor()
    try:
        curseur.execute(query, parameters)
    except sqlite3.Error as error:
        print("Echec de la modification de table", error)
    else:
        print("SModification réussie")
        db_conn.commit()


def delete_from_db(db_conn : sqlite3.Connection, query: str, parameters: tuple):
    curseur = db_conn.cursor()
    try:
        curseur.execute(query, parameters)
    except sqlite3.Error as error:
        print("Echec de la supression de tuples", error)
    else:
        print("Supression réussie")
        db_conn.commit()


def insert_db(table: str, my_dict: any):
    # dict = paire collone/valeurs
    connection = connect_db()
    curseur = connection.cursor()
    try:
        columns = ', '.join(my_dict.keys())
        placeholders = ':' + ', :'.join(my_dict.keys())
        query = f'INSERT INTO {table} (%s) VALUES (%s)' % (columns, placeholders)
        curseur.execute(query, my_dict)
        connection.commit()
        connection.close()
    except sqlite3.Error as error:
        print("Echec de l'insertion", error)




# print(select_db("../cli_panoptes/data/cli_panoptes.sqlite", "SELECT * FROM sa_sets"))
# alter_table_db("../cli_panoptes/data/cli_panoptes.sqlite", "ALTER TABLE fim_rules add BONJOUR VARCHAR(30)")
# alter_table_db("../cli_panoptes/data/cli_panoptes.sqlite", "ALTER TABLE fim_rules drop column BONJOUR")
# update_db("../cli_panoptes/data/cli_panoptes.sqlite", "UPDATE sa_sets set sa_set_name = 'OUIIII' where schedule = 19")
# delete_from_db("../cli_panoptes/data/cli_panoptes.sqlite", "DELETE FROM sa_sets")
