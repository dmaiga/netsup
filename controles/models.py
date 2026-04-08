#controles/models
from django.db import models
from django.conf import settings



class ControleSite(models.Model):

    site = models.ForeignKey('sites.Site', on_delete=models.CASCADE)
    superviseur = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

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
        ('mauvais', 'Mauvais'),
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

    @property
    def taux_presence(self):
        if self.techniciens_prevus and self.techniciens_prevus > 0:
            return round((self.techniciens_presents / self.techniciens_prevus) * 100)
        return 0


class PointageAgent(models.Model):
    """
    Enregistrement nominal du pointage d'un agent lors d'un contrôle.
    Créé automatiquement pour chaque agent affecté au site au moment du contrôle.
    """
    MOTIF_ABSENCE = [
        ('', '—'),
        ('retard', 'Retard'),
        ('absent_np', 'Absent non prévenu'),
        ('absent_prev', 'Absent prévenu'),
        ('conge', 'Congé'),
        ('maladie', 'Maladie'),
        ('autre', 'Autre'),
    ]

    controle = models.ForeignKey(
        ControleSite,
        on_delete=models.CASCADE,
        related_name='pointages'
    )
    technicien = models.ForeignKey(
        'users.Technicien',
        on_delete=models.CASCADE,
        related_name='pointages'
    )
    present = models.BooleanField(default=True)
    motif_absence = models.CharField(max_length=20, choices=MOTIF_ABSENCE, blank=True, default='')
    commentaire = models.CharField(max_length=200, blank=True)

    class Meta:
        unique_together = ('controle', 'technicien')
        ordering = ['technicien__nom', 'technicien__prenom']

    def __str__(self):
        statut = "présent" if self.present else f"absent ({self.motif_absence})"
        return f"{self.technicien} @ {self.controle.site} — {statut}"
