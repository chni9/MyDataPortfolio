using System;
using System.Linq;
using MySql.Data.MySqlClient;

namespace VeloMax
{
    class Program
    {
        #region Main
        static void Main(string[] args)
        {
            #region Ouverture de la connexion avec MySQL
            string connexionInfo = "SERVER=localhost;PORT=3306;DATABASE=velomax;UID=root;PASSWORD=Tournevis37?!";
            MySqlConnection maConnexion = ConnexionSQL(connexionInfo);
            #endregion
            bool done = false;
            while(! done) 
            { 
                done = Accueil();
            }

            maConnexion.Close();
        }
        #endregion

        #region Connexion SQL 
        static MySqlConnection ConnexionSQL(string connexionInfo)
        {
            MySqlConnection maConnexion = null;
            try
            {
                maConnexion = new MySqlConnection(connexionInfo);
                maConnexion.Open();

            }
            catch (MySqlException e)
            {
                Console.WriteLine("Erreur de connexion : " + e.ToString());
            }
            return maConnexion;
        }

        static void executeRequete(string requete)
        {
            MySqlCommand maRequete = ConnexionSQL("SERVER=localhost;PORT=3306;DATABASE=velomax;UID=root;PASSWORD=Tournevis37?!").CreateCommand();
            maRequete.CommandText = requete;
            maRequete.ExecuteNonQuery();
        }
        static string Requete(string requete)
        {
            MySqlCommand maRequete = ConnexionSQL("SERVER=localhost;PORT=3306;DATABASE=velomax;UID=root;PASSWORD=Tournevis37?!").CreateCommand();
            maRequete.CommandText = requete;
            MySqlDataReader exeRequete = maRequete.ExecuteReader();
            string tableau = "";
            while (exeRequete.Read())
            {
                string ligne = "";
                for (int i = 0; i < exeRequete.FieldCount; i++)
                {
                    ligne = ligne + "\t" + exeRequete.GetValue(i).ToString();
                }
                tableau = tableau + "\n" + ligne;
            }
            exeRequete.Close();
            return tableau;
        }
        #endregion

        #region Accueil
        static bool Accueil()
        {
            Console.WriteLine("==== VéloMax ====");
            Console.WriteLine("1 : Espace Client\t 2 : Espace Entreprise\t 3 : Espace Employé\t 4 : Mode évaluation (demo)\t5 : Quitter");
            int choix = int.Parse(Console.ReadLine());
            bool done = false;
            switch (choix)
            {
                case 1:
                    ConnexionClient();
                    break;
                case 2:
                    ConnexionEntreprise();
                    break;
                case 3:
                    EspaceEmployé();
                    break;
                case 4:
                    Demo();
                    break;
                case 5:
                    done = true;
                    break;
            }
            return done;
        }
        #endregion

        #region Espace Client
        static void ConnexionClient()
        {
            Console.WriteLine("==== Espace Client ====\nConnexion :");
            Console.WriteLine("1 : Connexion    2 : Créer un compte");
            int choix = int.Parse(Console.ReadLine());
            switch (choix)
            {
                case 1:
                    Console.WriteLine("ID utilisateur :");
                    int id_utilisateur = int.Parse(Console.ReadLine());
                    bool valid = false;
                    string[] requete = Requete("SELECT id_client FROM client").Split(new char[] {'\n','\t'});
                    for (int i = 0; i < requete.Length; i++)
                    {
                        if (requete[i] == id_utilisateur.ToString())
                        {
                            valid = true;
                        }
                    }
                    if (valid)
                    {
                        Console.WriteLine("Connexion ...");
                        EspaceClient(id_utilisateur);
                    }
                    else
                    {
                        Console.WriteLine("ID utilisateur invalide\nRéessayez");
                    }
                    break;
                case 2:
                    CreationClient();
                    break;
            }
        }
        static void CreationClient()
        {
            Console.WriteLine("==== Création Compte ====");
            bool id_ok = true;
            int id_client;
            do
            {
                Console.WriteLine("ID utilisateur (4 chiffres) : ");
                id_client = int.Parse(Console.ReadLine());
                id_ok = true;
                string[] requete_id = Requete("SELECT id_client FROM client").Split(new char[] { '\n', '\t' }); 
                for (int i = 0; i < requete_id.Length; i++)
                {
                    if (Convert.ToString(id_client) == requete_id[i]) 
                    { 
                        Console.WriteLine("|!| ID utilisateur déjà utilisé ! Réessayez ...");
                        id_ok = false;
                    }
                }
            } while (! id_ok);
            Console.WriteLine("Nom : ");
            string nom_client = Console.ReadLine();
            Console.WriteLine("Prénom : ");
            string prenom_client = Console.ReadLine();
            Console.WriteLine("Adresse : ");
            string adresse = Console.ReadLine();
            Console.WriteLine("Province : ");
            string province = Console.ReadLine();
            Console.WriteLine("Téléphone : ");
            string telephone = Console.ReadLine();
            Console.WriteLine("Email : ");
            string courriel = Console.ReadLine();
            string requete = "INSERT INTO `client` " +
                "(`id_client`,`Nom_client`,`Prenom_client`,`adresse_client`,`province`,`telephone`,`courriel`,`Num_fidelite`)" +
                " VALUES (" + id_client + "," + "'" + nom_client + "'" + "," + "'" + prenom_client + "'" + ", '" + adresse + "'," + "'" + province + "'" + "," + "'" + telephone + "'" + "," + "'" + courriel + "'" + "," + "null )";
            executeRequete(requete);
            Console.WriteLine("|-| Compte créé avec succès ! |-|");        
        }
        static void SuppressionClient()
        {
            Console.WriteLine("Quel compte client souhaitez-vous supprimer (id) ? ");
            Console.WriteLine(Requete("SELECT * FROM client"));
            int id_client = int.Parse(Console.ReadLine());
            executeRequete("DELETE FROM client WHERE id_client = " + id_client + ";");
            Console.WriteLine("|-| Suppression effectuée avec succès ! |-|");
        }

