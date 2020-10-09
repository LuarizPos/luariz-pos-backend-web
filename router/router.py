from flask import Blueprint
from app.controller.user_controller import UsersController

urls_blueprint = Blueprint('urls', __name__,)

@urls_blueprint.route('/get_user')
def get_user():
    return User().get_user()