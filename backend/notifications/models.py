from django.db import models
from users.models import User


class Notification(models.Model):
    TYPE_CHOICES = [
        ('reservation', 'Nouvelle réservation'),
        ('validation', 'Validation réservation'),
        ('facture', 'Facture émise'),
        ('paiement', 'Paiement reçu'),
        ('alerte', 'Alerte'),
        ('mfa', 'Code MFA'),
    ]

    destinataire = models.ForeignKey(User, on_delete=models.CASCADE, related_name='notifications')
    type_notification = models.CharField(max_length=20, choices=TYPE_CHOICES)
    sujet = models.CharField(max_length=200)
    message = models.TextField()
    lu = models.BooleanField(default=False)
    envoye_par_email = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.type_notification} - {self.destinataire} ({'lu' if self.lu else 'non lu'})"

    class Meta:
        verbose_name = "Notification"
        verbose_name_plural = "Notifications"
        ordering = ['-created_at']