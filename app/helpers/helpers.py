from flask_restful import Resource, Api
from datetime import datetime, timedelta,  date
import hashlib 
import hmac
import base64
import pybase64
import json
import os

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
        expired_session = datetime.strptime(time_session,"%Y/%m/%d %H:%M:%S")
        date_now = datetime.today()
        if expired_session <= date_now:
            result = {
                "code":440,
                "message": "Session Has Expired and Must Log in Again"        
            }
        else:
            result = {
                "code":200,
                "message": "Session Active"        
            }
        return result
        
