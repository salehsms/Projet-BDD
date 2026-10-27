import json
from database import menu_db

mois = [
    "Janvier", "Février", "Mars", "Avril", "Mai", "Juin",
    "Juillet", "Août", "Septembre", "Octobre", "Novembre", "Décembre"
]

data = []

for i, nom in enumerate(mois, start=1):
    menu_db.inserer_menu(i, nom)
    data.append({"id_menu": i, "nom_menu": nom})
 

with open("./data/menu.json", "w", encoding="utf-8") as f:
    json.dump(data, f, indent=4, ensure_ascii=False)

