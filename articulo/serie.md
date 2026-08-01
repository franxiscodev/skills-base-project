# La serie — nueve entregas

> El plan completo antes de escribir nada. Si el arco cambia, se cambia **aquí** y luego se
> escriben las piezas, no al revés.

## El principio que ordena todo

No son nueve consejos sueltos con un número cada uno. Es **una historia con orden**, y el
orden importa:

> Empieza por el final —una skill borrada—, retrocede para contar por qué me puse a contar,
> y termina admitiendo que la campaña de mediciones se estaba comiendo el proyecto.

Cada entrega cierra un hilo y abre otro. Quien llega en la cuarta entiende lo que lee;
quien viene desde la primera tiene motivo para esperar la quinta.

**Regla que no se rompe:** cada entrega lleva **un solo número** y **una sola idea**. Si
lleva dos, son dos entregas. Ese fue el error del primer borrador: cinco resultados en una
pieza, y ninguno se queda.

---

## El arco

| # | Título de trabajo | El número | Formato |
|---|---|---|---|
| 1 | La skill que borré | 518 caracteres, 0 de 40 sesiones | Post |
| 2 | La medí antes de escribirla, y no hacía falta | Falló las 5 predicciones · 3 de 3 sin ella | Post |
| 3 | La escribí igual, y creó un error que antes no existía | 6 README tocados, 0 correctos | **Artículo** |
| 4 | Mismo contenido, otra redacción | 0 de 3 → 3 de 3 | Post |
| 5 | La skill sube el techo, el código sube el suelo | 10 líneas de test, 6 de 6 fallos cazados | Post |
| 6 | 647 caracteres en cada sesión, cero veces usado | 0 invocaciones en 26 sesiones | Post |
| 7 | Ya tenía la herramienta. Instalé la que se solapaba | El agente eligió la nueva 3 de 3 | Post |
| 8 | Cuatro intentos, ningún error, tres mediciones perdidas | 6 pasadas tiradas | **Artículo** |
| 9 | Lo que me costó medir todo esto | El cierre, y el enlace al repositorio | **Artículo** |

**Siete posts y tres artículos.** Los artículos van donde la profundidad se paga: el
hallazgo más incómodo (3), el que más se generaliza fuera de Claude Code (8) y la síntesis
(9).

---

## Entrega por entrega

Para cada una: con qué abre, con qué cierra, y qué pregunta se hace.

### 1 · La skill que borré

**Abre:** «Borré una skill que había escrito yo, que estaba bien escrita y que funcionaba.
Nunca llegó a ejecutarse. Ni una vez en 40 sesiones.»

**Cierra:** lo descubrí contando, no porque fallara nada. Todo iba bien. Y lo que me llevó
a contar fue algo que había medido tres semanas antes y salió al revés de lo que esperaba.

**Pregunta:** *¿Cuántas skills tienes instaladas ahora mismo, y cuántas se han cargado esta
semana? Casi nadie lo sabe, y se mira en un minuto.*

> Esta pregunta hace dos cosas: da conversación, y le pone a la gente delante el problema
> del que va la serie entera. Los que contesten «no lo sé» son el público.

Base: [exp 05](../temario/experimentos/05-la-skill-que-nunca-gana.md).

### 2 · La medí antes de escribirla, y no hacía falta

**Abre:** el candidato perfecto. Una convención estricta, aplicada cinco veces en el
código, escrita en ninguna parte.

**Cierra:** escribí la hipótesis antes de ejecutar. Cinco predicciones concretas. **Falló
las cinco.** El agente había deducido la convención leyendo el código.

**Gancho al siguiente:** la escribí igual. Y ahí empezó lo interesante.

**Pregunta:** *¿Has probado alguna vez a hacer la tarea sin la herramienta antes de
construirla? Es el paso que casi nadie da, y es el único que te dice si sirve.*

Base: [exp 01](../temario/experimentos/01-convenciones-pipeline.md).

### 3 · La escribí igual, y creó un error que antes no existía — ARTÍCULO

**Abre:** subí la cobertura del 17 % al 100 %. Objetivo cumplido.

**El giro:** seis README tocados, cero correctos. Y antes de la skill ese error **no
existía** — porque cinco de seis pasadas ni tocaban el fichero.

**La idea:** *toda instrucción que añades se ejecuta también de la forma más barata que la
cumpla.* «Actualiza el README» se cumple tocándolo; no dice que tenga que quedar cierto.

**Pregunta:** *Coge una instrucción que le des a tu agente y pregúntate cuál es la forma
más barata de cumplirla. Si te vale, está bien escrita. ¿Cuál se te ha caído?*

Base: [exp 01](../temario/experimentos/01-convenciones-pipeline.md).

### 4 · Mismo contenido, otra redacción

**Abre:** no cambié lo que decía la regla. Cambié **cómo** lo decía: de lista de sitios a
criterio de terminado.

**El número:** 0 de 3 → 3 de 3.

**El límite, que es la mitad honesta:** con un modelo más pequeño, el mismo texto solo
levantó 1 de 3.

**Pregunta:** *¿Tus instrucciones están escritas como lista de sitios o como criterio de
terminado? La diferencia se ve en si funcionan en el sitio que no enumeraste.*

Base: [exp 02](../temario/experimentos/02-criterio-vs-lista.md).

### 5 · La skill sube el techo, el código sube el suelo

**Abre:** ese 1 de 3 del modelo pequeño no se arreglaba escribiendo mejor.

**El número:** bajé el punto a un test de diez líneas. Cazó 6 de 6 fallos, sin un solo
falso positivo en las 12 ejecuciones correctas. Y no gasta contexto ni depende de que nadie
se acuerde.

