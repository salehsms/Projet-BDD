import json
from connexion import get_connection

def charger_mapping_recettes():
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT id_recette, nom_recette FROM Recette")
    rows = cur.fetchall()
    cur.close()
    conn.close()
    return {nom.lower().strip(): id_rec for id_rec, nom in rows}

def insert_origines():
    dict_recettes = charger_mapping_recettes()
    
    try:
        with open("data/origines.json", "r", encoding="utf-8") as f:
            origines = json.load(f)
    except FileNotFoundError:
        print("Erreur : data/origines.json introuvable. Lancez origine.py d'abord.")
        return

    conn = get_connection()
    cur = conn.cursor()

    for o in origines:
        id_origine = o["id_origine"]
        id_recette_liee = None
        pays = o["pays"]
        region = o["region"]

        for nom_recette_db, id_db in dict_recettes.items():
            if pays.lower() in nom_recette_db:
                id_recette_liee = id_db
                break

        cur.execute("""
            INSERT INTO origine (id_origine, id_recette, pays, region)
            VALUES (%s, %s, %s, %s)
            ON CONFLICT (id_origine) DO UPDATE SET
                id_recette = EXCLUDED.id_recette,
                pays = EXCLUDED.pays,
                region = EXCLUDED.region
        """, (
            id_origine,
            id_recette_liee, 
            pays,
            region
        ))

    conn.commit()
    cur.close()
    conn.close()

if __name__ == "__main__":
    insert_origines()