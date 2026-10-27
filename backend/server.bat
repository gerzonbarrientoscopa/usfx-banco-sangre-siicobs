@echo off
cmd /k "cd /d C:\siicobs\venv\Scripts & activate & cd /d    C:\siicobs\ & python manage.py runserver  192.168.1.111:80


server {
    listen 80;
    server_name 201.131.45.30;

    location = /favicon.ico { access_log off; log_not_found off; }
    location /static/ {
        root /home/websrv/siicobs;
    }

    location / {
        include proxy_params;
        proxy_pass http://unix:/run/gunicorn.sock;
    }
}

