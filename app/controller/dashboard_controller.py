from app.models.category_models import CategoryModels, CategorySchema
from app.models.product_models import ProductModels, ProductSchema
from flask_restful import Resource
from app.helpers.helpers import Helpers
from app.helpers.response import ResponseApi
from app.manage import db
from datetime import datetime
import pdb

category_schema = CategorySchema()
categorys_schema = CategorySchema(many=True)
product_schema = ProductSchema()
products_schema = ProductSchema(many=True)
class DashboardController(Resource):
    def get_dashboard(self,param):
        start_time = ResponseApi().microtime(True)
        if Helpers().cek_auth(param):
            # cek_session = Helpers().cek_session(param)
            # if cek_session['code'] == 200:
                try:
                    total_category = CategoryModels.query.count()
                    total_product = ProductModels.query.count()
                    product_data = {
                        'total_product' :total_product
                    }
                    category_data ={
                        'total_category' :total_category
                    }
                    # print(xample)
                    # pdb.run('mymodule.test()')
                    data = {
                        'Product':product_data,
                        'Category':category_data
                    }
                    result = {
                        "code" : 200,
                        "SpeedTime" : ResponseApi().speed_response(start_time),
                        "endpoint": "Get Dashboard",
                        "message": "Get Dashboard Succes",
                        "result": data
                    }
                except Exception as e:
                    # error  = str(e)
                    result = {
                        "code" : 400,
                        "SpeedTime" : ResponseApi().speed_response(start_time),
                        "endpoint": "Get Dashboard",
                        "message": "Failed Get Data",
                        "result": {}
                    }
            
            # else:
            #     result = {
            #         "code" : cek_session['code'],
            #         "SpeedTime" : start_time,
            #         "endpoint": "Get Category",
            #         "message": cek_session['message'],
            #         "result": {}
            #     }
        else:
            result = {
                "code" : 400,
                "SpeedTime" : ResponseApi().speed_response(start_time),
                "endpoint": "Get Dashboard",
                "message": "Authentication signature calculation is wrong",
                "result": {}
            }
        response = ResponseApi().response_api(result)
        return response