        static void ModificationClient()
        {
            Console.WriteLine("Quel compte client souhaitez-vous modifier (id) ? ");
            Console.WriteLine(Requete("SELECT * FROM client"));
            int id_client = int.Parse(Console.ReadLine());
            Console.WriteLine("Quel attribut souhaitez-vous modifier ? ");
            Console.WriteLine(Requete("SHOW COLUMNS FROM client"));
            string attribut = Console.ReadLine();
            if (attribut == "id_client" || attribut == "Num_fidelite")
            {
                Console.WriteLine("Quelle valeur souhaitez-vous lui attribuer ?");
                int value = int.Parse(Console.ReadLine());
                executeRequete("UPDATE client SET " + attribut + " = " + value + " WHERE id_client = " + id_client + ";");
            }
            else
            {
                Console.WriteLine("Quelle valeur souhaitez-vous lui attribuer ?");
                string value = Console.ReadLine();
                executeRequete("UPDATE client SET " + attribut + " = '" + value + "' WHERE id_client = " + id_client + ";");
            }
            Console.WriteLine("|-| Modification effectuée avec succès ! |-|");
        }
        static void EspaceClient(int id_utilisateur)
        {
            Console.WriteLine("==== Espace client ====");
            Console.WriteLine("1 : Commander    2 : Souscrire au Programme Fidélio");
            int choix = int.Parse(Console.ReadLine());
            switch (choix)
            {
                case 1:
                    bool done = false;
                    do
                    {
                        int num_commande = int.Parse(Requete("SELECT MAX(Num_commande) FROM commande")) + 1;
                        string date_ajd = DateTime.Now.ToString("yyyy-MM-dd HH:mm:ss");
                        executeRequete("INSERT INTO commande (Num_commande, date_commande, adresse, date_livraison, id_entreprise, id_client) VALUES (" + num_commande + ",'" + date_ajd + " ','" + Requete("SELECT adresse_client FROM client WHERE id_client = " + id_utilisateur + ";") + "', null, null," + id_utilisateur + ");");
                        Console.WriteLine("1 : Catalogue vélo    2 : Catalogue pièce de rechange");
                        int choix_catalogue = int.Parse(Console.ReadLine());
                        switch (choix_catalogue)
                        {
                            case 1:
                                Console.WriteLine(Requete("SELECT * FROM modele_velo"));
                                Console.WriteLine("Sélectionner le produit souhaité (par numéro de produit) : ");
                                int choix_prod1 = int.Parse(Console.ReadLine());
                                Console.WriteLine("Quelle quantité ?");
                                int qte1 = int.Parse(Console.ReadLine());
                                string[] requete2 = Requete("SELECT * FROM modele_velo WHERE Num_produit = " + choix_prod1 + ";").Split(new char[] { '\n', '\t' });
                                int quantite_dispo  = int.Parse(requete2[7]);
                                if (quantite_dispo == 0)
                                {
                                    Console.WriteLine("|!| Erreur : Ce produit n'est plus disponible ! ");
                                    executeRequete("DELETE FROM commande WHERE Num_commande = " + num_commande + ";");
                                }
                                else
                                {
                                    if (qte1 > quantite_dispo)
                                    {
                                        Console.WriteLine("|!| Erreur : Nous n'avons pas assez d'exemplaires de ce produit ! ");
                                        executeRequete("DELETE FROM commande WHERE Num_commande = " + num_commande + ";");
                                    }
                                    else
                                    {
                                        TimeSpan delay = new TimeSpan(2, 0, 0, 0);
                                        DateTime livraison = DateTime.Now.Add(delay);
                                        string dt_livraison1 = livraison.ToString("yyyy-MM-dd");
                                        executeRequete("UPDATE commande SET date_livraison = '" + dt_livraison1 + "' WHERE Num_commande = " + num_commande + ";");
                                        done = CommandeClient(id_utilisateur, choix_prod1, qte1, quantite_dispo, num_commande, false, livraison);
                                    }
                                }
                                break;
                            case 2:
                                Console.WriteLine(Requete("SELECT Num_produit_piece, Description_piece, prix_unitaire_piece FROM piece_rechange"));
                                Console.WriteLine("Sélectionner le produit souhaité (par numéro de produit): ");
                                int choix_prod2 = int.Parse(Console.ReadLine());
                                Console.WriteLine("Quelle quantité ?");
                                int qte2 = int.Parse(Console.ReadLine());
                                TimeSpan delai = TimeSpan.Parse(Requete("SELECT delai_approvisionnement FROM piece_rechange WHERE Num_produit_piece = " + choix_prod2 +";"));
                                DateTime ajd = DateTime.Now;
                                DateTime date_livraison = ajd.Add(delai);
                                string dt_livraison = date_livraison.ToString("yyyy-MM-dd");
                                executeRequete("UPDATE commande SET date_livraison = '" + dt_livraison + "' WHERE Num_commande = " + num_commande + ";");
                                done = CommandeClient(id_utilisateur, choix_prod2, qte2, 0, num_commande, true, date_livraison);
                                break;
                        }
                    } while (! done);
                    break;
                case 2:
                    string requete;
                    Console.WriteLine("À quelle option souhaitez-vous souscrire ?");
                    Console.WriteLine("1 : Fidélio     2 : Fidélio OR   3 : Fidélio PLATINE    4 : Fidélio MAX");
                    int choix_prgm = int.Parse(Console.ReadLine());
                    switch (choix_prgm)
                    {
                        case 1:
                            requete = "UPDATE `client` SET Num_fidelite = 1 WHERE id_client = " + id_utilisateur + ";";
                            executeRequete(requete);
                            break;
                        case 2:
                            requete = "UPDATE `client` SET Num_fidelite = 2 WHERE id_client = " + id_utilisateur + ";";
                            executeRequete(requete);
                            break;
                        case 3:
                            requete = "UPDATE `client` SET Num_fidelite = 3 WHERE id_client = " + id_utilisateur + ";";
                            executeRequete(requete);
                            break;
                        case 4:
                            requete = "UPDATE `client` SET Num_fidelite = 4 WHERE id_client = " + id_utilisateur + ";";
                            executeRequete(requete);
                            break;
                    }
                    Console.WriteLine("|-| Souscription effectuée avec succès ! |-|");
                    break;
            }
        }
        static bool CommandeClient(int id_utilisateur, int choix_prod, int qte, int quantite_dispo, int num_commande, bool piece, DateTime date_livraison)
        {
            bool done = false;
            if (piece) { executeRequete("INSERT INTO ligne_commande (Num_commande, Num_produit_piece, Num_produit, quantite, id_entreprise, id_client) VALUES (" + num_commande + "," + choix_prod + ", null, " + qte + ", null, " + id_utilisateur + ");"); }
            else { executeRequete("INSERT INTO ligne_commande (Num_commande, Num_produit_piece, Num_produit, quantite, id_entreprise, id_client) VALUES (" + num_commande + ", null, " + choix_prod + ", " + qte + ", null, " + id_utilisateur + ");"); }
            Console.WriteLine("|-| Commande effectuée avec succès ! |-|");
            Console.WriteLine("|-| Vous serez livré le " + date_livraison + "|-|");
            int new_qte = quantite_dispo - qte;
            executeRequete("UPDATE modele_velo SET quantite_dispo = " + new_qte + " WHERE Num_produit = " + choix_prod + ";");
            Console.WriteLine("Souhaitez vous faire une autre commande ? \n 1 : Oui     2 : Non");
            int choix = int.Parse(Console.ReadLine());
            switch (choix)
            {
                case 1:
                    done = false;
                    break;
                case 2:
                    done = true;
                    Console.WriteLine("Déconnexion ...");
                    break;
            }
            return done;
        }
        #endregion

