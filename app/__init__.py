from flask import Flask
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_bootstrap import Bootstrap

from config import Config

app = Flask(__name__)
app.config.from_object(Config)

db = SQLAlchemy(app)

login = LoginManager(app)
login.login_view = 'auth.login'

migrate = Migrate(app, db)
bootstrap = Bootstrap(app)

from app import models, errors, logging
from app.main import routes

from app.errors import bp as errors_bp
from app.auth import bp as auth_bp
from app.main import bp as main_bp

app.register_blueprint(errors_bp)
app.register_blueprint(auth_bp, url_prefix="/auth")
app.register_blueprint(main_bp)