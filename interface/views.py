from django.http import HttpResponse
from django.shortcuts import render

def css (request):
    return render(request, 'interface/css/style.css', locals())

def index(request):
    return render(request, 'interface/index.html', locals())