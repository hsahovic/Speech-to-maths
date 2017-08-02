from django.contrib.auth.models import User
from django.db import models

class Utilisateur (User) :
    
    def __str__ (self) :
        return self.username

class Document (models.Model) :
    auteur = models.ForeignKey('Utilisateur')
    contenu = models.TextField()
    date_derniere_modification = models.DateField(auto_now = True)
    date_creation = models.DateField(auto_now_add = True)
    titre = models.CharField(max_length = 2048)
    is_in_trash = models.BooleanField()
    
    def __str__(self) :
        return self.titre