# sites/urls_superviseur.py

from django.urls import path

from . import views_superviseur


urlpatterns = [

    path(
        'create/',
        views_superviseur.create_site,
        name='create_site'
    ),
    path(
        '',
        views_superviseur.liste_site,
        name='liste_site'
    ),

    path(
        '<int:site_id>/',
        views_superviseur.site_detail,
        name='site_detail'
    ),

    path(
        '<int:site_id>/affecter-technicien/',
        views_superviseur.affecter_technicien,
        name='affecter_technicien'
    ),

    path(
        'retirer-technicien/<int:affectation_id>/',
        views_superviseur.retirer_technicien,
        name='retirer_technicien'
    ),

]