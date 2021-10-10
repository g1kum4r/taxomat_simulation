from bson import ObjectId
from flask import render_template, url_for, flash, request
from flask_login import login_required
from werkzeug.utils import redirect

from app.citizen import bp
from app.citizen.model import get_citizen, IncomeSourceForm, update_citizen_income_sources, get_business_lookup
from app.business.model import get_business


@bp.route('/<string:_id>/income_sources', methods=['GET', 'POST'])
@login_required
def get_citizen_income_sources(_id: str):
    citizen = get_citizen(ObjectId(_id))
    isf = IncomeSourceForm()
    isf.employer_id.choices = get_business_lookup(citizen.get('ntn'))

    args = request.args
    employement_id = None
    if args.get('employement_id') is not None:
        employement_id = ObjectId(args.get('employement_id'))
        employment = next()
        isf.employer_id.data = employement_id

    if isf.is_submitted():
        employer_id = isf.employer_id.data
        employer_id = ObjectId(employer_id) if isinstance(employer_id, str) else employer_id
        business = get_business(employer_id)
        if business is None:
            flash(f'business not found by id: {employer_id}', 'danger')
        else:
            income_sources = citizen.get('income_sources')
            if income_sources is None:
                income_sources = []

            if employement_id is not None:
                income_sources = [i for i in income_sources if i.get('_id') != employement_id]

            if employement_id is None:
                employement_id = ObjectId()

            income_sources.append({
                '_id': employement_id,
                'type': isf.type.data,
                'employer_id': business.get('_id'),
                'employer_name': business.get('title'),
                'dateFrom': isf.dateFrom.data.__str__() if isf.dateFrom.data is not None else None,
                'dateTo': isf.dateTo.data.__str__() if isf.dateTo.data is not None else None
            })
            update_citizen_income_sources(ObjectId(_id), income_sources)
            citizen = get_citizen(ObjectId(_id))

    return render_template('dashboard/citizen_profile_income_sources.html', title='Income Sources', income_sources=True,
                           data=citizen,
                           isf=isf)


@bp.route('/<string:_id>/income_sources/update/<string:is_id>', methods=['POST'])
@login_required
def update_citizen_income_source(_id: str, is_id: str):
    # citizen = get_citizen(ObjectId(_id))
    # isf = IncomeSourceForm(request.form)
    # if isf.is_submitted():
    #     is_id = ObjectId(is_id)
    #     citizen.get('')
    # args = request.args
    # if args.get('consumer_no') is not None:
    #     consumer_no = args.get('consumer_no', type=str)
    #     utilities = [u for u in citizen.get("utilities") if u.get('consumer_no') != consumer_no]
    #     update_citizen_utilities(ObjectId(_id), utilities)

    return redirect(url_for('citizens.income_sources', _id=_id))
