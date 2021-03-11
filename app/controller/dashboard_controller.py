from app.models.category_models import CategoryModels, CategorySchema
from app.models.product_models import ProductModels, ProductSchema
from flask_restful import Resource
from app.helpers.helpers import Helpers
from app.helpers.response import ResponseApi
import pdb

category_schema = CategorySchema()
categorys_schema = CategorySchema(many=True)
product_schema = ProductSchema()
products_schema = ProductSchema(many=True)
class DashboardController(Resource):
    def get_dashboard(self,param):
        start_time = ResponseApi().microtime(True)
        if Helpers().cek_auth(param):
            cek_session = Helpers().cek_session(param)
            if cek_session['code'] == 200:
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
                    
                    result = ResponseApi().error_response(200, "Get Dashboard", "Get Dashboard Succes", start_time, data)
                except Exception as e:
                    error  = str(e)
                    result = ResponseApi().error_response(400, "Get Dashboard", error, start_time)
            else:
                result = ResponseApi().error_response(cek_session['code'], "Get Dashboard", cek_session['message'], start_time)
        else:
            result = ResponseApi().error_response(400, "Get Dashboard", "Authentication signature calculation is wrong", start_time)
        response = ResponseApi().response_api(result)
        return response