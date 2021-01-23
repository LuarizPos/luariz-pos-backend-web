from flask_restful import Resource
import hashlib

class ValidationInput(Resource):

    def validation_register(self,param):
        if param['name'] == "":
            result = {
                "code" : 400,
                "message": "name is required",
                "result": []
            }
        elif param['email'] == "" :
            result = {
                "code" : 400,
                "message": "email is required",
                "result": []
            }
        elif param['no_telp'] == "" :
            result = {
                "code" : 400,
                "message": "no_telp is required",
                "result": []
            }
        elif param['password_1'] == '':
            result = {
                "code" : 400,
                "message": "password is required",
                "result": []
            }
        elif param['password_2'] != param['password_2']:
            result = {
                "code" : 400,
                "message": "invalid is password",
                "result": []
            }
        elif param['id_company'] == '':
            result = {
                "code" : 400,
                "message": "id_company is required",
                "result": []
            }
        elif param['address'] == '':
            result = {
                "code" : 400,
                "message": "address is required",
                "result": []
            }
        elif param['role_id'] == '':
            result = {
                "code" : 400,
                "message": "role is required",
                "result": []
            }
        else:
            result = {
                "code" : 200,
                "message": "Param Complete",
                "result": {
                    'name': param['name'],
                    'email': param['email'],
                    'password': hashlib.md5(param['password_1'].encode('utf-8')).hexdigest(),
                    'role_id': param['role_id'],
                    'id_company': param['id_company'],
                    'address': param['address'],
                    "no_telp": param['no_telp'],
                }
            }
        return result

    def validation_login(self,param):
        if param['email'] == "" :
            result = {
                "code" : 400,
                "message": "email is required",
                "result": []
            }
        elif param['password'] == '':
            result = {
                "code" : 400,
                "message": "password is required",
                "result": []
            }
        else:
            result = {
                "code" : 200,
                "message": "Param Complete",
                "result": {
                    'email': param['email'],
                    'password': hashlib.md5(param['password'].encode('utf-8')).hexdigest(),
                }
            }
        return result
    
    def validation_get_users(self,param):
        if param['email'] == "" :
            result = {
                "code" : 400,
                "message": "email is required",
                "result": []
            }
        else:
            result = {
                "code" : 200,
                "message": "Param Complete",
                "result": {
                    'email': param['email'],
                }
            }
        return result
    
    