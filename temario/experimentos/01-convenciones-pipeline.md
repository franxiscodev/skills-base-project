# Experimento 01 — ¿Hace falta una skill para las convenciones del pipeline?

> Método y reglas: [PLANTILLA.md](PLANTILLA.md).
> **Estado: en curso.** El "antes" está cerrado (6 pasadas, 2 modelos) y la decisión
> tomada. Falta escribir la skill y medir el "después".

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
| 1 | ✅ | ✅ | ✅ | ✅ (2) | ✅ | ❌ |
| 2 | ✅ | ✅ | ✅ | ✅ (2) | ✅ | ❌ |
| 3 | ✅ | ✅ | ✅ | ✅ (2) | ✅ | ✅ |

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

## 1.B El mismo prompt con un modelo más pequeño

La pregunta que de verdad le importa a un equipo, porque **nadie usa el modelo más
caro para todo**:

> ¿La calidad del código sustituye a la skill **siempre**, o solo cuando el modelo es
> lo bastante bueno?

**Condiciones:** idénticas, salvo el modelo — **Claude Haiku 4.5, esfuerzo medium**.
Pasadas 4, 5 y 6.

| # | Función propia | `Recuento` | Encadenada | Tests | README | Commitea sin que se lo pidan |
|---|:-:|:-:|:-:|:-:|:-:|:-:|
| 4 | ✅ | ✅ | ✅ | ✅ (1) | ❌ | ⚠️ sí |
| 5 | ✅ | ✅ | ✅ | ✅ (1) | ❌ | ⚠️ sí |
| 6 | ✅ | ✅ | ✅ | ✅ (1) | ❌ | no |

### El patrón estructural aguanta: 6 de 6

**Los dos modelos respetaron la convención sin excepción.** Función propia, misma
firma, `Recuento` con su motivo, encadenada en el sitio correcto y con las tablas
intermedias renumeradas. Ni una sola desviación en seis intentos.

Esto responde la pregunta principal: **el código enseña el patrón, y lo enseña lo
bastante bien como para que un modelo pequeño también lo copie.**

### Dónde sí se separan los modelos

| | Opus 5 | Haiku 4.5 |
|---|---|---|
| **Tests escritos** | 2 | 1 |
| **El caso negativo** (que una devolución **no** se descarte) | 3/3 | 0/3 |
| **Justifica por qué ese orden** | 3/3, con el detalle de `"0"` / `"0,00"` | superficial: "cuando ya es un número" |
| **Detecta el hueco no pedido** (el generador no produce ceros) | 3/3 | 0/3 |
| **Commitea sin permiso** | 0/3 | 2/3 |

Las diferencias **no están en la estructura, están en la profundidad**:

- Haiku escribe el test que demuestra que la regla funciona. Opus escribe además el
  que demuestra que **no se pasa de frenada** — que una devolución con importe real
  sobrevive. Ese segundo test es el que protege el criterio de negocio.
- Ninguna pasada de Haiku avisó de que, con los datos de muestra, la regla nueva
  descarta 0 filas y por tanto **no se puede comprobar que funcione en el pipeline
  real**. Las tres de Opus lo señalaron sin que nadie lo pidiera.

### El hallazgo lateral: quién decide commitear

Haiku commiteó por iniciativa propia en 2 de 3 pasadas —una de ellas en una rama de
documentación, para un cambio de código—. Opus, ninguna.

Y el detalle que lo hace interesante: **el mensaje de commit era impecable**. Tipo,
scope, imperativo, cuerpo explicando el porqué. La skill `git-conventional-commits`
de este repo **se disparó y funcionó perfectamente con el modelo pequeño**.

> Lo que falló no fue el formato, fue el juicio. La skill sabe **cómo** se escribe un
> commit. La decisión de **si tocaba commitear** no está en ninguna skill — y ahí es
> donde los modelos se separan.

Es un argumento a favor de las skills, no en contra: hacen bien exactamente aquello
para lo que se escriben, incluso con modelos modestos.

---

## 2. ¿Merece una skill?

Los tres filtros del árbol de decisión, con los seis resultados sobre la mesa. El
tercero hay que responderlo **por separado para cada cosa que la skill diría**, y ahí
está todo el hallazgo:

