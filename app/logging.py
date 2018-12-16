import os
from logging.handlers import RotatingFileHandler

import logging

from app import app

if not os.path.exists("logs"):
    os.mkdir("logs")
file_handler = RotatingFileHandler("logs/logs.txt", maxBytes=10240, backupCount=10)
file_handler.setFormatter(logging.Formatter(
        '%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]'))
file_handler.setLevel(app.config["LOG_LEVEL"])
app.logger.addHandler(file_handler)
app.logger.info('Microblog startup')