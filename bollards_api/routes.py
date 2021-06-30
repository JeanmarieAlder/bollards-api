from flask import render_template, url_for, flash, redirect
from bollards_api import app, db, bcrypt
from bollards_api.models import User, Bollard
from bollards_api.forms import LoginForm, BollardForm, RegisterForm
from flask_login import login_user

bollards = [
    {
        "number": "1",
        "name": "Vitiau",
        "comment": "This is the first comment of the bollard. Please like, subscribe and share",
        "dateAdded": "date",
        "dateUpdated": "date"
    },
    {
        "number": "2",
        "name": "lol",
        "comment": "This is the second comment of the bollard. Please like, subscribe and share",
        "dateAdded": "date",
        "dateUpdated": "date"
    },
    {
        "number": "3",
        "name": "betty",
        "comment": "This is the third comment of the bollard. Please like, subscribe and share OMG",
        "dateAdded": "date",
        "dateUpdated": "date"
    }
]

@app.route('/')
@app.route('/home')
def home():
    return render_template('home.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        existing_user = User.query.filter_by(username=form.username.data).first()
        if existing_user and bcrypt.check_password_hash(existing_user.password, form.password.data):
            login_user(existing_user, remember=form.remember.data)
            flash(f'Login successful. Welcome {existing_user.username}!', 'success')
            return redirect(url_for('home'))
        else:
            flash('Login failed, try again', 'danger')
    return render_template('login.html', title='Login', form=form)

@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        new_user = User(username=form.username.data, password=hashed_password)
        db.session.add(new_user)
        db.session.commit()
        flash(f'Account created. Welcome {form.username.data}. Please log in.', 'success')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)

@app.route('/list')
def list_bollards():
    return render_template('list.html', title='List', bollards=bollards)

@app.route('/manage')
def manage():
    form = BollardForm()
    return render_template('manage.html', title='Manage', form=form)

@app.route('/add', methods=['GET', 'POST'])
def add():
    form = BollardForm()
    if form.validate_on_submit():
        flash(f'Bollard {form.number.data} Created', 'success')
        return redirect(url_for('list_bollards'))
    return render_template('manage.html', title='Add', form=form)
