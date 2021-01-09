from app.models.transaction_models import TransactionModels, TransactionSchema
from flask_restful import Resource
from flask import request, jsonify
from app.helpers.helpers import Helpers
from app.helpers.response import ResponseApi
from app.manage import db
from PIL import Image
import pdb
import io

transaction_schema = TransactionSchema()
transactions_schema = TransactionSchema(many=True)

class TransactionController(Resource):
    def get_transaction(self,param):
        start_time = ResponseApi().microtime(True)
        if Helpers().cek_auth(param):
            # cek_session = Helpers().cek_session(param)
            # if cek_session['code'] == 200:
                form_req = param['form']
                if form_req:
                    try:
                        showAll = form_req['ShowAll']
                        id_transaction = form_req['id_transaction']
                        if showAll:
                            Transaction = TransactionModels.query.all()
                            data = transactions_schema.dump(Transaction)
                            
                        else:
                            Transaction = TransactionModels.query.filter_by(id=id_transaction).first()
                            data = transactions_schema.dump(Transaction)
                        
                        result = {
                            "code" : 200,
                            "SpeedTime" : ResponseApi().speed_response(start_time),
                            "endpoint": "Get Transaction",
                            "message": "Get Transaction Succes",
                            "result": data
                        }
                    except Exception as e:
                        error  = str(e)
                        result = {
                            "code" : 400,
                            "SpeedTime" : ResponseApi().speed_response(start_time),
                            "endpoint": "Get Transaction",
                            "message": error,
                            "result": {}
                        }
                else:
                    result = {
                        "code" : 400,
                        "SpeedTime" : ResponseApi().speed_response(start_time),
                        "endpoint": "Get Transaction",
                        "message": "Form Request Is Empty",
                        "result": {}
                    }
            # else:
            #     result = {
            #         "code" : cek_session['code'],
            #         "SpeedTime" : ResponseApi().speed_response(start_time),
            #         "endpoint": "Get Transaction",
            #         "message": cek_session['message'],
            #         "result": {}
            #     }
        else:
            result = {
                "code" : 400,
                "SpeedTime" : ResponseApi().speed_response(start_time),
                "endpoint": "Get Transaction",
                "message": "Authentication signature calculation is wrong",
                "result": {}
            }
        response = ResponseApi().response_api(result)
        return response
    
    def insert_transaction(self,param):
        start_time = ResponseApi().microtime(True)
        if Helpers().cek_auth(param):
            # cek_session = Helpers().cek_session(param)
            # if cek_session['code'] == 200:
                form_req = param['form']
                resultData = []
                if form_req:
                    try:
                        for form_value in form_req:
                            id_company = form_value['id_company']
                            id_user_company = form_value['id_user_company']
                            id_user_buyer = form_value['id_user_buyer']
                            buyer_name = form_value['buyer_name']
                            date_time = form_value['date_time']
                            amount_of_charge = form_value['amount_of_charge']
                            new_transaction = TransactionModels(id_company, id_user_company, id_user_buyer, 
                                    buyer_name, date_time, amount_of_charge)
                            db.session.add(new_transaction)
                            db.session.commit()
                            data = {
                                "id_company" : id_company,
                                "id_user_company" : id_user_company,
                                "id_user_buyer" : id_user_buyer,
                                "buyer_name" : buyer_name,
                                "date_time" : date_time,
                                "amount_of_charge" : amount_of_charge,
                            }
                        resultData.append(data)
                        result = {
                            "code" : 200,
                            "SpeedTime" : ResponseApi().speed_response(start_time),
                            "endpoint": "Insert Transasction",
                            "message": "Insert Transasction Succes",
                            "result": resultData
                        }    
                        # print(result)
                        # pdb.run('mymodule.test()')

                    except Exception as e:
                        error  = str(e)
                        result = {
                            "code" : 400,
                            "SpeedTime" : ResponseApi().speed_response(start_time),
                            "endpoint": "Insert Transasction",
                            "message": error,
                            "result": {}
                        }
                else:
                    result = {
                        "code" : 400,
                        "SpeedTime" : ResponseApi().speed_response(start_time),
                        "endpoint": "Insert Transasction",
                        "message": "Form Request Is Empty",
                        "result": {}
                    }
            # else:
            #     result = {
            #         "code" : cek_session['code'],
            #         "SpeedTime" : ResponseApi().speed_response(start_time),
            #         "endpoint": "Insert Transaction",
            #         "message": cek_session['message'],
            #         "result": {}
            #     }
        else:
            result = {
                "code" : 400,
                "SpeedTime" : ResponseApi().speed_response(start_time),
                "endpoint": "Insert Transaction",
                "message": "Authentication signature calculation is wrong",
                "result": {}
            }
        response = ResponseApi().response_api(result)
        return response
        
    def update_transaction(self,param):
        start_time = ResponseApi().microtime(True)
        if Helpers().cek_auth(param):
            # cek_session = Helpers().cek_session(param)
            # if cek_session['code'] == 200:
                form_req = param['form']
                resultData = []
                if form_req:
                    try:
                        for form_value in form_req:
                            id_transaction = form_value['id_transaction']
                            id_company = form_value['id_company']
                            id_user_company = form_value['id_user_company']
                            id_user_buyer = form_value['id_user_buyer']
                            buyer_name = form_value['buyer_name']
                            date_time = form_value['date_time']
                            amount_of_charge = form_value['amount_of_charge']
                            data = {
                                "id" : id_transaction,
                                "id_company" : id_company,
                                "id_user_company" : id_user_company,
                                "id_user_buyer" : id_user_buyer,
                                "buyer_name" : buyer_name,
                                "date_time" : date_time,
                                "amount_of_charge" : amount_of_charge,
                            }
                            Transaction = TransactionModels.query.filter_by(id=id_transaction)
                            Transaction.update(data)
                            db.session.commit()
                            resultData.append(data)
                        result = {
                            "code" : 200,
                            "SpeedTime" : ResponseApi().speed_response(start_time),
                            "endpoint": "Update Transaction",
                            "message": "Update Transaction Succes",
                            "result": resultData
                        }
                        # print(result)
                        # pdb.run('mymodule.test()')
                    except Exception as e:
                        error  = str(e)
                        result = {
                            "code" : 400,
                            "SpeedTime" : ResponseApi().speed_response(start_time),
                            "endpoint": "Update Transaction",
                            "message": error,
                            "result": {}
                        }
                else:
                    result = {
                        "code" : 400,
                        "SpeedTime" : ResponseApi().speed_response(start_time),
                        "endpoint": "Update Transaction",
                        "message": "Form Request Is Empty",
                        "result": {}
                    }
            # else:
            #     result = {
            #         "code" : cek_session['code'],
            #         "SpeedTime" : ResponseApi().speed_response(start_time),
            #         "endpoint": "Update Transaction",
            #         "message": cek_session['message'],
            #         "result": {}
            #     }
        else:
            result = {
                "code" : 400,
                "SpeedTime" : ResponseApi().speed_response(start_time),
                "endpoint": "Update Transaction",
                "message": "Authentication signature calculation is wrong",
                "result": {}
            }
        response = ResponseApi().response_api(result)
        return response

    def delete_transaction(self,param):
        start_time = ResponseApi().microtime(True)
        if Helpers().cek_auth(param):
            # cek_session = Helpers().cek_session(param)
            # if cek_session['code'] == 200:
                form_req = param['form']
                resultData = []
                if form_req:
                    try:
                        for form_value in form_req:
                            id_transaction = form_value['id_transaction']
                            Transaction = TransactionModels.query.filter_by(id=id_transaction).first()
                            transaction_value = transaction_schema.dump(Transaction)
                            db.session.delete(Transaction)
                            db.session.commit()
                            data = {
                                'id':transaction_value['id'],
                                "id_company" : transaction_value['id_company'],
                                "id_user_company" : transaction_value['id_user_company'],
                                "id_user_buyer" : transaction_value['id_user_buyer'],
                                "buyer_name" : transaction_value['buyer_name'],
                                "date_time" : transaction_value['date_time'],
                                "amount_of_charge" : transaction_value['amount_of_charge'],
                            }
                            resultData.append(data)
                        result = {
                            "code" : 200,
                            "SpeedTime" : ResponseApi().speed_response(start_time),
                            "endpoint": "Delete Transaction",
                            "message": "Delete Transaction Succes",
                            "result": resultData
                        }
                    except Exception as e:
                        error  = str(e)
                        result = {
                            "code" : 400,
                            "SpeedTime" : ResponseApi().speed_response(start_time),
                            "endpoint": "Delete Transaction",
                            "message": error,
                            "result": {}
                        }
                else:
                    result = {
                        "code" : 400,
                        "SpeedTime" : ResponseApi().speed_response(start_time),
                        "endpoint": "Delete Transaction",
                        "message": "Form Request Is Empty",
                        "result": {}
                    }
            # else:
            #     result = {
            #         "code" : cek_session['code'],
            #         "SpeedTime" : ResponseApi().speed_response(start_time),
            #         "endpoint": "Update Transaction",
            #         "message": cek_session['message'],
            #         "result": {}
            #     }
        else:
            result = {
                "code" : 400,
                "SpeedTime" : ResponseApi().speed_response(start_time),
                "endpoint": "Delete Transaction",
                "message": "Authentication signature calculation is wrong",
                "result": {}
            }
        response = ResponseApi().response_api(result)
        return response