        #region Espace Entreprise
        static void ConnexionEntreprise()
        {
            Console.WriteLine("==== Espace entreprise ====");
            Console.WriteLine("1: Connexion     2 : Créer un compte");
            int choix = int.Parse(Console.ReadLine());
            switch (choix)
            {
                case 1:
                    Console.WriteLine("ID entreprise :");
                    int id_entreprise = int.Parse(Console.ReadLine());
                    bool valid = false;
                    string[] requete = Requete("SELECT id_entreprise FROM entreprise").Split(new char[] { '\n', '\t' });
                    for (int i = 0; i < requete.Length; i++) {if (requete[i] == Convert.ToString(id_entreprise)) {valid = true;}}
                    if (valid)
                    {
                        Console.WriteLine("Connexion ...");
                        EspaceEntreprise(id_entreprise);
                    }
                    else {Console.WriteLine("ID entreprise invalide\nRéessayez");}
                    break;
                case 2:
                    CreationEntreprise();
                    break;
            }
        }

        static void CreationEntreprise()
        {
            Console.WriteLine("==== Création Compte ====");
            bool id_ok = true;
            int id_entreprise;
            do
            {
                Console.WriteLine("ID entreprise (4 chiffres) : ");
                id_entreprise = int.Parse(Console.ReadLine());
                id_ok = true;
                string[] requete_id = Requete("SELECT id_entreprise FROM entreprise").Split(new char[] { '\n', '\t' });
                for (int i = 0; i < requete_id.Length; i++)
                {
                    if (Convert.ToString(id_entreprise) == requete_id[i])
                    {
                        Console.WriteLine("|!| ID utilisateur déjà utilisé ! Réessayez ...");
                        id_ok = false;
                    }
                }
            } while (!id_ok);
            Console.WriteLine("Nom de l'entreprise : ");
            string nom_entreprise = Console.ReadLine();
            Console.WriteLine("Adresse : ");
            string adresse = Console.ReadLine();
            Console.WriteLine("Province : ");
            string province = Console.ReadLine();
            Console.WriteLine("Téléphone : ");
            string telephone = Console.ReadLine();
            Console.WriteLine("Email : ");
            string courriel = Console.ReadLine();
            Console.WriteLine("Nom contact : ");
            string nom_contact = Console.ReadLine();
            string requete = "INSERT INTO `entreprise` (`id_entreprise`,`Nom_entreprise`,`adresse_entreprise`,`province`,`telephone`,`courriel`,`Nom_contact`,`remise`) VALUES (" + id_entreprise + "," + "'" + nom_entreprise + "'" + "," + "'" + adresse + "'," + "'" + province + "'" + "," + "'" + telephone + "'" + "," + "'" + courriel + "'" + "," + "'" + nom_contact + "'" + "," + " null )";
            executeRequete(requete);
            Console.WriteLine("|-| Compte créé avec succès ! |-|");
            
        }
        static void SuppressionEntreprise()
        {
            Console.WriteLine("Quel compte d'entreprise souhaitez-vous supprimer (id) ? ");
            Console.WriteLine(Requete("SELECT * FROM entreprise"));
            int id_entreprise = int.Parse(Console.ReadLine());
            executeRequete("DELETE FROM entreprise WHERE id_entreprise = " + id_entreprise + ";");
            Console.WriteLine("|-| Suppression effectuée avec succès ! |-|");
        }
        static void ModificationEntreprise()
        {
            Console.WriteLine("Quel compte client souhaitez-vous modifier (id) ? ");
            Console.WriteLine(Requete("SELECT * FROM entreprise"));
            int id_entreprise = int.Parse(Console.ReadLine());
            Console.WriteLine("Quel attribut souhaitez-vous modifier ? ");
            Console.WriteLine(Requete("SHOW COLUMNS FROM entreprise"));
            string attribut = Console.ReadLine();
            if (attribut == "id_entreprise")
            {
                Console.WriteLine("Quelle valeur souhaitez-vous lui attribuer ?");
                int value = int.Parse(Console.ReadLine());
                executeRequete("UPDATE entreprise SET " + attribut + " = " + value + " WHERE id_entreprise = " + id_entreprise + ";");
            }
            else
            {
                Console.WriteLine("Quelle valeur souhaitez-vous lui attribuer ?");
                string value = Console.ReadLine();
                executeRequete("UPDATE entreprise SET " + attribut + " = '" + value + "' WHERE id_entreprise = " + id_entreprise + ";");
            }
            Console.WriteLine("|-| Modification effectuée avec succès ! |-|");
            
        }
        static void EspaceEntreprise(int id_entreprise)
        {
            Console.WriteLine("==== Espace entreprise ====");
            Console.WriteLine("Faites votre commande : ");
            bool done = false;
            do
            {
                int num_commande = int.Parse(Requete("SELECT MAX(Num_commande) FROM commande")) + 1;
                string date_ajd = DateTime.Now.ToString("yyyy-MM-dd HH:mm:ss");
                executeRequete("INSERT INTO commande (Num_commande, date_commande, adresse, date_livraison, id_entreprise, id_client) VALUES (" + num_commande + ",'" + date_ajd + "','" + Requete("SELECT adresse_entreprise FROM entreprise WHERE id_entreprise = " + id_entreprise + ";") + "', null, " + id_entreprise + ",null);");
                Console.WriteLine("1 : Catalogue vélo    2 : Catalogue pièce de rechange");
                int choix_catalogue = int.Parse(Console.ReadLine());
                switch (choix_catalogue)
                {
                    case 1:
                        Console.WriteLine(Requete("SELECT * FROM modele_velo"));
                        Console.WriteLine("Sélectionner le produit souhaité (par numéro de produit) : ");
                        int choix_prod1 = int.Parse(Console.ReadLine());
                        Console.WriteLine("Quelle quantité ?");
                        int qte1 = int.Parse(Console.ReadLine());
                        string[] requete2 = Requete("SELECT * FROM modele_velo WHERE Num_produit = " + choix_prod1 + ";").Split(new char[] { '\n', '\t' });
                        int quantite_dispo1 = int.Parse(requete2[7]);
                        if (quantite_dispo1 == 0)
                        {
                            Console.WriteLine("|!| Erreur : Ce produit n'est plus disponible ! ");
                            executeRequete("DELETE FROM commande WHERE Num_commande = " + num_commande + ";");
                        }
                        else
                        {
                            if (qte1 > quantite_dispo1)
                            {
                                Console.WriteLine("|!| Erreur : Nous n'avons pas assez d'exemplaires de ce produit ! ");
                                executeRequete("DELETE FROM commande WHERE Num_commande = " + num_commande + ";");
                            }
                            else
                            {
                                TimeSpan delay = new TimeSpan(2, 0, 0, 0);
                                DateTime livraison = DateTime.Now.Add(delay);
                                string dt_livraison1 = livraison.ToString("yyyy-MM-dd");
                                executeRequete("UPDATE commande SET date_livraison = '" + dt_livraison1 + "' WHERE Num_commande = " + num_commande + ";");
                                done = CommandeEntreprise(id_entreprise, choix_prod1, qte1, quantite_dispo1, num_commande, false, livraison);
                            }
                        }
                        break;
                    case 2:
                        Console.WriteLine(Requete("SELECT Num_produit_piece, Description_piece, prix_unitaire_piece FROM piece_rechange"));
                        Console.WriteLine("Sélectionner le produit souhaité (par numéro de produit): ");
                        int choix_prod2 = int.Parse(Console.ReadLine());
                        Console.WriteLine("Quelle quantité ?");
                        int qte2 = int.Parse(Console.ReadLine());
                        TimeSpan delai = TimeSpan.Parse(Requete("SELECT delai_approvisionnement FROM piece_rechange WHERE Num_produit_piece = " + choix_prod2 + ";"));
                        DateTime ajd = DateTime.Now;
                        DateTime date_livraison= ajd.Add(delai);
                        string dt_livraison = date_livraison.ToString("yyyy-MM-dd");
                        executeRequete("UPDATE commande SET date_livraison = '" + dt_livraison + "' WHERE Num_commande = " + num_commande + ";");
                        done = CommandeEntreprise(id_entreprise, choix_prod2, qte2, 0, num_commande, true, date_livraison);
                        break;
                }
            } while (!done);
        }

