from app.models.product_models import ProductModels, ProductSchema
from app.models.category_models import CategoryModels, CategorySchema
from flask_restful import Resource
from flask import request, jsonify
from app.helpers.helpers import Helpers
from app.helpers.response import ResponseApi
from app.manage import db, app
from cloudinary.uploader import upload
import cloudinary.api


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
                            Product = ProductModels.query.order_by(ProductModels.id.asc())
                            data_product = products_schema.dump(Product)
                            # print(data_product)
                            # pdb.run('mymodule.test()')
                            for product_value in data_product:
                                if(product_value):
                                    id_category = (product_value['id_category'])
                                    Category = CategoryModels.query.filter_by(id=id_category).first()
                                    data_category = category_schema.dump(Category)
                                    get_image_cloudinary = cloudinary.api.resources_by_ids([product_value['id_cloudinary']])
                                    data = {
                                        "id": product_value['id'],
                                        "price": product_value['price'],
                                        "stock": product_value['stock'],
                                        "description": product_value['description'],
                                        "id_category": product_value['id_category'],
                                        "category_name": data_category.get('name'),
                                        "image": get_image_cloudinary['resources'][0]['secure_url'],
                                        "name": product_value['name'],
                                    }
                                    resultData.append(data)
                        else:
                            Product = ProductModels.query.filter_by(id=id_product).first()
                            data_product = product_schema.dump(Product)
                            # print(data_product)
                            # pdb.run('mymodule.test()')
                            if(data_product):
                                id_category = int(data_product['id_category'])
                                Category = CategoryModels.query.filter_by(id=id_category).first()
                                data_category = category_schema.dump(Category)
                                get_image_cloudinary = cloudinary.api.resources_by_ids([data_product['id_cloudinary']])
                                data = {
                                    "id": data_product['id'],
                                    "price": data_product['price'],
                                    "stock": data_product['stock'],
                                    "description": data_product['description'],
                                    "id_category": data_product['id_category'],
                                    "category_name": data_category.get('name'),
                                    "image": get_image_cloudinary['resources'][0]['secure_url'],
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
                        # error  = str(e)
                        result = {
                            "code" : 400,
                            "endpoint": "Get Product",
                            "message": "Failed Get Data",
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
                                        upload_cloudinary = upload(image_path, 
                                            folder = "assets/images/", 
                                            public_id = image_name+'.'+image_type)
                                        # print(upload_cloudinary['public_id'])
                                        # pdb.run('mymodule.test()')
                                    else:
                                        result = {
                                            "code" : 400,
                                            "endpoint": "Insert Product",
                                            "message": "image_blob is wrong",
                                            "result": {}
                                        }
                                        response = ResponseApi().response_api(result)
                                        return response
                            
                            new_product = ProductModels(id_category, name_product, description, image, upload_cloudinary['public_id'], stock, price)
                            db.session.add(new_product)
                            db.session.commit()
                            Product = ProductModels.query.filter_by(name=name_product).first()
                            data_product = product_schema.dump(Product)
                            get_image_cloudinary = cloudinary.api.resources_by_ids([data_product['id_cloudinary']])
                            data = {
                                "id": data_product['id'],
                                "name" : data_product['name'],
                                "id_category" : data_product['id_category'],
                                "description" : data_product['description'],
                                "image" : get_image_cloudinary['resources'][0]['secure_url'],
                                "stock" : data_product['stock'],
                                "price" : data_product['price'],
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
                                "id_category" : id_category,
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
                            id_product = form_value['id_product']
                            product = ProductModels.query.filter_by(id=id_product).first()
                            product_value = product_schema.dump(product)
                            db.session.delete(product)
                            db.session.commit()
                            data = {
                                'id_product':product_value['id'],
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