from bs4 import BeautifulSoup
import time
import requests
import json
from database import necessite_bd

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
                  "(KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
}

ustensiles_bdd = necessite_bd.dic_ustensiles()
recettes_bdd   = necessite_bd.dic_recettes()

data      = []
vus       = set()
liens_vus = set()

for page in range(1, 51):
    print(f"📄 Page {page}/50")

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

        ustensiles_page = soup_recette.select(".card-utensil-quantity")
        

        for ust_tag in ustensiles_page:
            parties = ust_tag.text.strip().split()
            if len(parties) < 2:
                continue

            nom_ust = " ".join(parties[1:]).lower()

            # 1. correspondance exacte
            id_ustensile = ustensiles_bdd.get(nom_ust)

            # 2. correspondance partielle si pas trouvé
            if id_ustensile is None:
                for nom_bdd, id_bdd in ustensiles_bdd.items():
                    if nom_ust in nom_bdd or nom_bdd in nom_ust:
                        id_ustensile = id_bdd
                        nom_ust = nom_bdd
                        break

            if id_ustensile:
                cle = (id_ustensile, id_recette)
                if cle not in vus:
                    vus.add(cle)
                    data.append({
                        "id_ustensile": id_ustensile,
                        "id_recette":   id_recette
                    })
                    
            
                

        with open("data/necessite.json", "w", encoding="utf-8") as f:
            json.dump(data, f, indent=4, ensure_ascii=False)

        time.sleep(0.5)

