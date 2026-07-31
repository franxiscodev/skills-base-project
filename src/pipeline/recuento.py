"""Trazabilidad de lo que el pipeline descarta.

Existe por una razón concreta: sin esto, "limpiar los datos" es un paso opaco en
el que entran 510 filas y salen 480, y nadie sabe qué pasó con las otras 30. Cada
regla de limpieza deja aquí su rastro, y el informe final lo publica.
"""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class Recuento:
    """Qué hizo un paso: cuántas filas entraron, cuántas salieron y por qué."""

    paso: str
    entrantes: int
    salientes: int
    motivo: str

    @property
    def descartadas(self) -> int:
        return self.entrantes - self.salientes

    def __str__(self) -> str:
        if self.descartadas == 0:
            return f"{self.paso}: {self.salientes} filas, sin descartes"
        return (
            f"{self.paso}: {self.entrantes} → {self.salientes} "
            f"({self.descartadas} descartadas — {self.motivo})"
        )
