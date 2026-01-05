from collections import defaultdict

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from django.http import JsonResponse

from .forms import ReservaForm
from .models import Cancha, Reserva
from .utils import generar_horarios


def ver_calendario(request):
    return render(request, 'reservas/calendario.html')


def calendario_disponibilidad(request):
    fecha = request.GET.get('fecha')
    if not fecha:
        return JsonResponse({'data': {}})

    data = defaultdict(list)

    reservas = Reserva.objects.filter(
        fecha=fecha,
        estado='activa'
    ).select_related('cancha')

    for r in reservas:
        data[r.cancha.id].append(r.hora.strftime('%H:%M'))

    canchas = Cancha.objects.filter(activa=True).values('id', 'nombre')

    return JsonResponse({
        'canchas': list(canchas),
        'ocupadas': data
    })


@login_required
def cancelar_reserva(request, reserva_id):
    reserva = get_object_or_404(
        Reserva,
        id=reserva_id,
        usuario=request.user
    )

    reserva.estado = 'cancelada'
    reserva.save()

    return redirect('reservas:mis_reservas')


def horarios_disponibles(request):
    cancha_id = request.GET.get('cancha')
    fecha = request.GET.get('fecha')

    if not cancha_id or not fecha:
        return JsonResponse({'horarios': []})

    reservas = Reserva.objects.filter(
        cancha_id=cancha_id,
        fecha=fecha,
        estado='activa'
    )

    horarios_ocupados = [r.hora for r in reservas]
    horarios = generar_horarios()

    disponibles = [
        h.strftime('%H:%M')
        for h in horarios
        if h not in horarios_ocupados
    ]

    return JsonResponse({'horarios': disponibles})


def home(request):
    canchas = Cancha.objects.filter(activa=True)
    return render(request, 'reservas/home.html', {'canchas': canchas})


@login_required
def crear_reserva(request):
    if request.method == 'POST':
        form = ReservaForm(request.POST)
        if form.is_valid():
            reserva = form.save(commit=False)
            reserva.usuario = request.user

            try:
                reserva.save()
                return redirect('reservas:mis_reservas')  # ✅ CORREGIDO
            except IntegrityError:
                form.add_error(
                    None,
                    "Esa cancha ya está reservada en ese horario."
                )
    else:
        form = ReservaForm()

    return render(request, 'reservas/crear_reserva.html', {'form': form})


@login_required
def mis_reservas(request):
    reservas = request.user.reservas.all().order_by('-fecha')
    return render(
        request,
        'reservas/mis_reservas.html',
        {'reservas': reservas}
    )
