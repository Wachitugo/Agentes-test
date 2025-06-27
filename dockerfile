# Imagen base de Python 3.11
FROM python:3.11-slim

# Variables de entorno
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    POETRY_VERSION=1.7.1 \
    POETRY_HOME="/opt/poetry" \
    POETRY_VIRTUALENVS_IN_PROJECT=false \
    POETRY_NO_INTERACTION=1

# Agregar Poetry al PATH
ENV PATH="$POETRY_HOME/bin:$PATH"

# Instalar dependencias del sistema y Poetry
RUN apt-get update \
    && apt-get install -y --no-install-recommends curl \
    && curl -sSL https://install.python-poetry.org | python3 - \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Establecer directorio de trabajo
WORKDIR /app

# Copiar archivos de configuración de Poetry
COPY pyproject.toml poetry.lock ./

# Instalar dependencias
RUN poetry install --no-root --no-interaction

# Copiar código fuente
COPY app/ ./app/
COPY main.py .

# Copiar archivos de datos necesarios
COPY data/.gitkeep ./data/

# Puerto (si es necesario)
# EXPOSE 8000

# Comando para ejecutar la aplicación
ENTRYPOINT ["poetry", "run"]
CMD ["python", "main.py"]