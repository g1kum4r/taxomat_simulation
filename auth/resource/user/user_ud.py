from flask import request, make_response
from flask_restful import Resource, marshal_with, marshal

from auth.model import UserModel
from auth.resource.user.marshal import user_marshal
from auth.resource.user.post_args import user_post_args
from __main__ import db


# to get by id, update and delete user
def no_record_found():
    return make_response({'status': 'no record found'}, 200)


class UserResource(Resource):

    def get(self, id):
        user_model = UserModel.query.filter_by(id=id).one_or_none()
        if user_model is None:
            return no_record_found()
        return marshal(user_model, user_marshal)

    def post(self, id):
        args = user_post_args.parse_args(request)
        user_model = UserModel.query.filter_by(id=id).one_or_none()
        if user_model is None:
            return no_record_found()

        user_model.firstName=args.get("firstName")
        user_model.lastName=args.get("lastName")
        db.session.commit()
        return marshal(user_model, user_marshal)

    def delete(self, id):
        args = user_post_args.parse_args(request)
        user_model = UserModel.query.filter_by(id=id).one_or_none()
        if user_model is None:
            return no_record_found()

        db.session.delete(user_model)
        db.session.commit()
        return marshal(user_model, user_marshal)
