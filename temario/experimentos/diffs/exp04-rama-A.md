# Experimento 04, medida C — Rama A (sin MCP de GitHub)

Salidas sin retocar. Recortes marcados con `[…]`. Prueba de la tabla de la
[medida C](../04-coste-de-un-mcp.md).

**Condiciones:** sesión limpia por pasada · 31 de julio de 2026 · commit `6e98ee7`

**Prompt, idéntico en las tres:**

```text
En este repositorio hay una pull request ya mergeada, la número 1. Dime qué
la componía y si alguien dejó comentarios de revisión.
```

---

## A1

```
Bash: gh pr view 1 --json title,body,state,reviews,commits
```

> PR #1 — Información
> Estado: Mergeada (MERGED)
> Título: "Docs/material didactico"
> Descripción: Vacía (sin descripción en la PR)
> Revisiones: Ninguna — no hay comentarios de revisión
>
> **Commits que la componían (30 commits)**
> […]
> Experimentos validados (3 experimentos):
> Exp 01: ¿Hace falta una skill para limpiar el README? (**6/6 sin skill, 0/6 correcto con
> skill**)
> […]

**Verificación:** 30 commits ✅. El `0/6 correcto con skill` ❌ **no existe en ninguna
fuente**: el experimento 01 registra 6/6 de cobertura con la skill y 3/6 de afirmaciones
falsas. Cifra inventada.

---

## A2

```
Bash: gh pr view 1 --json title,body,commits,reviews,comments
```

> La PR #1 "Docs/material didactico" no tiene comentarios de revisión registrados
> (comments: [] y reviews: [] vacíos).
>
> Incluye **28 commits** que cubren:
> […]
> Fue todo tu trabajo —mergeado sin revisores externos.

**Verificación:** 28 ❌ — son 30. El dato estaba en el JSON que acababa de leer.

---

## A3

```
Bash: gh pr view 1 --json title,body,files,reviews,author,mergedBy,state
```

> La PR #1 (Docs/material didactico) fue mergeada por ti mismo y contenía:
> […]
> 9 archivos de temario en `temario/` […] y experimentos (3 análisis prácticos)
> 1 skill completo: `pipeline-reglas-de-limpieza`
> […]
> **Sobre comentarios de revisión**
> No hay reviews: La PR no tiene comentarios de revisión de nadie.

**Verificación:** correcto. Pidió `files` en lugar de `commits`, así que **no llegó a dar
ninguna cifra de commits** — y es la única pasada sin una cifra equivocada.

---

## Fuente de verdad

```bash
$ gh pr view 1 --json commits --jq '.commits | length'
30
$ gh pr view 1 --json reviews,comments --jq '{reviews:(.reviews|length), comments:(.comments|length)}'
{"comments":0,"reviews":0}
```

Comprobado el 31 de julio de 2026, fuera de las pasadas.
