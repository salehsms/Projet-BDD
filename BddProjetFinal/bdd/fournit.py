import json
import random
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from database import fournit_bd


ids_produits     = fournit_bd.get_ids_produits()
ids_fournisseurs = fournit_bd.get_ids_fournisseurs()

data = []
vus  = set()

for id_produit in ids_produits:
        nb = random.randint(1, 2)
        selection = random.sample(ids_fournisseurs, min(nb, len(ids_fournisseurs)))

        for id_fournisseur in selection:
            cle = (id_produit, id_fournisseur)
            if cle not in vus:
                vus.add(cle)
                prix = round(random.uniform(0.6, 50.0), 2)
                data.append({
                    "id_produit":     id_produit,
                    "id_fournisseur": id_fournisseur,
                    "prix":           prix
                })

with open("data/fournit.json", "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4, ensure_ascii=False)


