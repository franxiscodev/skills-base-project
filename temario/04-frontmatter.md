# 04 — El frontmatter: lo que decide si tu skill existe

> **Evidencia:** [experimento 01](experimentos/01-convenciones-pipeline.md) ·
> [experimento 02](experimentos/02-criterio-vs-lista.md)

## Las cuatro líneas que se leen siempre

```yaml
---
name: pipeline-reglas-de-limpieza
description: Qué hay que actualizar además del código al añadir, cambiar o quitar una
  regla de limpieza del pipeline de datos — los sitios que no se ven desde limpiar.py.
  Usar cuando se pida "añade una regla", "descarta las filas que...", "filtra las
  ventas...", "quita esa regla", "cambia el criterio de limpieza", o al tocar
  src/pipeline/limpiar.py.
---
```

De toda tu skill, **esto es lo único que está permanentemente en contexto**. El cuerpo
—las 96 líneas del capítulo anterior— no existe para el agente hasta que decide cargarlo,
y esa decisión la toma leyendo estas líneas y nada más.

> **El cuerpo decide qué hace tu skill. El `description` decide si tu skill llega a
> pasar.**

Es también el reparto de coste que hace que las skills sean baratas: pagas la descripción
siempre y el contenido solo cuando hace falta. Diez skills bien descritas cuestan menos
que un `CLAUDE.md` mediano.

---

## Lo que se midió

En este repositorio, `description` se disparó:

| | Pasadas | Disparos |
|---|---|---|
| Experimento 01 (Opus 5 + Haiku 4.5) | 6 | **6** |
| Experimento 02 (Haiku 4.5 + Opus 5) | 6 | **6** |

**12 de 12, con los dos modelos, y siempre antes de leer ningún fichero.** La misma
`description` no se tocó entre los dos experimentos precisamente para no meter una segunda
variable: es el punto más estable de toda la medición.

### Cómo se sabe que se disparó de verdad

Esta parte importa más que el número, porque es donde casi todo el mundo se engaña.

**Un buen resultado no prueba que la skill se cargara.** El agente puede haber hecho el
trabajo bien por su cuenta — de hecho, en el experimento 01 hizo bien 4 de las 7 cosas sin
skill ninguna.

Y el indicador de la interfaz tampoco basta del todo: dice que se cargó, no que se usara.

> **Busca una acción que no tenga otra causa posible.**

Aquí fue esta: **las seis pasadas leyeron `generar_datos.py`**. El prompt no lo menciona,
la tarea no lo necesita para funcionar, y el único sitio donde se pide mirarlo es la §3 de
la skill. Eso prueba más que cualquier indicador.

---

## Anatomía de un `description`

Tres cosas, en este orden.

### 1. Qué resuelve, no qué es

> *"**Qué hay que actualizar además del código** al añadir, cambiar o quitar una regla de
> limpieza"*

Si dijera *"convenciones del pipeline de datos"* estaría describiendo **el tema**. Y el
tema ya lo cubre el código: un agente que va a editar `limpiar.py` no tiene ninguna razón
para pensar que le falta información sobre las convenciones, porque las tiene delante.

El `description` tiene que nombrar **el hueco**, no el territorio.

> Prueba rápida: si tu descripción vale igual para el fichero fuente que para la skill, no
> distingue nada.

### 2. Disparadores literales, en el idioma en que se pide

> *"Usar cuando se pida **"añade una regla", "descarta las filas que...", "filtra las
> ventas...", "quita esa regla", "cambia el criterio de limpieza"**"*

Entrecomillados y tal como los escribiría la persona. Y **en su idioma**: si tu equipo
pide las cosas en español, los disparadores van en español, aunque el resto de la skill
esté en inglés.

Fíjate en que cubren las tres direcciones —**añadir, cambiar y quitar**—. Una skill que
solo se dispara al añadir no llega el día que alguien borra una regla, que es justo cuando
más frases quedan falsas.

### 3. El fichero

> *"o al tocar `src/pipeline/limpiar.py`"*

La vía de escape para cuando la petición está redactada de una forma que no anticipaste.
Alguien puede pedir *"que las ventas fantasma no cuenten"* sin usar ninguna de tus
palabras — pero va a acabar abriendo ese fichero igual.

**Si tu skill tiene un fichero o directorio propio, nómbralo.** Es el disparador más
robusto que existe, porque no depende de cómo se redacte la petición.

---

## El `name`

Va en minúsculas con guiones y coincide con el nombre de la carpeta. Descríbelo por el
**caso**, no por la tecnología: `pipeline-reglas-de-limpieza` dice cuándo aplica;
`duckdb-sql` no diría nada.

---

## Cuando dos skills se pisan

En este repo hay dos skills de Git y podrían haber competido en cada commit. Se resolvió
partiéndolas por una frontera que se declara **en los dos sitios**:

| Skill | Cubre |
|---|---|
| `git-conventional-commits` | **El contenido del mensaje** |
| `github-workflow` | **Dónde va el trabajo y qué pasa después**: rama, comprobaciones, PR, releases, recuperación |

Y cada cuerpo empieza remitiendo a la otra:

> Esta skill cubre el **contenido del mensaje** de commit. El **flujo de trabajo** […] lo
> cubre la skill `github-workflow`.

> **Dos skills que se solapan no se arreglan en el `description`: se arreglan decidiendo
> la frontera y escribiéndola en las dos.** Si no puedes enunciarla en una frase, es una
> sola skill.

Ambas se dispararon con Haiku y produjeron mensajes impecables — **las skills funcionan
con modelos modestos**. Lo que ninguna de las dos cubre es *decidir si tocaba commitear*,
que es juicio y no formato, y eso se vio en las mediciones: Haiku commiteó sin que se lo
pidieran en 3 de 6 pasadas.

---

## Los fallos típicos

| Fallo | Por qué no dispara |
|---|---|
| *"Buenas prácticas de Python"* | No hay ningún momento concreto en que aplique |
| Describir el tema, no el hueco | Compite con lo que el código ya enseña |
| Disparadores en un idioma distinto al de las peticiones | Nadie los va a escribir |
| Solo el caso de "añadir" | No llega al cambiar ni al borrar |
| Dos skills sin frontera declarada | Se carga cualquiera de las dos, a suertes |

Y el diagnóstico que sirve para todos: **si una skill no se dispara nunca, sospecha del
`description` antes que del cuerpo.** El cuerpo puede ser perfecto y no llegar a leerse.

---

## El ejercicio

Coge tus skills y, para cada una, escribe **tres peticiones reales** tal como las
teclearía alguien de tu equipo — con sus palabras, no con las tuyas.

Después mira si tu `description` las cubre. Lo normal es descubrir que cubre la forma en
que **tú** pides las cosas, que no es la que usa nadie más.

---

## Lo que se lleva a cualquier herramienta

1. **El `description` es lo único que se paga siempre.** Y lo único que decide.
2. **Nombra el hueco, no el tema.**
3. **Disparadores literales, en el idioma real**, y en las tres direcciones: añadir,
   cambiar, quitar.
4. **Si hay un fichero, nómbralo.** Es el disparador que no depende de la redacción.
5. **Prueba el disparo con una acción sin otra causa posible**, no con el resultado.
