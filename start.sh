#!/bin/bash
set -e
cd /app/backend
echo "Running migrations..."
python manage.py migrate --noinput
echo "Starting Gunicorn..."
exec gunicorn playto_pay.wsgi --bind 0.0.0.0:8000 --log-file -
