import json
from connexion import get_connection

def insert_fournisseurs():
    conn = get_connection()
    cursor = conn.cursor()

    with open("data/fournisseurs.json", "r", encoding="utf-8") as f:
        fournisseurs = json.load(f)

    for four in fournisseurs:         
        cursor.execute(
            """INSERT INTO fournisseur 
            (id_fournisseur, nom_entreprise, adresse_professionnelle, telephone_pro, site_web)
            VALUES (%s, %s, %s, %s, %s)
            ON CONFLICT (id_fournisseur) DO NOTHING""", 
            (
                four["id_fournisseur"],
                four["nom_entreprise"],
                four["adresse_professionnelle"],
                four["telephone_pro"],
                four["site_web"]
            )
        )

    conn.commit()
    cursor.close()
    conn.close()
