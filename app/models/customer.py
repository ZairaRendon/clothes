from app.extensions import db

class Customer(db.Model):
    __tablename__ = "customers"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), unique=True)
    phone = db.Column(db.String(20))

    sales = db.relationship("Sale", backref="customer", lazy=True)

    def __repr__(self):
        return f"<Customer {self.name}>"
