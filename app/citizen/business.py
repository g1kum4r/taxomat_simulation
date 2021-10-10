import random

from bson import ObjectId
from flask import flash, url_for, render_template, request
from flask_login import login_required
from pymongo.command_cursor import CommandCursor
from werkzeug.utils import redirect

from app.business import save_business, BusinessForm, delete_business
from app.citizen import bp
from app.citizen.model import get_citizen, update_citizen_business, get_citizen_with_business


@bp.route('/<string:_id>/business', methods=['GET', 'POST'])
@login_required
def get_citizen_business(_id: str):
    bf = BusinessForm()
    citizen = get_citizen_with_business(ObjectId(_id))
    print(f'citizen: {citizen}')
    if citizen is None:
        flash(f'citizen not found by id: {_id}', 'danger')
        return redirect(url_for('citizens.get_list'))
    else:
        bf.ntn.data = citizen.get('ntn')

    if bf.is_submitted():
        registration_no = bf.registration_no.data
        if registration_no is None or registration_no == '':
            registration_no = f'{random.randint(100000000, 999999999)}'

        result = save_business(bf.ntn.data, registration_no, bf.title.data, bf.code.data)
        if result is not None and result.inserted_id is not None:
            business_list = citizen.get('business')
            if business_list is None:
                business_list = []
            business_list.append(result.inserted_id)
            update_citizen_business(ObjectId(_id), business_list)
            citizen = get_citizen_with_business(ObjectId(_id))

    return render_template('dashboard/citizen_profile_business.html', title=citizen.get('cnic'),
                           data=citizen, bf=bf, business=True)


@bp.route('/<string:_id>/business/delete', methods=['GET'])
@login_required
def remove_citizen_business(_id: str):

    citizen = get_citizen(ObjectId(_id))
    if citizen is None:
        flash(f'citizen not found with id {_id}', 'danger')

    business_id = ObjectId(request.args.get("business_id"))
    delete_business(ObjectId(business_id))
    business = [b for b in citizen.get('business') if b != business_id]
    update_citizen_business(ObjectId(_id), business)
    return redirect(url_for('citizens.get_citizen_business', _id=_id))