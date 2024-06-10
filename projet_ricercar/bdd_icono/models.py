from django.db import models
from django.conf import settings
from .utils import miniatures,upload_location,validation_date_creation,validation_periode_creation
import os
from django.utils.translation import gettext_lazy as _

################################

#Tables

################################

class Image(models.Model):
    #Champs de la table image
    legende = models.TextField(null=True, blank=True, verbose_name='Légende')
    description = models.TextField(null=False, blank=False,verbose_name='Description libre', help_text='Indiquez une description de l\'image')
    existe_en_physique = models.BooleanField(null=False, blank=False, default=True)
    cote = models.CharField(max_length=150, null=True, blank=True, verbose_name = 'Cote', help_text='Indiquez la cote, en cas d\'image provenant d\'extrait pouvant être catalogué (manuscrit, livre, lettre, acte officiel etc.)')
    
    #Le champ n_cesr sert de réference pour les noms des fichiers images
    n_cesr = models.CharField(max_length=150, null=False, blank=False, verbose_name = 'numéro de document CESR', help_text=' Format : im_0000')
    
    #Le champ image_format est un peu redondant, donc on le génère automatiquement à l'aide du fichier téléversé et ne l'affiche pas dans l'administration pour éviter les confusions
    image_format = models.CharField(null=False, blank=False, verbose_name="Format de l'image", editable=False)
    mode = models.CharField(choices=[('Couleur', 'Couleur'), ('N & B', 'Noir et blanc'),('NR','Non-renseigné')], null=False, blank=False,default='Couleur', verbose_name='Mode')
    resolution = models.CharField(max_length=50, null=False, blank=False, default='non-renseigné', verbose_name = 'Résolution', help_text='Indiquez la résolution de l\'image en DPI.')
    photographie_type = models.CharField(choices=[('numerique', 'Numérique'), ('photo', 'Photo'),('NR','Non-renseigné')],default='numerique', null=False, blank=False, verbose_name="Type de photographie")
    credit = models.CharField(max_length=250, null=True, blank=True, verbose_name = "Crédit", help_text='Indiquez les crédits relatifs à la photographie.')
    lien_telechargement = models.ImageField(upload_to=upload_location, null=False, blank=False, verbose_name='Dépôt du fichier image', help_text='Les images doivent être de format TIFF ou JPEG.')
    permalien = models.CharField(max_length=250, null=True, blank=True, help_text='Indiquez ici un lien vers le site de l\'institution qui fournit la photographie.')
    n_cliche_numerique = models.CharField(max_length=250, null=True, blank=True, verbose_name = "Numéro de cliché numérique")
    n_cliche_photo = models.CharField(max_length=250, null=True, blank=True,  verbose_name = "Numéro de cliché physique")
    fk_photographe = models.ForeignKey('Photographe', on_delete=models.CASCADE, null=False, blank=False, verbose_name="Photographe")
    fk_departement = models.ForeignKey('DepartementCollection', on_delete=models.CASCADE, null=False, blank=False, verbose_name="Département de collection")
    fk_extrait_de = models.ForeignKey('ExtraitDe', on_delete=models.SET_NULL, null=True, blank=True, verbose_name="Extrait", help_text='Indiquez la provenance de l\'image.')
    themes = models.ManyToManyField('Theme', through='IntImageTheme')
    mots_cles = models.ManyToManyField('MotCle', through='IntImageMotCle')
    donnees_biblio = models.ManyToManyField('DonneesBiblio', through='IntImageDonneesBiblio')

    def set_format(self):
        """
        Cette méthode sert à générer automatiquement le champ 'image_format' en fonction du champ 'lien_telechargement' 
        qui contient donc l'extension du fichier
        """
        filebase, extension = self.lien_telechargement.path.split('.')
        self.image_format = extension
        
    def save(self, *args, **kwargs):
        """
        Redéfinition de la méthode save, afin d'appliquer deux modifications à l'entité Image avant la sauvegarde dans la base
        
        -Mise à jour du champ format, à l'aide de la méthode set_format
        -Génération de la miniature basse-définition à l'aide de la fonction utils.miniatures
        """

        self.set_format()
        super().save(*args, **kwargs)
        chemin_relatif_miniatures = 'bdd_icono/miniatures'
        chemin_miniatures = os.path.join(settings.MEDIA_ROOT, chemin_relatif_miniatures)
        os.makedirs(chemin_miniatures, exist_ok=True)
        miniatures(self.lien_telechargement.path, chemin_miniatures)
        
        #Enregistrement de l'Image dans la base
        super().save(*args, **kwargs)
        
    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['n_cesr'], name='unique_n_cesr'), #Un numéro par image
            models.UniqueConstraint(fields=['lien_telechargement'], name='unique_lien_telechargement') #Un fichier image par image
        ]

    def __str__(self):
        #Le n_cesr est utilisé pour représenter l'image car il est court, unique et obligatoire
        return f'{self.n_cesr}'

