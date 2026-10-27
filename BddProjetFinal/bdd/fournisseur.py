import requests
import json

data = {}
page = 1

while True:

    url = f"https://world.openfoodfacts.org/products.json?page={page}"
    response = requests.get(url)

    if response.status_code != 200:
        break

    result = response.json()
    products = result.get("products", [])

    if not products:
        break

    for product in products:

        stores = product.get("stores", "")
        brands = product.get("brands", "")
        website = product.get("link", None) 

        if stores:
            for store in stores.split(","):

                store = store.strip()

                if store and store not in data:

                    nom = store
                    adresse = None
                    telephone = None
                    site = None
                    if website:
                        site = website

                    if not site and brands:
                        site = None  

                    data[store] = {
                        "id_fournisseur": len(data) + 1,
                        "nom_entreprise": nom,
                        "adresse_professionnelle": adresse,
                        "telephone_pro": telephone,
                        "site_web": site
                    }

    page += 1


with open("data/fournisseurs.json", "w", encoding="utf-8") as f:
    json.dump(list(data.values()), f, indent=4, ensure_ascii=False)
