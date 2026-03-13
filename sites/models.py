from django.db import models
from netsup.settings import URL_QR
import qrcode
from io import BytesIO
from django.core.files import File
    

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

class Technicien(models.Model):

    nom = models.CharField(max_length=100)
    prenom = models.CharField(max_length=100)

    photo = models.ImageField(upload_to='techniciens/', blank=True, null=True)

    telephone = models.CharField(max_length=20, blank=True)

    TYPE_CONTRAT = (
        ('cdi', 'CDI'),
        ('cdd', 'CDD'),
        ('prestation', 'Prestation'),
    )

    type_contrat = models.CharField(max_length=20, choices=TYPE_CONTRAT)

    site = models.ForeignKey(
        'sites.Site',
        on_delete=models.CASCADE,
        related_name='techniciens'
    )

    actif = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.nom} {self.prenom}"