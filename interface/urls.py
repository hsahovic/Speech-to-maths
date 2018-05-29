from django.contrib.auth import views as auth_views
from django.conf.urls import url
from django.views.generic import TemplateView

from . import views

urlpatterns = [
    url(r'^$', TemplateView.as_view(template_name="index.html")),
    url(r'^index/?$', TemplateView.as_view(template_name="index.html"), name='index'),

    #url(r'^log-out/?$', auth_views.logout, {
        #'next_page': 'index'}, name='log_out'),
    url(r'^log-out/?$', views.log_out, {
        'next_page': 'index'}, name='log_out'),
    url(r'^sign-in/?$', auth_views.login, {
        'template_name': 'sign-in.html'}, name='sign_in'),
    url(r'^sign-up/?$', views.sign_up, name='sign_up'),

    url(r'^new_document/?$', views.add_doc, name='add_doc'),
    url(r'^documents/?$', views.documents, name='documents'),
    url(r"""^document/([a-zA-Z0-9]{8}-[a-zA-Z0-9]{4}-[a-zA-Z0-9]{4}-[a-zA-Z0-9]{4}-[a-zA-Z0-9]{12})/?$""", views.document, name='document'),

    url(r'^account/?$', views.account, name='account'),

    url(r'^training/?$', views.training, name='training'),

    url(r'^400/?$', TemplateView.as_view(template_name="400.html"), name="error_400"),
    url(r'^403/?$', TemplateView.as_view(template_name="403.html"), name="error_403"),
    url(r'^404/?$', TemplateView.as_view(template_name="404.html"), name="error_404"),
    url(r'^500/?$', TemplateView.as_view(template_name="500.html"), name="error_500"),

    url(r'^ajax/documents-search/?$',
        views.documents_search, name='documents_search'),
    url(r"""^ajax/regenerate-pdf/([a-zA-Z0-9]{8}-[a-zA-Z0-9]{4}-[a-zA-Z0-9]{4}-[a-zA-Z0-9]{4}-[a-zA-Z0-9]{12})/?$""", views.regenerate_pdf, name='regenerate_pdf'),
    url(r'^ajax/save-document/?$', views.save_document, name='save_document'),

    url(r'^ajax/change-email/?$', views.change_email, name='change_email'),
    url(r'^ajax/change-password/?$', views.change_password, name='change_password'),
    url(r'^ajax/delete-account/?$', views.delete_account, name='delete_account'),
]
