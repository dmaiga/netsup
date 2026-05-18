# users/urls_superviseur.py

from django.urls import path

from . import views_superviseur


urlpatterns = [

    path(
        'techniciens/create/',
        views_superviseur.create_technicien,
        name='create_technicien'
    ),

]