        static bool CommandeEntreprise(int id_entreprise, int choix_prod, int qte, int quantite_dispo, int num_commande, bool piece, DateTime date_livraison)
        {
            bool done = false;
            if (piece) 
            { executeRequete("INSERT INTO ligne_commande (Num_commande, Num_produit_piece, Num_produit, quantite, id_entreprise, id_client) VALUES (" + num_commande + "," + choix_prod + ", null, " + qte + "," + id_entreprise + ", null);");}
            else { executeRequete("INSERT INTO ligne_commande (Num_commande, Num_produit_piece, Num_produit, quantite, id_entreprise, id_client) VALUES (" + num_commande + ", null, " + choix_prod + ", " + qte + "," + id_entreprise + ", null );"); }
            Console.WriteLine("|-| Commande effectuée avec succès ! |-|");
            Console.WriteLine("|-| Vous serez livré le " + date_livraison + "|-|");
            int new_qte = quantite_dispo - qte;
            executeRequete("UPDATE modele_velo SET quantite_dispo = " + new_qte + " WHERE Num_produit = " + choix_prod + ";");
            Console.WriteLine("Souhaitez vous faire une autre commande ? \n 1 : Oui     2 : Non");
            int choix = int.Parse(Console.ReadLine());
            switch (choix)
            {
                case 1:
                    done = false;
                    break;
                case 2:
                    done = true;
                    Console.WriteLine("Déconnexion ...");
                    break;
            }
            return done;
        }
        #endregion

