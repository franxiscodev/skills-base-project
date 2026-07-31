# 02 — El árbol de decisión: dónde va cada cosa

> **Evidencia:** [experimento 01](experimentos/01-convenciones-pipeline.md) ·
> [experimento 03](experimentos/03-bajar-al-codigo.md)

## La pregunta está mal formulada

Tropiezas con algo. El agente hace una tarea peor de lo que querías, o repites una
corrección por tercera vez. Y entonces te haces la pregunta natural:

> ¿Esto merece una skill?

**Esa pregunta ya trae la respuesta metida dentro.** Presupone que la skill es el
destino por defecto y que lo único que falta es decidir si el caso "da la talla". De
ahí sale la carpeta con veinte skills de las que se disparan tres.

La pregunta correcta es otra:

> **¿Dónde va esto? — y una de las respuestas válidas es "a ningún sitio".**

Es la versión moderna del error que todo el mundo cometió antes con `CLAUDE.md`:
meterlo todo ahí porque era el sitio que existía.

---

## El árbol completo

| Destino | Cuándo | Coste de contexto |
|---|---|---|
| **Nada** | Pasó una vez y no se va a repetir | Cero |
| **El código** | Se resuelve en el propio código, con un comentario que explique el porqué | Cero |
| **Un linter o formateador** | Es una regla mecánica y verificable | Cero |
| **Un test** | Es un criterio que debe romperse ruidosamente si alguien lo cambia | Cero |
| **El README** | Lo necesita una **persona** que llega al proyecto | Cero para el agente |
| **Una skill** | Procedimiento con criterio, que se repite, y que el agente haría mal sin ella | Cero hasta dispararse |
| **La memoria** | Hecho duradero sobre *este* usuario o *este* proyecto | Casi cero |
| **`CLAUDE.md`** | Regla que aplica **en todos los turnos**, sin excepción | Fijo y permanente |

**Lo importante de esta tabla no son las filas de abajo: son las de arriba.** Las
cinco primeras resuelven la mayoría de los casos con coste cero, y son justo las que
nadie considera — porque no consisten en usar la herramienta nueva.

> Está ordenada por coste, y se recorre **de arriba abajo**. El primer destino que
> sirva, gana. Bajas un escalón solo cuando el anterior no puede con el caso.

---

## Los tres filtros para llegar a "skill"

**1. ¿Le pasaría igual a otra persona haciendo la misma tarea?**
No → es un hecho sobre ti o sobre tu proyecto → **memoria**.

**2. ¿Va a volver a ocurrir?**
No → **nada**, o como mucho una línea en el README.

**3. ¿El agente lo haría mal sin la skill?**
No → **decoración**. Bórrala.

### El tercero es el que nadie aplica, y el que más mata

Los dos primeros son intuitivos y se contestan pensando. El tercero exige algo
incómodo: **probar sin la skill primero**. Casi todo el material que circula sobre
skills escribe la skill, la prueba, funciona, y publica. Falta el paso que da sentido
a todo lo demás.

> **Sin el "antes" no hay forma de saber si la skill aportó algo o si el agente ya lo
> hacía bien.**

Y cuando lo mides, a veces la respuesta es que no hacía falta.

#### El caso medido

En este repositorio, `limpiar.py` sigue una convención estricta: *una regla de
limpieza = una función = un test = un recuento*. Está aplicada cinco veces y **no
está escrita en ninguna parte**. Parecía el candidato perfecto a skill.

Se midió antes de escribirla: mismo encargo, sesión limpia, seis veces, dos modelos
distintos.

| | Resultado |
|---|---|
| Función propia con la misma firma | 6/6 |
| Devuelve el recuento con su motivo | 6/6 |
| Encadenada en el sitio correcto | 6/6 |
| Con su test | 6/6 |

**Seis de seis, sin una sola desviación, incluido el modelo pequeño.** La skill que
íbamos a escribir era innecesaria. Toda la variación apareció en otro sitio: en lo
que el código no puede mostrar.

> **Lo que el código muestra, el código lo enseña. La skill hace falta para lo que el
> código no puede mostrar.**
>
> Corolario: **escribir bien el código es la forma más barata de no necesitar una
> skill.**

