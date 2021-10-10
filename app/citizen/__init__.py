import random

from bson import ObjectId
from flask import request, flash, render_template, Blueprint, url_for
from flask_login import login_required
from pymongo.errors import BulkWriteError, DuplicateKeyError
from werkzeug.utils import redirect

from app.business import BusinessForm
from app.citizen.model import citizens_list, generate_list, CitizenGenerateForm, get_citizen, BankAccountForm, \
    UtilityAccountForm, IncomeTaxForm, add_citizen_bank_accounts

bp = Blueprint('citizens', __name__, url_prefix='/citizens')


@bp.route('', methods=['GET', 'POST'])
@login_required
def get_list():
    args = request.args
    limit = args.get('limit', type=int, default=20)
    page = args.get('page', type=int, default=1)
    offset = 0
    if page > 1:
        offset = (page - 1) * limit
    else:
        page = 1

    form = CitizenGenerateForm()
    if form.validate_on_submit():
        print('generating...')
        try:
            result = generate_list(form.range.data, start_from_cnic=form.start_from_cnic.data)
            print(f'result: {result.__str__()}')
        except (BulkWriteError, DuplicateKeyError) as e:
            print(f'result: {e}')
            flash(f'error {e.args}', 'danger')

    data = citizens_list(offset, limit)
    return render_template('dashboard/citizens.html', title='Citizens', data=data, form=form, page=page)


@bp.route('/<string:_id>', methods=['GET'])
@login_required
def get(_id: str):
    uaf = UtilityAccountForm()
    uaf.consumer_no.data = random.randint(1000000, 9999999)
    itf = IncomeTaxForm()
    citizen = get_citizen(ObjectId(_id))
    if citizen is None:
        flash(f'citizen not found by id: {_id}', 'danger')
        return redirect(url_for('citizens.get_list'))
    return render_template('dashboard/citizen_profile.html', title=citizen.get('cnic'),
                           data=citizen, uaf=uaf, itf=itf)


@bp.route('/add_business', methods=['POST'])
@login_required
def add_business():
    _form = BusinessForm(request.form)
    if _form.is_submitted():
        pass


from app.citizen.bank_accounts import remove_bank_account, get_citizen_bank_accounts
from app.citizen.business import get_citizen_business
from app.citizen.utilities import get_citizen_utilities
