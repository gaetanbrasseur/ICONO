from django.contrib import admin
from .models import (
    Image, Theme, MotCle, ExtraitDe, Institution, DepartementCollection,
    DonneesBiblio, Photographe, Auteur, Technique, IntExtraitDeAuteur,
    IntExtraitDeTechnique, IntImageDonneesBiblio, IntImageTheme, IntImageMotCle,
    IntAuteurEcole, IntAuteurLieuActivite, Ecole, LieuActivite
)
from django import forms

class IntExtraitDeAuteurInLine(admin.StackedInline):
    model = IntExtraitDeAuteur
    extra = 0


class IntExtraitDeTechniqueInLine(admin.StackedInline):
    model = IntExtraitDeTechnique
    extra = 0


class IntImageDonneesBiblioInLine(admin.StackedInline):
    model = IntImageDonneesBiblio
    autocomplete_fields = ['fk_donnees_biblio']
    extra = 1

class IntImageMotCleInLine(admin.StackedInline):
    model = IntImageMotCle
    autocomplete_fields = ['fk_mot_cle']
    extra = 1

class IntImageThemeInLine(admin.StackedInline):
    model = IntImageTheme
    autocomplete_fields = ['fk_theme']
    extra = 1


class IntAuteurEcoleInLine(admin.StackedInline):
    model = IntAuteurEcole
    extra = 0


class IntAuteurLieuActiviteInLine(admin.StackedInline):
    model = IntAuteurLieuActivite
    extra = 0

class ImageAdmin(admin.ModelAdmin):
    fieldsets = (
        ('Information sur la photographie', { 
            'fields': ('n_cesr', 'existe_en_physique', 'mode', 'resolution', 'photographie_type', 'credit', 'permalien', 'lien_telechargement', 'n_cliche_numerique', 'n_cliche_photo', 'fk_photographe')
        }),
        ('Information sur l\'image', {
            'fields': ('description', 'legende',  'fk_extrait_de', 'cote' ,'fk_departement', )
        })
    )
    autocomplete_fields = ['mots_cles', 'themes', 'fk_photographe', 'fk_extrait_de', 'fk_departement']
    inlines = [IntImageMotCleInLine, IntImageThemeInLine, IntImageDonneesBiblioInLine]
    list_display = ('n_cesr','get_description_extrait', 'legende', 'cote', 'get_extrait', 'get_date', 'get_periode', 'image_format','lien_telechargement', 'mode', 'resolution', 'photographie_type', 'credit', 'n_cliche_numerique', 'n_cliche_photo')
    list_filter = ('fk_extrait_de__categorie', 'fk_extrait_de__periode_creation')
    search_fields = ['legende', 'cote', 'n_cesr', 'fk_extrait_de__extrait_de_nom', 'fk_departement__departement_nom', 'fk_departement__fk_institution__institution_nom']
    search_help_text = 'La recherche porte sur la légende accompagnant l\'image, son numéro de document CESR, son numéro d\'inventaire, le nom du support, le nom du département de collection ou le nom de l\'institution'
    ordering = ['n_cesr']

    def get_description_extrait(self, obj):
        return obj.description[:75] + '...' if obj.description and len(obj.description) > 75 else obj.description
    get_description_extrait.short_description = 'Description'

    def get_extrait(self, obj):
        return obj.fk_extrait_de.extrait_de_nom if obj.fk_extrait_de else "-"
    get_extrait.short_description = 'Extrait de'
    
    def get_date(self, obj):
        return obj.fk_extrait_de.date_creation if obj.fk_extrait_de else "-"
    get_date.short_description = 'Date de création'

    def get_periode(self, obj):
        return obj.fk_extrait_de.periode_creation if obj.fk_extrait_de else "-"
    get_periode.short_description = 'Periode de création'

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
    ordering = ['mot_cle_libelle']
    
class ExtraitDeAdmin(admin.ModelAdmin):
    fieldsets = (
        ('Description technique de l\'extrait d\'une image', {
            'fields': ('extrait_de_nom', 'categorie')
        }),
        ('Informations historiques et iconographiques', {
            'fields': ('date_creation', 'periode_creation')
        }),
    )
    list_display = ('extrait_de_nom', 'date_creation', 'periode_creation')
    list_filter = ('periode_creation', 'categorie')
    search_fields = ['extrait_de_nom']
    search_help_text = 'La recherche porte sur le nom du support, sa catégorie, etc.'
    inlines = [IntExtraitDeAuteurInLine, IntExtraitDeTechniqueInLine]
    ordering = ['extrait_de_nom']

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
    ordering = ['institution_nom']

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
    ordering = ['ref_biblio']


class PhotographeAdmin(admin.ModelAdmin):
    fieldsets = (
        ('Informations sur le photographe', {
            'fields': ('photographe_nom', 'photographe_prenom', 'agence')
        }),
    )
    list_display = ('photographe_nom', 'photographe_prenom', 'agence')
    search_fields = ('photographe_nom', 'photographe_prenom', 'agence')
    ordering = ['photographe_nom']

class EcoleAdmin(admin.ModelAdmin):
    fieldsets = (
        ('Information sur l\'école', {
            'fields': ('ecole',)
        }),
    )
    list_display = ('ecole',)
    search_fields = ('ecole',)
    

class LieuActiviteAdmin(admin.ModelAdmin):
    fieldsets = (
        ('Information sur le lieu d\'activité des auteurs', {
            'fields': ('lieu_activite',)
        }),
    )
    list_display = ('lieu_activite',)
    search_fields = ('lieu_activite',)


class AuteurAdmin(admin.ModelAdmin):
    fieldsets = (
        ('Informations sur l\'auteur.e', {
            'fields': ('auteur_nom', 'auteur_prenom', 'pseudonyme')
        }),
    )
    list_display = ('auteur_nom', 'auteur_prenom', 'pseudonyme')
    search_fields = ('auteur_nom', 'auteur_prenom', 'pseudonyme')
    inlines = [IntAuteurEcoleInLine, IntAuteurLieuActiviteInLine]
    ordering = ['auteur_nom']

class IntAuteurEcoleInLine(admin.TabularInline):
    model = IntAuteurEcole

class IntAuteurLieuActiviteInLine(admin.TabularInline):
    model = IntAuteurLieuActivite

admin.site.register(Ecole, EcoleAdmin)
admin.site.register(LieuActivite, LieuActiviteAdmin)
admin.site.register(Image, ImageAdmin)
admin.site.register(Theme, ThemeAdmin)
admin.site.register(MotCle, MotCleAdmin)
admin.site.register(ExtraitDe, ExtraitDeAdmin)
admin.site.register(Institution, InstitutionAdmin)
admin.site.register(DepartementCollection, DepartementCollectionAdmin)
admin.site.register(DonneesBiblio, DonneesBiblioAdmin)
admin.site.register(Photographe, PhotographeAdmin)
admin.site.register(Auteur, AuteurAdmin)
