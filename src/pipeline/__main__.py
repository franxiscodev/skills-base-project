"""Orquesta el pipeline completo.

    generar → cargar → limpiar → métricas → informe

Se ejecuta con `python -m pipeline`. Todo en memoria: DuckDB trabaja sin fichero
de base de datos porque no hay nada que conservar entre ejecuciones — el CSV es la
fuente y el informe es el resultado.
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

import duckdb

from . import cargar as paso_cargar
from . import generar_datos, informe, limpiar, metricas

RAIZ = Path(__file__).resolve().parents[2]
CSV_CRUDO = RAIZ / "datos" / "crudo" / "ventas.csv"
INFORME = RAIZ / "datos" / "salida" / "informe.md"


def _consola_en_utf8() -> None:
    """Fuerza UTF-8 en la salida estándar.

    La consola de Windows usa `cp1252` por defecto, que **no puede representar
    `→` ni `€`**. Sin esto, el pipeline calcula bien y revienta al imprimir, con
    un `UnicodeEncodeError` que apunta a `print` y no al problema real, que es la
    codificación del terminal.

    El fichero del informe no sufre esto porque se escribe con `encoding="utf-8"`
    explícito. Es la misma diferencia de siempre: lo que se guarda está bajo tu
    control; lo que se muestra depende del entorno de quien lo ejecuta.
    """
    for flujo in (sys.stdout, sys.stderr):
        try:
            flujo.reconfigure(encoding="utf-8", errors="replace")
        except (AttributeError, OSError):
            # Salida redirigida o no reconfigurable: se sigue igual.
            pass


def construir_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="pipeline",
        description="Lee un CSV de ventas sucio, lo limpia con DuckDB y emite un informe.",
    )
    parser.add_argument(
        "--filas",
        type=int,
        default=500,
        help="número de filas del CSV generado (por defecto: 500)",
    )
    parser.add_argument(
        "--solo-generar",
        action="store_true",
        help="genera el CSV de entrada y termina, sin procesarlo",
    )
    parser.add_argument(
        "--csv",
        type=Path,
        default=CSV_CRUDO,
        help=f"ruta del CSV de entrada (por defecto: {CSV_CRUDO})",
    )
    parser.add_argument(
        "--informe",
        type=Path,
        default=INFORME,
        help=f"ruta del informe de salida (por defecto: {INFORME})",
    )
    return parser


def main(argv: list[str] | None = None) -> int:
    _consola_en_utf8()
    args = construir_parser().parse_args(argv)

    csv = generar_datos.generar(args.csv, filas=args.filas)
    print(f"CSV generado en {csv} ({args.filas} filas + duplicados)")

    if args.solo_generar:
        return 0

    # Sin fichero de base de datos: no hay estado que conservar entre ejecuciones.
    con = duckdb.connect()

    recuentos = [paso_cargar.cargar(con, csv)]
    tabla, recuentos_limpieza = limpiar.limpiar(con, paso_cargar.TABLA_CRUDA)
    recuentos += recuentos_limpieza

    res = metricas.resumen(con, tabla)
    contenido = informe.construir(
        res,
        metricas.por_ciudad(con, tabla),
        metricas.por_producto(con, tabla),
        metricas.por_mes(con, tabla),
        recuentos,
    )
    destino = informe.escribir(contenido, args.informe)
    informe.resumir_en_consola(res, recuentos, destino)

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
