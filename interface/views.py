from django.contrib.auth import authenticate, login, update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.http import Http404
from django.shortcuts import render, redirect, HttpResponse

from . import forms, models


def get_user(request):
    return models.Utilisateur.objects.get(username=request.user.username)


def get_document(request, n):
    try:
        doc = models.Document.objects.get(id=n)
        if doc.auteur.username == request.user.username:
            return doc
        raise
    except Exception:
        pass
    return None


@login_required
def add_doc(request):
    doc = models.Document()
    user = get_user(request)
    doc.auteur = user
    n = 1
    while True:
        if models.Document.objects.filter(auteur=user, titre="Sans titre %d" % n):
            n += 1
        else:
            break
    doc.titre = "Sans titre %d" % n
    doc.contenu = ""
    doc.is_in_trash = False
    doc.save()
    return redirect("document", doc.id)


@login_required
def compte(request):
    user = get_user(request)
    if request.POST and "Changer adresse email" in request.POST:
        email_form = forms.ChangeEmailForm(
            request.POST, initial={'email': request.user.email})
    else:
        email_form = forms.ChangeEmailForm(
            None, initial={'email': request.user.email})
    if request.POST and "Changer mot de passe" in request.POST:
        password_form = forms.ChangePasswordForm(request.user, request.POST)
    else:
        password_form = forms.ChangePasswordForm(request.user, None)

    if request.POST and "Suppresion compte" in request.POST:
        suppression_form = forms.SuppressionCompte(request.user, request.POST)
    else:
        suppression_form = forms.SuppressionCompte(request.user, None)
    if email_form.is_valid():
        user.email = email_form.cleaned_data['email']
        user.save()
    if suppression_form.is_valid():
        mdp = request.POST['password']
        user = get_user(request)
        docs = models.Document.objects.filter(auteur=user)
        for doc in docs:
            doc.delete()
        user.delete()
        return redirect("index")
    if password_form.is_valid():
        user.set_password(password_form.cleaned_data['new_password'])
        user.save()
        update_session_auth_hash(request, user)
    return render(request, 'compte.html', locals())


@login_required
def docs(request):
    user = get_user(request)
    try:
        for n in request.POST['delete-value'].split(';'):
            doc = get_document(request, int(n))
            doc.is_in_trash = True
            doc.save()
    except:
        pass
    docs = models.Document.objects.filter(auteur=user, is_in_trash=False)
    return render(request, 'mes_documents.html', locals())


@login_required
def document(request, n):
    doc = get_document(request, n)
    if doc:
        try:
            doc.titre = request.POST['titre']
            doc.contenu = request.POST['contenu']
            doc.save()
        except Exception:
            pass
        return render(request, 'document.html', locals())
    raise Http404


def inscription(request):
    form = forms.InscriptionForm(request.POST or None)
    if form.is_valid():
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
