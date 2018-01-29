from django.contrib.auth.models import User
from django.db import models
from django.core.files import File

from s2m.settings import MEDIA_ROOT
from s2m.core.utils import generate_random_word
from s2m.core.formulae import Formula

import os
import subprocess
import uuid
import pickle


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
        path_to_file = os.path.join(MEDIA_ROOT, "pdf_generation")
        if not os.path.exists(path_to_file):
            try:
                os.makedirs(path_to_file)
            except OSError:
                pass
        path = os.path.join(path_to_file, generate_random_word())
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

class ElementaryFormula(models.Model):

    def validate_formula(self, value):
        try:
            obj = value.loads(value)
        except UnpicklingError:
            return False
        else:
            return isinstance(obj, Formula)

    document = models.ForeignKey('Document',on_delete=models.CASCADE, related_name='elementary_formulae')
    creation_date = models.DateField(auto_now_add=True)
    # Attribut max_length rajouté, il pourrait être opportun de transformer le char field en text field pour dépasser les 255 chars
    formula = models.CharField(validators=[validate_formula], max_length = 255)
    count = models.IntegerField(default=1)
        
class TrainingSample(models.Model):

    audio = models.FileField(upload_to="training_data")
    author = models.ForeignKey('Utilisateur')
    creation_date = models.DateField(auto_now_add=True)
    converted_to_wav = models.BooleanField(default=False)
    text = models.TextField()
    used = models.BooleanField(default=False)

    def __str__(self):
        return self.text
