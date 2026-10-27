import json
from database import necessite_bd

from connexion import get_connection

def dic_ustensiles():
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT id_ustensile, nom_ustensile FROM ustensile")
    rows = cur.fetchall()
    cur.close()
    conn.close()
    return {nom.lower(): id_ust for id_ust, nom in rows}

def dic_recettes():
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT id_recette, nom_recette FROM recette")
    rows = cur.fetchall()
    cur.close()
    conn.close()
    return {nom.lower(): id_rec for id_rec, nom in rows}

def inserer_necessite(id_ustensile, id_recette):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("""
        INSERT INTO necessite (id_ustensile, id_recette)
        VALUES (%s, %s)
        ON CONFLICT (id_ustensile, id_recette) DO NOTHING
    """, (id_ustensile, id_recette))
    conn.commit()
    cur.close()
    conn.close()

    
def insert_necessite():
    with open("data/necessite.json", "r", encoding="utf-8") as f:
        liaisons = json.load(f)

    for lien in liaisons:
        necessite_bd.inserer_necessite(
            lien["id_ustensile"],
            lien["id_recette"]
        )


