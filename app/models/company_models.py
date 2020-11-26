from app.manage import db,ma

class CompanyModels(db.Model):
    __tablename__ = 'Company'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(250))
    address = db.Column(db.String(500))
    no_telp = db.Column(db.BigInteger)
    facebook = db.Column(db.String(250))
    instagram = db.Column(db.String(250))
    email = db.Column(db.String(60), index=True, unique=True)
    website = db.Column(db.String(250))

    def __init__(self, name, address, no_telp, facebook, instagram, email, website ):
        self.name = name
        self.address = address
        self.no_telp = no_telp
        self.facebook = facebook
        self.instagram = instagram
        self.email = email
        self.website = website


class CompanySchema(ma.Schema):
    class Meta:
        fields = ('id', 'name', 'address', 'no_telp', 'facebook', 'instagram', 'email', 'website')