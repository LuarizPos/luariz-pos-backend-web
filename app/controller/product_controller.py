from app.models.product_models import ProductModels, ProductSchema
from app.models.category_models import CategoryModels, CategorySchema
from flask_restful import Resource
from flask import request, jsonify
from app.helpers.helpers import Helpers
from app.helpers.response import ResponseApi
from app.manage import db, app
from PIL import Image
import io
import pdb
import os
 

product_schema = ProductSchema()
products_schema = ProductSchema(many=True)
category_schema = CategorySchema()
categorys_schema = CategorySchema(many=True)
UPLOAD_FOLDER = 'assets/images/'
display = 'assets/images/'

class ProductController(Resource):
    def get_product(self,param):
        if Helpers().cek_auth(param):
            # cek_session = Helpers().cek_session(param)
            # if cek_session['code'] == 200:
                form_req = param['form']
                resultData = []
                if form_req:
                    try:
                        showAll = form_req['ShowAll']
                        id_product = form_req['id_product']
                        if showAll:
                            Product = ProductModels.query.all()
                            data_product = products_schema.dump(Product)
                            for product_value in data_product:
                                id_category = int(product_value['category_id'])
                                Category = CategoryModels.query.filter_by(id=id_category).first()
                                data_category = category_schema.dump(Category)
                                data = {
                                    "image": request.url_root+display+product_value['image'],
                                    "id": product_value['id'],
                                    "price": product_value['price'],
                                    "stock": product_value['stock'],
                                    "description": product_value['description'],
                                    "category_id": product_value['category_id'],
                                    "category_name": data_category['name'],
                                    "name": product_value['name'],
                                }
                                resultData.append(data)
                        else:
                            Product = ProductModels.query.filter_by(id=id_product).first()
                            data_product = product_schema.dump(Product)
                            id_category = int(data_product['category_id'])
                            Category = CategoryModels.query.filter_by(id=id_category).first()
                            data_category = category_schema.dump(Category)
                            data = {
                                "image": request.url_root+display+data_product['image'],
                                "id": data_product['id'],
                                "price": data_product['price'],
                                "stock": data_product['stock'],
                                "description": data_product['description'],
                                "category_id": data_product['category_id'],
                                "category_name": data_category['name'],
                                "name": data_product['name'],
                            }
                            resultData.append(data)
                        

                        result = {
                            "code" : 200,
                            "endpoint": "Get Product",
                            "message": "Get Product Succes",
                            "result": resultData
                        }
                    except Exception as e:
                        error  = str(e)
                        result = {
                            "code" : 400,
                            "endpoint": "Get Product",
                            "message": error,
                            "result": {}
                        }
                else:
                    result = {
                        "code" : 400,
                        "endpoint": "Get Product",
                        "message": "Form Request Is Empty",
                        "result": {}
                    }
            # else:
            #     result = {
            #         "code" : cek_session['code'],
            #         "endpoint": "Get Product",
            #         "message": cek_session['message'],
            #         "result": {}
            #     }
        else:
            result = {
                "code" : 400,
                "endpoint": "Get Product",
                "message": "Authentication signature calculation is wrong",
                "result": {}
            }
        response = ResponseApi().response_api(result)
        return response
    
    def insert_product(self,param):
        if Helpers().cek_auth(param):
            # cek_session = Helpers().cek_session(param)
            # if cek_session['code'] == 200:
                form_req = param['form']
                resultData = []
                if form_req:
                    try:
                        for form_value in form_req:
                            name_product = form_value['name']
                            id_category = form_value['id_category']
                            description = form_value['description']
                            price = form_value['price']
                            stock = form_value['stock']
                            image = ""
                            if form_value['image']:
                                image_encode = form_value['image']['image_blob'] 
                                image_name = form_value['image']['name']
                                image_type = form_value['image']['type']
                                image = image_name+"."+image_type
                                if image_encode != "" and image_name != "" and image_type != "":
                                    image_path = UPLOAD_FOLDER+image_name+'.'+image_type
                                    image_decode = Helpers().decode_image(image_encode)
                                    if image_decode !=0:
                                        image_file = Image.open(io.BytesIO(image_decode))
                                        image_file = image_file.convert('RGB')
                                        image_file.save(image_path)
                                    else:
                                        result = {
                                            "code" : 400,
                                            "endpoint": "Insert Product",
                                            "message": "image_blob is wrong",
                                            "result": {}
                                        }
                                        response = ResponseApi().response_api(result)
                                        return response
                            
                            new_product = ProductModels(id_category, name_product, description, image, stock, price)
                            db.session.add(new_product)
                            db.session.commit()
                            data = {
                                "name" : name_product,
                                "category_id" : id_category,
                                "description" : description,
                                "image" : request.url_root+display+image,
                                "stock" : stock,
                                "price" : price,
                            }
                            
                            resultData.append(data)
                        result = {
                            "code" : 200,
                            "endpoint": "Insert Product",
                            "message": "Insert Product Succes",
                            "result": resultData
                        }
                    except Exception as e:
                        error  = str(e)
                        result = {
                            "code" : 400,
                            "endpoint": "Insert Product",
                            "message": error,
                            "result": {}
                        }
                else:
                    result = {
                        "code" : 400,
                        "endpoint": "Insert Product",
                        "message": "Form Request Is Empty",
                        "result": {}
                    }
            # else:
            #     result = {
            #         "code" : cek_session['code'],
            #         "endpoint": "Insert Product",
            #         "message": cek_session['message'],
            #         "result": {}
            #     }
        else:
            result = {
                "code" : 400,
                "endpoint": "Insert Product",
                "message": "Authentication signature calculation is wrong",
                "result": {}
            }
        
        response = ResponseApi().response_api(result)
        return response
            
    def update_product(self,param):
        if Helpers().cek_auth(param):
            # cek_session = Helpers().cek_session(param)
            # if cek_session['code'] == 200:
                form_req = param['form']
                resultData = []
                if form_req:
                    # try:
                        for form_value in form_req:
                            id_product = form_value['id_product']
                            name_product = form_value['name']
                            id_category = form_value['id_category']
                            description = form_value['description']
                            price = form_value['price']
                            stock = form_value['stock']
                            image = ""
                            if form_value['image']:
                                image_encode = form_value['image']['image_blob'] 
                                image_name = form_value['image']['name']
                                image_type = form_value['image']['type']
                                image = image_name+"."+image_type
                                if image_encode != "" and image_name != "" and image_type != "":
                                    image_path = UPLOAD_FOLDER+image_name+'.'+image_type
                                    image_decode = Helpers().decode_image(image_encode)
                                    if image_decode !=0:
                                        image_file = Image.open(io.BytesIO(image_decode))
                                        image_file = image_file.convert('RGB')
                                        image_file.save(image_path)
                                    else:
                                        result = {
                                            "code" : 400,
                                            "endpoint": "Insert Product",
                                            "message": "image_blob is wrong",
                                            "result": {}
                                        }
                                        response = ResponseApi().response_api(result)
                                        return response
                            
                            Product = ProductModels.query.filter_by(id=id_product)
                            ge_product = ProductModels.query.filter_by(id=id_product).first()
                            data_product = product_schema.dump(ge_product)
                            if image == "":
                                image = data_product["image"]
                            
                            data = {
                                "id" : id_product,
                                "name" : name_product,
                                "category_id" : id_category,
                                "description" : description,
                                "image" : image,
                                "stock" : stock,
                                "price" : price,
                            }
                            Product.update(data)
                            db.session.commit()
                            resultData.append(data)
                        
                        result = {
                            "code" : 200,
                            "endpoint": "Update Product",
                            "message": "Update Product Succes",
                            "result": resultData
                        }
                    # except Exception as e:
                    #     error  = str(e)
                    #     result = {
                    #         "code" : 400,
                    #         "endpoint": "Update Product",
                    #         "message": error,
                    #         "result": {}
                    #     }
                else:
                    result = {
                        "code" : 400,
                        "endpoint": "Update Product",
                        "message": "Form Request Is Empty",
                        "result": {}
                    }
            # else:
            #     result = {
            #         "code" : cek_session['code'],
            #         "endpoint": "Update Product",
            #         "message": cek_session['message'],
            #         "result": {}
            #     }
        else:
            result = {
                "code" : 400,
                "endpoint": "Update Product",
                "message": "Authentication signature calculation is wrong",
                "result": {}
            }
        
        response = ResponseApi().response_api(result)
        return response

    def delete_product(self,param):
        if Helpers().cek_auth(param):
            # cek_session = Helpers().cek_session(param)
            # if cek_session['code'] == 200:
                form_req = param['form']
                resultData = []
                if form_req:
                    try:
                        for form_value in form_req:
                            id_product = form_value['id']
                            product = ProductModels.query.filter_by(id=id_product).first()
                            product_value = product_schema.dump(product)
                            db.session.delete(product)
                            db.session.commit()
                            data = {
                                'id':product_value['id'],
                                "name" : product_value['name'],
                            }
                            resultData.append(data)
                        result = {
                            "code" : 200,
                            "endpoint": "Delete Product",
                            "message": "Delete Product Succes",
                            "result": resultData
                        }
                        
                    except Exception as e:
                        error  = str(e)
                        result = {
                            "code" : 400,
                            "endpoint": "Delete Product",
                            "message": error,
                            "result": {}
                        }
                else:
                    result = {
                        "code" : 400,
                        "endpoint": "Delete Product",
                        "message": "Form Request Is Empty",
                        "result": {}
                    }
            # else:
            #     result = {
            #         "code" : cek_session['code'],
            #         "endpoint": "Update Product",
            #         "message": cek_session['message'],
            #         "result": {}
            #     }
        else:
            result = {
                "code" : 400,
                "endpoint": "Delete Product",
                "message": "Authentication signature calculation is wrong",
                "result": {}
            }
        response = ResponseApi().response_api(result)
        return response