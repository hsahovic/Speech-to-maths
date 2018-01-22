# -*- coding: utf-8 -*-
# Generated by Django 1.11.4 on 2017-11-27 21:29
from __future__ import unicode_literals

from django.conf import settings
import django.contrib.auth.models
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0008_alter_user_username_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='Document',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('address', models.TextField()),
                ('content', models.TextField(default='')),
                ('creation_date', models.DateField(auto_now_add=True)),
                ('is_in_trash', models.BooleanField(default=False)),
                ('last_modification_date', models.DateField(auto_now=True)),
                ('pdf', models.FileField(default='', upload_to='latex_files/')),
                ('title', models.CharField(max_length=2048)),
            ],
        ),
        migrations.CreateModel(
            name='DocumentConstant',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=16)),
                ('value', models.FloatField()),
                ('document', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='interface.Document')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='GeneralConstant',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=16)),
                ('value', models.FloatField()),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='TrainingSample',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('audio', models.FileField(upload_to='training_data')),
                ('creation_date', models.DateField(auto_now_add=True)),
                ('converted_to_wav', models.BooleanField(default=False)),
                ('text', models.TextField()),
                ('used', models.BooleanField(default=False)),
            ],
        ),
        migrations.CreateModel(
            name='UserConstant',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=16)),
                ('value', models.FloatField()),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Utilisateur',
            fields=[
                ('user_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'user',
                'abstract': False,
                'verbose_name_plural': 'users',
            },
            bases=('auth.user',),
            managers=[
                ('objects', django.contrib.auth.models.UserManager()),
            ],
        ),
        migrations.AddField(
            model_name='userconstant',
            name='user',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='interface.Utilisateur'),
        ),
        migrations.AddField(
            model_name='trainingsample',
            name='author',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='interface.Utilisateur'),
        ),
        migrations.AddField(
            model_name='document',
            name='author',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='interface.Utilisateur'),
        ),
    ]
