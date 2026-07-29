---
name: github-workflow
description: Flujo de trabajo con Git y GitHub — comprobaciones obligatorias antes de commitear y de hacer push, elección de branch, pull requests, merges, releases y recuperación de errores. Usar siempre que se vaya a commitear, crear o cambiar de branch, hacer push, pull, merge, abrir o revisar una PR, publicar una release o deshacer algo. Disparadores: "commit", "commitear", "push", "subir cambios", "pull request", "PR", "rama", "branch", "merge", "rebase", "release", "tag", "deshacer", "me equivoqué de rama", "conflicto".
---

# Flujo de trabajo Git y GitHub

Esta skill cubre **dónde** va el trabajo y **qué pasa después** del commit.
El **contenido del mensaje** de commit lo cubre la skill `git-conventional-commits`;
ambas se aplican a la vez cuando se va a commitear.

## Principio general

Git es fácil de deshacer en local y difícil de deshacer una vez publicado.
Por eso las comprobaciones se concentran en dos fronteras: **antes de commitear**
(¿estoy en el sitio correcto?) y **antes de hacer push** (¿esto es lo que quiero
publicar?). Entre esas dos fronteras se puede trabajar con soltura.

---

## Checkpoint A — antes de preparar un commit

Ejecutar siempre, sin excepción:

```bash
git branch --show-current
git status
```

Después, clasificar el cambio: ¿nueva funcionalidad, corrección, documentación
o mantenimiento?

**Si la branch actual es `main`, `master` o `develop` y el cambio es una feature
o un fix: detenerse y proponer una branch de trabajo antes de commitear.**

Proponerla con el nombre ya concreto y el motivo, por ejemplo:

> Estás en `main` y esto es una funcionalidad nueva. Sugiero crear
> `feature/filtro-por-fecha` antes de commitear, para que `main` se mantenga
> siempre estable y el cambio se pueda revisar por separado.
> ¿La creo? (`git switch -c feature/filtro-por-fecha`)

No crear la branch sin confirmación del usuario. Si el usuario prefiere commitear
directamente, aceptarlo sin insistir: es su repositorio y su decisión.

### Excepciones que NO deben disparar el aviso

Avisar cuando no toca convierte la regla en ruido y hace que se ignore siempre.
No avisar en estos casos:

- El commit raíz de un repositorio recién inicializado (no hay nada de donde ramificar).
- Cambios triviales de documentación o configuración (`docs`, `chore`) en un
  proyecto personal sin branches protegidas.
- El usuario ya ha dicho en esta sesión que quiere trabajar directamente sobre
  la branch principal.
- La branch actual ya es una branch de trabajo.

### Nombres de branch

- `feature/descripcion-corta` — funcionalidad nueva
- `fix/descripcion-del-bug` — corrección
- `hotfix/descripcion` — urgencia sobre producción
- `docs/`, `chore/`, `refactor/` — cuando aplique

Siempre kebab-case, en el mismo idioma que el resto del repositorio, y creadas
desde la branch principal actualizada.

---

## Checkpoint B — commit hecho en la branch equivocada

Situación frecuente y **completamente recuperable mientras no se haya hecho push**.
Ver [references/recuperacion.md](references/recuperacion.md) para el procedimiento
paso a paso.

Resumen: se crea la branch apuntando al commit actual y se retrocede la branch
principal. Como los commits quedan salvados en la branch nueva, no se pierde
trabajo — pero implica `git reset --hard`, que **sí** descarta los cambios sin
commitear del working tree. Comprobar `git status` antes y ofrecer `git stash`
si hay algo pendiente. Pedir confirmación explícita en todos los casos.

---

## Checkpoint C — antes de `git push`

Nunca hacer push a ciegas. Reunir primero esta información y mostrársela al usuario:

```bash
git branch --show-current                  # de dónde sale
git remote -v                              # a dónde va
git status -sb                             # ¿hay upstream configurado?
git log origin/<rama>..HEAD --oneline      # qué commits exactos se van a subir
```

Si la branch aún no tiene upstream, la comparación anterior falla; usar
`git log <rama-principal>..HEAD --oneline` en su lugar y avisar de que será el
primer push (`git push -u origin <rama>`).

Resumir al usuario en tres líneas —origen, destino, lista de commits— y **pedir
confirmación**. Levantar una alerta explícita si:

- El destino es `main`, `master`, `develop` o cualquier branch protegida.
- Aparecen commits cuyo autor no es el usuario.
- Van más commits de los esperados (indicio de una branch mal creada).

### Comandos que piden entrada interactiva

Un agente no puede escribir en un prompt interactivo: passphrases de SSH,
`gh auth login`, `git rebase -i` o cualquier editor que se abra. El intento
falla con un error engañoso — una passphrase no introducida se manifiesta como
`Permission denied (publickey)`, que parece un problema de claves.

Antes de una operación remota por SSH, comprobar si el agente tiene la clave cargada:

```bash
ssh-add -l          # "Error connecting to agent" o "no identities" = pedirá passphrase
```

Si va a pedirla, **no lanzar el comando**: avisar al usuario, darle el comando
escrito para que lo ejecute en su terminal y esperar su confirmación antes de
continuar. Ofrecer también la solución de fondo (cargar la clave en `ssh-agent`
una sola vez) para que los siguientes push no requieran intervención.

### Prohibido sin petición explícita

`git push --force` sobre una branch compartida. Si el usuario lo pide igualmente,
usar `git push --force-with-lease`, que aborta si alguien ha publicado algo
mientras tanto.

---

## Ciclo completo de trabajo

```bash
# 1. Partir de la branch principal actualizada
git switch main
git pull origin main

# 2. Branch de trabajo
git switch -c feature/nombre-descriptivo

# 3. Trabajar y commitear (ver skill git-conventional-commits)
git add <archivos-concretos>
git commit -m "feat(scope): descripción en imperativo"

# 4. Publicar la branch — pasando antes por el Checkpoint C
git push -u origin feature/nombre-descriptivo

# 5. Abrir la pull request
gh pr create --fill

# 6. Tras la revisión y con CI en verde
gh pr merge --squash --delete-branch
```

Detalles de PRs en [references/pull-requests.md](references/pull-requests.md)
y del CLI en [references/gh-cli.md](references/gh-cli.md).

---

## Reglas de colaboración

1. **No mergear con CI en rojo.** Comprobarlo con `gh pr checks` antes de proponer
   el merge.
2. **PRs pequeñas.** Si una PR toca más de ~400 líneas o mezcla asuntos distintos,
   proponer dividirla.
3. **No resolver conflictos a ciegas.** Mostrar las secciones enfrentadas y proponer
   una resolución que preserve la intención de ambos lados; confirmar antes de
   `git add`.
4. **Nunca publicar secretos.** Revisar el diff en busca de `.env`, claves, tokens
   o credenciales antes de cada push. Si algo así ya se ha publicado, avisar de
   que hay que **rotar la credencial**: borrarla del historial no basta.
5. **Idioma.** Detectar el idioma del historial existente (`git log --oneline -20`)
   y seguirlo en commits, branches y PRs.

---

## Referencias

- [references/gh-cli.md](references/gh-cli.md) — comandos de `gh` para PRs, issues y CI
- [references/pull-requests.md](references/pull-requests.md) — anatomía de una buena PR, squash vs merge vs rebase
- [references/releases-y-tags.md](references/releases-y-tags.md) — SemVer, tags y changelog
- [references/recuperacion.md](references/recuperacion.md) — deshacer errores, conflictos, `reflog`
