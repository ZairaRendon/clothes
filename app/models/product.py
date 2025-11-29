from app import db

class Product(db.Model):
    __tablename__ = "products"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(255))
    price = db.Column(db.Float, nullable=False)
    stock = db.Column(db.Integer, nullable=False, default=0)

    variations = db.relationship("ProductVariation", backref="product", lazy=True)
    discounts = db.relationship("Discount", backref="product", lazy=True)

    def __repr__(self):
        return f"<Product {self.name}>"
