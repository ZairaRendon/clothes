from flask import Flask
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

from .models import Product, Customer, Supplier, Sale, ProductVariation

def create_app():
    app = Flask(__name__)
    app.config.from_object("app.config.Config")
    db.init_app(app)

    # Crear tablas
    with app.app_context():
        db.create_all()

    return app
