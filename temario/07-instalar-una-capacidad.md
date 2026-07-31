# 07 — Instalar una capacidad: lo que nadie te cuenta antes

> **Evidencia:** [experimento 04](experimentos/04-coste-de-un-mcp.md) ·
> [rama B anulada](experimentos/diffs/exp04-rama-B-ANULADA.md) ·
> [rama B válida](experimentos/diffs/exp04-rama-B.md)

## Por qué existe este capítulo

Instalar un servidor MCP se documenta siempre igual: un comando, una captura donde pone
`✔ Connected`, y a otra cosa. Este capítulo cuenta lo que pasó entre ese comando y la
primera medición válida.

**Cuatro intentos. Tres mediciones perdidas. Seis pasadas de agente tiradas.**

Y el dato que lo hace útil:

> **En ninguno de los tres fallos hubo un solo mensaje de error.** Todos los diagnósticos
> decían la verdad. Aun así, tres veces medimos la condición equivocada creyendo que
> medíamos la buena.

No es un capítulo sobre una herramienta concreta. Es sobre una clase de fallo que se repite
en cualquier sistema donde **configuras en un sitio y ejecutas en otro**.

---

## La cronología

| # | Qué pasó | Qué decía el diagnóstico | Qué pasaba de verdad |
|---|---|---|---|
| 1 | El `add` falló | `Incompatible auth server: does not support dynamic client registration` | El servidor pedía credencial, no negociaba OAuth |
| 2 | Reintento | `MCP server github already exists` | El intento fallido había dejado su entrada |
| 3 | Instalado y conectado | `✔ Connected` | Instalado **en otra carpeta** |
| 4 | Instalado en la carpeta buena | `✔ Connected` | La sesión de medición **ya estaba abierta** |
| 5 | Sesión nueva | `✔ Connected` en el terminal, **ausente** en el IDE | Terminal escribía `C:/…`, el IDE leía `c:/…` |
| 6 | Instalado con ámbito global | `✔ Connected` en los dos | Por fin |

Seis pasos para lo que la documentación resuelve en uno.

---

## Las tres lecciones que no caducan

### 1. Una capacidad no se instala en tu máquina: se instala en un ámbito

Fue la causa de tres de los cuatro fallos, con tres caras distintas: otra carpeta, la misma
carpeta escrita de otra forma, y una sesión que había arrancado antes.

> **«Está instalado» no es una propiedad de tu ordenador.** Es una propiedad de la
> combinación *quién ejecuta · desde dónde · desde cuándo*. Si no sabes decir esas tres
> cosas, no sabes si está instalado.

La consecuencia práctica es incómoda y vale para cualquier herramienta con configuración
por proyecto: **el ámbito más estrecho es el que más silenciosamente se equivoca.** Un
alcance global es más caro en contexto y mucho más difícil de equivocar.

### 2. La comprobación tiene que mirar donde ocurre el trabajo

Todos los diagnósticos que consultamos eran correctos y **ninguno contestaba a la pregunta
que creíamos hacerle**. La lista de servidores respondía sobre el directorio desde el que
se lanzaba. Nosotros preguntábamos por otro.

> **Comprobar la configuración no es comprobar la ejecución.** La única verificación que
> vale es buscar la capacidad **dentro de la sesión que hace el trabajo**.

Es exactamente la misma disciplina que la del disparo de una skill
([capítulo 04](04-frontmatter.md)): que el resultado salga bien no prueba que la skill se
cargara. Aquí: que la lista diga *conectado* no prueba que la sesión lo tenga.

### 3. Distingue la mención del uso

Al contar cuántas sesiones usaban un servidor, **25 de 26 lo «mencionaban» y 0 lo
invocaban**. La mención era el propio bloque de instrucciones del servidor, presente en
todas.

Y volvió a pasar al verificar: apareció una sesión con la capacidad aparentemente
declarada. Era la sesión desde la que se estaban escribiendo los comandos de búsqueda — la
cadena aparecía porque la habíamos escrito nosotros.

