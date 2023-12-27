import os
from datetime import datetime, timezone

from bollards_api import bcrypt, db
from bollards_api.models import User
from bollards_api.users.forms import (LoginForm, RegisterForm,
                                      UpdateAccountForm,
                                      UpdateAccountPasswordForm)
from bollards_api.users.utils import save_picture_profile
from flask import Blueprint, flash, redirect, render_template, request, url_for
from flask_login import current_user, login_required, login_user, logout_user

users = Blueprint('users', __name__)

@users.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    form = LoginForm()
    if form.validate_on_submit():
        # print(request.form)
        existing_user = User.query.filter_by(username=form.username.data).first()
        if existing_user and bcrypt.check_password_hash(existing_user.password, form.password.data):
            login_user(existing_user, remember=form.remember.data)
            next_page = request.args.get('next')
            flash(f'Login successful. Welcome {existing_user.username}!', 'success')
            return redirect(next_page) if next_page else redirect(url_for('main.home'))
        else:
            flash('Login failed, try again', 'danger')
    return render_template('login.html', title='Login', form=form)

@users.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('main.home'))


@users.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    form = RegisterForm()
    if form.validate_on_submit():
        # Secret phrase is needed to 
        if bcrypt.check_password_hash(os.environ['REGISTRATION_SECRET_PHRASE'], form.secret_phrase.data):
            hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
            new_user = User(username=form.username.data, password=hashed_password)
            db.session.add(new_user)
            db.session.commit()
            flash(f'Account created. Welcome {form.username.data}. Please log in.', 'success')
            return redirect(url_for('users.login'))
        else:
            flash('Account creation is limited. Please contact the author for specific access', 'warning')
    return render_template('register.html', title='Register', form=form)


@users.route('/account', methods=['GET', 'POST'])
@login_required
def account(): 
    form_account = UpdateAccountForm()
    form_password = UpdateAccountPasswordForm()
    form_account_submitted = form_account.submit_account.data
    form_password_submitted = form_password.submit_password.data
    if form_account_submitted:
        accordion_account_open = "show"
        accordion_password_open = ""
    elif form_password_submitted:
        accordion_account_open = ""
        accordion_password_open = "show"
    else:
        accordion_account_open = ""
        accordion_password_open = ""
    # Check which form has been submitted, to make it work, submit buttons must have different names.
    if form_account_submitted and form_account.validate_on_submit():
        if form_account.profile_pic.data:
            picture_file = save_picture_profile(form_account.profile_pic.data)
            # print(picture_file)
            current_user.profile_pic = picture_file
        current_user.username = form_account.username.data
        current_user.date_updated = datetime.now(timezone.utc)
        db.session.commit()
        flash(f'Accound updated, your username is now {form_account.username.data}.', 'success')
    elif form_password_submitted and form_password.validate_on_submit():
        existing_user = User.query.filter_by(username=current_user.username).first()
        if existing_user and bcrypt.check_password_hash(existing_user.password, form_password.old_password.data):
            hashed_password = bcrypt.generate_password_hash(form_password.new_password.data).decode('utf-8')
            current_user.password = hashed_password
            current_user.date_updated = datetime.now(timezone.utc)
            db.session.commit()
            flash(f'Account password updated successfully.', 'success')
        else:
            flash('An error occured when changing the password, please try again.', 'danger')
    form_account.username.data = current_user.username
    profile_pic = url_for('static', filename='img/profile_pics/' + current_user.profile_pic)
    return render_template('account.html', title='Account', 
                            profile_pic=profile_pic,
                            accordion_account_open = accordion_account_open,
                            accordion_password_open = accordion_password_open,
                            form_account=form_account,
                            form_password=form_password)
