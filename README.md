# base-project — Aprendiendo Skills y MCP en Claude Code

Repositorio de aprendizaje. El código que contiene (un pipeline de datos con
DuckDB) es el **terreno de práctica**: el objetivo real es entender dos formas de
extender Claude Code.

| Mecanismo | Qué aporta | Vive en |
|---|---|---|
| **Skills** | Le enseñan a Claude *cómo trabajas tú* | Este repo, `.claude/skills/` |
| **MCP** | Le dan a Claude *capacidades nuevas* | Config global, `~/.claude.json` |

La diferencia en una frase: una skill es **conocimiento** (instrucciones que Claude
lee), un MCP es **una herramienta** (algo que Claude ejecuta y que le devuelve datos
que no tenía).

> **El material didáctico está en [`temario/`](temario/)**: siete capítulos de criterio
> y los experimentos que lo sostienen, con las salidas reales de cada pasada. Este
> README explica **qué hay en el repo**; el temario explica **cómo se decidió**.
>
> Si vas con prisa: [el árbol de decisión](temario/02-arbol-de-decision.md) y
> [cuándo **no** escribir una skill](temario/05-cuando-no-escribir-una-skill.md).

---

## El proyecto de ejemplo

Un **mini-pipeline de datos**: genera un CSV de ventas, lo limpia con
[DuckDB](https://duckdb.org/), calcula unas métricas y emite un informe en Markdown.

```text
generar → cargar → limpiar → métricas → informe
```

### Por qué los datos vienen sucios a propósito

Esta es la parte que importa. `generar_datos.py` fabrica el CSV **con los defectos
de cualquier extracción real**:

| Defecto | La decisión que obliga a tomar |
|---|---|
| Fechas en `dd/mm/aaaa`, `aaaa-mm-dd` y `dd-mm-aaaa` | Normalizar a ISO, y qué hacer con lo que no parsea |
| Importes con coma y con punto decimal | Un único criterio de conversión numérica |
| Espacios sobrantes y mayúsculas inconsistentes | Normalizar antes de agrupar, o los grupos salen partidos |
| Filas duplicadas exactas | Deduplicar, y decidir por qué clave |
| Ciudad e importe ausentes | Qué se imputa, qué se descarta y qué se registra |
| Cantidades negativas (devoluciones) | Si restan del total o se cuentan aparte |
| Ventas con importe cero | Si son una venta o un apunte que no mueve dinero |

Cada uno de esos defectos se resuelve **siempre de la misma manera**. Y ahí está el
enlace con el resto del repositorio: una decisión que se repite igual cada vez es
justo lo que justifica escribir una skill en vez de explicárselo al agente otra vez.

Todo eso vive en [`src/pipeline/limpiar.py`](src/pipeline/limpiar.py), una función
por regla, con su test al lado.

### Ejecutarlo

Necesitas **Python 3.11+** y [uv](https://docs.astral.sh/uv/). Sin red, sin API
keys y sin permisos de administrador: los datos se fabrican en local.

`uv` se distribuye por PyPI, así que se instala como cualquier otro paquete —no
hace falta descargar un binario ni pedir permisos:

```bash
pip install uv
```

Y luego:

```bash
uv sync                    # crea el entorno e instala las dependencias
uv run python -m pipeline  # ejecuta el pipeline
```

`uv run` usa el entorno del proyecto sin que haya que activarlo a mano. Si tienes
`VIRTUAL_ENV` apuntando a otro sitio, `uv` avisa y usa el correcto.

Sale el informe en `datos/salida/informe.md` y un resumen por consola:

```text
Procesado
  cargar: 510 filas, sin descartes
  deduplicar: 510 → 500 (10 descartadas — filas idénticas en todas sus columnas)
  normalizar_texto: 500 filas, sin descartes
  convertir_tipos: 500 → 490 (10 descartadas — fecha, importe o cantidad ilegibles)
  descartar_importe_cero: 490 → 481 (9 descartadas — importe exactamente cero)
  imputar_ciudad: 481 filas, sin descartes
  marcar_devoluciones: 481 filas, sin descartes

Resultado
  Ventas ........... 472
  Devoluciones ..... 9
  Importe neto ..... 464.787,85 €
```

**El pipeline dice siempre qué descartó y por qué.** Un total de facturación sin
saber cuántas filas se quedaron fuera es un número que no se puede auditar.

Los tests:

```bash
uv run pytest
```

Y con Docker, si prefieres no instalar nada:

```bash
docker compose run --rm pipeline
```

### Es reproducible, y eso no es un detalle

El generador usa una semilla fija: **dos ejecuciones producen exactamente el mismo
CSV**. Sin eso no se puede escribir un test sobre los datos, ni repetir una demo, ni
comparar el informe de ayer con el de hoy.

```bash
uv run python -m pipeline --solo-generar
```

### Estado: es el terreno, no el objetivo

Este pipeline no aspira a crecer. Existe para tener *algo real* sobre lo que
practicar: cambios que commitear con Conventional Commits, un historial donde ver el
resultado, y un contexto donde las skills se disparen de verdad. Un repositorio
vacío no sirve para aprender un flujo de trabajo.

Lo interesante está en [`.claude/skills/`](.claude/skills/) y en el resto de este
README.

---

## Parte 1 — Skills

### Qué es una skill

Un archivo Markdown con instrucciones que Claude carga **solo cuando hacen falta**.
No es un prompt que repites en cada sesión ni algo que tengas que invocar a mano:
Claude lee la descripción, detecta que la tarea encaja y carga el contenido.

El problema que resuelve: sin skills, o repites tus convenciones en cada conversación,
o las metes en `CLAUDE.md` y ocupan contexto permanentemente aunque no toquen.

### Anatomía

```
.claude/skills/
├── git-conventional-commits/
│   ├── SKILL.md                    ← se carga al activarse
│   └── references/
│       └── comandos.md             ← se carga solo si hace falta
└── github-workflow/
    ├── SKILL.md
    └── references/
        ├── gh-cli.md
        ├── pull-requests.md
        ├── releases-y-tags.md
        └── recuperacion.md
```

Cada skill es **una carpeta** con un `SKILL.md` obligatorio. El nombre de la carpeta
es el nombre de la skill.

### El frontmatter es lo que decide todo

```yaml
---
name: git-conventional-commits
description: Flujo de trabajo Git con Conventional Commits — usar al crear commits,
  ramas, sincronizar con el remoto o revisar el historial. Se activa con "commit",
  "commitear", "crear rama", "branch", "push", "pull", "merge", "changelog".
---
```

Esta es **la parte más importante y la que más se subestima**. La `description` es
lo único que Claude ve antes de decidir si carga la skill o no. Si está mal escrita,
la skill existe pero nunca se activa.

Lo que funciona:

- Decir **cuándo** usarla, no solo qué es
- Incluir los **disparadores literales** que dirías tú ("commitear", "subir cambios")
- Cubrir sinónimos y las dos formas de decirlo: "rama" y "branch", "PR" y "pull request"
- Escribirla en el idioma en el que vas a hablarle

### Progressive disclosure

El patrón de los tres niveles, que es lo que mantiene el contexto bajo control:

1. **`description`** — siempre en contexto. Unas líneas.
2. **`SKILL.md`** — se carga al activarse la skill.
3. **`references/*.md`** — se cargan solo si Claude decide que los necesita.

Por eso `github-workflow` tiene el cheat sheet de `gh`, el detalle de las PRs y el
procedimiento de recuperación en archivos aparte: el 90% de las veces basta con el
`SKILL.md`, y el resto no se paga.

Los referencias se enlazan con Markdown normal desde el `SKILL.md`:

```markdown
Ver [references/recuperacion.md](references/recuperacion.md) para el procedimiento.
```

### Las tres skills de este repo

Están **deliberadamente separadas** por responsabilidad, y se aplican a la vez:

#### `git-conventional-commits` — el *qué* dice el commit

Formato del mensaje, los nueve tipos permitidos (`feat`, `fix`, `docs`, `style`,
`refactor`, `perf`, `test`, `build`, `ci`, `chore`), imperativo y minúscula, scope,
breaking changes con `!` y pie `BREAKING CHANGE:`.

#### `github-workflow` — el *dónde* va y el *qué pasa después*

Organizada en checkpoints, que es lo que la hace utilizable:

- **Checkpoint A** — antes de commitear: ¿en qué branch estoy? ¿debería ramificar?
- **Checkpoint B** — commit en la branch equivocada: cómo recuperarlo
- **Checkpoint C** — antes de push: origen, destino, commits exactos, confirmación

#### `pipeline-reglas-de-limpieza` — lo que el código **no** puede enseñar

La única que se escribió **después de medir si hacía falta**, y la más interesante
por lo que **no** dice: no describe cómo se escribe una regla —firma, `Recuento`,
encadenado, test—, porque se comprobó que el código ya lo enseña solo. Seis intentos
con dos modelos distintos, seis aciertos.

Cubre únicamente los tres puntos donde sí hubo fallos: qué otros ficheros hay que
actualizar, el test del caso que **no** debe verse afectado, y avisar cuando los
datos de muestra no ejercitan la regla nueva.

El experimento completo, con las salidas reales, está en
[`temario/experimentos/01-convenciones-pipeline.md`](temario/experimentos/01-convenciones-pipeline.md).

> **Escribir bien el código es la forma más barata de no necesitar una skill.**

### Lecciones aprendidas al escribirlas

**Separar responsabilidades funciona mejor que una skill gigante.** El contenido del
mensaje y el flujo de trabajo son cosas distintas. Cada `SKILL.md` referencia al otro
explícitamente para que Claude sepa que ambos aplican.

**Hay que escribir las excepciones, no solo las reglas.** `github-workflow` dedica una
sección entera a *cuándo NO avisar* de que estás en `main`:

> Avisar cuando no toca convierte la regla en ruido y hace que se ignore siempre.

Sin eso, la skill avisaría en el commit raíz de un repo nuevo o al tocar el README de
un proyecto personal — y acabarías ignorándola.

**Documentar los límites reales del agente.** Claude no puede escribir en un prompt
interactivo (passphrase de SSH, `gh auth login`, `git rebase -i`). Y el fallo es
engañoso: una passphrase no introducida aparece como `Permission denied (publickey)`,
que parece un problema de claves. La skill lo recoge y manda comprobar `ssh-add -l`
antes, para pasarte el comando en vez de intentarlo y fallar.

**Poner reglas no negociables explícitas.** Nunca `--force` sobre branch compartida,
nunca commitear una feature en `main`, siempre revisar el diff buscando secretos.

---

## Parte 2 — MCP (Context7)

### Qué es MCP

**Model Context Protocol**: un estándar para conectar Claude a herramientas y fuentes
de datos externas. Cada servidor MCP expone tools que Claude puede llamar.

### Qué resuelve Context7, en simple

Claude tiene una fecha de corte de conocimiento. Todo lo que una librería cambió
después de esa fecha, no lo sabe — pero **tampoco sabe que no lo sabe**, así que
puede responderte con total seguridad usando una API que ya no existe.

Context7 resuelve eso: antes de contestar sobre una librería, va a buscar su
documentación oficial **actual** y responde con eso. En lugar de tirar de memoria,
lee la fuente.

En la prueba con React se ve el mecanismo: primero resolvió `React` →
`/reactjs/react.dev`, y luego los ejemplos salieron de los archivos reales de
react.dev, no de su memoria.

### Instalación

```bash
claude mcp add --transport http --scope user context7 https://mcp.context7.com/mcp
```

Desglose de la decisión:

| Parte | Por qué |
|---|---|
| `--transport http` | Context7 ofrece endpoint HTTP remoto: no hay que instalar nada en local |
| `--scope user` | Documentación general → útil en todos los proyectos |
| `context7` | Nombre local del servidor |

#### Los tres scopes

| Scope | Dónde se guarda | Cuándo |
|---|---|---|
| `user` | `~/.claude.json` | Vale para todos tus proyectos |
| `project` | `.mcp.json` en el repo (se commitea) | El equipo entero lo necesita |
| `local` | Config del proyecto, sin commitear | Solo tú, solo aquí |

#### Verificar

```bash
claude mcp list          # todos los servidores y su estado
claude mcp get context7  # detalle de uno
```

```
context7:
  Scope: User config (available in all your projects)
  Status: √ Connected
  Type: http
```

### Las dos tools que expone

| Tool | Función |
|---|---|
| `resolve-library-id` | Traduce un nombre ("React") al ID de Context7 (`/reactjs/react.dev`) |
| `query-docs` | Trae documentación de esa librería sobre un tema concreto |

Siempre en ese orden: primero resolver el ID, luego consultar.

### Uso

No hace falta invocarlo explícitamente — Claude lo usa cuando detecta una pregunta
sobre una librería. Pero puedes forzarlo:

```
usa context7 para traerme la documentación actual de routing de Next.js
```

Consejo sobre las queries: **una consulta = un concepto**. `"React useEffect cleanup
function"` funciona; `"routing y auth y caching en Next.js"` no.

### Utilidades en el día a día

- **Documentación al día** de librerías que cambian rápido
- **APIs salidas después de la fecha de corte**
- **Migraciones entre versiones mayores**
- **Consulta de una versión concreta**, no "la última" — `/vercel/next.js/v14.3.0`
- **Menos APIs inventadas** y firmas de funciones incorrectas
- **Configuración exacta** de herramientas y build
- **Ejemplos de código sacados de la doc oficial**, no reconstruidos de memoria
- **Librerías de nicho** con poca presencia en el entrenamiento
- **Uso de CLIs** y sus flags reales
- **Servicios cloud y SDKs** con cambios frecuentes
- **Alternativa a buscar en la web**: va directo a la doc del proyecto
- **Onboarding a un stack** que no conoces
- **Menos saltos al navegador** durante la sesión

### Dónde no aporta

**Refactorizar tu propio código** · **Depurar lógica de negocio** · **Conceptos
generales de programación** · **Código escrito desde cero sin librerías** ·
**Librerías estables que llevan años sin cambiar**

Ese último caso es el de la prueba que hicimos: "cómo crear un componente funcional
en React" funcionó perfectamente, pero no aportó nada que Claude no supiera ya. La
diferencia real se nota con Server Components, hooks recientes como `use()` o
migraciones entre versiones mayores.

### Detalles prácticos

**Hay que reiniciar Claude Code.** Las tools MCP se cargan al arrancar la sesión. Si
instalas un servidor a mitad de conversación, no aparece hasta reiniciar.

**Funciona sin API key**, con rate limits más bajos. Si te quedas corto, la key gratuita
está en [context7.com/dashboard](https://context7.com/dashboard):

```bash
claude mcp remove context7 -s user
claude mcp add --transport http --scope user context7 https://mcp.context7.com/mcp \
  --header "CONTEXT7_API_KEY: tu-key"
```

**Verifica antes de instalar.** La forma habitual de instalarlo es
`npx ctx7@latest setup`, que descarga y ejecuta código. Merece la pena comprobar de
dónde viene:

```bash
npm view ctx7 description repository.url maintainers
# → 'Context7 CLI - Fetch documentation context and configure Context7'
# → git+https://github.com/upstash/context7.git
# → fahreddin.ozcan <fahreddin@upstash.com>
```

**El wizard `setup` es interactivo**, así que aplica lo mismo que documenta la skill
`github-workflow`: mejor el comando directo `claude mcp add`, que no pide nada por
consola.

---

## Estructura del repositorio

```
base-project/
├── .claude/
│   └── skills/
│       ├── git-conventional-commits/
│       │   ├── SKILL.md
│       │   └── references/comandos.md
│       ├── github-workflow/
│       │   ├── SKILL.md
│       │   └── references/
│       │       ├── gh-cli.md
│       │       ├── pull-requests.md
│       │       ├── releases-y-tags.md
│       │       └── recuperacion.md
│       └── pipeline-reglas-de-limpieza/
│           └── SKILL.md    ← la única escrita después de medir
├── temario/                ← el material didáctico: criterio y mediciones
│   ├── 00-la-tesis.md … 06-conversacion-nueva.md
│   ├── anexo-volatil.md    ← lo que caduca, separado a propósito
│   └── experimentos/       ← el método y las mediciones, con salidas reales
├── src/pipeline/
│   ├── generar_datos.py    ← fabrica el CSV sucio, con semilla fija
│   ├── cargar.py           ← DuckDB lee el CSV: todo como texto, a propósito
│   ├── limpiar.py          ← una regla por función. El corazón del ejercicio
│   ├── metricas.py
│   ├── informe.py
│   ├── recuento.py         ← trazabilidad de lo que se descarta
│   └── __main__.py
├── tests/
├── datos/                  ← generado, fuera de git
├── Dockerfile · compose.yaml
├── pyproject.toml · uv.lock
├── .gitignore
└── README.md
```

Las skills viven **en el repo** (versionadas, compartibles). El MCP vive en la config
**global** del usuario. Esa asimetría es intencional: las convenciones son del
proyecto, la capacidad de leer documentación es tuya.

## Comandos de referencia

```bash
# El pipeline
uv sync                               # instala dependencias
uv run python -m pipeline             # ejecuta el pipeline completo
uv run python -m pipeline --solo-generar   # solo fabrica el CSV
uv run pytest                         # tests
docker compose run --rm pipeline      # sin instalar nada en local

# Skills — no hay CLI: se crean como archivos en .claude/skills/
# Se activan solas por la description, o a mano como slash command:
#   /git-conventional-commits
#   /github-workflow

# MCP
claude mcp list                       # servidores y estado
claude mcp get <nombre>               # detalle
claude mcp add --transport http --scope user <nombre> <url>
claude mcp remove <nombre> -s user
```
