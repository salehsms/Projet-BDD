import requests
import json
import random
import os


url = "https://world.openfoodfacts.org/api/v2/search"

params = {
    "categories_tags": "en:snacks", 
    "fields": "product_name",
    "page_size": 20
}

headers = {
    "User-Agent": "MonProjetEtudiant/1.0 (contact: saleh@example.com)"
}

try:
    print("Connexion à l'API Open Food Facts...")
    response = requests.get(url, params=params, headers=headers, timeout=10)
    
    
    response.raise_for_status() 
    
    data = response.json()
    products = data.get("products", [])

    stock = []
    MAX_INGREDIENT_ID = 241 

    for i, produit in enumerate(products, start=1):
        stock.append({
            "id_stock": i,
            "id_ingredient": random.randint(1, MAX_INGREDIENT_ID),
            "id_ustensille": None, # Correspond au NULL SQL
            "quantité_disponible": random.randint(1, 50),
            "quantité_minimale": random.randint(1, 10)
        })

   
    os.makedirs("data", exist_ok=True)
    with open("data/stock.json", "w", encoding="utf-8") as f:
        json.dump(stock, f, indent=4, ensure_ascii=False)


except requests.exceptions.HTTPError as err:
    print(f"Erreur HTTP : {err}")
except json.decoder.JSONDecodeError:
    print("Erreur : L'API n'a pas renvoyé de JSON. Essayez de changer les 'search_terms'.")
except Exception as e:
    print(f"Une erreur inattendue est survenue : {e}")