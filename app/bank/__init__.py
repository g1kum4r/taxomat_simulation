from bson import ObjectId
from flask import Blueprint, render_template, request, flash, url_for
from flask_login import login_required
from werkzeug.utils import redirect

from app.bank.model import banks_list, BankForm, save_bank, get_bank, delete_bank

bp = Blueprint('banks', __name__, url_prefix='/banks')


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
@bp.route('/form/<string:id>', methods=['GET', 'POST'])
@login_required
def form(id: str = None):
    form = BankForm()

    if id is None:
        title = 'Add Bank'
    else:
        title = 'Edit Bank'
        bank = get_bank(ObjectId(id))
        print(f'bank: {bank}')
        if bank is not None:
            if not form.is_submitted():
                form.name.data = bank.get('name')
                form.code.data = bank.get('code')
        else:
            flash(f'bank not found by id {id}', 'danger')

    if form.validate_on_submit():
        result = save_bank(form.name.data, form.code.data, ObjectId(id) if id is not None else None)
        if result is not None:
            flash(f'{form.name.data} Saved', 'success')
            return redirect(url_for('banks.list'))

    return render_template('dashboard/banks_form.html', title=title, form=form)


@bp.route('/delete/<string:id>', methods=['GET'])
@login_required
def delete(id: str = None):
    bank = get_bank(ObjectId(id))
    if bank is None:
        flash(f'bank not found by id: {id}', 'danger')
    else:
        result = delete_bank(ObjectId(id))
        if result is None:
            flash(f'unknown result from mongodb {id}', 'danger')
        else:
            flash(f'{bank.get("name")} deleted', 'success')

    return redirect(url_for('banks.list'))


