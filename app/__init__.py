from flask import Flask
from flask_sqlalchemy import SQLAlchemy


from .routes.main import main_bp
from .routes.auth import auth_bp

# Inicializamos SQLAlchemy
db = SQLAlchemy()

def create_app():
    app = Flask(__name__)
    
    app.config.from_object("app.config.Config")
    
    db.init_app(app)
    
    from app.models.product import Product
    from app.models.variation import ProductVariation
    from app.models.customer import Customer
    from app.models.supplier import Supplier
    from app.models.sale import Sale
    from app.models.discount import Discount

    with app.app_context():
        db.create_all()


    app.register_blueprint(main_bp)
    app.register_blueprint(auth_bp)
    return app
