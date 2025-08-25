# Usa una imagen oficial de Python como base.
FROM python:3.10-slim

# Establece el directorio de trabajo dentro del contenedor.
WORKDIR /app

# Copia el archivo de dependencias primero.
# Esto aprovecha el caché de Docker y acelera las construcciones futuras.
COPY requirements.txt .

# Instala las dependencias.
RUN pip install --no-cache-dir -r requirements.txt

# Copia el resto del código de tu aplicación al contenedor.
COPY . .

# El comando para ejecutar la aplicación se especificará en docker-compose.yml.