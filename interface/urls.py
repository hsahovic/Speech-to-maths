from django.contrib.auth import views as auth_views
from django.conf.urls import url
from django.views.generic import TemplateView

from . import views

urlpatterns = [
    url(r'^$', TemplateView.as_view(template_name="index.html")),
    url(r'^index/$', TemplateView.as_view(template_name="index.html"), name='index'),
    url(r'^connexion$', auth_views.login, {
        'template_name': 'connexion.html'}, name='connexion'),
    url(r'^inscription$', views.inscription, name='inscription'),
    url(r'^deconnexion$', auth_views.logout, {
        'next_page': 'index'}, name='deconnexion'),
    url(r'^mes_documents$', views.docs, name='docs'),
    url(r'^nouveau_document$', views.add_doc, name='add_doc'),
    url(r'^document/(\d+)$', views.document, name='document'),
    url(r'^mon_compte$', views.compte, name='compte'),
    url(r'^404$', TemplateView.as_view(template_name="404.html")),
    url(r'^403$', TemplateView.as_view(template_name="403.html")),
    url(r'^400$', TemplateView.as_view(template_name="400.html")),
    url(r'^500$', TemplateView.as_view(template_name="500.html")),
]
