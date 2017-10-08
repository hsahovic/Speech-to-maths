import os
from . import models

from s2m.core.utils import generate_random_word


def get_document(request, id_=None, adress=False):
    """Utility function allowing to get a document in a request (while also checking the user) by id or adress"""
    try:
        if id_ is not None:
            doc = models.Document.objects.get(id=id_)
            if doc.author.username == request.user.username:
                return doc
        elif adress:
            doc = models.Document.objects.get(adress=adress)
            if doc.author.username == request.user.username:
                return doc
    except Exception as exception:
        print("Exception :", exception)
    return None


def get_user(request):
    return models.Utilisateur.objects.get(username=request.user.username)


def save_file_from_request(request, file_extension, post_arg="file", filename=None, file_path=None):
    """
    Save file from request.FILE[post_arg] at file_path as filename.file_extension
    If no filename is given, generate_random_word() will be used
    """
    if filename is None:
        filename = generate_random_word()
    filename = '.'.join([filename, file_extension])
    if file_path is not None:
        filename = os.path.join(file_path, filename)
    with open(filename, "wb+") as f:
        for chunk in request.FILES[post_arg].chunks():
            f.write(chunk)
    return filename