class Photographe(models.Model):
    photographe_nom = models.CharField(max_length=150, null=True, blank=True, verbose_name="Nom du photographe")
    photographe_prenom = models.CharField(max_length=50, null=True, blank=True, verbose_name="Prénom du photographe")
    
    #Liste des choix définie à l'aide du jeu de données étendu, possibilté d'en faire une table à part entière
    AGENCE_CHOICES = [
        ('RNM', 'RNM'),
        ('BNF', 'BNF'),
        ('INDEPENDANT', 'Indépendant'),
    ]
    agence = models.CharField(choices=AGENCE_CHOICES, null=False, blank=False, default = "INDEPENDANT")

    def __str__(self):
        nom = self.photographe_nom if self.photographe_nom else ""
        prenom = self.photographe_prenom if self.photographe_prenom else ""
        return f"{prenom} {nom} - {self.agence}".strip(" -")
    
class DepartementCollection(models.Model):
    departement_nom = models.CharField(max_length=30, null=True, blank=True, verbose_name='Nom du département de collection')
    fk_institution = models.ForeignKey('Institution', on_delete=models.SET_NULL, null=True, blank=True, verbose_name= "Institution")

    class Meta:
        verbose_name = 'Département de collection'
        verbose_name_plural = 'Départements de collection'
        constraints = [
            models.UniqueConstraint(fields=['departement_nom'], name='unique_departement_nom')]
    def __str__(self):
        return self.departement_nom

class Theme(models.Model):
    theme_libelle = models.CharField(max_length=150, null=False, blank=False, verbose_name='Libellé du thème')

    class Meta:
        verbose_name = 'Thème'
        constraints = [
            models.UniqueConstraint(fields=['theme_libelle'], name='unique_theme_libelle')]

    def __str__(self):
        return self.theme_libelle

class ExtraitDe(models.Model):
    extrait_de_nom = models.CharField(max_length=150, null=False, blank=False, verbose_name='Nom de l\'extrait')
    categorie = models.CharField(max_length=40, null=False, blank=False, verbose_name='Catégorie', help_text='Catégorie de l\'extrait (manuscrit, tableau, etc.)')
    date_creation = models.CharField(max_length=17, null=True, blank=True, verbose_name='Date de création', help_text='Format : AAAA pour une année précise, AAAA - AAAA pour une plage d\'années. Préfixes possibles : Avant, Vers, Après', validators=[validation_date_creation])
    periode_creation = models.CharField(max_length=23, null=True, blank=True, verbose_name='Période de création', help_text='Format : Siècle en chiffre, suivi de "e Siècle". Exemple : 3e Siècle, 15e Siècle, 14e Siècle - 15e Siècle. Préfixes possibles : Avant, Vers, Après', validators=[validation_periode_creation])
    auteur = models.ManyToManyField('Auteur', through='IntExtraitDeAuteur')
    technique = models.ManyToManyField('Technique', through='IntExtraitDeTechnique')
    class Meta:
        verbose_name = 'Extrait de'
        constraints = [
            models.UniqueConstraint(fields=['extrait_de_nom'], name='unique_extrait_de_nom')]
    
    def __str__(self):
        return self.extrait_de_nom

