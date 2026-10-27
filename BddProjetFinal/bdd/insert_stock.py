import json
import random
from connexion import get_connection

def insert_stock():
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("SELECT id_ingredient FROM Ingredient")
    valides_ids = [row[0] for row in cur.fetchall()]

    if not valides_ids:
        print("Erreur : La table Ingredient est vide ! Remplissez-la d'abord.")
        return

    try:
        with open("data/stock.json", "r", encoding="utf-8") as f:
            stocks = json.load(f)
    except FileNotFoundError:
        return


    for s in stocks:
        try:
            id_ing_valide = random.choice(valides_ids)
            
            cur.execute("""
                INSERT INTO Stock (id_stock, id_ingredient, id_ustensille, quantite_disponible, quantite_minimale)
                VALUES (%s, %s, %s, %s, %s)
                ON CONFLICT (id_stock) DO UPDATE SET
                    id_ingredient = EXCLUDED.id_ingredient,
                    quantite_disponible = EXCLUDED.quantite_disponible,
                    quantite_minimale = EXCLUDED.quantite_minimale
            """, (
                s["id_stock"],
                id_ing_valide,  
                None,
                s["quantité_disponible"],
                s["quantité_minimale"]
            ))
        except Exception as e:
            print(f"Erreur sur la ligne {s['id_stock']} : {e}")
            conn.rollback() 
            continue 

    conn.commit()
    cur.close()
    conn.close()
    print("Table Stock mise à jour avec des IDs existants !")

if __name__ == "__main__":
    insert_stock()