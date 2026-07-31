# 03 — Anatomía de una skill

> **Evidencia:** [experimento 01](experimentos/01-convenciones-pipeline.md) ·
> [experimento 02](experimentos/02-criterio-vs-lista.md)
>
> Este capítulo trata **el cuerpo** de la skill. El `description`, que es lo único que
> está siempre en contexto y lo que decide si la skill llega a existir, tiene capítulo
> propio: el [04](04-frontmatter.md).

## El fichero

```
.claude/skills/<nombre>/
  SKILL.md          ← frontmatter + cuerpo
  references/       ← opcional: lo que solo hace falta a veces
    comandos.md
```

El formato es trivial y no es lo interesante. Lo interesante es que **cada decisión de
redacción cambia el resultado de forma medible**, y este capítulo va de esas.

El ejemplo de trabajo es la skill de este repositorio,
[`pipeline-reglas-de-limpieza`](../.claude/skills/pipeline-reglas-de-limpieza/SKILL.md):
96 líneas, escrita después de medir, reescrita después de volver a medir.

---

## Regla 1 — Escribe criterio de terminado, no lista de sitios

La más importante, y la que tiene el número más grande detrás.

La primera versión decía *"actualiza el README, el docstring del módulo y los vecinos"*.
Resultado: **6 de 6 tocaron el README y 0 de 6 lo dejaron verdadero.**

> **Una regla escrita como tarea se cumple como tarea.** Se ejecuta —también donde no
> toca— y termina cuando la tarea está hecha, no cuando el trabajo está bien.

Se reescribió el mismo contenido como criterio, sin tocar nada más:

| | Antes (lista) | Ahora (criterio) |
|---|---|---|
| §1 | "Actualiza el README, el docstring y los vecinos" | "Que no quede ni una frase falsa. **Búscalas, no las recuerdes**" |
| §2 | "Escribe un test de que no toca lo que no debe" | "**Rompe la regla a propósito** y comprueba que el test se pone rojo" |

| Deja el README verdadero | Lista | Criterio |
|---|---|---|
| Modelo grande | 0/3 | **3/3** |
| Modelo pequeño | 0/3 | 1/3 |

Mismo contenido, mismo coste de contexto, y en el modelo capaz la diferencia es todo.

**Por qué funciona:** un criterio decide también en los casos que la lista no enumera.
Y la lista nunca puede estar completa — si pudiera, no harías falta tú.

Se vio en algo que la lista jamás habría incluido: en una pasada, el agente corrigió una
frase falsa **que no venía de su cambio** (`__init__.py` decía *"Cuatro pasos"* sobre un
diagrama de cinco, llevaba mal desde el principio). Ninguna instrucción menciona ese
fichero.

> **Una skill que hace buscar encuentra cosas que no le tocaban.** Es un efecto lateral
> que no se puede pedir directamente: sale de haber escrito el criterio en vez del sitio.

**Cuándo sí conviene la lista:** cuando de verdad es cerrada —tres sitios fijos que no
van a cambiar— o cuando el criterio no se puede comprobar. *"Deja el README verdadero"*
vale porque se verifica con un `grep`. Un criterio que no se puede comprobar es una buena
intención.

Y la lista puede convivir con el criterio si dice lo que es. En la skill del repo:

> Empieza por el `README.md`, el docstring del módulo y los de las reglas vecinas — pero
> eso es **por dónde empezar a buscar**, no la lista de lo que hay que mirar.

---

## Regla 2 — Pregúntate cuál es la forma más barata de cumplir tu regla

Porque es la que vas a obtener.

Pasó dos veces, con dos reglas distintas:

| Lo que pedía la regla | La forma más barata que la cumple |
|---|---|
| *"Actualiza el README"* | Tocarlo. Aunque lo que escribas sea mentira — 3 de 6 metieron una afirmación falsa |
| *"Rompe la regla y comprueba que el test falla"* | Falsar **por un solo lado** del límite. Las 3 pasadas del modelo pequeño, el mismo test insuficiente |

> **Falsar por un solo lado da más confianza que no falsar, con la misma cobertura.** El
> sello de "verificado" no lo puso el rigor: lo puso haber pensado en un borde.

De ahí la regla:

> **Toda instrucción que añades a una skill se ejecuta también de la forma más barata que
> la cumpla.** Antes de escribirla, imagina esa forma. Si te vale, la regla está bien. Si
> no, falta acotarla.

Acotar es concreto. La §2 de la skill no dice "escribe un caso negativo": dice **qué fila
elegir**.

> Para elegir la fila: la que está **pegada al límite y del lado que se queda**. Una fila
> cualquiera que la regla no toca no sirve — de esas hay infinitas y ninguna demuestra
> nada.

---

## Regla 3 — Di lo que la skill **no** dice, y por qué

La sección que más extraña a quien la ve por primera vez es la primera:

