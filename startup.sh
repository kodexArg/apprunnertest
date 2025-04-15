#!/bin/sh
set -e

# Collect static files
python3 manage.py collectstatic --noinput

# Apply database migrations
python3 manage.py migrate

# Start the Gunicorn server
gunicorn project.wsgi:application --bind 0.0.0.0:${PORT:-8080} --workers 3 --log-file -