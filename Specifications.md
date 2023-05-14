# Projet Développement Web : Banque en Ligne 

## Technologies : 
Back : Python (Flask Framework) <br>
Front : HTML, CSS, Javascript <br>
BDD : sqlite3 
<br> <br>
### Fonctionnalités : 
Gérer son budget personnel <br> <br>

### Schèma de la BDD : 

**TABLE Users** : <br>
```
- id_user	            int auto_increment (Primary key)
- first_name	        string	NOT NULL
- last_name	            string	NOT NULL
- gender		        string 	NOT NULL
- password	            int	NOT NULL
- email		            string (unique) NOT NULL
- phone_number	        int	NOT NULL
- birthday	            date NOT NULL
- address	            string NOT NULL
- role		            string NOT NULL
```

**TABLE Monthly_savings** : <br>
```
- id_monthly_saving		int auto_increment (Primary key)
- id_account		    int (Foreign key)
- ammount		        int NOT NULL
- operation_type	    string NOT NULL
- date	                date NOT NULL
```

**TABLE Transactions** : <br>
```
- transaction_id		int auto_increment (Primary key)
- id_account		    int (Foreign key)
- beneficiary_name		string NOT NULL
- operation_type	    string NOT NULL
- amount		        int NOT NULL
- transaction_date	    date NOT NULL
```

**TABLE Account** : <br>
```
- id_account	        int auto_increment (Primary key)
- id_user		        int (Foreign key)
- card_nb		        int	NOT NULL
- name			        string NOT NULL
- solde			        int
- creation_date	        date NOT NULL
```