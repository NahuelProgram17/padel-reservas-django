from datetime import time

def generar_horarios():
    horarios = []
    for hora in range(10, 22):
        horarios.append(time(hora, 0))
    return horarios
