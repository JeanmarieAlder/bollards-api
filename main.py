from datetime import datetime
from flask import Flask, render_template, url_for, flash, redirect
from flask_sqlalchemy import SQLAlchemy
from forms import LoginForm, BollardForm

app = Flask(__name__)

app.config['SECRET_KEY'] = 'plzchangeit'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///bollards.db'

db = SQLAlchemy(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(25), unique=True, nullable=False)
    password = db.Column(db.String(100), nullable=False)

    def __repr__(self):
        return f"User('{self.username}')"

class Bollard(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    number = db.Column(db.String(10), unique=True, nullable=False)
    name = db.Column(db.String(50))
    comment = db.Column(db.Text())
    image_file = db.Column(db.String(20), nullable=False, default='default.jpg')
    date_created = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    date_updated = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    def __repr__(self):
        return f"Bollard('{self.number}', '{self.name}', '{self.comment}', '{self.image_file}')"

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
        if form.username.data == 'user' and form.password.data == 'password':
            flash(f'Logged in successfully. Welcome {form.username.data}.', 'success')
            return redirect(url_for('home'))
        else:
            flash('Login failed, try again', 'danger')
    return render_template('login.html', title='Login', form=form)

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

if __name__ == "__main__":
    app.run(debug=True)