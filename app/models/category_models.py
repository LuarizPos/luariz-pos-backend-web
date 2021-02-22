from app.manage import db,ma

class CategoryModels(db.Model):
    __tablename__ = 'Category'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(250), index=True, unique=True)
    id_company = db.Column(db.Integer)

    def __init__(self, name,id_company):
        self.name = name
        self.id_company = id_company
    

class CategorySchema(ma.Schema):
    class Meta:
        fields = ("id", "name", "id_company")