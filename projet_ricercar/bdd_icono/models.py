from django.db import models
class Image(models.Model):
    legende = models.TextField(null=True, blank=True, verbose_name='Légende')
    description = models.TextField(null=True, blank=True)
    commentaire = models.TextField(null=True, blank=True)
    existe_en_physique = models.BooleanField(null=False, blank=False, default=True)
    n_inventaire = models.CharField(max_length=150, null=True, blank=True, verbose_name = 'Numéro d\'inventaire dans l\'institution')
    n_cesr = models.CharField(max_length=150, null=True, blank=True, verbose_name = 'numéro de document CESR')
    image_format = models.CharField(choices=[('jpeg', 'JPEG'), ('tiff', 'TIFF')], null=False, blank=False, verbose_name="Format de l'image")
    couleur = models.CharField(choices=[('Couleur', 'Couleur'), ('N & B', 'Noir et blanc')], null=False, blank=False, verbose_name='Couleur')
    resolution = models.CharField(max_length=50, null=False, blank=False, verbose_name = 'Résolution')
    photographie_type = models.CharField(choices=[('numerique', 'Numérique'), ('photo', 'Photo')], null=False, blank=False, verbose_name="Type de photographie")
    credit = models.CharField(max_length=250, null=True, blank=True)
    lien_telechargement = models.ImageField(upload_to='images/', null=False, blank=False, verbose_name='Dépôt du fichier image')
    n_cliche_numerique = models.CharField(null=True, blank=True)
    n_cliche_photo = models.CharField(null=True, blank=True)
    fk_photographe = models.ForeignKey('Photographe', on_delete=models.CASCADE, null=True, blank=True, verbose_name="Photographe")
    fk_dpt = models.ForeignKey('DepartementCollection', on_delete=models.CASCADE, null=True, blank=True, verbose_name="Département de collection")
    fk_support = models.ForeignKey('Support', on_delete=models.CASCADE, null=True, blank=True, verbose_name="Support")
    theme = models.ManyToManyField('Theme', through='IntImageTheme')
    motCle = models.ManyToManyField('MotCle', through='IntImageMotCle')
    donneesBiblio = models.ManyToManyField('DonneesBiblio', through='IntImageDonneesBiblio')

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['n_cesr'], name='unique_n_cesr'),
            models.UniqueConstraint(fields=['lien_telechargement'], name='unique_lien_telechargement')
        ]


class Photographe(models.Model):
    photographe_nom = models.CharField(max_length=250, null=True, blank=True)
    photographe_prenom = models.CharField(max_length=250, null=True, blank=True)
    agence = models.CharField(choices=[('RNM', 'RNM'), ('BNF', 'BNF')], null=True, blank=True)

class DepartementCollection(models.Model):
    departement_nom = models.CharField(max_length=250, null=True, blank=True)
    fk_institution = models.ForeignKey('Institution', on_delete=models.CASCADE, null=True, blank=True, verbose_name= "Institution")

    class Meta:
        verbose_name = 'Département de collection'
        verbose_name_plural = 'Départements de collection'

class Theme(models.Model):
    theme_libelle = models.CharField(max_length=250, null=True, blank=True, verbose_name='Libellé du thème')

    class Meta:
        verbose_name = 'Thème'
        verbose_name_plural = 'Thèmes'
        constraints = [
            models.UniqueConstraint(fields=['theme_libelle'], name='unique_theme_libelle')]

class Support(models.Model):
    support_nom = models.CharField(max_length=250, null=True, blank=True)
    categorie = models.CharField(max_length=250, null=True, blank=True, verbose_name='Catégorie')
    date_creation = models.CharField(max_length=250, null=True, blank=True, verbose_name='Date de création')
    periode_creation = models.CharField(max_length=250, null=True, blank=True, verbose_name='Période de création')

class Technique(models.Model):
    technique_libelle = models.CharField(max_length=250, null=True, blank=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['technique_libelle'], name='unique_technique_libelle')]
