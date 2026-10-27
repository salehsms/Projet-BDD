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

def dic_recettes():
    cur = conn.cursor()
    cur.execute("SELECT id_recette, nom_recette FROM Recette")
    rows = cur.fetchall()
    cur.close()
    return {nom.lower(): id_rec for id_rec, nom in rows}

def inserer_etape(id_etape, id_recette, numero_ordre, description):
    cur = conn.cursor()
    cur.execute("""
        INSERT INTO Etape (id_etape, id_recette, numero_ordre, descrption_etape)
        VALUES (%s, %s, %s, %s)
        ON CONFLICT (id_etape) DO NOTHING
    """, (id_etape, id_recette, numero_ordre, description))
    conn.commit()
    cur.close()