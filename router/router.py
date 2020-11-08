from flask import Blueprint
from app.controller.user_controller import UsersController
from app.controller.product_controller import ProductController
from app.controller.category_controller import CategoryController

from flask import request

urls_blueprint = Blueprint('urls', __name__, url_prefix='/v1')

# ======================router user ============================
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
        'form':request.json['Register'],
        'auth':request.headers['Authorization']
    }
    return UsersController().register_user(param)

@urls_blueprint.route('/login_user', methods=['POST'])
def login_user():
    param = {
        'form':request.json['Login'],
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

# ======================end router user ============================

# ======================router Producr ============================
@urls_blueprint.route('/insert_product', methods=['POST'])
def insert_product():
    param = {
        'form':request.json['Product'],
        'auth':request.headers['Authorization'],
        'token':request.headers['Token']
    }
    
    return ProductController().insert_product(param)

@urls_blueprint.route('/update_product', methods=['POST'])
def update_product():
    param = {
        'form':request.json['Product'],
        'auth':request.headers['Authorization'],
        'token':request.headers['Token']
    }
    
    return ProductController().update_product(param)

@urls_blueprint.route('/get_product', methods=['POST'])
def get_product():
    param = {
        'form':request.json['Product'],
        'auth':request.headers['Authorization'],
        'token':request.headers['Token']
    }
    
    return ProductController().get_product(param)

# ======================End router Producr ============================

# ======================router Producr ============================
@urls_blueprint.route('/insert_category', methods=['POST'])
def insert_category():
    param = {
        'form':request.json['Category'],
        'auth':request.headers['Authorization'],
        'token':request.headers['Token']
    }
    
    return CategoryController().insert_category(param)

@urls_blueprint.route('/update_category', methods=['POST'])
def update_category():
    param = {
        'form':request.json['Category'],
        'auth':request.headers['Authorization'],
        'token':request.headers['Token']
    }
    
    return CategoryController().update_category(param)

@urls_blueprint.route('/get_category', methods=['POST'])
def get_category():
    param = {
        'form':request.json['Category'],
        'auth':request.headers['Authorization'],
        'token':request.headers['Token']
    }
    
    return CategoryController().get_category(param)
