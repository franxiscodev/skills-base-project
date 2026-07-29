# Pull requests

Una pull request (PR) es una propuesta de cambio: "he hecho esto en mi branch,
revísalo y, si está bien, intégralo en la principal". Es el punto donde el trabajo
pasa de ser tuyo a ser del proyecto.

## Antes de abrirla

```bash
git switch main && git pull origin main    # traer lo último
git switch <tu-branch>
git merge main                             # integrar y resolver conflictos AQUÍ, no en la PR
git push -u origin <tu-branch>
```

Resolver los conflictos en local antes de abrir la PR ahorra trabajo a quien
revisa y evita que la PR aparezca bloqueada.

## Anatomía de una buena descripción

```markdown
## Qué hace
Añade un filtro por rango de fechas al listado de operaciones.

## Por qué
Los usuarios con más de 500 operaciones no podían encontrar las de un mes
concreto (issue #42).

## Cómo probarlo
1. `npm start`
2. Abrir el listado y seleccionar "últimos 30 días"
3. Comprobar que solo aparecen operaciones de ese rango

## Notas
El filtro se aplica en cliente. Si el volumen crece habrá que moverlo al backend.

Closes #42
```

Reglas prácticas:

- El **título** sigue el mismo formato que un commit: `feat(listado): añadir filtro por fechas`.
- El **porqué** importa más que el qué: el qué ya se ve en el diff.
- Incluir siempre **cómo probarlo**. Quien revisa no conoce el contexto.
- Vincular el issue con `Closes #N`.
- Si hay cambios visuales, adjuntar captura.

## Tamaño

Una PR de 100 líneas recibe comentarios útiles; una de 2.000 recibe un "LGTM"
sin leer. Si la PR mezcla asuntos distintos (por ejemplo un refactor y una
funcionalidad nueva), dividirla en dos: se revisan mejor y se revierten mejor.

## Estrategias de merge

GitHub ofrece tres botones. No son intercambiables:

| Estrategia | Qué hace en `main` | Cuándo usarla |
|---|---|---|
| **Squash and merge** | Todos los commits de la branch se funden en **uno solo** | Por defecto. Ideal si la branch tiene commits de trabajo ("wip", "arreglar typo") |
| **Create a merge commit** | Conserva todos los commits + añade un commit de merge | Cuando cada commit de la branch es significativo y quieres conservar el detalle |
| **Rebase and merge** | Reaplica los commits sobre `main`, sin commit de merge | Historial lineal conservando commits. Reescribe hashes |

Recomendación para proyectos pequeños: **squash** casi siempre. Deja un historial
en `main` donde cada línea es una funcionalidad completa, y encaja perfectamente
con Conventional Commits — el mensaje del squash es el que acaba en el changelog,
así que hay que revisarlo antes de confirmar (GitHub lo prerrellena con el título
de la PR).

## Después del merge

```bash
git switch main
git pull origin main
git branch -d <tu-branch>              # borrar la branch local ya integrada
```

La branch remota se borra sola si se usó `--delete-branch` en `gh pr merge`.

`git branch -d` se niega a borrar una branch no integrada; ese error es una
protección, no un obstáculo que saltar con `-D`.

## Responder a una revisión

- Cada comentario merece respuesta: aplicar el cambio o explicar por qué no.
- Los cambios pedidos van en **commits nuevos** sobre la misma branch, no
  reescribiendo los anteriores: así el revisor ve solo lo que cambió desde su
  última lectura. El squash final los unificará de todos modos.
- Un `git push` a la branch actualiza la PR automáticamente. Pasa igualmente por
  el Checkpoint C.
