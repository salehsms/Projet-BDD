from insert_allergenes   import insert_allergenes
from insert_fournisseurs import insert_fournisseurs
from insert_produits     import insert_produits  
from insert_origine import insert_origines
from insert_stock import insert_stock
from database import compose_bd as cbd
from database import contient2_bd as con
from database import appartient_bd as app
from database import ingredientproduit_bd as ip
from database import fournit_bd as four
from database import necessite_bd as nbd



insert_allergenes()
print("Allergenes inseres")

insert_fournisseurs()
print("Fournisseurs inseres")

insert_produits()
print("Produits inseres")

insert_origines()
print("Origines inserées")

insert_stock()
print("Stock inserés")


con.insert_contient2()
print("Contient2 insérée")

nbd.insert_necessite()
print("necessite insérée")

ip.insert_ingredientproduit()
print("ingredientproduit insérée")

four.insert_fournit()
print("fournit insérée")

cbd.insert_compose()
print("Composition insérée")

app.insert_appartient()
print("appartient insérée")

print("Termine")