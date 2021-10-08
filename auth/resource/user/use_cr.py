from __main__ import db

from flask import request
from flask_restful import Resource, marshal_with, marshal

from auth.resource.user.marshal import user_marshal


# to fetch, filter and save user
class UserListResource(Resource):

    def get(self):
        args = request.args
        limit = args.get(key="limit", default=0, type=int)
        page = args.get(key="page", default=0, type=int)
        offset = 0
        if page > 0:
            offset = (page - 1) * limit
        return {
            'total': db.users.count(),
            'data': marshal([u for u in db.users.find().skip(offset).limit(limit)], user_marshal)
        }

    @marshal_with(user_marshal)
    def post(self):
        inserted_id = db.users.insert(request.get_json())
        return db.users.find_one({'_id': inserted_id})


class UserListGenerator(Resource):

    @marshal_with(user_marshal)
    def get(self):
        return [u for u in db.users.find()]

    @marshal_with(user_marshal)
    def post(self):
        inserted_id = db.users.insert(request.get_json())
        return db.users.find_one({'_id': inserted_id})
