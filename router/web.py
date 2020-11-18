from flask import Blueprint
from flask import request, render_template
from app.manage import app
import os

web_blueprint = Blueprint('web', __name__, url_prefix='/')

@web_blueprint.route('/', methods=['GET'])
def hello_word():
    return "WELCOME TO API LUARIZPOS V1"

@web_blueprint.route('/display/<filename>',methods=['GET'])
def display_image(filename):
    imageFilename = os.path.join(app.config['IMAGE_FOLDER'], filename)
    return render_template("index.html", images = imageFilename)
