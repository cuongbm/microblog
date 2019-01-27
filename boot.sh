#!/bin/sh
source venv/bin/activate
sleep 19
flask db upgrade
exec gunicorn -b :5000 --access-logfile - --error-logfile - microblog:app

