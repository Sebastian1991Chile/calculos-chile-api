import json
import os
from datetime import date, timedelta

import bcchapi


UF_SERIES = "F073.UFF.PRE.Z.D"
UTM_SERIES = "F073.UTR.PRE.Z.M"

def load_data():
    with open("data/ipc.json", "r", encoding="utf-8") as f:
        return json.load(f)


def get_bcch_indicators():
    token = os.getenv("BCCH_TOKEN")
    if not token:
        raise RuntimeError("BCCH_TOKEN no está configurado")

    end_date = date.today()
    start_date = end_date - timedelta(days=120)

    try:
        data = bcchapi.Siete(token=token).cuadro(
            series=[UF_SERIES, UTM_SERIES],
            desde=start_date.isoformat(),
            hasta=end_date.isoformat()
        )
    except Exception as error:
        raise RuntimeError("No fue posible consultar el Banco Central de Chile") from error

    uf = _get_latest_series_value(data, 0, "UF")
    utm = _get_latest_series_value(data, 1, "UTM")

    return {
        "uf": {
            "valor": round(float(uf[1]), 2),
            "fecha": uf[0].strftime("%Y-%m-%d"),
            "fuente": "Banco Central de Chile"
        },
        "utm": {
            "valor": _normalize_number(utm[1]),
            "periodo": utm[0].strftime("%Y-%m"),
            "fuente": "Banco Central de Chile"
        }
    }


def _get_latest_series_value(data, column_index, indicator_name):
    values = data.iloc[:, column_index].dropna()
    if values.empty:
        raise RuntimeError(
            f"No existe información disponible para {indicator_name}"
        )

    return values.index[-1], values.iloc[-1]


def _normalize_number(value):
    number = float(value)
    return int(number) if number.is_integer() else number