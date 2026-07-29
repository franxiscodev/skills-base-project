# GitHub CLI (`gh`)

`gh` es el cliente oficial de GitHub para la terminal. Evita tener que abrir el
navegador para crear PRs, revisar CI o leer issues.

Comprobar que está instalado y autenticado antes de usarlo:

```bash
gh auth status
```

Si no lo está, el usuario debe ejecutar `gh auth login` él mismo: es un flujo
interactivo con navegador y no se puede automatizar.

## Repositorios

```bash
gh repo view                    # datos del repo actual
gh repo view --web              # abrirlo en el navegador
gh repo clone <owner>/<repo>
gh repo create <nombre> --private --source=. --remote=origin
gh repo fork --clone            # fork de un repo ajeno + clon local
```

## Pull requests

```bash
gh pr create --fill                       # título y cuerpo desde los commits
gh pr create --title "..." --body "..."   # control total del contenido
gh pr create --draft                      # borrador: aún no pide revisión
gh pr create --base develop               # destino distinto de la branch por defecto

gh pr list                                # PRs abiertas del repo
gh pr status                              # las tuyas y las que te han asignado
gh pr view <n>                            # detalle
gh pr view <n> --web
gh pr diff <n>                            # ver el diff sin salir de la terminal
gh pr checkout <n>                        # traer la branch de una PR ajena para probarla
```

Revisión:

```bash
gh pr review <n> --approve
gh pr review <n> --request-changes --body "Falta manejar el caso de lista vacía"
gh pr review <n> --comment --body "..."
gh pr comment <n> --body "..."
```

Merge (ver `pull-requests.md` para elegir estrategia):

```bash
gh pr checks <n>                          # estado de CI — comprobar ANTES de mergear
gh pr merge <n> --squash --delete-branch
gh pr merge <n> --merge --delete-branch
gh pr merge <n> --rebase --delete-branch
```

## Issues

```bash
gh issue list
gh issue list --assignee @me
gh issue create --title "..." --body "..."
gh issue view <n>
gh issue close <n>
gh issue develop <n> --checkout      # crea una branch vinculada al issue
```

Para cerrar un issue automáticamente al mergear, incluir en el cuerpo del commit
o de la PR: `Closes #123` (también valen `Fixes #123` y `Resolves #123`).

## CI y GitHub Actions

```bash
gh run list                     # últimas ejecuciones de workflows
gh run watch                    # seguir en vivo la ejecución en curso
gh run view <id> --log-failed   # solo los logs de los pasos que fallaron
gh run rerun <id>
```

## Releases

```bash
gh release list
gh release create v1.2.0 --generate-notes    # notas a partir de las PRs mergeadas
gh release view v1.2.0
```

## Formato de salida para procesar

`gh` puede devolver JSON, útil cuando hay que leer un dato concreto en vez de
mostrárselo al usuario:

```bash
gh pr view <n> --json state,mergeable,reviewDecision
gh pr list --json number,title,author --limit 10
```
