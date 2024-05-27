from django.db import models
from django.conf import settings
from django.core.exceptions import ValidationError

class Image(models.Model):
    legende = models.TextField(null=True, blank=True, verbose_name='Légende')
    description = models.TextField(null=False, blank=False,verbose_name='Description libre')
    existe_en_physique = models.BooleanField(null=False, blank=False, default=True)
    cote = models.CharField(max_length=150, null=True, blank=True, verbose_name = 'Cote')
    n_cesr = models.CharField(max_length=150, null=False, blank=False, verbose_name = 'numéro de document CESR', help_text=' Format : im_0000')
    image_format = models.CharField(choices=[('jpeg', 'JPEG'), ('tiff', 'TIFF'),('NR','Non-renseigné')], default='tiff', null=False, blank=False, verbose_name="Format de l'image")
    mode = models.CharField(choices=[('Couleur', 'Couleur'), ('N & B', 'Noir et blanc'),('NR','Non-renseigné')], null=False, blank=False,default='Couleur', verbose_name='Mode')
    resolution = models.CharField(max_length=50, null=False, blank=False, default='non-renseigné', verbose_name = 'Résolution')
    photographie_type = models.CharField(choices=[('numerique', 'Numérique'), ('photo', 'Photo'),('NR','Non-renseigné')],default='numerique', null=False, blank=False, verbose_name="Type de photographie")
    credit = models.CharField(max_length=250, null=True, blank=True, verbose_name = "Crédit")
    lien_telechargement = models.ImageField(upload_to='media/bdd_icono/hd', null=False, blank=False, verbose_name='Dépôt du fichier image', help_text='Les images doivent être de format TIFF ou JPEG.')
    permalien = models.CharField(max_length=250, null=True, blank=True,)
    n_cliche_numerique = models.CharField(max_length=250, null=True, blank=True, verbose_name = "Numéro de cliché numérique")
    n_cliche_photo = models.CharField(max_length=250, null=True, blank=True,  verbose_name = "Numéro de cliché physique")
    fk_photographe = models.ForeignKey('Photographe', on_delete=models.CASCADE, null=False, blank=False, verbose_name="Photographe")
    fk_departement = models.ForeignKey('DepartementCollection', on_delete=models.CASCADE, null=False, blank=False, verbose_name="Département de collection")
    fk_extrait_de = models.ForeignKey('ExtraitDe', on_delete=models.SET_NULL, null=True, blank=True, verbose_name="Extrait de")
    themes = models.ManyToManyField('Theme', through='IntImageTheme')
    mots_cles = models.ManyToManyField('MotCle', through='IntImageMotCle')
    donnees_biblio = models.ManyToManyField('DonneesBiblio', through='IntImageDonneesBiblio')

    # def get_siecle(self):
    #     # penser à mettre un peu de doc pour expliciter les méthodes
    #     if self.fk_support and self.fk_support.date_creation:
    #         date_creation = self.fk_support.date_creation
    #         if date_creation.startswith("vers"):
    #             annee = date_creation.split("vers")[1].strip().split("-")
    #             if len(annee) == 1:
    #                 annee = int(annee[0])
    #                 siecle = annee // 100 + 1 if annee % 100 != 0 else annee // 100
    #                 return f"{siecle}ème siècle"
    #             else:
    #                 debut_annee = int(annee[0])
    #                 fin_annee = int(annee[1])
    #                 debut_siecle = debut_annee // 100 + 1 if debut_annee % 100 != 0 else debut_annee // 100
    #                 fin_siecle = fin_annee // 100 + 1 if fin_annee % 100 != 0 else fin_annee // 100
    #                 if debut_siecle == fin_siecle:
    #                     return f"{debut_siecle}ème siècle"
    #                 else:
    #                     return f"{debut_siecle}-{fin_siecle}ème siècle"
    #         elif date_creation.startswith("avant"):
    #             annee = int(date_creation.split("avant")[1].strip())
    #             siecle = annee // 100 + 1 if annee % 100 != 0 else annee // 100
    #             return f"{siecle}ème siècle"
    #         elif date_creation.startswith("après"):
    #             annee = int(date_creation.split("après")[1].strip())
    #             siecle = annee // 100 + 1 if annee % 100 != 0 else annee // 100
    #             return f"{siecle}ème siècle"
    #         else:
    #             annee = date_creation.split("-")[0].strip()
    #             annee = int(annee)
    #             siecle = annee // 100 + 1 if annee % 100 != 0 else annee // 100
    #             return f"{siecle}ème siècle"
    #     return "Non-renseigné
    
    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['n_cesr'], name='unique_n_cesr'),
            models.UniqueConstraint(fields=['lien_telechargement'], name='unique_lien_telechargement')
        ]
    

