from django.contrib import admin
from .models import (
    Image, Theme, MotCle, Support, Institution, DepartementCollection,
    DonneesBiblio, Photographe, Auteur, Technique, IntSupportAuteur,
    IntSupportTechnique, IntImageDonneesBiblio, IntImageTheme, IntImageMotCle,
    IntAuteurEcole, IntAuteurLieuActivite
)

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


class IntAuteurEcoleInLine(admin.StackedInline):
    model = IntAuteurEcole


class IntAuteurLieuActiviteInLine(admin.StackedInline):
    model = IntAuteurLieuActivite

class ImageAdmin(admin.ModelAdmin):
    fieldsets = (
        ('Informations sur la provenance de l\'image', {
            'fields': ('fk_support', 'legende', 'description', 'fk_departement', 'n_inventaire')
        }),
        ('Informations sur la photographie', {
            'fields': ('n_cesr', 'fk_photographe', 'image_format', 'couleur', 'resolution', 'photographie_type')
        }),
        ('Dépôt du fichier image :', {
            'fields': ('lien_telechargement',)
        })
    )
    list_display = ('legende', 'get_support', 'get_date', 'get_siecle', 'n_inventaire', 'get_institution_and_departement', 'n_cesr', 'fk_photographe', 'image_format', 'couleur', 'resolution', 'photographie_type')
    list_filter = ('image_format', 'couleur', 'photographie_type', 'fk_support__periode_creation')
    search_fields = ['legende','n_inventaire','n_cesr','fk_support__support_nom','fk_departement__departement_nom','fk_departement__fk_institution__institution_nom']
    search_help_text = 'La recherche porte sur la légende accompagnant l\'image, son numéro de document CESR, le nom du support, le nom du département de collection ou le nom de l\'institution'
    inlines = [IntImageDonneesBiblioInLine, IntImageMotCleInLine, IntImageThemeInLine]

    def get_support(self, obj):
        return obj.fk_support.support_nom if obj.fk_support else "-"
    get_support.short_description = 'Support'

    def get_date(self, obj):
        return obj.fk_support.date_creation if obj.fk_support else "-"
    get_date.short_description = 'Date'

    def get_siecle(self, obj):
        return obj.fk_support.periode_creation if obj.fk_support else "-"
    get_siecle.short_description = 'Siècle'

    def get_institution_and_departement(self, obj):
        if obj.fk_departement:
            departement = obj.fk_departement.departement_nom
            if obj.fk_departement.fk_institution:
                institution = obj.fk_departement.fk_institution.institution_nom
            else:
                institution = "-"
        else:
            departement = "-"
            institution = "-"
        return f"{institution} - {departement}"

    get_institution_and_departement.short_description = 'Institution et département'

class ThemeAdmin(admin.ModelAdmin):
    fieldsets = (
        ('Information sur le thème', {
            'fields': ('theme_libelle',)
        }),
    )
    list_display = ('theme_libelle',)
    search_fields = ('theme_libelle',)


class MotCleAdmin(admin.ModelAdmin):
    fieldsets = (
        ('Information sur le mot clé', {
            'fields': ('mot_cle_libelle', 'mot_cle_type',)
        }),
    )
    list_display = ('mot_cle_libelle', 'mot_cle_type')
    list_filter = ('mot_cle_type',)
    search_fields = ('mot_cle_libelle', 'mot_cle_type',)


class SupportAdmin(admin.ModelAdmin):
    fieldsets = (
        ('Description technique du support d\'une image', {
            'fields': ('support_nom', 'categorie')
        }),
        ('Informations historiques et iconographiques', {
            'fields': ('date_creation', 'periode_creation')
        }),
    )
    list_display = ('support_nom', 'date_creation', 'periode_creation')
    list_filter = ('periode_creation', 'categorie')
    search_fields = ['support_nom']
    search_help_text = 'La recherche porte sur le nom du support, sa catégorie, etc.'
    inlines = [IntSupportAuteurInLine, IntSupportTechniqueInLine]


class InstitutionAdmin(admin.ModelAdmin):
    fieldsets = (
        ('Information sur l\'institution', {
            'fields': ('institution_nom', 'pays', 'ville')
        }),
    )
    list_display = ('institution_nom', 'pays', 'ville')
    list_filter = ('pays', 'ville')
    search_fields = ['institution_nom', 'pays', 'ville']
    search_help_text = 'La recherche porte sur le nom de l\'institution, sa localisation, etc.'


class DepartementCollectionAdmin(admin.ModelAdmin):
    fieldsets = (
        ('Informations sur le département de collection', {
            'fields': ('departement_nom', 'fk_institution')
        }),
    )
    list_display = ('departement_nom', 'get_institution')
    def get_institution(self, obj):
        return obj.fk_institution.institution_nom if obj.fk_institution else "-"
    get_institution.short_description = 'Institution'
    search_fields = ('departement_nom', 'fk_institution__institution_nom', 'fk_institution__pays')


class DonneesBiblioAdmin(admin.ModelAdmin):
    fieldsets = (
        ('Informations bibliographiques', {
            'fields': ('ref_biblio', 'edition')
        }),
    )
    list_display = ('ref_biblio', 'edition')
    search_fields = ('ref_biblio', 'edition')


class PhotographeAdmin(admin.ModelAdmin):
    fieldsets = (
        ('Informations sur le photographe', {
            'fields': ('photographe_nom', 'photographe_prenom', 'agence')
        }),
    )
    list_display = ('photographe_nom', 'photographe_prenom', 'agence')
    search_fields = ('photographe_nom', 'photographe_prenom', 'agence')

class AuteurAdmin(admin.ModelAdmin):
    fieldsets = (
        ('Informations sur l\'auteur.e', {
            'fields': ('auteur_nom', 'auteur_prenom', 'pseudonyme')
        }),
    )
    list_display = ('auteur_nom', 'auteur_prenom', 'pseudonyme')
    search_fields = ('auteur_nom', 'auteur_prenom', 'pseudonyme')
    inlines = [IntAuteurEcoleInLine, IntAuteurLieuActiviteInLine]

class IntAuteurEcoleInLine(admin.TabularInline):
    model = IntAuteurEcole

class IntAuteurLieuActiviteInLine(admin.TabularInline):
    model = IntAuteurLieuActivite

admin.site.register(Image, ImageAdmin)
admin.site.register(Theme, ThemeAdmin)
admin.site.register(MotCle, MotCleAdmin)
admin.site.register(Support, SupportAdmin)
admin.site.register(Institution, InstitutionAdmin)
admin.site.register(DepartementCollection, DepartementCollectionAdmin)
admin.site.register(DonneesBiblio, DonneesBiblioAdmin)
admin.site.register(Photographe, PhotographeAdmin)
admin.site.register(Auteur, AuteurAdmin)
