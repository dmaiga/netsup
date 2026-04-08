from django.urls import path
from users.views import *

urlpatterns = [

    path("dashboard/superviseur/", dashboard_superviseur, name="dashboard_superviseur"),

    path("backoffice/", dashboard_direction, name="dashboard_admin"),
    path("backoffice/resoudre_incident/<int:controle_id>/", resoudre_incident, name="resoudre_incident"),
    path("backoffice/couverture_hebdo/", couverture_hebdo, name="couverture_hebdo"),

    # Rapport de présence (croisé agent × site)
    path('backoffice/rapport-presence/', rapport_presence, name='rapport_presence'),

    path('backoffice/rapports/', admin_rapport_list, name='admin_rapport_list'),
    path('backoffice/rapports/<int:pk>/', admin_rapport_detail, name='admin_rapport_detail'),

    # Anciennes routes affectation FK (conservées compatibilité)
#    path('backoffice/site/<int:site_id>/affecter/', affecter_technicien_existant, name='affecter_technicien'),
#    path('backoffice/technicien/<int:tech_id>/retirer/', retirer_technicien_site, name='retirer_technicien'),

    path('backoffice/incidents/', liste_incidents_critiques, name='liste_incidents_critiques'),
    path('personnel/list/', user_list, name='user_list'),
    path("personnel/detail/<int:pk>/", user_detail, name="user_detail"),
    
    path('personnel/create/', user_create, name='user_create'),
    path('personnel/update/<int:pk>/', user_update, name='user_update'),
    path('technicien/creer/', technicien_create, name='technicien_create_global'),
    path('technicien/<int:pk>/modifier/', technicien_update, name='technicien_update'),
    path('technicien/<int:pk>/supprimer/', technicien_soft_delete, name='technicien_soft_delete'),
    path('technicien/<int:pk>/', technicien_detail, name='technicien_detail'),
    path('personnel/toggle/<int:pk>/', user_toggle_active, name='user_toggle_active'),
    path('personnel/delete/<int:pk>/', user_soft_delete, name='user_soft_delete'),
]
