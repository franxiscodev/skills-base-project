# Experimento 05 — La skill que nunca gana

> Método: [PLANTILLA.md](PLANTILLA.md).
> **Estado: pre-registrado, sin ejecutar.** Todo lo que hay por debajo de la hipótesis se
> escribió antes de lanzar una sola pasada. Si el diseño se enmienda, se enmienda aquí y
> con su motivo ([regla 11](PLANTILLA.md)).

**Hipótesis** *(escrita antes de ejecutar nada)*:

> `github-workflow` no se dispara porque **compite con `git-conventional-commits` y
> pierde**: comparten disparadores literales y la más corta gana. Si se retira la
> competidora, `github-workflow` empezará a dispararse con la misma `description` que hoy
> no le sirve de nada.

La hipótesis alternativa, también escrita por adelantado: **el problema es suyo y no de la
competencia** — su `description` nombra el territorio tres veces y no nombra el hueco, que
es el fallo que el [capítulo 04](../04-frontmatter.md) da por diagnosticado. En ese caso
retirar a la competidora no cambiará nada.

El diseño distingue las dos. Esa es toda su razón de ser.

---

## 0. La observación de partida

⚠️ **Esto no es un resultado del experimento.** Es el recuento retrospectivo que lo motiva,
hecho sobre sesiones que nadie había planificado como medición. Se registra aquí porque es
lo que hay que explicar, no como conclusión.

Sobre las **40 transcripciones** de sesión de este proyecto:

| Skill | `description` | Invocaciones |
|---|---|---|
| `pipeline-reglas-de-limpieza` | 338 caracteres | 13 |
| `git-conventional-commits` | 276 caracteres | 5 |
| **`github-workflow`** | **518 caracteres** | **0** |

La skill más cara del repositorio no se ha cargado nunca. Existe desde el 29 de julio de
2026 (`8bdba74`), es decir, durante toda la campaña de mediciones.

**No fue por falta de ocasión.** Once sesiones ejecutaron `git commit`; diez hicieron push
o crearon ramas. Y en las cinco donde `git-conventional-commits` sí se cargó, las cinco
hicieron además trabajo del territorio exclusivo de `github-workflow`:

| Sesión | `git commit` | push / rama | Skill cargada |
|---|---|---|---|
| `33565e41` | 3 | 2 | `git-conventional-commits` |
| `36721dd6` | 3 | 1 | `git-conventional-commits` |
| `533199cd` | 4 | 2 | `git-conventional-commits` |
| `d99f9288` | 3 | 1 | `git-conventional-commits` |
| `f865ca23` | 2 | 1 | `git-conventional-commits` |

**Cinco a cero en enfrentamiento directo.** No es azar entre dos opciones parecidas: es
sistemático.

### Qué contradice esto del material ya publicado

El [capítulo 04](../04-frontmatter.md) sostiene que el solapamiento entre las dos skills de
Git **se resolvió** partiéndolas por una frontera *"que se declara en los dos sitios"*, y
enseña el enunciado que empieza cada cuerpo. La tabla de fallos del mismo capítulo predice
que dos skills sin frontera se cargan *"a suertes"*.

Ninguna de las dos cosas resiste el recuento:

- La frontera está declarada **en los cuerpos**, y el cuerpo no se lee si la `description`
  no gana. Está escrita en el único sitio que no participa en la decisión.
- No salió *a suertes*. Salió 5-0.

Si el experimento confirma el mecanismo, ese pasaje del capítulo 04 hay que reescribirlo.

---

## El problema

Dos skills cubren Git en este repositorio y sus disparadores literales se pisan:

| Disparador | `git-conventional-commits` | `github-workflow` |
|---|---|---|
| "commit" / "commitear" | ✅ | ✅ |
| "push" | ✅ | ✅ |
| "rama" / "branch" | ✅ | ✅ |
| "merge" | ✅ | ✅ |
| "pull request" / "PR" | ❌ | ✅ |
| "me equivoqué de rama" | ❌ | ✅ |
| "conflicto" / "deshacer" | ❌ | ✅ |

La segunda cubre estrictamente más territorio, cuesta casi el doble y nunca se carga. Su
cuerpo —los checkpoints antes de commitear y antes de hacer push, el procedimiento de
recuperación, la comprobación de `ssh-add -l`— no ha llegado a leerse ni una vez.

---

## Cómo se cuenta el disparo

**Artefacto:** las transcripciones de sesión, buscando el registro literal de invocación:

```text
"name":"Skill","input":{"skill":"<nombre>"
```

### Validación del artefacto (regla 10)

Antes de fijar el recuento se comprobó que el registro **puede contener la señal**: la
misma búsqueda devuelve 13 invocaciones de `pipeline-reglas-de-limpieza` y 5 de
`git-conventional-commits`. Un artefacto que solo devolviera ceros no probaría nada.

