from django.db import models
class Image(models.Model):
    legende = models.TextField(null=True, blank=True)
    existe_en_physique = models.BooleanField(null=False, blank=False, default=True)
    n_inventaire = models.CharField(max_length=150, null=True, blank=True, verbose_name = 'Numéro d\'inventaire dans l\'institution')
    n_cesr = models.CharField(max_length=150, null=True, blank=True, verbose_name = 'numéro du CESR')
    image_format = models.CharField(choices=[('jpeg', 'JPEG'), ('tiff', 'TIFF')], null=False, blank=False, verbose_name="Format de l'image")
    couleur = models.CharField(choices=[('Couleur', 'Couleur'), ('N & B', 'Noir et blanc')], null=False, blank=False)
    resolution = models.CharField(max_length=50, null=False, blank=False, verbose_name = 'Résolution')
    photographie_type = models.CharField(choices=[('numerique', 'Numérique'), ('photo', 'Photo')], null=False, blank=False, verbose_name="Type de photographie")
    credit = models.CharField(max_length=250, null=True, blank=True)
    lien_telechargement = models.URLField(null=False, blank=False)
    n_cliche_numerique = models.CharField(null=True, blank=True)
    n_cliche_photo = models.CharField(null=True, blank=True)
    fk_photographe = models.ForeignKey('Photographe', on_delete=models.CASCADE, null=True, blank=True, verbose_name="Photographe")
    fk_dpt = models.ForeignKey('DepartementCollection', on_delete=models.CASCADE, null=True, blank=True, verbose_name="Departement de collection")
    fk_support = models.ForeignKey('Support', on_delete=models.CASCADE, null=True, blank=True, verbose_name="Support")

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['n_cesr'], name='unique_n_cesr'),
            models.UniqueConstraint(fields=['lien_telechargement'], name='unique_lien_telechargement')
        ]


class Photographe(models.Model):
    nom = models.CharField(max_length=250, null=True, blank=True)
    prenom = models.CharField(max_length=250, null=True, blank=True)
    agence = models.CharField(choices=[('RNM', 'RNM'), ('BNF', 'BNF')], null=True, blank=True)

class DepartementCollection(models.Model):
    nom = models.CharField(max_length=250, null=True, blank=True)
    fk_institution = models.ForeignKey('Institution', on_delete=models.CASCADE, null=True, blank=True, verbose_name= "Institution")

    class Meta:
        verbose_name = 'Département de collection'
        verbose_name_plural = 'Départements de collection'

class Theme(models.Model):
    theme_libelle = models.CharField(max_length=250, null=True, blank=True)

    class Meta:
        verbose_name = 'Thème'
        verbose_name_plural = 'Thèmes'
        constraints = [
            models.UniqueConstraint(fields=['theme_libelle'], name='unique_theme_libelle')]

class Support(models.Model):
    nom = models.CharField(max_length=250, null=True, blank=True)
    categorie = models.CharField(max_length=250, null=True, blank=True)
    commentaire = models.TextField(null=True, blank=True)
    date_creation = models.CharField(max_length=250, null=True, blank=True)
    periode_creation = models.CharField(max_length=250, null=True, blank=True)
    description = models.TextField(null=True, blank=True)

class Technique(models.Model):
    technique_libelle = models.CharField(max_length=250, null=True, blank=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['technique_libelle'], name='unique_technique_libelle')]
class DonneesBiblio(models.Model):
    ref_biblio = models.TextField(null=True, blank=True)
    edition = models.TextField(null=True, blank=True)

    class Meta:
        verbose_name = 'Données bibliographique'
        verbose_name_plural = 'Données bibliographiques'
        constraints = [
            models.UniqueConstraint(fields=['ref_biblio'], name='unique_ref_biblio')]
class Institution(models.Model):
    institution_nom = models.CharField(max_length=250, null=True, blank=True, verbose_name="Institution")
    pays = models.CharField(max_length=250, null=True, blank=True)
    ville = models.CharField(max_length=250, null=True, blank=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['pays'], name='unique_pays')
        ]
        ordering = ['institution_nom']

class MotCle(models.Model):
    mot_cle_libelle = models.CharField(max_length=250, null=True, blank=True)
    mot_cle_type = models.CharField(max_length=50, null=True, blank=True)

    class Meta:
        verbose_name = 'Mot clé'
        verbose_name_plural = 'Mots clés'
        constraints = [
            models.UniqueConstraint(fields=['mot_cle_libelle'], name='unique_mot_cle_libelle'),
            models.UniqueConstraint(fields=['mot_cle_type'], name='unique_mot_cle_type')
        ]
        

class Auteur(models.Model):
    auteur_nom = models.CharField(max_length=250, null=True, blank=True)
    auteur_prenom = models.CharField(max_length=250, null=True, blank=True)
    pseudonyme = models.CharField(max_length=250, null=True, blank=True)
    ecole = models.CharField(max_length=250, null=True, blank=True)
    lieu_activite = models.CharField(max_length=250, null=True, blank=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['auteur_nom', 'auteur_prenom', 'pseudonyme'], name='unique_auteur'),
            models.UniqueConstraint(fields=['ecole'], name='unique_ecole')
        ]
        ordering = ['auteur_nom', 'auteur_prenom']
        verbose_name = 'Auteur.e'
        verbose_name_plural = 'Auteur.e.s'

class IntImageTheme(models.Model):
    fk_image = models.ForeignKey('Image', on_delete=models.CASCADE, null=False, blank=False)
    fk_theme = models.ForeignKey('Theme', on_delete=models.CASCADE, null=False, blank=False)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['fk_image', 'fk_theme'], name='unique_image_theme')
        ]

class IntSupportTechnique(models.Model):
    fk_technique = models.ForeignKey('Technique', on_delete=models.CASCADE, null=False, blank=False)
    fk_support = models.ForeignKey('Support', on_delete=models.CASCADE, null=False, blank=False)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['fk_technique', 'fk_support'], name='unique_support_technique')
        ]

class IntImageMotCle(models.Model):
    fk_image = models.ForeignKey('Image', on_delete=models.CASCADE, null=False, blank=False)
    fk_mot_cle = models.ForeignKey('MotCle', on_delete=models.CASCADE, null=False, blank=False)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['fk_image', 'fk_mot_cle'], name='unique_image_motcle')
        ]

class IntImageDonneesBiblio(models.Model):
    fk_donnees_biblio = models.ForeignKey('DonneesBiblio', on_delete=models.CASCADE, null=False, blank=False)
    fk_image = models.ForeignKey('Image', on_delete=models.CASCADE, null=False, blank=False)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['fk_donnees_biblio', 'fk_image'], name='unique_image_donneesbiblio')
        ]

class IntSupportAuteur(models.Model):
    fk_auteur = models.ForeignKey('Auteur', on_delete=models.CASCADE, null=False, blank=False)
    fk_support = models.ForeignKey('Support', on_delete=models.CASCADE, null=False, blank=False)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['fk_auteur', 'fk_support'], name='unique_support_auteur')
        ]