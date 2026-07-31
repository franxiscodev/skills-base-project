# Experimento 04 — Qué cuesta de verdad una capacidad instalada

> **Estado: medidas A y B cerradas. Medida C pre-registrada y pendiente.**
> Las secciones 0 a 2 se escribieron **antes de ejecutar nada**. La hipótesis se conserva
> tal cual **aunque haya fallado**: reescribirla ahora sería inventar un acierto.

**Hipótesis (pre-registrada, y ❌ refutada por la medida A):** en este cliente, un servidor
MCP conectado y no usado cuesta mucho menos de lo que dice la teoría —porque las
definiciones se cargan bajo demanda— y el coste real no está en el peaje permanente sino en
**el momento en que dos caminos hacen lo mismo**.

> **Lo que falló:** el peaje permanente resultó ser **mayor** que el de cualquier skill del
> repositorio. Acerté en que los esquemas se cargan bajo demanda y me equivoqué en la
> conclusión, porque el coste estaba en otro sitio que no había mirado.

---

## Por qué este experimento existe

El [capítulo 00](../00-la-tesis.md) afirma que se paga peaje permanente por *"la definición
de cada herramienta de cada servidor MCP"*. Al ir a diseñar esta medición apareció un
problema: **puede que esa frase sea más fuerte de lo que el material puede sostener.**

No se corrige todavía. Se mide, y luego se corrige con el número delante. Ese es el orden
del [método](PLANTILLA.md), y aplicarlo contra el propio material es la única forma de que
signifique algo.

---

## El problema

La recomendación habitual sobre MCP es *"instala lo que necesites"*, sin coste asociado.
La tesis de este repositorio dice lo contrario: toda capacidad instalada se paga en cada
turno. **Ninguna de las dos posturas se ha medido aquí.**

Y hay una tercera posibilidad, que es la que motiva el pre-registro: que el coste dependa
de **cómo el cliente carga las herramientas**, y que por tanto la respuesta correcta no sea
"sí" ni "no" sino "depende de algo que casi nadie mira".

---

## 0. Observación de partida (sin pasadas)

Registrada el 31 de julio de 2026, antes de diseñar nada. **No es un resultado del
experimento**: es la condición inicial, y es lo que obligó a cambiar el diseño.

Inventario declarado por el cliente (`claude mcp list`):

| Servidor | Estado declarado |
|---|---|
| context7 | Conectado |
| claude.ai Google Drive / Gmail / Google Calendar | Conectado |
| claude.ai Indeed / Canva | Requiere autenticación |

Inventario **realmente disponible en la sesión**:

| | Observado |
|---|---|
| Herramientas de `context7` | Presentes, **por nombre, sin esquema** |
| Herramientas de los cinco conectores de claude.ai | **Ausentes** — el sistema informa de que requieren autenticación en esta sesión |

Dos cosas que no esperaba ninguna de las dos posturas de arriba:

1. **`claude mcp list` no describe lo que hay en la sesión.** Un servidor puede figurar
   como conectado y no aportar ninguna herramienta al agente. Cualquiera que audite su
   propio contexto mirando esa lista está mirando el sitio equivocado.
2. **El cliente aplica a los MCP la misma *progressive disclosure* que a las skills.** Lo
   permanente es el nombre; el esquema se carga cuando se va a invocar. Es exactamente el
   mecanismo del [capítulo 04](../04-frontmatter.md), aplicado a otra cosa.

> Si esto se confirma, **el peaje permanente de un MCP se parece más al de una skill que
> al de un `CLAUDE.md`**, y el capítulo 00 está midiendo mal el coste que denuncia.

---

## 1. Qué se mide

Tres preguntas, en orden de coste creciente. **Las dos primeras no necesitan instalar
nada.**

### Medida A — El peaje permanente real

*¿Qué aparece en contexto de un servidor conectado, antes de usarlo?*

Observación directa, sin pasadas. Se registra qué se ve de `context7` en una sesión limpia
que no lo usa: nombres, esquemas, instrucciones del servidor.

**Ya se sabe que hay algo:** `context7` publica un bloque de instrucciones de servidor que
sí está presente. Falta cuantificarlo frente a lo que ocupa una `description` de skill.

### Medida B — La competencia por la atención

*Con capacidades irrelevantes disponibles, ¿el agente se desvía hacia ellas?*

