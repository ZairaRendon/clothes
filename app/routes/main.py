from flask import Blueprint, render_template
from app.decorators import login_required, admin_required


main_bp = Blueprint("main", __name__)

@main_bp.get("/")
def home():
    return render_template("index.html")

@main_bp.get("/dashboard")
@login_required
def dashboard():
    return render_template("dashboard.html")

@main_bp.get("/admin")
@admin_required
def admin_panel():
    return render_template("admin.html")