from connexion import get_connection
import json


def insert_ingredientproduit():
    with open("data/ingredientproduit.json", "r", encoding="utf-8") as f:
        liaisons = json.load(f)

    for lien in liaisons:
        inserer_ingredientproduit(
            lien["id_ingredient"],
            lien["id_produit"]
        )


if __name__ == "__main__":
    insert_ingredientproduit()
def dic_ingredients():
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT id_ingredient, nom_ingredient FROM ingredient")
    rows = cur.fetchall()
    cur.close()
    conn.close()
    return {nom.lower(): id_ing for id_ing, nom in rows}

def dic_produits():
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT id_produit, nom_produit FROM produit")
    rows = cur.fetchall()
    cur.close()
    conn.close()
    return {nom.lower(): id_prod for id_prod, nom in rows}

def inserer_ingredientproduit(id_ingredient, id_produit):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("""
        INSERT INTO IngredientProduit (id_ingredient, id_produit)
        VALUES (%s, %s)
        ON CONFLICT DO NOTHING
    """, (id_ingredient, id_produit))
    conn.commit()
    cur.close()
    conn.close()