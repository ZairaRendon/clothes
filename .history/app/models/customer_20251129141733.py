from .. import db

class Customer(db.Model):
    _tablename__ = "customers"
    id = db.Column(db.Integer, primary_key=True)
    name = db.column(db.SString(100), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    phone = db.Column(db.String(20))
    purchases = db.relationship("Sale", backref="customer", cascade="all, delete-orphan")
    