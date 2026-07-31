"""Una regla de limpieza, un test.

Si mañana alguien cambia el criterio —por ejemplo, descartar las ventas sin ciudad
en vez de imputarlas— el test que falla dice exactamente qué decisión de negocio
se está cambiando. Eso es lo que los hace útiles aquí: no protegen el código,
protegen los criterios.
"""

from __future__ import annotations

from pipeline import limpiar

VENTA = ("1", "15/03/2026", "Madrid", "Teclado", "2", "59.80")


def test_deduplicar_elimina_filas_identicas(con, tabla_cruda):
    origen = tabla_cruda([VENTA, VENTA, ("2", *VENTA[1:])])

    recuento = limpiar.deduplicar(con, origen, "salida")

    assert recuento.entrantes == 3
    assert recuento.salientes == 2
    assert recuento.descartadas == 1


def test_deduplicar_respeta_mismo_id_con_datos_distintos(con, tabla_cruda):
    """Mismo id e importe distinto no es un duplicado: es un conflicto de datos.

    Resolverlo aquí sería tomar una decisión que no le corresponde al pipeline.
    """
    origen = tabla_cruda([VENTA, ("1", "15/03/2026", "Madrid", "Teclado", "2", "99.00")])

    recuento = limpiar.deduplicar(con, origen, "salida")

    assert recuento.salientes == 2


def test_normalizar_texto_unifica_espacios_y_mayusculas(con, tabla_cruda):
    origen = tabla_cruda(
        [
            ("1", "15/03/2026", "  MADRID ", "teclado", "1", "29.90"),
            ("2", "15/03/2026", "Madrid", "TECLADO", "1", "29.90"),
        ]
    )

    limpiar.normalizar_texto(con, origen, "salida")

    valores = con.sql("SELECT DISTINCT ciudad, producto FROM salida").fetchall()
    assert valores == [("Madrid", "Teclado")]


def test_normalizar_texto_deja_en_nulo_el_texto_vacio(con, tabla_cruda):
    origen = tabla_cruda([("1", "15/03/2026", "   ", "Teclado", "1", "29.90")])

    limpiar.normalizar_texto(con, origen, "salida")

    assert con.sql("SELECT ciudad FROM salida").fetchone()[0] is None


def test_convertir_tipos_acepta_los_tres_formatos_de_fecha(con, tabla_cruda):
    origen = tabla_cruda(
        [
            ("1", "15/03/2026", "Madrid", "Teclado", "1", "29.90"),
            ("2", "2026-03-15", "Madrid", "Teclado", "1", "29.90"),
            ("3", "15-03-2026", "Madrid", "Teclado", "1", "29.90"),
        ]
    )

    limpiar.convertir_tipos(con, origen, "salida")

    fechas = con.sql("SELECT DISTINCT fecha FROM salida").fetchall()
    assert len(fechas) == 1
    assert str(fechas[0][0]) == "2026-03-15"


def test_convertir_tipos_admite_coma_decimal(con, tabla_cruda):
    origen = tabla_cruda([("1", "15/03/2026", "Madrid", "Teclado", "1", "1234,56")])

    limpiar.convertir_tipos(con, origen, "salida")

    assert con.sql("SELECT importe FROM salida").fetchone()[0] == 1234.56


def test_convertir_tipos_descarta_lo_ilegible(con, tabla_cruda):
    origen = tabla_cruda(
        [
            VENTA,
            ("2", "no es una fecha", "Madrid", "Teclado", "1", "29.90"),
            ("3", "15/03/2026", "Madrid", "Teclado", "1", ""),
        ]
    )

    recuento = limpiar.convertir_tipos(con, origen, "salida")

    assert recuento.entrantes == 3
    assert recuento.salientes == 1
    assert recuento.descartadas == 2


def test_imputar_ciudad_no_descarta_la_venta(con, tabla_cruda):
    """Una venta sin ciudad sigue siendo una venta: su importe es real."""
    origen = tabla_cruda(
        [VENTA, ("2", "15/03/2026", None, "Teclado", "1", "29.90")]
    )
    limpiar.normalizar_texto(con, origen, "texto")
    limpiar.convertir_tipos(con, "texto", "tipos")

    recuento = limpiar.imputar_ciudad(con, "tipos", "salida")

    assert recuento.descartadas == 0
    ciudades = con.sql("SELECT ciudad FROM salida ORDER BY id_venta").fetchall()
    assert ciudades == [("Madrid",), (limpiar.CIUDAD_DESCONOCIDA,)]


def test_marcar_devoluciones_no_elimina_filas(con, tabla_cruda):
    origen = tabla_cruda([VENTA, ("2", "15/03/2026", "Madrid", "Teclado", "-1", "29.90")])
    limpiar.convertir_tipos(con, origen, "tipos")

    recuento = limpiar.marcar_devoluciones(con, "tipos", "salida")

    assert recuento.descartadas == 0
    marcas = con.sql("SELECT es_devolucion FROM salida ORDER BY id_venta").fetchall()
    assert marcas == [(False,), (True,)]


def test_limpiar_encadena_las_cinco_reglas(con, tabla_cruda):
    origen = tabla_cruda([VENTA, VENTA, ("2", "sin fecha", "  BILBAO ", "Ratón", "1", "15,50")])

    tabla, recuentos = limpiar.limpiar(con, origen)

    assert tabla == limpiar.TABLA_LIMPIA
    assert [r.paso for r in recuentos] == [
        "deduplicar",
        "normalizar_texto",
        "convertir_tipos",
        "imputar_ciudad",
        "marcar_devoluciones",
    ]
    assert con.sql(f"SELECT count(*) FROM {tabla}").fetchone()[0] == 1
