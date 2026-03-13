from django.urls import path
from sites.views import *

urlpatterns = [

    path(
        "superviseur/sites/",
        superviseur_sites,
        name="superviseur_sites"
    )
]

