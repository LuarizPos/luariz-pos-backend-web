from app.models.company_models import CompanyModels, CompanySchema
from flask_restful import Resource
from flask import request, jsonify
from app.helpers.helpers import Helpers
from app.helpers.response import ResponseApi
from app.manage import db
import pdb
import io

company_schema = CompanySchema()
companys_schema = CompanySchema(many=True)

class ComponyController(Resource):
    def get_company(self,param):
        start_time = ResponseApi().microtime(True)
        if Helpers().cek_auth(param):
            cek_session = Helpers().cek_session(param)
            if cek_session['code'] == 200:
                form_req = param['form']
                if form_req:
                    try:
                        show_all = form_req['show_all']
                        id_company = form_req['id_company']
                        if show_all:
                            Company = CompanyModels.query.all()
                            data = companys_schema.dump(Company)
                        else:
                            Company = CompanyModels.query.filter_by(id=id_company).first()
                            data = company_schema.dump(Company)
                        
                        result = ResponseApi().error_response(200, "Get Company", "Get Company Succes", start_time, data)
                    except Exception as e:
                        error  = str(e)
                        result = ResponseApi().error_response(400, "Get Company", error, start_time)
                else:
                    result = ResponseApi().error_response(400, "Get Company", "Form Request Is Empty", start_time)
            else:
                result = ResponseApi().error_response(cek_session['code'], "Get Company", cek_session['message'], start_time)
        else:
            result = ResponseApi().error_response(400, "Get Company", "Authentication signature calculation is wrong", start_time)
        response = ResponseApi().response_api(result)
        return response
        
    def insert_company(self,param):
        start_time = ResponseApi().microtime(True)
        if Helpers().cek_auth(param):
            cek_session = Helpers().cek_session(param)
            if cek_session['code'] == 200:
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
                        result = ResponseApi().error_response(200, "Insert Company", "Insert Company Succes", start_time, resultData)
                        # print(result)
                        # pdb.run('mymodule.test()')
                    except Exception as e:
                        error  = str(e)
                        result = ResponseApi().error_response(400, "Insert Company", error, start_time)
                else:
                    result = ResponseApi().error_response(400, "Insert Company", "Form Request Is Empty", start_time)
            else:
                result = ResponseApi().error_response(cek_session['code'], "Insert Company", cek_session['message'], start_time)
        else:
            result = ResponseApi().error_response(400, "Insert Company", "Authentication signature calculation is wrong", start_time)
        response = ResponseApi().response_api(result)
        return response

    def update_company(self,param):
        start_time = ResponseApi().microtime(True)
        if Helpers().cek_auth(param):
            cek_session = Helpers().cek_session(param)
            if cek_session['code'] == 200:
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
                        
                        result = ResponseApi().error_response(200, "Update Company", "Update Company Succes", start_time, resultData)
                        # print(result)
                        # pdb.run('mymodule.test()')
                    except Exception as e:
                        error  = str(e)
                        result = ResponseApi().error_response(400, "Update Company", error, start_time)
                else:
                    result = ResponseApi().error_response(400, "Update Company", "Form Request Is Empty", start_time)
            else:
                result = ResponseApi().error_response(cek_session['code'], "Update Company", cek_session['message'], start_time)
        else:
            result = ResponseApi().error_response(400, "Update Company", "Authentication signature calculation is wrong", start_time)
        response = ResponseApi().response_api(result)
        return response

    def delete_company(self,param):
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
                                Company = CompanyModels.query.order_by(CompanyModels.id.asc())
                                data_company = companys_schema.dump(Company)
                                for Company_value in data_company:
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
                                CompanyModels.query.delete()
                                db.session.commit()
                            else:
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

                        result = ResponseApi().error_response(200, "Delete Company", "Delete Company Succes", start_time, resultData)
                    except Exception as e:
                        error  = str(e)
                        result = ResponseApi().error_response(400, "Delete Company", error, start_time)
                else:
                    result = ResponseApi().error_response(400, "Delete Company", "Form Request Is Empty", start_time)
            else:
                result = ResponseApi().error_response(cek_session['code'], "Delete Company", cek_session['message'], start_time)
        else:
            result = ResponseApi().error_response(400, "Delete Company", "Authentication signature calculation is wrong", start_time)
        response = ResponseApi().response_api(result)
        return response
        
