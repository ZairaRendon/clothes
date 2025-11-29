from app import db

class ProductVariation(db.Model):
    __tablename__ = "product_variations"

    id = db.Column(db.Integer, primary_key=True)
    product_id = db.Column(db.Integer, db.ForeignKey("products.id"), nullable=False)
    size = db.Column(db.String(50))
    color = db.Column(db.String(50))
    stock = db.Column(db.Integer, default=0)

    def __repr__(self):
        return f"<Variation {self.size} {self.color}>"
