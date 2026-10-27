import json
from connexion import get_connection

def insert_allergenes():
    conn = get_connection()
    cursor = conn.cursor()

    with open("data/allergenes.json", "r", encoding="utf-8") as f:
        allergenes = json.load(f)

    for a in allergenes:
        cursor.execute(
            "INSERT INTO allergien (id_allergene, nom_allergene, description) VALUES (%s, %s, %s) ON CONFLICT (id_allergene) DO NOTHING",
            (                                
                a["id_allergene"],
                a["nom_allergene"],
                a["description"]
            )
        )

    conn.commit()
    cursor.close()
    conn.close()
