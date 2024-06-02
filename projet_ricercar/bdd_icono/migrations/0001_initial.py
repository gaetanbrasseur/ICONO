# Generated by Django 5.0.5 on 2024-06-02 07:39

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Auteur',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('auteur_nom', models.CharField(help_text="Si artiste Anonyme, indiquez Anonyme en Nom et précisez si possible son école et/ou lieu d'activité", max_length=40, verbose_name='Nom')),
                ('auteur_prenom', models.CharField(blank=True, max_length=40, null=True, verbose_name='Prénom')),
                ('pseudonyme', models.CharField(blank=True, max_length=50, null=True)),
            ],
            options={
                'verbose_name': 'Auteur.e',
                'verbose_name_plural': 'Auteur.e.s',
                'ordering': ['auteur_nom', 'auteur_prenom'],
            },
        ),
        migrations.CreateModel(
            name='DepartementCollection',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('departement_nom', models.CharField(blank=True, max_length=30, null=True, verbose_name='Nom du département de collection')),
            ],
            options={
                'verbose_name': 'Département de collection',
                'verbose_name_plural': 'Départements de collection',
            },
        ),
        migrations.CreateModel(
            name='DonneesBiblio',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ref_biblio', models.TextField(verbose_name='Référence bibliographique')),
                ('edition', models.TextField(blank=True, null=True)),
            ],
            options={
                'verbose_name': 'Référence bibliographique',
                'verbose_name_plural': 'Références bibliographiques',
            },
        ),
        migrations.CreateModel(
            name='Ecole',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ecole', models.CharField(max_length=80)),
            ],
        ),
        migrations.CreateModel(
            name='ExtraitDe',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('extrait_de_nom', models.CharField(max_length=150, verbose_name="Nom de l'extrait")),
                ('categorie', models.CharField(help_text="Catégorie de l'extrait (manuscrit, tableau, etc.)", max_length=40, verbose_name='Catégorie')),
                ('date_creation', models.CharField(blank=True, help_text="Format : AAAA pour une année précise, AAAA - AAAA pour une plage d'années. Préfixes possibles : Avant, Vers, Après", max_length=40, null=True, verbose_name='Date de création')),
                ('periode_creation', models.CharField(blank=True, help_text='Format : Siècle en chiffre, suivi de "e Siècle". Exemple : 3e Siècle, 15e Siècle, 14e Siècle - 15e Siècle', max_length=40, null=True, verbose_name='Période de création')),
            ],
        ),
        migrations.CreateModel(
            name='Image',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('legende', models.TextField(blank=True, null=True, verbose_name='Légende')),
                ('description', models.TextField(verbose_name='Description libre')),
                ('existe_en_physique', models.BooleanField(default=True)),
                ('cote', models.CharField(blank=True, max_length=150, null=True, verbose_name='Cote')),
                ('n_cesr', models.CharField(help_text=' Format : im_0000', max_length=150, verbose_name='numéro de document CESR')),
                ('image_format', models.CharField(choices=[('jpeg', 'JPEG'), ('tiff', 'TIFF'), ('NR', 'Non-renseigné')], default='tiff', verbose_name="Format de l'image")),
                ('mode', models.CharField(choices=[('Couleur', 'Couleur'), ('N & B', 'Noir et blanc'), ('NR', 'Non-renseigné')], default='Couleur', verbose_name='Mode')),
                ('resolution', models.CharField(default='non-renseigné', max_length=50, verbose_name='Résolution')),
                ('photographie_type', models.CharField(choices=[('numerique', 'Numérique'), ('photo', 'Photo'), ('NR', 'Non-renseigné')], default='numerique', verbose_name='Type de photographie')),
                ('credit', models.CharField(blank=True, max_length=250, null=True, verbose_name='Crédit')),
                ('lien_telechargement', models.ImageField(help_text='Les images doivent être de format TIFF ou JPEG.', upload_to='media/bdd_icono/hd', verbose_name='Dépôt du fichier image')),
                ('permalien', models.CharField(blank=True, max_length=250, null=True)),
                ('n_cliche_numerique', models.CharField(blank=True, max_length=250, null=True, verbose_name='Numéro de cliché numérique')),
                ('n_cliche_photo', models.CharField(blank=True, max_length=250, null=True, verbose_name='Numéro de cliché physique')),
            ],
        ),
        migrations.CreateModel(
            name='Institution',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('institution_nom', models.CharField(max_length=50, verbose_name="Nom de l'institution")),
                ('pays', models.CharField(max_length=30)),
                ('ville', models.CharField(blank=True, max_length=30, null=True)),
            ],
            options={
                'ordering': ['institution_nom'],
            },
        ),
        migrations.CreateModel(
            name='IntAuteurEcole',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
            options={
                'verbose_name': "Ecole artistique de l'auteur",
                'verbose_name_plural': 'Ecoles artistiques des auteurs',
            },
        ),
        migrations.CreateModel(
            name='IntAuteurLieuActivite',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
            options={
                'verbose_name': "Lieu d'activité de l'auteur",
                'verbose_name_plural': "Lieux d'activité des auteurs",
            },
        ),
        migrations.CreateModel(
            name='IntExtraitDeAuteur',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
            options={
                'verbose_name': "Auteur.e de l'extrait",
                'verbose_name_plural': "Auteur.e.s de l'extrait",
            },
        ),
        migrations.CreateModel(
            name='IntExtraitDeTechnique',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
            options={
                'verbose_name': "Technique de l'extrait",
                'verbose_name_plural': "Techniques de l'extrait",
            },
        ),
        migrations.CreateModel(
            name='IntImageDonneesBiblio',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
            options={
                'verbose_name': 'Donnée bibliographique',
                'verbose_name_plural': 'Données bibliographiques',
            },
        ),
        migrations.CreateModel(
            name='IntImageMotCle',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
            options={
                'verbose_name': 'Mot clé',
                'verbose_name_plural': 'Mots clés',
            },
        ),
        migrations.CreateModel(
            name='IntImageTheme',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
            options={
                'verbose_name': 'Thème',
                'verbose_name_plural': 'Thèmes',
            },
        ),
        migrations.CreateModel(
            name='LieuActivite',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('lieu_activite', models.CharField(max_length=40)),
            ],
            options={
                'verbose_name': "Lieu d'activité",
                'verbose_name_plural': "Lieux d'activité",
            },
        ),
        migrations.CreateModel(
            name='MotCle',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('mot_cle_libelle', models.CharField(max_length=20, verbose_name='Libellé du mot clé')),
                ('mot_cle_type', models.CharField(choices=[('generique', 'Générique'), ('chant', 'Chant'), ('instrument', 'Instrument de musique')], max_length=20, verbose_name='Type du mot clé')),
            ],
            options={
                'verbose_name': 'Mot clé',
                'verbose_name_plural': 'Mots clés',
            },
        ),
        migrations.CreateModel(
            name='Photographe',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('photographe_nom', models.CharField(blank=True, max_length=150, null=True, verbose_name='Nom du photographe')),
                ('photographe_prenom', models.CharField(blank=True, max_length=50, null=True, verbose_name='Prénom du photographe')),
                ('agence', models.CharField(choices=[('RNM', 'RNM'), ('BNF', 'BNF'), ('INDEPENDANT', 'Indépendant')], default='INDEPENDANT')),
            ],
        ),
        migrations.CreateModel(
            name='Technique',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('technique_libelle', models.CharField(max_length=30)),
            ],
        ),
        migrations.CreateModel(
            name='Theme',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('theme_libelle', models.CharField(max_length=150, verbose_name='Libellé du thème')),
            ],
            options={
                'verbose_name': 'Thème',
            },
        ),
        migrations.AddConstraint(
            model_name='donneesbiblio',
            constraint=models.UniqueConstraint(fields=('ref_biblio',), name='unique_ref_biblio'),
        ),
        migrations.AddField(
            model_name='image',
            name='fk_departement',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='bdd_icono.departementcollection', verbose_name='Département de collection'),
        ),
        migrations.AddField(
            model_name='image',
            name='fk_extrait_de',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='bdd_icono.extraitde', verbose_name='Extrait de'),
        ),
        migrations.AddField(
            model_name='departementcollection',
            name='fk_institution',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='bdd_icono.institution', verbose_name='Institution'),
        ),
        migrations.AddField(
            model_name='intauteurecole',
            name='fk_auteur',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='bdd_icono.auteur'),
        ),
        migrations.AddField(
            model_name='intauteurecole',
            name='fk_ecole',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='bdd_icono.ecole', verbose_name='Ecole'),
        ),
        migrations.AddField(
            model_name='auteur',
            name='ecoles',
            field=models.ManyToManyField(related_name='auteurs', through='bdd_icono.IntAuteurEcole', to='bdd_icono.ecole'),
        ),
        migrations.AddField(
            model_name='intauteurlieuactivite',
            name='fk_auteur',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='bdd_icono.auteur'),
        ),
        migrations.AddField(
            model_name='intextraitdeauteur',
            name='fk_auteur',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='bdd_icono.auteur', verbose_name='Auteur.e'),
        ),
        migrations.AddField(
            model_name='intextraitdeauteur',
            name='fk_extrait_de',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='bdd_icono.extraitde'),
        ),
        migrations.AddField(
            model_name='intextraitdetechnique',
            name='fk_extrait_de',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='bdd_icono.extraitde'),
        ),
        migrations.AddField(
            model_name='intimagedonneesbiblio',
            name='fk_donnees_biblio',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='bdd_icono.donneesbiblio', verbose_name="Donnée bibliographique correspondante à l'image"),
        ),
        migrations.AddField(
            model_name='intimagedonneesbiblio',
            name='fk_image',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='bdd_icono.image'),
        ),
        migrations.AddField(
            model_name='image',
            name='donnees_biblio',
            field=models.ManyToManyField(through='bdd_icono.IntImageDonneesBiblio', to='bdd_icono.donneesbiblio'),
        ),
        migrations.AddField(
            model_name='intimagemotcle',
            name='fk_image',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='bdd_icono.image'),
        ),
        migrations.AddField(
            model_name='intimagetheme',
            name='fk_image',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='bdd_icono.image'),
        ),
        migrations.AddField(
            model_name='intauteurlieuactivite',
            name='fk_lieu_activite',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='bdd_icono.lieuactivite', verbose_name="Lieu d'activté"),
        ),
        migrations.AddField(
            model_name='auteur',
            name='lieux_activites',
            field=models.ManyToManyField(through='bdd_icono.IntAuteurLieuActivite', to='bdd_icono.lieuactivite'),
        ),
        migrations.AddConstraint(
            model_name='motcle',
            constraint=models.UniqueConstraint(fields=('mot_cle_libelle',), name='unique_mot_cle_libelle'),
        ),
        migrations.AddConstraint(
            model_name='motcle',
            constraint=models.UniqueConstraint(fields=('mot_cle_type',), name='unique_mot_cle_type'),
        ),
        migrations.AddField(
            model_name='intimagemotcle',
            name='fk_mot_cle',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='bdd_icono.motcle', verbose_name='Mot clé'),
        ),
        migrations.AddField(
            model_name='image',
            name='mots_cles',
            field=models.ManyToManyField(through='bdd_icono.IntImageMotCle', to='bdd_icono.motcle'),
        ),
        migrations.AddField(
            model_name='image',
            name='fk_photographe',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='bdd_icono.photographe', verbose_name='Photographe'),
        ),
        migrations.AddConstraint(
            model_name='technique',
            constraint=models.UniqueConstraint(fields=('technique_libelle',), name='unique_technique_libelle'),
        ),
        migrations.AddField(
            model_name='intextraitdetechnique',
            name='fk_technique',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='bdd_icono.technique', verbose_name='Technique'),
        ),
        migrations.AddConstraint(
            model_name='theme',
            constraint=models.UniqueConstraint(fields=('theme_libelle',), name='unique_theme_libelle'),
        ),
        migrations.AddField(
            model_name='intimagetheme',
            name='fk_theme',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='bdd_icono.theme', verbose_name='Thème'),
        ),
        migrations.AddField(
            model_name='image',
            name='themes',
            field=models.ManyToManyField(through='bdd_icono.IntImageTheme', to='bdd_icono.theme'),
        ),
        migrations.AddConstraint(
            model_name='intextraitdeauteur',
            constraint=models.UniqueConstraint(fields=('fk_auteur', 'fk_extrait_de'), name='unique_extrait_auteur'),
        ),
        migrations.AddConstraint(
            model_name='intimagedonneesbiblio',
            constraint=models.UniqueConstraint(fields=('fk_donnees_biblio', 'fk_image'), name='unique_image_donneesbiblio'),
        ),
        migrations.AddConstraint(
            model_name='auteur',
            constraint=models.UniqueConstraint(fields=('auteur_nom', 'auteur_prenom', 'pseudonyme'), name='unique_auteur'),
        ),
        migrations.AddConstraint(
            model_name='intextraitdetechnique',
            constraint=models.UniqueConstraint(fields=('fk_technique', 'fk_extrait_de'), name='unique_extrait_technique'),
        ),
        migrations.AddConstraint(
            model_name='image',
            constraint=models.UniqueConstraint(fields=('n_cesr',), name='unique_n_cesr'),
        ),
        migrations.AddConstraint(
            model_name='image',
            constraint=models.UniqueConstraint(fields=('lien_telechargement',), name='unique_lien_telechargement'),
        ),
    ]
