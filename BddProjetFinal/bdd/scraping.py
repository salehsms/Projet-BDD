from bs4 import BeautifulSoup
import time
import requests
import json
import os

os.makedirs("data", exist_ok=True)

# headers HTTP — tuto page 1
headers = {
    "User-Agent":      "Mozilla/5.0 (X11; Linux x86_64; rv:147.0) Gecko/20100101 Firefox/147.0",
    "Accept":          "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
    "Accept-Language": "fr,fr-FR;q=0.9,en-US;q=0.8,en;q=0.7",
}

categories = [
    {"id_categorie": 1, "nom_categorie": "Entree",            "description": "Plats servis en debut de repas"},
    {"id_categorie": 2, "nom_categorie": "Plat principal",    "description": "Plats chauds ou froids"},
    {"id_categorie": 3, "nom_categorie": "Dessert",           "description": "Sucreries et patisseries"},
    {"id_categorie": 4, "nom_categorie": "Soupe Potage",      "description": "Soupes et veloutes"},
    {"id_categorie": 5, "nom_categorie": "Sauce",             "description": "Sauces et condiments"},
    {"id_categorie": 6, "nom_categorie": "Aperitif",          "description": "Amuse-bouches et tapas"},
    {"id_categorie": 7, "nom_categorie": "Boisson",           "description": "Boissons chaudes et froides"},
    {"id_categorie": 8, "nom_categorie": "Pain Viennoiserie", "description": "Pains et brioches"},
]

f = open("data/Categorie.json", "w", encoding="utf-8")
json.dump(categories, f, ensure_ascii=False, indent=4)
f.flush()
f.close()


ustensiles = [
    {"id_ustensile":  1, "nom_ustensile": "Poele",             "type_ustensile": "cuisson"},
    {"id_ustensile":  2, "nom_ustensile": "Casserole",         "type_ustensile": "cuisson"},
    {"id_ustensile":  3, "nom_ustensile": "Cocotte",           "type_ustensile": "cuisson"},
    {"id_ustensile":  4, "nom_ustensile": "Moule a gateau",    "type_ustensile": "cuisson"},
    {"id_ustensile":  5, "nom_ustensile": "Moule a tarte",     "type_ustensile": "cuisson"},
    {"id_ustensile":  6, "nom_ustensile": "Plat a gratin",     "type_ustensile": "cuisson"},
    {"id_ustensile":  7, "nom_ustensile": "Sauteuse",          "type_ustensile": "cuisson"},
    {"id_ustensile":  8, "nom_ustensile": "Wok",               "type_ustensile": "cuisson"},
    {"id_ustensile":  9, "nom_ustensile": "Fouet",             "type_ustensile": "manuel"},
    {"id_ustensile": 10, "nom_ustensile": "Spatule",           "type_ustensile": "manuel"},
    {"id_ustensile": 11, "nom_ustensile": "Louche",            "type_ustensile": "manuel"},
    {"id_ustensile": 12, "nom_ustensile": "Cuillere en bois",  "type_ustensile": "manuel"},
    {"id_ustensile": 13, "nom_ustensile": "Rouleau patisserie","type_ustensile": "manuel"},
    {"id_ustensile": 14, "nom_ustensile": "Pinceau de cuisine","type_ustensile": "manuel"},
    {"id_ustensile": 15, "nom_ustensile": "Econome",           "type_ustensile": "tranchant"},
    {"id_ustensile": 16, "nom_ustensile": "Couteau de chef",   "type_ustensile": "tranchant"},
    {"id_ustensile": 17, "nom_ustensile": "Couteau a pain",    "type_ustensile": "tranchant"},
    {"id_ustensile": 18, "nom_ustensile": "Mandoline",         "type_ustensile": "tranchant"},
    {"id_ustensile": 19, "nom_ustensile": "Mixeur plongeant",  "type_ustensile": "electrique"},
    {"id_ustensile": 20, "nom_ustensile": "Robot patissier",   "type_ustensile": "electrique"},
    {"id_ustensile": 21, "nom_ustensile": "Batteur electrique","type_ustensile": "electrique"},
    {"id_ustensile": 22, "nom_ustensile": "Blender",           "type_ustensile": "electrique"},
    {"id_ustensile": 23, "nom_ustensile": "Four",              "type_ustensile": "electrique"},
    {"id_ustensile": 24, "nom_ustensile": "Saladier",          "type_ustensile": "contenant"},
    {"id_ustensile": 25, "nom_ustensile": "Bol",               "type_ustensile": "contenant"},
    {"id_ustensile": 26, "nom_ustensile": "Ramequin",          "type_ustensile": "contenant"},
    {"id_ustensile": 27, "nom_ustensile": "Planche a decouper","type_ustensile": "contenant"},
    {"id_ustensile": 28, "nom_ustensile": "Passoire",          "type_ustensile": "filtrage"},
    {"id_ustensile": 29, "nom_ustensile": "Tamis",             "type_ustensile": "filtrage"},
    {"id_ustensile": 30, "nom_ustensile": "Balance de cuisine","type_ustensile": "mesure"},
]

f = open("data/Ustensile.json", "w", encoding="utf-8")
json.dump(ustensiles, f, ensure_ascii=False, indent=4)
f.flush()
f.close()


data_ingredients     = []
noms_ingredients_vus = []
liens_vus            = []
id_ingredient        = 1


for page in range(1, 51):

    url = f"https://www.marmiton.org/recettes/recherche.aspx?type=all&page={page}"
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.text, "html.parser")

    for a in soup.find_all("a", href=True):
        href = a["href"]

        if "/recettes/recette_" not in href:
            continue

        lien_complet = href if href.startswith("http") else "https://www.marmiton.org" + href

        if lien_complet in liens_vus:
            continue
        liens_vus.append(lien_complet)

        if len(liens_vus) > 50:
            break

        try:
            r = requests.get(lien_complet, headers=headers)
            r.raise_for_status()
        except requests.exceptions.RequestException as e:
            continue

        soup_recette = BeautifulSoup(r.text, "html.parser")
        scripts = soup_recette.select("script[type='application/ld+json']")

        for script in scripts:
            try:
                data = json.loads(script.text.strip())

                if isinstance(data, list):
                    for item in data:
                        if isinstance(item, dict) and item.get("@type") == "Recipe":
                            data = item
                            break

                if not isinstance(data, dict) or data.get("@type") != "Recipe":
                    continue

                for ing in data.get("recipeIngredient", []):
                    nom_ing = str(ing).strip()
                    if len(nom_ing) < 2 or nom_ing in noms_ingredients_vus:
                        continue
                    noms_ingredients_vus.append(nom_ing)
                    data_ingredients.append({
                        "id_ingredient":       id_ingredient,
                        "nom_ingredient":      nom_ing,
                        "unite_mesure_defaut": None
                    })
                    id_ingredient += 1

                break

            except:
                continue

        time.sleep(1)

    if len(liens_vus) >= 50:
        break


f = open("data/Ingredient.json", "w", encoding="utf-8")
json.dump(data_ingredients, f, ensure_ascii=False, indent=4)
f.flush()
f.close()
