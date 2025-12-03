from flask import Flask
from .extensions import db, migrate

# from .routes.main import main_bp
# from .routes.auth import auth_bp

# # Inicializar SQLAlchemy
# db = SQLAlchemy()
# migrate = Migrate()

def create_app():
    app = Flask(__name__)
    
    app.config.from_object("app.config.Config")
    
    # inicializar extensiones
    db.init_app(app)
    migrate.init_app(app, db)
    
    with app.app_context():
        from app.models.product import Product
        from app.models.variation import ProductVariation
        from app.models.customer import Customer
        from app.models.supplier import Supplier
        from app.models.sale import Sale
        from app.models.discount import Discount
        from app.models.users import User
        from app.models.sale_item import SaleItem
        from app.models.discount import Discount
        from app.models.users import User

    #with app.app_context():
    #    db.create_all()

    from app.routes.main import main_bp
    from app.routes.auth import auth_bp
    from app.routes.inventory import inventory_bp
    from app.routes.sales import sales_bp

    app.register_blueprint(main_bp)
    app.register_blueprint(auth_bp)
    app.register_blueprint(inventory_bp)
    app.register_blueprint(sales_bp)
    
    return app
