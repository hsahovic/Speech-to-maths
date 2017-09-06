from django.contrib.auth.models import User
from django.db import models
import subprocess
from django.core.files import File


class Utilisateur (User):

    def __str__(self):
        return self.username


class Document (models.Model):
    auteur = models.ForeignKey('Utilisateur')
    contenu = models.TextField()
    latex = models.FileField(upload_to="latex_files/")
    date_derniere_modification = models.DateField(auto_now=True)
    date_creation = models.DateField(auto_now_add=True)
    titre = models.CharField(max_length=2048)
    is_in_trash = models.BooleanField()

    def __str__(self):
        return self.titre

    def as_pdf(self):
        chemin = self.titre
        f = open(chemin + ".tex", "w")
        if self.contenu=="":
            f.write("\\documentclass{article}\r\\begin{document}\rVous n'avez rien ecrit.\r\\end{document}")
        else:
            f.write(self.contenu)
        f.close()
        subprocess.call(["pdflatex", chemin + ".tex"])
        self.latex= File(open(chemin + ".pdf", 'rb'))
        self.save()
        subprocess.call(["rm", chemin + ".tex"])
        subprocess.call(["rm", chemin + ".pdf"])
        subprocess.call(["rm", chemin + ".log"])
        subprocess.call(["rm", chemin + ".aux"])
        return
