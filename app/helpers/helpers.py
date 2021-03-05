from flask_restful import Resource, Api
from datetime import datetime, timedelta
from app.models.users_models import UsersModel, UsersSchema
import hashlib 
import hmac
import base64
import pybase64
import json
import os
import pdb

user_schema = UsersSchema()
users_schema = UsersSchema(many=True)

class Helpers(Resource):
    def encode_auth(self,param):
        serialized_dct = param['secret_text']
        decode = hashlib.sha256(serialized_dct.encode('utf-8')).hexdigest()
        uniq_code_1 = decode[:10]
        uniq_code_2 = decode[10:]
        result = uniq_code_1+"92f"+uniq_code_2
        return result
    
    def encode_token(self,param):
        serialized_dct = json.dumps(param).encode('utf-8')
        base64_bytes = base64.b64encode(serialized_dct)
        base64_message = base64_bytes.decode('utf-8')
        uniq_code_1 = base64_message[:10]
        uniq_code_2 = base64_message[10:]
        result = uniq_code_1+"zYt"+uniq_code_2
        return result
    
    def decode_token(self,param):
        base64 = param['token']
        uniq_code_1 = base64[:10]
        uniq_code_2 = base64[13:]
        result = uniq_code_1+uniq_code_2
        bytess = result.encode('utf-8')
        message_bytes = pybase64.b64decode(bytess, altchars='_:', validate=True)
        return message_bytes
    
    def decode_image(self,image_encode):
        try:
            image_bytes = image_encode.encode('utf-8')
            image_decode = pybase64.b64decode(image_bytes, altchars='_:', validate=True)
        except Exception as e:
            image_decode = 0
        return image_decode
    
    def cek_auth(self,param):
        body_req = {
            "secret_text": os.getenv('SECRET_TOKEN')
        }
        encode_token = self.encode_auth(body_req)
        condition = "True" if encode_token == param['auth'] else "False" 
        return condition

    def cek_session(self,param):
        decode_token = self.decode_token(param)
        decode_token = json.loads(decode_token)
        time_session = decode_token['expired_session']
        status_token = decode_token['status']
        code_activated = decode_token['code_activated']
        email_token = decode_token['email']
        # print(decode_token)
        # pdb.run('mymodule.test()')
        expired_session = datetime.strptime(time_session,"%Y/%m/%d %H:%M:%S")
        date_now = datetime.today()
        if expired_session <= date_now:
            result = {
                "code":440,
                "message": "Session Has Expired and Must Log in Again",
                "time_session":"",
                "code_activated":"",
                "data":{}
            }
        else:
            user = UsersModel.query.filter_by(email=email_token).first()
            user_response = user_schema.dump(user)
            status_db   = user_response['status']
            if status_db == 'confirm':
                result = {
                    "code":200,
                    "message": "Account is confirm",
                    "time_session":time_session,
                    "code_activated":code_activated,
                    "data":user_response
                }
            elif status_token == status_db:
                result = {
                    "code":200,
                    "message": "Session Active",
                    "time_session":time_session,
                    "code_activated":code_activated,
                    "data":user_response
                }
            else:
                result = {
                    "code":440,
                    "message": "Session Is Logout",
                    "time_session":"",
                    "code_activated":"",
                    "data":{}
                }

        return result

    def create_session(self,params,status,code_activated):
        expired_session = (datetime.now() + timedelta(minutes = int(os.getenv('SESSION_EXPIRED'))))
        data_user = {
            "name":params['name'],
            "email":params['email'],
            "expired_session":expired_session.strftime('%Y/%m/%d %H:%M:%S'),
            "status":status,
            "code_activated":code_activated
        }
        encode_token = self.encode_token(data_user)
        return encode_token
