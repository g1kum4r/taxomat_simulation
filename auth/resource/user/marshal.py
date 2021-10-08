from flask_restful import fields

user_marshal = {
    "_id": fields.String,
    "email": fields.String,
    "password": fields.String,
    "firstName": fields.String,
    "lastName": fields.String
}
