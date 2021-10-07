from flask import Flask
from flask_restful import Api
from flask_sqlalchemy import SQLAlchemy

from auth.config import Config

app = Flask(__name__)
app.config.from_object(Config)
api = Api(app)
db = SQLAlchemy(app)

db.drop_all()
db.create_all()
from auth.resource import UserListResource, UserResource
api.add_resource(UserListResource, '/users')
api.add_resource(UserResource, '/users/<int:id>')

if __name__ == '__main__':
    app.run(debug=True)
