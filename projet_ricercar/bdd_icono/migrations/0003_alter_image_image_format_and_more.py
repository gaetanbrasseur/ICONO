# Generated by Django 5.0.5 on 2024-06-02 10:10

import bdd_icono.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bdd_icono', '0002_alter_image_lien_telechargement'),
    ]

    operations = [
        migrations.AlterField(
            model_name='image',
            name='image_format',
            field=models.CharField(editable=False, verbose_name="Format de l'image"),
        ),
        migrations.AlterField(
            model_name='image',
            name='lien_telechargement',
            field=models.ImageField(help_text='Les images doivent être de format TIFF ou JPEG.', upload_to=bdd_icono.models.upload_location, verbose_name='Dépôt du fichier image'),
        ),
    ]