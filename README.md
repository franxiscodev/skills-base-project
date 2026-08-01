# base-project — economía de contexto en Claude Code

Casi todo lo que se publica sobre skills y MCP enseña a **añadir**: más servidores, más
herramientas, más capacidades. Este repositorio hace lo contrario y lo hace midiendo.

> **La habilidad que importa no es saber usar skills y MCP. Es saber decidir qué merece
> estar en la ventana de contexto.**

## Lo que se midió

| Resultado | Dónde |
|---|---|
| La skill que íbamos a escribir **no hacía falta**: 6/6 sin ella, dos modelos | [Exp 01](temario/experimentos/01-convenciones-pipeline.md) |
| Una skill **crea errores que antes no existían**: 0/6 → 3/6 afirmaciones falsas | [Exp 01](temario/experimentos/01-convenciones-pipeline.md) |
| **Cómo está redactada** cambia el resultado más que el contenido: 0/3 → 3/3 | [Exp 02](temario/experimentos/02-criterio-vs-lista.md) |
| Un punto que la skill no sostenía, **resuelto en 10 líneas de test** | [Exp 03](temario/experimentos/03-bajar-al-codigo.md) |
| Un servidor MCP conectado y no usado: **647 caracteres siempre, 0 invocaciones en 26 sesiones** | [Exp 04](temario/experimentos/04-coste-de-un-mcp.md) |
| Una skill propia, bien escrita y nunca cargada: **518 caracteres, 0 de 40 sesiones** | [Exp 05](temario/experimentos/05-la-skill-que-nunca-gana.md) |

Cada experimento guarda las salidas reales de cada pasada en
[`temario/experimentos/diffs/`](temario/experimentos/diffs/). Los que refutaron la
hipótesis están publicados igual — son los únicos que nadie más te va a contar.

## El método

> **Primero se mide sin la skill. Después se decide si hace falta. Solo entonces se
> escribe.**

Suena obvio y casi nadie lo hace, porque exige el paso incómodo: probar **sin** la
herramienta primero. Sin ese "antes", todo lo que instalas funciona — no tienes con qué
compararlo. Las once reglas completas están en la
[plantilla de experimento](temario/experimentos/PLANTILLA.md).

---

## El material

Los **capítulos** dan el criterio; los **experimentos** dan la prueba. Están separados
porque envejecen distinto.

| # | Capítulo | Contesta |
|---|---|---|
| [00](temario/00-la-tesis.md) | La tesis | Por qué restar |
| [01](temario/01-tres-mecanismos.md) | Los tres mecanismos de contexto | Qué hay disponible y qué cuesta cada uno |
| [02](temario/02-arbol-de-decision.md) | El árbol de decisión | Dónde va cada cosa |
| [03](temario/03-anatomia-de-una-skill.md) | Anatomía de una skill | Cómo se escribe para que funcione |
| [04](temario/04-frontmatter.md) | El frontmatter | Qué decide si tu skill llega a pasar |
| [05](temario/05-cuando-no-escribir-una-skill.md) | Cuándo **no** escribir una skill | Cuándo la respuesta es que no |
| [06](temario/06-conversacion-nueva.md) | Cuándo abrir una conversación nueva | La misma tesis, dentro de la sesión |
| [07](temario/07-instalar-una-capacidad.md) | Instalar una capacidad | Cuatro intentos, ningún error, tres mediciones perdidas |
| — | [Anexo volátil](temario/anexo-volatil.md) | Rutas, campos, comandos y versiones — lo que caduca, con fecha |

**Si solo vas a leer dos:** el [02](temario/02-arbol-de-decision.md) y el
[05](temario/05-cuando-no-escribir-una-skill.md).

---

## El terreno de práctica

Un **mini-pipeline de datos**: fabrica un CSV de ventas sucio, lo limpia con
[DuckDB](https://duckdb.org/), calcula métricas y emite un informe.

```text
generar → cargar → limpiar → métricas → informe
```

Los datos vienen sucios **a propósito** —fechas en tres formatos, importes con coma y con
punto, duplicados exactos, ciudades ausentes, devoluciones— porque cada defecto se
resuelve siempre de la misma manera, y **una decisión que se repite igual cada vez es
justo lo que justifica escribir una skill.** Sin un terreno así no hay nada que medir.

Todo eso vive en [`src/pipeline/limpiar.py`](src/pipeline/limpiar.py): una función por
regla, con su test al lado.

### Ejecutarlo

Necesitas **Python 3.11+** y [uv](https://docs.astral.sh/uv/) (`pip install uv`). Sin red,
sin API keys y sin permisos de administrador: los datos se fabrican en local.

```bash
uv sync                                    # entorno y dependencias
uv run python -m pipeline                  # el pipeline completo
uv run python -m pipeline --solo-generar   # solo fabrica el CSV
uv run pytest                              # 21 tests
docker compose run --rm pipeline           # sin instalar nada en local
```

El informe sale en `datos/salida/informe.md`, y por consola el recuento de lo descartado:

```text
  deduplicar: 510 → 500 (10 descartadas — filas idénticas en todas sus columnas)
  convertir_tipos: 500 → 490 (10 descartadas — fecha, importe o cantidad ilegibles)
  descartar_importe_cero: 490 → 481 (9 descartadas — importe exactamente cero)
```

**El pipeline dice siempre qué descartó y por qué.** Un total de facturación sin saber
cuántas filas se quedaron fuera es un número que no se puede auditar.

El generador usa **semilla fija**: dos ejecuciones producen el mismo CSV. Sin eso no se
puede escribir un test sobre los datos, ni repetir una demo, ni comparar dos experimentos.

---

## Estructura

```text
base-project/
├── .claude/skills/          ← las convenciones: versionadas, del proyecto
│   ├── git-conventional-commits/
│   └── pipeline-reglas-de-limpieza/   ← la única escrita después de medir
├── temario/                 ← criterio (capítulos) y prueba (experimentos)
│   └── experimentos/diffs/  ← las salidas reales, byte a byte
├── articulo/                ← la divulgación, versionada aquí y no en la plataforma
├── src/pipeline/            ← generar · cargar · limpiar · métricas · informe
├── tests/
└── datos/                   ← generado, fuera de git
```

Las skills viven **en el repo**; los servidores MCP, en la configuración **del usuario**.
La asimetría es intencional: las convenciones son del proyecto, las capacidades son tuyas.

> **Este repositorio tuvo tres skills y tiene dos.** La tercera se borró tras medir que en
> 40 sesiones no se cargó ni una vez. Restar también es un resultado.
