from django.urls import path
from .views import (
    home,
    crear_reserva,
    mis_reservas,
    ver_calendario,
    calendario_disponibilidad,
)

app_name = 'reservas'

urlpatterns = [
    path('', home, name='home'),
    path('reservar/', crear_reserva, name='crear_reserva'),
    path('mis-reservas/', mis_reservas, name='mis_reservas'),
    path('ver-calendario/', ver_calendario, name='ver_calendario'),
    path('calendario/', calendario_disponibilidad, name='calendario'),
]

