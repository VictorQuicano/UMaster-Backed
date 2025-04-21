FROM python:3.10-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=off \
    PIP_DISABLE_PIP_VERSION_CHECK=on \
    PIP_DEFAULT_TIMEOUT=100

WORKDIR /app

RUN apt-get update \
    && apt-get install -y --no-install-recommends \
        postgresql-client \
        libpq-dev \
        gcc \
        gettext \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Actualiza pip e instala dependencias de Python
COPY requirements.txt .
RUN pip install --upgrade pip \
    && pip install -r requirements.txt

# No copiamos el código porque usaremos volúmenes para desarrollo

# Exponer el puerto en el que se ejecutará la aplicación
EXPOSE 8001

# Comando para ejecutar la aplicación en modo desarrollo
CMD ["python", "manage.py", "runserver", "0.0.0.0:8001"]