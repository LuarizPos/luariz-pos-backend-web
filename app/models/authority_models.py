from app.manage import db,ma

class AuthorityModels(db.Model):
    __tablename__ = 'Authority'

    id = db.Column(db.Integer, primary_key=True)
    name_authority = db.Column(db.String(250))

    def __init__(self, name_authority):
        self.name_authority = name_authority


class AuthoritySchema(ma.Schema):
    class Meta:
        fields = ('id', 'name_authority' )