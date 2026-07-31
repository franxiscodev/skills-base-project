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

## 1. Que no quede ni una frase falsa

El criterio **no** es "actualiza el README". Es que **no quede ni una afirmación falsa
en el repositorio**. Suena a lo mismo y no lo es: medido, **6 de 6 tocaron el README y
0 de 6 lo dejaron verdadero**.

Dos preguntas, en este orden:

- [ ] **¿Qué afirmaciones acaba de volver falsas mi cambio? Búscalas, no las
      recuerdes.** Cualquier texto que diga cuántos pasos hay, en qué orden van o cuál
      es *"el único"* que hace algo. Empieza por el `README.md`, el docstring del
      módulo y los de las reglas vecinas — pero eso es **por dónde empezar a buscar**,
      no la lista de lo que hay que mirar. En la medición, la frase que más veces quedó
      falsa estaba justo en el sitio que nadie habría enumerado.
- [ ] **¿Es verdad lo que estoy añadiendo?** Si escribes una traza de consola,
      **ejecútala y copia la salida real**. Si añades una fila a la tabla de defectos,
      comprueba en `generar_datos.py` que ese defecto se fabrica de verdad.

> Medido: **3 de 6 metieron en el README una afirmación falsa que no existía antes de
> su cambio** — uno de ellos, en la misma respuesta en la que explicaba por qué era
> falsa. El riesgo no es solo dejarse algo: es escribir de más.

## 2. El test que se rompe si alguien afloja el criterio

Un test que demuestre que la regla funciona **no basta**. El que hace falta es el que
se pondrá **rojo** el día que alguien ensanche el criterio sin darse cuenta.

- [ ] Escríbelo, y después **rompe la regla a propósito** —ensancha el operador, mete
      un umbral, invierte la condición— y comprueba que ese test falla. Si sigue en
      verde, no protege nada, por mucho que se llame *"caso negativo"*.

Para elegir la fila: la que está **pegada al límite y del lado que se queda**. Una
fila cualquiera que la regla no toca no sirve — de esas hay infinitas y ninguna
demuestra nada.

Ejemplo del repo: `test_imputar_ciudad_no_descarta_la_venta`. Si mañana la imputación
se convierte en un descarte, ese test cae. Sin él, los demás siguen verdes y la
facturación cambia sola.

> Medido: **6 de 6** escribieron un caso negativo y solo **4 protegían el criterio**.
> El más flojo comprobaba que una venta de 15,50 € no vale cero: cierto, e inútil.

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
[ ] Ninguna frase del repo sobre el pipeline ha quedado falsa — buscadas, no recordadas
[ ] Ninguna frase que he añadido afirma algo que no he comprobado
[ ] Test de que la regla hace lo que debe
[ ] Test que se pone rojo si alguien afloja el criterio — comprobado rompiéndola
[ ] ¿Los datos de muestra ejercitan la regla? Si no, decirlo y ofrecer sembrarlo
```

## Cuándo dejar de usar esta skill

Si el patrón de `limpiar.py` cambia de forma —por ejemplo, si las reglas dejan de ser
funciones hermanas y pasan a ser clases o configuración— **esta skill deja de valer y
hay que rehacer la medición**. Lo que aquí se afirma no es una opinión: es el
resultado de un experimento con condiciones concretas, y esas condiciones caducan.
