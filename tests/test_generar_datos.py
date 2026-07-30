"""El generador tiene que ser reproducible, o nada de lo demás se puede enseñar.

Con semilla fija, dos ejecuciones producen exactamente el mismo fichero. Sin eso
no se puede escribir un test sobre los datos, ni repetir una demo, ni comparar el
informe de ayer con el de hoy.
"""

from __future__ import annotations

import hashlib

from pipeline import generar_datos


def _hash(ruta):
    return hashlib.sha256(ruta.read_bytes()).hexdigest()


def test_dos_generaciones_dan_el_mismo_fichero(tmp_path):
    primera = generar_datos.generar(tmp_path / "a.csv", filas=50)
    segunda = generar_datos.generar(tmp_path / "b.csv", filas=50)

    assert _hash(primera) == _hash(segunda)


def test_genera_las_filas_pedidas_mas_los_duplicados(tmp_path):
    destino = generar_datos.generar(tmp_path / "ventas.csv", filas=100)

    lineas = destino.read_text(encoding="utf-8").strip().splitlines()

    # 100 filas + 2% de duplicados + la cabecera.
    assert len(lineas) == 100 + 2 + 1


def test_el_csv_trae_los_defectos_a_proposito(tmp_path):
    """Si el generador dejara de ensuciar, los tests de limpieza no probarían nada."""
    destino = generar_datos.generar(tmp_path / "ventas.csv", filas=300)
    texto = destino.read_text(encoding="utf-8")

    assert "/" in texto and "-" in texto, "faltan formatos de fecha distintos"
    assert ",," in texto, "faltan valores ausentes"
    assert '"' in texto or ",-" in texto, "faltan cantidades negativas"
