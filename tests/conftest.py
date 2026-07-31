"""Utilidades compartidas por los tests.

Los tests **no usan el generador de datos**: construyen a mano la tabla cruda con
las filas justas que hacen falta. Un test que depende de datos aleatorios prueba
lo que salió ese día, no la regla.
"""

from __future__ import annotations

import duckdb
import pytest

# La tabla cruda es todo texto, igual que la deja `cargar.py`.
COLUMNAS = ["id_venta", "fecha", "ciudad", "producto", "cantidad", "importe"]


@pytest.fixture
def con():
    """Una conexión DuckDB en memoria, nueva para cada test."""
    conexion = duckdb.connect()
    yield conexion
    conexion.close()


@pytest.fixture
def tabla_cruda(con):
    """Crea una tabla cruda con las filas indicadas y devuelve su nombre."""

    def _crear(filas: list[tuple], nombre: str = "cruda") -> str:
        definicion = ", ".join(f"{columna} VARCHAR" for columna in COLUMNAS)
        con.execute(f"CREATE OR REPLACE TABLE {nombre} ({definicion})")
        marcas = ", ".join("?" for _ in COLUMNAS)
        con.executemany(f"INSERT INTO {nombre} VALUES ({marcas})", filas)
        return nombre

    return _crear
