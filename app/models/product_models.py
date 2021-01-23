from app.manage import db,ma

class ProductModels(db.Model):
    __tablename__ = 'Product'

    id = db.Column(db.Integer, primary_key=True)
    id_category = db.Column(db.Integer)
    name = db.Column(db.String(250), index=True, unique=True)
    description = db.Column(db.String(500))
    image = db.Column(db.String(500))
    id_cloudinary = db.Column(db.String(500))
    id_imagekit = db.Column(db.String(500))
    stock = db.Column(db.Integer)
    price = db.Column(db.Integer)

    def __init__(self, id_category, name, description, image, id_cloudinary, id_imagekit, stock, price):
        self.id_category = id_category
        self.id_imagekit = id_imagekit
        self.name = name
        self.description = description
        self.image = image
        self.id_cloudinary = id_cloudinary
        self.stock = stock
        self.price = price


class ProductSchema(ma.Schema):
    class Meta:
        fields = ('id', 'id_category', 'name', 'description', 'image', 'id_cloudinary', 'id_imagekit', 'stock', 'price' )