from django.db import models


class Image(models.Model):
    legende = models.TextField(null=True, blank=True)
    num_inventaire = models.CharField(max_length=150, null=True, blank=True)
    folio = models.CharField(max_length=150, null=True, blank=True)
    dept_collection = models.CharField(max_length=250, null=True, blank=True)
    fond_collection = models.CharField(max_length=250, null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    fk_support = models.ForeignKey('Support', on_delete=models.CASCADE)
    fk_institution = models.ForeignKey('Institution', on_delete=models.CASCADE)

class DonneesBiblio(models.Model):
    ref_biblio = models.TextField()
    edition = models.TextField()

class Institution(models.Model):
    nom_institution = models.CharField(max_length=250, null=True, blank=True)
    pays = models.CharField(max_length=250, null=True, blank=True)
    ville = models.CharField(max_length=250, null=True, blank=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['nom_institution'], name='unique_nominstitution')
        ]

class MotCle(models.Model):
    libelle_motCle = models.CharField(max_length = 250)
    type_motCle = models.CharField(max_length=50)
    class Meta:
            ordering = ['libelle_motCle']

class Theme(models.Model):
    libelle_theme = models.CharField(max_length=250)

    class Meta:
        verbose_name = "Thème"
        verbose_name_plural = "Thèmes"
        constraints = [
            models.UniqueConstraint(fields=['libelle_theme'], name='unique_libelletheme')
            
        ]
        ordering = ['libelle_theme']

class IntImageTheme(models.Model):
    fk_image = models.ForeignKey('Image', on_delete=models.CASCADE)
    fk_theme = models.ForeignKey('Theme', on_delete=models.CASCADE)

class IntImageDonneesBiblio(models.Model):
    fk_image = models.ForeignKey('Image', on_delete=models.CASCADE)
    fk_donneesBiblio = models.ForeignKey('DonneesBiblio', on_delete=models.CASCADE)


class IntImageMotCle(models.Model):
    fk_image = models.ForeignKey('Image', on_delete=models.CASCADE)
    fk_motCle = models.ForeignKey('MotCle', on_delete=models.CASCADE)


class Support(models.Model):
    nom_support = models.CharField(max_length=250, null=True, blank=True)
    categorie = models.CharField(max_length=250, null=True, blank=True)
    commentaire = models.TextField(null=True, blank=True)
    date_creation = models.CharField( null=True, blank=True)
    periode = models.CharField(max_length=250, null=True, blank=True)

class Technique(models.Model):
    libelle_technique = models.CharField(max_length=250)

class Auteur(models.Model):
    nom_auteur = models.CharField(max_length=250, null=True, blank=True)
    prenom_auteur = models.CharField(max_length=250, null=True, blank=True)
    pseudonyme = models.CharField(max_length=250, null=True, blank=True)
    ecole = models.CharField(max_length=250, null=True, blank=True)
    lieu_activite = models.CharField(max_length=250, null=True, blank=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['nom_auteur', 'prenom_auteur', 'pseudonyme'], name='unique_auteur')
            
        ]
        ordering = ['nom_auteur', 'prenom_auteur']
        verbose_name = 'Auteur.e'
        verbose_name_plural = 'Auteur.e.s'

class IntSupportAuteur(models.Model):
    fk_support = models.ForeignKey('Support', on_delete=models.CASCADE)
    fk_auteur = models.ForeignKey('Auteur', on_delete=models.CASCADE)

class IntSupportTechnique(models.Model):
    fk_support = models.ForeignKey('Support', on_delete=models.CASCADE, verbose_name="Support")
    fk_technique = models.ForeignKey('Technique', on_delete=models.CASCADE)

class Photographie(models.Model):
    photographie_format = models.CharField(max_length = 50, null=True, blank=True)
    num_doc_cesr = models.CharField(max_length = 50, null=True, blank=True)
    type_photographie = models.CharField(max_length = 50, null=True, blank=True)
    agence = models.CharField(max_length = 250, null=True, blank=True)
    credit = models.CharField(max_length = 250, null=True, blank=True)
    nom_photographe = models.CharField(max_length = 250, null=True, blank=True)
    prenom_photographe = models.CharField(max_length = 250, null=True, blank=True)
    couleur = models.CharField(max_length = 50, null=True, blank=True)
    resolution = models.CharField(max_length = 50, null=True, blank=True)
    nom_cliche_physique = models.CharField(max_length = 250, null=True, blank=True)
    lien_telechargement = models.URLField(null=True, blank=True)
    fk_image = models.ForeignKey('Image', on_delete=models.CASCADE)

class Utilisateur(models.Model):
    nom_utilisateur = models.CharField(max_length=250)
    prenom_utilisateur = models.CharField(max_length=250)
    fk_autorisation = models.ForeignKey('Autorisation', on_delete=models.CASCADE)

class Autorisation(models.Model):
    niveau = models.CharField(max_length=50)
    description = models.TextField()

