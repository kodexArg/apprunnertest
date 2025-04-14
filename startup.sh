#!/bin/bash

# Set environment variables if needed
export DJANGO_SETTINGS_MODULE=project.settings
export PYTHONUNBUFFERED=1

# Install dependencies
pip install pipenv
pipenv install --system --deploy --ignore-pipfile

# Collect static files
pipenv run python manage.py collectstatic --noinput

# Apply database migrations
pipenv run python manage.py migrate

# Start the Gunicorn server
pipenv run gunicorn cakes_project.wsgi:application --bind 0.0.0.0:8000 --workers 2 --log-file -