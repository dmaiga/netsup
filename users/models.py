#models/users 
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.models import UserManager as DjangoUserManager
from django.db import models


class UserManager(DjangoUserManager):

    def get_queryset(self):
        return super().get_queryset().filter(is_deleted=False)


class User(AbstractUser):

    ROLE_CHOICES = (
        ('superviseur', 'Superviseur'),
        ('admin', 'Administration'),
        ('direction', 'Direction'),
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