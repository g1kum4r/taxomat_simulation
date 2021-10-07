from flask_restful import fields

user_marshal = {
    "id": fields.Integer,
    "email": fields.String,
    "password": fields.String,
    "firstName": fields.String,
    "lastName": fields.String
}
