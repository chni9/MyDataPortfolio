USE VeloMax;
SELECT * FROM fournisseur;
SELECT * FROM client;
SELECT * FROM entreprise;
SELECT * FROM fidelite;
SELECT * FROM commande;
SELECT * FROM modele_velo;
SELECT * FROM piece_rechange;
SELECT * FROM ligne_commande;
DELETE FROM client WHERE id_client = 1;
TRUNCATE TABLE commande;
TRUNCATE TABLE ligne_commande;
TRUNCATE TABLE modele_velo;
TRUNCATE TABLE piece_rechange;
TRUNCATE TABLE fidelite;

SELECT c.Nom_client, SUM(l.quantite * v.prix_unitaire) 
FROM client c JOIN ligne_commande l JOIN modele_velo v 
ON c.id_client = l.id_client AND v.Num_produit = l.Num_produit
GROUP BY c.Nom_client;

SELECT * FROM modele_velo WHERE quantite_dispo <= 2;

SELECT SUM(m.prix_unitaire * l.quantite) FROM modele_velo m JOIN ligne_commande l ON m.Num_produit = l.Num_produit;
SELECT MAX(Num_commande) FROM commande;
SELECT * FROM modele_velo For XML RAW;
