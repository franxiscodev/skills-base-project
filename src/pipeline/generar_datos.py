"""Genera el CSV de entrada del pipeline.

No descarga nada: el fichero se fabrica aquí, con una semilla fija, para que el
proyecto funcione sin red y para que dos ejecuciones den exactamente el mismo
resultado.

Los datos salen **sucios a propósito**. Cada defecto representa un problema real
que aparece en cualquier extracción de un sistema de gestión, y que se resuelve
siempre de la misma forma:

- fechas en tres formatos distintos      (dd/mm/aaaa, aaaa-mm-dd, dd-mm-aaaa)
- importes con coma decimal y con punto
- espacios sobrantes y mayúsculas inconsistentes en los textos
- filas duplicadas exactas
- valores ausentes en columnas opcionales y en alguna obligatoria
- cantidades negativas (devoluciones mal codificadas)
- ventas con importe cero, que no son un dato ausente sino un apunte sin dinero
"""

from __future__ import annotations

import csv
import random
from datetime import date, timedelta
from pathlib import Path

SEMILLA = 20260730

CIUDADES = ["Madrid", "Barcelona", "Valencia", "Sevilla", "Bilbao"]
PRODUCTOS = ["Teclado", "Monitor", "Ratón", "Portátil", "Auriculares"]
PRECIOS = {
    "Teclado": 29.90,
    "Monitor": 189.00,
    "Ratón": 15.50,
    "Portátil": 849.00,
    "Auriculares": 59.95,
}

CABECERA = ["id_venta", "fecha", "ciudad", "producto", "cantidad", "importe"]


def _formatear_fecha(dia: date, variante: int) -> str:
    """Devuelve la fecha en uno de los tres formatos que conviven en el origen."""
    if variante == 0:
        return dia.strftime("%d/%m/%Y")
    if variante == 1:
        return dia.isoformat()
    return dia.strftime("%d-%m-%Y")


def _formatear_importe(valor: float, con_coma: bool) -> str:
    """Coma o punto decimal, según el sistema que exportó la fila."""
    texto = f"{valor:.2f}"
    return texto.replace(".", ",") if con_coma else texto


def _ensuciar_texto(texto: str, rnd: random.Random) -> str:
    """Añade el ruido tipográfico habitual de un campo escrito a mano."""
    if rnd.random() < 0.15:
        texto = f"  {texto} "
    if rnd.random() < 0.10:
        texto = texto.upper()
    return texto


def generar(destino: Path, filas: int = 500) -> Path:
    """Escribe el CSV crudo en *destino* y devuelve la ruta."""
    rnd = random.Random(SEMILLA)
    inicio = date(2026, 1, 1)

    registros: list[list[str]] = []
    for i in range(1, filas + 1):
        producto = rnd.choice(PRODUCTOS)
        cantidad = rnd.randint(1, 8)

        # Devoluciones que el sistema de origen codifica como cantidad negativa.
        if rnd.random() < 0.03:
            cantidad = -cantidad

        importe = round(PRECIOS[producto] * abs(cantidad), 2)

        # Ventas fantasma: el sistema exporta el apunte con importe cero. No es un
        # dato ausente —el campo viene relleno— así que la conversión de tipos las
        # deja pasar y hay que decidir aparte qué se hace con ellas.
        if rnd.random() < 0.02:
            importe = 0.0

        dia = inicio + timedelta(days=rnd.randint(0, 180))

        fila = [
            str(i),
            _formatear_fecha(dia, rnd.randint(0, 2)),
            _ensuciar_texto(rnd.choice(CIUDADES), rnd),
            _ensuciar_texto(producto, rnd),
            str(cantidad),
            _formatear_importe(importe, rnd.random() < 0.4),
        ]

        # Ausencias: la ciudad falta a veces, y el importe en algún caso raro.
        if rnd.random() < 0.06:
            fila[2] = ""
        if rnd.random() < 0.02:
            fila[5] = ""

        registros.append(fila)

    # Duplicados exactos: la misma venta exportada dos veces.
    for _ in range(int(filas * 0.02)):
        registros.append(list(rnd.choice(registros)))

    rnd.shuffle(registros)

    destino.parent.mkdir(parents=True, exist_ok=True)
    with destino.open("w", newline="", encoding="utf-8") as fichero:
        escritor = csv.writer(fichero)
        escritor.writerow(CABECERA)
        escritor.writerows(registros)

    return destino
