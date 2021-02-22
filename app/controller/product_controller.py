from app.models.product_models import ProductModels, ProductSchema
from app.models.category_models import CategoryModels, CategorySchema
from flask_restful import Resource
from flask import request, jsonify
from app.helpers.helpers import Helpers
from app.helpers.response import ResponseApi
from app.manage import db, UseCloundiary, UseImagekit, imagekit
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
        start_time = ResponseApi().microtime(True)
        if Helpers().cek_auth(param):
            cek_session = Helpers().cek_session(param)
            if cek_session['code'] == 200:
                form_req = param['form']
                resultData = []
                if form_req:
                    try:
                        image = ''
                        show_all = form_req['show_all']
                        id_product = form_req['id_product']
                        if show_all:
                            Product = ProductModels.query.order_by(ProductModels.id.asc())
                            data_product = products_schema.dump(Product)
                            for product_value in data_product:
                                if(product_value):
                                    id_category = (product_value['id_category'])
                                    Category = CategoryModels.query.filter_by(id=id_category).first()
                                    data_category = category_schema.dump(Category)
                                    if bool(UseCloundiary) is True:
                                        # print(UseCloundiary)
                                        # pdb.run('mymodule.test()')
                                        get_image_cloudinary = cloudinary.api.resources_by_ids([product_value['id_cloudinary']])
                                        image = get_image_cloudinary['resources'][0]['secure_url']
                                    if bool(UseImagekit) is True:
                                        get_imagekit = imagekit.get_file_details(product_value['id_imagekit']) 
                                        # print(get_imagekit)
                                        # pdb.run('mymodule.test()')
                                        image = get_imagekit['response']['url']
                                    if bool(UseImagekit) is False and bool(UseCloundiary) is False:
                                        image = request.url_root+display+product_value['image']
                                    data = {
                                        "id": product_value['id'],
                                        "price": product_value['price'],
                                        "stock": product_value['stock'],
                                        "description": product_value['description'],
                                        "id_category": product_value['id_category'],
                                        "category_name": data_category.get('name'),
                                        "image": image,
                                        "name": product_value['name'],
                                    }
                                    resultData.append(data)
                        else:
                            Product = ProductModels.query.filter_by(id=id_product).first()
                            data_product = product_schema.dump(Product)
                            if(data_product):
                                id_category = int(data_product['id_category'])
                                Category = CategoryModels.query.filter_by(id=id_category).first()
                                data_category = category_schema.dump(Category)
                                if bool(UseCloundiary) is True:
                                    get_image_cloudinary = cloudinary.api.resources_by_ids([data_product['id_cloudinary']])
                                    image = get_image_cloudinary['resources'][0]['secure_url']
                                if bool(UseImagekit) is True:
                                    get_imagekit = imagekit.get_file_details(data_product['id_imagekit']) 
                                    image = get_imagekit['response']['url']
                                    
                                if bool(UseImagekit) is False and bool(UseCloundiary) is False:
                                    image = request.url_root+display+data_product['image']
                                data = {
                                    "id": data_product['id'],
                                    "price": data_product['price'],
                                    "stock": data_product['stock'],
                                    "description": data_product['description'],
                                    "id_category": data_product['id_category'],
                                    "category_name": data_category.get('name'),
                                    "image": image,
                                    "name": data_product['name'],
                                } 
                                resultData.append(data)
                        result = ResponseApi().error_response(200, "Get Product", "Get Product Succes", start_time, resultData)
                    except Exception as e:
                        error  = str(e)
                        result = ResponseApi().error_response(400, "Get Product", error, start_time) 
                else:
                    result = ResponseApi().error_response(400, "Get Product", "Form Request Is Empty", start_time)
            else:
                result = ResponseApi().error_response(cek_session['code'], "Get Product", cek_session['message'], start_time)
        else:
            result = ResponseApi().error_response(400, "Get Product", "Authentication signature calculation is wrong", start_time)
        response = ResponseApi().response_api(result)
        return response
    
    def insert_product(self,param):
        start_time = ResponseApi().microtime(True)
        if Helpers().cek_auth(param):
            cek_session = Helpers().cek_session(param)
            if cek_session['code'] == 200:
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
                            id_company = cek_session['data']['id_company']
                            # print(id_company)
                            # pdb.run('mymodule.test()')
                            image = ""
                            id_cloudinary = ''
                            id_imagekit = ''
                            save_imagekit = ''
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
                                        if bool(UseCloundiary) is True:
                                            # Upload cloudinary
                                            upload_cloudinary = upload(image_path, 
                                                folder = "assets/images/", 
                                                public_id = image_name+'.'+image_type)
                                            id_cloudinary = upload_cloudinary['public_id']
                                        
                                        if bool(UseImagekit) is True:
                                            # Upload imagekitt
                                            save_imagekit = imagekit.upload_file(
                                                file= image_encode, # required
                                                file_name= image_name+'.'+image_type, # required
                                                options= {
                                                    "folder" : "/assets/images/",
                                                    "tags": ["sample-tag"],
                                                    "is_private_file": False,
                                                    "use_unique_file_name": True,
                                                    "response_fields": ["is_private_file", "tags"],
                                                }
                                            )
                                            id_imagekit = save_imagekit['response']['fileId']
                                        # print(UseImagekit) 
                                        # pdb.run('mymodule.test()')
                                    else:
                                        result = { 
                                            "code" : 400,
                                            "SpeedTime" : ResponseApi().speed_response(start_time),
                                            "endpoint": "Insert Product",
                                            "message": "image_blob is wrong",
                                            "result": {}
                                        }
                                        response = ResponseApi().response_api(result)
                                        return response
                            
                            new_product = ProductModels(id_category, id_company, name_product, description, image, id_cloudinary, id_imagekit , stock, price)
                            db.session.add(new_product)
                            db.session.commit()
                            Product = ProductModels.query.filter_by(name=name_product).first()
                            data_product = product_schema.dump(Product)
                            if bool(UseCloundiary) is True:
                                get_image_cloudinary = cloudinary.api.resources_by_ids([data_product['id_cloudinary']])
                                image = get_image_cloudinary['resources'][0]['secure_url']
                            if bool(UseImagekit) is True:
                                get_imagekit = imagekit.get_file_details(data_product['id_imagekit']) 
                                image = get_imagekit['response']['url']
                            if bool(UseImagekit) is False and bool(UseCloundiary) is False:
                                image = request.url_root+display+data_product['image']
                            data = {
                                "id": data_product['id'],
                                "name" : data_product['name'],
                                "id_category" : data_product['id_category'],
                                "id_company" : data_product['id_company'],
                                "description" : data_product['description'],
                                "image" : image,
                                "stock" : data_product['stock'],
                                "price" : data_product['price'],
                            }
                            
                            resultData.append(data)
                        result = ResponseApi().error_response(200, "Insert Product", "Insert Product Succes", start_time, resultData)
                    except Exception as e:
                        error  = str(e)
                        result = ResponseApi().error_response(400, "Insert Product", error, start_time) 
                else:
                    result = ResponseApi().error_response(400, "Insert Product", "Form Request Is Empty", start_time)
            else:
                result = ResponseApi().error_response(cek_session['code'], "Insert Product", cek_session['message'], start_time)
        else:
            result = ResponseApi().error_response(400, "Insert Product", "Authentication signature calculation is wrong", start_time)
        response = ResponseApi().response_api(result)
        return response
            
    def update_product(self,param):
        start_time = ResponseApi().microtime(True)
        if Helpers().cek_auth(param):
            cek_session = Helpers().cek_session(param)
            if cek_session['code'] == 200:
                form_req = param['form']
                resultData = []
                image = ""
                if form_req:
                    try:
                        for form_value in form_req:
                            id_product = form_value['id_product']
                            name_product = form_value['name']
                            id_category = form_value['id_category']
                            description = form_value['description']
                            id_company = cek_session['data']['id_company']
                            price = form_value['price']
                            stock = form_value['stock']

                            Product = ProductModels.query.filter_by(id=id_product)
                            ge_product = ProductModels.query.filter_by(id=id_product).first()
                            data_product = product_schema.dump(ge_product)
                            id_cloudinary = data_product['id_cloudinary']
                            id_imagekit = data_product['id_imagekit']
                            save_imagekit = ''
                            if form_value['image']:
                                image_encode = form_value['image']['image_blob'] 
                                image_name = form_value['image']['name']
                                image_type = form_value['image']['type']
                                if image_encode != "" and image_name != "" and image_type != "":
                                    image_path = UPLOAD_FOLDER+image_name+'.'+image_type
                                    image_decode = Helpers().decode_image(image_encode)
                                    if image_decode !=0:
                                        image_file = Image.open(io.BytesIO(image_decode))
                                        image_file = image_file.convert('RGB')
                                        image_file.save(image_path)
                                        
                                        # Upload cloudinary
                                        if bool(UseCloundiary) is True:
                                            cloudinary.api.delete_resources([data_product['id_cloudinary']])
                                            upload_cloudinary = upload(image_path, 
                                                folder = "assets/images/", 
                                                public_id = image_name+'.'+image_type)
                                            id_cloudinary = upload_cloudinary['public_id']
                                        
                                        # Upload imagekitt
                                        if bool(UseImagekit) is True:
                                            imagekit.delete_file(data_product['id_imagekit'])
                                            save_imagekit = imagekit.upload_file(
                                                file= image_encode, # required
                                                file_name= image_name+'.'+image_type, # required
                                                options= {
                                                    "folder" : "/assets/images/",
                                                    "tags": ["sample-tag"],
                                                    "is_private_file": False,
                                                    "use_unique_file_name": True,
                                                    "response_fields": ["is_private_file", "tags"],
                                                }
                                            )
                                            id_imagekit = save_imagekit['response']['fileId']
                                        # print(UseImagekit) 
                                        # pdb.run('mymodule.test()')
                                        # print(upload_cloudinary)
                                        # pdb.run('mymodule.test()')
                                    else:
                                        result = {
                                            "code" : 400,
                                            "SpeedTime" : ResponseApi().speed_response(start_time),
                                            "endpoint": "Insert Product",
                                            "message": "image_blob is wrong",
                                            "result": {}
                                        }
                                        response = ResponseApi().response_api(result)
                                        return response
                            if bool(UseCloundiary) is True:
                                get_image_cloudinary = cloudinary.api.resources_by_ids([id_cloudinary])
                                image = get_image_cloudinary['resources'][0]['secure_url'],
                            if bool(UseImagekit) is True:
                                get_imagekit = imagekit.get_file_details(id_imagekit) 
                                image = get_imagekit['response']['url']
                            if bool(UseImagekit) is False and bool(UseCloundiary) is False:
                                image = request.url_root+display+data_product['image']
                            datas = {
                                "id" : id_product,
                                "name" : name_product,
                                "id_category" : id_category,
                                "id_company": id_company,
                                "description" : description,
                                "image" : image,
                                'id_cloudinary': id_cloudinary,
                                'id_imagekit': id_imagekit,
                                "stock" : stock,
                                "price" : price,
                            }
                            Product.update(datas)
                            db.session.commit()
                        
                        Product = ProductModels.query.filter_by(id=id_product).first()
                        data_product = product_schema.dump(Product)
                        data = {
                            "id": data_product['id'],
                            "price": data_product['price'],
                            "stock": data_product['stock'],
                            "description": data_product['description'],
                            "id_category": data_product['id_category'],
                            "id_company": data_product['id_company'],
                            "image": image,
                            "name": data_product['name'],
                        }
                        resultData.append(data)
                        
                        result = ResponseApi().error_response(200, "Update Product", "Update Product Succes", start_time, resultData)
                    except Exception as e:
                        error  = str(e)
                        result = ResponseApi().error_response(400, "Update Product", error, start_time) 
                else:
                    result = ResponseApi().error_response(400, "Update Product", "Form Request Is Empty", start_time)
            else:
                result = ResponseApi().error_response(cek_session['code'], "Update Product", cek_session['message'], start_time)
        else:
            result = ResponseApi().error_response(400, "Update Product", "Authentication signature calculation is wrong", start_time)
        response = ResponseApi().response_api(result)
        return response

    def delete_product(self,param):
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
                                product = ProductModels.query.order_by(ProductModels.id.asc())
                                data_product = products_schema.dump(product)
                                for product_value in data_product:
                                    data = {
                                        'id_product':product_value['id'],
                                        "name" : product_value['name'],
                                    }
                                    # Delete cloudinary
                                    cloudinary.api.delete_resources([product_value['id_cloudinary']])
                                    # Delete imagekit
                                    imagekit.delete_file(product_value['id_imagekit'])
                                    resultData.append(data)
                                ProductModels.query.delete()
                                db.session.commit()
                            else:
                                id_product = form_value['id_product']
                                product = ProductModels.query.filter_by(id=id_product).first()
                                product_value = product_schema.dump(product)
                                # Delete cloudinary
                                cloudinary.api.delete_resources([product_value['id_cloudinary']])
                                # Delete imagekit
                                imagekit.delete_file(product_value['id_imagekit'])

                                db.session.delete(product)
                                db.session.commit()
                                data = {
                                    'id_product':product_value['id'],
                                    "name" : product_value['name'],
                                }
                                resultData.append(data)
                        result = ResponseApi().error_response(200, "Delete Product", "Delete Product Succes", start_time, resultData)
                    except Exception as e:
                        error  = str(e)
                        result = ResponseApi().error_response(400, "Delete Product", error, start_time) 
                else:
                    result = ResponseApi().error_response(400, "Delete Product", "Form Request Is Empty", start_time)
            else:
                result = ResponseApi().error_response(cek_session['code'], "Delete Product", cek_session['message'], start_time)
        else:
            result = ResponseApi().error_response(400, "Delete Product", "Authentication signature calculation is wrong", start_time)
        response = ResponseApi().response_api(result)
        return response