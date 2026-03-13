#controles/urls
from django.urls import path
from controles.views import *
urlpatterns = [

    path(
        "controle/<int:site_id>/",
        controle_site,
        name="controle_site"
    ),
    path(
        "historique/",
        controle_list,
        name="controle_list"
    ),

    path(
        "historique/<int:pk>/",
        controle_detail,
        name="controle_detail"
    ),
   path(
        "scan/",
        scan,
        name="scan"
    ),

]