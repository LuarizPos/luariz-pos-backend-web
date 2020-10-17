from flask_restful import Resource, Api
import hashlib 
import hmac
import base64
import pybase64
import json
import os

class Helpers(Resource):
    def encode_auth(self,param):
        # serialized_dct = json.dumps(param)
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
        bytess = result
        message_bytes = base64.b64decode(bytess+ b'=' * (-len(bytess) % 4)).decode('ascii')
        return message_bytes
    
    def cek_auth(self,param):
        body_req = {
            "secret_text": os.getenv('SECRET_TOKEN')
        }
        encode_token = self.encode_auth(body_req)
        condition = "True" if encode_token == param['auth'] else "False" 
        return condition

        