**La idea:** si no controlas quién ejecuta, el punto tiene que bajar a algo que no dependa
del lector.

**Pregunta:** *¿Cuántas de tus reglas de agente son en realidad un test que no has
escrito?*

Base: [exp 03](../temario/experimentos/03-bajar-al-codigo.md).

### 6 · 647 caracteres en cada sesión, cero veces usado

**Abre:** cambio de mecanismo. Hasta aquí, skills. Ahora, MCP.

**El número:** 647 caracteres en el contexto de cada sesión, siempre. 0 invocaciones en 26
sesiones.

**El detalle que casi me engaña:** en 25 de esas 26 el nombre del servidor *aparecía*. Si
llego a contar apariciones en vez de invocaciones, habría concluido lo contrario de lo que
pasaba.

**Pregunta:** *¿Sabes cuánto texto mete en tu contexto cada servidor MCP que tienes
conectado? No lo decide cuántas herramientas trae: lo decide cuánto escribió su autor.*

Base: [exp 04](../temario/experimentos/04-coste-de-un-mcp.md).

### 7 · Ya tenía la herramienta. Instalé la que se solapaba

**Abre:** el argumento cómodo era «si ya tienes un CLI que hace eso, el MCP añade contexto
sin añadir capacidad».

**El giro:** lo medí y salió al revés. Con el CLI autenticado y disponible, y sin ninguna
instrucción sobre cuál usar, el agente fue al MCP **3 de 3**.

**La idea:** tener ya la herramienta no protege de instalar la que se solapa. La sustituye.
Y la elección no es tuya, es suya.

**Pregunta:** *Cuando instalas algo que se solapa con lo que ya tenías, ¿quién decide cuál
se usa? Spoiler: tú no.*

Base: [exp 04](../temario/experimentos/04-coste-de-un-mcp.md).

### 8 · Cuatro intentos, ningún error, tres mediciones perdidas — ARTÍCULO

**Abre:** instalarlo se documenta siempre igual: un comando, una captura donde pone
`Connected`, y a otra cosa.

**Lo que pasó de verdad:** cuatro intentos, seis pasadas de agente tiradas. Y el dato que
lo hace útil: **en ninguno de los tres fallos hubo un solo mensaje de error.** Todos los
diagnósticos decían la verdad.

**La parte incómoda:** en uno de ellos me inventé la causa. Publiqué una explicación
elegante cuando la real era aburrida y estaba a un comando de distancia. No la busqué
porque la interesante ya encajaba.

**Pregunta:** *¿Cuántas veces has dado por instalada una capacidad porque un panel decía
que sí? Comprobar la configuración no es comprobar la ejecución.*

> Esta entrega es la que más viaja fuera de Claude Code: vale para cualquier sistema donde
> configuras en un sitio y ejecutas en otro.

Base: [capítulo 07](../temario/07-instalar-una-capacidad.md).

### 9 · Lo que me costó medir todo esto — ARTÍCULO, cierre

**Abre:** recoge el hilo de la entrega 1 y lo cierra.

**El método:** primero se mide sin, después se decide, solo entonces se escribe. Y las dos
reglas que evitaron publicar cosas falsas: un experimento sin la salida guardada no
ocurrió, y los resultados que contradicen la hipótesis se publican igual.

**La confesión, que es lo que hace que esto no sea publicidad:** llegó un punto en que la
campaña de mediciones **se estaba convirtiendo en el proyecto**. Cancelé un experimento que
acababa de pre-registrar porque diez pasadas nuevas no iban a cambiar la decisión. Medir
tiene el mismo problema que instalar: cada medición parece barata y ninguna se cuenta
contra el total.

**El cierre:** *saber restar es la parte difícil, y es la única que no se puede improvisar.*

**Aquí sí va el enlace al repositorio**, con los cinco experimentos, el método completo y
las salidas reales de cada pasada.

Base: el [artículo largo ya escrito](articulo-linkedin.md), que se reconvierte en esta
entrega.

---

## Cadencia

**Dos por semana durante cinco semanas.** Martes y jueves, que es cuando LinkedIn tiene más
tráfico profesional.

| Semana | Entregas |
|---|---|
| 1 | 1 · 2 |
| 2 | 3 *(artículo)* · 4 |
| 3 | 5 · 6 |
| 4 | 7 · 8 *(artículo)* |
| 5 | 9 *(artículo, cierre)* |

Una por semana alargaría la serie a dos meses y medio y perdería el hilo entre entregas.
Tres por semana satura.

> **Escribe las dos siguientes antes de publicar la primera.** Una serie que se para en la
> tercera entrega hace más daño que no haberla empezado.

---

## Las preguntas no son para el algoritmo

Cada entrega termina en una pregunta abierta. No es *engagement bait*: son las preguntas
cuyas respuestas necesitas.

> **Lo que la gente conteste es la investigación de mercado del curso.** Si en la entrega 1
> veinte personas dicen «no tengo ni idea de cuántas se me cargan», eso es un módulo. Si
> nadie contesta, eso también es información y es barata.

Conviene guardar las respuestas. Un fichero por entrega, aquí mismo, con lo que llegue.

---

## Lo que NO hay que hacer

- **No prometer un número de entregas en la primera.** Si luego son siete y no nueve, se
  nota. Prometer «una serie» basta.
- **No repetir el número de la entrega anterior** para «recordar el contexto». Cada pieza se
  sostiene sola o no se publica.
- **No enlazar el repositorio hasta la 9**, salvo en el primer comentario. El enlace es el
  final del recorrido, no el principio.
- **No suavizar los dos errores propios** (la causa inventada, la pasada sin diff). Son lo
  que separa esto de un folleto.
