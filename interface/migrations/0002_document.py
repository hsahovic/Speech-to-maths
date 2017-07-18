# -*- coding: utf-8 -*-
# Generated by Django 1.11.3 on 2017-07-16 16:40
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('interface', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Document',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('contenu', models.TextField()),
                ('date_derniere_modification', models.DateField(auto_now=True)),
                ('date_creation', models.DateField(auto_now_add=True)),
                ('titre', models.CharField(max_length=2048)),
                ('auteur', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='interface.Utilisateur')),
            ],
        ),
    ]
