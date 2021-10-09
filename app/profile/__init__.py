from bson import ObjectId
from flask import Blueprint, flash, render_template
from flask_login import login_required, current_user
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField

from app import mongo
from app.auth import UserModel

bp = Blueprint('profile', __name__, url_prefix='/profile')


@bp.route('', methods=['GET', 'POST'])
@login_required
def page():
    user = current_user
    form = ProfileForm()

    if form.validate_on_submit():
        mongo.db.users.update({'_id': ObjectId(user.id)}, {
            '$set': {'first_name': form.first_name.data,
                     'last_name': form.last_name.data}
        })
        user = UserModel(mongo.db.users.find_one({'_id': ObjectId(user.id)}))
        flash('Profile updated', 'success')

    form.first_name.data = user.first_name
    form.last_name.data = user.last_name
    return render_template('dashboard/profile.html', title=user.email, user=user, form=form)


class ProfileForm(FlaskForm):
    first_name = StringField('First Name')
    last_name = StringField('Last Name')
    submit = SubmitField('Update')
