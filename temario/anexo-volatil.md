# Anexo volátil — rutas, campos y versiones

> **Comprobado el 31 de julio de 2026.** Todo lo que hay en esta página **caduca**, y por
> eso está aquí y no repartido por los capítulos.

## Por qué existe este anexo

Un material sobre herramientas envejece por dos motivos muy distintos, y mezclarlos es lo
que hace que caduque entero cuando en realidad caducó una quinta parte:

| | Ejemplo | Caduca |
|---|---|---|
| **El criterio** | *"Escribe criterio de terminado, no lista de sitios"* | No |
| **La mecánica** | Dónde va el fichero, cómo se llama el campo | Sí, y sin avisar |

Los capítulos llevan lo primero. Esta página lleva lo segundo, con fecha.

> **Antes de impartir o publicar esto, verifica esta página en vivo.** Si algo no coincide,
> se corrige aquí y los capítulos siguen valiendo.

---

## Dónde viven las skills

```
<raíz del proyecto>/.claude/skills/<nombre>/
  SKILL.md
  references/          ← opcional
```

También existen skills de usuario, fuera del proyecto, en la carpeta personal de
configuración.

### Campos del frontmatter

```yaml
---
name: nombre-en-minusculas-con-guiones
description: Qué resuelve + cuándo usarla + disparadores literales.
---
```

- `name` coincide con el nombre de la carpeta.
- `description` es **lo único que está siempre en contexto**.

Ver el [capítulo 04](04-frontmatter.md) para el criterio de redacción, que no caduca.

---

## Dónde vive la memoria

Fuera del repositorio, en la carpeta personal de configuración, **indexada por proyecto**:

```
<carpeta personal>/.claude/projects/<ruta-del-proyecto-como-slug>/memory/
  MEMORY.md            ← índice; una línea por hecho, se carga en cada sesión
  <un-fichero>.md      ← un hecho por fichero; se carga solo si es relevante
```

Frontmatter de cada ficha:

```yaml
---
name: slug-en-kebab-case
description: Una línea. Es lo que decide si la ficha se carga.
metadata:
  type: user | feedback | project | reference
---
```

- Los ficheros se enlazan entre sí con `[[nombre]]`.
- El nombre de la carpeta del proyecto es su **ruta convertida en slug**.

**Consecuencia práctica que conviene saber:** la memoria de un proyecto **no está en el
repositorio**. No se comparte con el equipo al hacer `push`, y no la ve nadie más. Eso es
coherente con lo que guarda —hechos sobre ti— pero sorprende la primera vez.

---

## Servidores MCP: ámbitos y comandos

El criterio está en el [capítulo 07](07-instalar-una-capacidad.md). Aquí solo la mecánica,
que es lo que cambia.

### Los tres ámbitos

| Ámbito | Alcance | Dónde se guarda |
|---|---|---|
| `local` | **Solo ese directorio.** Es el valor por defecto | Configuración personal, indexada por ruta |
| `user` | Todos tus proyectos | Configuración personal, sección global |
| `project` | El repositorio, compartido con el equipo | Un fichero dentro del repo |

> ⚠️ **`local` es el valor por defecto y es el más fácil de equivocar.** Se resuelve por la
> ruta desde la que lanzas el comando, y **la ruta se compara como texto**: `C:/proyecto` y
> `c:/proyecto` son dos entradas distintas para la misma carpeta. Nos costó tres
> mediciones.

> ⚠️ **`project` escribe un fichero dentro del repositorio.** Si el servidor necesita un
> token, ese token acabaría commiteado. Para servidores con credencial, `user` o `local`.

### Comandos

```bash
claude mcp add --scope user --transport http <nombre> <url>   # instalar
claude mcp add ... --header "Authorization: Bearer $(...)"     # con credencial
claude mcp list                                               # sobre el directorio actual
claude mcp get <nombre>
claude mcp remove <nombre> [--scope user]                     # desde el mismo directorio
```

`claude mcp remove` sin `--scope` actúa sobre el ámbito `local` **del directorio en el que
estás**. Para limpiar de verdad hay que repetirlo en cada sitio donde se instaló.

### Cómo comprobar que una sesión lo tiene de verdad

El único método fiable, y el que no depende de ninguna interfaz:

- En una sesión interactiva, `/mcp` muestra los servidores **con el número de herramientas**.
  Cero herramientas y «conectado» pueden convivir.
- En las transcripciones de sesión, la capacidad aparece como `deferred_tools_delta` con los
  nombres. **Cuenta invocaciones** (`"name":"mcp__<servidor>__…"`), no menciones.

### Credenciales

Las cabeceras se guardan **en claro** en la configuración. Un token de `gh` reutilizado con
`$(gh auth token)` evita crear uno nuevo, pero queda escrito igual.

---

## `CLAUDE.md`

Se busca en la raíz del proyecto y en la carpeta personal de configuración. **Este
repositorio no tiene ninguno de los dos**, a propósito
([capítulo 01](01-tres-mecanismos.md)).

---

## Condiciones de las mediciones

Todos los números de los experimentos se obtuvieron con esto:

| | |
|---|---|
| **Fecha** | 30–31 de julio de 2026 |
| **Modelos** | Claude Opus 5 (medium) y Claude Haiku 4.5 (medium) |
| **Python** | 3.12 |
| **DuckDB** | 1.5.5 |
| **pytest** | 9.1.1 |
| **uv** | 0.7.9 |
| **Sistema** | Windows 11 |

> Los resultados con modelos generativos **varían entre ejecuciones**. Los experimentos
> documentan lo que ocurrió en estas condiciones, no una garantía. Si al repetirlo obtienes
> algo distinto, eso también es información: anótalo.

---

## Qué revisar cuando algo de aquí cambie

1. Corrige **solo esta página**.
2. Comprueba si algún capítulo cita una ruta o un campo concreto. Si lo hace, ese capítulo
   tenía material volátil mal colocado: muévelo aquí.
3. **Los números de los experimentos no se tocan.** Son un registro de lo que pasó en una
   fecha. Si las condiciones cambian, se repite la medición y se anota como una nueva.
