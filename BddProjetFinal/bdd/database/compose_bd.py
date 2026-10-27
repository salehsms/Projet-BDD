import json
from connexion import get_connection

def dic_ingredients():
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT id_ingredient, nom_ingredient FROM ingredient")
    rows = cur.fetchall()
    cur.close()
    conn.close()
    return {nom.lower(): id_ing for id_ing, nom in rows}


def insert_compose():
    conn = get_connection()
    cursor = conn.cursor()

    with open("data/compose.json", "r", encoding="utf-8") as f:
        compositions = json.load(f)

    for comp in compositions:
        cursor.execute(
            """
            INSERT INTO compose (id_ingredient, id_recette)
            VALUES (%s, %s)
            ON CONFLICT (id_ingredient, id_recette) DO NOTHING
            """,
            (
                comp["id_ingredient"],
                comp["id_recette"]
            )
        )



    conn.commit()
    cursor.close()
    conn.close()
