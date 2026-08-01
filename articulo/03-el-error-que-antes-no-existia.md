# Entrega 3 — La escribí igual, y creó un error que antes no existía

> **Formato: ARTÍCULO** (nativo de LinkedIn) ·
> **Base:** [exp 01](../temario/experimentos/01-convenciones-pipeline.md)

El hallazgo más incómodo de toda la serie, y el que justifica el formato largo. Un solo
número: **6 tocados, 0 correctos**.

---

## Para pegar

### Subí la cobertura del 17 % al 100 %. Y ese fue el problema

En la entrega anterior conté que medí una skill antes de escribirla y resultó que no hacía
falta: el agente ya respetaba la convención leyendo el código, tres de tres.

La escribí igual.

No entera: acotada a los tres puntos donde sí hubo fallos en las pasadas sin ella. Uno de
esos tres era el más obvio de todos, el que cualquiera habría escrito.

> *"Actualiza el README cuando añadas una regla."*

Antes de la skill, solo **1 de 6** pasadas tocaba el README. Con la skill, **6 de 6**. La
instrucción funcionó exactamente como se le pidió.

Entonces fui a mirar si lo que habían escrito era cierto.

**Cero de seis.**

Seis README tocados. Ninguno correcto. Trazas de ejecución inventadas, cifras que no
cuadraban con la salida real del pipeline, una fila de ejemplo que no existía.

### El dato que lo cambia todo

Lo grave no es el 0 de 6. Es esto:

**Antes de la skill, ese error no existía.**

No porque el agente fuera más cuidadoso sin ella, sino por una razón mucho más tonta:
**cinco de las seis pasadas ni siquiera abrían el fichero.** No se puede mentir en un
documento que no tocas.

| | Sin skill | Con skill |
|---|---|---|
| Toca el README | 1 de 6 | 6 de 6 |
| Mete una afirmación falsa | **0 de 6** | **3 de 6** |

La skill hizo su trabajo, subió el número que le pedí que subiera, y **creó una clase de
error que el sistema no tenía**. Documentación falsa donde antes había documentación
desactualizada — que es peor, porque la desactualizada al menos envejece de forma visible.

Si solo cuentas aciertos, esto es invisible. Y contar solo aciertos es lo que hace todo el
mundo, porque para ver lo otro hay que haber medido el "antes".

### Por qué pasó, que es lo que sirve para otras cosas

La instrucción decía *"actualiza el README"*. Y se cumplió: los seis lo actualizaron.

No decía que tuviera que quedar **cierto**.

> **Toda instrucción que añades se ejecuta también de la forma más barata que la cumpla.**

Esa frase es lo único que me llevo de todo el experimento, y no depende de Claude Code ni
de skills ni de agentes. Es la misma dinámica de cualquier objetivo mal definido: pides
cobertura de tests y te llegan tests que no comprueban nada; pides documentación y te llega
documentación.

Al escribir una regla, pregúntate cuál es la forma más barata de cumplirla. Si esa forma te
vale, la regla está bien. Si no te vale, falta acotarla.

### Cómo lo reescribí

Cambié la instrucción de **tarea** a **criterio de terminado**:

- Antes: *"Actualiza el README, el docstring del módulo y los vecinos."*
- Después: *"Que no quede ni una frase falsa. Búscalas, no las recuerdes. Y comprueba que
  es verdad lo que añades."*

Mismo contenido. Mismo coste de contexto. Resultado distinto — pero eso, con su número y su
límite, va en la siguiente entrega.

### Y una cosa que hicieron las nuevas y ninguna de las viejas

Al pedir que **buscaran** en vez de actualizar, una pasada corrigió una frase falsa **que
no venía de su cambio**: un fichero decía "cuatro pasos, uno por módulo" sobre un diagrama
que lista cinco. Llevaba mal desde que se escribió el pipeline.

Ninguna instrucción menciona ese fichero. Una lista de sitios nunca lo habría incluido.

---

**La pregunta de hoy:** coge una instrucción que le des habitualmente a tu agente — o a tu
equipo — y pregúntate cuál es la forma más barata de cumplirla. ¿Cuál se te ha caído?

## Notas

- **Es artículo y no post** porque necesita la tabla y el "por qué pasó". Comprimido a 1.200
  caracteres pierde justo la parte que lo hace útil.
- Al pegar en LinkedIn, la tabla hay que rehacerla: dos líneas de texto o una imagen. El
  editor no soporta tablas de markdown.
- **Sigue sin ir el enlace al repositorio.** Va en la entrega 9.
- Los subtítulos van con el estilo de encabezado del editor de LinkedIn, no con `###`.
