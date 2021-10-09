from bson import ObjectId
from flask import Blueprint, render_template, request, flash, url_for
from flask_login import login_required
from werkzeug.utils import redirect

from app.bank.model import banks_list, BankForm, save_bank, get_bank, delete_bank

bp = Blueprint('banks', __name__, url_prefix='/banks')


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

    # form = CitizenGenerateForm()
    # if form.validate_on_submit():
    #     print('generating...')
    #     try:
    #         result = generate_list(form.range.data, start_from_cnic=form.start_from_cnic.data)
    #         print(f'result: {result.__str__()}')
    #     except BulkWriteError as e:
    #         print(f'result: {e}')
    #         flash(f'error {e.args}', 'danger')

    data = banks_list(offset, limit)
    return render_template('dashboard/banks.html', title='Banks', data=data, page=page)


@bp.route('/form', methods=['GET', 'POST'])
@bp.route('/form/<string:_id>', methods=['GET', 'POST'])
@login_required
def form(_id: str = None):
    _form = BankForm()

    if _id is None:
        title = 'Add Bank'
    else:
        title = 'Edit Bank'
        bank = get_bank(ObjectId(_id))
        print(f'bank: {bank}')
        if bank is not None:
            if not _form.is_submitted():
                _form.name.data = bank.get('name')
                _form.code.data = bank.get('code')
        else:
            flash(f'bank not found by _id {_id}', 'danger')

    if _form.validate_on_submit():
        result = save_bank(_form.name.data, _form.code.data, ObjectId(_id) if _id is not None else None)
        if result is not None:
            flash(f'{_form.name.data} Saved', 'success')
            return redirect(url_for('banks.get_list'))

    return render_template('dashboard/banks_form.html', title=title, form=_form)


@bp.route('/delete/<string:_id>', methods=['GET'])
@login_required
def delete(_id: str = None):
    bank = get_bank(ObjectId(_id))
    if bank is None:
        flash(f'bank not found by _id: {_id}', 'danger')
    else:
        result = delete_bank(ObjectId(_id))
        if result is None:
            flash(f'unknown result from mongodb {_id}', 'danger')
        else:
            flash(f'{bank.get("name")} deleted', 'success')

    return redirect(url_for('banks.get_list'))
