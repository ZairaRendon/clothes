from app.extensions import db
from datetime import datetime

class Sale(db.Model):
    __tablename__ = "sales"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    customer_id = db.Column(db.Integer, db.ForeignKey("customers.id"), nullable=True)
    date = db.Column(db.DateTime, default=datetime.utcnow)
    total = db.Column(db.Float, nullable=False)
    payment_method = db.Column(db.String(50), default="efectivo")  # efectivo, tarjeta, transferencia
    status = db.Column(db.String(50), default="completada")  # completada, pendiente, cancelada
    notes = db.Column(db.Text, nullable=True)

    # Relación con los items de la venta
    items = db.relationship("SaleItem", backref="sale", lazy=True, cascade="all, delete-orphan")

    def __repr__(self):
        return f"<Sale {self.id} Total {self.total}>"