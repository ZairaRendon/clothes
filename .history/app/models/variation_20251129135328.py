from .. import db

class ProductVariation(db.Model):
    __tablename__ = "product_variations"
    id = db.Column(db.Integer, primary_key=True)
    product_id = db.Column(db.Integer, db.ForeignKey("products.id"), nullable=False)
    size = db.Column(db.String(10))
    color = db.Column(db.String(20))