---

## El coste de una skill que no se dispara

No es cero, y este es el matiz que casi nunca se explica. Una skill inútil:

- ocupa sitio en el **índice de descripciones**, que sí está permanentemente en
  contexto;
- **compite** con las buenas cuando el agente decide cuál cargar;
- envejece sin que nadie la revise, y acaba diciendo mentiras;
- da **falsa sensación de control** — *"está documentado"* no es *"se aplica"*.

> **Una skill que no se dispara nunca es peor que no tenerla.** Está en tu cabeza y
> no en la del agente.

El caso completo —incluido el coste que solo se ve midiendo el "antes"— está en el
[capítulo 05](05-cuando-no-escribir-una-skill.md).

---

## Bajar un escalón: cuando la skill no llega

Elegir "skill" no cierra la decisión para siempre. A veces la escribes, la mides y
descubres que **ese punto no se sostiene ahí**.

En este repo pasó con algo tan simple como mantener el README diciendo la verdad
sobre la salida del pipeline. Se midió con la skill escrita de dos formas distintas:

| Deja el README verdadero | Skill como lista de sitios | Skill como criterio |
|---|---|---|
| Modelo grande | 0/3 | **3/3** |
| Modelo pequeño | 0/3 | 1/3 |

La redacción importaba —y mucho— pero el suelo seguía dependiendo de quién ejecutara.
Así que ese punto bajó al escalón de arriba: **un test** que compara la traza
documentada con la salida real. Diez líneas, y no vuelve a fallar.

> **La skill sube el techo. El código sube el suelo.**
>
> Una skill bien escrita hace que el modelo capaz haga el trabajo completo. No hace
> que el modelo pequeño lo haga. Si no controlas quién ejecuta, el punto tiene que
> bajar a algo que no dependa del lector.

### El criterio para repartir

No es la importancia del punto. Es este:

> **Lo que tiene una salida observable baja al test. Lo que exige juicio sobre una
> intención se queda en la skill.**

*"La traza documentada coincide con la que imprime el programa"* se comprueba. *"Esta
fila de la tabla describe un defecto que el generador fabrica de verdad"* exige
entender qué pretende el generador — y automatizarlo significaría escribir en el test
otra lista que también hay que mantener. Eso no resuelve el problema: lo muda de sitio.

---

## Casos resueltos

Reales, de este proyecto, con veredicto y motivo:

| Caso | Destino | Por qué |
|---|---|---|
| `initcap` no existe en DuckDB: verificar el dialecto antes de construir encima | **Skill** | Pasa los tres filtros. El modelo no sabe que no lo sabe |
| La consola de Windows no puede imprimir `→` ni `€` | **Código + comentario** | Falla el filtro 3: el agente ya escribe ficheros con codificación explícita, y el fallo estaba en la consola, donde una skill no habría llegado |
| Las convenciones de `limpiar.py` | **El código, ya** | 6/6 sin skill. Escribirla habría sido pagar contexto por algo resuelto |
| Mantener la traza del README al día | **Test** | Empezó como skill y bajó: 0/6 con la skill, 0 fallos con el test |
| Que el usuario prefiere que no le ejecuten `git push` | **Memoria** | Falla el filtro 1: es un hecho sobre esta persona, no sobre la tarea |

---

## El ejercicio

Coge ocho o diez cosas que te hayan pasado esta semana con un agente y, para cada
una, escribe **el destino, no la solución**.

Se corrige discutiendo, porque casi ninguna es evidente. Y el aprendizaje no es la
lista de destinos: es **notar cuántas veces habrías escrito una skill por defecto**.

---

## Lo que se lleva a cualquier herramienta

El árbol no habla de Claude Code. Habla de dónde vive el conocimiento de un equipo, y
eso aplica igual con otro agente, otro modelo u otro año:

1. **Pregunta dónde va, no si merece una skill.**
2. **Recorre el árbol de arriba abajo.** Lo barato primero.
3. **Mide antes de escribir.** El tercer filtro no se contesta opinando.
4. **Lo comprobable baja al código. Lo opinable se queda arriba.**
