def calculate_variation(fecha_inicio, fecha_fin, data):
    fecha_inicio = fecha_inicio.split("-")
    fecha_fin = fecha_fin.split("-")
    ipc_inicio = None
    ipc_fin = None

    for periodo in data:

        periodSplit = periodo.split("-")

        if periodSplit[0] == fecha_inicio[0] and periodSplit[1] == fecha_inicio[1]:
            ipc_inicio = float(data[periodo])

        if periodSplit[0] == fecha_fin[0] and periodSplit[1] == fecha_fin[1]:
            ipc_fin = float(data[periodo])

    if ipc_inicio is not None and ipc_fin is not None:
        return round(((ipc_fin / ipc_inicio) - 1) * 100, 1)
    
    return None

def calculate_adjusted_amount(initial_amount, readjustment):
    return initial_amount * (1 + (readjustment/100))



