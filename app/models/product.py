from .. import db

class Product(db.Model):
    __tablename__ = "products"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    category = db.Column(db.String(50), nullable=False)
    price = db.Column(db.Float, nullable=False)
    stock = db.Column(db.Integer, default=0)
    variations = db.relationship("ProductVariation", backref="product", cascade="all, delete-orphan")
    discounts = db.relationship("Discount", backref="product", cascade="all, delete-orphan")
