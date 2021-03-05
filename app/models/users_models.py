from app.manage import db,ma
# 

class UsersModel(db.Model):
    __tablename__ = 'Users'

    id = db.Column(db.Integer, primary_key=True)
    id_company = db.Column(db.Integer)
    name = db.Column(db.String(60), index=True, unique=True)
    email = db.Column(db.String(60), index=True, unique=True)
    address = db.Column(db.String(500))
    password = db.Column(db.String(128))
    no_telp = db.Column(db.String(15))
    user_role_id =  db.Column(db.Integer)
    token =  db.Column(db.String(500))
    status = db.Column(db.String(50))
    code_activated = db.Column(db.String(50))


    def __init__(self, name, email,no_telp, password, user_role_id,token, id_company, address, status,code_activated):
        self.name = name
        self.no_telp = no_telp
        self.email = email
        self.password = password
        self.user_role_id = user_role_id
        self.token = token
        self.id_company = id_company
        self.address = address
        self.status = status
        self.code_activated = code_activated

class UsersSchema(ma.Schema):
  class Meta:
    fields = ('id', 'name', 'email', 'no_telp', 'password', 'user_role_id', 'token', 'id_company', 'address', 'status', 'code_activated')