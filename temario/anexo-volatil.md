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
