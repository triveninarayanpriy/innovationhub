#!/bin/bash
set -e
cd innovationhubnitp
python manage.py migrate --noinput
exec gunicorn innovationhubnitp.wsgi:application --bind 0.0.0.0:$PORT
