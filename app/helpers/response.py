from flask_restful import Resource

class ResponseApi(Resource):

    def response_api(self,param):
        response = {
            "API_LuarizPost": {
                "Version": "V.1",
                "Timestamp": "2020-10-03T02:10:14+07:00",
                "NameEnd": param['endpoint'],
                "Status": "Complete",
                "Message": {
                    "Type": "Info",
                    "ShortText": param['message'],
                    "Speed": "21.36",
                    "Code": param['code']
                },
                "Response": param['result']
            }
        }
        return response
