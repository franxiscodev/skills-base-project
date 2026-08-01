# Medí las skills de mi repositorio. Una llevaba 40 sesiones cobrando y sin trabajar

La semana pasada borré una skill que había escrito yo, que estaba bien escrita, y que
funcionaba.

El problema es que nunca llegó a ejecutarse. Ni una vez en 40 sesiones. Y lo descubrí
porque me puse a contar, no porque nada fallara — de hecho, todo iba bien. Ese es
justamente el problema del que quiero hablar.

## El experimento que me obligó a cambiar de método

Empecé como empieza todo el mundo. Tenía un pipeline de datos en Python con una convención
estricta: cada regla de limpieza es una función, con su test y su recuento de filas
descartadas. Está aplicada cinco veces en el código y **no está escrita en ninguna parte**.

El candidato perfecto para una skill, ¿no? Escribes las convenciones, el agente las
respeta, y dejas de repetirlas en cada conversación.

Antes de escribirla hice algo que casi nadie hace: **la medí sin escribirla.** Sesión
limpia, sin ninguna pista, un prompt de una línea:

> *"Añade al pipeline una regla que descarte las ventas con importe cero."*

Mi hipótesis, escrita antes de ejecutar nada, era que metería la condición dentro de otra
función, sin test y sin recuento. Cinco predicciones concretas.

**Falló las cinco.** Tres pasadas de tres: función propia, tipo de retorno correcto,
encadenada donde tocaba, dos tests cada una, y un docstring explicando por qué la regla va
*después* de la conversión de tipos y no antes.

El agente había deducido la convención leyendo el código. La skill que iba a escribir no
hacía falta.

Sin ese "antes" la habría escrito, habría funcionado, y habría celebrado que funcionaba.
No tenía con qué compararlo.

## Lo que pasó cuando la escribí igual

La escribí de todas formas, acotada a los tres puntos donde sí hubo fallos. Y aquí está el
dato que no aparece en ningún tutorial.

Uno de esos puntos era *"actualiza el README"*. Resultado:

| | Sin skill | Con skill |
|---|---|---|
| Toca el README | 1 de 6 | **6 de 6** |
| **Lo deja verdadero** | — | **0 de 6** |

Seis README tocados. Cero correctos.

Y lo que lo hace incómodo de verdad: **antes de la skill, ese error no existía.** No
porque el agente fuera más cuidadoso, sino porque cinco de las seis pasadas ni siquiera
tocaban el fichero. La skill subió la cobertura del 17 % al 100 % y creó, de paso, una
clase de error nueva: afirmaciones falsas en la documentación.

Si solo cuentas aciertos, eso es invisible. Y contar solo aciertos es lo que hace todo el
mundo, porque para ver lo otro hay que haber medido el "antes".

De ahí salió la regla que más uso ahora:

> **Toda instrucción que añades se ejecuta también de la forma más barata que la cumpla.**
> Al escribir una regla, pregúntate cuál es esa forma. Si te vale, la regla está bien; si
> no, falta acotarla.

*"Actualiza el README"* se cumple tocándolo. No dice que tenga que quedar cierto.

## El peaje que se paga aunque no se use nunca

Lo siguiente que medí fue el otro mecanismo: MCP, los servidores que dan capacidades
nuevas al agente.

Tenía uno instalado que sirve documentación actualizada de librerías. Muy razonable, y muy
recomendado. Conté qué aportaba realmente:

- **647 caracteres** en el contexto de **cada sesión**, siempre.
- **0 invocaciones en 26 sesiones.**

Y un detalle que casi me lleva a la conclusión contraria: en 25 de esas 26 sesiones el
nombre del servidor *aparecía*. Si llego a contar apariciones en vez de invocaciones,
habría concluido que se usaba constantemente. Lo que aparecía era su propio bloque de
instrucciones, el que se carga aunque no lo llames.

> **Cuenta usos, no menciones.** Buscar el nombre da el resultado contrario al real.

Para poner los 647 caracteres en contexto: las **tres** skills de aquel repositorio
costaban 1.132 caracteres permanentes entre las tres. Un solo servidor MCP costaba más que
cualquiera de ellas por separado.

Y el coste no depende de cuántas herramientas traiga:

> **El coste de un MCP no lo decide cuántas herramientas trae, sino cuánto texto escribió
> su autor.** Y ese texto no lo controlas tú.

