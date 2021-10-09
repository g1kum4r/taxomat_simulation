from flask import Blueprint, render_template
from flask_login import login_required

bp = Blueprint('banks', __name__, url_prefix='/banks')


@bp.route('')
@login_required
def list():
    return render_template('dashboard/banks.html', title='Banks')
