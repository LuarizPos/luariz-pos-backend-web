from flask import Flask, request, jsonify
from flask_restful import Resource, Api
from app.models.users_models import UsersModel, UsersSchema

user_schema = UsersSchema()
users_schema = UsersSchema(many=True)

class UsersController(Resource):
    def get_user():
        all_data = UsersModel.query.all()
        result = users_schema.dump(all_data)
        return jsonify(result)