from bson import ObjectId
from flask import Blueprint, render_template, request, flash, url_for
from flask_login import login_required
from werkzeug.utils import redirect

from app.business.model import BusinessForm, business_list, get_business, save_business, delete_business

bp = Blueprint('business', __name__, url_prefix='/business')


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

    data = business_list(offset, limit)
    return render_template('dashboard/business.html', title='Business', data=data, page=page)


@bp.route('/form', methods=['GET', 'POST'])
@bp.route('/form/<string:_id>', methods=['GET', 'POST'])
@login_required
def form(_id: str = None):
    _form = BusinessForm()

    if _id is None:
        title = 'Add Business'
    else:
        title = 'Edit Business'
        bank = get_business(ObjectId(_id))
        print(f'bank: {bank}')
        if bank is not None:
            if not _form.is_submitted():
                _form.ntn.data = bank.get('ntn')
                _form.registration_no.data = bank.get('registration_no')
                _form.name.data = bank.get('name')
                _form.code.data = bank.get('code')
        else:
            flash(f'Business not found by _id {_id}', 'danger')

    if _form.validate_on_submit():
        result = save_business(_form.ntn.data, _form.registration_no.data,  _form.name.data, _form.code.data, ObjectId(_id) if _id is not None else None)
        if result is not None:
            flash(f'{_form.name.data} Saved', 'success')
            return redirect(url_for('business.get_list'))

    return render_template('dashboard/business_form.html', title=title, form=_form)


@bp.route('/delete/<string:_id>', methods=['GET'])
@login_required
def delete(_id: str = None):
    bank = get_business(ObjectId(_id))
    if bank is None:
        flash(f'business not found by _id: {_id}', 'danger')
    else:
        result = delete_business(ObjectId(_id))
        if result is None:
            flash(f'unknown result from mongodb {_id}', 'danger')
        else:
            flash(f'{bank.get("name")} deleted', 'success')

    return redirect(url_for('business.get_list'))
