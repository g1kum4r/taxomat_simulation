from bson import ObjectId
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField

from app import mongo


class SGCForm(FlaskForm):
    name = StringField('Name')
    code = StringField('Code')
    submit = SubmitField('Save')


def sgc_list(offset=0, limit=0):
    return {
        'count': mongo.db.sgc.count(),
        'list': mongo.db.sgc.find().skip(offset).limit(limit)
    }


def save_sgc(name: str, code: str, id: ObjectId = None):
    if id is None:
        return mongo.db.sgc.insert_one({
            'name': name,
            'code': code
        })
    else:
        return mongo.db.sgc.find_one_and_update({"_id": id}, {'$set': {
            "name": name,
            "code": code
        }})


def get_sgc(id: ObjectId):
    return mongo.db.sgc.find_one({"_id": id})


def delete_sgc(id: ObjectId):
    return mongo.db.sgc.delete_one({"_id": id})
