from bs4 import BeautifulSoup
import time
import requests
import json
import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from database import compose_bd, recette_bd

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
                  "(KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
}

ingredients_bdd = compose_bd.dic_ingredients()
recettes_bdd    = recette_bd.dic_recettes()
data = []
liens_vus = set()

for page in range(1, 51):

    url = f"https://www.marmiton.org/recettes/recherche.aspx?type=all&page={page}"

    try:
        response = requests.get(url, headers=HEADERS, timeout=10)
        response.raise_for_status()
    except requests.exceptions.RequestException as e:
        continue

    soup = BeautifulSoup(response.text, "html.parser")

    for a in soup.find_all("a", href=True):
        href = a["href"]

        if "/recettes/recette_" not in href:
            continue

        lien_complet = href if href.startswith("http") else "https://www.marmiton.org" + href
        lien_complet = lien_complet.split("?")[0]

        if lien_complet in liens_vus:
            continue
        liens_vus.add(lien_complet)

        try:
            r = requests.get(lien_complet, headers=HEADERS, timeout=10)
            r.raise_for_status()
        except requests.exceptions.RequestException as e:
            continue

        soup_recette = BeautifulSoup(r.text, "html.parser")

        titre_tag = soup_recette.select_one("h1")
        if not titre_tag:
            continue

        nom_recette = titre_tag.text.strip().lower()
        id_recette  = recettes_bdd.get(nom_recette)

        if id_recette is None:
            continue

        
        ingredients_page = soup_recette.select(".ingredient-name")

        for ing_tag in ingredients_page:
            nom_ing = ing_tag.text.strip().lower()
            id_ingredient = ingredients_bdd.get(nom_ing)

            if id_ingredient:
                data.append({
                    "id_ingredient": id_ingredient,
                    "id_recette": id_recette
                })

            

        with open("data/compose.json", "w", encoding="utf-8") as f:
            json.dump(data, f, indent=4, ensure_ascii=False)

        time.sleep(0.5)

