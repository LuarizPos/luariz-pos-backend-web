from flask import Flask, request, jsonify
from flask_marshmallow import Marshmallow 
from flask_migrate import Migrate, MigrateCommand
from flask_sqlalchemy import SQLAlchemy
import cloudinary

# from dotenv import load_dotenv
import os

# load_dotenv()
cloudinary.config( 
  cloud_name = os.getenv('CLOUD_NAME'),
  api_key = os.getenv('API_KEY'),
  api_secret = os.getenv('API_SECRET'),
)
UseCloundiary = os.getenv('USE_CLOUDINARY'),
picFolder = os.path.join('../assets','images')
DB_DATABASE = os.getenv('DB_DATABASE')
DB_USERNAME = os.getenv('DB_USERNAME')
DB_PASSWORD = os.getenv('DB_PASSWORD')
DB_HOST = os.getenv('DB_HOST')
app = Flask(__name__,template_folder='../view',static_folder = "../assets")
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://{}:{}@{}/{}'.format(DB_USERNAME,DB_PASSWORD,DB_HOST,DB_DATABASE)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['JSON_SORT_KEYS'] = False
app.config['IMAGE_FOLDER'] = picFolder
db = SQLAlchemy(app)
ma = Marshmallow(app)
migrate = Migrate(app,db)
db.init_app(app)
migrate.init_app(app,db)


