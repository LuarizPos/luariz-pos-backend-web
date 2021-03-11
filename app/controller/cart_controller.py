from app.models.cart_models import CartModels, CartSchema
from flask_restful import Resource
from app.helpers.helpers import Helpers
from app.helpers.response import ResponseApi
from app.manage import db
import pdb

cart_schema = CartSchema()
carts_schema = CartSchema(many=True)

class CartController(Resource):

    def get_cart(self,param):
        start_time = ResponseApi().microtime(True)
        if Helpers().cek_auth(param):
            cek_session = Helpers().cek_session(param)
            if cek_session['code'] == 200:
                form_req = param['form']
                if form_req:
                    try:
                        show_all = form_req['show_all']
                        id_cart = form_req['id_cart']
                        if show_all:
                            Cart = CartModels.query.all()
                            data = carts_schema.dump(Cart)
                        else:
                            Cart = CartModels.query.filter_by(id=id_cart).first()
                            data = carts_schema.dump(Cart)
                        
                        result = ResponseApi().error_response(200, "Delete Cart", "Get Cart Succes", start_time, data)
                    except Exception as e:
                        error  = str(e)
                        result = ResponseApi().error_response(400, "Get Cart", error, start_time)
                else:
                    result = ResponseApi().error_response(400, "Get Cart", "Form Request Is Empty", start_time)
            else:
                result = ResponseApi().error_response(cek_session['code'], "Get Cart", cek_session['message'], start_time)
        else:
            result = ResponseApi().error_response(400, "Get Cart", "Authentication signature calculation is wrong", start_time)
        response = ResponseApi().response_api(result)
        return response

    def insert_cart(self,param):
        start_time = ResponseApi().microtime(True)
        if Helpers().cek_auth(param):
            cek_session = Helpers().cek_session(param)
            if cek_session['code'] == 200:
                form_req = param['form']
                resultData = []
                if form_req:
                    try: 
                        for form_value in form_req:
                            id_transaction = form_value['id_transaction']
                            id_product = form_value['id_product']
                            qty = form_value['qty']
                            price = form_value['price']
                            new_cart = CartModels(id_transaction, id_product, qty, price)
                            db.session.add(new_cart)
                            db.session.commit()
                            data = {
                                "id_transaction" : id_transaction,
                                "id_product" : id_product,
                                "qty" : qty,
                                "price" : price,
                            }    
                            resultData.append(data)
                        result = ResponseApi().error_response(200, "Insert Cart", "Insert Cart Succes", start_time, resultData)
                        # print(result)
                        # pdb.run('mymodule.test()')
                    except Exception as e:
                        error  = str(e)
                        result = ResponseApi().error_response(400, "Insert Cart", error, start_time)
                else:
                    result = ResponseApi().error_response(400, "Insert Cart", "Form Request Is Empty", start_time)
            else:
                result = ResponseApi().error_response(cek_session['code'], "Insert Cart", cek_session['message'], start_time)
        else:
            result = ResponseApi().error_response(400, "Insert Cart", "Authentication signature calculation is wrong", start_time)
        response = ResponseApi().response_api(result)
        return response

    def update_cart(self,param):
        start_time = ResponseApi().microtime(True)
        if Helpers().cek_auth(param):
            cek_session = Helpers().cek_session(param)
            if cek_session['code'] == 200:
                form_req = param['form']
                resultData = []
                if form_req:
                    try:
                        for form_value in form_req:
                            id_cart = form_value['id_cart']
                            id_transaction = form_value['id_transaction']
                            id_product = form_value['id_product']
                            qty = form_value['qty']
                            price = form_value['price']
                            data = {
                                "id_transaction" : id_transaction,
                                "id_product" : id_product,
                                "qty" : qty,
                                "price" : price,
                            }
                            Cart = CartModels.query.filter_by(id=id_cart)
                            Cart.update(data)
                            db.session.commit()
                            resultData.append(data)
                        result = {
                            "code" : 200,
                            "SpeedTime" : ResponseApi().speed_response(start_time),
                            "endpoint": "Update Cart",
                            "message": "Update Cart Succes",
                            "result": resultData
                        }
                        result = ResponseApi().error_response(200, "Update Cart", "Cart Update Succes", start_time, resultData)
                        # print(result)
                        # pdb.run('mymodule.test()')
                    except Exception as e:
                        error  = str(e)
                        result = ResponseApi().error_response(400, "Update Cart", error, start_time)
                else:
                    result = ResponseApi().error_response(400, "Update Cart", "Form Request Is Empty", start_time)
            else:
                result = ResponseApi().error_response(cek_session['code'], "Update Cart", cek_session['message'], start_time)
        else:
            result = ResponseApi().error_response(400, "Update Cart", "Authentication signature calculation is wrong", start_time)
        response = ResponseApi().response_api(result)
        return response
        
    def delete_cart(self,param):
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
                                Cart = CartModels.query.order_by(CartModels.id.asc())
                                data_cart = carts_schema.dump(Cart)
                                for cart_value in data_cart:
                                    data = {
                                        'id_cart':cart_value['id_cart'],
                                        "id_transaction" : cart_value['id_transaction'],
                                        "id_product" : cart_value['id_product'],
                                        "qty" : cart_value['qty'],
                                        "price" : cart_value['price'],
                                    }
                                    resultData.append(data)
                                CartModels.query.delete()
                                db.session.commit()
                            else:
                                id_cart = form_value['id_cart']
                                Cart = CartModels.query.filter_by(id=id_cart).first()
                                Cart_value = cart_schema.dump(Cart)
                                db.session.delete(Cart)
                                db.session.commit()
                                data = {
                                    'id_cart':Cart_value['id_cart'],
                                    "id_transaction" : Cart_value['id_transaction'],
                                    "id_product" : Cart_value['id_product'],
                                    "qty" : Cart_value['qty'],
                                    "price" : Cart_value['price'],
                                }
                                resultData.append(data)
                        
                        result = ResponseApi().error_response(200, "Delete Cart", "Cart Delete Succes", start_time, resultData)
                    except Exception as e:
                        error  = str(e)
                        result = ResponseApi().error_response(400, "Delete Cart", error, start_time)
                else:
                    result = ResponseApi().error_response(400, "Delete Cart", "Form Request Is Empty", start_time)
            else:
                result = ResponseApi().error_response(cek_session['code'], "Delete Cart", cek_session['message'], start_time)
        else:
            result = ResponseApi().error_response(400, "Delete Cart", "Authentication signature calculation is wrong", start_time)
        response = ResponseApi().response_api(result)
        return response