| Lo que diría la skill | ¿El agente lo hace mal sin ella? | Medición |
|---|---|---|
| Una regla = una función con la misma firma | **No** | 6/6 |
| Devolver `Recuento` con su motivo | **No** | 6/6 |
| Encadenarla en `limpiar()` en el sitio correcto | **No** | 6/6 |
| Escribir un test de la regla | **No** | 6/6 |
| **Cubrir también el caso que NO debe verse afectado** | **Sí** | 3/6 — solo Opus |
| **Actualizar el README y el resto de sitios** | **Sí** | 1/6 |
| **Avisar si la regla no queda ejercitada por los datos** | **Sí** | 3/6 — solo Opus |

Los otros dos filtros salen sí: le pasaría igual a cualquiera, y volverá a ocurrir
cada vez que el pipeline crezca.

### Destino: dividido. Y esa es la conclusión del experimento

- **El patrón → el código.** Ya está ahí y funciona mejor que cualquier documento:
  cinco ejemplos aplicados vencen a una descripción, y los copian los dos modelos sin
  fallar una vez. Escribir una skill que repita lo que el código ya comunica sería
  **añadir contexto sin añadir criterio** — exactamente lo que la tesis del curso pide
  evitar.
- **El alcance y la profundidad → skill.** Qué otros ficheros hay que tocar, qué caso
  negativo hay que cubrir y qué avisar cuando la regla no queda ejercitada **no se
  deducen de `limpiar.py`**, y es justo donde apareció toda la variación.

### La regla general que sale de aquí

> **Lo que el código muestra, el código lo enseña. La skill hace falta para lo que el
> código no puede mostrar.**

Un fichero enseña sus propios patrones porque están a la vista, repetidos. Pero
`limpiar.py` no puede decir *"y además actualiza el README"*, ni *"comprueba que los
datos de muestra ejerciten la regla"*: eso no cabe en el código, porque no es código.

Se confirma mirando las dos skills que ya existen en este repo: **ninguna trata de
algo que se pueda leer en un fichero fuente.** Conventional Commits no se ve en el
código. Comprobar la rama antes de commitear, tampoco.

Y el corolario, que es probablemente lo más útil del experimento:

> **Escribir bien el código es la forma más barata de no necesitar una skill.**
> Cada patrón que dejas evidente en el propio código es una skill que no tienes que
> escribir, mantener ni pagar en contexto.

---

## 3. La skill

📄 [`.claude/skills/pipeline-reglas-de-limpieza/SKILL.md`](../../.claude/skills/pipeline-reglas-de-limpieza/SKILL.md)

**Fuera** — lo que el código ya enseña (6/6): la firma, el `Recuento`, el encadenado,
escribir un test. Meterlo sería pagar contexto por algo ya resuelto.

**Dentro** — solo los tres puntos donde hubo variación: los otros sitios a actualizar,
el caso negativo, y el aviso sobre los datos de muestra.

Es corta a propósito. Y es justo la contraria de la que íbamos a escribir al empezar.

### Decisiones de escritura

**La `description`.** Es lo único que el agente ve antes de decidir si carga la skill,
así que lleva:

- **Qué resuelve, no qué es**: *"qué hay que actualizar **además del código**"*. Si
  dijera "convenciones del pipeline" competiría con lo que el código ya hace.
- **Disparadores literales** en el idioma en que se pide: *"añade una regla"*,
  *"descarta las filas que..."*, *"filtra las ventas..."*, *"cambia el criterio"*.
- **El fichero**: `src/pipeline/limpiar.py`. Un agente que va a editarlo debería
  cargarla aunque la petición esté redactada de otra forma.

**La sección "Lo que esta skill NO dice".** Va la primera, y es deliberado: evita que
un lector futuro "complete" la skill añadiéndole el patrón que el código ya enseña.
Sin esa sección, esta skill engorda sola en tres meses.

**Cada regla lleva su medición** (`1 de 6`, `3 de 6`). Convierte la skill en algo
falsable: si mañana la medición cambia, la regla se cae. Una skill sin evidencia solo
se puede discutir por opiniones.

