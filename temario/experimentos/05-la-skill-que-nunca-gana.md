# Experimento 05 — La skill que nunca gana

> Método: [PLANTILLA.md](PLANTILLA.md).
> **Estado: cerrado sin pasadas controladas.** El pre-registro con tres ramas y diez
> pasadas se escribió, se commiteó (`7c552c6`) y **se canceló antes de ejecutar**. El
> motivo está abajo, en «Por qué no se ejecutó».

**Hipótesis** *(escrita antes de decidir nada, y conservada)*:

> `github-workflow` no se dispara porque **compite con `git-conventional-commits` y
> pierde**: comparten disparadores literales y la más corta gana.

**Sigue sin comprobarse.** No se sabe si pierde por competir o por estar mal escrita, y este
experimento ya no va a averiguarlo. Lo que sí quedó medido es que no se dispara.

---

## El recuento

Sobre las **40 transcripciones** de sesión de este proyecto, contando invocaciones reales y
no menciones del nombre:

| Skill | `description` | Invocaciones |
|---|---|---|
| `pipeline-reglas-de-limpieza` | 338 caracteres | 13 |
| `git-conventional-commits` | 276 caracteres | 5 |
| **`github-workflow`** | **518 caracteres** | **0** |

La `description` más cara del repositorio, y la única que nunca llegó a cobrarse. Existía
desde el 29 de julio de 2026 (`8bdba74`): toda la campaña.

**No fue por falta de ocasión.** Once sesiones ejecutaron `git commit`; diez hicieron push
o crearon ramas. Y en las cinco donde `git-conventional-commits` sí se cargó, las cinco
hicieron además trabajo del territorio **exclusivo** de la que perdió:

| Sesión | `git commit` | push / rama | Skill cargada |
|---|---|---|---|
| `33565e41` | 3 | 2 | `git-conventional-commits` |
| `36721dd6` | 3 | 1 | `git-conventional-commits` |
| `533199cd` | 4 | 2 | `git-conventional-commits` |
| `d99f9288` | 3 | 1 | `git-conventional-commits` |
| `f865ca23` | 2 | 1 | `git-conventional-commits` |

**Cinco a cero en enfrentamiento directo.** No es azar entre dos opciones parecidas.

### Cómo se contó

Artefacto: las transcripciones, buscando la forma literal de la llamada.

```bash
grep -o '"name":"Skill","input":{"skill":"[a-z-]*"' *.jsonl
```

⚠️ **No se cuenta por el nombre suelto.** Buscar `github-workflow` da decenas de
resultados: son las sesiones donde se ha escrito *sobre* la skill, no donde se ha usado. Es
el mismo falso positivo que en el [experimento 04](04-coste-de-un-mcp.md).

Y el artefacto se validó antes de contar ([regla 10](PLANTILLA.md)): la misma búsqueda
devuelve 13 y 5 para las otras dos skills. Un registro que solo diera ceros no probaría
nada.

---

## Por qué no se ejecutó

El diseño era correcto y la decisión de no ejecutarlo también. Las dos cosas a la vez:

> **Diez pasadas controladas habrían sido peor evidencia que las cuarenta sesiones reales
> que ya había.** Sesiones no planificadas como medición, con trabajo de verdad, sin nadie
> intentando que saliera nada.

Lo que las diez pasadas habrían añadido es el **mecanismo** —competencia o redacción— y el
mecanismo no cambiaba la decisión. Con 0 de 40, la skill se toca igual.

Se canceló además por un motivo que conviene decir en voz alta, porque le pasa a cualquiera
que monte un método así:

> **La campaña de mediciones se estaba convirtiendo en el proyecto.** Medir tiene el mismo
> problema que instalar: cada medición individual parece barata y ninguna se cuenta contra
> el total.

Es exactamente la tesis del material aplicada al material. Se anota como coste real, no
como anécdota.

---

## Qué se hizo con el resultado

**Se borró la skill.** Y se pudo borrar con riesgo cero por la misma razón por la que había
que borrarla:

> **Quitar algo que nunca se ejecutó no puede romper nada.** El 0 de 40 es a la vez el
> motivo del borrado y la garantía de que es seguro.

Su cuerpo era bueno —checkpoints antes de commitear y de hacer push, recuperación de
errores, la comprobación de `ssh-add -l` antes de una operación remota— y da igual: no se
leyó ni una vez. Sigue en el historial de Git (`8bdba74`) si alguna vez hace falta.

> **Una skill que no se dispara no es una skill a medias: es texto que pagas siempre y no
> recibes nunca.** No hay término medio, porque el cuerpo o se carga entero o no se carga.

---

## Qué obligó a corregir del material publicado

El [capítulo 04](../04-frontmatter.md) daba por resuelto el solapamiento entre las dos
skills de Git *"partiéndolas por una frontera que se declara en los dos sitios"*, y su tabla
de fallos predecía que dos skills sin frontera se cargan *"a suertes"*.

Ninguna de las dos cosas resiste el recuento:

- La frontera estaba declarada **en los cuerpos**. El cuerpo no se lee si la `description`
  no gana: estaba escrita en el único sitio que no participa en la decisión.
- No salió *a suertes*. Salió 5-0.

> **Una frontera entre skills solo existe si está en las `description`.** Todo lo demás es
> documentación para un lector que no llega.

---

## Qué aprendimos

1. **Una skill puede costar todos los días y no aportar ningún día.** 518 caracteres
   permanentes, 0 invocaciones, 40 sesiones.
2. **La frontera entre dos skills se declara donde se decide**, y se decide en la
   `description`.
3. **Quitar lo que nunca se disparó es la única poda gratis que existe.** Si dudas de si
   una skill sirve, mira si se ha cargado alguna vez antes de discutir su contenido.
4. **Cuenta las mediciones como cuentas las instalaciones.** Un método que obliga a medir
   antes de añadir también puede engordar hasta sustituir al trabajo.
5. **Un pre-registro cancelado no es un experimento fallido.** Es una decisión de coste, y
   se publica con su motivo — o el registro solo enseña lo que salió bien.

## Cuándo NO hacer esto

- **Cuando no tengas el histórico.** El 0 de 40 vale porque había cuarenta sesiones reales
  detrás. Con tres, el experimento controlado sigue siendo el camino.
- **Cuando la skill sea nueva.** Que no se haya disparado todavía no dice nada; puede que
  no haya habido ocasión. Aquí las hubo once.
- **Cuando la decisión sí dependa del mecanismo.** Si el plan fuera *reescribir* en vez de
  *borrar*, saber si pierde por competir o por redacción es justo lo que necesitas, y
  entonces las diez pasadas se pagan.

## Condiciones y reproducibilidad

- **Fecha:** 1 de agosto de 2026
- **Fuente:** 40 transcripciones en
  `~/.claude/projects/c--APRENDER-ClaudeCode-base-project/`
- **Pre-registro cancelado:** commit `7c552c6`, recuperable con
  `git show 7c552c6:temario/experimentos/05-la-skill-que-nunca-gana.md`
- **Cómo repetirlo:** contar invocaciones con la forma literal de la llamada, nunca por el
  nombre.

> Este experimento **no tiene diffs**: no generó pasadas. La evidencia son las
> transcripciones, que no viajan con el repositorio porque contienen trabajo real. El
> recuento es reproducible con el comando de arriba sobre las propias.
