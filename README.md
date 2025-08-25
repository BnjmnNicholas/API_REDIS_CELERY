# API de Ingesta de Facturas con Redis y Celery

## 📋 Descripción

Este proyecto implementa una API REST robusta para la ingesta masiva de facturas utilizando FastAPI, Redis y Celery. La arquitectura está diseñada para manejar cargas de trabajo pesadas de manera asíncrona y escalable.

### 🏗️ Arquitectura

- **FastAPI**: API REST para recibir las facturas
- **Redis**: Broker de mensajes y cache para idempotencia
- **Celery**: Sistema de colas para procesamiento asíncrono
- **Docker**: Contenedorización de todos los servicios

## 🚀 Características

- ✅ **Idempotencia**: Evita procesamiento duplicado de transacciones
- ✅ **Procesamiento Asíncrono**: Las facturas se procesan en segundo plano
- ✅ **Validación de Datos**: Usando Pydantic para validar estructura de facturas
- ✅ **Escalabilidad**: Fácil escalado horizontal de workers
- ✅ **Containerización**: Todo funciona con Docker Compose

## 📁 Estructura del Proyecto

```
API_REDIS_CELERY/
├── api.py                 # Aplicación FastAPI principal
├── worker.py              # Configuración y tareas de Celery
├── call.ipynb             # Notebook para probar la API
├── requirements.txt       # Dependencias de Python
├── dockerfile             # Imagen base para los contenedores
├── docker-compose.yml     # Configuración de servicios
└── README.md              # Este archivo
```

## 🔧 Instalación y Configuración

### Prerrequisitos

- Docker
- Docker Compose
- Python 3.10+ (solo para desarrollo local)

### 🐳 Ejecución con Docker (Recomendado)

1. **Clonar el repositorio**
   ```bash
   git clone https://github.com/BnjmnNicholas/API_REDIS_CELERY.git
   cd API_REDIS_CELERY
   ```

2. **Levantar todos los servicios**
   ```bash
   docker-compose up --build
   ```

   Esto iniciará:
   - Redis en el puerto `6379`
   - API FastAPI en el puerto `8000`
   - Worker de Celery para procesamiento

3. **Verificar que todos los servicios estén ejecutándose**
   ```bash
   docker-compose ps
   ```

### 🖥️ Desarrollo Local (Sin Docker)

1. **Instalar dependencias**
   ```bash
   pip install -r requirements.txt
   ```

2. **Iniciar Redis** (requiere instalación local de Redis)
   ```bash
   redis-server
   ```

3. **Iniciar el Worker de Celery**
   ```bash
   celery -A worker.app worker --loglevel=INFO
   ```

4. **Iniciar la API**
   ```bash
   uvicorn api:app --reload --host 0.0.0.0 --port 8000
   ```

## 📚 Uso de la API

### Endpoint Principal

**POST** `/facturas/`

### Headers Requeridos

- `Content-Type: application/json`
- `Idempotency-Key: string` (clave única para evitar duplicados)

### Estructura de una Factura

```json
{
  "numero_factura": "F-001",
  "rut_cliente": "11111111-1",
  "monto": 1500.50,
  "fecha_emision": "2025-08-24"
}
```

### Ejemplo de Petición

```bash
curl -X POST "http://localhost:8000/facturas/" \
  -H "Content-Type: application/json" \
  -H "Idempotency-Key: mi-transaccion-unica-123" \
  -d '[
    {
      "numero_factura": "F-001",
      "rut_cliente": "11111111-1", 
      "monto": 1500.50,
      "fecha_emision": "2025-08-24"
    },
    {
      "numero_factura": "F-002",
      "rut_cliente": "22222222-2",
      "monto": 999.99,
      "fecha_emision": "2025-08-24"
    }
  ]'
```

### Respuesta Exitosa

```json
{
  "status": "OK",
  "detail": "2 facturas recibidas y encoladas para procesamiento."
}
```

## 🧪 Pruebas

### Usando el Notebook Jupyter

1. Ejecutar el notebook `call.ipynb` que contiene ejemplos de llamadas a la API

### Usando Python

```python
import requests
import json

url = "http://localhost:8000/facturas/"
headers = {
    "Content-Type": "application/json",
    "Idempotency-Key": "mi-transaccion-unica-456"
}

data = [
    {
        "numero_factura": "F-003",
        "rut_cliente": "33333333-3",
        "monto": 750.25,
        "fecha_emision": "2025-08-24"
    }
]

response = requests.post(url, headers=headers, data=json.dumps(data))
print(f"Status: {response.status_code}")
print(f"Response: {response.json()}")
```

## 🔍 Monitoreo

### Ver logs de los contenedores

```bash
# Logs de la API
docker-compose logs api

# Logs del Worker
docker-compose logs worker

# Logs de Redis
docker-compose logs redis

# Logs de todos los servicios
docker-compose logs -f
```

### Conectarse a Redis para debug

```bash
docker-compose exec redis redis-cli
```

## ⚙️ Configuración

### Variables de Entorno

- `REDIS_URL`: URL de conexión a Redis (default: `redis://localhost:6379/0`)

### Escalado de Workers

Para escalar el número de workers:

```bash
docker-compose up --scale worker=3
```

## 🛠️ Comandos Útiles

```bash
# Detener todos los servicios
docker-compose down

# Reconstruir las imágenes
docker-compose build

# Limpiar volúmenes y datos
docker-compose down -v

# Ver estado de contenedores
docker-compose ps

# Ejecutar comandos dentro de un contenedor
docker-compose exec api bash
docker-compose exec worker bash
```

## 📋 Estados de Respuesta HTTP

- `202 Accepted`: Facturas recibidas y encoladas correctamente
- `409 Conflict`: Transacción duplicada (misma `Idempotency-Key`)
- `422 Unprocessable Entity`: Error de validación en los datos
- `500 Internal Server Error`: Error interno del servidor

## 🔒 Idempotencia

El sistema utiliza Redis para almacenar las claves de idempotencia por 24 horas. Esto garantiza que:

- Las transacciones duplicadas sean rechazadas
- Se evite el procesamiento múltiple de las mismas facturas
- Se mantenga la integridad de los datos

## 🤝 Contribución

1. Fork del proyecto
2. Crear una rama para tu feature (`git checkout -b feature/nueva-funcionalidad`)
3. Commit de tus cambios (`git commit -am 'Agregar nueva funcionalidad'`)
4. Push a la rama (`git push origin feature/nueva-funcionalidad`)
5. Crear un Pull Request

## 📄 Licencia

Este proyecto está bajo la Licencia MIT. Ver el archivo `LICENSE` para más detalles.

## 📞 Soporte

Para reportar bugs o solicitar nuevas funcionalidades, por favor abre un issue en GitHub.

---

**¡La API está lista para procesar tus facturas de manera eficiente y escalable!** 🚀
