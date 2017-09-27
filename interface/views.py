from django.contrib.auth import authenticate, login, update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.http import Http404
from django.shortcuts import render, redirect, HttpResponse, reverse

from . import forms, models

import json
import uuid


def get_user(request):
    return models.Utilisateur.objects.get(username=request.user.username)


def get_document(request, n=False, adress=False):
    """Utility function allowing to get a document in a request (while also checking the user) by id or adress"""
    try:
        if n:
            doc = models.Document.objects.get(id=n)
            if doc.author.username == request.user.username:
                return doc
        elif adress:
            doc = models.Document.objects.get(adress=adress)
            if doc.author.username == request.user.username:
                return doc
    except Exception as exception:
        print("Exception :", exception)
    return None


@login_required
def account(request):
    user = get_user(request)
    email_form = forms.ChangeEmailForm(
        None, initial={'email': request.user.email})
    password_form = forms.ChangePasswordForm(request.user, None)
    suppression_form = forms.DeleteAccountForm(request.user, None)
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
    uid = uuid.uuid4()
    while models.Document.objects.filter(adress=uid):
        uid = uuid.uuid4()
    doc.adress = uid
    doc.save()
    return redirect("document", doc.adress)


@login_required
def change_email(request):
    user = get_user(request)
    if request.POST:
        email_form = forms.ChangeEmailForm(
            request.POST, initial={'email': request.user.email})
        if email_form.is_valid():
            user.email = email_form.cleaned_data['email']
            user.save()
            return HttpResponse(json.dumps({"action": "informSuccess"}))
    else:
        email_form = forms.ChangeEmailForm(
            None, initial={'email': request.user.email})
    return HttpResponse(json.dumps({"action": "updateForm", "html": str(email_form)}))


@login_required
def change_password(request):
    user = get_user(request)
    if request.POST:
        password_form = forms.ChangePasswordForm(request.user, request.POST)
        if password_form.is_valid():
            user.set_password(password_form.cleaned_data['new_password'])
            user.save()
            update_session_auth_hash(request, user)
            return HttpResponse(json.dumps({"action": "informSuccess"}))
    else:
        password_form = forms.ChangePasswordForm(request.user, None)
    return HttpResponse(json.dumps({"action": "updateForm", "html": str(password_form)}))


@login_required
def delete_account(request):
    user = get_user(request)
    if request.POST:
        suppression_form = forms.DeleteAccountForm(request.user, request.POST)
        if suppression_form.is_valid():
            docs = models.Document.objects.filter(author=user)
            for doc in docs:
                doc.delete()
            user.delete()
            return HttpResponse(json.dumps({"action": "redirect", "newAdress": reverse(sign_up)}))
    else:
        suppression_form = forms.DeleteAccountForm(request.user, None)
    return HttpResponse(json.dumps({"action": "updateForm", "html": str(suppression_form)}))


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
            contains_end = position + \
                len(search_value) + context_length < len(doc.content)
            # On rajoute le tout à la liste envoyée
            response.append(
                {"docID": doc.id, "preContent": pre, "content": con, "postContent": post,
                 "containsStart": contains_start, "containsEnd": contains_end})
    response = json.dumps(response)
    return HttpResponse(response)


@login_required
def save_document(request):
    # sécurité ?
    data = json.loads(request.POST['data'])
    doc = get_document(request, n=data["docID"])
    doc.content = data["newContent"]
    doc.save()
    return HttpResponse(json.dumps({"result": True}))


@login_required
def document(request, adress):
    doc = get_document(request, adress=adress)
    if doc:
        if doc.is_in_trash:
            return redirect("error_400")
        return render(request, 'document.html', locals())
    raise Http404


@login_required
def documents(request):
    user = get_user(request)
    try:
        for n in request.POST['delete-value'].split(';'):
            doc = get_document(request, n=int(n))
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
