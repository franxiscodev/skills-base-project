# Guion de ejecución — Medida C del experimento 04

> Para ejecutar a mano. Cada pasada es una **sesión nueva**. Yo no puedo hacerlas: una
> sesión no puede abrirse a sí misma en limpio.
>
> Documento operativo. El diseño y la interpretación están en
> [04-coste-de-un-mcp.md](04-coste-de-un-mcp.md) y **no se tocan** a partir de aquí.

---

## Enmienda al pre-registro (regla 11: antes de ejecutar)

La tarea pre-registrada era *"abrir una PR desde una rama con cambios y comprobar su
estado"*. **No sirve, y hay que cambiarla antes de tocar nada.**

**El motivo:** abrir una PR exige `push`, y en esta máquina la clave SSH pide passphrase.
El agente se quedaría bloqueado esperando una entrada interactiva. Eso no mediría qué ruta
elige: mediría quién tropieza antes con el mismo obstáculo, que es el mismo para los dos.

> **Una tarea con un bloqueo común a las dos condiciones no distingue entre ellas.**
> Además ensuciaría el repositorio con seis PRs de prueba.

**La tarea nueva es de solo lectura.** Pierde el escenario de escritura y gana tres cosas:
sin efectos secundarios, sin passphrase, y repetible tantas veces como haga falta sobre un
objeto que no cambia.

Sigue midiendo lo que importa: **con dos caminos disponibles para lo mismo, ¿cuál coge?**

---

## Preparación (una vez)

```bash
git -C c:/APRENDER/ClaudeCode/base-project log --oneline -1   # anota el SHA
git -C c:/APRENDER/ClaudeCode/base-project status --short     # tiene que estar limpio
claude mcp list                                               # NO debe salir github
```

**Requisito de la rama A:** que el MCP de GitHub **no esté instalado**. Si aparece, párate.

---

## El prompt exacto

Idéntico en las seis pasadas, carácter por carácter. No añadas nada, no respondas a
preguntas más allá de lo imprescindible, y **no menciones ni `gh` ni MCP**.

```text
En este repositorio hay una pull request ya mergeada, la número 1. Dime qué
la componía y si alguien dejó comentarios de revisión.
```

Está redactado a propósito **sin nombrar ninguna herramienta**. Si el prompt dijera `gh`,
la elección de ruta estaría dictada por el enunciado y la medida no valdría nada — es la
misma razón por la que el [experimento 01](01-convenciones-pipeline.md) nunca nombra
`generar_datos.py`.

---

## Rama A — sin MCP de GitHub (3 pasadas)

Por cada pasada: **sesión nueva**, pega el prompt, deja terminar, y anota.

| Pasada | ¿Termina bien? | Ruta elegida | Nº de llamadas a herramienta | Notas |
|---|---|---|---|---|
| A1 | | | | |
| A2 | | | | |
| A3 | | | | |

**"Ruta elegida"** es literalmente qué ejecutó: `gh pr view 1`, `git log`, `WebFetch`…
Cópialo tal cual, no lo resumas.

---

## Entre A y B — instalar

```bash
claude mcp add --transport http github https://api.githubcopilot.com/mcp/
claude mcp list          # comprobar que sale conectado
```

Requiere autorizar por OAuth, y **eso lo tienes que hacer tú en una sesión interactiva**:
yo no puedo completar ese flujo.

**Anota dos cosas**, que son parte del coste medido y casi nadie las cuenta:

- Cuánto tardó la instalación de principio a fin, autorización incluida: **______**
- Si hizo falta crear algún token o permiso: **______**

---

## Rama B — con MCP de GitHub (3 pasadas)

Mismo prompt. Sesión nueva cada vez.

| Pasada | ¿Termina bien? | Ruta elegida | Nº de llamadas | ¿Usó el MCP? |
|---|---|---|---|---|
| B1 | | | | |
| B2 | | | | |
| B3 | | | | |

⚠️ **"Usó el MCP" se comprueba por la invocación, no por el resultado.** Una respuesta
correcta no prueba que lo usara. La huella válida es una llamada a una herramienta cuyo
nombre empiece por `mcp__github__`. Es la misma disciplina que la del disparo de una skill
([capítulo 04](../04-frontmatter.md)) — y la trampa exacta que la
[regla 10](PLANTILLA.md) obliga a evitar.

---

## Después: medir el peaje y desinstalar

**Antes de quitarlo**, mide lo mismo que se midió para `context7`, o se pierde el dato:

```bash
# el bloque de instrucciones del servidor github, en caracteres
# (mismo procedimiento que la medida A: buscarlo en el prompt de sistema
#  de cualquier transcripción de una sesión de la rama B)
```

Y entonces sí:

```bash
claude mcp remove github
claude mcp list          # confirmar que ya no está
```

---

## Cómo recojo yo los resultados

Pégame las seis tablas rellenas y, si puedes, la respuesta de una pasada de cada rama
**sin retocar**. Con eso cierro la medida C y el experimento 04 entero.

Si alguna pasada sale rara —se cuelga, pregunta algo, se va por otro lado— **no la
descartes**: anótala tal cual. La pasada anulada del
[experimento 01](01-convenciones-pipeline.md) resultó ser de lo más informativo que salió
de toda la campaña.
