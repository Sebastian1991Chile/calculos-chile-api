from datetime import date


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


def calculate_latest_ipc_indicators(data):
    if not data:
        raise ValueError("No existen datos IPC disponibles")

    latest_period = max(data)
    latest_date = date.fromisoformat(latest_period)
    previous_month = _shift_month(latest_date, -1).isoformat()
    previous_year = _shift_month(latest_date, -12).isoformat()

    monthly_variation = calculate_variation(
        previous_month,
        latest_period,
        data
    )
    annual_variation = calculate_variation(
        previous_year,
        latest_period,
        data
    )

    if monthly_variation is None:
        raise ValueError(f"No existe información IPC para {previous_month[:7]}")
    if annual_variation is None:
        raise ValueError(f"No existe información IPC para {previous_year[:7]}")

    source = "Instituto Nacional de Estadísticas"
    period = latest_period[:7]

    return {
        "ipc": {
            "valor": monthly_variation,
            "periodo": period,
            "fuente": source
        },
        "inflacion_12m": {
            "valor": annual_variation,
            "periodo": period,
            "fuente": source
        }
    }


def _shift_month(period, months):
    month_index = period.year * 12 + period.month - 1 + months
    year, month = divmod(month_index, 12)
    return date(year, month + 1, 1)



