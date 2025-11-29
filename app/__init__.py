from flask import Flask
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

def create_app():
    app = Flask(__name__)
    app.config.from_object("app.config.Config")
    db.init_app(app)

    from .models import Product, ProductVariation, Customer, Supplier, Sale, Discount

    with app.app_context():
        db.create_all()

    return app
