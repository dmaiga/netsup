#models/users 
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.models import UserManager as DjangoUserManager
from django.db import models

from sites.models import Site


class Technicien(models.Model):
    matricule = models.CharField(max_length=50, unique=True)
    nom = models.CharField(max_length=100)
    prenom = models.CharField(max_length=100)
    genre = models.CharField(max_length=10, choices=(('M','Homme'),('F','Femme')))
    date_naissance = models.DateField(null=True, blank=True)
    lieu_naissance = models.CharField(max_length=150, blank=True)
    quartier = models.CharField(max_length=150, blank=True)
    telephone = models.CharField(max_length=20, unique=True)
    photo = models.ImageField(upload_to='techniciens/', blank=True, null=True)
    actif = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.prenom} {self.nom}"
       
    def get_sites_actifs(self):
        """Retourne tous les sites sur lesquels cet agent est actuellement affecté."""
        return Site.objects.filter(
            affectations__technicien=self,
            affectations__actif=True
        ).distinct()

    
    
class UserManager(DjangoUserManager):

    def get_queryset(self):
        return super().get_queryset().filter(is_deleted=False)


class User(AbstractUser):

    ROLE_CHOICES = (
        ('superviseur', 'Superviseur'),
        ('admin', 'Administration'),
        ('direction', 'Direction'),
    )
    technicien = models.OneToOneField(
        Technicien,
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )
    role = models.CharField(max_length=20, choices=ROLE_CHOICES)

    telephone = models.CharField(max_length=20, unique=True)

    photo = models.ImageField(upload_to='users/', blank=True, null=True)

    objects = UserManager()

    is_active = models.BooleanField(default=True)

    is_deleted = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.username} - {self.role}"
    
    @property
    def full_name(self):
        if self.first_name and self.last_name:
            return f"{self.first_name} {self.last_name}"
        return self.username


class Conge(models.Model):

    technicien = models.ForeignKey(Technicien, on_delete=models.CASCADE)

    date_debut = models.DateField()
    date_fin = models.DateField()

    motif = models.CharField(max_length=100)

    valide = models.BooleanField(default=False)

class ProfilRH(models.Model):
    technicien = models.OneToOneField(Technicien, on_delete=models.CASCADE, related_name="rh")
    TYPE_CONTRAT = (
        ('cdi', 'CDI'),
        ('cdd', 'CDD'),
        ('prestation', 'Prestation'),
    )
    type_contrat = models.CharField(max_length=20, choices=TYPE_CONTRAT)

    niveau_contrat = models.IntegerField(default=1)  # renouvellement

    numero_inps = models.CharField(max_length=50, blank=True)
    numero_amo = models.CharField(max_length=50, blank=True)

    salaire = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)

    TYPE_HORAIRE = (
        ('temps_plein', 'Temps plein'),
        ('mi_temps', 'Mi-temps'),
    )

    type_horaire = models.CharField(max_length=20, choices=TYPE_HORAIRE)

    DISPONIBILITE = (
        ('matin', 'Matin'),
        ('soir', 'Soir'),
        ('les_deux', 'Les deux'),
    )

    disponibilite = models.CharField(max_length=20, choices=DISPONIBILITE)

    date_embauche = models.DateField(null=True, blank=True)

    def __str__(self):
        return f"RH - {self.technicien}"
