# 01 — Los tres mecanismos de contexto

> Continúa el [capítulo 00](00-la-tesis.md). Lo que aquí caduca —rutas, nombres de
> fichero, campos— vive en el [anexo volátil](anexo-volatil.md).

## No son tres funcionalidades

`CLAUDE.md`, las skills y la memoria se presentan casi siempre como tres cosas que la
herramienta trae. Vistas así no hay forma de elegir entre ellas, y por eso todo el mundo
acaba usando la primera que aprendió.

Son **tres respuestas a la misma pregunta**:

> **¿Cuándo entra esta información en la ventana de contexto?**

Y una vez planteado así, elegir deja de ser cuestión de gusto.

| Mecanismo | Cuándo entra | Coste | Para qué |
|---|---|---|---|
| **`CLAUDE.md`** | **Siempre**, en cada turno | Fijo y permanente | Reglas que no se negocian nunca |
| **Skill** | Solo al dispararse | **Cero** hasta que se usa | Procedimiento largo y ocasional |
| **Memoria** | Índice siempre; la ficha, bajo demanda | Casi cero + puntual | Hechos duraderos sobre el usuario o el proyecto |

Esta tabla es el capítulo entero. El resto es cómo se aplica.

---

## `CLAUDE.md` — el que se paga siempre

Es el más simple y el más caro: **cada línea se paga en cada turno de cada sesión**, se
use o no.

Eso lo hace el sitio correcto para una cosa muy concreta: reglas que aplican **siempre**,
sin excepción y sin condición. Y muy pocas cosas cumplen eso de verdad.

El error habitual no es usarlo mal, es usarlo **por defecto**: era el sitio que existía
primero, así que ahí acabó todo — convenciones, procedimientos, preferencias, notas. El
fichero crece, nadie lo revisa, y llega el día en que contiene instrucciones que
contradicen al propio repositorio.

> **Prueba para cada línea de tu `CLAUDE.md`:** ¿esto tiene que estar delante del agente
> también cuando la tarea no tiene nada que ver? Si la respuesta es no, no va aquí.

### La demostración está en este repositorio

**Este proyecto no tiene `CLAUDE.md`.** Ni de proyecto ni global. Compruébalo:

```bash
ls CLAUDE.md
# → No such file or directory
```

Y aun así el agente respeta las convenciones de commits, el idioma del proyecto y las
restricciones de Git — porque todo eso está en **skills** y en **memoria**, que es donde
corresponde.

> Un proyecto que se comporta según una decena de convenciones propias **con cero bytes de
> instrucciones permanentes**. Eso es la tesis del capítulo 00 en una comprobación de un
> segundo.

---

## Skill — la que no cuesta hasta que hace falta

El mecanismo con la mejor economía de los tres, por cómo está partido:

- **`description`**: siempre presente. Unas líneas.
- **cuerpo**: no existe para el agente hasta que decide cargarlo. Decenas o cientos de
  líneas.
- **`references/`**: no existe hasta que el cuerpo lo pide. Otro salto más.

Tres niveles, y solo pagas el primero de forma permanente. Por eso **diez skills bien
descritas cuestan menos que un `CLAUDE.md` mediano**, y por eso el `description` tiene
[capítulo propio](04-frontmatter.md): es lo único que se cobra siempre y lo único que
decide.

Su terreno natural es el **procedimiento largo y ocasional**: cinco pasos que solo
importan cuando vas a publicar una release, y que el resto del mes serían ruido.

Medido en este repo: **12 de 12 disparos** con dos modelos distintos, siempre antes de
leer ningún fichero.

---

## Memoria — lo que es verdad sobre ti, no sobre la tarea

Funciona con la misma idea de dos niveles que las skills: un **índice** que se carga en
cada sesión, con una línea por hecho, y **una ficha por hecho** que solo entra cuando es
relevante. Lo que decide esa relevancia es, otra vez, una descripción corta.

La diferencia con una skill no es de formato ni de tamaño. Es de **alcance**.

### La pregunta que separa skill de memoria

> **¿Esto sería igual de verdad para otra persona haciendo la misma tarea?**

- **Sí** → es conocimiento → **skill**. *Conventional Commits* vale para cualquiera.
- **No** → es un hecho tuyo → **memoria**. Que *tu* clave SSH pida passphrase solo te pasa
  a ti.

### El caso que lo enseña mejor: la misma lección, en dos sitios

En este proyecto, un agente no puede completar un `git push` porque la clave SSH pide una
passphrase que no puede teclear. El síntoma es un `Permission denied (publickey)` — que
apunta a un problema de claves **que no existe**.

Esa lección está partida en dos, por alcance:

| Parte | Dónde | Por qué |
|---|---|---|
| **El patrón**: un agente no puede escribir en un prompt interactivo, y los comandos que lo exigen hay que dárselos a la persona | **Skill** | Le pasa a cualquiera |
| **El hecho**: en esta máquina ocurre, y el error engañoso es este | **Memoria** | Solo pasa aquí |

> **Misma lección, dos alcances, dos mecanismos.** Cuando una cosa parece que no cabe en
> ninguno de los dos, casi siempre es que son dos cosas.

---

## Los tres, en orden de decisión

Junta esto con el [árbol del capítulo 02](02-arbol-de-decision.md) y el criterio queda
completo:

1. **¿Aplica siempre, sin excepción?** → `CLAUDE.md`. Muy pocas cosas.
2. **¿Es verdad para cualquiera haciendo esta tarea?** → **skill**.
3. **¿Es un hecho sobre ti o sobre este proyecto?** → **memoria**.
4. **¿Se puede dejar evidente en el código o en un test?** → entonces no es ninguno de los
   tres, y es la mejor respuesta de todas.

El cuarto no está fuera de sitio: **cuesta cero y no envejece en silencio**, que es más de
lo que puede decir cualquiera de los otros tres.

---

## El ejercicio

Abre tu `CLAUDE.md` —o el de tu equipo— y clasifica cada línea en una de cuatro columnas:
`CLAUDE.md`, skill, memoria, o el código.

Lo normal es que sobreviva menos de la cuarta parte. Y lo que sobrevive suele ser justo lo
que se escribió el primer día.

---

## Lo que se lleva a cualquier herramienta

1. **La pregunta no es "dónde lo pongo", es "cuándo quiero que entre".**
2. **`CLAUDE.md` se paga en cada turno.** Reservarlo para lo que aplica siempre.
3. **Las skills reparten el coste en niveles.** Pagas la descripción, no el contenido.
4. **La memoria es para lo que es verdad sobre ti**, no sobre la tarea.
5. **Si algo no cabe limpiamente en uno, probablemente son dos cosas** con alcances
   distintos.
