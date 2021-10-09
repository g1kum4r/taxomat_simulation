from bson import ObjectId
from flask import Blueprint, render_template, request, url_for, flash
from flask_login import login_required
from werkzeug.utils import redirect

from app.electricity_provider_companies.model import epc_list, EPCForm, get_epc, save_epc, delete_epc

bp = Blueprint('electricity_provider_companies', __name__, url_prefix='/electricity_provider_companies')


@bp.route('', methods=['GET'])
@login_required
def list():
    args = request.args
    limit = args.get('limit', type=int, default=20)
    page = args.get('page', type=int, default=1)
    offset = 0
    if page > 1:
        offset = (page - 1) * limit
    else:
        page = 1

    data = epc_list(offset, limit)
    return render_template('dashboard/electricity_provider_companies.html', title='Electricity Provider Companies', data=data, page=page)


@bp.route('/form', methods=['GET', 'POST'])
@bp.route('/form/<string:id>', methods=['GET', 'POST'])
@login_required
def form(id: str = None):
    form = EPCForm()

    if id is None:
        title = 'Add Electricity Provider Company'
    else:
        title = 'Edit Electricity Provider Company'
        epc = get_epc(ObjectId(id))
        # print(f'bank: {bank}')
        if epc is not None:
            if not form.is_submitted():
                form.name.data = epc.get('name')
                form.code.data = epc.get('code')
        else:
            flash(f'Electricity Provider Company not found by id {id}', 'danger')

    if form.validate_on_submit():
        result = save_epc(form.name.data, form.code.data, ObjectId(id) if id is not None else None)
        if result is not None:
            flash(f'{form.name.data} Saved', 'success')
            return redirect(url_for('electricity_provider_companies.list'))

    return render_template('dashboard/electricity_provider_companies_form.html', title=title, form=form)


@bp.route('/delete/<string:id>', methods=['GET'])
@login_required
def delete(id: str = None):
    bank = get_epc(ObjectId(id))
    if bank is None:
        flash(f'Electricity Provider Company not found by id: {id}', 'danger')
    else:
        result = delete_epc(ObjectId(id))
        if result is None:
            flash(f'unknown result from mongodb {id}', 'danger')
        else:
            flash(f'{bank.get("name")} deleted', 'success')

    return redirect(url_for('electricity_provider_companies.list'))