⚠️ **No se cuenta por el nombre suelto.** Buscar `github-workflow` en las transcripciones
da decenas de resultados: son las sesiones donde se ha escrito *sobre* la skill —incluida
esta— no donde se ha usado. Es el mismo falso positivo que en el
[experimento 04](04-coste-de-un-mcp.md), y se evita exigiendo la forma completa de la
llamada.

---

## El diseño

Tres ramas, con la misma tarea y el mismo estado de partida. Lo único que cambia entre
ellas es qué hay en `.claude/skills/`.

| Rama | Qué hay instalado | Qué aísla |
|---|---|---|
| **A — control** | Las dos skills, tal como están hoy | Reproduce la observación bajo condiciones controladas |
| **B — sin competencia** | Solo `github-workflow` | ¿Pierde por competir, o no gana nunca? |
| **C — redacción** | Las dos, con la `description` de `github-workflow` reescrita | ¿Se arregla escribiendo mejor, sin quitar nada? |

`pipeline-reglas-de-limpieza` **no se toca en ninguna rama**. Es la variable de control: si
sigue comportándose igual mientras las otras se mueven, el cambio viene del cambio.

### El prompt principal

```text
Commitea los cambios que hay pendientes.
```

Territorio compartido, y literalmente el caso donde se midió el 5-0. **Tres pasadas por
rama**, sesión limpia, mismo commit de partida.

### La sonda diagnóstica

Una sola pasada, solo sobre la rama A:

```text
Me equivoqué de rama, estos commits tenían que ir en otra.
```

Es un disparador **literal y exclusivo** de `github-workflow`: aparece entrecomillado en su
`description` y no está en la otra skill. Si tampoco se carga aquí, la competencia no puede
ser la explicación y la hipótesis principal cae sin necesidad de la rama B.

⚠️ **Es diagnóstico, no resultado.** n=1 y prompt distinto: no entra en ninguna comparación.

### La `description` de la rama C

Se reescribirá siguiendo el criterio del [capítulo 04](../04-frontmatter.md), que hoy la
skill incumple en los tres puntos. Se redacta **antes** de ver los resultados de A y B, y
se pega aquí literalmente antes de ejecutar la rama C.

| Criterio del capítulo 04 | Hoy |
|---|---|
| Nombrar el hueco, no el territorio | ❌ nombra el territorio, tres veces |
| Disparadores literales | ✅ los tiene, y aun así no gana |
| Nombrar el fichero propio | ❌ no nombra ninguno |

---

## Tabla de interpretación, escrita antes de ejecutar

| A | B | C | Qué significa | Qué se hace |
|---|---|---|---|---|
| 0/3 | **3/3** | — | **Pierde por competir.** La hipótesis se confirma | Reescribir el capítulo 04: la frontera hay que declararla en la `description`, no en el cuerpo |
| 0/3 | **0/3** | 3/3 | El problema era **su redacción**, no la competencia | Confirma el criterio del capítulo 04 con un caso negativo propio |
| 0/3 | 0/3 | 0/3 | No se arregla desde el frontmatter | La skill sobra: **se borra**, y eso es el resultado |
| 3/3 | — | — | La observación no se reproduce en condiciones controladas | Se registra el fallo y se investiga qué distinguía a las 40 sesiones |

**Y la decisión que se toma pase lo que pase:** una `description` de 518 caracteres que
gana 0 de 3 en su propio territorio no se queda como está. La única pregunta abierta es si
se reescribe o se borra.

> Se pre-registra también esto, porque es donde el método se pone a prueba de verdad: la
> rama que acabe ganando puede ser *borrar la skill*, y ese resultado se publica igual.

---

## Lo que este experimento NO mide

- **Si el cuerpo de `github-workflow` es bueno.** Nunca se ha leído; puede ser excelente e
  irrelevante. Aquí solo se mide si llega a leerse.
- **Si el orden o la longitud son la causa.** Con dos skills no se puede separar "más
  corta gana" de "mejor escrita gana": son la misma diferencia en esta muestra.
- **Nada sobre otros modelos.** Las pasadas irán con un solo modelo, indicado abajo.

---

## Condiciones y reproducibilidad

- **Fecha del pre-registro:** 1 de agosto de 2026
- **Commit de partida:** por fijar antes de la primera pasada, verificado con `git log`
- **Modelo:** por fijar
- **Observación de partida:** 40 transcripciones en
  `~/.claude/projects/c--APRENDER-ClaudeCode-base-project/`
- **Diffs:** cada pasada guarda el suyo en [`diffs/`](diffs/) como `exp05-<rama>-<n>.diff`

> Los resultados con modelos generativos **varían entre ejecuciones**. Este registro
> documenta lo que ocurrió en las condiciones indicadas, no una garantía. Si al repetirlo
> obtienes algo distinto, eso también es información: anótalo.
