from django.contrib import admin
from .models import Image, Theme, MotCle, Support, Institution, DepartementCollection, DonneesBiblio, Photographe, Auteur, Technique, IntSupportAuteur, IntSupportTechnique, IntImageDonneesBiblio, IntImageTheme, IntImageMotCle


class IntSupportAuteurInLine(admin.StackedInline):
    model = IntSupportAuteur

class IntSupportTechniqueInLine(admin.StackedInline):
    model = IntSupportTechnique

class IntImageDonneesBiblioInLine(admin.StackedInline):
    model = IntImageDonneesBiblio

class IntImageMotCleInLine(admin.StackedInline):
    model = IntImageMotCle

class IntImageThemeInLine(admin.StackedInline):
    model = IntImageTheme

class ImageAdmin(admin.ModelAdmin):
    fieldsets = (
        ('Informations sur la provenance de l\'image', {
            'fields': ('fk_support','legende', 'fk_dpt', 'n_inventaire')
        }),
        ('Informations sur la photographie', {
            'fields': ('n_cesr', 'fk_photographe', 'image_format', 'couleur', 'resolution', 'photographie_type')
        }),
        ('Dépôt du fichier image :', {
            'fields': ('lien_telechargement',)
        })
    )
    list_display = ('legende', 'fk_support', 'n_inventaire', 'fk_dpt', 'n_cesr', 'fk_photographe', 'image_format', 'couleur', 'resolution', 'photographie_type')
    list_filter = ('image_format', 'couleur', 'photographie_type', 'fk_support__date_creation', 'fk_support__periode_creation')
    search_fields = ['legende', 'n_inventaire', 'n_cesr', 'fk_support']
    search_help_text = 'La recherche porte sur la légende accompagnant l\'image, son numéro de document CESR ou le nom du support'
    inlines = [IntImageDonneesBiblioInLine, IntImageMotCleInLine, IntImageThemeInLine]

admin.site.register(Image, ImageAdmin)

class ThemeAdmin(admin.ModelAdmin):
    fieldsets = (
        ('Information sur le thème', {
            'fields' : ('theme_libelle',)
        }),
    )
    list_display = ('theme_libelle',)
    search_fields = ('theme_libelle',)
    

admin.site.register(Theme, ThemeAdmin)

class MotCleAdmin(admin.ModelAdmin):
    passfieldsets = (
        ('Information sur le mot clé', {
            'fields' : ('mot_cle_libelle', 'mot_cle_type',)
        })
    )
    list_display = ('mot_cle_libelle', 'mot_cle_type')
    list_filter = ('mot_cle_type',)
    search_field = ('mot_cle_libelle', 'mot_cle_type',)


admin.site.register(MotCle, MotCleAdmin)


class SupportAdmin(admin.ModelAdmin):
    fieldsets = (
        ('Description technique du support d\'une image', {
            'fields': ('nom','categorie')
        }),
        ('Informations historiques et iconographiques', {
            'fields': ('date_creation', 'periode_creation', 'commentaire', 'description')
        }),
    )
    list_display = ('nom', 'date_creation', 'periode_creation')
    list_filter = ('periode_creation', 'categorie')
    search_fields = ['nom', 'fk_auteur', 'categorie', 'fk_technique']
    search_help_text = 'La recherche porte sur le nom du support, son auteur, sa catégorie ou bien sa technique'
    inlines = [IntSupportAuteurInLine, IntSupportTechniqueInLine]

admin.site.register(Support, SupportAdmin)


class InstitutionAdmin(admin.ModelAdmin):
    fieldsets = (
        ('Information sur l\'institution', {
            'fields': ('institution_nom','pays', 'ville')
        }),
    )
    list_display = ('institution_nom', 'pays', 'ville')
    list_filter = ( 'pays', 'ville')
    search_fields = ['institution_nom', 'pays', 'ville']
    search_help_text = 'La recherche porte sur le nom de l\'institution, et sa localisation (ville ou pays)'

admin.site.register(Institution, InstitutionAdmin)

class DepartementCollectionAdmin(admin.ModelAdmin):
    fieldsets = (
        ('Informations sur le département de collection', {
            'fields': ('nom', 'fk_institution')
        }),
    )
    list_display = ('nom', 'fk_institution')
    search_fields = ('nom', 'fk_institution__institution_nom', 'fk_institution__institution_pays')

admin.site.register(DepartementCollection, DepartementCollectionAdmin)

class DonneesBiblioAdmin(admin.ModelAdmin):
    fieldsets = (
        ('Informations bibliographiques', {
            'fields': ('ref_biblio', 'edition')
        }),
    )
    list_display = ('ref_biblio', 'edition')
    search_fields = ('ref_biblio', 'edition')

admin.site.register(DonneesBiblio, DonneesBiblioAdmin)

class PhotographeAdmin(admin.ModelAdmin):
    fieldsets = (
        ('Informations sur le photographe', {
            'fields': ('nom', 'prenom', 'agence')
        }),
    )
    list_display = ('nom', 'prenom', 'agence')
    search_fields = ('nom', 'prenom', 'agence')

admin.site.register(Photographe, PhotographeAdmin)

class AuteurAdmin(admin.ModelAdmin):
    fieldsets = (
        ('Informations sur l\'auteur.e', {
            'fields': ('auteur_nom', 'auteur_prenom', 'pseudonyme', 'ecole', 'lieu_activite')
        }),
    )
    list_display = ('auteur_nom', 'auteur_prenom', 'pseudonyme', 'ecole', 'lieu_activite')
    search_fields = ('auteur_nom', 'auteur_prenom', 'pseudonyme', 'ecole', 'lieu_activite')
    list_filter = ('ecole',)
    search_help_text = 'La recherche porte sur le nom de l\'auteur.e, son prénom, son pseudonyme, son école, ou son lieu d\'activité.'

admin.site.register(Auteur, AuteurAdmin)
