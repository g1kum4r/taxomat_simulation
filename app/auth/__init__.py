from __main__ import mongo, login_manager, bcrypt

from bson import ObjectId

from app.auth.forms import LoginForm, RegisterForm, PasswordForget, PasswordReset

from flask import Blueprint, render_template, flash, url_for, request
from flask_login import login_user, current_user,  logout_user
from werkzeug.utils import redirect

from app.auth.model import UserModel

bp = Blueprint("auth", __name__, url_prefix="/auth")


@login_manager.user_loader
def load_user(user_id):
    _user = mongo.db.users.find_one({"_id": ObjectId(user_id)})
    if _user is not None:
        user = UserModel(mongo.db.users.find_one({"_id": ObjectId(user_id)}))
        return user
    return None


@bp.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()

    args = request.args
    if args.get('email') is not None:
        form.email.data = args.get('email')

    if form.validate_on_submit():
        _user = mongo.db.users.find_one({'email': form.email.data})
        user = UserModel(_user)
        if user is not None:
            if bcrypt.check_password_hash(_user.get('password'), form.password.data):
                if login_user(user, remember=form.remember_me.data):
                    args = request.args
                    if args.get('next') is not None:
                        return redirect(args.get('next'))
                    else:
                        return redirect(url_for('dashboard.index'))
                else:
                    flash('Internal error occurred', 'error')

            else:
                flash('Incorrect password', 'error')
        else:
            flash(f'email {form.email.data} not registered', 'error')

    return render_template("auth/login.html", title='Sign In', form=form)


@bp.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('dashboard'))

    form = RegisterForm()
    if form.validate_on_submit():
        email = form.email.data
        password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        inserted_id = mongo.db.users.insert({
            'email': email,
            'password': password
        })
        flash(f'Account created {email}. Login in now', 'success')
        return redirect(url_for('auth.login', email=email))
    return render_template("auth/register.html", title='Register', form=form)


@bp.route('/password/forget', methods=['GET', 'POST'])
def forget_password():
    form = PasswordForget()
    if form.validate_on_submit():
        flash(f'Password reset link sent. check your inbox.', 'success')
        # return redirect(url_for('auth.login'))
    return render_template("auth/password_forget.html", title='Forget Password', form=form)


@bp.route('/password/reset/<token>', methods=['GET', 'POST'])
def reset_password(token):
    form = PasswordReset()
    if form.validate_on_submit():
        flash(f'Password reset. Login with your new password.', 'success')
        return redirect(url_for('auth.login'))
    return render_template("auth/password_reset.html", title='Reset Password', form=form)

@bp.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('auth.login'))