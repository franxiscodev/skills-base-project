# base-project — Aprendiendo Skills y MCP en Claude Code

Repositorio de aprendizaje. El código que contiene (un visualizador de precios de
Bitcoin y Ethereum) es la **excusa**: el objetivo real es entender dos formas de
extender Claude Code.

| Mecanismo | Qué aporta | Vive en |
|---|---|---|
| **Skills** | Le enseñan a Claude *cómo trabajas tú* | Este repo, `.claude/skills/` |
| **MCP** | Le dan a Claude *capacidades nuevas* | Config global, `~/.claude.json` |

La diferencia en una frase: una skill es **conocimiento** (instrucciones que Claude
lee), un MCP es **una herramienta** (algo que Claude ejecuta y que le devuelve datos
que no tenía).

---

## El proyecto de ejemplo

Un script de consola que consulta la API pública de
[CoinGecko](https://www.coingecko.com/en/api) y muestra el precio en euros de Bitcoin
y Ethereum con su variación en 24 horas.

### Ejecutarlo

Necesitas **Node.js 18 o superior** (usa `fetch` nativo). No hay dependencias que
instalar ni API key que configurar:

```bash
npm start
# o directamente
node index.js
```

### Salida

```
Precios de criptomonedas — fuente: CoinGecko

┌─────────┬──────────────────┬───────────────┬────────────────┬──────────────────┬───────────┐
│ (index) │ Criptomoneda     │ Precio (EUR)  │ Cambio 24h (%) │ Cambio 24h (EUR) │ Tendencia │
├─────────┼──────────────────┼───────────────┼────────────────┼──────────────────┼───────────┤
│ 0       │ 'Bitcoin (BTC)'  │ '56.394,00 €' │ '+1.07 %'      │ '595,42 €'       │ '▲ sube'  │
│ 1       │ 'Ethereum (ETH)' │ '1671,00 €'   │ '+0.50 %'      │ '8,37 €'         │ '▲ sube'  │
└─────────┴──────────────────┴───────────────┴────────────────┴──────────────────┴───────────┘
Variación en las últimas 24 horas:
  ▲ sube  Bitcoin (BTC)    +1.07 %
  ▲ sube  Ethereum (ETH)   +0.50 %
```

Todo vive en un único archivo, [`index.js`](index.js): construcción de la URL, la
petición, el formateo con `Intl.NumberFormat` y el render con `console.table`.

Si ves un error `429`, has superado el límite de peticiones de CoinGecko: espera un
minuto. El script lo detecta y lo explica en vez de soltar el error crudo.

### Estado: congelado a propósito

**Este código no se va a seguir desarrollando.** No le faltan features por descuido —
es que nunca fue el objetivo.

Existe para tener *algo real* sobre lo que practicar: cambios que commitear con
Conventional Commits, un historial donde ver el resultado, un contexto donde las
skills se disparen de verdad. Un repositorio vacío no sirve para aprender un flujo
de trabajo de Git.

Así que no busques aquí tests, arquitectura por capas ni configuración: lo interesante
está en [`.claude/skills/`](.claude/skills/) y en el resto de este README.

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

### Las dos skills de este repo

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

### Qué resuelve Context7 en concreto

Claude tiene una fecha de corte de conocimiento. Todo lo que una librería cambió
después, no lo sabe — pero **tampoco sabe que no lo sabe**, así que puede responderte
con seguridad usando una API que ya no existe.

Context7 va a buscar la documentación oficial **actual** de la librería antes de
responder. Lee la fuente en vez de tirar de memoria.

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

### Cuándo aporta y cuándo no

**Sí aporta**

- Librerías que cambian rápido
- APIs posteriores a la fecha de corte
- Migraciones entre versiones mayores
- Consultar una versión concreta (`/vercel/next.js/v14.3.0`)
- Menos APIs inventadas y firmas incorrectas
- Configuración exacta de herramientas y build
- Librerías de nicho con poca presencia en el entrenamiento
- Flags reales de CLIs

**No aporta**

- Refactorizar tu propio código
- Depurar lógica de negocio
- Conceptos generales de programación
- Librerías estables que llevan años igual

Probamos con "cómo crear un componente funcional en React" y funcionó — pero es
justo el caso donde no aporta: eso lleva años sin cambiar.

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
│       └── github-workflow/
│           ├── SKILL.md
│           └── references/
│               ├── gh-cli.md
│               ├── pull-requests.md
│               ├── releases-y-tags.md
│               └── recuperacion.md
├── bases/
│   └── git_conventional_commits_skill_plan.md
├── .gitignore
└── README.md
```

Las skills viven **en el repo** (versionadas, compartibles). El MCP vive en la config
**global** del usuario. Esa asimetría es intencional: las convenciones son del
proyecto, la capacidad de leer documentación es tuya.

## Comandos de referencia

```bash
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
