from flask_wtf import FlaskForm
from wtforms import SubmitField
from wtforms.fields.html5 import IntegerField
from app.dasboard.citizen.doa import citizens_list, generate_list


class CitizenGenerateForm(FlaskForm):
    start_from_cnic = IntegerField('Start from CNIC')
    range = IntegerField('Range')
    submit = SubmitField('Generate')