from flask import Blueprint, render_template
from flask_login import login_required

bp = Blueprint('electricity_provider_companies', __name__, url_prefix='/electricity_provider_companies')


@bp.route('')
@login_required
def list():
    return render_template('dashboard/electricity_provider_companies.html', title='Electricity Provider Companies')


