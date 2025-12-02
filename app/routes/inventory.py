from flask import Blueprint, render_template, request, redirect, url_for, flash
from app.decorators import login_required
from app.models.product import Product
from app.models.variation import ProductVariation
from app.extensions import db

inventory_bp = Blueprint("inventory", __name__, url_prefix="/inventory")

@inventory_bp.route("/")
@login_required
def inventory():
    search = request.args.get("search", "")
    if search:
        products = Product.query.filter