class Photographe(models.Model):
    photographe_nom = models.CharField(max_length=150, null=True, blank=True, verbose_name="Nom du photographe")
    photographe_prenom = models.CharField(max_length=50, null=True, blank=True, verbose_name="Prénom du photographe")
    AGENCE_CHOICES = [
        ('RNM', 'RNM'),
        ('BNF', 'BNF'),
    ]
    agence = models.CharField(choices=AGENCE_CHOICES, null=True, blank=True)

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
    
    def __str__(self):
        return self.departement_nom

class Theme(models.Model):
    theme_libelle = models.CharField(max_length=150, null=False, blank=False, verbose_name='Libellé du thème')

    class Meta:
        verbose_name = 'Thème'
        constraints = [
            models.UniqueConstraint(fields=['theme_libelle'], name='unique_theme_libelle')]

class ExtraitDe(models.Model):
    extrait_de_nom = models.CharField(max_length=150, null=False, blank=False, verbose_name='Nom de l\'extrait')
    categorie = models.CharField(max_length=40, null=False, blank=False, verbose_name='Catégorie', help_text='Catégorie de l\'extrait (manuscrit, tableau, etc.)')
    date_creation = models.CharField(max_length=40, null=True, blank=True, verbose_name='Date de création', help_text='Format : AAAA pour une année précise, AAAA - AAAA pour une plage d\'années. Préfixes possibles : Avant, Vers, Après')
    periode_creation = models.CharField(max_length=40, null=True, blank=True, verbose_name='Période de création', help_text='Format : Siècle en chiffre, suivi de "e Siècle". Exemple : 3e Siècle, 15e Siècle, 14e Siècle - 15e Siècle')

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
        
class Institution(models.Model):
    institution_nom = models.CharField(max_length=50, null=False, blank=False, verbose_name="Nom de l'institution")
    pays = models.CharField(max_length=30, null=False, blank=False)
    ville = models.CharField(max_length=30, null=True, blank=True)

    class Meta:
        ordering = ['institution_nom']

    def __str__(self):
        return self.institution_nom

class MotCle(models.Model):
    mot_cle_libelle = models.CharField(max_length=20, null=False, blank=False, verbose_name='Libellé du mot clé')
    mot_cle_type = models.CharField(max_length=20, choices=settings.MOT_CLE_TYPE_CHOICES, null=False, blank=False, verbose_name='Type du mot clé')

    class Meta:
        verbose_name = 'Mot clé'
        verbose_name_plural = 'Mots clés'
        constraints = [
            models.UniqueConstraint(fields=['mot_cle_libelle'], name='unique_mot_cle_libelle'),
            models.UniqueConstraint(fields=['mot_cle_type'], name='unique_mot_cle_type')
        ]

    def __str__(self):
        return self.mot_cle_libelle

class Auteur(models.Model):
    auteur_nom = models.CharField(max_length=40, null=False, blank=False, verbose_name='Nom', help_text='Si artiste Anonyme, indiquez Anonyme en Nom et précisez si possible son école et/ou lieu d\'activité')
    auteur_prenom = models.CharField(max_length=40, null=True, blank=True, verbose_name='Prénom')
    pseudonyme = models.CharField(max_length=50, null=True, blank=True)
    lieux_activites = models.ManyToManyField('LieuActivite', through='IntAuteurLieuActivite')
    ecoles = models.ManyToManyField('Ecole', through='IntAuteurEcole', related_name='auteurs')

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['auteur_nom', 'auteur_prenom', 'pseudonyme'], name='unique_auteur'),
        ]
        ordering = ['auteur_nom', 'auteur_prenom']
        verbose_name = 'Auteur.e'
        verbose_name_plural = 'Auteur.e.s'

