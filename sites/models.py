#site/models
from django.db import models
from netsup.settings import URL_QR
import qrcode
from io import BytesIO
from django.core.files import File
from django.conf import settings
import re
from django.db import transaction
from django.utils.text import slugify

class Site(models.Model):
    nom = models.CharField(max_length=200)
    code_site = models.CharField(max_length=50, unique=True)

    adresse = models.CharField(max_length=255,blank=True, null=True)
    client_nom = models.CharField(max_length=200, blank=True, null=True)

    nombre_techniciens_prevus = models.IntegerField()

    latitude = models.FloatField(null=True, blank=True)
    longitude = models.FloatField(null=True, blank=True)

    qr_code = models.ImageField(upload_to='qr_codes/', blank=True, null=True)

    actif = models.BooleanField(default=True)

    superviseur = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='sites_supervises',
        verbose_name='Superviseur'
    )

    def __str__(self):
        return self.nom


    def generate_code_site(self):
        base_code = slugify(self.nom).replace("-", "_")

        with transaction.atomic():
            existing_codes = list(
                Site.objects.select_for_update().filter(
                    code_site__regex=rf"^{base_code}(-\d+)?$"
                ).values_list("code_site", flat=True)
            )

            # ✅ Aucun existant → code simple
            if base_code not in existing_codes:
                return base_code

            # ✅ Extraire les suffixes existants
            numbers = []
            pattern = re.compile(rf"^{base_code}-(\d+)$")

            for code in existing_codes:
                match = pattern.match(code)
                if match:
                    numbers.append(int(match.group(1)))

            next_number = 1 if not numbers else max(numbers) + 1

            return f"{base_code}-{next_number}"

    def generate_qr_code(self):
        url = f"{URL_QR}/{self.id}"
        qr = qrcode.make(url)
        buffer = BytesIO()
        qr.save(buffer, format="PNG")
        filename = f"site_{self.id}.png"
        self.qr_code.save(filename, File(buffer), save=False)
    
    def save(self, *args, **kwargs):
        creating = self.pk is None

        # Générer le code seulement à la création
        if creating and not self.code_site:
            self.code_site = self.generate_code_site()

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