**Predicción pre-registrada: no.** Y hay control gratis: los experimentos
[01](01-convenciones-pipeline.md) y [02](02-criterio-vs-lista.md) se ejecutaron con
`context7` conectado. Son **18 pasadas** sobre tareas de datos donde consultar
documentación externa era plausible.

Se revisan los diffs guardados y se cuenta en cuántas aparece una invocación a `context7`.

| | Predicción | Observado |
|---|---|---|
| Pasadas de 01 y 02 que invocan `context7` | 0 / 18 | *(pendiente)* |

> **Si sale 0/18, el coste de un MCP irrelevante es casi cero y hay que decirlo**, aunque
> debilite la tesis. Regla 6 del método.

### Medida C — El caso solapado (fase B, requiere instalar)

Es la única parte cara, y la única interesante.

*Cuando el agente tiene **dos caminos** para lo mismo —`gh` CLI, ya autenticado, y el MCP
de GitHub—, ¿cuál elige, y le sale mejor o peor?*

**Condiciones:** dos ramas, tres pasadas cada una, sesión limpia, prompt idéntico.

| | Herramientas | Skills |
|---|---|---|
| **A** | Sin MCP de GitHub | Las dos de Git |
| **B** | Con MCP de GitHub | Las mismas |

**Tarea:** una real y mixta, del tipo *abrir una PR desde una rama con cambios y comprobar
su estado*. Requisito de validez: **las dos ramas tienen que poder completarla**. Si solo
una puede, no se está midiendo la elección sino la capacidad, y el resultado no dice nada.

**Qué se registra por pasada:** si termina bien; qué ruta elige; y si la mezcla de ambas
produce algún fallo que ninguna produce sola.

---

## 2. Interpretación pre-registrada

Se escribe **ahora**, para no poder acomodarla al resultado.

| Resultado | Qué significa | Qué hay que cambiar en el material |
|---|---|---|
| B ≈ A en calidad, B gasta más | La tesis se sostiene, pero por competencia, no por peaje | Reescribir la frase del cap. 00 |
| B mejor que A | El MCP aporta de verdad sobre una CLI ya autenticada | **La tesis pierde su ejemplo principal.** Se publica igual |
| B peor que A | Tener dos caminos degrada la elección | Resultado nuevo, y el más útil de los tres |
| Empate absoluto | Un empate **ya es un resultado**: instalar no aportó | Se publica como tal |
| Medida B > 0/18 | La predicción falla y la sección de "competencia" del cap. 00 se queda sin apoyo | Corregir el capítulo |

> **El resultado que más incomoda es "B mejor que A", y es el que tiene más probabilidad
> de ser silenciado.** Queda escrito aquí para que no pueda serlo.

---

## 3. Riesgos del diseño, admitidos antes

- **La instalación es parte del coste.** No hay MCP de GitHub en esta máquina. Instalarlo
  y retirarlo cuenta, y se registra el tiempo real que llevó.
- **Una tarea de Git favorece a `gh`** por familiaridad del modelo. El resultado no
  generaliza a dominios sin CLI equivalente, y el capítulo tendrá que decirlo.
- **n=3 por rama** detecta diferencias grandes, no matices. Es el mismo n de los
  experimentos anteriores, y la misma limitación.
- **Fase B puede no ejecutarse.** Si se decide no instalar nada, este documento se cierra
  con A y B medidas y C declarada pendiente — no se rellena con razonamiento.

---

## Enmienda al pre-registro (antes de ejecutar)

La medida B estaba mal diseñada y se corrige **antes de ejecutarla**, que es el único
momento en que enmendar un pre-registro es legítimo.

**El error:** iba a contarse buscando `context7` en los 18 diffs guardados. Pero un diff
registra **el árbol de trabajo resultante**, no las herramientas que se invocaron. Habría
salido `0/18` de forma trivial, y se habría leído como confirmación de la predicción.

> **Un artefacto que no puede contener la señal tampoco puede refutarla.** Es la misma
> trampa que la regla de disparo del [capítulo 04](../04-frontmatter.md): un buen resultado
> no prueba que la skill se cargara.

**El artefacto correcto** son las transcripciones de sesión, que sí registran cada llamada
a herramienta. Es lo que se usa a partir de aquí.

---

## Resultados

### Medida A — El peaje permanente: **647 caracteres, en todas las sesiones**

Un servidor MCP conectado aporta al contexto permanente **dos cosas muy distintas**:

| Qué | Cuándo entra | Tamaño |
|---|---|---|
| Bloque de instrucciones del servidor | **Siempre**, en cada sesión | **647 caracteres** |
| Nombres de sus 2 herramientas | Siempre | Un nombre cada uno |
| **Esquemas** de esas herramientas | **Solo al ir a invocarlas** | — |

