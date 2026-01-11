#!/bin/bash
cd innovationhubnitp
gunicorn innovationhubnitp.wsgi:application --bind 0.0.0.0:$PORT
