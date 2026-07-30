# Imagen para ejecutar el pipeline sin instalar nada en la máquina anfitriona.
#
# La versión base va fijada a propósito (no `python:slim` a secas): una etiqueta
# móvil convierte una build reproducible en una lotería, y el día que cambie no
# habrá forma de saber por qué el pipeline dejó de funcionar.
FROM python:3.12-slim

# uv se copia desde su imagen oficial, también con versión fijada.
COPY --from=ghcr.io/astral-sh/uv:0.7.9 /uv /usr/local/bin/uv

WORKDIR /app

# Primero las dependencias, después el código: si solo cambia el código, Docker
# reutiliza la capa de dependencias y la build tarda segundos en vez de minutos.
COPY pyproject.toml uv.lock ./
COPY src ./src

# --frozen: usa uv.lock tal cual y falla si no coincide, en vez de resolver por su
# cuenta. --no-dev: pytest no pinta nada en la imagen de ejecución.
RUN uv sync --frozen --no-dev

ENTRYPOINT ["uv", "run", "--no-dev", "python", "-m", "pipeline"]
