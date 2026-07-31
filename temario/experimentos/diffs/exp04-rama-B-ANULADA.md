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

**La causa:** `claude mcp add` usa scope `local` por defecto, que se guarda **por
directorio**. El comando se lanzó desde otra carpeta, así que el servidor quedó configurado
en `C:\proyectos\devspell` y `C:/Users/Francisco`, y **no** en el repositorio donde corrían
las pasadas.

`claude mcp list` decía `✔ Connected` y era cierto — sobre la carpeta desde la que se
lanzó.

**La rama B fue la rama A otra vez**, con el servidor existiendo en un sitio y las sesiones
ejecutándose en otro.

> ⚠️ **Corrección.** La primera versión de este documento atribuía la ausencia a que el
> servidor *"estaba conectado y no aportaba ninguna herramienta"*, y sacaba de ahí que
> «Connected» no significa disponible. **Era falso.** Las transcripciones decían lo que yo
> leí; lo inventado fue la causa. Se corrigió al comprobar dónde estaba realmente
> configurado, que era un solo comando.

---

## Instalación: lo que costó de verdad

Parte del coste medido, y lo que nadie publica.

1. `claude mcp add --transport http github https://api.githubcopilot.com/mcp/`
   → ✘ `Incompatible auth server: does not support dynamic client registration`
2. Rodeo: reutilizar el token de `gh` como cabecera `Authorization: Bearer`.
3. `MCP server github already exists in local config` → hace falta `remove` antes de
   reintentar.
4. `claude mcp remove github` + `add` con la cabecera → `✔ Connected`.
5. **Y aun así, cero herramientas en las sesiones** — porque los pasos 1 a 4 se ejecutaron
   desde otra carpeta, y el scope por defecto es por directorio.

Cuatro comandos, dos errores y una credencial escrita en claro en la configuración local,
para acabar con el servidor instalado donde no se iba a medir.

> El paso 5 es el que más enseña: **ninguno de los cuatro anteriores dio el menor indicio
> de que algo fuera mal.** El único síntoma estaba a un directorio de distancia.

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
