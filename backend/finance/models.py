from django.db import models
from users.models import User
from reservations.models import Reservation


class Facture(models.Model):
    STATUT_CHOICES = [
        ('en_attente', 'En attente'),
        ('payee', 'Payée'),
        ('partiellement_payee', 'Partiellement payée'),
        ('annulee', 'Annulée'),
    ]

    reservation = models.OneToOneField(Reservation, on_delete=models.CASCADE, related_name='facture')
    client = models.ForeignKey(User, on_delete=models.CASCADE, related_name='factures')
    numero = models.CharField(max_length=50, unique=True)
    montant_total = models.DecimalField(max_digits=10, decimal_places=2)
    montant_paye = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    statut = models.CharField(max_length=25, choices=STATUT_CHOICES, default='en_attente')
    date_emission = models.DateTimeField(auto_now_add=True)
    date_echeance = models.DateField()

    def __str__(self):
        return f"Facture {self.numero} - {self.statut}"

    class Meta:
        verbose_name = "Facture"
        verbose_name_plural = "Factures"


class Paiement(models.Model):
    MODE_CHOICES = [
        ('mobile_money', 'Mobile Money'),
        ('airtel_money', 'Airtel Money'),
        ('especes', 'Espèces'),
        ('virement', 'Virement'),
    ]

    facture = models.ForeignKey(Facture, on_delete=models.CASCADE, related_name='paiements')
    montant = models.DecimalField(max_digits=10, decimal_places=2)
    mode_paiement = models.CharField(max_length=20, choices=MODE_CHOICES)
    reference = models.CharField(max_length=100, blank=True, null=True)
    date_paiement = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Paiement {self.id} - {self.montant} ({self.mode_paiement})"

    class Meta:
        verbose_name = "Paiement"
        verbose_name_plural = "Paiements"