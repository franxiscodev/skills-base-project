"""Las decisiones repetitivas. El corazón del proyecto.

Cada función de este módulo resuelve **un** defecto de los datos de origen, y cada
una responde a una pregunta que se contesta siempre igual. Por eso están separadas:
una regla, una función, un test, un recuento.

El orden importa y no es arbitrario:

1. `deduplicar`   — antes de nada, para no arrastrar trabajo inútil.
2. `normalizar_texto` — antes de agrupar: "  MADRID " y "Madrid" son la misma ciudad,
   y si se agrupa antes de normalizar salen dos filas donde hay una.
3. `convertir_tipos`  — descarta lo que no se puede convertir.
4. `descartar_importe_cero` — después de convertir, que es cuando el importe ya es
   un número y se puede comparar con cero.
5. `imputar_ciudad`   — después de descartar, sobre las filas que sobreviven.
6. `marcar_devoluciones` — clasifica, no elimina.

Descartan filas `deduplicar`, `convertir_tipos` y `descartar_importe_cero`; las otras
tres reescriben o clasifican.

Los nombres de tabla se interpolan en el SQL porque son constantes de este módulo,
nunca entrada externa. Los **valores** siempre van como parámetros.
"""

from __future__ import annotations

import duckdb

from .recuento import Recuento

# Los tres formatos de fecha que conviven en el origen.
FORMATOS_FECHA = ["%d/%m/%Y", "%Y-%m-%d", "%d-%m-%Y"]

CIUDAD_DESCONOCIDA = "Desconocida"

TABLA_LIMPIA = "ventas_limpias"


def _contar(con: duckdb.DuckDBPyConnection, tabla: str) -> int:
    return con.sql(f"SELECT count(*) FROM {tabla}").fetchone()[0]


def _capitalizar(columna: str) -> str:
    """SQL que deja `  MADRID ` como `Madrid`.

    DuckDB **no tiene `initcap`** (sí lo tienen PostgreSQL y otros), así que hay
    que componerlo: primera letra en mayúscula y el resto en minúscula, sobre el
    texto ya recortado. Es exactamente el tipo de detalle que no aparece en la
    documentación que uno recuerda y que solo se descubre ejecutándolo.
    """
    recortado = f"trim({columna})"
    return f"upper(substr({recortado}, 1, 1)) || lower(substr({recortado}, 2))"


def deduplicar(con: duckdb.DuckDBPyConnection, origen: str, destino: str) -> Recuento:
    """Elimina filas idénticas en todas sus columnas.

    Se deduplica por la fila completa y no por `id_venta` a propósito: dos filas
    con el mismo id pero distinto importe **no** son un duplicado, son un conflicto
    de datos, y esconderlo aquí sería tomar una decisión que no nos corresponde.
    """
    antes = _contar(con, origen)
    con.execute(f"CREATE OR REPLACE TABLE {destino} AS SELECT DISTINCT * FROM {origen}")
    despues = _contar(con, destino)

    return Recuento(
        paso="deduplicar",
        entrantes=antes,
        salientes=despues,
        motivo="filas idénticas en todas sus columnas",
    )


def normalizar_texto(
    con: duckdb.DuckDBPyConnection, origen: str, destino: str
) -> Recuento:
    """Quita espacios sobrantes y unifica mayúsculas en los campos de texto.

    Va antes de cualquier agregación: si se agrupa por una ciudad sin normalizar,
    `"  MADRID "` y `"Madrid"` cuentan como dos grupos distintos y el informe sale
    mal sin que salte ningún error. Es el fallo más silencioso de los seis.
    """
    antes = _contar(con, origen)
    con.execute(
        f"""
        CREATE OR REPLACE TABLE {destino} AS
        SELECT
            id_venta,
            fecha,
            nullif({_capitalizar('ciudad')}, '')   AS ciudad,
            nullif({_capitalizar('producto')}, '') AS producto,
            cantidad,
            importe
        FROM {origen}
        """
    )
    despues = _contar(con, destino)

    return Recuento(
        paso="normalizar_texto",
        entrantes=antes,
        salientes=despues,
        motivo="normalizar no descarta: solo reescribe",
    )


def convertir_tipos(
    con: duckdb.DuckDBPyConnection, origen: str, destino: str
) -> Recuento:
    """Convierte texto a fecha, entero y decimal, y descarta lo que no encaja.

    Tres decisiones explícitas:

    - **Fecha:** se prueban los tres formatos conocidos con `try_strptime`. Lo que
      no encaje en ninguno queda a NULL, no revienta.
    - **Importe:** la coma decimal se sustituye por punto antes de convertir. Ojo
      con el orden — hacerlo al revés convierte "1,50" en 150.
    - **Cantidad:** entero directo.

    Una fila sin fecha, sin importe o sin cantidad no es recuperable: no se puede
    agregar por un mes que no existe. Se descarta y queda contada.
    """
    antes = _contar(con, origen)
    con.execute(
        f"""
        CREATE OR REPLACE TABLE {destino} AS
        SELECT * FROM (
            SELECT
                try_cast(id_venta AS INTEGER)                    AS id_venta,
                try_strptime(fecha, $formatos)::DATE             AS fecha,
                ciudad,
                producto,
                try_cast(cantidad AS INTEGER)                    AS cantidad,
                try_cast(replace(importe, ',', '.') AS DOUBLE)   AS importe
            FROM {origen}
        )
        WHERE fecha IS NOT NULL
          AND importe IS NOT NULL
          AND cantidad IS NOT NULL
        """,
        {"formatos": FORMATOS_FECHA},
    )
    despues = _contar(con, destino)

    return Recuento(
        paso="convertir_tipos",
        entrantes=antes,
        salientes=despues,
        motivo="fecha, importe o cantidad ilegibles",
    )


