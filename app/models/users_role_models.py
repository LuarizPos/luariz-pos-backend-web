from app.manage import db,ma

class UsersRoleModels(db.Model):
    __tablename__ = 'Users_role'

    id = db.Column(db.Integer, primary_key=True)
    name_user_role = db.Column(db.String(250))
    authorities = db.Column(db.Integer)

    def __init__(self, name_user_role, authorities):
        self.name_user_role = name_user_role
        self.authorities = authorities


class UsersRoleSchema(ma.Schema):
    class Meta:
        fields = ('id', 'name_user_role', 'authorities' )