# ICONO

Setup : 

Pour la production, on va utiliser le meme système que durant le cours de Mme Piat

Installation de nouveaux modules : verifier son installation en comparant le requirements.txt avec son enviroement en utilisant la commande suivante : 

pip list

Si il y a des différences, installer les modules manquants

Création de la base de données sur pgMyAdmin : bdd_icono
Effectuer les migrations sur django
Ensuite, à l'aide du JeuTest.sql, on importe les données directement dans pgAdmin à l'aide de l'outil requêtes

Modifications du settings.py : 

Ligne 33:

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'bdd_icono.apps.BddIconoConfig',
    'crispy_forms',
    'crispy_bootstrap5'
]

Ligne 124 :

import os
STATIC_ROOT = os.path.join(BASE_DIR, 'bdd_icono','static')
STATIC_URL = 'static/'

MEDIA_ROOT = os.path.join(BASE_DIR,'bdd_icono', 'media')
MEDIA_URL = 'media/'

Fin du document :

MOT_CLE_TYPE_CHOICES = [
    ('generique', 'Générique'),
    ('chant', 'Chant'),
    ('instrument', 'Instrument de musique'),
]

A la suite, ajouter pour les connexions :

LOGIN_URL = 'login'
LOGOUT_URL = 'logout'

LOGIN_REDIRECT_URL = '/'  
LOGOUT_REDIRECT_URL = '/'  


