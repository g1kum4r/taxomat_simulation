from bson import ObjectId
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField

from app import mongo


class EPCForm(FlaskForm):
    name = StringField('Name')
    code = StringField('Code')
    submit = SubmitField('Save')


def epc_list(offset=0, limit=0):
    return {
        'count': mongo.db.epc.count(),
        'list': mongo.db.epc.find().skip(offset).limit(limit)
    }


def save_epc(name: str, code: str, id: ObjectId = None):
    if id is None:
        print('create new')
        return mongo.db.epc.insert_one({
            'name': name,
            'code': code
        })
    else:
        print('update')
        return mongo.db.epc.find_one_and_update({"_id": id}, {'$set': {
            "name": name,
            "code": code
        }})


def get_epc(id: ObjectId):
    return mongo.db.epc.find_one({"_id": id})


def delete_epc(id: ObjectId):
    return mongo.db.epc.delete_one({"_id": id})
