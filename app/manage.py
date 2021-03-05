from flask import Flask, request, jsonify
from flask_marshmallow import Marshmallow 
from flask_migrate import Migrate, MigrateCommand
from flask_sqlalchemy import SQLAlchemy
import cloudinary
from imagekitio import ImageKit
from flask_mail import Mail
from pprint import pprint
# from dotenv import load_dotenv
import os

# Config Imaegekit
imagekit = ImageKit(
    private_key = os.getenv('PRIVATE_KEY_IMAGEKIT'),
    public_key = os.getenv('PUBLIC_KEY_IMAGEKIT'),
    url_endpoint = os.getenv('URL_ENDPOINT_IMAEKIT'),
)
UseImagekit = os.getenv('USE_IMAGEKIT')

#Config Cloudinary
cloudinary.config( 
  cloud_name = os.getenv('CLOUD_NAME'),
  api_key = os.getenv('API_KEY'),
  api_secret = os.getenv('API_SECRET'),
)
UseCloundiary = os.getenv('USE_CLOUDINARY')

#Config Flask
picFolder = os.path.join('../assets','images')
picFolderTempate = os.path.join('../assets','/template/images')
DB_DATABASE = os.getenv('DB_DATABASE')
DB_USERNAME = os.getenv('DB_USERNAME')
DB_PASSWORD = os.getenv('DB_PASSWORD')
DB_HOST = os.getenv('DB_HOST')
app = Flask(__name__,template_folder='../view',static_folder = "../assets")
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://{}:{}@{}/{}'.format(DB_USERNAME,DB_PASSWORD,DB_HOST,DB_DATABASE)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['JSON_SORT_KEYS'] = False
app.config['IMAGE_FOLDER'] = picFolder
app.config['IMAGE_FOLDER_TEMPLATE'] = picFolderTempate

app.config['MAIL_SERVER']= 'smtp.gmail.com'
app.config['MAIL_PORT'] = os.getenv('MAIL_PORT', 465)
app.config['MAIL_USERNAME'] = os.getenv('MAIL_USERNAME')
app.config['MAIL_PASSWORD'] = os.getenv('MAIL_PASSWORD')
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USE_SSL'] = True

db = SQLAlchemy(app)
ma = Marshmallow(app)
mail = Mail(app)
migrate = Migrate(app,db)
db.init_app(app)
migrate.init_app(app,db)



