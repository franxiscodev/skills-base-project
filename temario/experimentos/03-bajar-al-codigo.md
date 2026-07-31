# Experimento 03 — Bajar al código lo que la skill no sostiene

> Cierra lo que dejaron abierto el [01](01-convenciones-pipeline.md) y el
> [02](02-criterio-vs-lista.md). Método: [PLANTILLA.md](PLANTILLA.md).
> **Estado: cerrado.** Sin generar ni una pasada nueva.

**Hipótesis** *(escrita antes de ejecutar nada)*:

> El punto que ninguna redacción de la skill sostuvo —mantener cierto lo que el README
> dice de la salida— se resuelve con un test, y se puede demostrar **contra las
> ejecuciones ya guardadas**, sin generar ninguna nueva.

## El problema

Dos experimentos midieron lo mismo desde dos ángulos:

| Deja el README verdadero | Sin skill | Skill como lista | Skill como criterio |
|---|---|---|---|
| Opus 5 | — | 0/3 | 3/3 |
| Haiku 4.5 | — | 0/3 | 1/3 |
| Ambos, toca el README | 1/6 | 6/6 | 6/6 |

La skill sube el techo y no sube el suelo. Un punto que depende de cuánto juicio tenga
quien ejecuta **no pertenece a una skill**: pertenece al código, donde no gasta
contexto, no depende del lector y falla solo.

## El método: replay, no pasadas

Las dieciocho ejecuciones dejaron su `.diff` guardado. Eso permite algo que no
habíamos usado hasta ahora:

> **Un test se puede validar contra ejecuciones pasadas.** Se aplica cada diff sobre
> el repo, se corre el test y se anota si lo caza. Coste: cero generaciones.

Y trae gratis lo que suele faltar en este tipo de comprobación: **las pasadas buenas
son el control de falsos positivos.** Un test que cace los fallos y también las
ejecuciones correctas no sirve de nada, y sin ellas no te enterarías.

## 1. El test de la traza

[`tests/test_documentacion.py`](../../tests/test_documentacion.py) — ejecuta el
pipeline de verdad y compara su salida, línea por línea, con el bloque documentado en
el README.

Dos decisiones de diseño que importan:

- **Busca el bloque por su encabezado, no por número de línea.** Un test que dependa
  de dónde está el bloque falla cuando alguien reordena el README, que no es lo que
  queremos detectar.
- **Compara contra una ejecución real, no contra un texto esperado.** Escribir a mano
  la salida esperada sería cometer dentro del test exactamente el error que el test
  persigue.

### Resultado del replay — 18 diffs

| Origen | Cazadas | Correctas |
|---|---|---|
| Sin skill (5 diffs) | **4** | 1 |
| Skill como lista (7 diffs) | **2** | 5 |
| Skill como criterio (6 diffs) | 0 | 6 |

**Ninguna ejecución correcta falla.** Cero falsos positivos en 18.

Las cazadas son exactamente las que debían serlo:

- **Cuatro de las cinco sin skill** añadieron la regla y no tocaron el README. La que
  se salva es la única que sí lo actualizó — la del `1/6` del experimento 01. El test
  reproduce la medición por su cuenta.
- **La traza inventada.** Una ejecución escribió
  `descartar_importe_cero: 490 → 490 (0 descartadas — importe cero)` cuando el
  programa imprime `490 filas, sin descartes`, teniendo el formato real en las líneas
  contiguas. **Es el fallo que más difícil sería pillar leyendo**, y el test lo caza
  sin esfuerzo.

## 2. El test de las cuentas en prosa

La línea `# ejecuta los cinco pasos` sobrevivió a las dos redacciones de la skill. No
es que se les olvidara mirarla: **una cuenta escrita en prosa caduca cada vez que
cambia el pipeline y nada avisa.**

El test rechaza la construcción entera, no el número equivocado. Es más estricto que
*"¿es verdad?"* a propósito.

### Resultado del replay — 18 diffs

| Estado en que quedó la línea | Ejecuciones | ¿Caza? |
|---|---|---|
| Falsa — *"los cinco pasos"* con seis | 11 | ✅ |
| Cierta pero frágil — *"los seis pasos"* | 3 | ✅ |
| Sin cuenta — *"el pipeline completo"* | 4 | correctamente no |