def descartar_importe_cero(
    con: duckdb.DuckDBPyConnection, origen: str, destino: str
) -> Recuento:
    """Elimina las ventas cuyo importe es exactamente cero.

    Un importe de 0 no es una venta: es un apunte técnico del sistema de origen
    —un ajuste, una línea anulada, un envío sin cargo—. Suma 0 al total, así que
    dejarla no cambia la facturación, pero sí infla el número de ventas y el
    recuento por ciudad y por producto. Se descarta y queda contada.

    El criterio es **igualdad estricta con cero**, no `<= 0`, y esa diferencia
    importa: una devolución se codifica con cantidad negativa e importe positivo,
    pero un importe negativo real seguiría siendo dinero que se movió, y esta
    regla no es quién para hacerlo desaparecer.

    Va después de `convertir_tipos` porque hasta ahí el importe es texto: `"0,00"`
    y `"0.00"` son cadenas distintas y ninguna se puede comparar con cero.
    """
    antes = _contar(con, origen)
    con.execute(
        f"CREATE OR REPLACE TABLE {destino} AS SELECT * FROM {origen} WHERE importe <> 0"
    )
    despues = _contar(con, destino)

    return Recuento(
        paso="descartar_importe_cero",
        entrantes=antes,
        salientes=despues,
        motivo="importe exactamente cero",
    )


def imputar_ciudad(
    con: duckdb.DuckDBPyConnection, origen: str, destino: str
) -> Recuento:
    """Sustituye la ciudad ausente por un valor explícito, en vez de descartar.

    El criterio: **una venta sin ciudad sigue siendo una venta.** El importe es
    real y debe entrar en el total. Descartarla falsearía la facturación para
    ahorrarse una fila en el desglose geográfico.

    Y se marca como `"Desconocida"` en lugar de dejarla a NULL para que aparezca en
    el informe. Un NULL desaparece de los agrupados; un valor con nombre obliga a
    mirarlo.
    """
    antes = _contar(con, origen)
    con.execute(
        f"""
        CREATE OR REPLACE TABLE {destino} AS
        SELECT * REPLACE (coalesce(ciudad, $desconocida) AS ciudad)
        FROM {origen}
        """,
        {"desconocida": CIUDAD_DESCONOCIDA},
    )
    despues = _contar(con, destino)

    return Recuento(
        paso="imputar_ciudad",
        entrantes=antes,
        salientes=despues,
        motivo=f"ciudad ausente → '{CIUDAD_DESCONOCIDA}', sin descartar",
    )


def marcar_devoluciones(
    con: duckdb.DuckDBPyConnection, origen: str, destino: str
) -> Recuento:
    """Clasifica las cantidades negativas como devoluciones. No las elimina.

    El sistema de origen codifica una devolución como cantidad negativa. Borrarlas
    inflaría las ventas; sumarlas sin distinguir mezclaría dos hechos de negocio
    distintos. Se marcan con una columna y que decida quien lea el informe.
    """
    antes = _contar(con, origen)
    con.execute(
        f"""
        CREATE OR REPLACE TABLE {destino} AS
        SELECT *, cantidad < 0 AS es_devolucion
        FROM {origen}
        """
    )
    despues = _contar(con, destino)

    return Recuento(
        paso="marcar_devoluciones",
        entrantes=antes,
        salientes=despues,
        motivo="cantidad negativa → marcada, no eliminada",
    )


def limpiar(con: duckdb.DuckDBPyConnection, origen: str) -> tuple[str, list[Recuento]]:
    """Encadena las seis reglas y devuelve la tabla final con sus recuentos."""
    pasos = [
        (deduplicar, "_paso1_dedup"),
        (normalizar_texto, "_paso2_texto"),
        (convertir_tipos, "_paso3_tipos"),
        (descartar_importe_cero, "_paso4_cero"),
        (imputar_ciudad, "_paso5_ciudad"),
        (marcar_devoluciones, TABLA_LIMPIA),
    ]

    recuentos: list[Recuento] = []
    entrada = origen
    for funcion, salida in pasos:
        recuentos.append(funcion(con, entrada, salida))
        entrada = salida

    return TABLA_LIMPIA, recuentos
