from django.db import models
from users.models import User
from terrain.models import Caveau


class Reservation(models.Model):
    STATUT_CHOICES = [
        ('en_attente', 'En attente'),
        ('validee', 'Validée'),
        ('refusee', 'Refusée'),
        ('annulee', 'Annulée'),
    ]

    MODE_PAIEMENT_CHOICES = [
        ('mobile_money', 'Mobile Money'),
        ('airtel_money', 'Airtel Money'),
        ('especes', 'Especes'),
        ('virement', 'Virement'),
    ]

    client = models.ForeignKey(User, on_delete=models.CASCADE, related_name='reservations')
    caveau = models.ForeignKey(Caveau, on_delete=models.CASCADE, related_name='reservations')

    # Infos défunt
    nom_defunt = models.CharField(max_length=100)
    prenom_defunt = models.CharField(max_length=100)
    date_naissance_defunt = models.DateField()
    date_deces_defunt = models.DateField()

    statut = models.CharField(max_length=20, choices=STATUT_CHOICES, default='en_attente')
    date_reservation = models.DateTimeField(auto_now_add=True)
    date_validation = models.DateTimeField(blank=True, null=True)
    valide_par = models.ForeignKey(
        User, on_delete=models.SET_NULL,
        null=True, blank=True,
        related_name='reservations_validees'
    )
    mode_paiement_prefere = models.CharField(max_length=20, choices=MODE_PAIEMENT_CHOICES, default='especes')
    notes = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"Réservation {self.id} - {self.nom_defunt} ({self.statut})"

    class Meta:
        verbose_name = "Réservation"
        verbose_name_plural = "Réservations"