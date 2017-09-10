from django.contrib.auth.models import User
from django.db import models
from django.core.files import File

import subprocess


class Utilisateur (User):

    def __str__(self):
        return self.username


class Document (models.Model):
    author = models.ForeignKey('Utilisateur')
    content = models.TextField()
    pdf = models.FileField(upload_to="latex_files/", default="")
    last_modification_date = models.DateField(auto_now=True)
    creation_date = models.DateField(auto_now_add=True)
    title = models.CharField(max_length=2048)
    is_in_trash = models.BooleanField()

    def __str__(self):
        return self.titre

    def generate_pdf(self):
        path = self.title
        with open(path + ".tex", "w") as f:
            if self.content == "":
                f.write(
                    "\\documentclass{article}\r\\begin{document}\rVous n'avez rien ecrit.\r\\end{document}")
            else:
                f.write(self.content)
        subprocess.call(["pdflatex", "%s.tex" % path])
        self.pdf = File(open(path + ".pdf", 'rb'))
        self.save()
        subprocess.call(["rm", path + ".tex"])
        subprocess.call(["rm", path + ".pdf"])
        subprocess.call(["rm", path + ".log"])
        subprocess.call(["rm", path + ".aux"])
