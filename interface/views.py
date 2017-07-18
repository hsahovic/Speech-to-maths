from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect

from . import forms, models

def get_user (request) :
    return models.Utilisateur.objects.get(username = request.user.username)

def get_document (request, n) :
    doc = models.Document.objects.get(id = n)
    if doc.auteur.username == request.user.username :
        return doc
    return None

@login_required
def add_doc (request) :
    doc = models.Document()
    user = get_user (request)
    n_doc = len(models.Document.objects.filter(auteur = user)) + 1
    doc.auteur = user
    doc.titre = "Nouveau document %d" % n_doc
    doc.contenu = ""
    doc.save()
    return redirect("document", doc.id)

@login_required
def docs (request) :
    user = get_user (request)
    try :
        doc = get_document(request, request.GET['s'])
        doc.delete()
    except Exception :
        pass
    docs = models.Document.objects.filter(auteur = user)
    return render(request, 'mes_documents.html', locals())

@login_required
def document(request, n) :
    doc = get_document(request, n)
    if doc :
        try : 
            doc.titre = request.POST['titre']
            doc.contenu = request.POST['contenu']
            doc.save()
        except Exception :
            pass
        return render(request, 'document.html', locals())
    return redirect('docs')


def index (request) :
    return render(request, 'index.html', locals())

def inscription (request) :
    form = forms.InscriptionForm(request.POST or None)
    if form.is_valid() :
        username = form.cleaned_data['username']
        psw = form.cleaned_data['password']
        email = form.cleaned_data['email']
        user = models.Utilisateur()
        user.username = username
        user.set_password(psw)
        user.email = email
        user.save()
        user = authenticate(username=username, password=psw)
        login(request, user)
        return redirect("docs")
    return render(request, 'inscription.html', locals())