        #region Espace Fournisseur
        static void CreationFournisseur()
        {
            Console.WriteLine("==== Création Fournisseur ====");
            Console.WriteLine("SIRET : ");
            int siret = int.Parse(Console.ReadLine());
            Console.WriteLine("Nom entreprise : ");
            string nom_entreprise = Console.ReadLine();
            Console.WriteLine("Contact : ");
            string contact = Console.ReadLine();
            Console.WriteLine("Adresse : ");
            string adresse = Console.ReadLine();
            Console.WriteLine("Libellé : ");
            string libelle = Console.ReadLine();
            string requete = "INSERT INTO `fournisseur` (`siret`,`Nom_entreprise`,`contact`,`adresse_entreprise`,`libelle`) VALUES (" + siret + ",'" + nom_entreprise + "','" + contact + "','" + adresse + "','" + libelle + "');";
            executeRequete(requete);
            Console.WriteLine("|-| Fournisseur créé avec succès ! |-|");
            
        }
        static void ModificationFournisseur()
        {
            Console.WriteLine("Quel fournisseur souhaitez-vous modifier (siret) ? ");
            Console.WriteLine(Requete("SELECT * FROM fournisseur"));
            int siret = int.Parse(Console.ReadLine());
            Console.WriteLine("Quel attribut souhaitez-vous modifier ? ");
            Console.WriteLine(Requete("SHOW COLUMNS FROM fournisseur"));
            string attribut = Console.ReadLine();
            if (attribut == "siret")
            {
                Console.WriteLine("Quelle valeur souhaitez-vous lui attribuer ?");
                int value = int.Parse(Console.ReadLine());
                executeRequete("UPDATE fournisseur SET " + attribut + " = " + value + " WHERE siret = " + siret + ";");
            }
            else
            {
                Console.WriteLine("Quelle valeur souhaitez-vous lui attribuer ?");
                string value = Console.ReadLine();
                executeRequete("UPDATE fournisseur SET " + attribut + " = '" + value + "' WHERE siret = " + siret + ";");
            }
            Console.WriteLine("|-| Modification effectuée avec succès ! |-|");
            
        }
        static void SuppressionFournisseur()
        {
            Console.WriteLine("Quel fournisseur souhaitez-vous supprimer (siret) ? ");
            Console.WriteLine(Requete("SELECT * FROM fournisseur"));
            int siret = int.Parse(Console.ReadLine());
            executeRequete("DELETE FROM fournisseur WHERE siret = " + siret + ";");
            Console.WriteLine("|-| Suppression effectuée avec succès ! |-|");
            
        }

       
        #endregion

