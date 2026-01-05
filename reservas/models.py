from django.db import models
from django.contrib.auth.models import User


class Cancha(models.Model):
    TIPO_CHOICES = [
        ('indoor', 'Indoor'),
        ('outdoor', 'Outdoor'),
    ]

    nombre = models.CharField(max_length=50)
    tipo = models.CharField(max_length=10, choices=TIPO_CHOICES)
    precio_por_hora = models.PositiveIntegerField(default=150000)
    activa = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.nombre} ({self.tipo})"
    
class Reserva(models.Model):
    ESTADO_CHOICES = [
        ('activa', 'Activa'),
        ('cancelada', 'Cancelada'),
    ]

    usuario = models.ForeignKey(User, on_delete=models.CASCADE, related_name='reservas')
    cancha = models.ForeignKey(Cancha, on_delete=models.CASCADE)
    fecha = models.DateField()
    hora = models.TimeField()
    estado = models.CharField(
        max_length=10,
        choices=ESTADO_CHOICES,
        default='activa'
    )
    creada_en = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('cancha', 'fecha', 'hora')
        ordering = ['fecha', 'hora']

    def __str__(self):
        return f"{self.cancha} - {self.fecha} {self.hora}"
