import random

from bson import ObjectId
from flask import request, flash, render_template, Blueprint, url_for
from flask_login import login_required
from pymongo.errors import BulkWriteError
from werkzeug.utils import redirect

from app.bank import get_bank
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
        except BulkWriteError as e:
            print(f'result: {e}')
            flash(f'error {e.args}', 'danger')

    data = citizens_list(offset, limit)
    return render_template('dashboard/citizens.html', title='Citizens', data=data, form=form, page=page)


@bp.route('/<string:_id>', methods=['GET'])
@login_required
def get(_id: str):
    baf = BankAccountForm()
    baf.iban.data = random.randint(10000000000000, 99999999999999)
    uaf = UtilityAccountForm()
    uaf.consumer_no.data = random.randint(1000000, 9999999)
    itf = IncomeTaxForm()
    citizen = get_citizen(ObjectId(_id))
    if citizen is None:
        flash(f'citizen not found by id: {_id}', 'danger')
        return redirect(url_for('citizens.get_list'))
    return render_template('dashboard/citizen_profile.html', title=citizen.get('cnic'),
                           data=citizen, baf=baf, uaf=uaf, itf=itf)


@bp.route('/add_bank_account/<string:_id>', methods=['POST'])
@login_required
def add_bank_account(_id: str):
    baf = BankAccountForm(request.form)
    print(f'add_bank_account: {baf}')
    citizen: dict = get_citizen(ObjectId(_id))
    if citizen is None:
        flash(f'citizen not found by id: {_id}', 'danger')
        return redirect(url_for('citizens.get_list'))

    if baf.is_submitted():
        bank = get_bank(ObjectId(baf.bank_id.data))
        if bank is None:
            flash(f'bank not exist by id {baf.bank_id.data}', 'danger')
        else:
            if baf.iban.data is None:
                baf.iban.data = random.randint(10000000000000, 99999999999999)
            bank.update({'iban': baf.iban.data})
            bank_accounts = citizen.get('bank_accounts')
            bank_accounts.append(bank)
            add_citizen_bank_accounts(citizen.get('_id'), bank_accounts)
    else:
        print('not submitted')

    return redirect(url_for('citizens.get', _id=_id))


@bp.route('/remove_bank_account/<string:_id>', methods=['GET'])
@login_required
def remove_bank_account(_id: str):
    iban = request.args.get('iban', type=str)
    # print(f'iban: {iban} {type(iban)}')
    citizen: dict = get_citizen(ObjectId(_id))
    if citizen is None:
        flash(f'citizen not found by id: {_id}', 'danger')
        return redirect(url_for('citizens.get_list'))

    bank_accounts = citizen.get('bank_accounts')
    # print(f'ba: {bank_accounts}')
    bank_accounts = [b for b in bank_accounts if str(b.get('iban')) != iban]
    # print(f'ba: {bank_accounts}')
    add_citizen_bank_accounts(citizen.get('_id'), bank_accounts)

    return redirect(url_for('citizens.get', _id=_id))
