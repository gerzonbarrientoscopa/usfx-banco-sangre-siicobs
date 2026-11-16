# Ejecución local con Docker

La configuración levanta el frontend Vue y el backend Django. El backend se
conecta al SQL Server institucional existente; Compose no instala ni inicia
otro servidor de base de datos.

## Inicio

1. Instale Docker Desktop o Docker Engine con Docker Compose.
2. Copie `.env.docker.example` a `.env`.
3. Configure `DB_NAME`, `DB_USER`, `DB_PASSWORD`, `DB_HOST` y `DB_PORT` con los
   datos proporcionados por el administrador de la base de datos. Reemplace
   también `DJANGO_SECRET_KEY` por una clave larga y aleatoria.
4. Asegúrese de que Docker pueda acceder al servidor institucional por la red o
   VPN. Dentro del contenedor, `localhost` apunta al contenedor del backend;
   use el hostname o IP institucional. Si la conexión se publica en la máquina
   anfitriona, en Docker Desktop puede usar `host.docker.internal`.
5. Ejecute:

   ```sh
   docker compose up --build
   ```

6. Abra `http://localhost:3000`. El backend también queda disponible en
   `http://localhost:8001`.

El contenedor espera a que la base configurada responda y sirve los archivos
cargados desde un volumen Docker. No crea la base ni aplica migraciones
automáticamente, para evitar cambios no autorizados en la base institucional.
Si se requieren cambios de esquema, coordínelos con el administrador de BD.

Para detener los contenedores sin borrar los archivos cargados, ejecute
`docker compose down`. `docker compose down -v` también elimina el volumen de
archivos cargados.