Comparado con lo que cuesta una skill instalada, que es su `description`:

| | Caracteres permanentes |
|---|---|
| `git-conventional-commits` | 276 |
| `pipeline-reglas-de-limpieza` | 338 |
| `github-workflow` | 518 |
| **Las tres skills juntas** | **1.132** |
| **`context7`, un solo servidor MCP** | **647** |

> **Un servidor MCP conectado cuesta más que cualquiera de las tres skills, y el 57 % de
> las tres juntas.** Y a diferencia de una `description`, ese texto **no lo escribes tú**:
> lo redacta quien publica el servidor, y le conviene ser persuasivo.

Ese bloque no es neutro. El de `context7` dice, literalmente, *"Use even when you think you
know the answer"* y *"Prefer this over web search"*. **Es instrucción de comportamiento, no
descripción de capacidad**, y está en contexto en cada turno de cada sesión.

### Medida B — La competencia: **0 invocaciones en 26 sesiones**

Transcripciones del 30 y 31 de julio de 2026, el periodo que cubre las 19 pasadas de los
experimentos 01 y 02.

| | Predicción | Observado |
|---|---|---|
| Sesiones que **invocan** `context7` | 0 | **0 / 26** |
| Sesiones que lo **mencionan** | — | 25 / 26 |

Las dos filas juntas son el resultado, no la primera sola:

> **25 de 26 sesiones «mencionan» `context7` y ninguna lo usa.** La mención es el bloque de
> instrucciones del propio servidor, presente en el prompt de sistema. Quien audite su
> contexto con un buscador de texto verá 25 aciertos y concluirá lo contrario de lo que
> pasa.

La única invocación real del proyecto entero está en una sesión del 29 de julio en la que
`context7` **era el tema de conversación**. Ninguna pasada de experimento lo tocó.

### Medida C — El caso solapado

**Rama A cerrada** (sin MCP). Rama B pendiente de instalar el servidor.

Condiciones: sesión limpia · 31 de julio de 2026 · commit `6e98ee7` · prompt del
[guion](04-guion-medida-c.md), sin nombrar ninguna herramienta.

| Pasada | ¿Termina bien? | Ruta elegida | Llamadas |
|---|---|---|---|
| A1 | Sí | `gh pr view 1 --json title,body,state,reviews,commits` | 1 |
| A2 | Sí | `gh pr view 1 --json title,body,commits,reviews,comments` | 1 |
| A3 | Sí | `gh pr view 1 --json title,body,files,reviews,author,mergedBy,state` | 1 |

**Ruta: 3/3 idéntica.** Las tres eligieron `gh pr view 1 --json`, una sola llamada, sin
tantear antes con otra cosa. Ni una miró `git log`, ni la web, ni preguntó. La variación
entre pasadas está solo en **qué campos pidieron**, no en el camino.

Y las tres contestaron bien lo que se preguntaba: **no hubo comentarios de revisión**
(verificado: `reviews: 0`, `comments: 0`).

> Esto fija el listón para la rama B: **A resuelve la tarea con una llamada y sin dudar.**
> Para que el MCP aporte algo tendrá que igualar eso, porque mejorarlo es difícil.

---

### Hallazgo **no pre-registrado**: la ruta era idéntica, las respuestas no

Esto **no estaba en el diseño** y por tanto **no puede usarse para comparar A con B**. Se
registra porque es más interesante que lo que sí se pre-registró.

Las tres pasadas ejecutaron prácticamente el mismo comando sobre el mismo objeto. Al
verificar sus respuestas contra la fuente:

| | Afirmación | Real | |
|---|---|---|---|
| A1 | 30 commits | 30 | ✅ |
| A2 | 28 commits | 30 | ❌ |
| A3 | No dio ninguna cifra de commits | — | — |

Y una segunda, del mismo tipo, en A1: al resumir el experimento 01 afirmó *"6/6 sin skill,
**0/6 correcto con skill**"*. Ese `0/6` **no existe en ningún sitio**. Es una cifra
inventada, presentada con la misma seguridad que la correcta que da dos líneas antes.

> **Misma herramienta, misma llamada, mismos datos: 2 de 3 metieron una cifra falsa.** El
> error no está en el acceso a la información. Está en el paso de resumirla.

