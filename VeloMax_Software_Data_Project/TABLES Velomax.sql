
DROP DATABASE IF EXISTS VeloMax; 
CREATE DATABASE IF NOT EXISTS VeloMax; 
USE VeloMax;

DROP TABLE IF EXISTS modele_velo;
CREATE TABLE IF NOT EXISTS modele_velo(
Num_produit INTEGER PRIMARY KEY, 
Nom_modele VARCHAR(40), 
grandeur VARCHAR(40),
prix_unitaire DECIMAL,
ligne_produit VARCHAR(40),
quantite_dispo INTEGER);
DESC modele_velo;



DROP TABLE IF EXISTS fournisseur;
CREATE TABLE IF NOT EXISTS fournisseur(
siret INTEGER PRIMARY KEY,
Nom_entreprise VARCHAR(40),  
contact VARCHAR(40),
adresse_entreprise VARCHAR(40), 
libelle ENUM('tres bon','bon','moyen','mauvais'));
DESC fournisseur;

DROP TABLE IF EXISTS piece_rechange;
CREATE TABLE IF NOT EXISTS piece_rechange(
Num_produit_piece INTEGER PRIMARY KEY, 
Description_piece VARCHAR(40), 
Nom_fournisseur VARCHAR(40),
Num_produit_fournisseur INTEGER, 
prix_unitaire_piece DECIMAL, 
date_intro DATE, 
date_discontinuation DATE,
delai_approvisionnement VARCHAR(40),
siret INTEGER,
FOREIGN KEY (siret) references fournisseur (siret) ON DELETE CASCADE);
DESC piece_rechange;


DROP TABLE IF EXISTS entreprise;
CREATE TABLE IF NOT EXISTS entreprise(
id_entreprise INTEGER PRIMARY KEY,
Nom_entreprise VARCHAR(40),
adresse_entreprise VARCHAR(40), 
province VARCHAR(40), 
telephone VARCHAR(40),
courriel VARCHAR(40),
Nom_contact VARCHAR(40),
remise VARCHAR(40));
DESC entreprise;

DROP TABLE IF EXISTS fidelite;
CREATE TABLE IF NOT EXISTS fidelite(
Num_fidelite INTEGER PRIMARY KEY,
Nom_fidelite VARCHAR(40),  
cout VARCHAR(40), 
duree VARCHAR(40), 
reduction VARCHAR(40));
DESC fidelite;


DROP TABLE IF EXISTS client;
CREATE TABLE IF NOT EXISTS client(
id_client INTEGER PRIMARY KEY,
Nom_client VARCHAR(40),Prenom_client VARCHAR(40),
adresse_client VARCHAR(40), 
province VARCHAR(40), 
telephone VARCHAR(40),
courriel VARCHAR(40),
Num_fidelite INTEGER, FOREIGN KEY (Num_fidelite) references fidelite (Num_fidelite));
DESC client;

DROP TABLE IF EXISTS commande;
CREATE TABLE IF NOT EXISTS commande(
Num_commande INTEGER PRIMARY KEY,
date_commande DATE,
adresse VARCHAR(40), 
date_livraison DATE,
id_entreprise INTEGER,FOREIGN KEY (id_entreprise) references entreprise (id_entreprise) ON DELETE CASCADE,
id_client INTEGER,FOREIGN KEY (id_client) references client (id_client) ON DELETE CASCADE);
DESC commande;

DROP TABLE IF EXISTS ligne_commande;
CREATE TABLE IF NOT EXISTS ligne_commande(
Num_commande INTEGER PRIMARY KEY,
Num_produit_piece INTEGER,FOREIGN KEY (Num_produit_piece) references piece_rechange (Num_produit_piece) ON DELETE CASCADE,
Num_produit INTEGER,FOREIGN KEY (Num_produit) references modele_velo (Num_produit) ON DELETE CASCADE,   
quantite INTEGER, 
id_entreprise INTEGER,FOREIGN KEY (id_entreprise) references entreprise (id_entreprise) ON DELETE CASCADE,
id_client INTEGER,FOREIGN KEY (id_client) references client (id_client) ON DELETE CASCADE);
DESC ligne_commande;

DROP TABLE IF EXISTS assemblage;
CREATE TABLE IF NOT EXISTS assemblage(
Num_produit INTEGER primary key,
FOREIGN KEY (Num_produit) references modele_velo (Num_produit) ON DELETE CASCADE,
Nom_modele VARCHAR(40),
grandeur VARCHAR(40),  
cadre VARCHAR(40), 
guidon VARCHAR(40), 
frein VARCHAR(40), 
selle VARCHAR(40),
derailleur_av VARCHAR(40),
derailleur_ar VARCHAR(40),
roue_av VARCHAR(40),
roue_ar VARCHAR(40),
reflecteur VARCHAR(40),
pedalier VARCHAR(40),
ordinateur VARCHAR(40),
panier VARCHAR(40));
DESC assemblage;

