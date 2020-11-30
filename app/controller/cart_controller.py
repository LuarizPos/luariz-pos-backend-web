from app.models.cart_models import CartModels, CartSchema
from flask_restful import Resource
from flask import request, jsonify
from app.helpers.helpers import Helpers
from app.helpers.response import ResponseApi
from app.manage import db
import pdb

cart_schema = CartSchema()
carts_schema = CartSchema(many=True)

class CartController(Resource):

    def get_Cart(self,param):
        if Helpers().cek_auth(param):
            # cek_session = Helpers().cek_session(param)
            # if cek_session['code'] == 200:
                form_req = param['form']
                if form_req:
                    try:
                        showAll = form_req['ShowAll']
                        id_cart = form_req['id_cart']
                        if showAll:
                            Cart = CartModels.query.all()
                            data = carts_schema.dump(Cart)
                        else:
                            Cart = CartModels.query.filter_by(id=id_cart).first()
                            data = carts_schema.dump(Cart)
                        
                        result = {
                            "code" : 200,
                            "endpoint": "Get Cart",
                            "message": "Get Cart Succes",
                            "result": data
                        }
                    except Exception as e:
                        error  = str(e)
                        result = {
                            "code" : 400,
                            "endpoint": "Get Cart",
                            "message": error,
                            "result": {}
                        }
                else:
                    result = {
                        "code" : 400,
                        "endpoint": "Get Cart",
                        "message": "Form Request Is Empty",
                        "result": {}
                    }
            # else:
            #     result = {
            #         "code" : cek_session['code'],
            #         "endpoint": "Get Cart",
            #         "message": cek_session['message'],
            #         "result": {}
            #     }
        else:
            result = {
                "code" : 400,
                "endpoint": "Get Cart",
                "message": "Authentication signature calculation is wrong",
                "result": {}
            }
        response = ResponseApi().response_api(result)
        return response

    def insert_cart(self,param):
        if Helpers().cek_auth(param):
            # cek_session = Helpers().cek_session(param)
            # if cek_session['code'] == 200:
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
                        result = {
                            "code" : 200,
                            "endpoint": "Insert Cart",
                            "message": "Insert Cart Succes",
                            "result": resultData
                        }    
                        # print(result)
                        # pdb.run('mymodule.test()')
                    except Exception as e:
                        error  = str(e)
                        result = {
                            "code" : 400,
                            "endpoint": "Insert Cart",
                            "message": error,
                            "result": {}
                        }
                else:
                    result = {
                        "code" : 400,
                        "endpoint": "Insert Cart",
                        "message": "Form Request Is Empty",
                        "result": {}
                    }
            # else:
            #     result = {
            #         "code" : cek_session['code'],
            #         "endpoint": "Insert Cart",
            #         "message": cek_session['message'],
            #         "result": {}
            #     }
        else:
            result = {
                "code" : 400,
                "endpoint": "Insert Cart",
                "message": "Authentication signature calculation is wrong",
                "result": {}
            }

        response = ResponseApi().response_api(result)
        return response

    def update_cart(self,param):
        if Helpers().cek_auth(param):
            # cek_session = Helpers().cek_session(param)
            # if cek_session['code'] == 200:
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
                            "endpoint": "Update Cart",
                            "message": "Update Cart Succes",
                            "result": resultData
                        }
                        # print(result)
                        # pdb.run('mymodule.test()')
                    except Exception as e:
                        error  = str(e)
                        result = {
                            "code" : 400,
                            "endpoint": "Update Cart",
                            "message": error,
                            "result": {}
                        }
                else:
                    result = {
                        "code" : 400,
                        "endpoint": "Update Cart",
                        "message": "Form Request Is Empty",
                        "result": {}
                    }
            # else:
            #     result = {
            #         "code" : cek_session['code'],
            #         "endpoint": "Update Cart",
            #         "message": cek_session['message'],
            #         "result": {}
            #     }
        else:
            result = {
                "code" : 400,
                "endpoint": "Update Cart",
                "message": "Authentication signature calculation is wrong",
                "result": {}
            }    
        response = ResponseApi().response_api(result)
        return response
        

    def delete_cart(self,param):
        if Helpers().cek_auth(param):
            # cek_session = Helpers().cek_session(param)
            # if cek_session['code'] == 200:
                form_req = param['form']
                resultData = []
                if form_req:
                    try:
                        for form_value in form_req:
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
                        result = {
                            "code" : 200,
                            "endpoint": "Delete Cart",
                            "message": "Delete Cart Succes",
                            "result": resultData
                        }
                    except Exception as e:
                        error  = str(e)
                        result = {
                            "code" : 400,
                            "endpoint": "Delete Cart",
                            "message": error,
                            "result": {}
                        }
                else:
                    result = {
                        "code" : 400,
                        "endpoint": "Delete Cart",
                        "message": "Form Request Is Empty",
                        "result": {}
                    }
            # else:
            #     result = {
            #         "code" : cek_session['code'],
            #         "endpoint": "Update Cart",
            #         "message": cek_session['message'],
            #         "result": {}
            #     }
        else:
            result = {
                "code" : 400,
                "endpoint": "Delete Cart",
                "message": "Authentication signature calculation is wrong",
                "result": {}
            }
        response = ResponseApi().response_api(result)
        return response