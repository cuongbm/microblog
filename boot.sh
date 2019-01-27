#!/bin/sh
sleep 30
source venv/bin/activate
flask db upgrade
exec gunicorn -b :5000 --access-logfile - --error-logfile - microblog:app