> ## Lo que esta skill NO dice, y por qué
>
> **No describe cómo se escribe la regla.** Ni la firma, ni que devuelva `Recuento`, ni
> que se encadene, ni que lleve test. Eso ya lo enseña el propio código […] Se midió —
> seis intentos, dos modelos, **seis aciertos sin una sola desviación**.

Cuesta contexto y no da ninguna instrucción. Está ahí por tres razones:

1. **Impide que la skill engorde.** Dentro de seis meses alguien va a querer añadir "y
   acuérdate de devolver `Recuento`". Esa sección contesta antes de que lo escriba.
2. **Enseña el criterio a quien la lea.** Una skill también la leen personas.
3. **Es la parte auditable.** Deja por escrito qué se midió y qué se decidió.

> **Una skill sin fronteras declaradas crece hasta que deja de dispararse por lo que
> importaba.**

---

## Regla 4 — Pon el número al lado de la regla

Cada sección de la skill del repo termina igual:

> Medido: **3 de 6** lo detectaron sin que se lo pidieran.

No es adorno. Hace tres cosas:

- **Justifica que esa regla esté ahí.** Las que salían 6/6 no están.
- **Da la señal para borrarla.** Si mañana sale 6/6 sin la skill, ese punto sobra.
- **Convence.** Una instrucción con un número al lado se sigue distinto que una afirmada
  a pelo — y esto vale igual para el modelo y para tu equipo.

---

## Regla 5 — El ejemplo nunca puede ser el caso con el que vas a medir

Esta salió de un error mío, y por eso está.

La primera versión de la skill ilustraba las reglas con el mismo caso que después se usó
para medirla. Las tres pasadas repitieron los tres ejemplos, literalmente. La pasada
quedó **anulada**: no medía si la skill funcionaba, medía si el modelo sabe copiar.

> **La skill no puede usar como ejemplo el caso con el que se va a medir.**
> ([PLANTILLA](experimentos/PLANTILLA.md), regla 9)

El ejemplo se cambió a una regla lejana —`test_imputar_ciudad_no_descarta_la_venta`— y en
la medición buena **las seis pasadas eligieron un límite distinto**: el importe negativo,
el céntimo, la devolución con importe positivo.

> **La prueba de que no hubo copia es la variación.** Si todas hacen lo mismo que tu
> ejemplo, no has medido nada.

---

## Regla 6 — Ponle fecha de caducidad

La última sección de la skill:

> ## Cuándo dejar de usar esta skill
>
> Si el patrón de `limpiar.py` cambia de forma —si las reglas dejan de ser funciones
> hermanas y pasan a ser clases o configuración— **esta skill deja de valer y hay que
> rehacer la medición**. Lo que aquí se afirma no es una opinión: es el resultado de un
> experimento con condiciones concretas, y esas condiciones caducan.

Una skill envejece **en silencio**: nadie revisa lo que no falla. Escribir la condición
de caducidad dentro es lo único que convierte "esto ya no aplica" en algo detectable por
quien la lee, en vez de por quien la escribió y ya no se acuerda.

---

## La forma del cuerpo

Con las seis reglas puestas, la anatomía queda así:

| Parte | Para qué |
|---|---|
| **Qué NO dice, y por qué** | Frontera. Impide que crezca |
| **Dos o tres secciones**, una por punto medido | El contenido. Criterio, no lista |
| **`- [ ]` en cada punto accionable** | Se puede recorrer y se puede comprobar |
| **`> Medido: N de 6`** al cierre de cada sección | Justifica y da la señal de borrado |
| **Checklist final** | Recorrido único al terminar |
| **Cuándo dejar de usarla** | Caducidad explícita |

**Longitud:** las tres de este repo van de 96 a 183 líneas. Lo que solo hace falta a veces
—tablas de comandos, casos de recuperación— sale a `references/`, que **no entra en
contexto hasta que la skill lo pide**. Esa es la parte de "economía de contexto" que se
juega dentro del fichero: un cuerpo corto que decide, y el detalle a un salto de
distancia.

---

## El ejercicio

Coge una skill tuya y haz solo dos cosas:

1. Subraya cada regla que sea **una lista de sitios**. Reescríbela como criterio.
2. Para cada regla, escribe al lado **la forma más barata de cumplirla**. Si esa forma no
   te vale, la regla está sin acotar.

No hace falta más. Con esas dos pasadas se arregla la mayoría de lo que falla en una
skill escrita a ojo.

---

## Lo que se lleva a cualquier herramienta

1. **Criterio de terminado, no lista de sitios.** 0/3 → 3/3 con el mismo contenido.
2. **Vas a obtener la forma más barata de cumplir lo que pides.** Acótala.
3. **Declara lo que la skill no cubre**, o crecerá hasta no servir.
4. **Cada regla, con su número.** El número es también la condición para borrarla.
5. **El ejemplo no puede ser el caso de prueba.**
6. **Escribe dentro cuándo deja de valer.**
