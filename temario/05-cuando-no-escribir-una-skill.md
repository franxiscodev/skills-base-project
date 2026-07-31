# 05 — Cuándo **no** escribir una skill

> **Evidencia:** [experimento 01](experimentos/01-convenciones-pipeline.md) ·
> [experimento 02](experimentos/02-criterio-vs-lista.md) ·
> [experimento 03](experimentos/03-bajar-al-codigo.md)

## El capítulo que falta en todo el material que vas a leer

Busca cualquier guía sobre skills y encontrarás siempre la misma forma: aquí tienes el
formato, aquí un ejemplo, mira qué bien funciona. Nunca verás una skill que se escribió,
se midió y se tiró a la basura.

No es mala fe. Es que **para contar ese caso hay que haber medido antes de escribir**, y
casi nadie lo hace. Sin el "antes" no hay ningún resultado negativo que contar: todo lo
que escribes funciona, porque no tienes con qué compararlo.

> **Este capítulo existe porque en este repositorio la primera skill que íbamos a
> escribir resultó innecesaria, y la segunda cosa que le metimos dentro tuvo que salir.**

Las dos veces lo dijo la medición, no el criterio.

---

## Los cinco casos

| No la escribas cuando… | Porque… | Dónde va |
|---|---|---|
| El código ya lo enseña | Cinco ejemplos aplicados ganan a una descripción | **El código** |
| Hay un sitio más barato que la sostiene | Un test no gasta contexto y no se olvida | **Test / linter** |
| Es un hecho sobre ti o sobre este proyecto | No le pasa a cualquiera haciendo la misma tarea | **Memoria** |
| La forma del proyecto va a cambiar pronto | Envejece antes de dispararse por primera vez | **Nada, todavía** |
| No puedes medir el "antes" en limpio | Sin comparación, la skill es una creencia | **Nada, todavía** |

Los tres primeros son de destino: el conocimiento existe y va a otro sitio. Los dos
últimos son de momento: quizá sí, pero no ahora.

---

### 1. Cuando el código ya lo enseña

Este es el caso que más veces se va a dar, y el que más cuesta creer sin datos.

`limpiar.py` sigue una convención estricta —*una regla = una función = un test = un
recuento*— aplicada cinco veces y **escrita en ninguna parte**. El candidato perfecto a
skill. Se midió antes: mismo encargo, sesión limpia, seis veces, dos modelos.

| Lo que diría la skill | ¿Lo hace mal sin ella? | Medición |
|---|---|---|
| Una función propia con la misma firma | No | 6/6 |
| Devolver el recuento con su motivo | No | 6/6 |
| Encadenarla en el sitio correcto | No | 6/6 |
| Escribir su test | No | 6/6 |

Seis de seis, sin una desviación, **incluido el modelo pequeño**. Escribir esa skill
habría sido pagar contexto por algo que el repositorio ya resolvía solo.

> **Lo que el código muestra, el código lo enseña.** Un fichero enseña sus propios
> patrones porque están a la vista y repetidos. Una skill que repite lo que el código ya
> comunica añade contexto sin añadir criterio.

Compruébalo con las skills que ya tengas: si la tuya describe algo que se puede leer
abriendo un fichero fuente, sobra.

### 2. Cuando hay un sitio más barato que lo sostenga

*"Mantén el README diciendo la verdad"* parecía trabajo de skill. Se escribió. Se midió.

| Deja el README verdadero | Sin skill | Skill como lista | Skill como criterio |
|---|---|---|---|
| Modelo grande | — | 0/3 | **3/3** |
| Modelo pequeño | — | 0/3 | 1/3 |

Reescribirla arregló el techo y no arregló el suelo. Así que ese punto **salió de la
skill** y bajó a un test de diez líneas que compara la traza documentada con la salida
real del pipeline. Validado contra los dieciocho diffs guardados: caza los 6 fallos y no
da un falso positivo en las 12 ejecuciones correctas.

> **La skill sube el techo. El código sube el suelo.** Si no controlas quién ejecuta —y
> en un equipo nunca lo controlas—, el punto tiene que bajar a algo que no dependa del
> lector.

El criterio para repartir no es la importancia:

> **Lo que tiene una salida observable baja al test. Lo que exige juicio sobre una
> intención se queda en la skill.**

### 3. Cuando es un hecho sobre ti, no sobre la tarea

*"No me ejecutes `git push`, la clave SSH pide passphrase"* es verdad sobre **esta**
máquina. A cualquier otra persona haciendo la misma tarea no le pasa. Eso es memoria, no
skill: si lo metes en una skill, lo estás publicando como si fuera criterio general.

La pregunta que lo resuelve en un segundo: **¿le pasaría igual a otra persona haciendo
esto mismo?** Si no, no es una skill.

### 4. Cuando el proyecto va a cambiar de forma pronto

Una skill que describe una estructura inestable **envejece antes de dispararse por
primera vez**. Y envejece en silencio: nadie revisa una skill que no se ha activado
nunca, así que el día que por fin se dispare dirá algo que dejó de ser verdad hace meses.

