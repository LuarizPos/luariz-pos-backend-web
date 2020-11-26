from app.manage import db,ma

class CartModels(db.Model):
    __tablename__ = 'Cart'

    id = db.Column(db.Integer, primary_key=True)
    id_transaction = db.Column(db.Integer)
    id_product = db.Column(db.Integer)
    qty = db.Column(db.Integer)
    price = db.Column(db.Float)

    def __init__(self, id_transaction, id_product, qty, price):
        self.id_transaction = id_transaction
        self.id_product = id_product
        self.qty = qty
        self.price = price


class CartSchema(ma.Schema):
    class Meta:
        fields = ('id', 'id_transaction', 'id_product', 'qty', 'price')