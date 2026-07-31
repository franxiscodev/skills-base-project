# Diffs de las pasadas

El registro en bruto de cada pasada de los experimentos. **No son documentación: son la
prueba.** Cada número publicado en un experimento se puede recontar aquí.

## Por qué están dentro del repositorio

Al principio no lo estaban. Vivían en el disco, fuera del proyecto, con el argumento
razonable de que *"son registro de la medición, no código"*.

Ese argumento era correcto y la decisión estaba mal:

> **Un experimento cuyas pruebas no viajan con el material es un experimento que hay que
> creerse.** Quien clone el repositorio podía leer que el test *"caza 6 de 6 fallos y no da
> un falso positivo en 12 ejecuciones correctas"* y no tenía forma de comprobarlo.

Se descubrió por las malas: hicieron falta tres búsquedas para encontrarlos, y en medio
llegué a darlos por perdidos. Si a quien los guardó le cuesta eso, a un lector le es
imposible.

Por eso la [regla 7 del método](../PLANTILLA.md) ya no dice solo *guarda el diff*: dice
**dónde**.

## Qué hay

| Ficheros | Experimento | Qué registran |
|---|---|---|
| `exp01-pasada-1..5.diff` | [01](../01-convenciones-pipeline.md) | El "antes", sin skill. **Falta la sexta** ([aviso](../01-convenciones-pipeline.md#condiciones-y-reproducibilidad)) |
| `exp01-despues-opus-1..3.diff`<br>`exp01-despues-haiku-1..3.diff` | [01](../01-convenciones-pipeline.md) | El "después", con skill, dos modelos |
| `exp01-despues-CONTAMINADA.diff` | [01](../01-convenciones-pipeline.md) | **Pasada anulada.** Se conserva a propósito |
| `exp02-haiku-1..3.diff`<br>`exp02-opus-2/3.diff`<br>`exp02-opus-desempate.diff` | [02](../02-criterio-vs-lista.md) | Skill reescrita como criterio |

## La pasada anulada

`exp01-despues-CONTAMINADA.diff` no cuenta para ningún número y **no se borra**.

Una pasada inválida es el único registro que demuestra que las reglas se aplicaron cuando
tocaba perder trabajo. Un experimento donde nada se anuló nunca no prueba rigor: prueba que
nadie miró.

## Cómo leerlos

```bash
git apply --stat temario/experimentos/diffs/exp02-haiku-1.diff   # qué tocó
git apply --check temario/experimentos/diffs/exp02-haiku-1.diff  # si aplica limpio
```

Aplican sobre el commit de partida que indica cada experimento en su sección de
condiciones, no sobre `main`.
