# 00 — La tesis: economía de contexto

> **Evidencia:** [experimento 01](experimentos/01-convenciones-pipeline.md) ·
> [experimento 02](experimentos/02-criterio-vs-lista.md) ·
> [experimento 03](experimentos/03-bajar-al-codigo.md)

## La frase

> **La habilidad que importa no es saber usar skills y MCP. Es saber decidir qué merece
> estar en la ventana de contexto.**

Todo lo que circula empuja en la dirección contraria: más servidores, más herramientas,
más skills, más capacidades. Es una dirección cómoda porque cada paso parece gratis —
añades algo, no rompes nada, y quedas con más que antes.

Este material sostiene lo contrario, y no como aforismo. *"Menos es más"* no sirve para
decidir nada. Lo que sirve es **el criterio, caso por caso**, y el criterio solo se
sostiene con mediciones.

---

## Qué se ha medido aquí, exactamente

Es importante decir qué está probado y qué no, porque la tesis es fácil de sobrevender.

**Lo que sí:**

| Resultado | Dónde |
|---|---|
| La skill que íbamos a escribir **no hacía falta**: 6/6 sin ella, dos modelos | [Exp 01](experimentos/01-convenciones-pipeline.md) |
| Una skill **crea errores que antes no existían**: 0/6 → 3/6 afirmaciones falsas | [Exp 01](experimentos/01-convenciones-pipeline.md) |
| **Cómo está redactada** cambia el resultado más que el contenido: 0/3 → 3/3 | [Exp 02](experimentos/02-criterio-vs-lista.md) |
| Un punto que la skill no sostenía, **resuelto en 10 líneas de test** | [Exp 03](experimentos/03-bajar-al-codigo.md) |
| Un servidor MCP conectado y no usado: **647 caracteres siempre, 0 invocaciones en 26 sesiones** | [Exp 04](experimentos/04-coste-de-un-mcp.md) |

**Lo que no:** no se ha medido qué pasa cuando un MCP **se solapa** con una herramienta que
el agente ya tiene — el caso más caro y el más frecuente. Está pre-registrado y sin
ejecutar. Hasta que tenga número se enuncia como razonamiento, no como resultado. Este
material distingue las dos cosas siempre.

---

## Por qué añadir no es gratis

Tres costes, de menos a más incómodo.

**1. El sitio.** Todo lo que instalas paga peaje permanente, y se paga aunque no se use
nunca. Medido en este repositorio ([exp 04](experimentos/04-coste-de-un-mcp.md)):

| | Permanente en contexto |
|---|---|
| Una skill | Su `description`: **276–518 caracteres** |
| Un servidor MCP | Su bloque de instrucciones: **647 caracteres** |

Lo que **no** se paga por adelantado es el detalle: el cuerpo de la skill y los esquemas de
las herramientas del MCP se cargan cuando hacen falta. Conviene saberlo porque cambia la
conclusión práctica:

> **El coste de un MCP no lo decide cuántas herramientas trae, sino cuánto texto escribió
> su autor.** Y ese texto no lo controlas tú.

En el caso medido son instrucciones de comportamiento, no descripciones: *"úsalo aunque
creas que sabes la respuesta"*, *"prefiérelo a buscar en la web"*. Está delante del agente
en cada turno de cada sesión, incluidas las 26 en las que no se invocó ni una vez.

**2. La competencia.** Cuantas más opciones parecidas tenga delante, peor elige. Una skill
mediocre no ocupa solo su sitio: **compite con la buena** en el momento de decidir cuál
cargar.

**3. El fallo propio.** Este es el que nadie cuenta, y es medible:

| | Sin skill | Con skill |
|---|---|---|
| Toca el README | 1/6 | 6/6 |
| Mete una afirmación falsa | **0/6** | **3/6** |

La skill hizo exactamente lo que se le pidió, subió la cobertura del 17 % al 100 % — y
creó un error que antes no existía, porque antes nadie tocaba ese fichero.

> **Toda capacidad que añades se ejecuta también de la forma más barata que la cumpla.**
> Si solo cuentas aciertos, esa parte es invisible. Y contar solo aciertos es lo que hace
> todo el mundo, porque para ver lo otro hace falta medir el "antes".

---

## Capacidad y criterio son ejes distintos

