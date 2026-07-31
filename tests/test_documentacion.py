"""El README no puede mentir sobre lo que hace el pipeline.

Este fichero existe por una medición, no por una intuición. Dieciocho ejecuciones
registradas en `temario/experimentos/` pidieron añadir una regla de limpieza. En
todas ellas la parte del código salió bien; la que falló fue mantener cierto lo que
el README dice de la salida. Con la instrucción escrita como lista de sitios, ninguna
de las seis dejó el README verdadero; reescrita como criterio, el modelo grande
acertó tres de tres y el pequeño una de tres.

Un punto que depende de que el ejecutor se acuerde —y de cuánto juicio tenga— no
pertenece a una skill: pertenece aquí. Este test no gasta contexto, no depende de
quién ejecute y falla solo.

Lo que comprueba es una sola cosa, y por eso se puede confiar en ella: **el bloque de
consola documentado en el README es, línea por línea, lo que el pipeline imprime hoy.**
"""

from __future__ import annotations

import re
from pathlib import Path

import duckdb
import pytest

from pipeline import cargar as paso_cargar
from pipeline import generar_datos, informe, limpiar, metricas

RAIZ = Path(__file__).resolve().parents[1]
README = RAIZ / "README.md"

#: Filas con las que se generó la traza que está escrita en el README.
FILAS_DOCUMENTADAS = 500


def _bloque_documentado() -> list[str]:
    """Extrae del README el bloque de consola de ejemplo, ya sin indentación.

    Se busca por el encabezado `Procesado` dentro de un bloque ```text``` en lugar
    de por número de línea: el README se reordena a menudo, y un test que dependa de
    dónde está el bloque falla por moverlo, que no es lo que queremos detectar.
    """
    texto = README.read_text(encoding="utf-8")
    bloques = re.findall(r"```text\n(.*?)```", texto, re.DOTALL)
    candidatos = [b for b in bloques if b.lstrip().startswith("Procesado")]

    if len(candidatos) != 1:
        pytest.fail(
            "Se esperaba exactamente un bloque ```text``` que empiece por "
            f"'Procesado' en el README, y hay {len(candidatos)}. "
            "Si has movido o duplicado la traza de ejemplo, ajusta este test."
        )

    return [linea.strip() for linea in candidatos[0].strip().splitlines() if linea.strip()]


def _salida_real(tmp_path: Path) -> list[str]:
    """Ejecuta el pipeline de verdad y devuelve las mismas líneas que imprimiría.

    Se replica el orden de `informe.resumir_en_consola` en vez de capturar `stdout`
    porque aquí interesa el contenido, no el mecanismo de impresión.
    """
    csv = generar_datos.generar(tmp_path / "ventas.csv", filas=FILAS_DOCUMENTADAS)

    con = duckdb.connect()
    recuentos = [paso_cargar.cargar(con, csv)]
    tabla, recuentos_limpieza = limpiar.limpiar(con, paso_cargar.TABLA_CRUDA)
    recuentos += recuentos_limpieza
    res = metricas.resumen(con, tabla)

    lineas = ["Procesado"]
    lineas += [str(recuento) for recuento in recuentos]
    lineas += [
        "Resultado",
        f"Ventas ........... {res.ventas}",
        f"Devoluciones ..... {res.devoluciones}",
        f"Importe neto ..... {informe._euros(res.importe_neto)}",
    ]
    return lineas


def test_la_traza_del_readme_es_la_salida_real(tmp_path):
    """Cada línea documentada existe y dice exactamente lo que el pipeline imprime.

    Cubre los tres fallos que aparecieron en la medición:

    - **Falta un paso** — se añade una regla y no se documenta.
    - **Sobra un paso** — se quita una regla y la línea se queda.
    - **La línea es inventada** — se escribe a mano un formato plausible en lugar de
      copiar la salida (`490 → 490 (0 descartadas)` donde el programa dice
      `490 filas, sin descartes`).
    """
    documentado = _bloque_documentado()
    real = _salida_real(tmp_path)

    assert documentado == real, (
        "El bloque de consola del README ya no coincide con lo que imprime el "
        "pipeline. Ejecuta `uv run python -m pipeline` y copia la salida literal "
        "en lugar de editarla a mano."
    )


#: Cuentas escritas a mano en prosa: "los cinco pasos", "las seis reglas".
CUENTA_EN_PROSA = re.compile(
    r"\b(un|dos|tres|cuatro|cinco|seis|siete|ocho|nueve|diez|\d+)\s+"
    r"(pasos?|reglas?|etapas?|m[óo]dulos?)\b",
    re.IGNORECASE,
)


def test_el_readme_no_lleva_cuentas_escritas_a_mano():
    """Prohíbe la construcción que caducó en catorce de las dieciocho ejecuciones.

    La línea `# ejecuta los cinco pasos` quedó falsa una y otra vez al añadir una
    regla. No es que se les olvidara mirarla: es que **una cuenta escrita en prosa
    caduca cada vez que cambia el pipeline** y nada avisa.

    Este test es más estricto que "¿es verdad?" a propósito. Tres ejecuciones la
    dejaron cierta poniendo *"los seis pasos"* — y esa versión vuelve a caducar en el
    cambio siguiente. El arreglo bueno no es actualizar el número sino escribir la
    frase de forma que no dependa de él: *"ejecuta el pipeline completo"*. Cuatro
    ejecuciones llegaron solas a esa solución; este test la impone para las demás.

    Si algún día hace falta enumerar de verdad, la lista se genera desde el código.
    """
    hallazgos = [
        f"  README.md:{numero}: {linea.strip()}"
        for numero, linea in enumerate(README.read_text(encoding="utf-8").splitlines(), 1)
        if CUENTA_EN_PROSA.search(linea)
    ]

    assert not hallazgos, (
        "El README lleva una cuenta escrita a mano que caducará al cambiar el "
        "pipeline. Reescribe la frase sin el número:\n" + "\n".join(hallazgos)
    )
