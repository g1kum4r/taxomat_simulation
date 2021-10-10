from flask import Blueprint, render_template
from flask_login import login_required

bp = Blueprint('excise', __name__, url_prefix='/excise')


@bp.route('')
@login_required
def get_list():
    return render_template('dashboard/excise.html', title='Excise')

