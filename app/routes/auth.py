from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from werkzeug.security import check_password_hash, generate_password_hash
from app.models.users import User
from app.extensions import db

auth_bp = Blueprint("auth", __name__, url_prefix="/auth")


@auth_bp.route("/login", methods=["GET", "POST"]) 
def login():
    if request.method == "POST":
        email = request.form.get("email")
        password = request.form.get("password")
        
        # Buscar usuario por email
        user = User.query.filter_by(email=email).first()
        
        if user and check_password_hash(user.password, password):
            # Guardar información del usuario en la sesión
            session["user_id"] = user.id
            session["user_name"] = user.name
            session["user_role"] = user.role
            
            flash("Inicio de sesión exitoso", "success")
            return redirect(url_for("main.home"))
        else:
            flash("Correo o contraseña incorrectos", "danger")
            return redirect(url_for("auth.login"))
    
    return render_template("login.html")


@auth_bp.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        name = request.form.get("name")
        email = request.form.get("email")
        password = request.form.get("password")
        confirm_password = request.form.get("confirm_password")

        if not name or not password:
            flash("Todos los campos son obligatorios")
            return redirect(url_for("auth.register"))
        
        if len(password) < 8:
            flash("La contraseña debe tener al menos 8 caracteres", "danger")
            return redirect(url_for("auth.register"))
        
        if password != confirm_password:
            flash("La contraseñas no coinciden", "danger")
            return redirect(url_for("auth.register"))
        
        # si email ya existe
        existing_user = User.query.filter_by(email=email).first()
        if existing_user:
            flash("Este correo ya está registrado", "danger")
            return redirect(url_for("auth.register"))
        
        # crear nuevo usuario
        hashed_password = generate_password_hash(password)
        new_user = User(
            name=name,
            email=email,
            password=hashed_password,
            role="user" 
        )

        try:
            db.session.add(new_user)
            db.session.commit()
            flash("Cuenta creada exitosamente", "success")
            return redirect(url_for("auth.login"))
        except Exception as e:
            db.session.rollback()
            flash("Ocurrió un error al crear la cuenta. Intenta de nuevo", "danger")
            return redirect(url_for("auth.login"))

    return render_template("register.html")


@auth_bp.get("/logout")
def logout():
    session.clear()
    flash("Has cerrado sesión correctamente", "info")
    return redirect(url_for("auth.login"))


@auth_bp.get("/forgot-password")
def forgot_password():
    return render_template("forgot_password.html")