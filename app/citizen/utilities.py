import random

from bson import ObjectId
from flask import render_template, request, url_for
from flask_login import login_required
from werkzeug.utils import redirect

from app.citizen import bp
from app.citizen.model import get_citizen, UtilityAccountForm, update_citizen_utilities, get_citizen_with_utility_provider


@bp.route('/<string:_id>/utilities', methods=['GET', 'POST'])
@login_required
def get_citizen_utilities(_id: str):
    citizen = get_citizen_with_utility_provider(ObjectId(_id))
    uaf = UtilityAccountForm()
    if uaf.is_submitted():
        consumer_no = uaf.consumer_no.data
        if consumer_no is None or consumer_no == '':
            consumer_no = f'{random.randint(1000000, 9999999)}'

        meter_no = uaf.meter_no.data
        if meter_no is None or meter_no == '':
            meter_no = f'{random.randint(1000000, 9999999)}'

        utilities = citizen.get('utilities')
        if utilities is None:
            utilities = []
        utilities.append({
            'provider_id': ObjectId(uaf.provider_id.data),
            'consumer_no': consumer_no,
            'meter_no': meter_no,
        })
        update_citizen_utilities(ObjectId(_id), utilities)
        citizen = get_citizen_with_utility_provider(ObjectId(_id))

    return render_template('dashboard/citizen_profile_utilities.html', title='Utilities', utilities=True, data=citizen,
                           uaf=uaf)


@bp.route('/<string:_id>/utilities/delete', methods=['GET'])
@login_required
def remove_citizen_utility(_id: str):
    citizen = get_citizen(ObjectId(_id))
    args = request.args
    if args.get('consumer_no') is not None:
        consumer_no = args.get('consumer_no', type=str)
        utilities = [u for u in citizen.get("utilities") if u.get('consumer_no') != consumer_no]
        update_citizen_utilities(ObjectId(_id), utilities)

    return redirect(url_for('citizens.get_citizen_utilities', _id=_id))