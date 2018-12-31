from flask import Flask
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_bootstrap import Bootstrap

from app.logging import configLogging
from config import Config
from elasticsearch import Elasticsearch


db = SQLAlchemy()

login = LoginManager()
login.login_view = 'auth.login'

migrate = Migrate()
bootstrap = Bootstrap()

from app import models, errors, logging
from app.main import routes

from app.errors import bp as errors_bp
from app.auth import bp as auth_bp
from app.main import bp as main_bp

def createApp(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)
    db.init_app(app)
    login.init_app(app)
    migrate.init_app(app, db)
    bootstrap.init_app(app)

    app.register_blueprint(errors_bp)
    app.register_blueprint(auth_bp, url_prefix="/auth")
    app.register_blueprint(main_bp)
    configLogging(app)

    app.elasticsearch = Elasticsearch(app.config["ELASTICSEARCH_URL"]
                                      if app.config["ELASTICSEARCH_URL"] else None)


    return app
