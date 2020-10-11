from app.manage import db,ma

class UsersModel(db.Model):
    __tablename__ = 'Users'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(60), index=True, unique=True)
    email = db.Column(db.String(60), index=True, unique=True)
    password = db.Column(db.String(128))
    status = db.Column(db.Boolean, default=False)
    position = db.Column(db.String(200))
    role_id =  db.Column(db.Integer)

    def __init__(self, name, email, password, status, position, role_id):
        self.name = name
        self.email = email
        self.password = password
        self.status = status
        self.position = position
        self.role_id = role_id

class UsersSchema(ma.Schema):
  class Meta:
    fields = ('id', 'name', 'email', 'password', 'status', 'position', 'role_id')