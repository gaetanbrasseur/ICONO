from django.contrib import admin
from bdd_icono.models import Image, Support, Auteur, Photographie, Institution

@admin.register(Image)
class ImageAdmin(admin.ModelAdmin):
    list_display = ['legende', 'num_inventaire','dept_collection', 'fk_support', 'fk_institution']
    list_display_links = ['legende']
    search_fields = ['legende']

@admin.register(Support)
class SupportAdmin(admin.ModelAdmin):
    list_display = ['nom_support', 'categorie']
    list_display_links = ['nom_support']
    search_fileds = ['nom_support']

@admin.register(Auteur)
class AuteurAdmin(admin.ModelAdmin):
    list_display = ['nom_auteur', 'prenom_auteur', 'pseudonyme']
    list_display_links = ['nom_auteur']
    search_field = ['nom_auteur', 'prenom_auteur', 'pseudonyme']
    search_fields_help = 'Chercher par nom, prénom ou pseudonyme'

@admin.register(Photographie)
class PhotographieAdmin(admin.ModelAdmin):
    list_display = ['num_doc_cesr','fk_image']


@admin.register(Institution)
class InstitutionAdmin(admin.ModelAdmin):
    list_display = ['nom_institution']

