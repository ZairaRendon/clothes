from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from werkzeug.security import check_password_hash
from app.models.users import User

auth_bp = Blueprint("auth", __name__, url_prefix="/auth")


@auth_bp.route("/login", methods=["GET", "POST"]) 
def login():
    if request.method == "POST":
        email = request.form.get("email")
        password = request.form.get("password")
        
        # Buscar usuario por email
        user = User.query.filter_by(email=email).first()
        
        # Verificar si el usuario existe y la contraseña es correcta
        if user and check_password_hash(user.password, password):
            # Guardar información del usuario en la sesión
            session["user_id"] = user.id
            session["user_name"] = user.name
            session["user_role"] = user.role
            
            flash("¡Inicio de sesión exitoso!", "success")
            return redirect(url_for("main.home"))
        else:
            flash("Correo o contraseña incorrectos", "danger")
            return redirect(url_for("auth.login"))
    
    return render_template("login.html")


@auth_bp.get("/logout")
def logout():
    session.clear()
    flash("Has cerrado sesión correctamente", "info")
    return redirect(url_for("auth.login"))


@auth_bp.get("/register")
def register():
    return render_template("register.html")


@auth_bp.get("/forgot-password")
def forgot_password():
    return render_template("forgot_password.html")