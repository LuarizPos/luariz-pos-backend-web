from flask import request, jsonify
from flask_restful import Resource
from app.helpers.helpers import Helpers
from app.helpers.response import ResponseApi
from app.helpers.validation import ValidationInput
from app.manage import db
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
                    validation = ValidationInput().validation_register(form_req)
                    if validation['code'] == 200:
                        input_data = validation['result']
                        new_user = UsersModel(input_data['name'], input_data['email'] , input_data['password'], True, input_data['position'], input_data['role_id'])
                        db.session.add(new_user)
                        db.session.commit()
                        result = {
                            "code" : 200,
                            "message": "Register Succes"
                        }
                    else:
                        result = {
                            "code" : validation['code'],
                            "message": validation['message']
                        }
                except Exception as e:
                    error  = str(e)
                    result = {
                        "code" : 400,
                        "message": error
                    }
            else:
                result = {
                    "code" : 400,
                    "message": "Form Request Is Empty"
                }
        else:
            result = {
                "code" : 400,
                "message": "Form Request Is Empty"
            }
        
        response = ResponseApi().response_api(result)
        return jsonify(response)
    
