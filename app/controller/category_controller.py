from app.models.category_models import CategoryModels, CategorySchema
from app.models.product_models import ProductModels, ProductSchema
from flask_restful import Resource
from flask import request, jsonify
from app.helpers.helpers import Helpers
from app.helpers.response import ResponseApi
from app.manage import db
import pdb
import io


category_schema = CategorySchema()
categorys_schema = CategorySchema(many=True)
product_schema = ProductSchema()
products_schema = ProductSchema(many=True)

class CategoryController(Resource):
    def get_category(self,param):
        start_time = ResponseApi().microtime(True)
        if Helpers().cek_auth(param):
            cek_session = Helpers().cek_session(param)
            if cek_session['code'] == 200:
                form_req = param['form']
                resultData = []
                if form_req:
                    try:
                        show_all = form_req['show_all']
                        id_category = form_req['id_category']
                        if show_all:
                            Category = CategoryModels.query.all()
                            data_category = categorys_schema.dump(Category)
                            for category_value in data_category:
                                id_category = int(category_value['id'])
                                total_product = ProductModels.query.filter_by(id_category=id_category).count()
                                data = {
                                    "id_category": category_value['id'],
                                    "name": category_value['name'],
                                    'total_product':total_product
                                }
                                resultData.append(data)
                        else:
                            Category = CategoryModels.query.filter_by(id=id_category).first()
                            data_category = category_schema.dump(Category)
                            id_category = int(data_category['id'])
                            total_product = ProductModels.query.filter_by(id_category=id_category).count()
                            data = {
                                "id_category": data_category['id'],
                                "name": data_category['name'],
                                'total_product':total_product
                            }
                            resultData.append(data)
                        
                        result = {
                            "code" : 200,
                            "SpeedTime" : ResponseApi().speed_response(start_time),
                            "endpoint": "Get Category",
                            "message": "Get Category Succes",
                            "result": resultData
                        }
                    except Exception as e:
                        # error  = str(e)
                        result = {
                            "code" : 400,
                            "SpeedTime" : ResponseApi().speed_response(start_time),
                            "endpoint": "Get Category",
                            "message": "Failed Get Data",
                            "result": {}
                        }
                else:
                    result = {
                        "code" : 400,
                        "SpeedTime" : ResponseApi().speed_response(start_time),
                        "endpoint": "Get Category",
                        "message": "Form Request Is Empty",
                        "result": {}
                    }
            else:
                result = {
                    "code" : cek_session['code'],
                    "SpeedTime" : ResponseApi().speed_response(start_time),
                    "endpoint": "Get Category",
                    "message": cek_session['message'],
                    "result": {}
                }
        else:
            result = {
                "code" : 400,
                "SpeedTime" : ResponseApi().speed_response(start_time),
                "endpoint": "Get Category",
                "message": "Authentication signature calculation is wrong",
                "result": {}
            }
        response = ResponseApi().response_api(result)
        return response
    
    def insert_category(self,param):
        start_time = ResponseApi().microtime(True)
        if Helpers().cek_auth(param):
            cek_session = Helpers().cek_session(param)
            if cek_session['code'] == 200:
                form_req = param['form']
                resultData = []
                if form_req:
                    try:
                        for form_value in form_req:
                            name_category = form_value['name']
                            new_category = CategoryModels(name_category)
                            db.session.add(new_category)
                            db.session.commit()
                            Category = CategoryModels.query.filter_by(name=name_category).first()
                            data_category = category_schema.dump(Category)
                            data = {
                                "id_category" : data_category['id'],
                                "name" : name_category,
                            }
                            resultData.append(data)
                        
                        result = {
                            "code" : 200,
                            "SpeedTime" : ResponseApi().speed_response(start_time),
                            "endpoint": "Insert Category",
                            "message": "Insert Category Succes",
                            "result": resultData
                        }
                    except Exception as e:
                        error  = str(e)
                        result = {
                            "code" : 400,
                            "SpeedTime" : ResponseApi().speed_response(start_time),
                            "endpoint": "Insert Category",
                            "message": error,
                            "result": {}
                        }
                else:
                    result = {
                        "code" : 400,
                        "SpeedTime" : ResponseApi().speed_response(start_time),
                        "endpoint": "Insert Category",
                        "message": "Form Request Is Empty",
                        "result": {}
                    }
            else:
                result = {
                    "code" : cek_session['code'],
                    "SpeedTime" : ResponseApi().speed_response(start_time),
                    "endpoint": "Insert Category",
                    "message": cek_session['message'],
                    "result": {}
                }
        else:
            result = {
                "code" : 400,
                "SpeedTime" : ResponseApi().speed_response(start_time),
                "endpoint": "Insert Category",
                "message": "Authentication signature calculation is wrong",
                "result": {}
            }
        
        response = ResponseApi().response_api(result)
        return response
            
    def update_category(self,param):
        start_time = ResponseApi().microtime(True)
        if Helpers().cek_auth(param):
            cek_session = Helpers().cek_session(param)
            if cek_session['code'] == 200:
                form_req = param['form']
                resultData = []
                if form_req:
                    try:
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
                            "SpeedTime" : ResponseApi().speed_response(start_time),
                            "endpoint": "Update Category",
                            "message": "Update Category Succes",
                            "result": resultData
                        }
                    except Exception as e:
                        error  = str(e)
                        result = {
                            "code" : 400,
                            "SpeedTime" : ResponseApi().speed_response(start_time),
                            "endpoint": "Update Category",
                            "message": error,
                            "result": {}
                        }
                else:
                    result = {
                        "code" : 400,
                        "SpeedTime" : ResponseApi().speed_response(start_time),
                        "endpoint": "Update Category",
                        "message": "Form Request Is Empty",
                        "result": {}
                    }
            else:
                result = {
                    "code" : cek_session['code'],
                    "SpeedTime" : ResponseApi().speed_response(start_time),
                    "endpoint": "Update Category",
                    "message": cek_session['message'],
                    "result": {}
                }
        else:
            result = {
                "code" : 400,
                "SpeedTime" : ResponseApi().speed_response(start_time),
                "endpoint": "Update Category",
                "message": "Authentication signature calculation is wrong",
                "result": {}
            }
        
        response = ResponseApi().response_api(result)
        return response
    
    def delete_category(self,param):
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
                                category = CategoryModels.query.order_by(CategoryModels.id.asc())
                                data_category = categorys_schema.dump(category)
                                for category_value in data_category:
                                    data = {
                                        'id_category':category_value['id'],
                                        "name" : category_value['name'],
                                    }
                                    resultData.append(data)
                                CategoryModels.query.delete()
                                db.session.commit()
                            else:
                                id_category = form_value['id_category']
                                category = CategoryModels.query.filter_by(id=id_category).first()
                                category_value = category_schema.dump(category)
                                db.session.delete(category)
                                db.session.commit()
                                data = {
                                    'id_category':category_value['id'],
                                    "name" : category_value['name'],
                                }
                                resultData.append(data)
                        result = {
                            "code" : 200,
                            "SpeedTime" : ResponseApi().speed_response(start_time),
                            "endpoint": "Delete Category",
                            "message": "Delete Category Succes",
                            "result": resultData
                        }
                        
                    except Exception as e:
                        error  = str(e)
                        result = {
                            "code" : 400,
                            "SpeedTime" : ResponseApi().speed_response(start_time),
                            "endpoint": "Delete Category",
                            "message": error,
                            "result": {}
                        }
                else:
                    result = {
                        "code" : 400,
                        "SpeedTime" : ResponseApi().speed_response(start_time),
                        "endpoint": "Delete Category",
                        "message": "Form Request Is Empty",
                        "result": {}
                    }
            else:
                result = {
                    "code" : cek_session['code'],
                    "SpeedTime" : ResponseApi().speed_response(start_time),
                    "endpoint": "Update Category",
                    "message": cek_session['message'],
                    "result": {}
                }
        else:
            result = {
                "code" : 400,
                "SpeedTime" : ResponseApi().speed_response(start_time),
                "endpoint": "Delete Category",
                "message": "Authentication signature calculation is wrong",
                "result": {}
            }
        response = ResponseApi().response_api(result)
        return response