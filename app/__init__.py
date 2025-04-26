import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_mail import Mail

# Initialize extensions
db = SQLAlchemy()
login_manager = LoginManager()
mail = Mail()

def create_app():
    app = Flask(__name__)

    # Load configuration from config.py
    app.config.from_object('config.Config')
    
    # Ensure uploads folder exists
    create_upload_folder(app.config["UPLOAD_FOLDER"])

    # Initialize extensions
    db.init_app(app)
    login_manager.init_app(app)
    mail.init_app(app)
    login_manager.login_view = "auth.login"

    # Import models (important for creating tables)
    from . import models

    # Register blueprints
    from .routes import main
    from .auth import auth as auth_blueprint
    app.register_blueprint(main)
    app.register_blueprint(auth_blueprint)

    return app

def create_upload_folder(upload_folder):
    """Creates the uploads folder if it doesn't exist."""
    os.makedirs(upload_folder, exist_ok=True)