class Ecole(models.Model):
    ecole = models.CharField(max_length=80, null=False, blank=False)

    def __str__(self):
        return self.ecole

class LieuActivite(models.Model):
    lieu_activite = models.CharField(max_length=40, null=False, blank=False)

    class Meta:
        verbose_name = 'Lieu d\'activité'
        verbose_name_plural = 'Lieux d\'activité'

    def __str__(self):
        return self.lieu_activite


class IntAuteurEcole(models.Model):
    fk_auteur = models.ForeignKey('Auteur', on_delete=models.CASCADE, null=False, blank=False)
    fk_ecole = models.ForeignKey('Ecole', on_delete=models.CASCADE, null=False, blank=False, verbose_name='Ecole')  # Relation inverse avec Ecole

    class Meta:
        verbose_name = 'Ecole artistique de l\'auteur'
        verbose_name_plural = 'Ecoles artistiques des auteurs'

class IntAuteurLieuActivite(models.Model):
    fk_auteur = models.ForeignKey('Auteur', on_delete=models.CASCADE)
    fk_lieu_activite = models.ForeignKey('LieuActivite', on_delete=models.CASCADE, verbose_name='Lieu d\'activté')

    class Meta:
        verbose_name = 'Lieu d\'activité de l\'auteur'
        verbose_name_plural = 'Lieux d\'activité des auteurs'

class IntImageTheme(models.Model):
    fk_image = models.ForeignKey('Image', on_delete=models.CASCADE, null=False, blank=False)
    fk_theme = models.ForeignKey('Theme', on_delete=models.CASCADE, null=False, blank=False, verbose_name='Thème')

    class Meta:
        verbose_name='Thème'
        verbose_name_plural='Thèmes'

class IntExtraitDeTechnique(models.Model):
    fk_technique = models.ForeignKey('Technique', on_delete=models.CASCADE, null=False, blank=False, verbose_name = 'Technique')
    fk_extrait_de = models.ForeignKey('ExtraitDe', on_delete=models.CASCADE, null=False, blank=False)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['fk_technique', 'fk_extrait_de'], name='unique_extrait_technique')
        ]
        verbose_name = 'Technique de l\'extrait'
        verbose_name_plural = 'Techniques de l\'extrait'

class IntImageMotCle(models.Model):
    fk_image = models.ForeignKey('Image', on_delete=models.CASCADE, null=False, blank=False)
    fk_mot_cle = models.ForeignKey('MotCle', on_delete=models.CASCADE, null=False, blank=False, verbose_name='Mot clé')

    class Meta:
        verbose_name='Mot clé'
        verbose_name_plural='Mots clés'

class IntImageDonneesBiblio(models.Model):
    fk_donnees_biblio = models.ForeignKey('DonneesBiblio', on_delete=models.CASCADE, null=False, blank=False, verbose_name='Donnée bibliographique correspondante à l\'image')
    fk_image = models.ForeignKey('Image', on_delete=models.CASCADE, null=False, blank=False)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['fk_donnees_biblio', 'fk_image'], name='unique_image_donneesbiblio')
        ]
        verbose_name='Donnée bibliographique'
        verbose_name_plural='Données bibliographiques'

class IntExtraitDeAuteur(models.Model):
    fk_auteur = models.ForeignKey('Auteur', on_delete=models.CASCADE, null=False, blank=False, verbose_name='Auteur.e')
    fk_extrait_de = models.ForeignKey('ExtraitDe', on_delete=models.CASCADE, null=False, blank=False)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['fk_auteur', 'fk_extrait_de'], name='unique_extrait_auteur')
        ]
        verbose_name = 'Auteur.e de l\'extrait'
        verbose_name_plural = 'Auteur.e.s de l\'extrait'
