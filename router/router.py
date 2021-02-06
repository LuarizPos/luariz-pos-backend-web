from flask import Blueprint
from app.controller.user_controller import UsersController
from app.controller.product_controller import ProductController
from app.controller.category_controller import CategoryController
from app.controller.company_controller import ComponyController
from app.controller.transaction_controller import TransactionController
from app.controller.authority_controller import AuthorityController
from app.controller.dashboard_controller import DashboardController

from flask import request

urls_blueprint = Blueprint('urls', __name__, url_prefix='/v1')

# ======================router user ============================
@urls_blueprint.route('/dashboard', methods=['GET'])
def get_dashboard():
    param = {
        'auth':request.headers['Authorization'],
        'token':request.headers['Token']
    }
    return DashboardController().get_dashboard(param)

# ======================router user ============================
@urls_blueprint.route('/get_user', methods=['POST'])
def get_user():
    param = {
        'form':request.json['GetUser'],
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

@urls_blueprint.route('/logout_user', methods=['POST'])
def logout_user():
    param = {
        'form':request.json['Logout'],
        'auth':request.headers['Authorization']
    }
    return UsersController().logout_user(param)

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

@urls_blueprint.route('/delete_product', methods=['POST'])
def delete_product():
    param = {
        'form':request.json['Product'],
        'auth':request.headers['Authorization'],
        'token':request.headers['Token']
    }
    
    return ProductController().delete_product(param)


# ======================End router Producr ============================

# ======================router Category ============================
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

@urls_blueprint.route('/delete_category', methods=['POST'])
def delete_category():
    param = {
        'form':request.json['Category'],
        'auth':request.headers['Authorization'],
        'token':request.headers['Token']
    }
    
    return CategoryController().delete_category(param)


# ======================end router Category ============================


# ======================router Company ============================
@urls_blueprint.route('/get_company', methods=['POST'])
def get_company():
    param = {
        'form':request.json['Company'],
        'auth':request.headers['Authorization'],
        'token':request.headers['Token']
    }
    
    return ComponyController().get_company(param)

@urls_blueprint.route('/insert_company', methods=['POST'])
def insert_company():
    param = {
        'form':request.json['Company'],
        'auth':request.headers['Authorization'],
        'token':request.headers['Token']
    }
    
    return ComponyController().insert_company(param)

@urls_blueprint.route('/update_company', methods=['POST'])
def update_company():
    param = {
        'form':request.json['Company'],
        'auth':request.headers['Authorization'],
        'token':request.headers['Token']
    }
    
    return ComponyController().update_company(param)

@urls_blueprint.route('/delete_company', methods=['POST'])
def delete_company():
    param = {
        'form':request.json['Company'],
        'auth':request.headers['Authorization'],
        'token':request.headers['Token']
    }
    
    return ComponyController().delete_company(param)
# ======================end router Company ============================

# ======================router Transaction ============================
@urls_blueprint.route('/get_transaction', methods=['POST'])
def get_transaction():
    param = {
        'form':request.json['Transaction'],
        'auth':request.headers['Authorization'],
        'token':request.headers['Token']
    }
    
    return TransactionController().get_transaction(param)

@urls_blueprint.route('/insert_transaction', methods=['POST'])
def insert_transaction():
    param = {
        'form':request.json['Transaction'],
        'auth':request.headers['Authorization'],
        'token':request.headers['Token']
    }
    
    return TransactionController().insert_transaction(param)

@urls_blueprint.route('/update_transaction', methods=['POST'])
def update_transaction():
    param = {
        'form':request.json['Transaction'],
        'auth':request.headers['Authorization'],
        'token':request.headers['Token']
    }
    
    return TransactionController().update_transaction(param)

@urls_blueprint.route('/delete_transaction', methods=['POST'])
def delete_transaction():
    param = {
        'form':request.json['Transaction'],
        'auth':request.headers['Authorization'],
        'token':request.headers['Token']
    }
    
    return TransactionController().delete_transaction(param)
# ======================end router Transaction ============================

# ======================router Authority ============================
@urls_blueprint.route('/get_authority', methods=['POST'])
def get_authority():
    param = {
        'form':request.json['Authority'],
        'auth':request.headers['Authorization'],
        'token':request.headers['Token']
    }
    
    return AuthorityController().get_authority(param)

@urls_blueprint.route('/insert_authority', methods=['POST'])
def insert_authority():
    param = {
        'form':request.json['Authority'],
        'auth':request.headers['Authorization'],
        'token':request.headers['Token']
    }
    
    return AuthorityController().insert_authority(param)

@urls_blueprint.route('/update_authority', methods=['POST'])
def update_authority():
    param = {
        'form':request.json['Authority'],
        'auth':request.headers['Authorization'],
        'token':request.headers['Token']
    }
    
    return AuthorityController().update_authority(param)

@urls_blueprint.route('/delete_authority', methods=['POST'])
def delete_authority():
    param = {
        'form':request.json['Authority'],
        'auth':request.headers['Authorization'],
        'token':request.headers['Token']
    }
    
    return AuthorityController().delete_authority(param)
# ======================end router Authority ============================
