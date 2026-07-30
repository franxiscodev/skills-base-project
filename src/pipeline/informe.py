"""Emite el informe en Markdown y un resumen por consola.

El informe publica **los recuentos de descarte junto a las cifras**. No es
decoración: un total de facturación sin decir cuántas filas se quedaron fuera es
un número que no se puede auditar. Quien lo lea tiene que poder ver las dos cosas
a la vez.
"""

from __future__ import annotations

from pathlib import Path

from .metricas import Resumen
from .recuento import Recuento

Fila = tuple[str, int, float]


def _euros(valor: float) -> str:
    """Formato español: miles con punto y decimales con coma."""
    entero, _, decimal = f"{valor:,.2f}".partition(".")
    return f"{entero.replace(',', '.')},{decimal} €"


def _tabla(cabeceras: tuple[str, str, str], filas: list[Fila]) -> list[str]:
    lineas = [
        f"| {cabeceras[0]} | {cabeceras[1]} | {cabeceras[2]} |",
        "|---|---:|---:|",
    ]
    lineas += [f"| {c} | {n} | {_euros(i)} |" for c, n, i in filas]
    return lineas


def construir(
    res: Resumen,
    ciudades: list[Fila],
    productos: list[Fila],
    meses: list[Fila],
    recuentos: list[Recuento],
) -> str:
    """Devuelve el informe completo en Markdown."""
    lineas: list[str] = [
        "# Informe de ventas",
        "",
        "> Generado por el pipeline. Los datos de origen se fabrican con una semilla",
        "> fija, así que este informe es reproducible: dos ejecuciones dan lo mismo.",
        "",
        "## Resumen",
        "",
        f"- Ventas: **{res.ventas}**",
        f"- Devoluciones: **{res.devoluciones}**",
        f"- Importe bruto: **{_euros(res.importe_bruto)}**",
        f"- Importe devuelto: **{_euros(res.importe_devuelto)}**",
        f"- **Importe neto: {_euros(res.importe_neto)}**",
        "",
        "## Trazabilidad del procesado",
        "",
        "Qué hizo cada paso con las filas que recibió:",
        "",
        "| Paso | Entrantes | Salientes | Descartadas | Motivo |",
        "|---|---:|---:|---:|---|",
    ]
    lineas += [
        f"| `{r.paso}` | {r.entrantes} | {r.salientes} | {r.descartadas} | {r.motivo} |"
        for r in recuentos
    ]

    for titulo, cabecera, filas in (
        ("Por ciudad", "Ciudad", ciudades),
        ("Por producto", "Producto", productos),
        ("Por mes", "Mes", meses),
    ):
        lineas += ["", f"## {titulo}", ""]
        lineas += _tabla((cabecera, "Operaciones", "Importe neto"), filas)

    lineas.append("")
    return "\n".join(lineas)


def escribir(contenido: str, destino: Path) -> Path:
    destino.parent.mkdir(parents=True, exist_ok=True)
    destino.write_text(contenido, encoding="utf-8")
    return destino


def resumir_en_consola(res: Resumen, recuentos: list[Recuento], destino: Path) -> None:
    print("\nProcesado")
    for recuento in recuentos:
        print(f"  {recuento}")

    print("\nResultado")
    print(f"  Ventas ........... {res.ventas}")
    print(f"  Devoluciones ..... {res.devoluciones}")
    print(f"  Importe neto ..... {_euros(res.importe_neto)}")
    print(f"\nInforme escrito en {destino}\n")
