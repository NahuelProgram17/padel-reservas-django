from django import forms
from datetime import time
from .models import Reserva, Cancha


class ReservaForm(forms.ModelForm):
    class Meta:
        model = Reserva
        fields = ['cancha', 'fecha', 'hora']
        widgets = {
            'fecha': forms.DateInput(attrs={'type': 'date'}),
            'hora': forms.Select(),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['cancha'].queryset = Cancha.objects.filter(activa=True)
        self.fields['hora'].choices = []

    def clean_hora(self):
        hora = self.cleaned_data['hora']

        if hora < time(10, 0) or hora >= time(22, 0):
            raise forms.ValidationError(
                "Las reservas solo están disponibles entre las 10:00 y las 22:00."
            )

        return hora
