# Projet Développement Web : Banque en Ligne 

Ce projet consiste en une application web de gestion de budget personnel et de comptes bancaires en ligne, développée en Python avec le framework Flask pour le back-end, et en HTML, CSS et Javascript pour le front-end. La base de données utilisée est sqlite3.

## Prérequis 

Python - https://www.python.org/downloads/

## 1. Utilisation

```
python views.py
```

## 2. Installation

```
pip install -r requirements.txt
```

## 3. Fonctionnalités

### I. Vue Utilisateur : <br> <br>

#### A) Onglet Budget :  
Création de diagramme circulaires montrant le pourcentage de dépenses réalisés par rapport au revenu <br> 
Création de diagramme en barre montrant le montant d’argent économisé et le montant d’argent dépensé <br>
Génération de tableaux montrant : <br>
- Les différentes sources de revenus et leur montant 
- Les différents types de dépenses et leur montant 
- Le montant des économies par mois <br> <br>

#### B) Onglet Création de Comptes Bancaires : 
Possibilité pour chaque utilisateur de créer au maximum deux comptes d'épargne différents ("A Account", "DDS Account") avec une somme minimum de 50 euros à l'ouverture de chaque compte épargne <br> <br>

#### C) Onglet Transactions : 
Possibilité de créer une nouvelle transaction pour un utilisateur en précisant la valeur de la transaction : <br>
    - Crédit ou Débit de son compte principal ("Checking Account") <br>
Possibilité de s'effectuer un virement vers un de ses deux autres comptes : <br>
    -  Crédit ou Débit entre le compte principal ("Checking Account") et les comptes d'épargne ("A Account", "DDS Account") <br> <br>

#### D) Onglet Profil : 
Informations personnelles
Possibilité de modifier son addresse mail, son numéro de téléphone, son addresse de domicile et son mot de passe <br>
Possibilité de consulter ses différents comptes bancaires (type de compte, numéro de carte si c'est le compte principal, la date de création) <br> <br>

### II. Vue Admin : 
Possibilité de créer des dépenses par catégories pour un utilisateur pour son compte bancaire principal <br>
Consultation de la liste des utilisateurs (prénom, nom, addresse mail et numéro de téléphone)<br> <br>

Pour consulter la structure de la base de données et des tables, veuillez vous référer au document [Specifications.md](./Specifications.md).
