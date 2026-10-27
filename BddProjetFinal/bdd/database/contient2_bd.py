import json
from connexion import get_connection

def insert_contient2():
    conn = get_connection()
    cursor = conn.cursor()

    with open("data/contient2.json", "r", encoding="utf-8") as f:
        liaisons = json.load(f)

    for lien in liaisons:
        cursor.execute(
            """
            INSERT INTO contient2 (id_ingredient, id_allergene)
            VALUES (%s, %s)
            ON CONFLICT (id_ingredient, id_allergene) DO NOTHING
            """,
            (lien["id_ingredient"], lien["id_allergene"])
        )

    conn.commit()
    cursor.close()
    conn.close()

def dic_ingredients():
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT id_ingredient, nom_ingredient FROM ingredient")
    rows = cur.fetchall()
    cur.close()
    conn.close()
    return {nom.lower(): id_ing for id_ing, nom in rows}

def dic_allergenes():
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT id_allergene, nom_allergene FROM allergien")
    rows = cur.fetchall()
    cur.close()
    conn.close()
    return {nom.lower(): id_all for id_all, nom in rows}


if __name__ == "__main__":
    insert_contient2()