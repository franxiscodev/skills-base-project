# Experimento 04 — Qué cuesta de verdad una capacidad instalada

> **PRE-REGISTRO.** Este documento se escribe **antes de ejecutar ninguna pasada**.
> Lo que hay debajo de "Resultados" está vacío a propósito. Si al terminar algo no
> coincide con lo pre-registrado, se anota la discrepancia; no se reescribe la hipótesis.

**Hipótesis:** en este cliente, un servidor MCP conectado y no usado cuesta mucho menos
de lo que dice la teoría —porque las definiciones se cargan bajo demanda— y el coste real
no está en el peaje permanente sino en **el momento en que dos caminos hacen lo mismo**.

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

## Resultados

*(Vacío. Se rellena al ejecutar, con la salida sin retocar.)*

---

## Qué aprendimos

*(Vacío hasta tener las medidas.)*

---

## Cuándo NO hacer esto

*(Vacío hasta tener las medidas. Sin esta sección el capítulo estaría vendiendo.)*

---

## Condiciones y reproducibilidad

- **Fecha del pre-registro:** 31 de julio de 2026
- **Commit de partida:** `adc0d63`
- **Modelos:** por fijar al ejecutar
- **Cliente:** Claude Code (VS Code), Windows 11
- **Inventario MCP al pre-registrar:** el de la sección 0

> Los resultados con modelos generativos **varían entre ejecuciones**. Este registro
> documentará lo que ocurrió en las condiciones indicadas, no una garantía.
