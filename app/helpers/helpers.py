from flask_restful import Resource, Api
import hashlib 
import hmac
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
    
    def decode_token(self,param):
        pass
    
    def cek_auth(self,param):
        body_req = {
            "secret_text": os.getenv('SECRET_TOKEN')
        }
        encode_token = self.encode_auth(body_req)
        condition = "True" if encode_token == param['headers'] else "False" 
        return condition

        
