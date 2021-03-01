from flask import request, jsonify
from flask_restful import Resource
from app.helpers.helpers import Helpers
from app.helpers.response import ResponseApi
from app.helpers.validation import ValidationInput
from app.helpers.send_email import SendEmail
from app.manage import db
from datetime import datetime, timedelta
from app.models.users_models import UsersModel, UsersSchema
from app.models.company_models import CompanyModels, CompanySchema
import json
import os
import pdb
import hashlib

user_schema = UsersSchema()
users_schema = UsersSchema(many=True)
company_schema = CompanySchema()
companys_schema = CompanySchema(many=True)

class UsersController(Resource):
    def get_user(self,param):
        start_time = ResponseApi().microtime(True)
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
                        data = {
                            "id":user_response['id'],
                            "name":user_response['name'],
                            "email":user_response['email'],
                            "role_id":user_response['user_role_id'],
                            "token":user_response['token'],
                        }
                        result = ResponseApi().error_response(200, "Get User", "Get User Succes", start_time, data)
                    else:
                        result = ResponseApi().error_response(400, "Get User", "Your account email not found", start_time)
                 else:
                    result = ResponseApi().error_response(validation['code'], "Get User", validation['message'], start_time)
            else:
                result = ResponseApi().error_response(cek_session['code'], "Get User", cek_session['message'], start_time)
        else:
            result = ResponseApi().error_response(400, "Get Users", "Authentication signature calculation is wrong", start_time)
        response = ResponseApi().response_api(result)
        return response
    
    def generate_token(self,param):
        return Helpers().encode_auth(param)

    def get_token(self,param):
        return Helpers().decode_token(param)

    def register_user(self,param):
        start_time = ResponseApi().microtime(True)
        if Helpers().cek_auth(param):
            form_req = param['form']
            if form_req:
                try:
                    validation = ValidationInput().validation_register(form_req)
                    if validation['code'] == 200:
                        input_data = validation['result']
                        Companys = CompanyModels.query.filter_by(name=input_data["company_name"]).first()
                        data_companys = company_schema.dump(Companys)
                        if not data_companys:
                            # print() 
                            # pdb.run('mymodule.test()')
                            new_company = CompanyModels(input_data['company_name'], input_data['address'], input_data['no_telp'], 
                                    '', '', input_data['email'], '')
                            db.session.add(new_company)
                            db.session.commit()
                            Company = CompanyModels.query.filter_by(name=input_data["company_name"]).first()
                            data_company = company_schema.dump(Company)
                            if data_company:
                                new_user = UsersModel(input_data['name'], input_data['email'] , input_data['no_telp'], input_data['password'], input_data['role_id'], 'null', data_company["id"], input_data['address'],"")
                                db.session.add(new_user)
                                db.session.commit()
                                data = {
                                    "name" : input_data['name'],
                                    "email" : input_data['email']
                                }
                                result = ResponseApi().error_response(200, "Register", "Register Succes", start_time, data)
                            else:
                                result = ResponseApi().error_response(400, "Register", "Company cannot be saved", start_time)
                        else:
                            result = ResponseApi().error_response(400, "Register", "Company Already Exist Please Change Your Name Company", start_time)
                    else:
                        result = ResponseApi().error_response(validation['code'], "Logout", validation['message'], start_time)
                except Exception as e:
                    error  = str(e)
                    result = ResponseApi().error_response(400, "Register", error, start_time) 
            else:
                result = ResponseApi().error_response(400, "Register", "Form Request Is Empty", start_time)
        else:
            result = ResponseApi().error_response(400, "Register", "Authentication signature calculation is wrong", start_time)
        
        response = ResponseApi().response_api(result)
        return jsonify(response)

    def login_user(self,param):
        start_time = ResponseApi().microtime(True)
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
                                    "role_id":user_response['user_role_id'],
                                    "expired_session":expired_session.strftime('%Y/%m/%d %H:%M:%S'),
                                    "status":"Active"
                                }
                                encode_token = Helpers().encode_token(data_user)
                                update_session = self.update_session_user(user_response['id'],encode_token,"Active")
                                if update_session: 
                                    Company = CompanyModels.query.filter_by(id=user_response["id_company"]).first()
                                    data_company = company_schema.dump(Company)
                                    # print(data_company['name'])
                                    # pdb.run('mymodule.test()')
                                    data = {
                                        "name":update_session['name'],
                                        "email":update_session['email'],
                                        "role_id":update_session['user_role_id'],
                                        "token":update_session['token'],
                                        "company":data_company
                                    }
                                    result = ResponseApi().error_response(200, "Login", "Login Succes", start_time, data)
                                else:    
                                    result = ResponseApi().error_response(400, "Login", "Failed Session", start_time)
                            else:
                                
                                result = ResponseApi().error_response(400, "Login", "Your account email is incorrect", start_time)
                        else:
                            
                            result = ResponseApi().error_response(400, "Login", "Your account email is incorrect", start_time)
                    else:
                        result = ResponseApi().error_response(validation['code'], "Logout", validation['message'], start_time)
                except Exception as e:
                    error  = str(e)
                    result = ResponseApi().error_response(400, "Login", error, start_time) 
            else:
                result = ResponseApi().error_response(400, "Login", "Form Request Is Empty", start_time)
        else:
            result = ResponseApi().error_response(400, "Login", "Authentication signature calculation is wrong", start_time)
        response = ResponseApi().response_api(result) 
        return response

    def logout_user(self,param):
        start_time = ResponseApi().microtime(True)
        result ={}
        if Helpers().cek_auth(param):
            form_req = param['form']    
            if form_req:
                try:
                    validation = ValidationInput().validation_logout(form_req)
                    if validation['code'] == 200:
                        input_data = validation['result']
                        email = input_data['email']
                        user = UsersModel.query.filter_by(email=email).first()
                        if user:
                            user_response = user_schema.dump(user)
                            expired_session = (datetime.now() + timedelta(minutes = int(os.getenv('SESSION_EXPIRED'))))
                            data_user = {
                                "name":user_response['name'],
                                "email":user_response['email'],
                                "role_id":user_response['user_role_id'],
                                "expired_session":expired_session.strftime('%Y/%m/%d %H:%M:%S'),
                                "status":"Logout"
                            }
                            encode_token = Helpers().encode_token(data_user)
                            update_session = self.update_session_user(user_response['id'],encode_token,"Logout")
                            if update_session: 
                                data = {
                                    "name":update_session['name'],
                                    "email":update_session['email'],
                                    "role_id":update_session['user_role_id'],
                                    "token":update_session['token'],
                                }
                                result = ResponseApi().error_response(200, "Logout", "Logout Succes", start_time, data)
                        else:
                            result = ResponseApi().error_response(400, "Logout", "Your account email is incorrect", start_time)
                    else:
                        result = ResponseApi().error_response(validation['code'], "Logout", validation['message'], start_time)
                except Exception as e:
                    error  = str(e)
                    result = ResponseApi().error_response(400, "Logout", error, start_time) 
            else:
                result = ResponseApi().error_response(400, "Logout", "Form Request Is Empty", start_time)
        else:
            result = ResponseApi().error_response(400, "Logout", "Authentication signature calculation is wrong", start_time)

        response = ResponseApi().response_api(result)
        return response
    
    def update_user(self,param):
        start_time = ResponseApi().microtime(True)
        if Helpers().cek_auth(param):
            cek_session = Helpers().cek_session(param)
            if cek_session['code'] == 200:
                form_req = param['form']
                resultData = []
                data = {}
                if form_req:
                    try:
                        for form_value in form_req:
                            id_user = form_value['id_user']
                            name = form_value['name']
                            old_password = form_value['old_password']
                            new_password = form_value['new_password']
                            no_telp = form_value['no_telp']
                            role_id = form_value['role_id']
                            address = form_value['address']
                            email = form_value['email']
                            data['name'] = name
                            data['user_role_id'] = role_id
                            data['no_telp'] = no_telp
                            data['address'] = address
                            data['email'] = email
                                
                            user = UsersModel.query.filter_by(id=id_user).first()
                            user_response = user_schema.dump(user)
                            if old_password:
                                if hashlib.md5(old_password.encode('utf-8')).hexdigest() == user_response['password']:
                                    data['password'] = hashlib.md5(new_password.encode('utf-8')).hexdigest()
                                else:
                                    result = ResponseApi().error_response(400, "Update User", "Old Password is Wrong", start_time)
                                    response = ResponseApi().response_api(result)
                                    return response
                            
                            Users = UsersModel.query.filter_by(id=id_user)
                            Users.update(data)
                            db.session.commit()
                            resultData.append(data)
                            result = ResponseApi().error_response(200, "Update Company", "Update Company Succes", start_time, resultData)
                    except Exception as e:
                        error  = str(e)
                        result = ResponseApi().error_response(400, "Update User", error, start_time)
                else:
                    result = ResponseApi().error_response(400, "Update User", "Form Request Is Empty", start_time)

            else:
                result = ResponseApi().error_response(cek_session['code'], "Update User", cek_session['message'], start_time)
        else:
            result = ResponseApi().error_response(400, "Update User", "Authentication signature calculation is wrong", start_time)
        response = ResponseApi().response_api(result)
        return response

    def update_session_user(self,id,token,status):
        user = UsersModel.query.get(id)
        user.token = token
        user.status = status
        db.session.commit()
        return user_schema.dump(user)

    def get_email(self,params):
        paramss = {
            "sample":"halo",
        }
        get = SendEmail().send_email(paramss)
        return get
        
    
