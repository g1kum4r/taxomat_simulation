from bson import ObjectId
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField

from app import mongo


class BankForm(FlaskForm):
    name = StringField('Name')
    code = StringField('Code')
    submit = SubmitField('Save')


def banks_list(offset=0, limit=0):
    return {
        'count': mongo.db.banks.count(),
        'list': mongo.db.banks.find().skip(offset).limit(limit)
    }


def save_bank(name: str, code: str, _id: ObjectId = None):
    if _id is None:
        print('create new')
        return mongo.db.banks.insert_one({
            'name': name,
            'code': code
        })
    else:
        print('update')
        return mongo.db.banks.find_one_and_update({"_id": _id}, {'$set': {
            "name": name,
            "code": code
        }})


def get_bank(_id: ObjectId):
    return mongo.db.banks.find_one({"_id": _id})


def delete_bank(id: ObjectId):
    return mongo.db.banks.delete_one({"_id": id})
