#!/bin/bash
set -e
cd /app/backend
echo "Running migrations..."
python manage.py migrate --noinput
echo "Ensuring test data exists..."
python manage.py seed_test_data
echo "Starting Gunicorn..."
exec gunicorn playto_pay.wsgi --bind 0.0.0.0:${PORT:-8000} --log-file -
