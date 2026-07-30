"""Tests de las agregaciones.

El más importante es el primero: **una devolución resta**. Es la decisión que más
fácil se pierde en un refactor, porque el código sigue funcionando y solo cambia
el número.
"""

from __future__ import annotations

from pipeline import limpiar, metricas


def _preparar(con, tabla_cruda, filas):
    """Deja las filas listas en la tabla limpia y devuelve su nombre."""
    origen = tabla_cruda(filas)
    tabla, _ = limpiar.limpiar(con, origen)
    return tabla


def test_la_devolucion_resta_del_neto(con, tabla_cruda):
    tabla = _preparar(
        con,
        tabla_cruda,
        [
            ("1", "15/03/2026", "Madrid", "Teclado", "2", "100.00"),
            ("2", "16/03/2026", "Madrid", "Teclado", "-1", "40.00"),
        ],
    )

    res = metricas.resumen(con, tabla)

    assert res.ventas == 1
    assert res.devoluciones == 1
    assert res.importe_bruto == 100.00
    assert res.importe_devuelto == 40.00
    assert res.importe_neto == 60.00


def test_agrupar_por_ciudad_no_parte_los_grupos(con, tabla_cruda):
    """Sin normalizar el texto antes, esto daría tres ciudades en vez de una.

    Es el fallo silencioso del pipeline: no lanza ningún error, solo da mal el
    informe.
    """
    tabla = _preparar(
        con,
        tabla_cruda,
        [
            ("1", "15/03/2026", "Madrid", "Teclado", "1", "10.00"),
            ("2", "15/03/2026", "  MADRID ", "Teclado", "1", "10.00"),
            ("3", "15/03/2026", "madrid", "Teclado", "1", "10.00"),
        ],
    )

    filas = metricas.por_ciudad(con, tabla)

    assert filas == [("Madrid", 3, 30.00)]


def test_la_ciudad_ausente_aparece_en_el_desglose(con, tabla_cruda):
    """Se imputa con nombre, no con NULL, precisamente para que se vea."""
    tabla = _preparar(
        con,
        tabla_cruda,
        [
            ("1", "15/03/2026", "Madrid", "Teclado", "1", "10.00"),
            ("2", "15/03/2026", None, "Teclado", "1", "10.00"),
        ],
    )

    ciudades = [fila[0] for fila in metricas.por_ciudad(con, tabla)]

    assert limpiar.CIUDAD_DESCONOCIDA in ciudades


def test_por_mes_ordena_cronologicamente(con, tabla_cruda):
    tabla = _preparar(
        con,
        tabla_cruda,
        [
            ("1", "15/03/2026", "Madrid", "Teclado", "1", "30.00"),
            ("2", "10/01/2026", "Madrid", "Teclado", "1", "10.00"),
            ("3", "05/02/2026", "Madrid", "Teclado", "1", "20.00"),
        ],
    )

    meses = [fila[0] for fila in metricas.por_mes(con, tabla)]

    assert meses == ["2026-01", "2026-02", "2026-03"]
