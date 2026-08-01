# Entrega 5 — La skill sube el techo, el código sube el suelo

> **Formato:** post · **Base:** [exp 03](../temario/experimentos/03-bajar-al-codigo.md)

Un solo número: **6 de 6 fallos cazados, 0 falsos positivos**. Y el detalle que más gusta:
no hizo falta ejecutar ninguna pasada nueva.

## Para pegar

```text
Me quedaba un 1 de 3. El modelo pequeño seguía dejando el README con frases falsas por mucho que reescribiera la instrucción.

Se puede insistir. Redactarlo mejor, dar ejemplos, poner mayúsculas. Es lo que suele hacerse y es lo que yo iba a hacer.

Hice otra cosa: saqué el punto de la skill y lo bajé al código.

Diez líneas de test. Lee la traza de ejecución que está documentada en el README, ejecuta el pipeline de verdad, y compara. Si no coinciden, rojo.

Y aquí viene lo que no esperaba.

No tuve que lanzar ninguna pasada nueva para validarlo. Tenía guardadas las salidas reales de las 18 pasadas de los experimentos anteriores, así que ejecuté el test contra todas.

Cazó 6 de 6 de los fallos conocidos. Cero falsos positivos en las 12 ejecuciones que estaban bien.

Compara lo que cuesta cada cosa:

Una regla en una skill: ocupa contexto en cada sesión, depende de que el modelo la lea, la entienda y le apetezca aplicarla, y no te avisa cuando no lo hace.

Un test: no ocupa contexto, no depende de nadie, y falla solo.

De ahí sale el criterio que más uso ahora para decidir dónde va cada cosa:

Una skill sube el techo. El código sube el suelo.

Si controlas quién ejecuta y quieres que haga el trabajo completo, la skill. Si lo que quieres es que algo no pueda salir mal, eso no era trabajo de una skill: era un test que no habías escrito.

¿Cuántas de tus reglas de agente son en realidad un test que no has escrito?
```

## Notas

- **El argumento más fuerte no es el 6 de 6: es que no hubo que ejecutar nada.** Guardar
  las salidas de los experimentos anteriores hizo que validar el test costara cero. Esa es
  la parte que a un técnico le hace pensar «tengo que empezar a guardar esto».
- La comparación skill/test va en dos bloques cortos y paralelos. Es lo que se recuerda
  del post.
- La pregunta final es la más accionable de la serie: casi todo el mundo tiene una regla
  que debería ser un test.
