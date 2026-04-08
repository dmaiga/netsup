from django.contrib import admin
from users.models import Technicien, User


admin.site.register(User)



@admin.register(Technicien)
class TechnicienAdmin(admin.ModelAdmin):
    list_display = ['nom', 'prenom', 'actif']
    list_filter = [ 'actif']
    search_fields = ['nom', 'prenom']


