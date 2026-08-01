# Artículo

Las piezas para publicar el material del repositorio. Se escriben y se versionan **aquí**;
LinkedIn es una copia, no la fuente.

**Empieza por [00-serie.md](00-serie.md):** el arco completo, la cadencia y por qué cada
entrega va donde va. Las nueve piezas están escritas y listas para copiar.

| # | Entrega | Formato |
|---|---|---|
| [00](00-serie.md) | El plan de la serie | — |
| [01](01-la-skill-que-borre.md) | La skill que borré | Post |
| [02](02-la-medi-antes-de-escribirla.md) | La medí antes de escribirla, y no hacía falta | Post |
| [03](03-el-error-que-antes-no-existia.md) | La escribí igual, y creó un error que antes no existía | **Artículo** |
| [04](04-misma-regla-otra-redaccion.md) | Mismo contenido, otra redacción | Post |
| [05](05-el-techo-y-el-suelo.md) | La skill sube el techo, el código sube el suelo | Post |
| [06](06-647-caracteres-cero-usos.md) | 647 caracteres en cada sesión, cero veces usado | Post |
| [07](07-la-herramienta-que-se-solapa.md) | Ya tenía la herramienta. Instalé la que se solapaba | Post |
| [08](08-cuatro-intentos-ningun-error.md) | Cuatro intentos, ningún error, tres mediciones perdidas | **Artículo** |
| [09](09-lo-que-me-costo-medirlo.md) | Lo que me costó medir todo esto | **Artículo**, cierre |

Cada fichero trae el texto listo para pegar dentro de un bloque, y debajo las notas de por
qué está escrito así.

La **portada** ya está hecha: el [README del repositorio](../README.md) abre con la tesis y
la tabla de resultados medidos, así que funciona como landing sin ser una landing. Es donde
cae quien llegue desde la entrega 9.

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