Enlaza con lo medido en el [experimento 01](01-convenciones-pipeline.md), donde una skill
subió la cobertura del README al 100 % y creó afirmaciones falsas que antes no existían, y
con el [03](03-bajar-al-codigo.md), que existe justamente porque un recuento escrito a mano
se desvía del real.

**Lo que este hallazgo *no* autoriza a concluir:** que el MCP mejore o empeore eso. No es
lo que se está midiendo, n=3, y no estaba pre-registrado. Lo que sí deja es una pregunta
con forma de experimento propio: **¿el camino de acceso cambia la fidelidad del resumen, o
es independiente de él?**

---

## Qué aprendimos (con A y B; C sigue abierta)

**1. La hipótesis falló, y falló hacia el lado incómodo.** Se pre-registró que el coste
sería *"mucho menor de lo que dice la teoría"*. Son 647 caracteres permanentes por
servidor: más que cualquier skill de este repo. **El coste es real y es mayor de lo que yo
esperaba.**

**2. Pero el mecanismo que denuncia el [capítulo 00](../00-la-tesis.md) es el equivocado.**
No se paga por *"la definición de cada herramienta"* —los esquemas se cargan bajo demanda,
igual que el cuerpo de una skill—, se paga por **un bloque de instrucciones de
comportamiento que el servidor te impone**. La frase del capítulo acierta en la magnitud y
se equivoca en el porqué, y eso importa: **la conclusión práctica cambia.** Un servidor con
50 herramientas y un servidor con 2 pueden costar lo mismo; lo que decide es cuánto texto
haya escrito su autor.

**3. `claude mcp list` no dice lo que hay en tu contexto.** Declaraba cinco conectores
conectados que no aportan ninguna herramienta a la sesión. Auditar por ahí es auditar el
sitio equivocado.

**4. Buscar el nombre del servidor en tus sesiones da el resultado contrario al real.**
25/26 mencionan, 0/26 usan. La mención es el peaje; la invocación es el beneficio. Contar
la primera y llamarla la segunda es el error más fácil de cometer aquí.

> **El peaje se cobra en todas las sesiones. El beneficio, en ninguna.** Ese es el caso
> completo contra una capacidad instalada y no usada — y no hacía falta ninguna pasada
> nueva para medirlo.

---

## Cuándo NO hacer esto

- **Si usas el servidor de verdad**, esto no dice nada en su contra: 647 caracteres a
  cambio de documentación actualizada es un cambio excelente. Lo que se mide aquí es el
  caso en que **no** lo usas.
- **La medida A depende del servidor concreto.** Un servidor con un bloque de instrucciones
  de dos líneas cuesta mucho menos. No generalices el número: **generaliza el sitio donde
  mirar.**
- **La medida B es correlacional.** Que no se invocara en 26 sesiones de trabajo con datos
  no prueba que no sirva; prueba que en ese trabajo no aportó.
- **Sin la medida C no hay conclusión sobre solapamiento**, que es el caso más caro y el
  más frecuente en la práctica.

---

## Condiciones y reproducibilidad

- **Fecha del pre-registro y de las medidas A y B:** 31 de julio de 2026
- **Commit de partida:** `adc0d63`
- **Cliente:** Claude Code (VS Code), Windows 11
- **Servidor medido:** `context7`
- **Inventario MCP:** el de la sección 0
- **Modelos:** no aplica a A ni a B — se miden sobre registros ya existentes, no sobre
  pasadas nuevas. Aplicará a la medida C.

**Cómo repetirlo.** No hacen falta pasadas: se mide sobre lo que el cliente ya guarda.

1. **El peaje (A).** Busca el bloque de instrucciones del servidor en el prompt de sistema
   de cualquier transcripción de sesión y cuenta sus caracteres. Compáralo con la
   `description` de tus skills, que es su equivalente exacto.
2. **El uso (B).** En las transcripciones, cuenta **invocaciones**, no menciones: busca el
   nombre del servidor como nombre de herramienta en un `tool_use`, no como texto libre. La
   diferencia entre las dos cuentas fue aquí de 25 a 0.
3. **El contraste.** Compara la lista de servidores que declara el cliente con las
   herramientas realmente disponibles en la sesión. Si no coinciden, la lista no sirve para
   auditar.

> Los resultados con modelos generativos **varían entre ejecuciones**. Las medidas A y B no
> dependen de eso —son recuentos sobre registros— pero **sí dependen de la versión del
> cliente y del servidor**, que pueden cambiar el bloque de instrucciones sin avisar.
