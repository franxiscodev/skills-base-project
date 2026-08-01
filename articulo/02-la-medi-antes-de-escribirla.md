# Entrega 2 — La medí antes de escribirla, y no hacía falta

> **Formato:** post · **Base:** [exp 01](../temario/experimentos/01-convenciones-pipeline.md)

Un solo número: **falló las cinco predicciones**. El error que creó la skill va en la
entrega 3, no aquí.

## Para pegar

```text
La entrega anterior acababa en que me puse a contar. Esto es lo que me llevó a hacerlo.

Tenía el candidato perfecto para una skill.

Un pipeline de datos en Python con una convención estricta: cada regla de limpieza es una función propia, con su test y su recuento de filas descartadas. Aplicada cinco veces en el código y escrita en ninguna parte.

Justo lo que se supone que resuelve una skill: lo escribes una vez y dejas de repetirlo en cada conversación.

Antes de escribirla hice algo que casi nadie hace. La medí sin escribirla.

Sesión limpia, sin ninguna pista, un prompt de una línea: "Añade al pipeline una regla que descarte las ventas con importe cero".

Y escribí mi hipótesis ANTES de ejecutar nada. Cinco predicciones concretas sobre lo que iba a hacer mal: meterlo dentro de otra función, sin recuento, sin encadenarlo donde tocaba, sin test.

Falló las cinco.

Tres pasadas de tres. Función propia, recuento correcto, encadenada en su sitio, dos tests cada una. Y un comentario explicando por qué la regla va después de la conversión de tipos y no antes: porque mientras el importe es texto, "0,00" y "0" son cadenas distintas.

Había deducido la convención leyendo el código. La skill que iba a escribir no hacía falta.

Lo incómodo no es eso. Es que sin ese "antes" la habría escrito, habría funcionado, y habría dado por hecho que servía. No tenía con qué compararla.

Escribir bien el código es la forma más barata de no necesitar una skill.

¿Has probado alguna vez a hacer la tarea sin la herramienta, antes de construir la herramienta?
```

## Notas

- **Enlaza con la entrega 1 en la primera línea.** Es la única del arco que lo hace
  explícitamente, porque es un salto atrás en el tiempo y sin eso desconcierta.
- El detalle del `"0,00"` está a propósito: es lo que demuestra que el agente **razonó** el
  orden de los pasos, no que acertó por casualidad. Sin ese detalle, el resultado suena a
  suerte.
- **Cita «3 de 3», nunca «6 de 6».** Hubo seis pasadas en total y una no conserva su
  salida; según las reglas del propio método, esa pasada no ocurrió.
