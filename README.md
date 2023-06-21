# EPICEvent CRM

## Requirements

+ [Python v3+](https://www.python.org/downloads/)
+ [Django](https://www.djangoproject.com/download/)
+ [Django REST](https://www.django-rest-framework.org/)
+ [PostGres SQL](https://www.postgresql.org/download/)

## Installation & Get Started

#### Récuperer le projet sur GitHub

    git clone https://github.com/JLenseele/Project_12
    cd Project_12

#### Créer l'environement virtuel

    python -m venv env
    env\Scripts\activate
    pip install -r requirements.txt
    
#### Lancer le serveur

    python epicevent\manage.py runserver

## Current Setup

Cette application fonctionne avec une BDD PostGres.  
db.sqlite3  
  
#### Connexion et utilisation

Voici la liste des utilisateurs préalablement enregistrés dans la bdd.
Ils vous permettront de tester les fonctionnalités du CRM.

Team Management :

    admin@admin.com
    pwd : admin

    camille@gmail.com
    pwd : Axr456789

Team Ventes :

    password : Axr456789
    
    - xavier@gmail.com
    - noemie@gmail.com

    READ : All model
    UPDATE : All model quand l'user est "sales_contact" du client
    CREATE : Client /
             Contrat, Event quand l'user est sales_contact du client
    

Team Support :

    password : Axr456789

    - clement@gmail.com
    - antoine@gmail.com

    READ : All model
    UPDATE : Evenement dont l'user est "support_contact"

## Contributors

[JLenseele](https://github.com/JLenseele)
