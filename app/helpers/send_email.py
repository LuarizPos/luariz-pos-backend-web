from flask_restful import Resource
from app.manage import mail
from flask_mail import Message
import pdb
from flask import render_template, request
import os

class SendEmail(Resource):
    def send_email_confirm_register(self,**kwargs):
        subject = "【Luariz Pos】Confirm Your Registration"
        cek_connection = kwargs['cek_connection']
        if cek_connection is not True:
            to = kwargs['params']['email']
            encode_validation = kwargs['encode_validation']
        else:
            to = 'startcode01@gmail.com'
            encode_validation = kwargs['encode_validation']
        sender = os.getenv('MAIL_USERNAME')
        url_roots = request.url_root
        content = {
            'url_roots' : url_roots+'v1/verify_account/',
            'encode_validation' : encode_validation
        }
        template = render_template('mail_verify_register.html',content = content)
        msg = Message(
            subject,
            recipients=[to],
            html=template,
            sender= sender
        )
        try:
            mail.send(msg)
            response = {
                "code":200,
                "status":"Succes",
                "Message":"Send Email Succes",
            }
        except Exception as e:
            error  = str(e)
            response = {
                "code":400,
                "status":"Succes",
                "Message":"Email Not Send",
        }
        
        return response