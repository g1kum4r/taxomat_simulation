from bson import ObjectId
from flask import Blueprint, render_template, url_for, flash, request
from flask_login import login_required
from werkzeug.utils import redirect

from app.sui_gas_provider_companies.model import sgc_list, SGCForm, get_sgc, save_sgc, delete_sgc

bp = Blueprint('sui_gas_provider_companies', __name__, url_prefix='/sui_gas_provider_companies')


@bp.route('', methods=['GET'])
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

    data = sgc_list(offset, limit)
    return render_template('dashboard/sui_gas_provider_companies.html',
                           title='SUI Gas Provider Companies', data=data, page=page)


@bp.route('/form', methods=['GET', 'POST'])
@bp.route('/form/<string:_id>', methods=['GET', 'POST'])
@login_required
def form(_id: str = None):
    _form = SGCForm()

    if _id is None:
        title = 'Add SUI Gase Provider Company'
    else:
        title = 'Edit SUI Gase Provider Company'
        epc = get_sgc(ObjectId(_id))
        # print(f'bank: {bank}')
        if epc is not None:
            if not _form.is_submitted():
                _form.name.data = epc.get('name')
                _form.code.data = epc.get('code')
        else:
            flash(f'SUI Gase Provider Company not found by id {_id}', 'danger')

    if _form.validate_on_submit():
        result = save_sgc(_form.name.data, _form.code.data, ObjectId(_id) if _id is not None else None)
        if result is not None:
            flash(f'{_form.name.data} Saved', 'success')
            return redirect(url_for('sui_gas_provider_companies.get_list'))

    return render_template('dashboard/sui_gas_provider_companies_form.html', title=title, form=_form)


@bp.route('/delete/<string:_id>', methods=['GET'])
@login_required
def delete(_id: str = None):
    bank = get_sgc(ObjectId(_id))
    if bank is None:
        flash(f'SUI Gase Provider Company not found by id: {_id}', 'danger')
    else:
        result = delete_sgc(ObjectId(_id))
        if result is None:
            flash(f'unknown result from mongodb {_id}', 'danger')
        else:
            flash(f'{bank.get("name")} deleted', 'success')

    return redirect(url_for('sui_gas_provider_companies.get_list'))
