# Experimento 01 — ¿Hace falta una skill para las convenciones del pipeline?

> Método y reglas: [PLANTILLA.md](PLANTILLA.md).
> **Estado: en curso.** Las secciones 1 y 2 están cerradas; la 3 y la 4, pendientes.

**Hipótesis** *(escrita antes de ejecutar nada)*:

> Sin la skill, el agente añadirá la condición **dentro de `convertir_tipos`** o como
> un filtro suelto: sin función propia, sin devolver `Recuento`, sin encadenarla en
> `limpiar()` y sin test. El informe seguirá cuadrando, así que **el fallo pasará
> desapercibido** — que es lo que lo hace interesante.

---

## El problema

`src/pipeline/limpiar.py` tiene una convención estricta: **una regla de limpieza =
una función = un test = un `Recuento`**. Está aplicada cinco veces, pero **no está
escrita en ninguna parte**. La pregunta es si hace falta escribirla como skill para
que el agente la respete al añadir la sexta.

---

## 1. Antes: sin skill

**Prompt exacto**, idéntico en todas las pasadas y sin ninguna pista añadida:

```text
Añade al pipeline una regla que descarte las ventas con importe cero.
```

**Condiciones:** sesión limpia · 30/07/2026 · **Claude Opus 5, esfuerzo medium** ·
Python 3.12 · DuckDB 1.5.5.

El agente **sí veía el repo entero**, incluido `limpiar.py` con sus docstrings. Eso
es deliberado: sube el listón. Si deduce la convención leyendo el código, la skill
sobra. Lo único aislado era la conversación donde se diseñó el pipeline.

### Resultados

| # | Función propia | Devuelve `Recuento` | Encadenada en `limpiar()` | Tests | Documenta el porqué | Actualiza README |
|---|:-:|:-:|:-:|:-:|:-:|:-:|
| 1 | ✅ | ✅ | ✅ | ✅ | ✅ | ❌ |
| 2 | ✅ | ✅ | ✅ | ✅ | ✅ | ❌ |
| 3 | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |

**Tres de tres en el diseño. La hipótesis falló en las cinco predicciones.**

### Salida representativa (pasada 1, sin retocar)

```python
def descartar_importe_cero(
    con: duckdb.DuckDBPyConnection, origen: str, destino: str
) -> Recuento:
    """Elimina las ventas con importe cero.

    Un importe a cero no es una venta: no aporta facturación y sí ensucia los
    promedios y el recuento de operaciones. […]

    Va **después** de `convertir_tipos` a propósito: antes, `importe` es texto y
    `"0,00"`, `"0"` y `"0.00"` serían tres cadenas distintas. Comparar con el
    número cero solo es fiable cuando ya es un número.
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
        motivo="importe cero: no es una venta",
    )
```

### Diagnóstico

No solo acertó: **convergió**. Las tres pasadas, sin contacto entre sí, tomaron las
mismas decisiones no triviales:

- **Colocarla después de `convertir_tipos`**, con el mismo razonamiento: antes el
  importe es texto y `"0"`, `"0.00"` y `"0,00"` son tres cadenas distintas que valen
  lo mismo.
- **Descartar solo el cero exacto**, conservando los negativos, porque son el reverso
  de las devoluciones. La pasada 3 lo expresó como *"filtrarlos aquí inflaría el
  importe neto por la puerta de atrás"*.
- **Corregir el docstring del módulo**, que decía que `convertir_tipos` era la única
  función que descartaba y habría quedado mintiendo.
- **Avisar del mismo hueco no pedido**: el generador no produce importes a cero, así
  que la regla reportará siempre 0 descartadas.

Tres agentes independientes produjeron el mismo diseño y detectaron el mismo hueco.
Eso no es acierto, es que **el repositorio no deja margen de interpretación**.

### La única variación: el alcance, no el diseño

Solo una de las tres actualizó el `README.md` para añadir el paso nuevo a la traza de
salida. Y esa diferencia no es casual:

