from flask import Flask, request, jsonify
from flask_restful import Resource, Api
from app.helpers.helpers import Helpers
from app.manage import db,ma
from app.models.users_models import UsersModel, UsersSchema
import json
import hashlib 

user_schema = UsersSchema()
users_schema = UsersSchema(many=True)

class UsersController(Resource):
    def get_user():
        all_data = UsersModel.query.all()
        result = users_schema.dump(all_data)
        return jsonify(result)
    
    def generate_token(self,param):
        return Helpers().encode_auth(param)

    def get_token(self,param):
        return Helpers().decode_token(param)

    def register_user(self,param):
        if Helpers().cek_auth(param):
            form_req = param['form']
            if form_req:
                try:
                    name = form_req['name'] 
                    email = form_req['email']
                    password = form_req['password']
                    password = hashlib.md5(password.encode('utf-8')).hexdigest()
                    status = form_req['status']
                    position = form_req['position']
                    role_id = form_req['role_id']
                    new_user = UsersModel(name, email, password, True, position, role_id)
                    db.session.add(new_user)
                    db.session.commit()
                    result = {
                        "code" : 200,
                        "message ": "Data Save Succes"
                    }
                except Exception as e:
                    error  = str(e)
                    result = {
                        "code" : 400,
                        "message ": error
                    }
            else:
                result = {
                    "code" : 400,
                    "message ": "Form Request Is Empty"
                }
            
        return jsonify(result)