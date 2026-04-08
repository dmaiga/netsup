#site/models
from django.db import models
from netsup.settings import URL_QR
import qrcode
from io import BytesIO
from django.core.files import File
from django.conf import settings


class Site(models.Model):

    nom = models.CharField(max_length=200)
    code_site = models.CharField(max_length=50, unique=True)

    adresse = models.CharField(max_length=255)
    client_nom = models.CharField(max_length=200)

    nombre_techniciens_prevus = models.IntegerField()

    latitude = models.FloatField(null=True, blank=True)
    longitude = models.FloatField(null=True, blank=True)

    qr_code = models.ImageField(upload_to='qr_codes/', blank=True, null=True)

    actif = models.BooleanField(default=True)
    superviseur = models.ForeignKey(
        settings.AUTH_USER_MODEL,  # Utilisation du modèle utilisateur par défaut
        on_delete=models.SET_NULL,  # Si le superviseur est supprimé, le champ devient null
        null=True,  # Permet que ce champ soit vide
        blank=True,  # Permet que ce champ soit vide dans les formulaires
        related_name='sites_supervises',  # Permet d'accéder aux sites supervisés depuis un utilisateur
        verbose_name='Superviseur'
    )

    def __str__(self):
        return self.nom

    def generate_qr_code(self):
        url = f"{URL_QR}/{self.id}"
        qr = qrcode.make(url)
        buffer = BytesIO()
        qr.save(buffer, format="PNG")
        filename = f"site_{self.id}.png"
        self.qr_code.save(filename, File(buffer), save=False)

    def save(self, *args, **kwargs):
        creating = self.pk is None
        super().save(*args, **kwargs)
        if creating and not self.qr_code:
            self.generate_qr_code()
            super().save(update_fields=["qr_code"])

    def get_agents_actifs(self):
        """Retourne les techniciens actuellement affectés à ce site."""
        from users.models import Technicien
        return Technicien.objects.filter(
            affectations__site=self,
            affectations__actif=True
        ).distinct()


class AffectationAgent(models.Model):
    """
    Relation M2M entre Technicien et Site.
    Un agent peut être sur plusieurs sites simultanément.
    """
    technicien = models.ForeignKey(
         'users.Technicien',
        on_delete=models.CASCADE,
        related_name='affectations'
    )
    site = models.ForeignKey(
        Site,
        on_delete=models.CASCADE,
        related_name='affectations'
    )
    date_debut = models.DateField(auto_now_add=True)
    date_fin = models.DateField(null=True, blank=True)
    actif = models.BooleanField(default=True)

    class Meta:
        unique_together = ('technicien', 'site')
        ordering = ['-date_debut']

    def __str__(self):
        statut = "actif" if self.actif else "inactif"
        return f"{self.technicien} → {self.site} ({statut})"