        #region Espace Employé
        static void EspaceEmployé()
        {
            Console.WriteLine("==== Espace employé ====");
            Console.WriteLine("1 : Gestion des fournisseurs   2 : Gestion des clients et entreprises     3 : Gestion des commandes    4 : Gestion du stock      5 : Module statistique");
            int choix = int.Parse(Console.ReadLine());
            switch (choix)
            {
                case 1:
                    Console.WriteLine("==== Gestion des fournisseurs ====");
                    Console.WriteLine("1 : Créer      2 : Supprimer     3 : Modifier ");
                    int choix_fournisseur = int.Parse(Console.ReadLine());
                    switch (choix_fournisseur)
                    {
                        case 1:
                            CreationFournisseur();
                            break;
                        case 2:
                            SuppressionFournisseur();
                            break;
                        case 3:
                            ModificationFournisseur();
                            break;

                    }
                    break;
                case 2:
                    Console.WriteLine("==== Gestion des clients et entreprises ====");
                    Console.WriteLine("1 : Client      2 : Entreprise");
                    int choix_ce = int.Parse(Console.ReadLine());
                    switch (choix_ce)
                    {
                        case 1:
                            Console.WriteLine("==== Gestion clients ====");
                            Console.WriteLine("1 : Créer un compte      2 : Supprimer un compte     3 : Modifier un compte");
                            int choix_client = int.Parse(Console.ReadLine());
                            switch (choix_client)
                            {
                                case 1:
                                    CreationClient();
                                    break;
                                case 2:
                                    SuppressionClient();
                                    break;
                                case 3:
                                    ModificationClient();
                                    break;
                            }
                            break;
                        case 2:
                            Console.WriteLine("==== Gestion entreprises ====");
                            Console.WriteLine("1 : Créer un compte      2 : Supprimer un compte     3 : Modifier un compte");
                            int choix_entreprise = int.Parse(Console.ReadLine());
                            switch (choix_entreprise)
                            {
                                case 1:
                                    CreationEntreprise();
                                    break;
                                case 2:
                                    SuppressionEntreprise();
                                    break;
                                case 3:
                                    ModificationEntreprise();
                                    break;
                            }
                            break;
                    }
                    break;
                case 3:
                    Console.WriteLine("==== Gestion commande ====");
                    Console.WriteLine("1 : Créer une commande      2 : Supprimer une commande     3 : Modifier une commande");
                    int choix_commande = int.Parse(Console.ReadLine());
                    switch (choix_commande)
                    {
                        case 1:
                            CreationCommande();
                            break;
                        case 2:
                            SuppressionCommande();
                            break;
                        case 3:
                            ModificationCommande();
                            break;
                    }
                    break;
                case 4:
                    GestionStock();
                    break;
                case 5:
                    ModuleStat();
                    break;
            }
        }
        #endregion

        #region Gestion Stock
        static void GestionStock()
        {
            Console.WriteLine("==== Gestion du stock ====");
            Console.WriteLine("1 : Stock vélo      2 : Stock pièce     3 : Livraison fournisseur");
            int choix_stock = int.Parse(Console.ReadLine());
            switch (choix_stock)
            {
                case 1:
                    Console.WriteLine(Requete("SELECT * FROM modele_velo"));
                    for (int num_produit = 101; num_produit <= 115; num_produit++)
                    {
                        string[] requete = Requete("SELECT * FROM modele_velo WHERE Num_produit = " + num_produit + ";").Split(new char[] { '\n', '\t' });
                        int quantite = int.Parse(requete[7]);
                        if (quantite == 0)
                        {
                            Console.WriteLine("|!| Attention, le produit numéro " + num_produit + " est à cours de stock ! ");
                        }
                    }
                    
                    break;
                case 2:
                    Console.WriteLine("==== Stock des pièces ====");
                    Console.WriteLine("Num_produit_piece,Description_piece,Nom_fournisseur,Num_produit_fournisseur,prix_unitaire_piece,date_intro,date_discontinuation,delai_approvisionnement,siret");
                    Console.WriteLine(Requete("SELECT * FROM piece_rechange"));
                    
                    break;
                case 3:
                    LivraisonProduit();
                    
                    break;
            }
        }

