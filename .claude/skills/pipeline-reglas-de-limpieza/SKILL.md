---
name: pipeline-reglas-de-limpieza
description: Qué hay que actualizar además del código al añadir, cambiar o quitar una regla de limpieza del pipeline de datos — los sitios que no se ven desde limpiar.py. Usar cuando se pida "añade una regla", "descarta las filas que...", "filtra las ventas...", "quita esa regla", "cambia el criterio de limpieza", o al tocar src/pipeline/limpiar.py.
---

# Al tocar una regla de limpieza del pipeline

## Lo que esta skill NO dice, y por qué

**No describe cómo se escribe la regla.** Ni la firma, ni que devuelva `Recuento`,
ni que se encadene en `limpiar()`, ni que lleve test.

Eso ya lo enseña el propio código: `limpiar.py` tiene las reglas aplicadas una tras
otra, con la misma forma. Se midió — seis intentos, dos modelos distintos, **seis
aciertos sin una sola desviación** ([experimento 01](../../../temario/experimentos/01-convenciones-pipeline.md)).
Repetirlo aquí sería pagar contexto por algo que ya está resuelto.

Esta skill cubre **solo lo que el código no puede mostrar**, que es exactamente
donde apareció toda la variación.

---

## 1. Los otros sitios

Una regla nueva no vive solo en `limpiar.py`. Antes de dar el trabajo por terminado:

- [ ] **`README.md`** — la traza de ejemplo de la salida por consola lleva una línea
      por paso. Si añades o quitas un paso y no la tocas, el README pasa a mentir.
- [ ] **El docstring del módulo** `limpiar.py` — enumera las reglas en orden y dice
      cuáles descartan filas. Es lo primero que lee quien llega al fichero.
- [ ] **El docstring de las reglas vecinas**, si tu cambio las convierte en falsas.
      Varias se describen por contraste con las demás —*"clasifica, no elimina"*,
      *"la única que descarta"*— y esas frases caducan cuando entra una regla nueva.

> Medido: **1 de 6** actualizó el README por su cuenta. Es el punto más frágil.

## 2. El caso negativo

Un test que demuestre que la regla funciona **no basta**. Hace falta el otro:

- [ ] Un test que compruebe que la regla **no toca lo que no debe tocar.**

Ejemplo del repo: `imputar_ciudad` tiene el test de que rellena la ciudad ausente,
y además `test_imputar_ciudad_no_descarta_la_venta`, que comprueba que la fila
**sigue ahí**. El segundo es el que impide que mañana alguien convierta la
imputación en un descarte sin que nadie se entere: los tests seguirían en verde y
la facturación cambiaría.

Para escribirlo, pregúntate qué fila está **cerca del límite de tu regla pero
fuera de él**, y protégela.

**El primer test protege la funcionalidad. El segundo protege el criterio de
negocio**, que es el que de verdad cuesta reconstruir.

> Medido: **3 de 6** escribieron el caso negativo.

## 3. El aviso sobre los datos de muestra

- [ ] Comprueba si el CSV que genera `generar_datos.py` **contiene** el defecto que
      tu regla trata.

Si no lo contiene, la regla descartará 0 filas y el pipeline **no demuestra nada**:
pasa por ahí sin ejercitarse, y el informe se ve idéntico con la regla y sin ella.

Cuando ocurra, **dilo explícitamente** y ofrece sembrar el defecto en el generador —
pero no lo hagas sin permiso: cambia los totales del informe de referencia y rompe la
comparación con ejecuciones anteriores.

> Medido: **3 de 6** lo detectaron sin que se lo pidieran.

---

## Checklist final

```
[ ] README.md actualizado si cambia el número o el orden de los pasos
[ ] Docstring del módulo actualizado
[ ] Docstrings vecinos que hayan quedado falsos
[ ] Test de que la regla hace lo que debe
[ ] Test de que NO hace lo que no debe
[ ] ¿Los datos de muestra ejercitan la regla? Si no, avisar
```

## Cuándo dejar de usar esta skill

Si el patrón de `limpiar.py` cambia de forma —por ejemplo, si las reglas dejan de ser
funciones hermanas y pasan a ser clases o configuración— **esta skill deja de valer y
hay que rehacer la medición**. Lo que aquí se afirma no es una opinión: es el
resultado de un experimento con condiciones concretas, y esas condiciones caducan.
