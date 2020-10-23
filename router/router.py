from flask import Blueprint
from app.controller.user_controller import UsersController
from flask import request

urls_blueprint = Blueprint('urls', __name__, url_prefix='/v1')

@urls_blueprint.route('/get_user', methods=['POST'])
def get_user():
    param = {
        'form':request.form,
        'auth':request.headers['Authorization'],
        'token':request.headers['Token']
    }
    return UsersController().get_user(param)

@urls_blueprint.route('/register_user', methods=['POST'])
def register_user():
    param = {
        'form':request.form,
        'auth':request.headers['Authorization']
    }
    return UsersController().register_user(param)

@urls_blueprint.route('/login_user', methods=['POST'])
def login_user():
    param = {
        'form':request.form,
        'auth':request.headers['Authorization']
    }
    return UsersController().login_user(param)

@urls_blueprint.route('/generate_token', methods=['POST'])
def generate_token():
    param = request.form
    return UsersController().generate_token(param)

@urls_blueprint.route('/decode_token', methods=['POST'])
def decode_token():
    param = request.form
    return UsersController().get_token(param)
