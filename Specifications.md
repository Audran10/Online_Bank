# Projet Développement Web : Banque en Ligne 

## Technologies : 
Python, Framework  : Flask 
BDD : sqlite3 
<br> 
### Fonctionnalités : 

Gérer son budget personnel, familial et recevoir des suggestions d’investissements personnalisés. 


### I. Vue Utilisateur : <br> 

#### A) Onglet Budget :  
Création de diagramme circulaires montrant le pourcentage de dépenses réalisés par rapport au revenu 
Création de diagramme en barre montrant le montant d’argent économisé et le montant d’argent dépensé 
Génération de tableaux montrant : 
Les différentes sources de revenus et leur montant 
Les différents types de dépenses et leur montant 
Le montant des économies par mois 

#### B) Onglet Rappels : 
Rappels de paiement pour les factures, prêts immobiliers, dettes…

#### C) Onglet Investissement : 
Suggestion d’investissement par secteurs : immobilier, numériques, énergies…
Possibilité d’investissement (crowdfunding type boursorama)
Affichage des informations

#### D) Onglet Objectif : 
Possibilité d’ajouter un événement, une somme à économiser et une date pour cet événement (ex : un voyage à Hawaï en Juillet d’une valeur de 2500€)

#### E) Onglet Profil : 
Informations personnelles
Possibilité de modifier son mot de passe 
Possibilité d’ajouter une deuxième carte de crédit <br> <br>

### II. Vue Admin : 
Possibilité de créer des dépenses par catégories pour un utilisateur 
Possibilité d’accepter ou non un prêt
Création & Modification & Suppression de compte <br> <br>

### Schèma de la BDD : 

**TABLE Users** : <br>
```
- id_user	            int auto_increment (Primary key)
- first_name	        string	NOT NULL
- last_name	            string	NOT NULL
- sex		            string 	NOT NULL
- password	            int	NOT NULL
- email		            string (unique) NOT NULL
- phone_nb	            int	NOT NULL
- birthday	            date NOT NULL
- address	            string NOT NULL
- role		            string NOT NULL
```

**TABLE Account** : <br>
```
- id_account	        int auto_increment (Primary key)
- id_user		        int auto_increment (Foreign key)
- card_nb		        int	NOT NULL
- name			        string NOT NULL
- solde			        int
- creation_date	        date NOT NULL
- end_date		        date NOT NULL
```

**TABLE Bank_accounts** : <br>
```
- id_bank_account	    int auto_increment (Primary key)
- Id_account		    int auto_increment (Foreign key) 
```

**TABLE Loan** : <br>
```
- id_loan		        int auto_increment (Primary key)
- id_account		    int auto_increment (Foreign key)
- duration		        string NOT NULL
- loan_amount		    int NOT NULL
- interest		        int NOT NULL
- amount_reimbursed     int NOT NULL
- monthly_payment	    int	NOT NULL
- start_date		    date	
- end_date		        date
- status			    string NOT NULL
```

**TABLE Transactions** : <br>
```
- transaction_id		int auto_increment (Primary key)
- id_account		    int auto_increment (Foreign key)
- beneficiary_name		string NOT NULL
- operation_type	    string NOT NULL
- amount		        int NOT NULL
- transaction_date	    date NOT NULL
```