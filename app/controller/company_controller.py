from app.models.company_models import CompanyModels, CompanySchema
from flask_restful import Resource
from flask import request, jsonify
from app.helpers.helpers import Helpers
from app.helpers.response import ResponseApi
from app.manage import db
from PIL import Image
import pdb
import io

company_schema = CompanySchema()
companys_schema = CompanySchema(many=True)

class ComponyController(Resource):
    def get_company(self,param):
        if Helpers().cek_auth(param):
            # cek_session = Helpers().cek_session(param)
            # if cek_session['code'] == 200:
                form_req = param['form']
                if form_req:
                    try:
                        showAll = form_req['ShowAll']
                        id_company = form_req['id_company']
                        if showAll:
                            Company = CompanyModels.query.all()
                            data = companys_schema.dump(Company)
                        else:
                            Company = CompanyModels.query.filter_by(id=id_company).first()
                            data = companys_schema.dump(Company)
                        
                        result = {
                            "code" : 200,
                            "endpoint": "Get Company",
                            "message": "Get Company Succes",
                            "result": data
                        }
                    except Exception as e:
                        error  = str(e)
                        result = {
                            "code" : 400,
                            "endpoint": "Get Company",
                            "message": error,
                            "result": {}
                        }
                else:
                    result = {
                        "code" : 400,
                        "endpoint": "Get Company",
                        "message": "Form Request Is Empty",
                        "result": {}
                    }
            # else:
            #     result = {
            #         "code" : cek_session['code'],
            #         "endpoint": "Get Company",
            #         "message": cek_session['message'],
            #         "result": {}
            #     }
        else:
            result = {
                "code" : 400,
                "endpoint": "Get Company",
                "message": "Authentication signature calculation is wrong",
                "result": {}
            }
        response = ResponseApi().response_api(result)
        return response
        

    def insert_company(self,param):
        if Helpers().cek_auth(param):
            # cek_session = Helpers().cek_session(param)
            # if cek_session['code'] == 200:
                form_req = param['form']
                resultData = []
                if form_req:
                    try: 
                        for form_value in form_req:
                            name_company = form_value['name_company']
                            address_company = form_value['address_company']
                            no_tlp_company = form_value['no_tlp_company']
                            facebook_company = form_value['facebook_company']
                            instagram_company = form_value['instagram_company']
                            email_company = form_value['email_company']
                            website_company = form_value['website_company']
                            new_company = CompanyModels(name_company, address_company, no_tlp_company, 
                                    facebook_company, instagram_company, email_company, website_company)
                            db.session.add(new_company)
                            db.session.commit()
                            data = {
                                "name" : name_company,
                                "address" : address_company,
                                "no_telp" : no_tlp_company,
                                "facebook" : facebook_company,
                                "instagram" : instagram_company,
                                "email" : email_company,
                                "website" : website_company
                            }    
                            resultData.append(data)
                        result = {
                            "code" : 200,
                            "endpoint": "Insert Company",
                            "message": "Insert Company Succes",
                            "result": resultData
                        }    
                        # print(result)
                        # pdb.run('mymodule.test()')
                    except Exception as e:
                        error  = str(e)
                        result = {
                            "code" : 400,
                            "endpoint": "Insert Company",
                            "message": error,
                            "result": {}
                        }
                else:
                    result = {
                        "code" : 400,
                        "endpoint": "Insert Company",
                        "message": "Form Request Is Empty",
                        "result": {}
                    }
            # else:
            #     result = {
            #         "code" : cek_session['code'],
            #         "endpoint": "Insert Company",
            #         "message": cek_session['message'],
            #         "result": {}
            #     }
        
        else:
            result = {
                "code" : 400,
                "endpoint": "Insert Company",
                "message": "Authentication signature calculation is wrong",
                "result": {}
            }

        response = ResponseApi().response_api(result)
        return response

    def update_company(self,param):
        if Helpers().cek_auth(param):
            # cek_session = Helpers().cek_session(param)
            # if cek_session['code'] == 200:
                form_req = param['form']
                resultData = []
                if form_req:
                    try:
                        for form_value in form_req:
                            id_company = form_value['id_company']
                            name_company = form_value['name_company']
                            address_company = form_value['address_company']
                            no_tlp_company = form_value['no_tlp_company']
                            facebook_company = form_value['facebook_company']
                            instagram_company = form_value['instagram_company']
                            email_company = form_value['email_company']
                            website_company = form_value['website_company']
                            data = {
                                "name" : name_company,
                                "address" : address_company,
                                "no_telp" : no_tlp_company,
                                "facebook" : facebook_company,
                                "instagram" : instagram_company,
                                "email" : email_company,
                                "website" : website_company
                            }
                            Company = CompanyModels.query.filter_by(id=id_company)
                            Company.update(data)
                            db.session.commit()
                            resultData.append(data)
                        result = {
                            "code" : 200,
                            "endpoint": "Update Company",
                            "message": "Update Company Succes",
                            "result": resultData
                        }
                        # print(result)
                        # pdb.run('mymodule.test()')
                    except Exception as e:
                        error  = str(e)
                        result = {
                            "code" : 400,
                            "endpoint": "Update Company",
                            "message": error,
                            "result": {}
                        }
                else:
                    result = {
                        "code" : 400,
                        "endpoint": "Update Company",
                        "message": "Form Request Is Empty",
                        "result": {}
                    }
            # else:
            #     result = {
            #         "code" : cek_session['code'],
            #         "endpoint": "Update Company",
            #         "message": cek_session['message'],
            #         "result": {}
            #     }
        else:
            result = {
                "code" : 400,
                "endpoint": "Update Company",
                "message": "Authentication signature calculation is wrong",
                "result": {}
            }    
        response = ResponseApi().response_api(result)
        return response

    def delete_company(self,param):
        if Helpers().cek_auth(param):
            # cek_session = Helpers().cek_session(param)
            # if cek_session['code'] == 200:
                form_req = param['form']
                resultData = []
                if form_req:
                    try:
                        for form_value in form_req:
                            id_company = form_value['id_company']
                            Company = CompanyModels.query.filter_by(id=id_company).first()
                            Company_value = company_schema.dump(Company)
                            db.session.delete(Company)
                            db.session.commit()
                            data = {
                                'id':Company_value['id'],
                                "name" : Company_value['name'],
                                "address" : Company_value['address'],
                                "no_telp" : Company_value['no_telp'],
                                "facebook" : Company_value['facebook'],
                                "instagram" : Company_value['instagram'],
                                "email" : Company_value['email'],
                                "website" : Company_value['website'],
                            }
                            resultData.append(data)
                        result = {
                            "code" : 200,
                            "endpoint": "Delete Company",
                            "message": "Delete Company Succes",
                            "result": resultData
                        }
                        
                    except Exception as e:
                        error  = str(e)
                        result = {
                            "code" : 400,
                            "endpoint": "Delete Company",
                            "message": error,
                            "result": {}
                        }
                else:
                    result = {
                        "code" : 400,
                        "endpoint": "Delete Company",
                        "message": "Form Request Is Empty",
                        "result": {}
                    }
            # else:
            #     result = {
            #         "code" : cek_session['code'],
            #         "endpoint": "Update Company",
            #         "message": cek_session['message'],
            #         "result": {}
            #     }
        else:
            result = {
                "code" : 400,
                "endpoint": "Delete Company",
                "message": "Authentication signature calculation is wrong",
                "result": {}
            }
        response = ResponseApi().response_api(result)
        return response
        
