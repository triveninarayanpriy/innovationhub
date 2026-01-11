#!/bin/bash
set -e
cd innovationhubnitp
exec gunicorn innovationhubnitp.wsgi:application --bind 0.0.0.0:$PORT