> **Buscar el nombre da el resultado contrario al real.** Cuenta invocaciones, no
> apariciones. Y desconfía especialmente cuando el recuento confirma lo que esperabas.

---

## El error de razonamiento, que fue mío

Cuando la primera comprobación salió vacía, publiqué esta conclusión:

> *"El servidor figuraba como conectado, no dio ningún error, y aportó cero herramientas a
> la sesión. Luego «Connected» no significa disponible."*

Los datos eran correctos. **La causa me la inventé.** El servidor sí aportaba herramientas
— en la carpeta donde estaba instalado. La explicación aburrida estaba a un comando de
distancia y no la busqué, porque la interesante ya encajaba.

> **Cuando una observación admite una causa mundana y otra publicable, la mundana se
> comprueba primero.** Si no, acabas enseñando una regla que no existe.

Es el fallo más fácil de cometer en material didáctico, porque **el incentivo empuja en esa
dirección**: la causa interesante se cuenta mejor. Aquí se detectó por una pregunta directa
—*"revísalo, no asumas"*— y no por ningún proceso.

---

## La lista de comprobación

Antes de dar por instalada cualquier capacidad y, sobre todo, **antes de medir con ella**:

1. **¿Con qué alcance quedó?** Global, por proyecto, o por directorio. Si no lo elegiste tú,
   lo eligió el valor por defecto.
2. **¿El sitio donde la instalaste es el mismo donde vas a trabajar?** Incluida la grafía
   exacta de la ruta.
3. **¿Tu sesión arrancó después de instalarla?** Una sesión toma su inventario al empezar y
   no lo vuelve a mirar.
4. **¿Aparece dentro de la sesión, no solo en la lista?** Es la única comprobación que
   responde a la pregunta real.
5. **Si vas a medir: ¿se ha invocado de verdad?** Una respuesta correcta no prueba que se
   usara.

Los cuatro primeros puntos habrían ahorrado seis pasadas.

---

## El coste que sí conviene contar

De todo el proceso, esto es lo que ninguna guía menciona y lo que de verdad decide si
merece la pena:

| | |
|---|---|
| Comandos hasta tenerlo funcionando | 6 |
| Errores por el camino | 2 explícitos, 3 silenciosos |
| Credencial | Un token guardado **en claro** en la configuración |
| Residuos tras el experimento | 3 entradas en 3 ámbitos distintos, cada una con el token |

El último punto es el más desagradable: **desinstalar no fue un comando, fueron tres**, y
solo porque llevábamos la cuenta de dónde habíamos escrito.

> **Si añadir algo es un comando y quitarlo son tres, no estabas contando bien el coste de
> añadirlo.**

---

## Cuándo NO aplica esto

- **Si el servidor lo instala y mantiene otra persona** —el equipo, la organización—, la
  parte de ámbitos no es tuya. La de comprobar dentro de la sesión sigue siéndolo.
- **Si no vas a medir nada**, los puntos 4 y 5 son opcionales. Todo lo que cuenta este
  capítulo aparece porque había una medición que podía salir mal en silencio; sin medición,
  una capacidad que no está simplemente no se usa y lo notas.
- **Los comandos y los nombres de los ámbitos caducan.** Están en el
  [anexo volátil](anexo-volatil.md), con fecha. El criterio de este capítulo, no.

---

## Lo que se lleva a cualquier herramienta

1. **«Instalado» es una propiedad de un ámbito, no de una máquina.**
2. **La configuración correcta y la ejecución correcta son dos comprobaciones distintas.**
3. **Ningún diagnóstico tiene por qué mentir para que llegues a la conclusión equivocada.**
4. **Cuenta usos, no apariciones.**
5. **Comprueba antes la causa aburrida que la interesante.**
6. **El coste de añadir incluye el de quitar.**
