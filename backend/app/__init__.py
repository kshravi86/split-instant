
from flask import Flask
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_jwt_extended import JWTManager

app = Flask(__name__)
app.config.from_object(Config)

db = SQLAlchemy(app)
migrate = Migrate(app, db)
jwt = JWTManager(app)

from app.auth import auth_bp
app.register_blueprint(auth_bp, url_prefix='/api/auth')

from app.routes import bp as routes_bp
app.register_blueprint(routes_bp, url_prefix='/api')

from app import models
