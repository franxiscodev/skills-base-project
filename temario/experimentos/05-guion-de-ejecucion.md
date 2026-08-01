# Experimento 05 — guion de ejecución

> Operativo. El diseño y las hipótesis están en
> [05-la-skill-que-nunca-gana.md](05-la-skill-que-nunca-gana.md) y **no se tocan** una vez
> empezadas las pasadas.

## Por qué en un clon y no aquí

Las pasadas tienen que **quitar y reescribir skills**, y una de ellas parte de commits
puestos a propósito en la rama equivocada. Hacer eso en el repositorio de trabajo es pedir
un accidente.

Se ejecuta sobre un clon desechable. Trae las tres skills consigo —están commiteadas— y sus
transcripciones caen en un directorio de proyecto **distinto**, lo que además deja el
recuento limpio: ahí dentro solo hay sesiones del experimento.

```bash
CLON="$TMP/exp05"   # cualquier ruta fuera del repositorio
git clone c:/APRENDER/ClaudeCode/base-project "$CLON"
cd "$CLON" && git log --oneline -1     # anotar este commit en el experimento
```

⚠️ **Anota la grafía exacta de la ruta del clon.** Es la que da nombre al directorio de
transcripciones, y ya nos costó tres mediciones en el
[experimento 04](04-coste-de-un-mcp.md).

---

## El estado de partida de cada pasada

Idéntico en las diez. Desde el clon, antes de abrir la sesión:

```bash
git checkout -- . && git clean -fd && git switch main
printf 'Nota de trabajo pendiente de archivar.\n' > NOTAS.md
```

Queda un fichero sin trackear y el árbol por lo demás limpio. Es cambio real y desechable.

---

## Las pasadas

**Sesión nueva para cada una** — la sesión toma su inventario de skills al arrancar y no lo
vuelve a mirar ([capítulo 07](../07-instalar-una-capacidad.md)). Si editas una `description`
con la sesión abierta, estás midiendo la anterior.

### Rama A — control (3 pasadas)

Nada instalado ni retirado. Prompt exacto:

```text
Commitea los cambios que hay pendientes.
```

### La sonda diagnóstica (1 pasada, solo aquí)

Prepara commits en la rama equivocada y pregunta por su disparador exclusivo:

```bash
git add NOTAS.md && git commit -m "chore: nota de trabajo"
```

```text
Me equivoqué de rama, estos commits tenían que ir en otra.
```

> **Si aquí tampoco se dispara**, la competencia no explica nada y la hipótesis principal
> cae. La rama B se ejecuta igual, para tener el 0/3 registrado en vez de deducido.

### Rama B — sin competencia (3 pasadas)

```bash
rm -rf .claude/skills/git-conventional-commits
```

Mismo prompt que la rama A, carácter por carácter.

### Rama C — redacción (3 pasadas)

Se restaura la skill retirada y se sustituye **solo** la línea `description:` de
`github-workflow` por la reescrita.

⚠️ **La nueva `description` se pega en el experimento antes de ejecutar esta rama.** Se
redacta a partir del criterio del [capítulo 04](../04-frontmatter.md), no a partir de lo
que hayan dado A y B.

Mismo prompt.

---

## Cómo se lee cada pasada

Al terminar, sobre la transcripción de esa sesión:

```bash
grep -o '"name":"Skill","input":{"skill":"[a-z-]*"' <sesion>.jsonl
```

Se anota **qué skill salió y en qué orden**. Que no aparezca ninguna también es un
resultado.

⚠️ **No cuentes apariciones del nombre.** Solo vale la forma completa de la llamada
([regla 10](PLANTILLA.md)).

Y el diff de cada pasada a [`diffs/`](diffs/) como `exp05-<rama>-<n>.diff`, antes de
limpiar el árbol para la siguiente. Sin diff no hubo pasada.

---

## Al terminar

1. Rellenar las tablas del experimento y **conservar la hipótesis aunque haya fallado**.
2. Aplicar la decisión pre-registrada: reescribir la `description` en el repositorio real,
   o borrar la skill.
3. Si el mecanismo se confirma, **reescribir el pasaje del
   [capítulo 04](../04-frontmatter.md)** que da el solapamiento por resuelto.
4. Borrar el clon.
