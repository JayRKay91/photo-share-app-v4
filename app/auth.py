from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, login_required, logout_user, current_user
from itsdangerous import URLSafeTimedSerializer
from flask_mail import Message
from .models import db, User
from . import login_manager, mail
import os

auth = Blueprint("auth", __name__, template_folder="templates")

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# Serializer for generating tokens
s = URLSafeTimedSerializer(os.getenv("SECRET_KEY", "dev_key"))

# ---------- Register ----------
@auth.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form.get("username")
        email = request.form.get("email")
        password = request.form.get("password")

        existing_user = User.query.filter((User.username == username) | (User.email == email)).first()
        if existing_user:
            flash("Username or email already exists.")
            return redirect(url_for("auth.register"))

        new_user = User(
            username=username,
            email=email,
            password_hash=generate_password_hash(password),
            is_verified=False
        )
        db.session.add(new_user)
        db.session.commit()

        # Send verification email
        token = s.dumps(email, salt="email-confirm")
        link = url_for("auth.verify_email", token=token, _external=True)
        msg = Message("Confirm Your Email", recipients=[email])
        msg.body = f"Click the link to verify your account: {link}"
        mail.send(msg)

        flash("A verification email has been sent. Please check your inbox.")
        return redirect(url_for("auth.login"))

    return render_template("auth/register.html")

# ---------- Verify Email ----------
@auth.route("/verify/<token>")
def verify_email(token):
    try:
        email = s.loads(token, salt="email-confirm", max_age=3600)
        user = User.query.filter_by(email=email).first()
        if user:
            user.is_verified = True
            db.session.commit()
            flash("Email verified. You can now log in.")
            return redirect(url_for("auth.login"))
    except Exception:
        flash("The confirmation link is invalid or has expired.")
    return redirect(url_for("auth.login"))

# ---------- Login ----------
@auth.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form.get("email")
        password = request.form.get("password")

        user = User.query.filter_by(email=email).first()
        if not user or not check_password_hash(user.password_hash, password):
            flash("Invalid email or password.")
            return redirect(url_for("auth.login"))

        if not user.is_verified:
            flash("Please verify your email before logging in.")
            return redirect(url_for("auth.login"))

        login_user(user)
        return redirect(url_for("main.dashboard"))

    return render_template("auth/login.html")

# ---------- Logout ----------
@auth.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("auth.login"))

# ---------- Password Reset Request ----------
@auth.route("/reset", methods=["GET", "POST"])
def reset_request():
    if request.method == "POST":
        email = request.form.get("email")
        user = User.query.filter_by(email=email).first()

        if user:
            token = s.dumps(email, salt="password-reset")
            link = url_for("auth.reset_token", token=token, _external=True)
            msg = Message("Reset Your Password", recipients=[email])
            msg.body = f"Click to reset your password: {link}"
            mail.send(msg)
            flash("Password reset email sent.")
        else:
            flash("No account with that email.")

        return redirect(url_for("auth.login"))

    return render_template("auth/reset_request.html")

# ---------- Password Reset via Token ----------
@auth.route("/reset/<token>", methods=["GET", "POST"])
def reset_token(token):
    try:
        email = s.loads(token, salt="password-reset", max_age=3600)
    except Exception:
        flash("Reset link is invalid or has expired.")
        return redirect(url_for("auth.reset_request"))

    user = User.query.filter_by(email=email).first()
    if request.method == "POST":
        new_password = request.form.get("password")
        user.password_hash = generate_password_hash(new_password)
        db.session.commit()
        flash("Your password has been updated.")
        return redirect(url_for("auth.login"))

    return render_template("auth/reset_password.html")
