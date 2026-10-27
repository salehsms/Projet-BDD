un petit guide pour les scripts : 

structure du dossier BDD :
    |_dossier data : les fichiers json de chaque table
    |_dossier database :  la plupart des fichiers de gestions de la base de données (insertion/récuperation des clès étrangére) sous le nom : nomTable_bd.py
    |_les autres fichiers scripts (insertion / récuperation des clès etrangère) sous le nom : insert_nomTable.bd 
    |_les scripts de collecte (scrapping) sous le nom : nomTable.py 
    |_le script de la creation des tables : mysql.sql
    |_la source de l'interface avec Tkinter : interface.py

L'exécution des fichiers : 
    pour l'insertion des données exécutez successivement les fichiers suivants :
     python insertiondatamelissa.py
     python recette.py   (patientez 1/2 min, puis ctrl+c)
     python etape.py      (patientez 1/2 min, puis ctrl+c)
     python menu.py      
     python main.py
     python interface.py 

Dans l'invite de commande Windows : 

**se connecter à la base de donnée : 
psql -U postgres 
Mot de passe :  123456789

**creer la base de donnée :  
CREATE DATABASE Recette_BD;

**Entrer à la base de donnée : 
\c Recette_BD

**copier le script que j'ai envoyé 

**verifier si toute les base sont creer :  

\dt (toutes les tables)
\d nom_table (une table spécifique)

**quiter le sgbd 
\q 
