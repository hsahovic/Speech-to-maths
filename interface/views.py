from django.http import HttpResponse
from django.shortcuts import render, redirect
from . import forms, models

def index(request):
    return render(request, 'index.html', locals())

def inscription (request):
    
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
        return redirect("index")
    return render(request, 'inscription.html', locals())