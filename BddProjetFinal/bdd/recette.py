from bs4 import BeautifulSoup
import time 
import requests
import json
from database import recette_bd
import random
 
data = []
id_recette  = 1

for page in range(1, 51):

    url = f"https://www.marmiton.org/recettes/recherche.aspx?type=all&page={page}"
    
    response = requests.get(url)
    soup = BeautifulSoup(response.text, "html.parser")

    for a in soup.find_all("a", href=True):
        href = a["href"]
    
        if "/recettes/recette_" in href:
            if href.startswith("http"):
                lien_complet = href
            else:
                lien_complet = "https://www.marmiton.org" + href

            try:
                r = requests.get(lien_complet)
                r.raise_for_status()
            except requests.exceptions.RequestException as e:
                continue

            soup_recette = BeautifulSoup(r.text, "html.parser")
            titre = soup_recette.select_one("h1")

            # Description
            description = soup_recette.select_one("div.mrtn-block-dropcap-text > div.dropcap-text")

            #Récuperper l'id de la catégorie de la recette 
            categorie = soup_recette.select_one(".breadcrumb span:nth-child(3)")
            if categorie:
                nom_categorie = categorie.text.strip().lower()
                categories = recette_bd.dic_categories()
                id_categorie = categories.get(nom_categorie)  
            else:
                 id_categorie = None
            if id_categorie is None:
                categories = recette_bd.dic_categories()
                id_categorie = random.choice(list(categories.values()))
    

           

            # Temps de préparation
            temps_preparation = soup_recette.select_one("div.recipe-primary__item:nth-child(1) > span:nth-child(2)")

            # Temps de cuisson
            temps_cuisson = soup_recette.select_one(".time_details div div")


            #date_creation 
            date_creation = soup_recette.select_one("#recipe-reviews-list__container > div.recipe-reviews-list > div > div:nth-child(1) > span")
            data.append({
                    'id_recette' : id_recette,
                    'id_categorie': id_categorie if not None else None,
                    'titre': titre.text.strip(),
                    'Description': description.text.strip() if description else None,
                    'temps de préparation': temps_preparation.text.strip() if temps_preparation else None,
                    'temps cuisson': temps_cuisson.text.strip() if temps_cuisson else None,
                    'Date de publication': date_creation.text.strip() if date_creation else None

                })
            recette_bd.inserer_recette(
                id_recette,
                id_categorie,
                titre.text.strip(),
                description.text.strip()if description else None,
                temps_preparation.text.strip() if temps_preparation else None,
                temps_cuisson.text.strip() if temps_cuisson else None,
                date_creation.text.strip()if date_creation else None,
            )

            

            with open("data/recette.json", "w", encoding='UTF-8') as f:
                    json.dump(data, f, indent=4, ensure_ascii=False)

            time.sleep(0.5)
            id_recette += 1 