        static void LivraisonProduit()
        {
            Console.WriteLine("==== Livraison ====");
            Console.WriteLine("1: Livraison vélo        2 : Livraison pièce");
            int choix_livre = int.Parse(Console.ReadLine());
            switch (choix_livre)
            {
                case 1:
                    Console.WriteLine(Requete("SELECT * FROM modele_velo"));
                    Console.WriteLine("Quel produit a été livré ?");
                    int num_produit = int.Parse(Console.ReadLine());
                    Console.WriteLine("Quelle quantité ?");
                    int newquantite = int.Parse(Console.ReadLine());
                    string[] requete = Requete("SELECT * FROM modele_velo WHERE Num_produit = " + num_produit + ";").Split(new char[] { '\n', '\t' });
                    int oldquantite = int.Parse(requete[7]);
                    int quantite = oldquantite + newquantite;
                    executeRequete("UPDATE modele_velo SET quantite_dispo = " + quantite + " WHERE Num_produit = " + num_produit + ";");
                    Console.WriteLine("|-| Produit ajouté avec succès |-|");
                    break;
                case 2:
                    Console.WriteLine("Numéro produit : ");
                    int num_prod = int.Parse(Console.ReadLine());
                    Console.WriteLine("Description : ");
                    string desc = Console.ReadLine();
                    Console.WriteLine("Nom du fournisseur : ");
                    string nom_fournisseur = Console.ReadLine();
                    Console.WriteLine("Numéro du produit chez le fournisseur : ");
                    int num_prod_fournisseur = int.Parse(Console.ReadLine());
                    Console.WriteLine("Prix unitaire : ");
                    int prix_unitaire = int.Parse(Console.ReadLine());
                    Console.WriteLine("Date d'introduction : ");
                    string date_int = Console.ReadLine();
                    Console.WriteLine("Date de discontinuation : ");
                    string date_disc = Console.ReadLine();
                    Console.WriteLine("Délai approvisionnement : ");
                    string delai = Console.ReadLine();
                    Console.WriteLine("SIRET fournisseur : ");
                    int siret = int.Parse(Console.ReadLine());
                    string requete1 = "INSERT INTO `piece_rechange` (`Num_produit_piece`,`Description_piece`,`Nom_fournisseur`,`Num_produit_fournisseur`,`prix_unitaire_piece`, date_intro, date_discontinuation, delai_approvisionnement, siret) VALUES (" + num_prod + ",'" + desc + "','" + nom_fournisseur + "'," + num_prod_fournisseur + "," + prix_unitaire + ",'" + date_int + "','" + date_disc + "','" + delai + "'," + siret + "); ";
                    executeRequete(requete1);
                    Console.WriteLine("|-| Produit ajouté avec succès |-|");
                    break;
            }
        }
        #endregion

        #region Gestion commande
        static void CreationCommande()
        {
            Console.WriteLine("==== Création Commande ====");
            int num_commande = int.Parse(Requete("SELECT COUNT(*) FROM commande")) + 1;
            Console.WriteLine("Date de la commande : ");
            string date_commande = Console.ReadLine();
            Console.WriteLine("Adresse de livraison : ");
            string adresse = Console.ReadLine();
            Console.WriteLine("Date de livraison : ");
            string date_livraison = Console.ReadLine();
            Console.WriteLine("ID entreprise : ");
            string id_entreprise = Console.ReadLine();
            Console.WriteLine("ID client : ");
            string id_client = Console.ReadLine();
            string requete = "INSERT INTO commande (`Num_commande`,`date_commande`,`adresse`,`date_livraison`,`id_entreprise`, id_client) VALUES (" + num_commande + ",'" + date_commande + "','" + adresse + "','" + date_livraison + "'," + id_entreprise + "," + id_client + ");";
            executeRequete(requete);
            Console.WriteLine("|-| Commande créé avec succès ! |-|");
            
        }
        static void SuppressionCommande()
        {
            Console.WriteLine("Quel commande souhaitez-vous supprimer (num_commande) ? ");
            Console.WriteLine(Requete("SELECT * FROM commande"));
            int num_commande = int.Parse(Console.ReadLine());
            executeRequete("DELETE FROM commande WHERE Num_commande = " + num_commande + ";");
            executeRequete("DELETE FROM ligne_commande WHERE Num_commande = " + num_commande + ";");
            Console.WriteLine("|-| Suppression effectuée avec succès ! |-|");
            
        }
        static void ModificationCommande()
        {
            Console.WriteLine("Quel commande souhaitez-vous modifier (num_commande) ? ");
            Console.WriteLine(Requete("SELECT * FROM commande"));
            int num_commande = int.Parse(Console.ReadLine());
            Console.WriteLine("Quel attribut souhaitez-vous modifier ? ");
            Console.WriteLine(Requete("SHOW COLUMNS FROM commande"));
            string attribut = Console.ReadLine();
            if (attribut == "Num_commande" || attribut == "id_entreprise" || attribut == "id_cleint")
            {
                Console.WriteLine("Quelle valeur souhaitez-vous lui attribuer ?");
                int value = int.Parse(Console.ReadLine());
                executeRequete("UPDATE commande SET " + attribut + " = " + value + " WHERE Num_commande = " + num_commande + ";");
            }
            else
            {
                Console.WriteLine("Quelle valeur souhaitez-vous lui attribuer ?");
                string value = Console.ReadLine();
                executeRequete("UPDATE commande SET " + attribut + " = '" + value + "' WHERE Num_commande = " + num_commande + ";");
            }
            Console.WriteLine("|-| Modification effectuée avec succès ! |-|");
            
        }
        #endregion

