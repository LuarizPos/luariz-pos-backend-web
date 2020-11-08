from app.manage import db,ma

class ProductModels(db.Model):
    __tablename__ = 'Product'

    id = db.Column(db.Integer, primary_key=True)
    category_id = db.Column(db.Integer)
    name = db.Column(db.String(250), index=True, unique=True)
    description = db.Column(db.String(500))
    image = db.Column(db.String(500))
    stock = db.Column(db.Integer)
    price = db.Column(db.Integer)

    def __init__(self, category_id, name, description, image, stock, price):
        self.category_id = category_id
        self.name = name
        self.description = description
        self.image = image
        self.stock = stock
        self.price = price


class ProductSchema(ma.Schema):
    class Meta:
        fields = ('id', 'category_id', 'name', 'description', 'image', 'stock', 'price' )