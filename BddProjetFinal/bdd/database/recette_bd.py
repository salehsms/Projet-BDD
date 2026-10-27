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

def dic_categories():
    cur = conn.cursor()

    cur.execute("SELECT id_categorie, nom_catgorie FROM Categorie")
    rows = cur.fetchall()


    categories = {}

    for row in rows:
        id_cat, nom_cat = row
        categories[nom_cat.lower()] = id_cat
    
    return categories

def inserer_recette(id_recette, id_categorie, nom, description, temps_prep, temps_cuisson, date_creation):
    cur = conn.cursor()
    cur.execute("""
        INSERT INTO Recette (id_recette, id_categorie, nom_recette, description_, temps_preparation, temps_cuisson, date_creation)
        VALUES (%s, %s, %s, %s, %s, %s, %s)
        ON CONFLICT (id_recette) DO NOTHING
    """, (id_recette, id_categorie, nom, description, temps_prep, temps_cuisson, date_creation))
    conn.commit()
    cur.close()
    
def dic_recettes():
   
    cur = conn.cursor()
    cur.execute("SELECT id_recette, nom_recette FROM Recette")
    rows = cur.fetchall()
    cur.close()
    return {nom.lower(): id_rec for id_rec, nom in rows}
    
#conn.commit()


    