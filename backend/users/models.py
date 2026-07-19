from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    ROLE_CHOICES = [
        ('admin', 'Administrateur'),
        ('agent', 'Agent de terrain'),
        ('secretariat', 'Secrétariat'),
        ('client', 'Client'),
    ]

    STATUT_CHOICES = [
        ('en_attente', 'En attente'),
        ('approuve', 'Approuvé'),
        ('refuse', 'Refusé'),
    ]

    role = models.CharField(
        max_length=20,
        choices=ROLE_CHOICES,
        default='client'
    )
    statut = models.CharField(
        max_length=20,
        choices=STATUT_CHOICES,
        default='approuve'
    )
    phone = models.CharField(max_length=20, blank=True, null=True)
    mfa_code = models.CharField(max_length=6, blank=True, null=True)
    mfa_verified = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    groups = models.ManyToManyField(
        'auth.Group',
        related_name='custom_user_set',
        blank=True
    )
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        related_name='custom_user_set',
        blank=True
    )

    def __str__(self):
        return f"{self.username} ({self.role})"

    class Meta:
        verbose_name = "Utilisateur"
        verbose_name_plural = "Utilisateurs"