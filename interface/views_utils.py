import os
from . import models

from s2m.core.utils import generate_random_word


def get_document(request, id_=None, address=False):
    """
    Returns a document from a request (also checks the user) by id or address
    """
    try:
        if id_ is not None:
            doc = models.Document.objects.get(id=id_)
            if doc.author.username == request.user.username:
                return doc
        elif address:
            doc = models.Document.objects.get(address=address)
            if doc.author.username == request.user.username:
                return doc
    except Exception as exception:
        print("Exception :", exception)
    return None


def get_user(request):
    """
    Returns the user from a request
    """
    return models.Utilisateur.objects.get(username=request.user.username)


def save_file_from_request(request, file_extension, post_arg="file", filename=None, file_path=None):
    """
    Saves a file from request.FILE[post_arg] at file_path as filename.file_extension
    If no filename is given, generate_random_word() will be used
    Creates all missing directories
    """
    if filename is None:
        filename = generate_random_word()
    filename = '.'.join([filename, file_extension])
    if file_path is not None:
        filename = os.path.join(file_path, filename)
    if not os.path.exists(file_path) :
        os.makedirs(file_path)
    with open(filename, "wb+") as f:
        for chunk in request.FILES[post_arg].chunks():
            f.write(chunk)
    return filename
