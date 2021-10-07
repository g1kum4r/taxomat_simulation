from flask import request, current_app
from flask_restful import Resource, marshal_with

from auth.model import UserModel
from auth.resource.user.marshal import user_marshal
from auth.resource.user.post_args import user_post_args
from __main__ import db


# to fetch, filter and save user
class UserListResource(Resource):

    @marshal_with(user_marshal)
    def get(self):
        return [u for u in UserModel.query.all()]

    @marshal_with(user_marshal)
    def post(self):
        args = user_post_args.parse_args(request)
        user_model = UserModel(email=args.get('email'),
                               password=args.get('password'),
                               firstName=args.get('firstName'),
                               lastName=args.get('lastName'))
        db.session.add(user_model)
        db.session.commit()
        return user_model
