# import sqlite3
#
#
# def connect_db():
#     db_filename = '../cli_panoptes/data/cli_panoptes.sqlite'
#     sqlite_connection = None
#     try:
#         sqlite_connection = sqlite3.connect(db_filename)
#     except sqlite3.Error as error:
#         print("Failed to connect database", db_filename, error)
#     finally:
#         if sqlite_connection:
#             return sqlite_connection
#
#
# def select_db(query):
#     curseur = connect_db().cursor()
#     liste = []
#     for iteration in curseur.execute(query):
#         liste.append(iteration)
#     return liste
#
#
# def insert_db(table, my_dict):
#     # dict = paire collone/valeurs
#     connection = connect_db()
#     curseur = connection.cursor()
#     try:
#         columns = ', '.join(my_dict.keys())
#         placeholders = ':' + ', :'.join(my_dict.keys())
#         query = f'INSERT INTO {table} (%s) VALUES (%s)' % (columns, placeholders)
#         curseur.execute(query, my_dict)
#         connection.commit()
#         connection.close()
#     except sqlite3.Error as error:
#         print("Echec de l'insertion", error)
#
#
# def insert_mais_plus_simple(query):
#     connexion = connect_db()
#     curseur = connexion.cursor()
#     try:
#         curseur.execute(query)
#         connexion.commit()
#     except sqlite3.Error as error:
#         print("Echec de l'insertion ", error)
#
#
# def alter_table_db(query):
#     connexion = connect_db()
#     curseur = connexion.cursor()
#     try:
#         curseur.execute(query)
#         connexion.commit()
#     except sqlite3.Error as error:
#         print("Echec de la modification de table", error)
#
#
# def drop_table_db(query):
#     connexion = connect_db()
#     curseur = connexion.cursor()
#     try:
#         curseur.execute(query)
#         connexion.commit()
#     except sqlite3.Error as error:
#         print("Echec de la supression de table", error)
#
#
# def update_db(query):
#     connexion = connect_db()
#     curseur = connexion.cursor()
#     try:
#         curseur.execute(query)
#         connexion.commit()
#     except sqlite3.Error as error:
#         print("Echec de la modification de table", error)
#
#
# def delete_from_db(query):
#     connexion = connect_db()
#     curseur = connexion.cursor()
#     try:
#         curseur.execute(query)
#         connexion.commit()
#     except sqlite3.Error as error:
#         print("Echec de la supression de tuples", error)
#
#
# def deconnect_db():
#     connect_db().close()