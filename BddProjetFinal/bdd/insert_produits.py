import json
from connexion import get_connection

def insert_produits():
    conn = get_connection()
    cursor = conn.cursor()

    with open("data/produits.json", "r", encoding="utf-8") as f:
        produits = json.load(f)

    for prod in produits:
        marques_str = ", ".join(prod["marques"])

        cursor.execute(
            """
            INSERT INTO Produit
            (id_produit, nom_produit, marques, disponiblite)
            VALUES (%s, %s, %s, %s)
            ON CONFLICT (id_produit) DO NOTHING
            """,
            (
                prod["id_produit"],
                prod["nom_produit"],
                marques_str,
                prod["disponibilite"]
            )
        )

    conn.commit()
    cursor.close()
    conn.close()
