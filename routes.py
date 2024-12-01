from app import app, db, bcrypt, limiter
from flask import render_template, redirect, url_for, flash, request
from flask_login import login_user, logout_user, login_required, current_user
from models import User
from datetime import datetime
import pytz  # Para ajustar la zona horaria

# Limitar intentos para prevenir fuerza bruta
@limiter.limit("5 per minute")
@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        user = User.query.filter_by(username=request.form['username']).first()
        if user and bcrypt.check_password_hash(user.password, request.form['password']):
            # Ajustar la hora UTC a la zona horaria de Santiago
            user.last_login = datetime.utcnow().replace(tzinfo=pytz.utc).astimezone(pytz.timezone("America/Santiago"))
            db.session.commit()
            login_user(user)
            return redirect(url_for('dashboard'))
        else:
            flash("Credenciales inválidas.", "danger")
    return render_template("login.html")

@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form['username']
        password = request.form['password']
        confirm_password = request.form['confirm_password']

        # Validar que las contraseñas coincidan
        if password != confirm_password:
            flash("Las contraseñas no coinciden. Por favor, inténtalo de nuevo.", "danger")
            return redirect(url_for('register'))

        # Crear el nuevo usuario
        hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')
        user = User(username=username, password=hashed_password)
        db.session.add(user)
        db.session.commit()

        flash("Cuenta creada con éxito. Ahora puedes iniciar sesión.", "success")
        return redirect(url_for('login'))
    return render_template("register.html")

@app.route("/dashboard")
@login_required
def dashboard():
    return render_template(
        "dashboard.html",
        username=current_user.username,
        last_login=current_user.last_login
    )

@app.route("/logout")
@login_required
def logout():
    logout_user()
    flash("Sesión cerrada.", "info")
    return redirect(url_for('login'))

# Nueva ruta para la página principal
@app.route("/")
def home():
    return render_template("home.html")
