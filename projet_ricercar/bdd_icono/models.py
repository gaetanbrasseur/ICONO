from django.db import models


class Image(models.Model):
    legende = models.TextField(null=True, blank=True)
    num_inventaire = models.CharField(max_length=150, null=True, blank=True)
    folio = models.CharField(max_length=150, null=True, blank=True)
    dept_collection = models.CharField(max_length=250, null=True, blank=True)
    fond_collection = models.CharField(max_length=250, null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    fk_support = models.ForeignKey('Support', on_delete=models.CASCADE, null=True, blank=True)
    fk_institution = models.ForeignKey('Institution', on_delete=models.CASCADE,null=True, blank=True)
    existe_en_physique = models.CharField(null=True, blank=True)
class DonneesBiblio(models.Model):
    ref_biblio = models.TextField(null=True, blank=True)
    edition = models.TextField(null=True, blank=True)

class Institution(models.Model):
    nom_institution = models.CharField(max_length=250, null=True, blank=True, verbose_name="Institution")
    pays = models.CharField(max_length=250, null=True, blank=True)
    ville = models.CharField(max_length=250, null=True, blank=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['nom_institution'], name='unique_nominstitution')
        ]
        ordering = ['nom_institution']

class MotCle(models.Model):
    motCle_libelle = models.CharField(max_length = 250, null=True, blank=True)
    motCle_type = models.CharField(max_length=50, null=True, blank=True)
    class Meta:
            ordering = ['motCle_libelle']

class Theme(models.Model):
    theme_libelle = models.CharField(max_length=250, null=True, blank=True)

    class Meta:
        verbose_name = "Thème"
        verbose_name_plural = "Thèmes"
        constraints = [
            models.UniqueConstraint(fields=['theme_libelle'], name='unique_libelletheme')
            
        ]
        ordering = ['theme_libelle']

class IntImageTheme(models.Model):
    fk_image = models.ForeignKey('Image', on_delete=models.CASCADE, null=True, blank=True)
    fk_theme = models.ForeignKey('Theme', on_delete=models.CASCADE, null=True, blank=True)

class IntImageDonneesBiblio(models.Model):
    fk_image = models.ForeignKey('Image', on_delete=models.CASCADE, null=True, blank=True)
    fk_donneesBiblio = models.ForeignKey('DonneesBiblio', on_delete=models.CASCADE,null=True, blank=True)


class IntImageMotCle(models.Model):
    fk_image = models.ForeignKey('Image', on_delete=models.CASCADE, null=True, blank=True)
    fk_motCle = models.ForeignKey('MotCle', on_delete=models.CASCADE, null=True, blank=True)


class Support(models.Model):
    nom_support = models.CharField(max_length=250, null=True, blank=True)
    categorie = models.CharField(max_length=250, null=True, blank=True)
    commentaire = models.TextField(null=True, blank=True)
    date_creation = models.CharField( null=True, blank=True)
    periode = models.CharField(max_length=250, null=True, blank=True)

class Technique(models.Model):
    libelle_technique = models.CharField(max_length=250, null=True, blank=True)

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
    fk_support = models.ForeignKey('Support', on_delete=models.CASCADE,null=True, blank=True)
    fk_auteur = models.ForeignKey('Auteur', on_delete=models.CASCADE,null=True, blank=True)

class IntSupportTechnique(models.Model):
    fk_support = models.ForeignKey('Support', on_delete=models.CASCADE, verbose_name="Support", null=True, blank=True)
    fk_technique = models.ForeignKey('Technique', on_delete=models.CASCADE,null=True, blank=True)

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
    lienTelechargement = models.URLField(null=True, blank=True)
    fk_image = models.ForeignKey('Image', on_delete=models.CASCADE, null=True, blank=True)

class Utilisateur(models.Model):
    nom_utilisateur = models.CharField(max_length=250, null=True, blank=True)
    prenom_utilisateur = models.CharField(max_length=250, null=True, blank=True)
    fk_autorisation = models.ForeignKey('Autorisation', on_delete=models.CASCADE, null=True, blank=True)

class Autorisation(models.Model):
    niveau = models.CharField(max_length=50, null=True, blank=True)
    description = models.TextField(null=True, blank=True)

