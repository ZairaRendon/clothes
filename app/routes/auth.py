from flask import Blueprint, render_template

auth_bp = Blueprint("auth", __name__, url_prefix="/auth")


@auth_bp.get("/login")
def login():
    return render_template("login.html")


@auth_bp.get("/register")
def register():
    return render_template("register.html")


@auth_bp.get("/forgot-password")
def forgot_password():
    return render_template("forgot_password.html")
