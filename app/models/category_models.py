from app.manage import db,ma

class CategoryModels(db.Model):
    __tablename__ = 'Category'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(250), index=True, unique=True)

    def __init__(self, name):
        self.name = name
    

class CategorySchema(ma.Schema):
    class Meta:
        fields = ("id", "name")