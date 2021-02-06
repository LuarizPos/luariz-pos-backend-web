from app.models.authority_models import AuthorityModels, AuthoritySchema
from flask_restful import Resource
from flask import request, jsonify
from app.helpers.helpers import Helpers
from app.helpers.response import ResponseApi
from app.manage import db
import pdb

authority_schema = AuthoritySchema()
authoritys_schema = AuthoritySchema(many=True)

class AuthorityController(Resource):

    def get_authority(self,param):
        start_time = ResponseApi().microtime(True)
        if Helpers().cek_auth(param):
            cek_session = Helpers().cek_session(param)
            if cek_session['code'] == 200:
                form_req = param['form']
                resultData = []
                if form_req:
                    try:
                        show_all = form_req['show_all']
                        id_authority = form_req['id_authority']
                        if show_all:
                            Authority = AuthorityModels.query.all()
                            data_auth = authoritys_schema.dump(Authority)
                            for auth_value in data_auth:
                                if(auth_value):
                                    data = {
                                        "id_authority": auth_value['id'],
                                        "name_authority": auth_value['name_authority'],
                                    }
                                    resultData.append(data)

                        else:
                            Authority = AuthorityModels.query.filter_by(id=id_authority).first()
                            data_auth = authority_schema.dump(Authority)
                            data = {
                                "id_authority": data_auth['id'],
                                "name_authority": data_auth['name_authority'],
                            }
                            resultData.append(data)
                        
                        result = {
                            "code" : 200,
                            "SpeedTime" : ResponseApi().speed_response(start_time),
                            "endpoint": "Get Authority",
                            "message": "Get Authority Succes",
                            "result": resultData
                        }
                    except Exception as e:
                        error  = str(e)
                        result = {
                            "code" : 400,
                            "SpeedTime" : ResponseApi().speed_response(start_time),
                            "endpoint": "Get Authority",
                            "message": error,
                            "result": {}
                        }
                else:
                    result = {
                        "code" : 400,
                        "SpeedTime" : ResponseApi().speed_response(start_time),
                        "endpoint": "Get Authority",
                        "message": "Form Request Is Empty",
                        "result": {}
                    }
            else:
                result = {
                    "code" : cek_session['code'],
                    "SpeedTime" : ResponseApi().speed_response(start_time),
                    "endpoint": "Get Authority",
                    "message": cek_session['message'],
                    "result": {}
                }
        else:
            result = {
                "code" : 400,
                "SpeedTime" : ResponseApi().speed_response(start_time),
                "endpoint": "Get Authority",
                "message": "Authentication signature calculation is wrong",
                "result": {}
            }
        response = ResponseApi().response_api(result)
        return response

    def insert_authority(self,param):
        start_time = ResponseApi().microtime(True)
        if Helpers().cek_auth(param):
            cek_session = Helpers().cek_session(param)
            if cek_session['code'] == 200:
                form_req = param['form']
                resultData = []
                if form_req:
                    try: 
                        for form_value in form_req:
                            name_authority = form_value['name_authority']
                            new_authority = AuthorityModels(name_authority)
                            db.session.add(new_authority)
                            db.session.commit()
                            data = {
                                "name_authority" : name_authority,
                            }    
                            resultData.append(data)
                        result = {
                            "code" : 200,
                            "SpeedTime" : ResponseApi().speed_response(start_time),
                            "endpoint": "Insert Authority",
                            "message": "Insert Authority Succes",
                            "result": resultData
                        }    
                        # print(result)
                        # pdb.run('mymodule.test()')
                    except Exception as e:
                        error  = str(e)
                        result = {
                            "code" : 400,
                            "SpeedTime" : ResponseApi().speed_response(start_time),
                            "endpoint": "Insert Authority",
                            "message": error,
                            "result": {}
                        }
                else:
                    result = {
                        "code" : 400,
                        "SpeedTime" : ResponseApi().speed_response(start_time),
                        "endpoint": "Insert Authority",
                        "message": "Form Request Is Empty",
                        "result": {}
                    }
            else:
                result = {
                    "code" : cek_session['code'],
                    "SpeedTime" : ResponseApi().speed_response(start_time),
                    "endpoint": "Insert Authority",
                    "message": cek_session['message'],
                    "result": {}
                }
        else:
            result = {
                "code" : 400,
                "SpeedTime" : ResponseApi().speed_response(start_time),
                "endpoint": "Insert Authority",
                "message": "Authentication signature calculation is wrong",
                "result": {}
            }

        response = ResponseApi().response_api(result)
        return response

    def update_authority(self,param):
        start_time = ResponseApi().microtime(True)
        if Helpers().cek_auth(param):
            cek_session = Helpers().cek_session(param)
            if cek_session['code'] == 200:
                form_req = param['form']
                resultData = []
                if form_req:
                    try:
                        for form_value in form_req:
                            id_authority = form_value['id_authority']
                            name_authority = form_value['name_authority']
                            data = {
                                "name_authority" : name_authority,
                            }
                            Authority = AuthorityModels.query.filter_by(id=id_authority)
                            Authority.update(data)
                            db.session.commit()
                            resultData.append(data)
                        result = {
                            "code" : 200,
                            "SpeedTime" : ResponseApi().speed_response(start_time),
                            "endpoint": "Update Authority",
                            "message": "Update Authority Succes",
                            "result": resultData
                        }
                        # print(result)
                        # pdb.run('mymodule.test()')
                    except Exception as e:
                        error  = str(e)
                        result = {
                            "code" : 400,
                            "SpeedTime" : ResponseApi().speed_response(start_time),
                            "endpoint": "Update Authority",
                            "message": error,
                            "result": {}
                        }
                else:
                    result = {
                        "code" : 400,
                        "SpeedTime" : ResponseApi().speed_response(start_time),
                        "endpoint": "Update Authority",
                        "message": "Form Request Is Empty",
                        "result": {}
                    }
            else:
                result = {
                    "code" : cek_session['code'],
                    "SpeedTime" : ResponseApi().speed_response(start_time),
                    "endpoint": "Update Authority",
                    "message": cek_session['message'],
                    "result": {}
                }
        else:
            result = {
                "code" : 400,
                "SpeedTime" : ResponseApi().speed_response(start_time),
                "endpoint": "Update Authority",
                "message": "Authentication signature calculation is wrong",
                "result": {}
            }    
        response = ResponseApi().response_api(result)
        return response

    def delete_authority(self,param):
        start_time = ResponseApi().microtime(True)
        if Helpers().cek_auth(param):
            cek_session = Helpers().cek_session(param)
            if cek_session['code'] == 200:
                form_req = param['form']
                resultData = []
                if form_req:
                    try:
                        for form_value in form_req:
                            delete_All = form_value['delete_all']
                            if delete_All:
                                Authority = AuthorityModels.query.order_by(AuthorityModels.id.asc())
                                data_authority = authoritys_schema.dump(Authority)
                                for auth_value in data_authority:
                                    data = {
                                        'id':auth_value['id'],
                                        "name_authority" : auth_value['name_authority'],
                                    }
                                    resultData.append(data)
                                AuthorityModels.query.delete()
                                db.session.commit()
                            else:
                                id_authority = form_value['id_authority']
                                Authority = AuthorityModels.query.filter_by(id=id_authority).first()
                                Authority_value = authority_schema.dump(Authority)
                                db.session.delete(Authority)
                                db.session.commit()
                                data = {
                                    'id':Authority_value['id'],
                                    "name_authority" : Authority_value['name_authority'],
                                }
                                resultData.append(data)
                        result = {
                            "code" : 200,
                            "SpeedTime" : ResponseApi().speed_response(start_time),
                            "endpoint": "Delete Authority",
                            "message": "Delete Authority Succes",
                            "result": resultData
                        }
                        
                    except Exception as e:
                        error  = str(e)
                        result = {
                            "code" : 400,
                            "SpeedTime" : ResponseApi().speed_response(start_time),
                            "endpoint": "Delete Authority",
                            "message": error,
                            "result": {}
                        }
                else:
                    result = {
                        "code" : 400,
                        "SpeedTime" : ResponseApi().speed_response(start_time),
                        "endpoint": "Delete Authority",
                        "message": "Form Request Is Empty",
                        "result": {}
                    }
            else:
                result = {
                    "code" : cek_session['code'],
                    "SpeedTime" : ResponseApi().speed_response(start_time),
                    "endpoint": "Update Authority",
                    "message": cek_session['message'],
                    "result": {}
                }
        else:
            result = {
                "code" : 400,
                "SpeedTime" : ResponseApi().speed_response(start_time),
                "endpoint": "Delete Authority",
                "message": "Authentication signature calculation is wrong",
                "result": {}
            }
        response = ResponseApi().response_api(result)
        return response