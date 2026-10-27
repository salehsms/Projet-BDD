import json
from connexion import get_connection

def dic_recettes():
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT id_recette, nom_recette FROM recette")
    rows = cur.fetchall()
    cur.close()
    conn.close()
    return {nom.lower(): id_rec for id_rec, nom in rows}

def dic_menus():
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT id_menu, nom_menu FROM menu")
    rows = cur.fetchall()
    cur.close()
    conn.close()
    return {nom.lower(): id_menu for id_menu, nom in rows}

def inserer_appartient(id_recette, id_menu):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("""
        INSERT INTO appartient (id_recette, id_menu)
        VALUES (%s, %s)
        ON CONFLICT (id_recette, id_menu) DO NOTHING
    """, (id_recette, id_menu))
    conn.commit()
    cur.close()
    conn.close()


def insert_appartient():
    with open("data/appartient.json", "r", encoding="utf-8") as f:
        liaisons = json.load(f)

    for lien in liaisons:
        inserer_appartient(
            lien["id_recette"],
            lien["id_menu"]
        )

  

