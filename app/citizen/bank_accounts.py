import random

from bson import ObjectId
from flask import request, flash, url_for, render_template
from flask_login import login_required
from werkzeug.utils import redirect

from app.bank import get_bank
from app.citizen import bp
from app.citizen.model import BankAccountForm, get_citizen, update_citizen_bank_accounts


@bp.route('/<string:_id>/bank_accounts', methods=['GET', 'POST'])
@login_required
def get_citizen_bank_accounts(_id: str):
    baf = BankAccountForm()
    citizen = get_citizen(ObjectId(_id))
    if citizen is None:
        flash(f'citizen not found by id: {_id}', 'danger')
        return redirect(url_for('citizens.get_list'))
    elif baf.is_submitted():
        bank = get_bank(ObjectId(baf.bank_id.data))
        if bank is None:
            flash(f'bank not exist by id {baf.bank_id.data}', 'danger')
        else:
            print(f'baf.iban.data: {baf.iban.data}')
            iban = baf.iban.data
            if iban is None or iban.strip() == '':
                iban = f'PK{bank.get("code")}{str(random.randint(10000000000000, 99999999999999))}'
            print(f'baf.iban.data: {iban}')
            bank.update({'iban': iban})
            bank_accounts = citizen.get('bank_accounts')
            bank_accounts.append(bank)
            update_citizen_bank_accounts(citizen.get('_id'), bank_accounts)
    else:
        print('not submitted')
    return render_template('dashboard/citizen_profile_bank_accounts.html', title=citizen.get('cnic'),
                           data=citizen, baf=baf, bank_accounts=True)


# @bp.route('/add_bank_account/<string:_id>', methods=['POST'])
# @login_required
# def add_bank_account(_id: str):
#     baf = BankAccountForm(request.form)
#     # print(f'add_bank_account: {baf}')
#     citizen: dict = get_citizen(ObjectId(_id))
#     if citizen is None:
#         flash(f'citizen not found by id: {_id}', 'danger')
#         return redirect(url_for('citizens.get_list'))
#
#     if baf.is_submitted():
#         bank = get_bank(ObjectId(baf.bank_id.data))
#         if bank is None:
#             flash(f'bank not exist by id {baf.bank_id.data}', 'danger')
#         else:
#             print(f'baf.iban.data: {baf.iban.data}')
#             if baf.iban.data is None or baf.iban.data.strip() == '':
#                 baf.iban.data = f'PK{bank.get("code")}{str(random.randint(10000000000000, 99999999999999))}'
#             print(f'baf.iban.data: {baf.iban.data}')
#             bank.update({'iban': baf.iban.data})
#             bank_accounts = citizen.get('bank_accounts')
#             bank_accounts.append(bank)
#             update_citizen_bank_accounts(citizen.get('_id'), bank_accounts)
#     else:
#         print('not submitted')
#
#     return redirect(url_for('citizens.get', _id=_id))


@bp.route('/<string:_id>/bank_accounts/delete', methods=['GET'])
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
    update_citizen_bank_accounts(citizen.get('_id'), bank_accounts)

    return redirect(url_for('citizens.get_citizen_bank_accounts', _id=_id))
