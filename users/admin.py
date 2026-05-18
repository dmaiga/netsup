from django.contrib import admin

from users.models import Technicien, User


admin.site.register(User)


@admin.register(Technicien)
class TechnicienAdmin(admin.ModelAdmin):

    list_display = [
        'nom',
        'prenom',
        'telephone',
        'superviseur',
        'actif'
    ]

    list_filter = [
        'actif',
        'genre',
        'superviseur'
    ]

    search_fields = [
        'nom',
        'prenom',
        'telephone',
        'matricule',
        'superviseur__username',
        'superviseur__first_name',
        'superviseur__last_name'
    ]