La confusión más común es tratar skills y MCP como dos formas de lo mismo. No lo son:

| | Qué es | Qué aporta |
|---|---|---|
| **MCP** | **Capacidad** | Qué *puede* hacer el agente: conexión, permisos, endpoints |
| **Skill** | **Criterio** | *Cómo* y *cuándo* debe hacerlo, y qué comprobar antes |

> Un MCP sin skill es un agente con herramientas y sin protocolo.
> Una skill sin MCP es un agente con criterio y sin manos.

De ahí sale la pregunta que ordena cualquier evaluación de un servidor MCP — y no es
"¿esto reemplaza mi skill?":

> **¿Me da acceso a algo que ahora mismo no puedo alcanzar?**

Si ya hay un CLI que lo hace y el agente puede ejecutarlo, el MCP **añade contexto sin
añadir capacidad**. Si en cambio permite algo que no era posible —ver el DOM de una
aplicación corriendo, por ejemplo— eso es capacidad nueva y se paga con gusto.

*(Medido: el peaje y la ausencia de uso. **Todavía razonamiento:** que el solapamiento con
un CLI empeore el resultado. Es la medida C del [exp 04](experimentos/04-coste-de-un-mcp.md),
pre-registrada y pendiente.)*

Y una advertencia práctica que salió de la misma medición: **no audites esto con la lista
de servidores conectados.** Declaraba cinco que no aportaban ninguna herramienta a la
sesión. Lo que cuenta es lo que llega al contexto, no lo que dice el inventario.

*(Razonamiento, no medición: pendiente de experimento propio.)*

---

## Lo que la tesis obliga a hacer

Si el criterio es "qué merece estar", la única forma honesta de contestarlo es esta:

> **Primero se mide sin. Después se decide si hace falta. Solo entonces se escribe.**

Suena obvio y casi nadie lo hace, porque exige el paso incómodo: **probar sin la
herramienta primero**. Sin ese "antes", todo lo que instalas funciona — no tienes con qué
compararlo.

En el experimento 01 la hipótesis de partida **falló en las cinco predicciones**. Sin
haber medido antes, habríamos escrito una skill inútil y celebrado que funcionaba. Ese es
literalmente el material que circula.

Las reglas completas del método están en la [plantilla](experimentos/PLANTILLA.md). Dos
merecen adelantarse:

- **Un experimento sin diff guardado no ocurrió.**
- **Los resultados que contradicen la hipótesis se publican igual.** Son los únicos que
  nadie más te va a contar.

---

## Cómo leer este material

Los **capítulos** dan el criterio; los **experimentos** dan la prueba. Están separados a
propósito, porque envejecen distinto: el criterio dura, y los números concretos dependen
del modelo y de la versión de las herramientas.

| # | Capítulo | Contesta |
|---|---|---|
| 00 | Esta tesis | Por qué restar |
| 01 | Los tres mecanismos de contexto | Qué hay disponible y qué cuesta cada uno |
| [02](02-arbol-de-decision.md) | El árbol de decisión | Dónde va cada cosa |
| [03](03-anatomia-de-una-skill.md) | Anatomía de una skill | Cómo se escribe para que funcione |
| [04](04-frontmatter.md) | El frontmatter | Qué decide si tu skill llega a pasar |
| [05](05-cuando-no-escribir-una-skill.md) | Cuándo **no** escribir una skill | Cuándo la respuesta es que no |
| 06 | Cuándo abrir una conversación nueva | La misma tesis, dentro de la sesión |

Si solo vas a leer dos, lee el **02** y el **05**. El resto es cómo hacerlo bien una vez
has decidido que hay que hacerlo.

---

## Lo que se lleva a cualquier herramienta

Nada de esto depende de Claude Code, ni de un modelo, ni de un año concreto. Depende de
que un agente tenga una ventana de contexto finita y de que tú decidas qué entra:

1. **Añadir no es gratis**, aunque no se dispare nunca.
2. **Toda capacidad nueva trae su propio fallo.** Cuéntalo también.
3. **Capacidad y criterio son ejes distintos.** No se sustituyen.
4. **Sin el "antes" no sabes si sirve**, solo sabes que funcionó.
5. **Saber restar es la parte difícil**, y es la que no se puede improvisar.
