from PIL import Image as PILImage, UnidentifiedImageError
from django.core.exceptions import ValidationError
import os,re

################################

#Image

################################
def upload_location(instance, filename):
    """
    Normalise les noms des images dans la base, en se basant sur le numero de document CESR qui est unique et obligatoire
    
    Paramètres :  instance: Objet Image défini dans models .
                  filename: chemin du fichier image que l'on cherche a uploader dans la base.
                  
    Renvoie le chemin ou sera enregistrée l'image
    """
    filebase, extension = filename.split('.')
    return 'bdd_icono/hd/%s.%s' % (instance.n_cesr, extension)

def miniatures(image_dossier, chemin_miniatures):
    """
    Génère une miniature basse résolution pour une image et l'enregistre dans chemin_miniatures.
    
    Paramètres :  image_dossier: Chemin vers l'image source.
                  chemin_miniatures: Chemin où enregistrer la miniature générée.
    """
    # Taille de la basse résolution pour la miniature
    basse_resolution = (800, 600)
    
    try:
        # Ouvre l'image à partir du chemin donné
        image = PILImage.open(image_dossier)
        # Obtient la largeur et la hauteur de l'image originale
        largeur, hauteur = image.size
        # Calcule le ratio de l'image (largeur/hauteur)
        ratio = largeur / hauteur

        # Calcule les dimensions de la nouvelle image en gardant le même ratio pour éviter les déformations
        if largeur / basse_resolution[0] > hauteur / basse_resolution[1]:
            nouvelle_largeur = basse_resolution[0]
            nouvelle_hauteur = int(nouvelle_largeur / ratio)
        else:
            nouvelle_hauteur = basse_resolution[1]
            nouvelle_largeur = int(nouvelle_hauteur * ratio)

        # Redimensionne l'image en utilisant le filtre LANCZOS pour une meilleure qualité
        image_bassedef = image.resize((nouvelle_largeur, nouvelle_hauteur), PILImage.Resampling.LANCZOS)

        # Extrait le nom de fichier sans extension de l'image source
        nom_fichier_sans_ext = os.path.splitext(os.path.basename(image_dossier))[0]
        # Crée le chemin complet pour sauvegarder la miniature
        dossier_miniature = os.path.join(chemin_miniatures, f"{nom_fichier_sans_ext}.jpg")

        # Sauvegarde l'image redimensionnée en tant que fichier JPEG
        image_bassedef.save(dossier_miniature, "JPEG")

    except (UnidentifiedImageError, IOError) as e:
        # Gestion des erreurs lors de l'ouverture ou de la modification de l'image
        print(f"Erreur lors de l'ouverture de {image_dossier}: {e}")
        
################################

#Extrait_de

################################

def validation_date_creation(value):
    """
    Validation du champ date_creation.
    Format accepté : AAAA, Avant AAAA, Vers AAAA, Après AAAA, AAAA - AAAA, Vers AAAA - AAAA
    """
    pattern = re.compile(r'^(Avant|Vers|Après )?\d{3,4}( - \d{3,4})?$')
    if not pattern.match(value):
        raise ValidationError(
            ('Format de date invalide. Utilisez : "AAAA", "Avant AAAA", "Vers AAAA", "Après AAAA", "AAAA - AAAA", "Vers AAAA - AAAA".'),
            params={'value': value},
        )

def validation_periode_creation(value):
    """
    Validation du champ periode_creation.
    Format accepté : 1 e Siècle, Avant 16 e Siècle, Vers 8 e Siècle, Après 15 e Siècle, 14 e Siècle - 15 e Siècle
    """
    pattern = re.compile(r'^(Avant|Vers|Après )?\d{1,2}e Siècle( - \d{1,2}e Siècle)?$')
    if not pattern.match(value):
        raise ValidationError(
            ('Format de période invalide. Utilisez : "4 e Siècle", "Avant 17 e Siècle", "Vers 10 e Siècle", "Après 15 e Siècle", "16 e Siècle - 17 e Siècle".'),
            params={'value': value},
        )


