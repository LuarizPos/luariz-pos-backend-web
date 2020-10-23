from flask import request, jsonify
from flask_restful import Resource
from app.helpers.helpers import Helpers
from app.helpers.response import ResponseApi
from app.helpers.validation import ValidationInput
from app.manage import db
from datetime import datetime, timedelta
from app.models.users_models import UsersModel, UsersSchema
import json
import os
import hashlib 

user_schema = UsersSchema()
users_schema = UsersSchema(many=True)


class UsersController(Resource):
    def get_user(self,param):
        if Helpers().cek_auth(param):
            cek_session = Helpers().cek_session(param)
            if cek_session['code'] == 200:
                 form_req = param['form']
                 validation = ValidationInput().validation_get_users(form_req)
                 if validation['code'] == 200:
                    input_data = validation['result']
                    email = input_data['email']
                    user = UsersModel.query.filter_by(email=email).first()
                    if user:
                        user_response = user_schema.dump(user)
                        result = {
                            "code" : 200,
                            "endpoint": "Get Users",
                            "message": "Succes Get Users",
                            "result": {
                                "id":user_response['id'],
                                "name":user_response['name'],
                                "email":user_response['email'],
                                "role_id":user_response['role_id'],
                                "status":user_response['status'],
                                "position":user_response['position'],
                                "token":user_response['token'],
                            }
                        }
                    else:
                        result = {
                            "code" : 400,
                            "endpoint": "Get Users",
                            "message": "Your account email not found",
                            "result": {}
                        }
                 else:
                    result = {
                            "code" : validation['code'],
                            "endpoint": "Get Users",
                            "message": validation['message'],
                            "result": {}
                        }

            else:
                result = {
                    "code" : cek_session['code'],
                    "endpoint": "Get Users",
                    "message": cek_session['message'],
                    "result": {}
                }
            
        else:
            result = {
                "code" : 400,
                "endpoint": "Get Users",
                "message": "Authentication signature calculation is wrong",
                "result": {}
            }
        response = ResponseApi().response_api(result)
        return response
    
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
                        new_user = UsersModel(input_data['name'], input_data['email'] , input_data['password'], True, input_data['position'], input_data['role_id'],'null')
                        db.session.add(new_user)
                        db.session.commit()
                        result = {
                            "code" : 200,
                            "endpoint": "Register",
                            "message": "Register Succes",
                            "result": {}
                        }
                    else:
                        result = {
                            "code" : validation['code'],
                            "endpoint": "Register",
                            "message": validation['message'],
                            "result": {}
                        }
                except Exception as e:
                    error  = str(e)
                    result = {
                        "code" : 400,
                        "endpoint": "Register",
                        "message": error,
                        "result": {}
                    }
            else:
                result = {
                    "code" : 400,
                    "endpoint": "Register",
                    "message": "Form Request Is Empty",
                    "result": {}
                }
        else:
            result = {
                "code" : 400,
                "endpoint": "Register",
                "message": "Authentication signature calculation is wrong",
                "result": {}
            }
        
        response = ResponseApi().response_api(result)
        return jsonify(response)

    def login_user(self,param):
        if Helpers().cek_auth(param):
            form_req = param['form']
            
            if form_req:
                try:
                    validation = ValidationInput().validation_login(form_req)
                    if validation['code'] == 200:
                        input_data = validation['result']
                        email = input_data['email']
                        password = input_data['password']
                        user = UsersModel.query.filter_by(email=email).first()
                        
                        if user:
                            user_response = user_schema.dump(user)
                            
                            if user_response['password'] == password:
                                expired_session = (datetime.now() + timedelta(minutes = int(os.getenv('SESSION_EXPIRED'))))
                                data_user = {
                                    "name":user_response['name'],
                                    "email":user_response['email'],
                                    "role_id":user_response['role_id'],
                                    "status":user_response['status'],
                                    "position":user_response['position'],
                                    "expired_session":expired_session.strftime('%Y/%m/%d %H:%M:%S')
                                }
                                encode_token = Helpers().encode_token(data_user)
                                update_session = self.update_session_user(user_response['id'],encode_token)
                                if update_session:
                                    result = {
                                        "code" : 200,
                                        "message": "Succes Login",
                                        "endpoint": "Login",
                                        "result": {
                                            "name":update_session['name'],
                                            "email":update_session['email'],
                                            "role_id":update_session['role_id'],
                                            "status":update_session['status'],
                                            "position":update_session['position'],
                                            "token":update_session['token'],
                                        }
                                    }
                                else:    
                                    result = {
                                        "code" : 400,
                                        "endpoint": "Login",
                                        "message": "Failed Session",
                                        "result": {}
                                    }
                            else:
                                result = {
                                    "code" : 400,
                                    "endpoint": "Login",
                                    "message": "Your account email or password is incorrect",
                                    "result": {}
                                }
                        else:
                            result = {
                                "code" : 400,
                                "endpoint": "Login",
                                "message": "Your account email or password is incorrect",
                                "result": {}
                            }
                    else:
                        result = {
                            "code" : validation['code'],
                            "endpoint": "Login",
                            "message": validation['message'],
                            "result": {}
                        }

                except Exception as e:
                    error  = str(e)
                    result = {
                        "code" : 400,
                        "endpoint": "Login",
                        "message": error,
                        "result": {}
                    }
            
            else:
                result = {
                    "code" : 400,
                    "endpoint": "Login",
                    "message": "Form Request Is Empty",
                    "result": {}
                }

        else:
            result = {
                "code" : 400,
                "endpoint": "Login",
                "message": "Authentication signature calculation is wrong",
                "result": {}
            }
        response = ResponseApi().response_api(result)
        return response
    
    def update_session_user(self,id,token):
        user = UsersModel.query.get(id)
        user.token = token
        db.session.commit()
        return user_schema.dump(user)
        
    
