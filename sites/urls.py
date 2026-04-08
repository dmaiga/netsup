from django.urls import path
from sites.views import *

urlpatterns = [

    path(
        "superviseur/sites/",
        superviseur_sites,
        name="superviseur_sites"
    ),
    path('backoffice/sites/', admin_site_list, name='admin_site_list'),
    path('backoffice/sites/nouveau/', admin_site_create, name='admin_site_create'),
    path('backoffice/sites/<int:pk>/', admin_site_detail, name='admin_site_detail'),

    # Nouvelle route affectations M2M
    path('backoffice/sites/<int:site_id>/affectations/', gestion_affectations, name='gestion_affectations'),

]

