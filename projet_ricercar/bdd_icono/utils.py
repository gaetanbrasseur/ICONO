from PIL import Image as PILImage, UnidentifiedImageError
import os

def miniatures(image_dossier, chemin_miniatures):
    """
    Génère une miniature basse résolution pour une image et l'enregistre dans chemin_miniatures.
    
    paramètres :  image_dossier: Chemin vers l'image source.
                  chemin_miniatures: Chemin où sauvegarder la miniature générée.
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
