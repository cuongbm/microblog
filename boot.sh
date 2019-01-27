#!/bin/sh
source venv/bin/activate
flask db upgrade
exec gunicorn -b :5000 --access-logfile - --error-logfile - microblog:app
sleep 10
flask db upgrade
sleep 10
flask db upgrade
sleep 10
flask db upgrade
