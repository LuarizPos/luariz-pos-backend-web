from app.manage import db,ma

class TransactionModels(db.Model):
    __tablename__ = 'Transaction'

    id = db.Column(db.Integer, primary_key=True)
    id_company = db.Column(db.Integer)
    id_user_company = db.Column(db.Integer)
    id_user_buyer = db.Column(db.Integer)
    buyer_name = db.Column(db.String(250))
    date_time = db.Column(db.TIMESTAMP(timezone=True))
    amount_of_charge = db.Column(db.Float)

    def __init__(self, id_company, id_user_company, id_user_buyer, buyer_name, date_time, amount_of_charge):
        self.id_company = id_company
        self.id_user_company = id_user_company
        self.id_user_buyer = id_user_buyer
        self.buyer_name = buyer_name
        self.date_time = date_time
        self.amount_of_charge = amount_of_charge


class TransactionSchema(ma.Schema):
    class Meta:
        fields = ('id', 'id_company', 'id_user_company', 'id_user_buyer', 'buyer_name', 'date_time', 'amount_of_charge' )