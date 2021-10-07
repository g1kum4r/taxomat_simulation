from flask_restful import reqparse

# for create/update profile
user_post_args = reqparse.RequestParser()
user_post_args.add_argument("firstName", type=str)
user_post_args.add_argument("lastName", type=str)


# for registration and authentication
user_auth_args = reqparse.RequestParser()
user_auth_args.add_argument("email", type=str, help="email is required", required=True)
user_auth_args.add_argument("password", type=str, help="password is required", required=True)
