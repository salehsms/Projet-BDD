import json
import random
from database import appartient_bd


recettes = appartient_bd.dic_recettes()  
menus    = appartient_bd.dic_menus()     

ids_recettes = list(recettes.values())
ids_menus    = list(menus.values())

data = []
vus  = set()

for id_recette in ids_recettes:
        nb = random.randint(1, 2)
        selection = random.sample(ids_menus, min(nb, len(ids_menus)))

        for id_menu in selection:
            cle = (id_recette, id_menu)
            if cle not in vus:
                vus.add(cle)
                data.append({
                    "id_recette": id_recette,
                    "id_menu": id_menu
                })

with open("data/appartient.json", "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4, ensure_ascii=False)