class Technique(models.Model):
    technique_libelle = models.CharField(max_length=30, null=False, blank=False)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['technique_libelle'], name='unique_technique_libelle')]
    
    def __str__(self):
        return self.technique_libelle
        
class DonneesBiblio(models.Model):
    ref_biblio = models.TextField(null=False, blank=False, verbose_name='Référence bibliographique')
    edition = models.TextField(null=True, blank=True)

    class Meta:
        verbose_name = 'Référence bibliographique'
        verbose_name_plural = 'Références bibliographiques'
        constraints = [
            models.UniqueConstraint(fields=['ref_biblio'], name='unique_ref_biblio')]
    
    def __str__(self):
        return self.edition
    
class Institution(models.Model):
    institution_nom = models.CharField(max_length=50, null=False, blank=False, verbose_name="Nom de l'institution")
    pays = models.CharField(max_length=30, null=False, blank=False)
    ville = models.CharField(max_length=30, null=True, blank=True)

    class Meta:
        ordering = ['institution_nom']
        #Pas de contraintes d'unicité, car le nom de l'institution peut être "bibliothèque municipale" par exemple
        
    def __str__(self):
        institution_nom = self.institution_nom if self.institution_nom else ""
        pays = self.pays if self.pays else ""
        ville = self.ville if self.ville else ""
        return f"{institution_nom} : {pays} - {ville}".strip(" -")

class MotCle(models.Model):
    mot_cle_libelle = models.CharField(max_length=20, null=False, blank=False, verbose_name='Libellé du mot clé')
    mot_cle_type = models.CharField(max_length=20, choices=settings.MOT_CLE_TYPE_CHOICES, null=False, blank=False, verbose_name='Type du mot clé')

    class Meta:
        verbose_name = 'Mot clé'
        verbose_name_plural = 'Mots clés'
        constraints = [
            models.UniqueConstraint(fields=['mot_cle_libelle'], name='unique_mot_cle_libelle')
        ]

    def __str__(self):
        libelle = self.mot_cle_libelle if self.mot_cle_libelle else ""
        type = self.mot_cle_type if self.mot_cle_type else ""
        return f"{libelle} - {type}"

class Auteur(models.Model):
    auteur_nom = models.CharField(max_length=40, null=False, blank=False, verbose_name='Nom', help_text='Si artiste Anonyme, indiquez Anonyme en Nom et précisez si possible son école et/ou lieu d\'activité')
    auteur_prenom = models.CharField(max_length=40, null=True, blank=True, verbose_name='Prénom')
    pseudonyme = models.CharField(max_length=50, null=True, blank=True)
    lieux_activites = models.ManyToManyField('LieuActivite', through='IntAuteurLieuActivite')
    ecoles = models.ManyToManyField('Ecole', through='IntAuteurEcole', related_name='auteurs')

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['auteur_nom', 'auteur_prenom', 'pseudonyme'], name='unique_auteur'),]
        ordering = ['auteur_nom', 'auteur_prenom']
        verbose_name = 'Auteur.e'
        verbose_name_plural = 'Auteur.e.s'
        
    def __str__(self):
        return self.auteur_nom

class Ecole(models.Model):
    ecole = models.CharField(max_length=80, null=False, blank=False, help_text='Indiquez l\'école artistique à laquelle appartient l\'auteur. Exemple : allemande, française, hollandaise...')

    def __str__(self):
        return self.ecole

class LieuActivite(models.Model):
    lieu_activite = models.CharField(max_length=40, null=False, blank=False)

    class Meta:
        verbose_name = 'Lieu d\'activité'
        verbose_name_plural = 'Lieux d\'activité'

    def __str__(self):
        return self.lieu_activite

################################

#Tables intermédiaires

################################