        #region Mode demo
        static void Demo()
        {
            // 1)
            string[] requete1 = Requete("SELECT COUNT(*) FROM client").Split(new char[] { '\n', '\t' });
            int nb_client = int.Parse(requete1[2]);
            Console.WriteLine("\n\n\n\nLe nombre de clients inscrits sur la plateforme est de " + nb_client);
            // 2)
            Console.WriteLine("\n\n\n\nLe cumul des dépenses par nom de client : ");
            Console.WriteLine(Requete("SELECT c.Nom_client, SUM(l.quantite * v.prix_unitaire) FROM client c JOIN ligne_commande l JOIN modele_velo v ON c.id_client = l.id_client AND v.Num_produit = l.Num_produit GROUP BY c.Nom_client;"));
            Console.WriteLine("\n\n\n\nListe des produits ayant une quantité en stock <= 2 : ");
            Console.WriteLine(Requete("SELECT * FROM modele_velo WHERE quantite_dispo <= 2;"));
            // 4)
            Console.WriteLine("\n\n\n\nNombres de pièces fournis par fournisseur :");
            Console.WriteLine("Nom_fournisseur, nombre de pièces fournies");
            Console.WriteLine(Requete("SELECT Nom_fournisseur, Count(*) FROM piece_rechange GROUP BY siret;"));
        }
        #endregion

        #region Module Statistique
        static void ModuleStat()
        {
            Console.WriteLine("==== Module Statistique ===");
            Console.WriteLine("Quantités vendues de chaque produit de l'inventaire :");
            Console.WriteLine("Numéro produit, quantité");
            Console.WriteLine(Requete("SELECT Num_produit_piece, SUM(quantite) FROM ligne_commande GROUP BY Num_produit_piece HAVING Num_produit_piece IS NOT NULL "));
            Console.WriteLine(Requete("SELECT Num_produit, SUM(quantite) FROM ligne_commande GROUP BY Num_produit HAVING Num_produit IS NOT NULL") + "\n\n\n");
            Console.WriteLine("Liste des membres pour chaque programme d’adhésion :");
            Console.WriteLine("Programme fidélité, Nom, Prénom");
            Console.WriteLine(Requete("SELECT  f.Nom_fidelite, c.Nom_client, c.Prenom_client FROM fidelite f NATURAL JOIN client c ORDER BY f.Num_fidelite") + "\n\n\n");
            //Console.WriteLine("Date d'expiration des programmes :");
            //int duree = int.Parse(Requete("SELECT duree FROM fidelite"));
            Console.WriteLine("Liste des clients par nombre de produits commandés :");
            Console.WriteLine(Requete("SELECT c.Nom_client, c.Prenom_client, SUM(quantite) FROM client c JOIN ligne_commande l ON c.id_client = l.id_client GROUP BY l.id_client ORDER BY SUM(quantite) DESC" + "\n\n\n"));
            int somme_piece = int.Parse(Requete("SELECT SUM(p.prix_unitaire_piece * l.quantite) FROM piece_rechange p JOIN ligne_commande l ON p.Num_produit_piece = l.Num_produit_piece"));
            int somme_velo = int.Parse(Requete("SELECT SUM(m.prix_unitaire * l.quantite) FROM modele_velo m JOIN ligne_commande l ON m.Num_produit = l.Num_produit"));
            int quantite = int.Parse(Requete("SELECT COUNT(*) FROM ligne_commande"));
            int moyenne = (somme_velo + somme_piece) / quantite;
            Console.WriteLine("\n\n\nLa moyenne des montants des commandes est de " + moyenne + " euros");
            
        }
        #endregion 
    }
}

