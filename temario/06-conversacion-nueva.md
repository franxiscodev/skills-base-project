# 06 — Cuándo abrir una conversación nueva

> La misma tesis del [capítulo 00](00-la-tesis.md), aplicada dentro de la sesión.

## La pregunta

> *"¿Sigo en esta conversación o abro una nueva?"*

Parece una cuestión de comodidad y no lo es: es **economía de contexto en el único sitio
donde tú decides en tiempo real**. Todo lo demás —qué skills instalas, qué va en memoria—
se decide una vez. Esto se decide varias veces al día.

Este capítulo no tiene experimento propio. Lo que tiene es un criterio y una prueba, y
ambos se comprueban solos la primera vez que los aplicas.

---

## Una conversación acumula dos cosas, y solo una estorba

| Lo que se acumula | Dónde vive | Al cerrar la sesión |
|---|---|---|
| **Trabajo hecho** | En ficheros, commits, tests | **No se pierde** |
| **Deliberación** | Solo en la conversación | Se pierde |

La deliberación es todo lo que se probó y se descartó, los caminos que no se tomaron, las
diez versiones de una frase. Fue necesaria para llegar donde estás, y **a partir de ahí
compite por atención en cada turno** aunque ya no venga a cuento.

De ahí el criterio, que es más corto de lo que la gente espera:

> **Se abre sesión nueva cuando cambia la tarea, no cuando la conversación se hace larga.**

La longitud no es el problema. **La mezcla de tareas sí.** Media sesión discutiendo una
cosa y media escribiendo código deja la primera mitad como ruido puro para todo lo que
venga después.

---

## El anti-patrón

> *"Sigo aquí porque el agente ya sabe de qué hablamos."*

Eso es depender de un estado que **no existe en ningún sitio**. Y va a desaparecer igual:
por límite de contexto, por un cierre accidental, o porque el sistema resuma la
conversación automáticamente cuando crezca.

Cuanto más cómodo te resulte seguir ahí, más grande es la deuda: significa que hay
decisiones vivas que solo están en el chat.

---

## La prueba que lo convierte en algo útil

Esta es la parte que casi nadie hace, y es la mejor de todo el capítulo.

> **Abrir una sesión nueva audita tu propio sistema de persistencia.**

- Arranca bien solo con la memoria y los documentos → **tu sistema funciona**.
- Arranca mal → acabas de encontrar, con nombre y apellidos, **exactamente lo que no
  estabas guardando**.

> **El coste de cerrar una conversación mide la calidad de lo que escribiste.**

Es la única métrica de este material que no necesita ni una pasada de medición: es gratis
y la tienes cada vez que cierras.

Y encaja con todo lo anterior. Si al abrir en frío tienes que volver a explicar una
convención, esa convención pedía un sitio: el código, un test, una skill o la memoria
([capítulo 02](02-arbol-de-decision.md)).

---

## Lo que hay que hacer antes de cerrar

Una sola cosa, y lleva menos de un minuto:

> **Vuelca lo decidido que solo esté en la conversación.**

No el resumen de lo que pasó — eso está en los commits. Solo **las decisiones vivas**: lo
acordado que todavía no ha llegado a ningún fichero. Dos líneas en el sitio que les toque.

Si al intentarlo descubres que son quince cosas, no es que la sesión fuera productiva: es
que llevas quince decisiones sin sitio.

---

## Cómo se ve esto en el material que estás leyendo

Este temario salió de una campaña de medición de varias decenas de pasadas, y el criterio
aparece dos veces, en dos escalas distintas.

**Dentro del método.** Cada pasada exige **sesión limpia**
([plantilla](experimentos/PLANTILLA.md)). No es ceremonia: si el agente ya ha visto la
tarea, ya no estás midiendo lo que crees. Ahí la sesión nueva no es higiene, **es la
condición de validez del resultado**.

**Y a lo bruto.** La conversación que produjo esta campaña se pasó de largo y hubo que
resumirla a mitad. Sobrevivió lo que estaba escrito —los experimentos, los diffs
guardados, los commits— y se perdió la deliberación. El trabajo continuó sin problema
**precisamente porque la regla 7 de la plantilla obliga a guardar el diff**: sin ella, la
mitad de las mediciones se habrían evaporado con el resumen.

> **La disciplina de escribir las cosas fuera de la conversación no es orden: es lo que
> hace que la conversación pueda terminar sin coste.**

---

## El ejercicio

La próxima vez que termines algo, **cierra la sesión y abre otra en frío** para lo
siguiente.

Anota qué has tenido que volver a explicar. Esa lista es, exactamente, lo que te falta por
escribir — y no hay ninguna otra forma de obtenerla.

---

## Lo que se lleva a cualquier herramienta

1. **Cambia la tarea → sesión nueva.** La longitud no es el criterio.
2. **La deliberación compite por atención** mucho después de haber servido.
3. **"El agente ya sabe de qué hablamos" es una deuda**, no una ventaja.
4. **Abrir en frío audita lo que has guardado.** Gratis, y no falla.
5. **Antes de cerrar, vuelca solo las decisiones vivas.**
