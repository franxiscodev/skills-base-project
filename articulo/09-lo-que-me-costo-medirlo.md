# Entrega 9 — Lo que me costó medir todo esto

> **Formato: ARTÍCULO** (nativo de LinkedIn) · **Cierre de la serie** ·
> **Base:** el [método](../temario/experimentos/PLANTILLA.md) y la
> [tesis](../temario/00-la-tesis.md)

Aquí sí va el enlace al repositorio. Es la única entrega que lo lleva.

> ⚠️ **No repite los hallazgos uno por uno.** Cada uno ya tuvo su entrega; volver a
> enumerarlos convierte el cierre en un resumen, y un resumen no se lee. Lo que aporta esta
> pieza es el **método** y el **coste**.

---

## Para pegar

### Empecé por una skill borrada. Termino por lo que me costó llegar a borrarla

Hace cinco semanas abrí esta serie contando que había borrado una skill escrita por mí, que
funcionaba, y que nunca llegó a ejecutarse. Entre medias he ido contando lo que me llevó a
mirar: una skill que no hacía falta, otra que creó un error que antes no existía, un
servidor que costaba en cada sesión y no se usó ni una vez.

Cierro con lo que hay debajo de todo eso, que es lo único que se traslada a otra
herramienta.

### El método, en una frase

> **Primero se mide sin. Después se decide si hace falta. Solo entonces se escribe.**

Suena obvio y casi nadie lo hace, porque exige el paso incómodo: **probar sin la
herramienta primero.**

Sin ese "antes", todo lo que instalas funciona. No tienes con qué compararlo. Y esa es
literalmente la estructura de casi todo el material que circula: se escribe la skill, se
prueba, funciona, se publica. Falta el paso que le daría sentido al resto.

En mi primer experimento la hipótesis falló las cinco predicciones. Sin haber medido antes,
habría escrito una skill inútil y habría celebrado que funcionaba.

### Las reglas que evitaron que publicara cosas falsas

De once que acabé escribiendo, tres hicieron casi todo el trabajo.

**Un experimento sin la salida guardada no ocurrió.** Y la salida se guarda **dentro** del
repositorio, no en una carpeta suelta del disco. Una prueba que no viaja con el experimento
obliga a creerse el experimento.

Esta se me cayó encima: al mover las pruebas dentro del repo descubrí en un minuto que una
de mis dieciocho pasadas no tenía salida guardada. Llevaba semanas ahí. Según mis propias
reglas, esa pasada no ocurrió — así que el resultado que publico es el verificable, que es
peor que el que ya tenía escrito.

**El artefacto tiene que poder contener la señal que buscas.** Diseñé una medición que
contaba invocaciones de herramientas mirando los diffs del código. Un diff guarda el árbol
de trabajo, no las herramientas que se llamaron: habría dado cero siempre. Y ese cero
habría parecido una confirmación de lo que yo esperaba.

**Los resultados que contradicen la hipótesis se publican igual.** Son los únicos que nadie
más te va a contar.

### La parte que hace que esto no sea publicidad

Llegó un punto en que **la campaña de mediciones se estaba convirtiendo en el proyecto.**

Lo vi cuando diseñé un experimento con tres ramas y diez pasadas para explicar por qué una
skill no se disparaba nunca. Lo dejé pre-registrado, lo guardé, y media hora después lo
cancelé sin ejecutar ni una pasada: las diez me iban a dar el *mecanismo*, y el mecanismo no
cambiaba la decisión. Con cero de cuarenta, esa skill se tocaba igual.

> **Medir tiene el mismo problema que instalar: cada medición individual parece barata y
> ninguna se cuenta contra el total.**

Es la trampa de la que va la serie entera, aplicada a la serie entera. La cuento porque el
material que solo enseña lo que salió bien es exactamente el material del que me estaba
quejando.

### Lo que se lleva a cualquier herramienta

Nada de esto depende de Claude Code, ni de un modelo, ni de este año. Depende de que un
agente tenga una ventana de contexto finita y de que alguien decida qué entra:

1. **Añadir no es gratis**, aunque no se dispare nunca.
2. **Toda capacidad nueva trae su propio fallo.** Cuéntalo también.
3. **Capacidad y criterio son ejes distintos.** Un MCP da manos; una skill, protocolo. No
   se sustituyen.
4. **Sin el "antes" no sabes si sirve**, solo sabes que funcionó.
5. **Cuenta usos, no apariciones.**
6. **Comprueba antes la causa aburrida que la interesante.**

Casi todo lo que se publica sobre esto enseña a añadir: más servidores, más herramientas,
más skills. Es cómodo porque cada paso parece gratis — añades algo, no rompes nada, y te
quedas con más que antes.

Después de cinco semanas midiéndolo, mi conclusión es la contraria:

> **La habilidad que importa no es saber usar skills y MCP. Es saber decidir qué merece
> estar en la ventana de contexto.**

Y saber restar es la parte difícil, porque es la única que no se puede improvisar.

---

Los cinco experimentos están publicados enteros: el método, las salidas reales de cada
pasada, los resultados que refutaron mi hipótesis y el que anulé por haberlo diseñado mal.
También está la skill que borré, en el historial, por si alguien quiere ver qué se pierde.

**[enlace al repositorio]**

**La pregunta de hoy, y con esta cierro:** ¿qué tienes instalado ahora mismo que no has
comprobado nunca si se usa?

## Notas

- **Es la única entrega con enlace en el cuerpo.** Después de nueve piezas, quien llega
  aquí ya ha decidido si le interesa.
- La confesión de la campaña que se come al proyecto es el centro de la pieza, no un
  añadido. Es lo que separa esto de un caso de éxito.
- El cierre recoge la pregunta de la entrega 1 en otra forma. Quien haya seguido la serie
  lo nota; quien llegue nuevo no lo echa de menos.
