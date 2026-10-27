from bs4 import BeautifulSoup
import time
import requests
import json
from database import etape_bd

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
                  "(KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
}

data = []
id_etape = 1
liens_vus = set()


recettes = etape_bd.dic_recettes()  

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
            print(f" Erreur : {e}")
            continue

        soup_recette = BeautifulSoup(r.text, "html.parser")

       
        nom_tag = soup_recette.select_one("h1")
        if not nom_tag:
            continue

        nom_recette = nom_tag.text.strip().lower()
        id_recette = recettes.get(nom_recette) 

        if id_recette is None:
            continue

        
        etapes = soup_recette.select(".recipe-step-list__container p")
        if not etapes:
            continue

        print(f" {nom_recette} — {len(etapes)} étapes")

        for num, etape in enumerate(etapes, start=1):
            description = etape.text.strip()
            if not description:
                continue

            data.append({
                "id_etape": id_etape,
                "id_recette": id_recette,
                "numero_ordre": num,
                "description": description
            })

            etape_bd.inserer_etape(id_etape, id_recette, num, description)
            id_etape += 1
            time.sleep(0.3)

        with open("data/etape.json", "w", encoding="utf-8") as f:
            json.dump(data, f, indent=4, ensure_ascii=False)

