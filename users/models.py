#models/users 
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.models import UserManager as DjangoUserManager
from django.db import models
from tomlkit import datetime
from datetime import datetime

from django.db import transaction
from datetime import datetime
    

from sites.models import Site

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
        'users.Technicien',
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
    
    superviseur = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='techniciens'
    )
    def __str__(self):
        return f"{self.prenom} {self.nom}"
    

    def generate_matricule(self):
        year = datetime.now().year
    
        with transaction.atomic():
            last = (
                Technicien.objects
                .select_for_update()
                .filter(matricule__startswith=f"TECH-{year}")
                .order_by('-id')
                .first()
            )
    
            if last and last.matricule:
                try:
                    last_number = int(last.matricule.split('-')[-1])
                except ValueError:
                    last_number = 0
            else:
                last_number = 0
    
            new_number = last_number + 1
    
            return f"TECH-{year}-{str(new_number).zfill(4)}"

    def get_sites_actifs(self):
        """Retourne tous les sites sur lesquels cet agent est actuellement affecté."""
        return Site.objects.filter(
            affectations__technicien=self,
            affectations__actif=True
        ).distinct()

    def save(self, *args, **kwargs):
        creating = self.pk is None
    
        if creating and not self.matricule:
            self.matricule = self.generate_matricule()
    
        super().save(*args, **kwargs)

    
    


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
