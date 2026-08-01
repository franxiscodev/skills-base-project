# Entrega 8 — Cuatro intentos, ningún error, tres mediciones perdidas

> **Formato: ARTÍCULO** (nativo de LinkedIn) ·
> **Base:** [capítulo 07](../temario/07-instalar-una-capacidad.md)

La entrega que más viaja fuera de Claude Code: vale para cualquier sistema donde
**configuras en un sitio y ejecutas en otro**. Y la que contiene el error propio más gordo
de la serie.

---

## Para pegar

### Instalar algo se documenta siempre igual. Un comando, una captura, y a otra cosa

La medición de la entrega anterior tenía un problema: para hacerla había que instalar el
servidor. Eso se cuenta en todas partes en un comando y una captura donde pone `Connected`.

A mí me costó cuatro intentos, seis pasadas de agente tiradas y tres mediciones perdidas.

Y el dato que hace que esto valga la pena contarlo:

> **En ninguno de los tres fallos hubo un solo mensaje de error.** Todos los diagnósticos
> que consulté decían la verdad.

Aun así, tres veces medí la condición equivocada creyendo que medía la buena.

### La cronología

| Qué pasó | Qué decía el diagnóstico | Qué pasaba de verdad |
|---|---|---|
| Instalado y conectado | ✔ Connected | Instalado **en otra carpeta** |
| Instalado en la carpeta buena | ✔ Connected | La sesión de medición **ya estaba abierta** |
| Sesión nueva | ✔ Connected en el terminal, ausente en el editor | Una escribía `C:/…` y el otro leía `c:/…` |

Sí: la última fue una diferencia de mayúscula en la letra de la unidad. Dos entradas
distintas para la misma carpeta.

### Lo que se lleva a cualquier herramienta

**Una capacidad no se instala en tu máquina. Se instala en un ámbito.**

«Está instalado» no es una propiedad de tu ordenador. Es una propiedad de la combinación
*quién ejecuta · desde dónde · desde cuándo*. Si no sabes decir esas tres cosas, no sabes
si está instalado.

Y la consecuencia es incómoda, porque va contra el instinto: **el ámbito más estrecho es el
que más silenciosamente se equivoca.** Instalar algo «solo para este proyecto» parece la
opción prudente. Es la que más veces te deja midiendo otra cosa.

**Comprobar la configuración no es comprobar la ejecución.**

Todos los paneles que miré eran correctos, y ninguno contestaba a la pregunta que yo creía
hacerle. La lista de servidores respondía sobre el directorio desde el que la lanzaba. Yo
preguntaba por otro.

La única verificación que vale es buscar la capacidad **dentro de la sesión que hace el
trabajo**.

### Y ahora la parte que preferiría no contar

Cuando la primera comprobación salió vacía, publiqué esta conclusión:

> *"El servidor figuraba como conectado, no dio ningún error, y aportó cero herramientas a
> la sesión. Luego «Connected» no significa disponible."*

Los datos eran correctos. **La causa me la inventé.**

El servidor sí aportaba herramientas — en la carpeta donde estaba instalado. La explicación
aburrida estaba a un comando de distancia y no la busqué, porque la interesante ya
encajaba.

> **Cuando una observación admite una causa mundana y otra publicable, la mundana se
> comprueba primero.** Si no, acabas enseñando una regla que no existe.

Es el fallo más fácil de cometer cuando escribes material didáctico, porque **el incentivo
empuja en esa dirección**: la causa interesante se cuenta mejor. Se detectó porque alguien
me dijo «revísalo, no asumas», no por ningún proceso mío.

### El coste que nadie pone en la cuenta

| | |
|---|---|
| Comandos hasta tenerlo funcionando | 6 |
| Errores por el camino | 2 explícitos, 3 silenciosos |
| Credencial | Un token guardado en claro en la configuración |
| Residuos al desinstalar | 3 entradas en 3 sitios distintos, cada una con el token |

Desinstalar no fue un comando: fueron tres. Y **uno de los tres no funcionó**: el comando
contestó «no existe ese servidor» mientras la entrada seguía en el fichero, por la misma
diferencia de mayúscula de antes. Hubo que editarlo a mano.

La misma grafía que impidió instalarlo impidió después quitarlo. Un residuo con una
credencial dentro, invisible para la herramienta que lo creó.

> **Si añadir algo es un comando y quitarlo son tres —y uno no funciona—, no estabas
> contando bien el coste de añadirlo.**

---

**La pregunta de hoy:** ¿cuántas veces has dado por instalada una capacidad porque un panel
decía que sí? No hace falta que sea esto: vale cualquier configuración que se aplica en un
sitio y se ejecuta en otro.

## Notas

- **Es la entrega más transversal de la serie.** Un responsable de plataforma o de
  infraestructura la entiende entera sin saber qué es una skill. Conviene publicarla como
  artículo por eso, no solo por la longitud.
- La confesión del error propio va **después** de las lecciones, no antes. Si va antes,
  el lector la lee como excusa; después, la lee como método.
- Las dos tablas hay que rehacerlas al pegar. La primera se puede dejar como tres líneas
  seguidas; la segunda funciona bien como lista.
