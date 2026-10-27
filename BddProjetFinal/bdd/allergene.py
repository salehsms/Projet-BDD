import requests
import json

url = "https://world.openfoodfacts.org/data/taxonomies/allergens.json"
response = requests.get(url)
data = response.json()

allergenes = []
i = 1

for key in data:

    element = data[key]

    if "name" in element and "fr" in element["name"]:
        nom = element["name"]["fr"]
    else:
        nom = key.replace("en:", "")

    description = None

    if "description" in element and "fr" in element["description"]:
        description = element["description"]["fr"]

    elif "wikipedia_url" in element and "fr" in element["wikipedia_url"]:
        description = element["wikipedia_url"]["fr"]

    allergenes.append({
        "id_allergene": i,
        "nom_allergene": nom,
        "description": description
    })

    i += 1


with open("data/allergenes.json", "w", encoding="utf-8") as f:
    json.dump(allergenes, f, ensure_ascii=False, indent=2)
