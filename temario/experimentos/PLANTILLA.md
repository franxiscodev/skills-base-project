# Plantilla de experimento

> Cópiala para cada experimento nuevo. **No la edites**: si el método cambia, se
> discute y se cambia aquí a propósito, no de refilón dentro de un experimento.

---

## Para qué existe este formato

Casi todo el material que circula sobre skills sigue este guion: se escribe la
skill, se prueba, funciona, se publica. Falta el paso que da sentido a todo lo
demás.

> **Nadie enseña el "antes".** Y sin el "antes" no hay forma de saber si la skill
> aportó algo o si el agente ya lo hacía bien.

Este formato obliga a medir antes de construir. Tiene un efecto incómodo y
deliberado: **a veces el experimento demuestra que la skill no hacía falta.** Ese
resultado se publica igual. Es el más valioso de los dos, porque es el único que
nadie más va a contarte.

---

## Reglas del método

1. **El "antes" se ejecuta en una sesión limpia.** Si el agente ya tiene el
   contexto de la conversación donde diseñamos la convención, no está actuando sin
   la skill: está actuando con la skill dictada de viva voz. El resultado no valdría
   nada.
2. **El "antes" se repite tres veces.** Los modelos no son deterministas: una sola
   pasada puede acertar por casualidad. Si de tres falla una, ya hay señal; si
   acierta tres de tres, probablemente no necesitas la skill.
3. **El prompt del "antes" y el del "después" son idénticos, carácter por
   carácter.** Si cambian, no se está comparando lo mismo.
4. **Las salidas se pegan sin retocar.** Se pueden recortar (marcando el recorte
   con `[…]`), nunca mejorar.
5. **Se registran las condiciones**: fecha, modelo, versiones. Un experimento sin
   condiciones no es reproducible ni refutable.
6. **Si el resultado contradice la hipótesis, se publica igual.**

---

## La plantilla

```markdown
# Experimento NN — <lo que se prueba>

**Hipótesis:** <qué esperamos que falle sin la skill. Una frase, escrita ANTES
de ejecutar nada.>

## El problema

Qué duele, en dos o tres frases. Sin teoría todavía.

## 1. Antes: sin skill

**Prompt exacto:**

​```text
<literal, copiable, el mismo que se usará después>
​```

**Condiciones:** sesión limpia · <fecha> · <modelo> · <versiones relevantes>

| Pasada | Resultado | Qué falló |
|---|---|---|
| 1 | | |
| 2 | | |
| 3 | | |

**Salida representativa** (sin retocar, recortada con `[…]`):

​```
<pegar aquí>
​```

**Diagnóstico:** qué hizo mal, y sobre todo **por qué era predecible que lo hiciera
mal**. Si no falló, decirlo aquí y saltar a "Qué aprendimos".

## 2. ¿Merece una skill?

Los tres filtros del árbol de decisión, respondidos para este caso concreto:

| Filtro | Respuesta | Motivo |
|---|---|---|
| ¿Le pasaría igual a otra persona? | | |
| ¿Va a volver a ocurrir? | | |
| ¿El agente lo haría mal sin ella? | | |

**Destino elegido:** skill / memoria / código / test / linter / README / nada.
Y por qué no cualquiera de los otros.

## 3. La skill

Enlace al fichero + las decisiones de escritura que importan:

- **La `description`**, palabra por palabra: qué disparadores lleva y por qué.
  Es lo único que el agente ve antes de decidir si la carga.
- Qué se dejó **fuera** a propósito.
- Qué va en `references/` en lugar de en el `SKILL.md`, y con qué criterio.

## 4. Después: con skill

**Mismo prompt exacto.**

**Condiciones:** sesión limpia · <fecha> · <modelo>

| Pasada | ¿Se disparó la skill? | Resultado |
|---|---|---|
| 1 | | |
| 2 | | |
| 3 | | |

**Salida representativa:**

​```
<pegar aquí>
​```

**Qué cambió:** comparación concreta, no impresiones. Lista de diferencias
observables.

⚠️ **Comprobar que se disparó de verdad.** Que el resultado sea bueno no prueba
que la skill se cargara: puede haber acertado igual. Si no se disparó, el problema
está en la `description`, no en el cuerpo.

## Qué aprendimos

Lo generalizable. Lo que sirve aunque no uses este proyecto ni este lenguaje.

## Cuándo NO hacer esto

El límite. En qué situaciones esta skill sobra, molesta o se queda obsoleta.
**Un capítulo sin esta sección está vendiendo, no enseñando.**

## Condiciones y reproducibilidad

- **Fecha:**
- **Modelo:**
- **Versiones:** <lenguaje, librerías, herramientas>
- **Cómo repetirlo:** los pasos exactos para que otra persona lo reproduzca.

> Los resultados con modelos generativos **varían entre ejecuciones**. Este
> registro documenta lo que ocurrió en las condiciones indicadas, no una garantía.
> Si al repetirlo obtienes algo distinto, eso también es información: anótalo.
```

---

## Errores que este formato busca evitar

| Error | Cómo lo evita |
|---|---|
| Escribir la skill y asumir que aportó | Obliga al "antes", tres veces |
| Comparar peras con manzanas | Exige prompt idéntico |
| Confundir "salió bien" con "se disparó la skill" | Lo comprueba por separado |
| Material que caduca entero | Aísla versiones en "Condiciones" |
| Vender en vez de enseñar | Exige la sección "Cuándo NO hacer esto" |
