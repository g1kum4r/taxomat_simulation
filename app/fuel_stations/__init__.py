from flask import Blueprint, render_template
from flask_login import login_required

bp = Blueprint('fuel_stations', __name__, url_prefix='/fuel_stations')


@bp.route('')
@login_required
def get_list():
    return render_template('dashboard/fuel_stations.html', title='Fuel Stations')

