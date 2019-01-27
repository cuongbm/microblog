#!/bin/sh
sleep 10
source venv/bin/activate
flask db upgrade
exec gunicorn -b :5000 --access-logfile - --error-logfile - microblog:app