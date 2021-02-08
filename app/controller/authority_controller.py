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
                        
                        result = ResponseApi().error_response(200, "Delete Authority", "Get Authority Succes", start_time, resultData)
                    except Exception as e:
                        error  = str(e)
                        result = ResponseApi().error_response(400, "Get Authority", error, start_time)
                else:
                    result = ResponseApi().error_response(400, "Get Authority", "Form Request Is Empty", start_time)
            else:
                result = ResponseApi().error_response(cek_session['code'], "Get Authority", cek_session['message'], start_time)
        else:
            result = ResponseApi().error_response(400, "Get Authority", "Authentication signature calculation is wrong", start_time)
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
                        
                        result = ResponseApi().error_response(200, "Insert Authority", "Insert Authority Succes", start_time, resultData)
                        # print(result)
                        # pdb.run('mymodule.test()')
                    except Exception as e:
                        error  = str(e)
                        result = ResponseApi().error_response(400, "Insert Authority", error, start_time)
                else:
                    result = ResponseApi().error_response(400, "Insert Authority", "Form Request Is Empty", start_time)
            else:
                result = ResponseApi().error_response(cek_session['code'], "Insert Authority", cek_session['message'], start_time)
        else:
            result = ResponseApi().error_response(400, "Insert Authority", "Authentication signature calculation is wrong", start_time)
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
                        
                        result = ResponseApi().error_response(200, "Update Authority", "Update Authority Succes", start_time, resultData)
                        # print(result)
                        # pdb.run('mymodule.test()')
                    except Exception as e:
                        error  = str(e)
                        result = ResponseApi().error_response(400, "Update Authority", error, start_time)
                else:
                    result = ResponseApi().error_response(400, "Update Authority", "Form Request Is Empty", start_time)
            else:
                result = ResponseApi().error_response(cek_session['code'], "Update Authority", cek_session['message'], start_time)
        else:
            result = ResponseApi().error_response(400, "Update Authority", "Authentication signature calculation is wrong", start_time)
            
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
                        
                        result = ResponseApi().error_response(200, "Delete Authority", "Delete Authority Succes", start_time, resultData)
                        
                    except Exception as e:
                        error  = str(e)
                        result = ResponseApi().error_response(400, "Delete Authority", error, start_time)
                else:
                    result = ResponseApi().error_response(400, "Delete Authority", "Form Request Is Empty", start_time)
            else:
                result = ResponseApi().error_response(cek_session['code'], "Delete Authority", cek_session['message'], start_time)
        else:
            result = ResponseApi().error_response(400, "Delete Authority", "Authentication signature calculation is wrong", start_time)
        response = ResponseApi().response_api(result)
        return response