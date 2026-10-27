import json
import random
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from database import contient2_bd


ingredients = contient2_bd.dic_ingredients()  
allergenes  = contient2_bd.dic_allergenes()   

ids_ingredients = list(ingredients.values())
ids_allergenes  = list(allergenes.values())

data = []
vus = set()

for id_ingredient in ids_ingredients:
        nb = random.randint(0, 2)
        selection = random.sample(ids_allergenes, min(nb, len(ids_allergenes)))

        for id_allergene in selection:
            cle = (id_ingredient, id_allergene)
            if cle not in vus:
                vus.add(cle)
                data.append({
                    "id_ingredient": id_ingredient,
                    "id_allergene": id_allergene
                })

with open("data/contient2.json", "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4, ensure_ascii=False)

