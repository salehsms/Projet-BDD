from connexion import get_connection
import json


def insert_fournit():
    with open("data/fournit.json", "r", encoding="utf-8") as f:
        liaisons = json.load(f)

    for lien in liaisons:
        inserer_fournit(
            lien["id_produit"],
            lien["id_fournisseur"],
            lien["prix"]
        )


def get_ids_produits():
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT id_produit FROM produit")
    ids = [r[0] for r in cur.fetchall()]
    cur.close()
    conn.close()
    return ids

def get_ids_fournisseurs():
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT id_fournisseur FROM fournisseur")
    ids = [r[0] for r in cur.fetchall()]
    cur.close()
    conn.close()
    return ids

def inserer_fournit(id_produit, id_fournisseur, prix):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("""
        INSERT INTO fournit (id_produit, id_fournisseur, prix)
        VALUES (%s, %s, %s)
        ON CONFLICT (id_produit, id_fournisseur) DO NOTHING
    """, (id_produit, id_fournisseur, prix))
    conn.commit()
    cur.close()
    conn.close()