## La skill que nunca ganó

Volvamos a la que borré.

Tenía dos skills de Git. Una cubría el contenido del mensaje de commit; la otra, el flujo
de trabajo — en qué rama estás, qué comprobar antes de un push, cómo recuperar un commit
mal puesto. Las separé a propósito y declaré la frontera **en el cuerpo de las dos**, cada
una remitiendo a la otra. Un diseño del que estaba bastante satisfecho.

Conté las invocaciones reales sobre 40 sesiones:

| Skill | Coste permanente | Veces que se cargó |
|---|---|---|
| Convenciones del pipeline | 338 caracteres | 13 |
| Mensajes de commit | 276 caracteres | 5 |
| **Flujo de trabajo Git** | **518 caracteres** | **0** |

Cinco a cero, en sesiones donde las dos aplicaban: las cinco veces que ganó la primera,
esas mismas sesiones hicieron además push o crearon ramas — territorio exclusivo de la que
perdió.

El diagnóstico, cuando lo vi, fue evidente y lo tenía delante desde el principio:

> **Una frontera entre dos skills solo existe si está en la descripción.** El cuerpo no se
> lee si la descripción no gana. Escribirla ahí es documentarla para un lector que no
> llega.

Lo de "se carga cualquiera de las dos, a suertes" que yo mismo había escrito no era
cierto. No salió a suertes. Salió siempre la misma.

Así que la borré. Con una ventaja curiosa:

> **Quitar algo que nunca se ejecutó no puede romper nada.** El 0 de 40 es a la vez el
> motivo del borrado y la garantía de que es seguro.

Su contenido era bueno. Da igual: nunca se leyó.

## Dos cosas que hice mal, por si sirven

**Me inventé una causa.** Cuando una medición salió vacía, publiqué una explicación
elegante: *"el servidor figura como conectado, no da ningún error, y aporta cero
herramientas"*. Los datos eran correctos; la causa me la inventé. La real era aburrida —
lo había instalado desde otra carpeta. Estaba a un comando de distancia y no lo busqué,
porque la explicación interesante ya encajaba.

> **Cuando una observación admite una causa mundana y otra publicable, la mundana se
> comprueba primero.** Si no, acabas enseñando una regla que no existe.

Es el fallo más fácil de cometer en material didáctico, porque el incentivo empuja en esa
dirección: la causa interesante se cuenta mejor.

**Y una pasada que no puedo probar.** De las seis del "antes", una no tiene guardada su
salida. Según mis propias reglas, esa pasada no ocurrió. Así que el resultado honesto es
cinco de cinco verificable más una sexta que registré en su día y hoy nadie puede
recontar. No cambia la conclusión, pero prefiero decirlo a que lo descubra otro.

## El método, que es lo único que se lleva a otra herramienta

> **Primero se mide sin. Después se decide si hace falta. Solo entonces se escribe.**

Suena obvio y casi nadie lo hace, porque exige el paso incómodo: probar **sin** la
herramienta primero. Sin ese "antes" todo lo que instalas funciona — no tienes con qué
compararlo.

Y dos reglas que me ahorraron publicar cosas falsas:

- **Un experimento sin la salida guardada no ocurrió**, y la salida se guarda dentro del
  repositorio. Una prueba que no viaja con el experimento obliga a creerse el experimento.
- **Los resultados que contradicen la hipótesis se publican igual.** Son los únicos que
  nadie más te va a contar.

Nada de esto depende de Claude Code, ni de un modelo, ni de este año. Depende de que un
agente tenga una ventana de contexto finita y de que alguien decida qué entra.

Casi todo lo que se publica sobre esto enseña a **añadir**: más servidores, más
herramientas, más skills. Es cómodo porque cada paso parece gratis — añades algo, no rompes
nada, y te quedas con más que antes.

Después de medirlo durante dos semanas, mi conclusión es la contraria:

> **La habilidad que importa no es saber usar skills y MCP. Es saber decidir qué merece
> estar en la ventana de contexto.**

Y saber restar es la parte difícil, porque es la única que no se puede improvisar.

---

*Los cinco experimentos están publicados con el método, las salidas reales de cada pasada
y los resultados que refutaron mi hipótesis:* **[enlace al repositorio]**
