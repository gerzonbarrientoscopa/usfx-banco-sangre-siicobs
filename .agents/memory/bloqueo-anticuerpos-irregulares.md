---
name: Bloqueo por anticuerpos irregulares
description: Decisión sobre cómo configurar los hemocomponentes restringidos ante anticuerpos irregulares positivos.
---

Para bloquear ciertos hemocomponentes cuando Anticuerpos Irregulares resulte positivo, identificar los tipos restringidos con un indicador en el catálogo existente de tipos de hemocomponente. No crear una tabla nueva.

**Why:** el usuario eligió esta opción frente a mantener nombres hardcodeados; el catálogo existente permite configurarlo por tipo y evitar depender de IDs o nombres idénticos entre entornos.

**How to apply:** usar el indicador del catálogo existente para controlar la interfaz y validar todas las rutas de liberación en el servidor.
