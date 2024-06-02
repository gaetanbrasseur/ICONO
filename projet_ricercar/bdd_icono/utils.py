from PIL import Image as PILImage, UnidentifiedImageError
import os

def miniatures(image_path, output_dir):
    """
    Génère une miniature basse définition pour une image et l'enregistre dans output_dir.
    """
    basse_resolution = (800, 600)
    
    try:
        image = PILImage.open(image_path)
        largeur, hauteur = image.size
        ratio = largeur / hauteur

        if largeur / basse_resolution[0] > hauteur / basse_resolution[1]:
            nouvelle_largeur = basse_resolution[0]
            nouvelle_hauteur = int(nouvelle_largeur / ratio)
        else:
            nouvelle_hauteur = basse_resolution[1]
            nouvelle_largeur = int(nouvelle_hauteur * ratio)

        image_bassedef = image.resize((nouvelle_largeur, nouvelle_hauteur), PILImage.Resampling.LANCZOS)

        nom_fichier_sans_ext = os.path.splitext(os.path.basename(image_path))[0]
        thumbnail_path = os.path.join(output_dir, f"{nom_fichier_sans_ext}.jpg")

        image_bassedef.save(thumbnail_path, "JPEG")

    except (UnidentifiedImageError, IOError) as e:
        print(f"Erreur lors de l'ouverture de {image_path}: {e}")
