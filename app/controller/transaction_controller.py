from app.models.transaction_models import TransactionModels, TransactionSchema
from flask_restful import Resource
from app.helpers.helpers import Helpers
from app.helpers.response import ResponseApi
from app.manage import db
import pdb
import io

transaction_schema = TransactionSchema()
transactions_schema = TransactionSchema(many=True)

class TransactionController(Resource):
    def get_transaction(self,param):
        start_time = ResponseApi().microtime(True)
        if Helpers().cek_auth(param):
            cek_session = Helpers().cek_session(param)
            if cek_session['code'] == 200:
                form_req = param['form']
                if form_req:
                    try:
                        show_all = form_req['show_all']
                        id_transaction = form_req['id_transaction']
                        if show_all:
                            Transaction = TransactionModels.query.all()
                            data = transactions_schema.dump(Transaction)
                            
                        else:
                            Transaction = TransactionModels.query.filter_by(id=id_transaction).first()
                            data = transactions_schema.dump(Transaction)
                        
                        result = ResponseApi().error_response(200, "Get Transaction", "Get Transaction Succes", start_time, data)
                    except Exception as e:
                        error  = str(e)
                        result = ResponseApi().error_response(400, "Get Transaction", error, start_time) 
                else:
                    result = ResponseApi().error_response(400, "Get Transaction", "Form Request Is Empty", start_time)
            else:
                result = ResponseApi().error_response(cek_session['code'], "Get Transaction", cek_session['message'], start_time)
        else:
            result = ResponseApi().error_response(400, "Get Transaction", "Authentication signature calculation is wrong", start_time)
        response = ResponseApi().response_api(result)
        return response
    
    def insert_transaction(self,param):
        start_time = ResponseApi().microtime(True)
        if Helpers().cek_auth(param):
            cek_session = Helpers().cek_session(param)
            if cek_session['code'] == 200:
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
                        
                        result = ResponseApi().error_response(200, "Insert Transaction", "Insert Transaction Succes", start_time, resultData) 
                        # print(result)
                        # pdb.run('mymodule.test()')

                    except Exception as e:
                        error  = str(e)
                        result = ResponseApi().error_response(400, "Insert Transaction", error, start_time) 
                else:
                    result = ResponseApi().error_response(400, "Insert Transaction", "Form Request Is Empty", start_time)
            else:
                result = ResponseApi().error_response(cek_session['code'], "Insert Transaction", cek_session['message'], start_time)
        else:
            result = ResponseApi().error_response(400, "Insert Transaction", "Authentication signature calculation is wrong", start_time)
        response = ResponseApi().response_api(result)
        return response
        
    def update_transaction(self,param):
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
                        
                        result = ResponseApi().error_response(200, "Update Transaction", "Update Transaction Succes", start_time, resultData)
                        # print(result)
                        # pdb.run('mymodule.test()')
                    except Exception as e:
                        error  = str(e)
                        result = ResponseApi().error_response(400, "Update Transaction", error, start_time) 
                else:
                    result = ResponseApi().error_response(400, "Update Transaction", "Form Request Is Empty", start_time)
            else:
                result = ResponseApi().error_response(cek_session['code'], "Update Transaction", cek_session['message'], start_time)
        else:
            result = ResponseApi().error_response(400, "Update Transaction", "Authentication signature calculation is wrong", start_time)
        response = ResponseApi().response_api(result)
        return response

    def delete_transaction(self,param):
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
                                Transaction = TransactionModels.query.order_by(TransactionModels.id.asc())
                                data_transaction = transactions_schema.dump(Transaction)
                                for transaction_value in data_transaction:
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
                                TransactionModels.query.delete()
                                db.session.commit()
                            else:
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
                        
                        result = ResponseApi().error_response(200, "Delete Transaction", "Delete Transaction Succes", start_time, resultData)
                    except Exception as e:
                        error  = str(e)
                        result = ResponseApi().error_response(400, "Delete Transaction", error, start_time) 
                else:
                    result = ResponseApi().error_response(400, "Delete Transaction", "Form Request Is Empty", start_time)
            else:
                result = ResponseApi().error_response(cek_session['code'], "Delete Transaction", cek_session['message'], start_time)
        else:
            result = ResponseApi().error_response(400, "Delete Transaction", "Authentication signature calculation is wrong", start_time)
        response = ResponseApi().response_api(result)
        return response