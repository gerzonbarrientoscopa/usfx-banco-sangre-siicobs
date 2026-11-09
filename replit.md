# SIICOBS en Replit

## Estructura y alcance
- Se conservan el frontend Vue 2 y el backend Django originales.
- Esta configuración es exclusivamente para desarrollo y pruebas, no para publicación.
- Por elección del usuario se usa una base SQLite nueva y vacía. No conectar bases reales ni cargar `seed.json` o datos de donantes sin autorización.
- No hay usuarios iniciales ni contraseñas predeterminadas.

## Arranque
Usar **Run** para ejecutar el flujo **Iniciar aplicación**, o:

```bash
bash scripts/start-replit.sh
```

El script aplica las migraciones pendientes a `backend/replit.sqlite3`, inicia Django en el puerto interno 8000 y Vue en `0.0.0.0:5000`. Si termina uno de los servicios, finaliza también el otro.

Vue envía `/api`, `/media`, `/admin` y `/static` a Django mediante el proxy de desarrollo. No se usa el servidor de respuestas simuladas de la plantilla.

## Dependencias
- Python 3.11: dependencias administradas en `pyproject.toml` y `uv.lock`, basadas en `backend/requirements.txt`.
- Node 20: dependencias en `frontend/package.json` y `frontend/package-lock.json`.
- Para reinstalar el frontend: `cd frontend && HUSKY_SKIP_INSTALL=1 npm ci --legacy-peer-deps`. Se omite el instalador de hooks Git de la plantilla, no los scripts de los demás paquetes.
- Vue CLI 5 y los ajustes de compilación permiten mantener Vue 2 sin instalar versiones bloqueadas por el filtro de seguridad. Esto no equivale a una revisión integral de seguridad.
- `SESSION_SECRET` debe existir en Replit Secrets. Se usa como clave Django; no imprimirla ni guardarla en archivos.

## Crear el primer administrador
En la consola Shell de Replit ejecutar:

```bash
cd backend
DJANGO_SETTINGS_MODULE=siicobs_main.replit_settings ../.pythonlibs/bin/python manage.py createsuperuser
```

Introducir usuario, correo y contraseña en la consola interactiva. No compartir la contraseña por chat. Después usar esas credenciales en la pantalla de acceso.

## Configuración de desarrollo
`siicobs_main.replit_settings` separa la configuración local de la configuración original:
- SQLite local persistente, excluida de Git.
- Archivos subidos guardados localmente; no requiere AWS.
- Hosts de vista previa permitidos y `DEBUG=True` únicamente para desarrollo.
- La configuración original de la base externa no se modifica.

## Verificación
```bash
cd backend
DJANGO_SETTINGS_MODULE=siicobs_main.replit_settings ../.pythonlibs/bin/python manage.py check
DJANGO_SETTINGS_MODULE=siicobs_main.replit_settings ../.pythonlibs/bin/python manage.py test users.test_replit_setup
```

Las pruebas crean una base temporal, verifican credenciales inválidas, acceso, permisos de administrador, GraphQL autenticado y cierre de sesión; no crean cuentas en la base de trabajo.

La pantalla de acceso se comprueba visualmente. Las pantallas internas requieren una cuenta y no quedan verificadas por esa captura.

## Advertencias heredadas
- Django detecta un cambio sin migración en la etiqueta del campo `cheia` de laboratorios. No bloquea el arranque; no se generaron migraciones ajenas a esta instalación.
- La pila original incluye componentes antiguos, algunos fuera de soporte. Antes de usar datos reales o publicar, revisar seguridad, permisos, dependencias y configuración de producción.
