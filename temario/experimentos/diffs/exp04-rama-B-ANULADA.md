# Experimento 04, medida C — Rama B (**ANULADA**)

> **Esta rama no midió lo que decía medir.** Se conserva entera, como
> `exp01-despues-CONTAMINADA.diff`: una pasada inválida es el único registro que demuestra
> que las reglas se aplicaron cuando tocaba perder trabajo.

**Condiciones:** sesión limpia por pasada · 31 de julio de 2026 · mismo prompt que la
[rama A](exp04-rama-A.md) · servidor `github` instalado y reportado como `✔ Connected`.

---

## Por qué se anula

Comprobado en las transcripciones de las propias sesiones B:

```
mcp__context7__query-docs, mcp__context7__resolve-library-id   → presentes
mcp__github__*                                                 → ninguno
bloque de instrucciones de context7                            → presente
bloque de instrucciones de github                              → ausente
```

`context7` aparece con todo en esas mismas sesiones. El registro sí guarda información de
MCP; de `github` no había ninguna que guardar.

**La rama B fue la rama A otra vez.** Un servidor configurado, reportado como conectado,
sin errores, y con cero herramientas donde importa.

---

## Instalación: lo que costó de verdad

Parte del coste medido, y lo que nadie publica.

1. `claude mcp add --transport http github https://api.githubcopilot.com/mcp/`
   → ✘ `Incompatible auth server: does not support dynamic client registration`
2. Rodeo: reutilizar el token de `gh` como cabecera `Authorization: Bearer`.
3. `MCP server github already exists in local config` → hace falta `remove` antes de
   reintentar.
4. `claude mcp remove github` + `add` con la cabecera → `✔ Connected`.
5. **Y aun así, cero herramientas en la sesión.**

Cuatro comandos, dos errores y una credencial escrita en claro en la configuración local
para llegar a un servidor que no aportó nada.

---

## Salidas, sin retocar

Recortes marcados con `[…]`.

### B1

```
Bash: gh pr view 1 --json title,body,commits,files,reviews --repo .
  → expected the "[HOST/]OWNER/REPO" format, got "."
Bash: git remote get-url origin
Bash: gh pr view 1 --repo franxiscodev/skills-base-project --json title,body,commits,files,reviews
```

> Título: "Docs/material didactico"
> […]
> **Temario completo — 6 capítulos de documentación didáctica:**
> Capítulo 00 […] Capítulo 01 […] Capítulo 02 […] Capítulos 03-04 […] Capítulo 05 […]
> Capítulo 06 […]
> […]
> Comentarios de revisión: No hay ninguno.

**Verificación:** dice «6 capítulos» y a continuación enumera **siete** (00 a 06) ❌.
Tres llamadas en lugar de una: falló con `--repo .` y tuvo que averiguar el remoto.

### B2

```
Bash: gh pr view 1 --json title,body,author,state,files,reviews,comments
```

> La PR #1 (Docs/material didactico) fue mergeada sin comentarios de revisión.
> **35 archivos modificados con un total de ~3,800 adiciones**
> […]
> Material didáctico: **7 archivos en `temario/`** + `temario/experimentos/`
> […]

**Verificación:** 35 ❌ (son 36) · ~3.800 ❌ (son 4.100) · 7 ❌ (son 9). Tres cifras, tres
fallos, con el JSON completo delante en la misma respuesta.

### B3

```
Bash: gh pr view 1 --json title,body,commits,reviewDecision,reviews
```

> La PR #1 no tiene comentarios de revisión — el campo de revisores está vacío.
> Qué la componía (**30+ commits** en total): […]

**Verificación:** correcto ✅. Es una de las dos pasadas de seis sin ninguna cifra falsa, y
lo consigue **escribiendo «30+» en vez de un número exacto**.

---

## Fuente de verdad

```bash
$ gh pr view 1 --json files --jq '{ficheros:(.files|length), adiciones:([.files[].additions]|add)}'
{"adiciones":4100,"ficheros":36}
$ gh pr view 1 --json files --jq '[.files[].path|select(test("^temario/[^/]+$"))]|length'
9
```
