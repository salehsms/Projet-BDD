import psycopg2
import os


os.environ["PGCLIENTENCODING"] = "UTF8"


conn = psycopg2.connect(
    dbname="recette",
    user="postgres",
    password="123456789",
    host="localhost",
    port="5432",
    options="-c client_encoding=UTF8"
)


def inserer_menu(id_menu, nom_menu):
    cur = conn.cursor()
    cur.execute("""
        INSERT INTO Menu (id_menu, nom_menu)
        VALUES (%s, %s)
        ON CONFLICT (id_menu) DO NOTHING
    """, (id_menu, nom_menu))
    conn.commit()
    cur.close()

   