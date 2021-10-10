from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField
from wtforms.validators import DataRequired, Length, Email, EqualTo


class LoginForm(FlaskForm):
    email = StringField('Email', validators=[
        DataRequired(), Email(), Length(min=8, max=32)
    ])
    password = PasswordField('Password', validators=[
        DataRequired(), Length(min=6, max=20)
    ])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Login')


class RegisterForm(FlaskForm):
    email = StringField('Email', validators=[
        DataRequired(), Email(), Length(min=8, max=32)
    ])
    password = PasswordField('Password', validators=[
        DataRequired(), Length(min=6, max=20)
    ])
    confirm_password = PasswordField('Confirm Password', validators=[
        DataRequired(), Length(min=6, max=20), EqualTo(fieldname='password', message="password not matched")
    ])
    submit = SubmitField('Register')


class PasswordForget(FlaskForm):
    email = StringField('Email', validators=[
        DataRequired(), Email(), Length(min=8, max=32)
    ])
    submit = SubmitField('Email reset password link')


class PasswordReset(FlaskForm):
    password = PasswordField('New Password', validators=[
        DataRequired(), Length(min=6, max=20)
    ])
    confirm_password = PasswordField('Confirm New Password', validators=[
        DataRequired(), Length(min=6, max=20), EqualTo(fieldname='password', message="password not matched")
    ])
    submit = SubmitField('Reset Password')