**"Cuándo dejar de usar esta skill".** Las condiciones del experimento caducan. Si
`limpiar.py` deja de ser funciones hermanas, la medición no vale y la skill tampoco.

## 3.bis Una pasada anulada, y por qué se cuenta

La primera pasada del "después" salió **bien** y hubo que **tirarla**. Se conserva el
diff como `exp01-despues-CONTAMINADA.diff`. Falló por dos motivos independientes.

**Primero, el punto de partida no era el mismo.** El commit que cerraba la
documentación del "antes" arrastró sin querer el código de una de las pasadas: la
regla y su test entraron en el repo. El agente del "después" no se encontró la tarea
del "antes" —*escribe la regla y todo lo demás*— sino solo *todo lo demás*. Prompt
idéntico, condiciones distintas.

> **Un "después" empieza en el mismo commit que el "antes".** Verificarlo con
> `git status` no basta: el árbol estaba limpio, y aun así contaminado. Hay que mirar
> **qué hay commiteado**, no si hay cambios pendientes.

**Segundo, y peor: la skill contenía la respuesta.** Al escribirla usamos como
ejemplos el mismo caso con el que íbamos a medirla —el importe a cero, la devolución
que debe sobrevivir, el docstring de `convertir_tipos`—. El agente reprodujo los tres
ejemplos casi literalmente. Eso no mide si la skill sirve: mide si el modelo sabe
copiar un ejemplo que tiene delante.

> **Una skill no puede usar como ejemplo el caso con el que se va a medir.** Si lo
> hace, el "después" no mide transferencia, mide copia. El ejemplo tiene que estar
> cerca del principio y lejos de la prueba.

Es el error clásico de cualquier evaluación mal montada —*teaching to the test*— y
apareció aquí sin mala intención: al redactar la skill teníamos el caso de prueba
fresco y fue el ejemplo que salió solo. Solo se ve con un resultado delante.

**Lo que sí sobrevive de esa pasada**, porque no estaba en la skill: el agente se negó
a añadir a la tabla de defectos del README una fila que habría afirmado que el
generador fabrica importes a cero, cuando no lo hace. Eso es criterio, no copia. Es
una observación, no una medida.

**Correcciones aplicadas antes de repetir:** el código volvió al estado previo, y los
ejemplos del `SKILL.md` se reescribieron con reglas distintas de la de prueba
(`imputar_ciudad`, `marcar_devoluciones`). El enunciado de cada regla no cambió.

## 4. Después: con skill

*Pendiente.* Se repetirá el mismo prompt, tres pasadas por modelo, y se comprobará
por separado que la skill **se disparó** — que el resultado salga bien no prueba que
se cargara.

---

## Qué aprendimos

*Provisional: falta la sección 4.*

1. **La hipótesis falló en las cinco predicciones.** El "antes" no es un trámite
   burocrático: era donde estaba toda la información. Sin él habríamos escrito una
   skill inútil y celebrado que funcionaba.
2. **Un repositorio con el patrón aplicado enseña mejor que un documento que lo
   describe.** Cinco funciones hermanas convencieron a dos modelos distintos, seis
   veces seguidas, sin una línea de instrucciones.
3. **La variación aparece exactamente donde el criterio no deja rastro** — otros
   ficheros, casos negativos, avisos sobre los datos. Ahí es donde una skill paga.
4. **Un modelo más pequeño copia la estructura igual de bien, pero pierde
   profundidad.** No se equivoca de forma distinta: hace menos. Es un argumento
   fuerte para escribir la skill aunque tú uses el modelo grande, porque tu equipo
   no lo hará siempre.
5. **Las skills funcionan con modelos modestos.** La de commits se disparó con Haiku
   y produjo mensajes impecables. Lo que no cubre una skill de formato es el
   *juicio* — decidir si tocaba commitear.

## Cuándo NO hacer esto

- **Cuando el patrón se pueda dejar evidente en el código.** Sale más barato escribir
  bien el código que mantener una skill que lo describa.
- **Cuando no puedas medir el "antes" en condiciones limpias.** Sin comparación, la
  skill es una creencia.
- **Cuando el proyecto vaya a cambiar de forma pronto.** Una skill que describe una
  estructura inestable envejece antes de dispararse por primera vez.

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
