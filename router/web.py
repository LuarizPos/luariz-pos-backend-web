from flask import Blueprint
from flask import request, render_template
from app.manage import app
import secrets
from app.helpers.helpers import Helpers
import os

web_blueprint = Blueprint('web', __name__, url_prefix='/')

@web_blueprint.route('/', methods=['GET'])
def hello_word():
    return "WELCOME TO API LUARIZPOS V1"

@web_blueprint.route('/desplay/<filename>',methods=['GET'])
def display_image(filename):
    imageFilename = os.path.join(app.config['IMAGE_FOLDER'], filename)
    return render_template("index.html", images = imageFilename)

@web_blueprint.route('/images/<filename>',methods=['GET'])
def display_images(filename):
    imageFilename = os.path.join(app.config['IMAGE_FOLDER_TEMPLATE'], filename)
    return render_template("index.html", images = imageFilename)

@web_blueprint.route('/get_email_view', methods=['GET'])
def get_email_view():
    code_activated = secrets.token_urlsafe(16)
    input_data = {
        "name":"ss",
        "email":"ss@mail.com",
    }
    encode_validation = Helpers().create_session(input_data,'not_confirm',code_activated)
    url_roots = request.url_root
    content = {
        'url_roots' : url_roots,
        'encode_validation' : encode_validation
    }
    return render_template('mail_welcome_confirm.html',content = content)