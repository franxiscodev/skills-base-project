# Experimento 02 — ¿Se arregla cambiando cómo está escrita la regla?

> Continúa el [experimento 01](01-convenciones-pipeline.md). Método:
> [PLANTILLA.md](PLANTILLA.md).
> **Estado: cerrado.** Seis pasadas —tres por modelo—, con la hipótesis y la condición
> de desempate escritas antes de ejecutar nada.

**Hipótesis** *(escrita antes de ejecutar nada)*:

> Reescribir las reglas como **criterio de terminado** en vez de como **lista de
> sitios** sube el "README verdadero" por encima de 0, porque un criterio se puede
> aplicar a un sitio que no está enumerado y una lista no.

## El problema

El experimento 01 midió una skill que funcionó en todo lo que pedía y aun así dejó el
trabajo mal:

| | Antes | Después |
|---|---|---|
| Toca el README | 1/6 | 6/6 |
| **Deja el README verdadero** | — | **0/6** |
| Escribe un caso negativo | 3/6 | 6/6 |
| **El caso negativo protege el criterio** | — | **4/6** |

El diagnóstico fue que las reglas estaban escritas como tareas, y una tarea se ejecuta
—también donde no toca—. Este experimento comprueba si eso se arregla con la
redacción, o si no se arregla con una skill en absoluto.

## Qué cambia y qué no

**Cambia:** §1 y §2 del `SKILL.md`, reescritas en criterio.

| | Antes (lista) | Ahora (criterio) |
|---|---|---|
| §1 | "Actualiza el README, el docstring del módulo y los vecinos" | "Que no quede ni una frase falsa. Búscalas, no las recuerdes. Y comprueba que es verdad lo que añades" |
| §2 | "Escribe un test de que no toca lo que no debe" | "Rompe la regla a propósito y comprueba que el test se pone rojo" |

**No cambia, a propósito:**

- **La `description`.** Se disparó 6 de 6; tocarla metería una segunda variable en la
  misma medición.
- **La §3** (el aviso sobre los datos de muestra). Es la **variable de control**: si se
  mantiene en 6/6 mientras las otras dos se mueven, el cambio viene del cambio y no de
  la sesión, del día o del humor del modelo.
- **El prompt**, carácter por carácter.

## 1. Las pasadas

**Prompt exacto:**

```text
Añade al pipeline una regla que descarte las ventas con importe cero.
```

**Condiciones:** sesión limpia · commit de partida verificado con `git log` ·
Claude Haiku 4.5 (medium)

### Por qué solo un modelo, y por qué el pequeño

Opus está **en el techo** del caso negativo: 3 de 3 en el experimento 01. Un resultado
que no puede subir no mide nada. Haiku tiene recorrido en las dos cosas —README 0/3,
caso negativo útil 1/3— y además es la prueba más dura: si un criterio bien redactado
arregla al modelo pequeño, con el grande casi seguro que también. Al revés no vale.

> **Regla general:** mide la mejora donde haya margen. Repetir con el modelo que ya
> acierta produce una tabla bonita y ninguna información.

### La condición de desempate, escrita por adelantado

| Resultado con Haiku | Qué significa | Qué se hace |
|---|---|---|
| Mejora | La redacción importa. Hipótesis confirmada | Se cierra |
| **No mejora** | **Ambiguo**: puede ser la redacción o el modelo | **Una pasada con Opus** para desempatar |

Y el desempate, también decidido de antemano:

- **Opus tampoco mejora** → el problema no es cómo está escrita la regla. Ese punto
  **no se arregla con una skill** y baja al código: un test que compare la traza
  documentada en el README con la salida real del pipeline. No gasta contexto y falla
  solo.
- **Opus sí mejora** → el problema no era la redacción sino el lector. La lección
  cambia entera: **una skill puede exigir más juicio del que tiene el modelo que la
  lee**, y eso obliga a escribirla para el modelo más pequeño que vaya a usarla.

### Resultados

**Haiku 4.5** — las tres pasadas previstas:

| Pasada | ¿Se disparó? | README verdadero | Test de los dos lados | §3 (control) |
|---|---|---|---|---|
| 1 | ✅ | ❌ | ❌ un lado | ✅ |
| 2 | ✅ | ✅ | ❌ un lado | ✅ |
| 3 | ✅ | ❌ | ❌ un lado | ✅ |

**Opus 5** — una de desempate, más dos por insuficiencia muestral (ver más abajo):

| Pasada | ¿Se disparó? | README verdadero | Test de los dos lados | §3 (control) |
|---|---|---|---|---|
| 1 | ✅ | ✅ | ✅ | ✅ |
| 2 | ✅ | ✅ | ✅ | ✅ |
| 3 | ✅ | ✅ | ✅ | ✅ |

**El control aguantó 6 de 6.** La §3 no se tocó y siguió disparándose siempre: lo que
se movió, lo movió el cambio de redacción, no la sesión ni el día.

### Por qué el desempate acabó siendo tres pasadas

La condición pre-registrada preveía **una** pasada con Opus. Salió limpia, y esa
respuesta habría bastado para elegir rama — pero no para publicar la comparación, que
enfrentaba **n=3 con lista contra n=1 con criterio**. Se ejecutaron dos más hasta
igualar el tamaño de muestra.

> Es una desviación del plan y se anota como tal. La regla que sale: **el
> pre-registro decide qué significa el resultado, no cuántas veces basta con medirlo.**
> Son dos cosas distintas y conviene fijar las dos por adelantado.

## Qué cambió

| | Exp 01 (lista) | Exp 02 (criterio) |
|---|---|---|
| README verdadero — **Opus** | 0/3 | **3/3** |
| README verdadero — **Haiku** | 0/3 | 1/3 |
| Test que cubre los dos lados — **Opus** | 3/3 | 3/3 *(ya estaba en el techo)* |
| Test que cubre los dos lados — **Haiku** | 1/3 | 0/3 |

