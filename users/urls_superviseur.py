# users/urls_superviseur.py

from django.urls import path

from . import views_superviseur


urlpatterns = [

    path(
        'techniciens/create/',
        views_superviseur.create_technicien,
        name='create_technicien'
    ),
    path(
        'techniciens/',
        views_superviseur.technicien_list,
        name='technicien_list'
    ),

    path(
        'techniciens/<int:pk>/',
        views_superviseur.technicien_detail,
        name='technicien_detail'
    ),
]