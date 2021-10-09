from flask import request, flash, render_template, Blueprint
from flask_login import login_required
from flask_wtf import FlaskForm
from pymongo.errors import BulkWriteError
from wtforms import SubmitField
from wtforms.fields.html5 import IntegerField
from app.citizen.model import citizens_list, generate_list


class CitizenGenerateForm(FlaskForm):
    start_from_cnic = IntegerField('Start from CNIC')
    range = IntegerField('Range')
    submit = SubmitField('Generate')


bp = Blueprint('citizens', __name__, url_prefix='/citizens')


@bp.route('', methods=['GET', 'POST'])
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