**La hipótesis se confirma, con un límite.** La redacción importa —y mucho: el mismo
modelo pasa de fallar el README las tres veces a acertarlo las tres— pero el mismo
texto solo levanta a Haiku 1 de 3.

### Lo que hicieron las seis, y ninguna del experimento 01

- **Buscaron en vez de recordar.** Cinco de seis dijeron explícitamente que habían ido
  a buscar las frases afectadas.
- **Rompieron la regla a propósito** para comprobar que el test se ponía rojo.

Las dos instrucciones nuevas se ejecutan. Lo que cambia entre modelos no es si las
ejecutan: es **con cuánta imaginación**.

### El fallo nuevo que trajo la §2

Las tres pasadas de Haiku falsaron de verdad, y las tres escribieron el mismo test
insuficiente: solo `0,01 €`, sin ningún importe negativo.

> **Falsar por un solo lado del límite da más confianza que no falsar, con la misma
> cobertura.** El sello de "verificado" no lo puso el rigor: lo puso el haber pensado
> en un solo borde.

Es la segunda vez que una regla mejora un número y trae su propio defecto —la primera
fue la fila falsa del experimento 01—. Ya no es casualidad:

> **Toda instrucción que añades a una skill se ejecuta también de la forma más barata
> que la cumpla.** Al escribir una regla, pregúntate cuál es esa forma. Si te vale, la
> regla está bien; si no, falta acotarla.

### El indicio de que el criterio hace algo más que la lista

En una pasada, Opus corrigió una frase falsa **que no venía de su cambio**:
`__init__.py` decía *"Cuatro pasos, uno por módulo"* sobre un diagrama que lista
cinco. Llevaba mal desde que se escribió el pipeline. Ninguna instrucción menciona ese
fichero, y una lista de sitios nunca lo habría incluido.

Dos pasadas resolvieron además la línea 431 **quitando la cuenta** —*"ejecuta el
pipeline completo"*— en vez de actualizar el número. Eso no arregla el error: elimina
la clase entera de error.

## Qué aprendimos

1. **Una regla se redacta como criterio de terminado, no como lista de sitios.** Mismo
   contenido, mismo coste de contexto, y en el modelo capaz la diferencia es 0/3 → 3/3.
2. **La skill sube el techo; el código sube el suelo.** Una skill bien escrita hace que
   el modelo capaz haga el trabajo completo. **No** hace que el modelo pequeño lo haga.
   Si no controlas quién ejecuta, el punto tiene que bajar a algo que no dependa del
   lector.
3. **Toda instrucción se cumple también de la forma más barata posible.** Pide falsar y
   te falsan un lado. Pide actualizar y te actualizan hacia la mentira.
4. **Una skill que hace buscar encuentra cosas que no le tocaban.** Es un efecto lateral
   deseable y no se puede pedir directamente: sale de haber escrito el criterio en vez
   del sitio.
5. **Medir donde hay margen.** Repetir con el modelo que ya acierta produce una tabla
   bonita y ninguna información. El caso negativo de Opus estaba en 3/3 antes de
   empezar: por eso el bloque principal fue con Haiku.

## Cuándo NO hacer esto

- **Cuando la lista sea de verdad cerrada.** Si los sitios afectados son tres, fijos y
  no van a cambiar, enumerarlos es más corto y más claro. El criterio paga cuando la
  lista **no puede estar completa**, que es casi siempre.
- **Cuando no puedas comprobar el criterio.** *"Deja el README verdadero"* funciona
  porque se puede verificar con un `grep`. Un criterio que no se puede comprobar es una
  buena intención.
- **Cuando el ejecutor no dé para el criterio.** Con modelos pequeños, un criterio
  abierto rinde peor que una lista cerrada, aunque en el modelo grande gane. **Escribe
  para el ejecutor más modesto que vaya a leerlo**, o baja el punto al código.

## Lo que sigue

El 1/3 de Haiku es lo que justifica el paso siguiente, y ya no como opinión: **añadir
un test que compare la traza documentada en el README con la salida real del
pipeline.** No gasta contexto, no depende de que nadie se acuerde y falla solo. La
skill se queda —sube el techo—; el test pone el suelo.

**Hecho:** [experimento 03](03-bajar-al-codigo.md). El test se validó contra los
dieciocho diffs guardados, sin generar ninguna pasada nueva: caza 6 de 6 fallos y no
da un solo falso positivo en las 12 ejecuciones correctas.

## Condiciones y reproducibilidad

- **Fecha:** 31 de julio de 2026
- **Modelos:** tres pasadas con Claude Haiku 4.5 (medium) y tres con Claude Opus 5
  (medium)
- **Versiones:** Python 3.12 · DuckDB 1.5.5 · pytest 9.1.1 · uv 0.7.9
- **Rama:** `docs/material-didactico`
- **Commit de referencia:** `f7e4e5b` — verificado con `git log` antes de cada pasada
- **Diffs guardados:** en [`diffs/`](diffs/) — `exp02-haiku-1/2/3.diff`,
  `exp02-opus-desempate.diff` (la primera de Opus, con el nombre que tenía cuando se
  planificó) y `exp02-opus-2/3.diff`.
- **Cómo repetirlo:** igual que el [experimento 01](01-convenciones-pipeline.md), con
  el mismo prompt. La comparación exige partir del commit de referencia, no solo de un
  árbol limpio.

> Los resultados con modelos generativos **varían entre ejecuciones**. Este registro
> documenta lo que ocurrió en las condiciones indicadas, no una garantía. Si al
> repetirlo obtienes algo distinto, eso también es información: anótalo.
