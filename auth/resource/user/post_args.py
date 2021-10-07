from flask_restful import reqparse

user_post_args = reqparse.RequestParser()
user_post_args.add_argument("email", type=str, help="this field is required", required=True)
user_post_args.add_argument("password", type=str, help="this field is required", required=True)
user_post_args.add_argument("firstName", type=str)
user_post_args.add_argument("lastName", type=str)
