from django.db import models

class Zone(models.Model):
    TYPE_CHOICES = [
        ('section', 'Section'),
        ('bloc', 'Bloc'),
        ('allee', 'Allée'),
        ('non_exploitable', 'Zone non exploitable'),
    ]

    nom = models.CharField(max_length=100)
    type_zone = models.CharField(max_length=20, choices=TYPE_CHOICES)
    description = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.nom} ({self.type_zone})"

    class Meta:
        verbose_name = "Zone"
        verbose_name_plural = "Zones"


class Caveau(models.Model):
    ETAT_CHOICES = [
        ('disponible', 'Disponible'),
        ('reserve', 'Réservé'),
        ('occupe', 'Occupé'),
        ('non_exploitable', 'Non exploitable'),
    ]

    zone = models.ForeignKey(Zone, on_delete=models.CASCADE, related_name='caveaux')
    numero = models.CharField(max_length=20, unique=True)
    latitude = models.FloatField()
    longitude = models.FloatField()
    longueur = models.FloatField(help_text="Longueur en mètres")
    largeur = models.FloatField(help_text="Largeur en mètres")
    etat = models.CharField(max_length=20, choices=ETAT_CHOICES, default='disponible')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Caveau {self.numero} - {self.etat}"

    class Meta:
        verbose_name = "Caveau"
        verbose_name_plural = "Caveaux"