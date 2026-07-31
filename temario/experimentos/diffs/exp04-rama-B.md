# Experimento 04, medida C — Rama B (con MCP de GitHub) ✅ válida

Cuarto intento, y el primero en el que el servidor llegó realmente a las sesiones. Los tres
anteriores están en [`exp04-rama-B-ANULADA.md`](exp04-rama-B-ANULADA.md).

**Condiciones:** sesión limpia por pasada · 31 de julio de 2026 · mismo prompt que la
[rama A](exp04-rama-A.md) · `github` instalado con `--scope user`.

**Verificación del disparo**, sobre las transcripciones:

| Pasada | Herramientas `mcp__github__*` declaradas | Invocaciones |
|---|---|---|
| B1 | 44 | 4 |
| B2 | 44 | 4 |
| B3 | 44 | 4 |

Las doce invocaciones son de la misma herramienta: `mcp__github__pull_request_read`.

---

## Resultado

| | B1 | B2 | B3 |
|---|---|---|---|
| Ruta | MCP | MCP | MCP |
| Llamadas al MCP | 4 | 4 | 4 |
| Llamadas de apoyo | 3 | 1 | 4 |
| Respuesta desbordada (161.848 car.) | Sí | No | Sí |
| Cifras de portada correctas | ✅ | ✅ | ✅ |
| Alguna cifra falsa | No | No | **Sí** |

Las tres dieron **+4.100 · −190 · 36 ficheros · 30 commits**, exactas. Ninguna pasada de la
rama A lo consiguió.

---

## El fallo de B3, que es el más informativo

B3 acertó el total y **erró el desglose que calculó ella misma**:

| | Cifra | Real | |
|---|---|---|---|
| Del objeto resumen del MCP | 36 ficheros | 36 | ✅ |
| Contada sobre la lista devuelta | 26 nuevos · 2 modificados · 2 eliminados | 32 · 2 · 2 | ❌ |

La lista venía **paginada a 30 de 36**. El script que escribió imprimió *"Total de
archivos: 30"* y la respuesta final presenta, sin advertirlo, un `36` de portada junto a un
desglose que suma `30`.

> **El número servido salió bien; el número calculado, mal.** En la misma pasada, con la
> misma herramienta y en la misma respuesta.

Comprobación:

```bash
$ gh api repos/franxiscodev/skills-base-project/pulls/1/files --paginate --jq '.[].status' | sort | uniq -c
     32 added
      2 modified
      2 removed
```

---

## El coste, en concreto

Dos de las tres pasadas recibieron una respuesta de **161.848 caracteres** que superó el
límite del turno. Las dos tuvieron que volcarla a fichero y procesarla aparte —una con
PowerShell tras fallar `jq`, otra con Python tras un `KeyError`—, lo que añadió entre dos y
cuatro llamadas.

`gh pr view --json <campos>` no se acercó a ese tamaño ni una vez, porque **obliga a elegir
qué se pide**.

> Cuatro llamadas y un desbordamiento frente a una llamada. La herramienta específica trae
> todo; la genérica te hace pedir lo que quieres — y pedirlo salió más barato.

---

## Salidas

Se conservan íntegras en las transcripciones de sesión:

| Pasada | Sesión |
|---|---|
| B1 | `0461c980-5ecf-499b-8d6d-679378925d91` |
| B2 | `855a2baf-0c70-4c19-aad7-a0b698ae01bf` |
| B3 | `21928dd5-527e-4e36-8ac8-f64b3eb3f540` |

**Nota de método:** al buscar estas sesiones aparece una cuarta con dos herramientas
`mcp__github__` «declaradas». Es la sesión de trabajo desde la que se hicieron las
comprobaciones, y es un **falso positivo**: la cadena aparece porque se escribió en los
propios comandos de búsqueda. El rastro válido es la invocación (`"name":"mcp__…"`), nunca
la mención — la misma distinción que separó 25 menciones de 0 usos en la
[medida B](../04-coste-de-un-mcp.md).
