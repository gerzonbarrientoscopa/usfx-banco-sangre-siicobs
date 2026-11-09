---
name: Instalación de Python en Replit
description: Selección inesperada de intérprete al instalar dependencias heredadas.
---

Antes de instalar dependencias Python heredadas, alinear la restricción de Python del proyecto con el módulo habilitado.

**Why:** En esta importación, habilitar Python 3.11 no impidió que el instalador generara metadatos que exigían 3.12 y eligiera ese intérprete. Las versiones heredadas dejaron de tener ruedas compatibles y falló la compilación. Corregir la restricción resolvió la instalación sin cambiar las versiones originales del backend.

**How to apply:** Si una instalación intenta compilar inesperadamente dependencias antiguas, comprobar primero el intérprete que realmente seleccionó el instalador y las restricciones del proyecto. No asumir que coincide con el comando `python` de la consola.
