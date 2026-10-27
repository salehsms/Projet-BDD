import json
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from database import ingredientproduit_bd


ingredients = ingredientproduit_bd.dic_ingredients()  
produits    = ingredientproduit_bd.dic_produits()     

data = []
vus  = set()

for nom_produit, id_produit in produits.items():
        for nom_ingredient, id_ingredient in ingredients.items():

            if nom_ingredient in nom_produit or nom_produit in nom_ingredient:
                cle = (id_ingredient, id_produit)
                if cle not in vus:
                    vus.add(cle)
                    data.append({
                        "id_ingredient": id_ingredient,
                        "id_produit": id_produit
                    })

if not data:
        print("Aucune correspondance trouvée")
    
with open("data/ingredientproduit.json", "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4, ensure_ascii=False)

