from celery import Celery
import time
import os # <-- Importa la librería os

# Lee la URL de Redis desde la variable de entorno.
# Si no la encuentra, usa localhost (para seguir funcionando sin Docker).
REDIS_URL = os.getenv('REDIS_URL', 'redis://localhost:6379/0')
# Configuración de Celery
app = Celery('tasks', broker=REDIS_URL)

# Nueva tarea para procesar las facturas
@app.task
def procesar_lote_facturas(lote_facturas: list):
    """
    Esta tarea recibe una lista de facturas (como diccionarios)
    y ejecuta la lógica de negocio.
    """
    total_facturas = len(lote_facturas)
    print(f"\nWORKER: Recibido un lote de {total_facturas} facturas. Empezando a procesar...")

    for i, factura in enumerate(lote_facturas):
        print(f"  > Procesando factura {i+1}/{total_facturas}: N° {factura['numero_factura']} por un monto de {factura['monto']}...")
        
        # --- AQUÍ VA TU LÓGICA DE NEGOCIO REAL ---
        # 1. Conectarse a la base de datos.
        # 2. Verificar si el cliente con `factura['rut_cliente']` existe. Si no, crearlo.
        # 3. Insertar la factura usando lógica UPSERT para evitar duplicados.
        # 4. Actualizar saldos, etc.
        # -------------------------------------------
        
        time.sleep(1) # Simula el trabajo en la base de datos

    print(f"WORKER: Lote de {total_facturas} facturas procesado exitosamente.\n")
    return f"Se procesaron {total_facturas} facturas."
