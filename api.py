from fastapi import FastAPI, Header, HTTPException, Depends
from pydantic import BaseModel, field_validator, model_validator
from datetime import date
import os
from dotenv import load_dotenv

from data_manager import get_bcch_indicators, load_data
from calculations import (
    calculate_adjusted_amount,
    calculate_latest_ipc_indicators,
    calculate_variation
)

app = FastAPI()

load_dotenv(override=True)
API_KEY = os.getenv("API_KEY")

if not API_KEY:
    raise RuntimeError("API_KEY no está configurada")

def verify_api_key(x_api_key: str = Header()):
    if x_api_key != API_KEY:
        raise HTTPException(
            status_code=401,
            detail="API Key inválida"
        )

class DateRequest(BaseModel):
    fecha_inicio: str
    fecha_fin: str

    @field_validator("fecha_inicio", "fecha_fin")
    @classmethod
    def validar_fecha(cls, value):
        try:
            date.fromisoformat(value)
        except ValueError:
            raise ValueError("La fecha debe tener formato YYYY-MM-DD")

        return value

    @model_validator(mode="after")
    def validar_rango(self):
        if self.fecha_inicio > self.fecha_fin:
            raise ValueError(
                "La fecha de inicio no puede ser posterior a la fecha de fin"
            )

        return self

class IPCRequest(DateRequest):
    pass

class AmountRequest(DateRequest):
    monto: float

def validate_periods(request):
    data = load_data()

    if request.fecha_inicio not in data:
        raise HTTPException(
            status_code=400,
            detail="La fecha de inicio no está disponible"
        )

    if request.fecha_fin not in data:
        raise HTTPException(
            status_code=400,
            detail="La fecha de fin no está disponible"
        )

    return data


@app.get("/indicadores")
def get_indicators(_: str = Depends(verify_api_key)):
    try:
        bcch_indicators = get_bcch_indicators()
        ipc_indicators = calculate_latest_ipc_indicators(load_data())
    except RuntimeError as error:
        raise HTTPException(status_code=502, detail=str(error)) from error
    except ValueError as error:
        raise HTTPException(status_code=503, detail=str(error)) from error

    return {**bcch_indicators, **ipc_indicators}

@app.post("/ipc")
def calculate_ipc(
    request: IPCRequest,
    _: str = Depends(verify_api_key)
):
    data = validate_periods(request)

    variation = calculate_variation(
        request.fecha_inicio,
        request.fecha_fin,
        data
    )

    return {
        "variacion": variation
    }

@app.post("/arriendo")
def calculate_arriendo(
    request: AmountRequest,
    _: str = Depends(verify_api_key)
):
    data = validate_periods(request)
    
    variation = calculate_variation(
        request.fecha_inicio,
        request.fecha_fin,
        data
    )

    amount = calculate_adjusted_amount(
        request.monto,
        variation
    )

    return {
        "variacion": variation,
        "monto_original": request.monto,
        "monto_reajustado": amount
    }

@app.post("/sueldo")
def calculate_sueldo(
    request: AmountRequest,
    _: str = Depends(verify_api_key)
):
    data = validate_periods(request)

    variation = calculate_variation(
        request.fecha_inicio,
        request.fecha_fin,
        data
    )

    amount = calculate_adjusted_amount(
        request.monto,
        variation
    )

    return {
        "variacion": variation,
        "monto_original": request.monto,
        "monto_reajustado": amount
    }

@app.post("/inflacion")
def calculate_inflacion(
    request: AmountRequest,
    _: str = Depends(verify_api_key)
):
    data = validate_periods(request)

    variation = calculate_variation(
        request.fecha_inicio,
        request.fecha_fin,
        data
    )

    amount = calculate_adjusted_amount(
        request.monto,
        variation
    )

    return {
        "inflacion": variation,
        "monto_inicial": request.monto,
        "monto_actual": amount
    }