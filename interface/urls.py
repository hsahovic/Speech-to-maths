from django.conf.urls import url
from . import views
from django.contrib.auth import views as auth_views
        
urlpatterns = [
    url(r'^index/', views.index, name = 'index'),
    url(r'^connexion$', auth_views.login, {'template_name': 'connexion.html'}, name = 'connexion'),
    url(r'^inscription$', views.inscription, name = 'inscription'),
    url(r'^deconnexion$', auth_views.logout, {'next_page': 'index'}, name = 'deconnexion'),
]