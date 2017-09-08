from django.contrib.auth import authenticate, login, update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.http import Http404
from django.shortcuts import render, redirect, HttpResponse
from django.core.files import File

from . import forms, models

import json


def get_user(request):
    return models.Utilisateur.objects.get(username=request.user.username)


def get_document(request, n):
    try:
        doc = models.Document.objects.get(id=n)
        if doc.author.username == request.user.username:
            return doc
    except Exception:
        pass
    return None


@login_required
def account(request):
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
        user = get_user(request)
        docs = models.Document.objects.filter(author=user)
        for doc in docs:
            doc.delete()
        user.delete()
        return redirect("index")
    if password_form.is_valid():
        user.set_password(password_form.cleaned_data['new_password'])
        user.save()
        update_session_auth_hash(request, user)
    return render(request, 'account.html', locals())


@login_required
def add_doc(request):
    doc = models.Document()
    user = get_user(request)
    doc.author = user
    n = 1
    while True:
        if models.Document.objects.filter(author=user, title="Sans titre %d" % n):
            n += 1
        else:
            break
    doc.title = "Sans titre %d" % n
    doc.content = ""
    doc.is_in_trash = False
    doc.save()
    return redirect("document", doc.id)


@login_required
def document(request, n):
    doc = get_document(request, n)
    if doc.is_in_trash:
        return redirect("error_400")
    if doc:
        # try:
        #     doc.title = request.POST['titre']
        #     doc.content = request.POST['contenu']
        #     doc.save()
        #     # A mieux placer ; sans doute un système asynchrone serait plus efficient
        #     doc.generate_pdf()
        # except Exception:
        #     pass
        return render(request, 'document.html', locals())
    raise Http404


@login_required
def documents(request):
    user = get_user(request)
    try:
        for n in request.POST['delete-value'].split(';'):
            doc = get_document(request, int(n))
            doc.is_in_trash = True
            doc.save()
    except Exception:
        pass
    docs = models.Document.objects.filter(author=user, is_in_trash=False)
    return render(request, 'documents.html', locals())


def sign_up(request):
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
        return redirect("documents")
    return render(request, 'sign-up.html', locals())


@login_required
def documents_search(request, context_length=50):
    user = get_user(request)
    docs = models.Document.objects.filter(author=user, is_in_trash=False)
    data = json.loads(request.POST['data'])
    search_value = data["searchValue"]
    response = []
    # On parcourt les documents, et on envoie ceux contenant les termes de la recherche
    # Cette structure peut être étendue à une regex
    for doc in docs:
        position = doc.content.lower().find(search_value)
        # Si l'on trouve le texte rechercé
        if position != -1:
            # On récupère ce qu'il y a avant, dans, et après le contenu
            pre = doc.content[max(0, position - context_length):position]
            con = doc.content[position:position + len(search_value)]
            post = doc.content[position + len(search_value):min(
                len(doc.content), position + len(search_value) + context_length)]
            contains_start = position > context_length
            contains_end = position + len(search_value) + context_length < len(doc.content)
            # On rajoute le tout à la liste envoyée
            response.append(
                {"docID": doc.id, "preContent": pre, "content": con, "postContent": post, "containsStart" : contains_start, "containsEnd" : contains_end})
    response = json.dumps(response)
    return (HttpResponse(response))


@login_required
def save_document(request):
    # sécurité
    data = json.loads(request.POST['data'])
    doc = get_document(request, data["docID"])
    doc.content = data["newContent"]
    doc.save()
    return (HttpResponse(""))
