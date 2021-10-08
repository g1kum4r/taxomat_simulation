from bson import ObjectId
from flask import Blueprint, render_template, flash, request
from flask_login import current_user, login_required
from pymongo.errors import BulkWriteError

from app import mongo
from app.auth import UserModel
from app.dasboard.citizen import CitizenGenerateForm, citizens_list, generate_list
from app.dasboard.profile import ProfileForm

bp = Blueprint('dashboard', __name__)


@bp.route('/')
@bp.route('/dashboard')
@login_required
def index():
    return render_template('dashboard.html', title='Dashboard')


@bp.route('/citizens', methods=['GET', 'POST'])
@login_required
def citizens():
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


@bp.route('/banks')
@login_required
def banks():
    return render_template('dashboard/banks.html', title='Banks')


@bp.route('/electricity')
@login_required
def electricity():
    return render_template('dashboard/electricity.html', title='Electricity')


@bp.route('/fuelstations')
@login_required
def fuel_stations():
    return render_template('dashboard/fuelstations.html', title='Fuel Stations')


@bp.route('/profile',  methods=['GET', 'POST'])
@login_required
def profile():
    user = current_user
    form = ProfileForm()

    if form.validate_on_submit():
        mongo.db.users.update({'_id': ObjectId(user.id)}, {
            '$set' : {'first_name': form.first_name.data,
                      'last_name': form.last_name.data}
        })
        user = UserModel(mongo.db.users.find_one({'_id': ObjectId(user.id)}))
        flash('Profile updated', 'success')

    form.first_name.data = user.first_name
    form.last_name.data = user.last_name
    return render_template('dashboard/profile.html', title=user.email, user=user, form=form)
