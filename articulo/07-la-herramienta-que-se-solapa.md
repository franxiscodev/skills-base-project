# Entrega 7 — Ya tenía la herramienta. Instalé la que se solapaba

> **Formato:** post · **Base:** [exp 04](../temario/experimentos/04-coste-de-un-mcp.md)

Un solo número: **3 de 3**. El giro es que el resultado refutó mi propio argumento, y el
argumento estaba publicado.

## Para pegar

```text
Yo tenía un argumento cómodo para decidir si instalar un servidor MCP, y lo tenía escrito:

"Si ya hay una herramienta de línea de comandos que hace eso y el agente puede ejecutarla, el MCP añade contexto sin añadir capacidad."

Suena bien. Lo medí y salió al revés.

Monté las dos condiciones sobre la misma tarea: leer una pull request ya cerrada y contar qué la componía.

Sin el MCP, con solo el CLI: el agente fue al comando, tres de tres. Una sola llamada cada vez.

Con el MCP instalado, y el CLI seguía ahí, autenticado y disponible: el agente fue al MCP, tres de tres. Cuatro llamadas cada vez.

Ninguna pasada mezcló las dos rutas. Y en ningún momento le dije cuál usar.

Tener ya la herramienta no protege de instalar la que se solapa. La sustituye.

Y la elección no es tuya. Es suya.

Así que mi argumento sigue siendo cierto —no añade capacidad— y no sirve para lo que yo lo usaba. Si no aporta capacidad nueva, quítalo. Si lo dejas puesto, asume que va a ser el camino por defecto a partir de ese momento.

Un detalle más, del que salió la lección que más me está sirviendo.

En una de las pasadas con MCP, la respuesta traía dos cifras. El total de ficheros: correcto. El desglose entre nuevos, modificados y eliminados: mal.

El motivo es mecánico. El total venía servido por la herramienta. El desglose había que calcularlo contando una lista que llegaba paginada: 30 elementos de 36.

El número servido salía bien. El número calculado salía mal. No depende de la herramienta: depende de si el número viene hecho o hay que hacerlo.

Cuando instalas algo que se solapa con lo que ya tenías, ¿quién decide cuál se usa?
```

## Notas

- **Es la entrega donde te refutas a ti mismo en público**, y eso es lo que la hace
  circular. El argumento del «no añade capacidad» estaba escrito antes de medirlo.
- Los dos números —3/3 en cada rama— son inseparables: el de la rama sin MCP es lo que
  demuestra que el CLI funcionaba perfectamente.
- El cierre sobre número servido vs. número calculado es material aparte y podría ser su
  propia entrega. Va aquí porque salió de la misma medición; si el post se te hace largo,
  córtalo y guárdalo para más adelante.
- La muestra es pequeña y de una sola tarea de lectura. **No lo presentes como ley.**