Las tres del medio son la razón de ser del test:

> **Actualizar el número deja el documento cierto y el problema intacto.** Vuelve a
> caducar en el cambio siguiente. Solo cuatro ejecuciones —todas de Opus— llegaron
> solas a quitar la cuenta, que elimina la clase de error en vez de la instancia.

El README del repo llevaba esa línea desde el principio: el test falló nada más
escribirse, sobre nuestro propio trabajo.

## Lo que estos tests NO cubren

**La fila falsa en la tabla de defectos** — tres ejecuciones añadieron una fila
afirmando que el generador fabrica importes a cero, cuando no los fabrica.

Automatizarlo exigiría que el test supiera qué defectos produce `generar_datos.py`, y
eso es una afirmación sobre la intención del generador, no sobre su salida. Se queda
**en la skill**, que es donde funcionó: dos ejecuciones se negaron explícitamente a
añadir la fila, y una de ellas dio el motivo correcto sin que nadie se lo pidiera.

> **El reparto no es "o skill o código": es cada cosa donde se puede comprobar.** Lo
> que tiene una salida observable baja al test. Lo que exige juicio sobre una
> intención se queda arriba.

## Qué aprendimos

1. **Un test puede validarse contra ejecuciones pasadas.** Si guardas los diffs —y el
   método obliga a guardarlos— tienes un banco de pruebas gratis para cualquier
   comprobación que escribas después. Dieciocho casos reales, cero generaciones.
2. **Las ejecuciones correctas valen tanto como las fallidas.** Son el único control
   de falsos positivos que vas a tener. Un test que cace 6 de 6 fallos y también 12
   aciertos no vale nada, y sin las buenas no te enteras.
3. **Elimina la clase de error, no la instancia.** *"Los seis pasos"* es cierto hoy y
   falso en el próximo cambio. *"El pipeline completo"* no puede caducar. Cuando un
   punto se rompe una y otra vez, la pregunta no es cómo arreglarlo: es cómo dejar de
   poder romperlo.
4. **Lo comprobable baja; lo opinable se queda.** El criterio para repartir entre
   skill y código no es la importancia: es si existe una comprobación que decida.

## Cuándo NO hacer esto

- **Cuando el test sea más frágil que lo que protege.** Un test que se rompa cada vez
  que alguien reordena el README genera más trabajo del que ahorra. Por eso este busca
  por encabezado y no por posición.
- **Cuando la comprobación exija adivinar la intención.** La tabla de defectos no se
  automatiza sin escribir en el test una lista que también hay que mantener — y
  entonces has movido el problema, no lo has resuelto.
- **Cuando todavía no tengas la medición.** Escribir estos dos tests antes de los
  experimentos 01 y 02 habría sido adivinar. Aquí cada uno responde a un fallo
  concreto que se produjo un número concreto de veces.

## Nota de método: el instrumento también se pierde

Al montar el replay borré tres veces el propio fichero de test: el paso de limpieza
entre diffs (`git checkout -- . ; git clean -fd`) se lleva por delante cualquier
trabajo sin commitear, y el test **era** trabajo sin commitear.

> Es la misma regla del experimento 01 —*un experimento sin diff guardado no
> ocurrió*— aplicada al otro lado: **commitea el instrumento antes de medir con él.**
> Un arnés que restaura el repo no distingue entre lo que mides y con qué lo mides.

## Condiciones y reproducibilidad

- **Fecha:** 31 de julio de 2026
- **Sin modelos:** este experimento no genera nada. Se ejecuta sobre los diffs de los
  experimentos 01 y 02.
- **Versiones:** Python 3.12 · DuckDB 1.5.5 · pytest 9.1.1 · uv 0.7.9
- **Diffs usados:** 18. Del "antes" del experimento 01 solo hay cinco de las seis
  pasadas: una se perdió al deshacer un commit no solicitado, antes de que existiera
  la regla de guardar siempre el diff.
- **Cómo repetirlo:** por cada diff, `git apply`, `uv run pytest
  tests/test_documentacion.py`, anotar, y `git checkout -q -- . ; git clean -fdq`.
  Con el test **ya commiteado**.
