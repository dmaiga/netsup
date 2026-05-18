from django.contrib import admin
from sites.models import Site,  AffectationAgent

from users.models import User,Technicien

@admin.register(Site)
class SiteAdmin(admin.ModelAdmin):

    list_display = [
        'nom',
        'code_site',
        'client_nom',
        'superviseur',
        'nombre_techniciens_prevus',
        'actif'
    ]

    list_filter = [
        'actif',
        'superviseur'
    ]

    search_fields = [
        'nom',
        'code_site',
        'client_nom',
        'superviseur__username',
        'superviseur__first_name',
        'superviseur__last_name'
    ]
    
@admin.register(AffectationAgent)
class AffectationAgentAdmin(admin.ModelAdmin):
    list_display = ['technicien', 'site', 'actif', 'date_debut', 'date_fin']
    list_filter = ['actif', 'site']
    search_fields = ['technicien__nom', 'technicien__prenom', 'site__nom']
