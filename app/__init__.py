import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_mail import Mail

db = SQLAlchemy()
login_manager = LoginManager()
mail = Mail()

def create_app():
    app = Flask(__name__)

    # Upload configuration
    app.config["UPLOAD_FOLDER"] = os.path.join(app.static_folder, "uploads")
    app.config["MAX_CONTENT_LENGTH"] = 10 * 1024 * 1024 * 1024  # 10 GB

    # Security and secrets
    app.secret_key = os.getenv("SECRET_KEY", "supersecretkey")

    # Database setup (SQLite by default)
    app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv("DATABASE_URL", "sqlite:///app.db")
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    # Mail setup (update with your mail provider later)
    app.config["MAIL_SERVER"] = "smtp.gmail.com"
    app.config["MAIL_PORT"] = 587
    app.config["MAIL_USE_TLS"] = True
    app.config["MAIL_USERNAME"] = os.getenv("MAIL_USERNAME")
    app.config["MAIL_PASSWORD"] = os.getenv("MAIL_PASSWORD")
    app.config["MAIL_DEFAULT_SENDER"] = os.getenv("MAIL_USERNAME")

    # Initialize extensions
    db.init_app(app)
    login_manager.init_app(app)
    mail.init_app(app)

    login_manager.login_view = "auth.login"

    # Import models here so Flask knows about them
    from . import models

    # Register blueprints
    from .routes import main
    from .auth import auth as auth_blueprint
    app.register_blueprint(main)
    app.register_blueprint(auth_blueprint)

    return app

