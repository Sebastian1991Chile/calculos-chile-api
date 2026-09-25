import logging

from fastapi import FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from pydantic import BaseModel, field_validator, model_validator
from datetime import date

from config import settings
from data_manager import get_bcch_indicators, load_data
from calculations import (
    calculate_adjusted_amount,
    calculate_latest_ipc_indicators,
    calculate_variation
)

logger = logging.getLogger(__name__)

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins,
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.exception_handler(Exception)
async def unhandled_exception_handler(request: Request, exc: Exception):
    logger.exception("Error no controlado en %s", request.url.path)
    return JSONResponse(
        status_code=500,
        content={"detail": "Error interno del servidor"}
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
def get_indicators():
    try:
        bcch_indicators = get_bcch_indicators()
        ipc_indicators = calculate_latest_ipc_indicators(load_data())
    except RuntimeError as error:
        raise HTTPException(status_code=502, detail=str(error)) from error
    except ValueError as error:
        raise HTTPException(status_code=503, detail=str(error)) from error

    return {**bcch_indicators, **ipc_indicators}

@app.post("/ipc")
def calculate_ipc(request: IPCRequest):
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
def calculate_arriendo(request: AmountRequest):
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
def calculate_sueldo(request: AmountRequest):
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
def calculate_inflacion(request: AmountRequest):
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