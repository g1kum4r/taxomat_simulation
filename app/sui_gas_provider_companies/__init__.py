from flask import Blueprint, render_template
from flask_login import login_required

bp = Blueprint('sui_gas_provider_companies', __name__, url_prefix='/sui_gas_provider_companies')


@bp.route('')
@login_required
def list():
    return render_template('dashboard/sui_gas_provider_companies.html', title='SUI Gas Provider Companies')

