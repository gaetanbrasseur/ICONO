from django.contrib import admin
from .models import Image, Theme, MotCle, Support, Institution, DepartementCollection, DonneesBiblio, Photographe

class ImageAdmin(admin.ModelAdmin):
    fieldsets = (
        ('Informations sur la provenance de l\'image', {
            'fields': ('fk_support', 'legende', 'fk_dpt', 'n_inventaire')
        }),
        ('Informations sur la photographie', {
            'fields': ('n_cesr', 'fk_photographe', 'image_format', 'couleur', 'resolution', 'photographie_type')
        }),
    )
    list_display = ('legende', 'fk_support', 'n_inventaire', 'fk_dpt', 'n_cesr', 'fk_photographe', 'image_format', 'couleur', 'resolution', 'photographie_type')
    list_filter = ('image_format', 'couleur', 'photographie_type')
    search_fields = ['legende', 'n_inventaire', 'n_cesr']

admin.site.register(Image, ImageAdmin)
admin.site.register(Theme)
admin.site.register(MotCle)
admin.site.register(Support)
admin.site.register(Institution)
admin.site.register(DepartementCollection)
admin.site.register(DonneesBiblio)
admin.site.register(Photographe)