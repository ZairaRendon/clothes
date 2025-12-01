from app.extensions import db
from datetime import datetime

class Discount(db.Model):
    __tablename__ = "discounts"

    id = db.Column(db.Integer, primary_key=True)
    product_id = db.Column(db.Integer, db.ForeignKey("products.id"), nullable=False)
    percentage = db.Column(db.Float, nullable=False)
    start_date = db.Column(db.DateTime, default=datetime.utcnow)
    end_date = db.Column(db.DateTime)

    def __repr__(self):
        return f"<Discount {self.percentage}% Product {self.product_id}>"