> El **diseño** deja rastro en el código: cinco funciones hermanas con la misma
> firma lo enseñan sin que nadie lo escriba.
> La **lista de qué más hay que actualizar** no deja rastro en ninguna parte. Y ahí
> es justo donde apareció la variación.

---

## 2. ¿Merece una skill?

Los tres filtros del árbol de decisión, con lo que acabamos de medir:

| Filtro | Respuesta | Motivo |
|---|---|---|
| ¿Le pasaría igual a otra persona? | **Sí** | Cualquiera que añada una regla se enfrenta a lo mismo |
| ¿Va a volver a ocurrir? | **Sí** | El pipeline crecerá con más reglas |
| **¿El agente lo haría mal sin ella?** | **No, para el diseño. Sí, para el alcance** | 3/3 clavaron el patrón; 1/3 actualizó el README |

**Destino elegido: dividido, y esa es la conclusión del experimento.**

- **El patrón → el código.** Ya está ahí, y funciona mejor que cualquier documento:
  cinco ejemplos aplicados vencen a una descripción. Escribir una skill que repita lo
  que el código ya comunica sería añadir contexto sin añadir criterio.
- **El alcance → skill (candidata).** *"Al añadir una regla, actualiza también el
  README y el docstring del módulo"* no se deduce de `limpiar.py`, y es donde hubo
  variación real.

### La regla general que sale de aquí

> **Si el criterio deja rastro en el código, el código lo enseña.
> La skill hace falta cuando el criterio no deja rastro.**

Se comprueba mirando las dos skills que ya existen en este repo: ninguna trata de
algo que se pueda leer en un fichero fuente. Conventional Commits no se ve en el
código. Comprobar la rama antes de commitear, tampoco.

Corolario incómodo, y probablemente lo más útil de todo el experimento:

> **Escribir bien el código es la forma más barata de no necesitar una skill.**

---

## 3. La skill

*Pendiente.* Depende del resultado de la sección 4.

## 4. Después: con skill

*Pendiente.*

### 4.1 Variante: ¿depende del modelo o del repositorio?

Las pasadas 1-3 usaron el modelo más capaz disponible. Eso deja abierta la pregunta
que de verdad le importa a un equipo, porque **nadie usa el modelo más caro para
todo**:

> ¿La calidad del código sustituye a la skill **siempre**, o solo cuando el modelo es
> lo bastante bueno?

**Pasada 4:** mismo prompt, sesión limpia, **Claude Haiku 4.5, esfuerzo medium**.

- Si converge → la conclusión "el código enseña" queda blindada.
- Si falla → la skill sí se justifica, y con un matiz mucho más útil: **la skill es lo
  que iguala el resultado hacia abajo**, no lo que mejora el resultado hacia arriba.

*Resultado: pendiente.*

---

## Qué aprendimos

*Pendiente de cerrar.* Provisional, con las secciones 1 y 2 hechas:

1. La hipótesis falló en las cinco predicciones. **El "antes" no es un trámite: es
   donde estaba toda la información.**
2. Un repositorio con el patrón aplicado y explicado enseña mejor que un documento
   que lo describe.
3. La variación aparece exactamente donde el criterio no deja rastro.

## Cuándo NO hacer esto

*Pendiente.*

## Condiciones y reproducibilidad

- **Fecha:** 30 de julio de 2026
- **Modelos:** pasadas 1-3, Claude Opus 5 (medium) · pasada 4, Claude Haiku 4.5 (medium)
- **Versiones:** Python 3.12 · DuckDB 1.5.5 · pytest 9.1.1 · uv 0.7.9
- **Rama:** `docs/material-didactico`
- **Cómo repetirlo:** partir del repo limpio, abrir sesión nueva sin contexto previo,
  pegar el prompt tal cual, no responder a preguntas más allá de lo imprescindible,
  no dejar commitear. Entre pasadas: `git checkout -- . ; git clean -fd`.

> Los resultados con modelos generativos **varían entre ejecuciones**. Este registro
> documenta lo que ocurrió en las condiciones indicadas, no una garantía. Si al
> repetirlo obtienes algo distinto, eso también es información: anótalo.
