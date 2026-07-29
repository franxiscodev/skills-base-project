# Recuperación: deshacer errores en Git

Regla general: **en Git casi nada se pierde de verdad mientras esté commiteado**.
Lo que sí se pierde sin remedio son los cambios del working tree que nunca
llegaron a un commit. Por eso, ante cualquier duda, el primer paso es siempre:

```bash
git status          # ¿hay algo sin commitear que se pueda perder?
git stash           # si lo hay, ponerlo a salvo antes de tocar nada
```

---

## Commit hecho en la branch equivocada (sin push)

El caso más frecuente. Has commiteado en `main` algo que debería ir en una branch.

```bash
# 1. Comprobar cuántos commits hay que mover
git log --oneline -5

# 2. Crear la branch: apunta al commit actual, con todo el trabajo dentro
git branch feature/nombre-correcto

# 3. Retroceder main hasta donde estaba
git reset --hard origin/main      # si main sigue al remoto
git reset --hard HEAD~1           # o retroceder N commits (aquí, 1)

# 4. Continuar en la branch nueva
git switch feature/nombre-correcto
```

**Por qué no se pierde nada:** el paso 2 crea una referencia a los commits *antes*
de mover `main`, así que siguen siendo alcanzables desde la branch nueva.

**Qué sí destruye el paso 3:** cualquier cambio sin commitear del working tree.
De ahí el `git stash` previo. Pedir confirmación explícita al usuario antes de
ejecutar `reset --hard`, siempre.

## Commit ya publicado que hay que deshacer

Con push hecho, **no** se reescribe la historia. Se publica un commit que hace lo
contrario:

```bash
git revert <hash>                 # crea un commit inverso
git revert <hash1>..<hash2>       # rango
git revert -m 1 <hash-de-merge>   # revertir un merge (1 = conservar la branch destino)
```

`revert` es seguro y colaborativo: no rompe el repositorio de nadie.

## `reset` vs `revert` vs `restore`

| Comando | Qué toca | Peligro |
|---|---|---|
| `git restore <archivo>` | Descarta cambios del working tree | Destructivo e irrecuperable |
| `git restore --staged <archivo>` | Saca del staging, conserva los cambios | Seguro |
| `git reset --soft <ref>` | Mueve la branch, conserva cambios en staging | Seguro |
| `git reset --mixed <ref>` | Mueve la branch, conserva cambios sin stagear | Seguro (por defecto) |
| `git reset --hard <ref>` | Mueve la branch y **borra** el working tree | Destructivo |
| `git revert <hash>` | Añade un commit que deshace otro | Seguro, apto para historia publicada |

## Corregir el último commit

Solo si **no** se ha hecho push:

```bash
git commit --amend -m "mensaje corregido"    # cambiar el mensaje
git add <archivo-olvidado> && git commit --amend --no-edit   # añadir un archivo
```

Si ya se hizo push, `--amend` obliga a un force push. Cuando la branch es propia
y nadie más trabaja en ella, es aceptable con `--force-with-lease` y confirmación
del usuario. Sobre una branch compartida, no.

## Traer un commit concreto de otra branch

```bash
git cherry-pick <hash>
git cherry-pick <hash1> <hash2>
git cherry-pick --abort           # si sale mal
```

Útil para llevar un hotfix de `main` a una branch de trabajo, o al revés.

## `reflog`: la red de seguridad

`git reflog` registra **todos** los movimientos de HEAD, incluidos los borrados
por `reset --hard`. Mientras Git no haya recolectado basura (semanas), todo es
recuperable:

```bash
git reflog                        # historial de posiciones de HEAD
git reset --hard HEAD@{3}         # volver a donde estaba hace 3 movimientos
git branch rescate <hash>         # o rescatar el commit a una branch nueva
```

Si el usuario cree haber perdido trabajo commiteado, este es el primer sitio donde mirar.

## Conflictos de merge

```bash
git status                        # lista los archivos en conflicto
```

En el archivo aparecen los marcadores:

```text
<<<<<<< HEAD
versión de la branch actual
=======
versión de la branch que se está integrando
>>>>>>> feature/otra
```

Procedimiento:

1. Mostrar al usuario las secciones enfrentadas de cada archivo.
2. Proponer una resolución que preserve la intención de **ambos** lados — no
   elegir un lado por comodidad.
3. Borrar los tres marcadores al editar.
4. Confirmar con el usuario **antes** de `git add`.
5. `git add <archivos>` y `git commit` (el mensaje de merge viene prerrellenado).

Para abandonar:

```bash
git merge --abort
git rebase --abort
```

## Limpiar archivos no rastreados

```bash
git clean -n -d      # SIEMPRE primero: simulacro, muestra qué se borraría
git clean -f -d      # borrado real — destructivo, requiere confirmación
```

## Se ha publicado un secreto

Si un token, clave o `.env` llega al remoto:

1. **Rotar la credencial inmediatamente.** Es lo único que de verdad importa.
2. Borrarla del código y añadir el patrón a `.gitignore`.
3. Limpiar el historial solo si es imprescindible (`git filter-repo`, BFG). Reescribe
   todos los hashes y afecta a todo el equipo — decisión del usuario, nunca automática.

Asumir siempre que un secreto publicado ya está comprometido, aunque el repo sea privado.
