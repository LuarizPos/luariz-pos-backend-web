from flask import Flask, request, jsonify
from flask_marshmallow import Marshmallow 
from flask_migrate import Migrate, MigrateCommand
from flask_sqlalchemy import SQLAlchemy
import os

DB_DATABASE = os.getenv('DB_DATABASE')
DB_USERNAME = os.getenv('DB_USERNAME')
DB_PASSWORD = os.getenv('DB_PASSWORD')
DB_HOST = os.getenv('DB_HOST')
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://{}:{}@{}/{}'.format(DB_USERNAME,DB_PASSWORD,DB_HOST,DB_DATABASE)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
migrate = Migrate()
db.init_app(app)
migrate.init_app(app,db)
ma = Marshmallow()

