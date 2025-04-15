#!/bin/bash

# Install dependencies
pip3 install pipenv
pipenv install --system --deploy --ignore-pipfile

# print virtualenv, pipenv, freeze
echo "Virtualenv: $(which python3)"
echo "Pipenv: $(pipenv --version)"
echo "Freeze: $(pipenv freeze)"

# Collect static files
pipenv run python3 manage.py collectstatic --noinput

# Apply database migrations
pipenv run python3 manage.py migrate

# Start the Gunicorn server
pipenv run gunicorn project.wsgi:application --bind 0.0.0.0:8000 --workers 2 --log-file -