class IntImageMotCle(models.Model):
    fk_image = models.ForeignKey('Image', on_delete=models.CASCADE, null=False, blank=False)
    fk_mot_cle = models.ForeignKey('MotCle', on_delete=models.CASCADE, null=False, blank=False, verbose_name='Mot clé')

    class Meta:
        verbose_name = 'Mot clé'
        verbose_name_plural = 'Mots clés'
        constraints = [
            models.UniqueConstraint(fields=['fk_image', 'fk_mot_cle'], name='unique_image_mot_cle')
        ]

class IntImageDonneesBiblio(models.Model):
    fk_donnees_biblio = models.ForeignKey('DonneesBiblio', on_delete=models.CASCADE, null=False, blank=False, verbose_name='Donnée bibliographique correspondante à l\'image')
    fk_image = models.ForeignKey('Image', on_delete=models.CASCADE, null=False, blank=False)

    class Meta:
        verbose_name='Donnée bibliographique'
        verbose_name_plural='Données bibliographiques'
        constraints = [
            models.UniqueConstraint(fields=['fk_donnees_biblio', 'fk_image'], name='unique_image_donneesbiblio')]

class IntImageTheme(models.Model):
    fk_image = models.ForeignKey('Image', on_delete=models.CASCADE, null=False, blank=False)
    fk_theme = models.ForeignKey('Theme', on_delete=models.CASCADE, null=False, blank=False, verbose_name='Thème')

    class Meta:
        verbose_name='Thème'
        verbose_name_plural='Thèmes'
        constraints = [
            models.UniqueConstraint(fields=['fk_image', 'fk_theme'], name='unique_image_theme')]
        
class IntExtraitDeTechnique(models.Model):
    fk_technique = models.ForeignKey('Technique', on_delete=models.CASCADE, null=False, blank=False, verbose_name = 'Technique')
    fk_extrait_de = models.ForeignKey('ExtraitDe', on_delete=models.CASCADE, null=False, blank=False)

    class Meta:
        verbose_name = 'Technique de l\'extrait'
        verbose_name_plural = 'Techniques de l\'extrait'
        constraints = [
            models.UniqueConstraint(fields=['fk_technique', 'fk_extrait_de'], name='unique_extrait_technique')]

class IntExtraitDeAuteur(models.Model):
    fk_auteur = models.ForeignKey('Auteur', on_delete=models.CASCADE, null=False, blank=False, verbose_name='Auteur.e')
    fk_extrait_de = models.ForeignKey('ExtraitDe', on_delete=models.CASCADE, null=False, blank=False)

    class Meta:
        verbose_name = 'Auteur.e de l\'extrait'
        verbose_name_plural = 'Auteur.e.s de l\'extrait'
        constraints = [
            models.UniqueConstraint(fields=['fk_auteur', 'fk_extrait_de'], name='unique_extrait_auteur')]

class IntAuteurEcole(models.Model):
    fk_auteur = models.ForeignKey('Auteur', on_delete=models.CASCADE, null=False, blank=False)
    fk_ecole = models.ForeignKey('Ecole', on_delete=models.CASCADE, null=False, blank=False, verbose_name='Ecole')  # Relation inverse avec Ecole

    class Meta:
        verbose_name = 'Ecole artistique de l\'auteur'
        verbose_name_plural = 'Ecoles artistiques des auteurs'
        constraints = [
            models.UniqueConstraint(fields=['fk_auteur', 'fk_ecole'], name='unique_auteur_ecole')]

class IntAuteurLieuActivite(models.Model):
    fk_auteur = models.ForeignKey('Auteur', on_delete=models.CASCADE)
    fk_lieu_activite = models.ForeignKey('LieuActivite', on_delete=models.CASCADE, verbose_name='Lieu d\'activté')

    class Meta:
        verbose_name = 'Lieu d\'activité de l\'auteur'
        verbose_name_plural = 'Lieux d\'activité des auteurs'
        constraints = [
            models.UniqueConstraint(fields=['fk_auteur', 'fk_lieu_activite'], name='unique_auteur_lieu_activite')]
