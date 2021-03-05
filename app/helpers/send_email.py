from flask_restful import Resource
from sib_api_v3_sdk.rest import ApiException
from app.manage import mail
from flask_mail import Message
from pprint import pprint
import pdb
from flask import render_template, request
import os

class SendEmail(Resource):
    def send_email_confirm_register(self,params,encode_validation):
        subject = "【Luariz Pos】Confirm Your Registration"
        to = params['email']
        sender = os.getenv('MAIL_USERNAME')
        url_roots = request.url_root
        content = {
            'url_roots' : url_roots+'v1/verify_account/',
            'encode_validation' : encode_validation
        }
        template = render_template('mail_welcome_confirm.html',content = content)
        msg = Message(
            subject,
            recipients=[to],
            html=template,
            sender= sender
        )
        mail.send(msg)
        return mail