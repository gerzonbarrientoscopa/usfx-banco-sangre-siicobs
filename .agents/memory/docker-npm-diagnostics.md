---
name: Diagnóstico de npm en Docker
description: Distinguir fallos de resolución de red de problemas de dependencias al compilar Docker.
---

No atribuir `Exit handler never called!` a una versión de npm sin revisar primero su registro de diagnóstico.

**Why:** Durante las pruebas de Docker en este entorno, npm 10.8.2 mostró ese error genérico por fallos DNS `EAI_AGAIN`. La misma imagen y dependencias compilaron correctamente con la red del host. Esto no prueba la causa de un fallo en el equipo del usuario.

**How to apply:** Mostrar los registros de npm al fallar la instalación y distinguir las pruebas locales de los resultados del equipo del usuario. No recomendar cambios de versiones ni asumir que una red de host sea una solución portable para Docker Desktop.
