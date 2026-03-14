#controles/models
from django.db import models
from django.conf import settings
from sites.models import Site


class ControleSite(models.Model):

    site = models.ForeignKey(Site, on_delete=models.CASCADE)

    superviseur = models.ForeignKey( settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    date = models.DateTimeField(auto_now_add=True)

    gps_lat = models.FloatField(null=True, blank=True)
    gps_long = models.FloatField(null=True, blank=True)

    techniciens_prevus = models.IntegerField()
    techniciens_presents = models.IntegerField()
    techniciens_absents = models.IntegerField()

    ETAT_CHOICES = [
        ('tres_propre', 'Très propre'),
        ('propre', 'Propre'),
        ('moyen', 'Moyen'),
        ('mauvais', 'Mauvais')
    ]

    etat_proprete = models.CharField(max_length=20, choices=ETAT_CHOICES)
    
    incident = models.BooleanField(default=False)
    problemes = models.TextField(blank=True)
    
    incident_resolu = models.BooleanField(default=False)
    date_resolution = models.DateTimeField(null=True, blank=True)
    
    observations = models.TextField(blank=True)

    photo_site = models.ImageField(upload_to='sites/', blank=True, null=True)

    photo_presence = models.ImageField(upload_to='presence/', blank=True, null=True)

    def __str__(self):
        return f"{self.site} - {self.date}"