Si estás en medio de una refactorización, la respuesta no es "no", es "todavía no".

### 5. Cuando no puedes medir el "antes" en limpio

Sin comparación no sabes si la skill aportó algo o si el agente ya lo hacía bien. Y el
sesgo va siempre en la misma dirección: escribes, pruebas, sale bien, concluyes que
funcionó.

En el experimento 01 la hipótesis de partida **falló en las cinco predicciones**. Si no
llegamos a medir el "antes", habríamos escrito una skill inútil y celebrado que
funcionaba.

---

## Lo que cuesta una skill que no hace falta

El argumento de siempre es *"y si sobra, no pasa nada: no se dispara"*. No es cierto, y
tiene dos partes muy distintas.

### La parte barata: el índice

De cada skill instalada hay algo **permanentemente en contexto**: su `description`. No es
mucho por skill, pero:

- **compite** con las buenas cuando el agente decide cuál cargar;
- envejece sin que nadie la mire;
- da **falsa sensación de control** — *"está documentado"* no es *"se aplica"*.

> **Una skill que no se dispara nunca es peor que no tenerla.** El conocimiento está en
> tu cabeza y no en la del agente, pero tú crees que sí está.

### La parte cara, y esta no la cuenta nadie

**Una skill causa fallos propios, no solo aciertos.**

Con la skill de limpieza puesta, tres pasadas de seis metieron en el README una fila
falsa: afirmaban que el generador fabricaba ventas con importe cero, en la misma
respuesta en la que explicaban que no las fabricaba.

Sin la skill, esa mentira apareció **cero veces**. No porque el agente fuera más
cuidadoso: porque 5 de 6 **ni tocaban el README**, así que no tenían ocasión de mentir en
él.

| | Sin skill | Con skill |
|---|---|---|
| Toca el README | 1/6 | 6/6 |
| Mete una afirmación falsa | 0/6 | 3/6 |

La skill subió la cobertura del 17 % al 100 % y **creó un error que antes no existía**.

> **Ninguna evaluación que solo cuente aciertos vería ese coste.** Y contar solo aciertos
> es lo que hace todo el mundo, porque para ver lo otro hace falta el "antes".

### El mecanismo, que se repitió

No fue casualidad: volvió a pasar en el experimento 02. Se añadió *"rompe la regla a
propósito y comprueba que el test se pone rojo"*, y las tres pasadas del modelo pequeño
falsaron de verdad… por un solo lado del límite. Un test con el sello de verificado y la
misma cobertura de antes.

> **Toda instrucción que añades a una skill se ejecuta también de la forma más barata que
> la cumpla.**
>
> Antes de añadir una regla, pregúntate cuál es esa forma más barata. Si te vale, la
> regla está bien. Si no, falta acotarla — o la regla no debería estar ahí.

---

## Señales de que una skill que ya tienes sobra

Aplícalas a tu carpeta, hoy:

1. **No se ha disparado nunca.** O la `description` está mal, o el caso no ocurre.
2. **Describe algo que se lee abriendo un fichero.** Lo enseña el código.
3. **Sus reglas son listas de sitios.** Enumerar caduca; el criterio no.
   *(Ver el [capítulo 03](03-anatomia-de-una-skill.md))*
4. **Nadie la ha tocado desde que se escribió, y el proyecto sí ha cambiado.**
5. **No sabrías decir qué hacía mal el agente antes de tenerla.** Entonces no lo sabes.

La quinta es la definitiva. Si no puedes contestarla, la skill no está sostenida por
nada.

---

## Borrarla es un resultado, no un fracaso

Cuando una skill no se sostiene, **se borra y se anota por qué**. Ese registro vale más
que la skill: es lo que evita que dentro de seis meses alguien —tú— vuelva a escribir la
misma.

Y no hace falta que sea todo o nada. Lo normal es lo que pasó aquí: **el destino se
divide**. El patrón se quedó en el código, tres puntos entraron en la skill, y de esos
tres uno acabó bajando a un test. La skill final es más corta que la que se planeó, y
cada punto que sobrevivió tiene un número detrás.

---

## El ejercicio

Abre tu carpeta de skills. Para cada una, contesta solo esto:

> **¿Qué hacía mal el agente antes de tener esta skill? Ponle un número.**

Las que no tengan respuesta no se borran todavía: se **miden**. Tres pasadas sin ella, en
sesión limpia, con el mismo encargo.

Es el ejercicio más incómodo del curso y el único que cambia de verdad lo que haces
después.

---

## Lo que se lleva a cualquier herramienta

1. **El destino por defecto no es la skill.** Es "nada", y es una respuesta válida.
2. **Escribir bien el código es la forma más barata de no necesitar una skill.**
3. **Una skill que no se dispara es peor que no tenerla**, porque crees que sí funciona.
4. **Toda instrucción trae su propio fallo.** Cuenta también lo que empeoró.
5. **Si no sabes qué iba mal sin ella, no sabes si sirve.**
