# Releases, tags y versionado semántico

Aquí es donde Conventional Commits deja de ser una convención estética y empieza
a servir para algo: los tipos de commit determinan el número de versión y generan
el changelog.

## Versionado semántico (SemVer)

Formato `MAJOR.MINOR.PATCH`, por ejemplo `2.4.1`:

| Se incrementa | Cuándo | Tipo de commit que lo provoca |
|---|---|---|
| **MAJOR** (`2.0.0`) | Cambio incompatible: el código que usaba la versión anterior deja de funcionar | Cualquier commit con `!` o con pie `BREAKING CHANGE:` |
| **MINOR** (`1.3.0`) | Funcionalidad nueva compatible hacia atrás | `feat` |
| **PATCH** (`1.2.4`) | Corrección compatible hacia atrás | `fix` |

Los demás tipos (`docs`, `style`, `refactor`, `test`, `chore`, `ci`, `build`) no
incrementan versión por sí solos, aunque sí aparecen en el historial.

Antes de `1.0.0` la API se considera inestable y las reglas se relajan: es
habitual que los breaking changes suban solo la MINOR.

## Tags

Un tag es un nombre fijo apuntando a un commit concreto. Para releases se usan
siempre **tags anotados** (`-a`), que guardan autor, fecha y mensaje:

```bash
git tag -a v1.2.0 -m "Versión 1.2.0"
git tag                                # listar
git tag -n                             # listar con mensaje
git show v1.2.0                        # ver el commit etiquetado

git push origin v1.2.0                 # los tags NO se suben con un push normal
git push origin --tags                 # subir todos los pendientes
```

Convención: prefijo `v` (`v1.2.0`), coincidiendo con el campo `version` de
`package.json` u equivalente.

Borrar un tag ya publicado rompe a quien lo haya descargado. Requiere
confirmación explícita:

```bash
git tag -d v1.2.0                      # local
git push origin --delete v1.2.0        # remoto
```

## Publicar una release en GitHub

```bash
gh release create v1.2.0 --generate-notes
```

`--generate-notes` construye las notas automáticamente a partir de las PRs
mergeadas desde la release anterior — otra razón para que los títulos de PR
estén bien escritos.

Con notas propias:

```bash
gh release create v1.2.0 --title "1.2.0 — Filtros avanzados" --notes-file CHANGELOG-1.2.0.md
gh release create v1.2.0 --prerelease        # beta / RC
```

## Generar el CHANGELOG

Manualmente, agrupando por tipo:

```bash
git log v1.1.0..HEAD --oneline --no-merges
```

Automáticamente, con herramientas que leen Conventional Commits:

```bash
npx standard-version          # sube versión + tag + CHANGELOG.md en un paso
npx conventional-changelog -p angular -i CHANGELOG.md -s
```

Estructura habitual del archivo:

```markdown
## [1.2.0] - 2026-07-29

### Features
- **listado:** añadir filtro por rango de fechas (#42)

### Bug Fixes
- **api:** corregir error 500 con formularios vacíos (#45)

### BREAKING CHANGES
- El endpoint `/users` ahora exige el parámetro `page`.
```

## Checklist antes de publicar una release

1. `main` actualizada y con CI en verde.
2. Versión actualizada en `package.json` (o equivalente) y commiteada como
   `chore(release): v1.2.0`.
3. CHANGELOG revisado por una persona: lo genera la herramienta, pero lo lee un humano.
4. Tag anotado creado y subido.
5. Release publicada.
