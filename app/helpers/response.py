from flask_restful import Resource
import time
from datetime import datetime

class ResponseApi(Resource):

    def response_api(self,param):
        response = {
            "API_LuarizPos": {
                "Version": "V.1",
                "Timestamp": "2020-10-03T02:10:14+07:00",
                "NameEnd": param['endpoint'],
                "Status": "Complete",
                "Message": {
                    "Type": "Info",
                    "ShortText": param['message'],
                    "Speed": param['SpeedTime'],
                    "Code": param['code']
                },
                "Response": param['result']
            }
        }
        return response

    def speed_response(self,start):
        end = self.microtime(True)
        timer = end - start
        hours = (int)(timer/60/60)
        minute = (int)(timer/60) - hours*60
        second = timer - hours*60*60 - minute*60
        return float("{:.2f}".format(second))

    def microtime(self,get_as_float = False) :
        d = datetime.now()
        t = time.mktime(d.timetuple()) + d.microsecond / 1000000.00
        if get_as_float:
            return t
        else:
            ms = d.microsecond / 1000000.
            return '%f %d' % (ms, t)
    
    def error_response(self, code, endpoint, messege, start_time, result={}):
        result = {
            "code" : code,
            "SpeedTime" : self.speed_response(start_time),
            "endpoint": messege,
            "message": endpoint,
            "result": result
        }
        return result
