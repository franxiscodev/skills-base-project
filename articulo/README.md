# Artículo

Las piezas para publicar el material del repositorio. Se escriben y se versionan **aquí**;
LinkedIn es una copia, no la fuente.

| Pieza | Fichero | Para qué |
|---|---|---|
| **El plan de la serie** | [serie.md](serie.md) | Nueve entregas con arco, cadencia y las preguntas de cada una. **Empieza por aquí** |
| **Síntesis** | [articulo-linkedin.md](articulo-linkedin.md) | ~1.400 palabras. Se reconvierte en la **entrega 9**, el cierre |
| **Post del feed** | [post-linkedin.md](post-linkedin.md) | Dos versiones del gancho. Materia prima de la **entrega 1** |
| **Portada** | [`README.md`](../README.md) de la raíz | Donde cae quien llegue desde la serie |

La portada ya está hecha: el README del repositorio abre con la tesis y la tabla de
resultados medidos. Funciona como landing sin ser una landing.

⚠️ **El artículo largo no se publica tal cual.** Quema los cinco hallazgos en una sola
pieza, que fue el error del primer borrador. Su sitio es el final de la serie, cuando cada
número ya se ha contado por separado.

## Qué números se citan y de dónde salen

Todo lo del artículo es verificable dentro del repositorio. Si alguna cifra cambia al
repetir un experimento, **se corrige aquí antes de volver a publicar**:

| Cifra | Origen |
|---|---|
| La skill no hacía falta: 3 de 3 sin ella | [Exp 01](../temario/experimentos/01-convenciones-pipeline.md) |
| README tocado 1/6 → 6/6, verdadero 0/6 | [Exp 01](../temario/experimentos/01-convenciones-pipeline.md) |
| MCP: 647 caracteres, 0 invocaciones en 26 sesiones | [Exp 04](../temario/experimentos/04-coste-de-un-mcp.md) |
| Las tres skills: 1.132 caracteres permanentes | [Exp 04](../temario/experimentos/04-coste-de-un-mcp.md) |
| La skill borrada: 518 caracteres, 0 de 40 sesiones, 5-0 | [Exp 05](../temario/experimentos/05-la-skill-que-nunca-gana.md) |

⚠️ **El artículo dice «3 de 3», no «6 de 6».** El experimento 01 tuvo seis pasadas en el
«antes» y una no conserva su salida; según la regla 7 del método, esa pasada no ocurrió. El
artículo cita solo el bloque verificable y además lo explica en su último tramo. **No subas
esa cifra a 6 de 6** aunque la veas escrita así en algún capítulo.

## Antes de publicar

1. **Sustituir `[enlace al repositorio]`** al final del artículo por la URL real.
2. **Elegir opción A o B** del post y borrar la otra de la cabeza, no del fichero.
3. **Quitar el markdown al pegar.** LinkedIn no lo interpreta: las tablas hay que
   rehacerlas como listas o como imagen, y las negritas se pierden.
4. **El enlace al repositorio va en el artículo y en el primer comentario**, nunca en el
   cuerpo del post.
5. Comprobar que el repositorio está **pusheado** antes de que exista un enlace público.

## Lo que viene después, si funciona

El artículo es la pieza barata: todo su contenido ya estaba medido y escrito. Si mueve
algo, lo siguiente en coste creciente es una landing propia y, solo entonces, un módulo
grabable. Cada uno reutiliza el anterior en vez de empezar de cero.
