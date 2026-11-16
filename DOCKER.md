# Ejecución local con Docker

La configuración levanta el frontend Vue, el backend Django y una instancia
local de SQL Server Developer. La base de datos se crea vacía al iniciar por
primera vez y Django aplica las migraciones automáticamente. Los datos de SQL
Server y los archivos cargados se conservan en volúmenes de Docker.

## Inicio

1. Instale Docker Desktop o Docker Engine con Docker Compose.
2. Copie `.env.docker.example` a `.env`.
3. Cambie `SQLSERVER_SA_PASSWORD` por una contraseña segura que cumpla los
   requisitos de SQL Server y reemplace `DJANGO_SECRET_KEY` por una clave larga
   y aleatoria.
4. Ejecute:

   ```sh
   docker compose up --build
   ```

5. Abra `http://localhost:3000`. El backend también queda disponible en
   `http://localhost:8001` y SQL Server en `localhost:1433`.

Para detener los servicios sin borrar los datos, ejecute
`docker compose down`. Para eliminar también la base de datos y los archivos
cargados, ejecute `docker compose down -v`; esta última operación borra los
volúmenes persistentes.

SQL Server Developer está destinado a desarrollo y pruebas, no a producción.
