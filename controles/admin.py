from django.contrib import admin
from controles.models import ControleSite, PointageAgent

@admin.register(ControleSite)
class ControleSiteAdmin(admin.ModelAdmin):
    list_display = ['site', 'superviseur', 'date', 'etat_proprete', 'techniciens_presents', 'techniciens_absents', 'incident']
    list_filter = ['etat_proprete', 'incident', 'incident_resolu', 'site']
    search_fields = ['site__nom', 'superviseur__username']
    date_hierarchy = 'date'

@admin.register(PointageAgent)
class PointageAgentAdmin(admin.ModelAdmin):
    list_display = ['technicien', 'controle', 'present', 'motif_absence']
    list_filter = ['present', 'motif_absence']
    search_fields = ['technicien__nom', 'technicien__prenom']
