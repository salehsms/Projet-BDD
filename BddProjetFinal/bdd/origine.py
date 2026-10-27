import requests
import json
import os

def extraire_donnees_origines():
    url = "https://www.themealdb.com/api/json/v1/1/list.php?a=list"
    
    try:
        response = requests.get(url, timeout=10)
        data = response.json()
        
        liste_origines = []
        
        for i, item in enumerate(data["meals"], start=1):
            liste_origines.append({
                "id_origine": i,
                "id_recette": None,  
                "pays": item["strArea"],
                "region": "inconnue"
            })

        os.makedirs("data", exist_ok=True)
        with open("data/origines.json", "w", encoding="utf-8") as f:
            json.dump(liste_origines, f, indent=4, ensure_ascii=False)
            

    except Exception as e:
        print(f"Erreur lors de l'extraction : {e}")

if __name__ == "__main__":
    extraire_donnees_origines()