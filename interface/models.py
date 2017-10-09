from django.contrib.auth.models import User
from django.db import models
from django.core.files import File

import subprocess
import uuid


class Utilisateur(User):

    def __str__(self):
        return self.username


class Document(models.Model):

    address = models.TextField()
    author = models.ForeignKey('Utilisateur')
    content = models.TextField(default="")
    creation_date = models.DateField(auto_now_add=True)
    is_in_trash = models.BooleanField(default=False)
    last_modification_date = models.DateField(auto_now=True)
    pdf = models.FileField(upload_to="latex_files/", default="")
    title = models.CharField(max_length=2048)

    def __str__(self):
        return self.title

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


class TrainingSample(models.Model):

    audio = models.FileField(upload_to="training_data")
    author = models.ForeignKey('Utilisateur')
    creation_date = models.DateField(auto_now_add=True)
    converted_to_wav = models.BooleanField(default=False)
    text = models.TextField()
    used = models.BooleanField(default=False)

    def __str__(self):
        return self.text
