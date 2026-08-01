# El post del feed

> LinkedIn corta en «…ver más» alrededor de los **200 caracteres**. Todo lo que tenga que
> hacer que alguien pulse ahí va antes de esa marca.
>
> Va **sin markdown**: LinkedIn no lo interpreta. Nada de `**negritas**`, ni viñetas con
> `-`, ni títulos con `#`. Solo texto y saltos de línea.

---

## Opción A — la que recomiendo

Abre por el hecho más raro y no explica nada hasta después del corte.

```text
Borré una skill que había escrito yo, que estaba bien escrita y que funcionaba.

Nunca llegó a ejecutarse. Ni una vez en 40 sesiones.

Lo descubrí porque me puse a contar, no porque fallara nada. Todo iba bien. Ese es el problema.

Llevo dos semanas midiendo qué aportan de verdad las skills y los MCP en Claude Code, en vez de dar por hecho que aportan. Tres números:

→ La primera skill que iba a escribir no hacía falta. El agente ya lo hacía bien 3 de 3 sin ella.

→ La escribí igual. Subió la cobertura del 17% al 100% y creó un error que antes no existía: 6 README tocados, 0 correctos.

→ Un servidor MCP conectado: 647 caracteres en cada sesión, 0 invocaciones en 26.

El método es incómodo y es todo lo que hay: primero se mide sin. Después se decide si hace falta. Solo entonces se escribe.

Sin ese "antes", todo lo que instalas funciona. No tienes con qué compararlo.

Lo he contado entero en el artículo, con los experimentos que refutaron mi propia hipótesis.
```

**973 caracteres.** Lo que se ve antes del corte son las dos primeras frases: la skill
borrada y el «ni una vez en 40 sesiones».

---

## Opción B — más corta y más incómoda

Si prefieres que el gancho sea el error propio en vez del hallazgo.

```text
Escribí una skill para Claude Code. Funcionó a la primera.

Luego medí qué pasaba sin ella y descubrí que no hacía falta: el agente ya lo hacía bien 3 de 3.

La había dado por buena porque no tenía con qué compararla.

Eso me llevó a medir el resto durante dos semanas. Lo que salió:

→ Esa misma skill, ya escrita, creó un error que antes no existía. 6 README tocados, 0 correctos.

→ Otra skill mía llevaba 40 sesiones sin cargarse ni una vez. 518 caracteres pagados en cada sesión, cero trabajo hecho.

→ Un MCP conectado: 647 caracteres siempre, 0 invocaciones en 26 sesiones.

Casi todo lo que se publica enseña a añadir. Añadir parece gratis porque no rompe nada.

Saber restar es la parte difícil, y es la única que no se puede improvisar.
```

**746 caracteres.**

---

## Detalles de publicación

- **Sin enlace en el post.** LinkedIn penaliza el alcance de las publicaciones que sacan
  gente fuera. El enlace al repositorio va **dentro del artículo**, y el artículo se
  publica nativo.
- **Primer comentario propio:** ahí sí, el enlace al repositorio. Es la vía habitual para
  no pagar el peaje del algoritmo.
- **Sin hashtags apilados.** Dos o tres como mucho, y al final.
- Ambas opciones evitan la primera persona del plural: es trabajo tuyo, y el artículo
  cuenta dos errores propios. Esa es la parte que da credibilidad.
