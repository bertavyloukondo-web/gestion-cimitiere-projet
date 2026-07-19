from django.db import models
from users.models import User
from terrain.models import Caveau
from reservations.models import Reservation


class Concession(models.Model):
    TYPE_CHOICES = [
        ('temporaire', 'Temporaire'),
        ('perpetuelle', 'Perpétuelle'),
    ]
    STATUT_CHOICES = [
        ('active', 'Active'),
        ('expiree', 'Expirée'),
        ('resiliee', 'Résiliée'),
    ]

    reservation = models.OneToOneField(Reservation, on_delete=models.CASCADE, related_name='concession')
    client = models.ForeignKey(User, on_delete=models.CASCADE, related_name='concessions')
    caveau = models.ForeignKey(Caveau, on_delete=models.CASCADE, related_name='concessions')
    type_concession = models.CharField(max_length=20, choices=TYPE_CHOICES)
    statut = models.CharField(max_length=20, choices=STATUT_CHOICES, default='active')
    date_debut = models.DateField()
    date_fin = models.DateField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Concession {self.id} - {self.client} ({self.statut})"

    class Meta:
        verbose_name = "Concession"
        verbose_name_plural = "Concessions"


class Exhumation(models.Model):
    STATUT_CHOICES = [
        ('demandee', 'Demandée'),
        ('validee', 'Validée'),
        ('effectuee', 'Effectuée'),
        ('refusee', 'Refusée'),
    ]

    concession = models.ForeignKey(Concession, on_delete=models.CASCADE, related_name='exhumations')
    demandeur = models.ForeignKey(User, on_delete=models.CASCADE, related_name='exhumations')
    motif = models.TextField()
    statut = models.CharField(max_length=20, choices=STATUT_CHOICES, default='demandee')
    date_demande = models.DateTimeField(auto_now_add=True)
    date_validation = models.DateTimeField(blank=True, null=True)
    valide_par = models.ForeignKey(
        User, on_delete=models.SET_NULL,
        null=True, blank=True,
        related_name='exhumations_validees'
    )

    def __str__(self):
        return f"Exhumation {self.id} - {self.statut}"

    class Meta:
        verbose_name = "Exhumation"
        verbose_name_plural = "Exhumations"