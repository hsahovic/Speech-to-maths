from django.contrib.auth import views as auth_views
from django.conf.urls import url

from . import views
        
urlpatterns = [
    url(r'^$', views.index),
    url(r'^index/$', views.index, name = 'index'),
    url(r'^connexion$', auth_views.login, {'template_name': 'connexion.html'}, name = 'connexion'),
    url(r'^inscription$', views.inscription, name = 'inscription'),
    url(r'^deconnexion$', auth_views.logout, {'next_page': 'index'}, name = 'deconnexion'),
    url(r'^mes_documents$', views.docs, name = 'docs'),
    url(r'^nouveau_document$', views.add_doc, name = 'add_doc'),
    url(r'^document/(\d+)$', views.document, name = 'document'),
    url(r'^mon_compte$', views.compte, name = 'compte'),
#    url(r'^suppression_compte$', views.suppression_compte, name = 'suppression_compte'),
]