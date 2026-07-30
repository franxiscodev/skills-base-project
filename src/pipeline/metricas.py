"""Agregaciones sobre la tabla ya limpia.

Una decisión de negocio que conviene dejar escrita, porque cambia el resultado y
no es evidente: **una devolución resta.**

El sistema de origen guarda la devolución con cantidad negativa pero importe
positivo. Si se suman todos los importes sin mirar el signo de la cantidad, las
devoluciones acaban sumando facturación, que es justo lo contrario de lo que
pasó. Aquí el importe se aplica con el signo de la cantidad.
"""

from __future__ import annotations

from dataclasses import dataclass

import duckdb

# Importe con signo: negativo si la venta es en realidad una devolución.
IMPORTE_CON_SIGNO = "CASE WHEN es_devolucion THEN -importe ELSE importe END"


@dataclass(frozen=True)
class Resumen:
    """Las cuatro cifras de cabecera del informe."""

    ventas: int
    devoluciones: int
    importe_bruto: float
    importe_devuelto: float

    @property
    def importe_neto(self) -> float:
        return self.importe_bruto - self.importe_devuelto


def resumen(con: duckdb.DuckDBPyConnection, tabla: str) -> Resumen:
    fila = con.sql(
        f"""
        SELECT
            count(*) FILTER (WHERE NOT es_devolucion)          AS ventas,
            count(*) FILTER (WHERE es_devolucion)              AS devoluciones,
            coalesce(sum(importe) FILTER (WHERE NOT es_devolucion), 0) AS bruto,
            coalesce(sum(importe) FILTER (WHERE es_devolucion), 0)     AS devuelto
        FROM {tabla}
        """
    ).fetchone()

    return Resumen(
        ventas=fila[0],
        devoluciones=fila[1],
        importe_bruto=round(fila[2], 2),
        importe_devuelto=round(fila[3], 2),
    )


def _agrupar(
    con: duckdb.DuckDBPyConnection, tabla: str, expresion: str, alias: str
) -> list[tuple[str, int, float]]:
    """Agrupa por una expresión y devuelve (clave, nº operaciones, importe neto)."""
    return con.sql(
        f"""
        SELECT
            {expresion}                        AS {alias},
            count(*)                           AS operaciones,
            round(sum({IMPORTE_CON_SIGNO}), 2) AS importe_neto
        FROM {tabla}
        GROUP BY 1
        ORDER BY importe_neto DESC
        """
    ).fetchall()


def por_ciudad(con: duckdb.DuckDBPyConnection, tabla: str):
    return _agrupar(con, tabla, "ciudad", "ciudad")


def por_producto(con: duckdb.DuckDBPyConnection, tabla: str):
    return _agrupar(con, tabla, "producto", "producto")


def por_mes(con: duckdb.DuckDBPyConnection, tabla: str):
    """Agrupa por mes en formato `aaaa-mm`, que ordena bien como texto."""
    return sorted(_agrupar(con, tabla, "strftime(fecha, '%Y-%m')", "mes"))
