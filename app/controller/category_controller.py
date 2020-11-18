from app.models.category_models import CategoryModels, CategorySchema
from flask_restful import Resource
from flask import request, jsonify
from app.helpers.helpers import Helpers
from app.helpers.response import ResponseApi
from app.manage import db
from PIL import Image
import io


category_schema = CategorySchema()
categorys_schema = CategorySchema(many=True)

class CategoryController(Resource):
    def get_category(self,param):
        if Helpers().cek_auth(param):
            # cek_session = Helpers().cek_session(param)
            # if cek_session['code'] == 200:
                form_req = param['form']
                if form_req:
                    try:
                        showAll = form_req['ShowAll']
                        id_category = form_req['id_category']
                        if showAll:
                            Category = CategoryModels.query.all()
                            data = categorys_schema.dump(Category)
                            
                        else:
                            Category = CategoryModels.query.filter_by(id=id_category).first()
                            data = category_schema.dump(Category)
                        
                        result = {
                            "code" : 200,
                            "endpoint": "Get Category",
                            "message": "Get Category Succes",
                            "result": data
                        }
                    except Exception as e:
                        error  = str(e)
                        result = {
                            "code" : 400,
                            "endpoint": "Get Category",
                            "message": error,
                            "result": {}
                        }
                else:
                    result = {
                        "code" : 400,
                        "endpoint": "Get Category",
                        "message": "Form Request Is Empty",
                        "result": {}
                    }
            # else:
            #     result = {
            #         "code" : cek_session['code'],
            #         "endpoint": "Get Category",
            #         "message": cek_session['message'],
            #         "result": {}
            #     }
        else:
            result = {
                "code" : 400,
                "endpoint": "Get Category",
                "message": "Authentication signature calculation is wrong",
                "result": {}
            }
        response = ResponseApi().response_api(result)
        return response
    
    def insert_category(self,param):
        if Helpers().cek_auth(param):
            # cek_session = Helpers().cek_session(param)
            # if cek_session['code'] == 200:
                form_req = param['form']
                if form_req:
                    try:
                        resultData = []
                        for form_value in form_req:
                            name_category = form_value['name']
                            new_category = CategoryModels(name_category)
                            db.session.add(new_category)
                            db.session.commit()
                            data = {
                                "name" : name_category,
                            }
                            resultData.append(data)
                        result = {
                            "code" : 200,
                            "endpoint": "Insert Category",
                            "message": "Insert Category Succes",
                            "result": resultData
                        }
                    except Exception as e:
                        error  = str(e)
                        result = {
                            "code" : 400,
                            "endpoint": "Insert Category",
                            "message": error,
                            "result": {}
                        }
                else:
                    result = {
                        "code" : 400,
                        "endpoint": "Insert Category",
                        "message": "Form Request Is Empty",
                        "result": {}
                    }
            # else:
            #     result = {
            #         "code" : cek_session['code'],
            #         "endpoint": "Insert Category",
            #         "message": cek_session['message'],
            #         "result": {}
            #     }
        else:
            result = {
                "code" : 400,
                "endpoint": "Insert Category",
                "message": "Authentication signature calculation is wrong",
                "result": {}
            }
        
        response = ResponseApi().response_api(result)
        return response
            
    def update_category(self,param):
        if Helpers().cek_auth(param):
            # cek_session = Helpers().cek_session(param)
            # if cek_session['code'] == 200:
                form_req = param['form']
                if form_req:
                    try:
                        resultData = []
                        for form_value in form_req:
                            id_category = form_value['id_category']
                            name_category = form_value['name']
                            data = {
                                "id" : id_category,
                                "name" : name_category,
                            }
                            Category = CategoryModels.query.filter_by(id=id_category)
                            Category.update(data)
                            db.session.commit()
                            resultData.append(data)
                        
                        result = {
                            "code" : 200,
                            "endpoint": "Update Category",
                            "message": "Update Category Succes",
                            "result": resultData
                        }
                    except Exception as e:
                        error  = str(e)
                        result = {
                            "code" : 400,
                            "endpoint": "Update Category",
                            "message": error,
                            "result": {}
                        }
                else:
                    result = {
                        "code" : 400,
                        "endpoint": "Update Category",
                        "message": "Form Request Is Empty",
                        "result": {}
                    }
            # else:
            #     result = {
            #         "code" : cek_session['code'],
            #         "endpoint": "Update Category",
            #         "message": cek_session['message'],
            #         "result": {}
            #     }
        else:
            result = {
                "code" : 400,
                "endpoint": "Update Category",
                "message": "Authentication signature calculation is wrong",
                "result": {}
            }
        
        response = ResponseApi().response_api(result)
        return response
    
    def delete_category(self,param):
        if Helpers().cek_auth(param):
            # cek_session = Helpers().cek_session(param)
            # if cek_session['code'] == 200:
                form_req = param['form']
                if form_req:
                    try:
                        resultData = []
                        for form_value in form_req:
                            id_category = form_value['id']
                            category = CategoryModels.query.filter_by(id=id_category).first()
                            category_value = category_schema.dump(category)
                            db.session.delete(category)
                            db.session.commit()
                            data = {
                                'id':category_value['id'],
                                "name" : category_value['name'],
                            }
                            resultData.append(data)
                        result = {
                            "code" : 200,
                            "endpoint": "Delete Category",
                            "message": "Delete Category Succes",
                            "result": resultData
                        }
                        
                    except Exception as e:
                        error  = str(e)
                        result = {
                            "code" : 400,
                            "endpoint": "Delete Category",
                            "message": error,
                            "result": {}
                        }
                else:
                    result = {
                        "code" : 400,
                        "endpoint": "Delete Category",
                        "message": "Form Request Is Empty",
                        "result": {}
                    }
            # else:
            #     result = {
            #         "code" : cek_session['code'],
            #         "endpoint": "Update Category",
            #         "message": cek_session['message'],
            #         "result": {}
            #     }
        else:
            result = {
                "code" : 400,
                "endpoint": "Delete Category",
                "message": "Authentication signature calculation is wrong",
                "result": {}
            }
        response = ResponseApi().response_api(result)
        return response