class DonneesBiblio(models.Model):
    ref_biblio = models.TextField(null=True, blank=True, verbose_name='Référence bibliographique')
    edition = models.TextField(null=True, blank=True)

    class Meta:
        verbose_name = 'Données bibliographique'
        verbose_name_plural = 'Données bibliographiques'
        constraints = [
            models.UniqueConstraint(fields=['ref_biblio'], name='unique_ref_biblio')]
class Institution(models.Model):
    institution_nom = models.CharField(max_length=250, null=True, blank=True, verbose_name="Nom de l'institution")
    pays = models.CharField(max_length=250, null=True, blank=True)
    ville = models.CharField(max_length=250, null=True, blank=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['pays'], name='unique_pays')
        ]
        ordering = ['institution_nom']

class MotCle(models.Model):
    mot_cle_libelle = models.CharField(max_length=250, null=True, blank=True, verbose_name='Libellé du mot clé')
    mot_cle_type = models.CharField(max_length=50, null=True, blank=True, verbose_name='Type du mot clé')

    class Meta:
        verbose_name = 'Mot clé'
        verbose_name_plural = 'Mots clés'
        constraints = [
            models.UniqueConstraint(fields=['mot_cle_libelle'], name='unique_mot_cle_libelle'),
            models.UniqueConstraint(fields=['mot_cle_type'], name='unique_mot_cle_type')
        ]
        

class Auteur(models.Model):
    auteur_nom = models.CharField(max_length=250, null=True, blank=True, verbose_name='Nom')
    auteur_prenom = models.CharField(max_length=250, null=True, blank=True, verbose_name='Prénom')
    pseudonyme = models.CharField(max_length=250, null=True, blank=True)
    lieu_activite = models.ManyToManyField('LieuActivite', through='IntAuteurLieuActivite')
    ecole = models.ManyToManyField('Ecole', through='IntAuteurEcole')

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['auteur_nom', 'auteur_prenom', 'pseudonyme'], name='unique_auteur'),
        ]
        ordering = ['auteur_nom', 'auteur_prenom']
        verbose_name = 'Auteur.e'
        verbose_name_plural = 'Auteur.e.s'


class Ecole(models.Model):
    ecole = models.CharField(null=False, blank=False)

class LieuActivite(models.Model):
    lieu_activite = models.CharField(null=False, blank=False)

    class Meta:
        verbose_name = 'Lieu d\'activité'
        verbose_name_plural = 'Lieux d\'activité'

class IntAuteurEcole(models.Model):
    fk_auteur = models.ForeignKey('Auteur', on_delete=models.CASCADE, null=False, blank=False)
    fk_ecole = models.ForeignKey('Ecole', on_delete=models.CASCADE, null=False, blank=False, verbose_name='Ecole', related_name='auteurs')  # Relation inverse avec Ecole

    class Meta:
        verbose_name = 'Ecole artistique de l\'auteur'
        verbose_name_plural = 'Ecoles artistiquess des auteurs'

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

class IntSupportTechnique(models.Model):
    fk_technique = models.ForeignKey('Technique', on_delete=models.CASCADE, null=False, blank=False, verbose_name = 'Technique')
    fk_support = models.ForeignKey('Support', on_delete=models.CASCADE, null=False, blank=False)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['fk_technique', 'fk_support'], name='unique_support_technique')
        ]
        verbose_name = 'Technique du support'
        verbose_name_plural = 'Techniques du support'

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

class IntSupportAuteur(models.Model):
    fk_auteur = models.ForeignKey('Auteur', on_delete=models.CASCADE, null=False, blank=False, verbose_name='Auteur.e')
    fk_support = models.ForeignKey('Support', on_delete=models.CASCADE, null=False, blank=False)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['fk_auteur', 'fk_support'], name='unique_support_auteur')
        ]
        verbose_name = 'Auteur.e du support'
        verbose_name_plural = 'Auteur.e.s du support'
