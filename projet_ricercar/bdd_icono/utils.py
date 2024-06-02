from PIL import Image as PILImage, UnidentifiedImageError
import os


def miniatures(image_dossier, chemin_miniatures):
    """
    Génère une miniature pour une image et l'enregistre dans chemin_miniatures.
    """
    basse_resolution = (800, 600)
    
    try:
        image = PILImage.open(image_dossier)
        largeur, hauteur = image.size
        ratio = largeur / hauteur

        if largeur / basse_resolution[0] > hauteur / basse_resolution[1]:
            nouvelle_largeur = basse_resolution[0]
            nouvelle_hauteur = int(nouvelle_largeur / ratio)
        else:
            nouvelle_hauteur = basse_resolution[1]
            nouvelle_largeur = int(nouvelle_hauteur * ratio)

        image_bassedef = image.resize((nouvelle_largeur, nouvelle_hauteur), PILImage.Resampling.LANCZOS)

        nom_fichier_sans_ext = os.path.splitext(os.path.basename(image_dossier))[0]
        dossier_miniature = os.path.join(chemin_miniatures, f"{nom_fichier_sans_ext}.jpg")

        image_bassedef.save(dossier_miniature, "JPEG")

    except (UnidentifiedImageError, IOError) as e:
        print(f"Erreur lors de l'ouverture de {image_path}: {e}")
