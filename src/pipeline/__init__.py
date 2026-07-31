"""Mini-pipeline de datos con DuckDB.

Un paso por módulo, en este orden:

    generar_datos  →  cargar  →  limpiar  →  metricas  →  informe

Cada paso devuelve, además de sus datos, un recuento de lo que dejó por el
camino. Un pipeline que no dice cuántas filas descartó y por qué no es un
pipeline, es una caja negra.
"""

from .recuento import Recuento

__all__ = ["Recuento"]
