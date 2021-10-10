from bson import ObjectId
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField

from app import mongo


class BusinessForm(FlaskForm):
    ntn = StringField('NTN')
    registration_no = StringField('Registration No')
    title = StringField('Title')
    code = StringField('Code')
    submit = SubmitField('Save')


def business_list(offset=0, limit=0):
    return {
        'count': mongo.db.business.count(),
        'list': mongo.db.business.find().skip(offset).limit(limit)
    }


def save_business(ntn: str, registration_no: str, title: str, code: str, _id: ObjectId = None):
    if _id is None:
        print('create new')
        return mongo.db.business.insert_one({
            'ntn': ntn,
            'registration_no': registration_no,
            'title': title,
            'code': code
        })
    else:
        print('update')
        return mongo.db.business.find_one_and_update({"_id": _id}, {'$set': {
            'ntn': ntn,
            'registration_no': registration_no,
            "title": title,
            "code": code
        }})


def get_business(_id: ObjectId):
    return mongo.db.business.find_one({"_id": _id})


def delete_business(_id: ObjectId):
    return mongo.db.business.delete_one({"_id": _id})
