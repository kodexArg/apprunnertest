#!/bin/bash

set -e

echo ">>> [Startup Script] Iniciando script..."

echo ">>> [Startup Script] Aplicando migraciones de base de datos y collectstatic..."
pipenv run python manage.py migrate --noinput
pipenv run python manage.py collectstatic --noinput
echo ">>> [Startup Script] Migraciones aplicadas."

echo ">>> [Startup Script] Iniciando Gunicorn..."
exec pipenv run gunicorn project.wsgi:application \
    --bind 0.0.0.0:$PORT \
    --log-level debug \
    -t 240 \
    --workers 2 \
    --threads 4

echo ">>> [Startup Script] Gunicorn iniciado."