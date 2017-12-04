from django.contrib.auth.models import User
from django.db import models
from django.core.files import File
from django.core.exceptions import ObjectDoesNotExist

from s2m.settings import MEDIA_ROOT
from s2m.core.utils import generate_random_word

import os
import subprocess
import uuid

class Utilisateur(User):

    def __str__(self):
        return self.username

    def __init__(self, *args, **kwargs):
        from s2m.core.constants import ConstantsWrapper
        self.constants = ConstantsWrapper(self)
        super().__init__(*args, **kwargs)

    def save(self, *args, **kwargs):
        if not self.pk:
            from s2m.core.constants import constants
            constants.create_user_constants(self)
        super().save(*args, **kwargs)

class Document(models.Model):

    address = models.TextField()
    author = models.ForeignKey('Utilisateur')
    content = models.TextField(default="")
    creation_date = models.DateField(auto_now_add=True)
    is_in_trash = models.BooleanField(default=False)
    last_modification_date = models.DateField(auto_now=True)
    pdf = models.FileField(upload_to="latex_files/", default="")
    title = models.CharField(max_length=2048)

    def __init__(self, *args, **kwargs):
        from s2m.core.constants import ConstantsWrapper
        self.constants = ConstantsWrapper(self)
        super().__init__(*args, **kwargs)

    def save(self, *args, **kwargs):
        if not self.pk:
            from s2m.core.constants import constants
            constants.create_document_constants(self)
        super().save(*args, **kwargs)
        
    def generate_pdf(self):
        path_to_file = os.path.join(MEDIA_ROOT, "pdf_generation")
        if not os.path.exists(path_to_file) :
            try :
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


class TrainingSample(models.Model):

    audio = models.FileField(upload_to="training_data")
    author = models.ForeignKey('Utilisateur')
    creation_date = models.DateField(auto_now_add=True)
    converted_to_wav = models.BooleanField(default=False)
    text = models.TextField()
    used = models.BooleanField(default=False)

    def __str__(self):
        return self.text

class Constant(models.Model):
    
    name = models.CharField(max_length=16)
    value = models.FloatField()

    class Meta:
        abstract = True
    
class DocumentConstant(Constant):

    document = models.ForeignKey(Document,
                                 blank=True,
                                 null=True,
                                 on_delete=models.CASCADE,
                                 related_name='constset')

class UserConstant(Constant):

    user = models.ForeignKey(Utilisateur,
                             blank=True,
                             null=True,
                             on_delete=models.CASCADE,
                             related_name='constset')

class GeneralConstant(Constant):

    pass
