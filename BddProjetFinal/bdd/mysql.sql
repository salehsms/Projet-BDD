drop table if exists IngredientProduit CASCADE;
drop table if exists Categorie CASCADE;
drop table if exists Ingredient CASCADE; 
drop table if exists Allergien CASCADE; 
drop table if exists Ustensile CASCADE; 
drop table if exists Stock CASCADE; 
drop table if exists Produit CASCADE; 
drop table if exists Fournisseur CASCADE; 
drop table if exists recette CASCADE; 
drop table if exists menu CASCADE; 
drop table if exists etape CASCADE; 
drop table if exists origine CASCADE; 
drop table if exists fournit CASCADE; 
drop table if exists contient2 CASCADE; 
drop table if exists compose CASCADE; 
drop table if exists convient CASCADE; 
drop table if exists appartient CASCADE; 
drop table if exists necessite CASCADE; 


CREATE  table Categorie (
    id_categorie  INT ,
    nom_catgorie varchar(80),
    description text,
    constraint id_categorie primary key(id_categorie)


);

CREATE TABLE Ingredient(
    id_ingredient INT,
    nom_ingredient text, 
    unite_mesure_defaut Int,
    
    constraint id_ingredient primary key(id_ingredient)
);


CREATE table Allergien(
    id_allergene INT primary key,
    nom_allergene varchar(80) ,
    description varchar(30)
    );

CREATE TABLE  Fournisseur(
    id_fournisseur INT primary key,
    nom_entreprise varchar(100),
    adresse_professionnelle text,
    telephone_pro Integer ,
    site_web text 
);

create table Recette (
id_recette integer primary key,
id_categorie integer,
nom_recette varchar(100),
description_ text,
temps_preparation varchar(50),
temps_cuisson varchar(50),
date_creation varchar(100),
constraint fk_categorie foreign key (id_categorie) references Categorie (id_categorie)
);

create table menu(
    id_menu integer,
    nom_menu varchar(100),
    constraint pk_menu primary key (id_menu)
);

create table etape( 
    id_etape integer primary key,
    id_recette integer, 
    numero_ordre integer,
    descrption_etape text,
    constraint fk_recette foreign key (id_recette) references Recette(id_recette)
);



create table origine(
    id_origine integer,
    id_recette integer, 
    pays varchar(60),
    region varchar(60),
    constraint pk_origine primary key (id_origine),
    constraint fk_origine foreign key(id_recette) references Recette (id_recette)
);


create table compose(
    id_ingredient integer,
    id_recette integer,
    constraint pk_compose primary key(id_ingredient, id_recette)
);



create table contient2(
    id_ingredient integer,
    id_allergene integer,
    constraint pk_contient2 primary key(id_ingredient, id_allergene)
);

create table appartient(
    id_recette integer,
    id_menu integer, 
    constraint pk_appartient primary key(id_recette, id_menu)
);



CREATE TABLE Ustensile(
    id_ustensile INT primary key ,
    nom_ustensile varchar(100),
    type_ustensile varchar(70)
    );


CREATE TABLE  Stock(
    id_stock INT primary key,
    id_ingredient INT references Ingredient (id_ingredient),
    id_ustensille INT references Ustensile (id_ustensile),
    quantité_disponible INT,
    quantité_minimale INT 
);

ALTER TABLE Stock
RENAME COLUMN "quantité_disponible" TO quantite_disponible;

ALTER TABLE Stock
RENAME COLUMN "quantité_minimale" TO quantite_minimale;


CREATE TABLE  Produit(
    id_produit INT primary key,
    nom_produit VARCHAR(100),
    marques text,
    disponiblite INT 
);


CREATE TABLE IngredientProduit (
    id_ingredient INT references Ingredient (id_ingredient),
    id_produit INT references Produit (id_produit)
);

create table fournit(
    id_produit integer, 
    id_fournisseur integer,
    prix integer,
    constraint pk_fournit primary key(id_produit, id_fournisseur)
);
ALTER TABLE fournit ALTER COLUMN prix TYPE numeric(6,2);


create table necessite( 
    id_ustensile integer,
    id_recette integer,
    constraint pk_necessite primary key(id_ustensile, id_recette)
);

