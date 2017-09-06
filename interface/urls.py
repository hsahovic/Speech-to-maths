from django.contrib.auth import views as auth_views
from django.conf.urls import url
from django.views.generic import TemplateView

from . import views

urlpatterns = [
    url(r'^$', TemplateView.as_view(template_name="index.html")),
    url(r'^index$', TemplateView.as_view(template_name="index.html"), name='index'),

    url(r'^log-out$', auth_views.logout, {
        'next_page': 'index'}, name='log_out'),
    url(r'^sign-in$', auth_views.login, {
        'template_name': 'sign-in.html'}, name='sign_in'),
    url(r'^sign-up$', views.sign_up, name='sign_up'),

    url(r'^new_document$', views.add_doc, name='add_doc'),
    url(r'^document/(\d+)$', views.document, name='document'),
    url(r'^documents$', views.documents, name='documents'),

    url(r'^account$', views.account, name='account'),
    
    url(r'^400$', TemplateView.as_view(template_name="400.html"), name = "error_400"),
    url(r'^403$', TemplateView.as_view(template_name="403.html"), name = "error_403"),
    url(r'^404$', TemplateView.as_view(template_name="404.html"), name = "error_404"),
    url(r'^500$', TemplateView.as_view(template_name="500.html"), name = "error_500"),

    url(r'^ajax/documents-search$', views.documents_search, name='documents_search'),
]
