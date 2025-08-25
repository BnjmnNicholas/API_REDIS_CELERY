import os
from fastapi import FastAPI, status, Header, HTTPException
from pydantic import BaseModel
from typing import List
from datetime import date
from redis import asyncio as aioredis # <--- ESTE ES EL CAMBIO

from worker import procesar_lote_facturas

# El resto del código funciona exactamente igual.
# --- Configuración de Redis ---
REDIS_URL = os.getenv('REDIS_URL', 'redis://localhost:6379/0')
redis_client = aioredis.from_url(REDIS_URL, decode_responses=True)


# --- Modelo de Datos para una Factura ---
class Factura(BaseModel):
    numero_factura: str
    rut_cliente: str
    monto: float
    fecha_emision: date

# --- Aplicación FastAPI ---
app = FastAPI(title="API de Ingesta de Facturas")

@app.post("/facturas/", status_code=status.HTTP_202_ACCEPTED)
async def recibir_facturas(
    facturas: List[Factura],
    idempotency_key: str = Header(..., description="Clave única para la transacción.")
):
    """
    Recibe un lote de facturas, valida la idempotencia y encola el procesamiento.
    """
    # 1. VERIFICAR IDEMPOTENCIA
    is_new = await redis_client.set(f"idempotency:{idempotency_key}", 1, ex=86400, nx=True)
    if not is_new:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Transacción duplicada: esta petición ya ha sido recibida."
        )

    # 2. ENCOLAR LA TAREA
    # Convertimos los objetos Pydantic a diccionarios para enviarlos a Celery.
    datos_para_celery = [f.model_dump(mode='json') for f in facturas]

    # delay por detras envia a redis
    procesar_lote_facturas.delay(datos_para_celery)

    return {"status": "OK", "detail": f"{len(facturas)} facturas recibidas y encoladas para procesamiento."}