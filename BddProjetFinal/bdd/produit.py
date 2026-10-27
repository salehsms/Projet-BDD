import requests
from bs4 import BeautifulSoup
import json
import time

base = "https://www.marmiton.org"

url = base + "/recettes/recherche.aspx?aqt=&start=0"

r = requests.get(url)
soup = BeautifulSoup(r.text, "html.parser")

links = []

for a in soup.select("a[href*='/recettes/recette_']"):

    lien = a["href"]

    if lien.startswith("/"):
        lien = base + lien

    if lien not in links:
        links.append(lien)


ingredients_set = set()

for lien in links[:10]:  


    r = requests.get(lien)
    soup = BeautifulSoup(r.text, "html.parser")

    ingredients = soup.select("span.ingredient-name")

    for ing in ingredients:
        nom = ing.get_text(strip=True)

        if nom:
            ingredients_set.add(nom.lower())

    time.sleep(1)


resultats = []

i = 1

for ingredient in ingredients_set:

    print("Recherche marques pour :", ingredient)

    url_api = "https://world.openfoodfacts.org/cgi/search.pl"

    params = {
        "search_terms": ingredient,
        "search_simple": 1,
        "json": 1
    }

    r = requests.get(url_api, params=params)

    try:
        data = r.json()
    except:
        data = {"products": []}

    marques = []

    for p in data.get("products", [])[:5]:  
        marque = p.get("brands")

        if marque and marque not in marques:
            marques.append(marque)

    resultats.append({
        "id_produit": i,
        "nom_produit": ingredient,
        "marques": marques,
        "disponibilite": None
    })

    i += 1

    time.sleep(1)
with open("data/produits.json", "w", encoding="utf-8") as f:
    json.dump(resultats, f, indent=4, ensure_ascii=False)
