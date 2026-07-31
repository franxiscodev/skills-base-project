"""Carga el CSV crudo en DuckDB, sin interpretar nada.

**Todas las columnas entran como texto** (`all_varchar=True`), y es la decisión de
diseño más importante del pipeline.

DuckDB sabe adivinar tipos, y si le dejamos hacerlo se come el problema en
silencio: decide por su cuenta qué formato de fecha usar, qué hacer con
`"1.234,56"` y qué es un nulo. Cuando algo salga mal, el error aparecerá tres
pasos más abajo y sin rastro de dónde vino.

Al cargar todo como texto, **cada conversión pasa a ser una decisión explícita** de
`limpiar.py`, escrita, con su regla y su test. Se puede leer y se puede discutir.
"""

from __future__ import annotations

from pathlib import Path

import duckdb

from .recuento import Recuento

TABLA_CRUDA = "ventas_crudo"


def cargar(con: duckdb.DuckDBPyConnection, csv: Path) -> Recuento:
    """Crea la tabla cruda a partir del CSV y devuelve cuántas filas trajo."""
    if not csv.exists():
        raise FileNotFoundError(
            f"No existe {csv}. Ejecuta el paso de generación antes de cargar."
        )

    relacion = con.read_csv(str(csv), header=True, all_varchar=True)
    relacion.create(TABLA_CRUDA)

    filas = con.sql(f"SELECT count(*) FROM {TABLA_CRUDA}").fetchone()[0]

    return Recuento(
        paso="cargar",
        entrantes=filas,
        salientes=filas,
        motivo="la carga no descarta nada: solo lee",
    )
