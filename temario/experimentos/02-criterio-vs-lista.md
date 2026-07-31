# Experimento 02 — ¿Se arregla cambiando cómo está escrita la regla?

> Continúa el [experimento 01](01-convenciones-pipeline.md). Método:
> [PLANTILLA.md](PLANTILLA.md).
> **Estado: en curso.** Hipótesis y condiciones escritas antes de ejecutar nada.

**Hipótesis** *(escrita antes de ejecutar nada)*:

> Reescribir las reglas como **criterio de terminado** en vez de como **lista de
> sitios** sube el "README verdadero" por encima de 0, porque un criterio se puede
> aplicar a un sitio que no está enumerado y una lista no.

## El problema

El experimento 01 midió una skill que funcionó en todo lo que pedía y aun así dejó el
trabajo mal:

| | Antes | Después |
|---|---|---|
| Toca el README | 1/6 | 6/6 |
| **Deja el README verdadero** | — | **0/6** |
| Escribe un caso negativo | 3/6 | 6/6 |
| **El caso negativo protege el criterio** | — | **4/6** |

El diagnóstico fue que las reglas estaban escritas como tareas, y una tarea se ejecuta
—también donde no toca—. Este experimento comprueba si eso se arregla con la
redacción, o si no se arregla con una skill en absoluto.

## Qué cambia y qué no

**Cambia:** §1 y §2 del `SKILL.md`, reescritas en criterio.

| | Antes (lista) | Ahora (criterio) |
|---|---|---|
| §1 | "Actualiza el README, el docstring del módulo y los vecinos" | "Que no quede ni una frase falsa. Búscalas, no las recuerdes. Y comprueba que es verdad lo que añades" |
| §2 | "Escribe un test de que no toca lo que no debe" | "Rompe la regla a propósito y comprueba que el test se pone rojo" |

**No cambia, a propósito:**

- **La `description`.** Se disparó 6 de 6; tocarla metería una segunda variable en la
  misma medición.
- **La §3** (el aviso sobre los datos de muestra). Es la **variable de control**: si se
  mantiene en 6/6 mientras las otras dos se mueven, el cambio viene del cambio y no de
  la sesión, del día o del humor del modelo.
- **El prompt**, carácter por carácter.

## 1. Las pasadas

**Prompt exacto:**

```text
Añade al pipeline una regla que descarte las ventas con importe cero.
```

**Condiciones:** sesión limpia · commit de partida verificado con `git log` ·
Claude Haiku 4.5 (medium)

### Por qué solo un modelo, y por qué el pequeño

Opus está **en el techo** del caso negativo: 3 de 3 en el experimento 01. Un resultado
que no puede subir no mide nada. Haiku tiene recorrido en las dos cosas —README 0/3,
caso negativo útil 1/3— y además es la prueba más dura: si un criterio bien redactado
arregla al modelo pequeño, con el grande casi seguro que también. Al revés no vale.

> **Regla general:** mide la mejora donde haya margen. Repetir con el modelo que ya
> acierta produce una tabla bonita y ninguna información.

### La condición de desempate, escrita por adelantado

| Resultado con Haiku | Qué significa | Qué se hace |
|---|---|---|
| Mejora | La redacción importa. Hipótesis confirmada | Se cierra |
| **No mejora** | **Ambiguo**: puede ser la redacción o el modelo | **Una pasada con Opus** para desempatar |

Y el desempate, también decidido de antemano:

- **Opus tampoco mejora** → el problema no es cómo está escrita la regla. Ese punto
  **no se arregla con una skill** y baja al código: un test que compare la traza
  documentada en el README con la salida real del pipeline. No gasta contexto y falla
  solo.
- **Opus sí mejora** → el problema no era la redacción sino el lector. La lección
  cambia entera: **una skill puede exigir más juicio del que tiene el modelo que la
  lee**, y eso obliga a escribirla para el modelo más pequeño que vaya a usarla.

### Resultados

| Pasada | ¿Se disparó? | README verdadero | Caso negativo útil | §3 (control) |
|---|---|---|---|---|
| 1 | | | | |
| 2 | | | | |
| 3 | | | | |
| Desempate (Opus) | | | | |

## Qué aprendimos

*Pendiente.*

## Cuándo NO hacer esto

*Pendiente.*

## Condiciones y reproducibilidad

- **Fecha:**
- **Modelo:** Claude Haiku 4.5 (medium), con Opus 5 (medium) solo como desempate
- **Versiones:** Python 3.12 · DuckDB 1.5.5 · pytest 9.1.1 · uv 0.7.9
- **Rama:** `docs/material-didactico`
- **Commit de referencia:**
