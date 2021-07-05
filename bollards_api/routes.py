import secrets
import os
from PIL import Image
from flask import render_template, url_for, flash, redirect, request
from bollards_api import app, db, bcrypt
from bollards_api.models import User, Bollard
from bollards_api.forms import LoginForm, BollardForm, RegisterForm, UpdateAccountForm, UpdateAccountPasswordForm
from flask_login import login_user, logout_user , current_user, login_required

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
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = LoginForm()
    if form.validate_on_submit():
        print(request.form)
        existing_user = User.query.filter_by(username=form.username.data).first()
        if existing_user and bcrypt.check_password_hash(existing_user.password, form.password.data):
            login_user(existing_user, remember=form.remember.data)
            next_page = request.args.get('next')
            flash(f'Login successful. Welcome {existing_user.username}!', 'success')
            return redirect(next_page) if next_page else redirect(url_for('home'))
        else:
            flash('Login failed, try again', 'danger')
    return render_template('login.html', title='Login', form=form)

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('home'))


def crop_center(pil_img, crop_width, crop_height):
    img_width, img_height = pil_img.size
    return pil_img.crop(((img_width - crop_width) // 2,
                         (img_height - crop_height) // 2,
                         (img_width + crop_width) // 2,
                         (img_height + crop_height) // 2))


def crop_max_square(pil_img):
    return crop_center(pil_img, min(pil_img.size), min(pil_img.size))


def save_picture(new_picture, folder_path):

    fixed_square_size = 150

    random_hex = secrets.token_hex(8)
    _, file_ext = os.path.splitext(new_picture.filename)
    picture_filename = random_hex + file_ext
    picture_path = os.path.join(app.root_path, 'static', 'img', 
                                    folder_path, picture_filename)
    output_size = (fixed_square_size, fixed_square_size)
    i = Image.open(new_picture)

    # Crop image to square
    print(str(i.width) + " " + str(i.height))
    i_width = i.width
    i_height = i.height
    if i_width > fixed_square_size and i_height > fixed_square_size:
        i = crop_max_square(i)
        
    # Reduce the size of picture
    i.thumbnail(output_size, Image.ANTIALIAS)

    i.save(picture_path)
    return picture_filename

@app.route('/account', methods=['GET', 'POST'])
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
            picture_file = save_picture(form_account.profile_pic.data, 'profile_pics')
            print(picture_file)
            current_user.profile_pic = picture_file
        current_user.username = form_account.username.data
        db.session.commit()
        flash(f'Accound updated, your username is now {form_account.username.data}.', 'success')
    elif form_password_submitted and form_password.validate_on_submit():
        existing_user = User.query.filter_by(username=current_user.username).first()
        if existing_user and bcrypt.check_password_hash(existing_user.password, form_password.old_password.data):
            hashed_password = bcrypt.generate_password_hash(form_password.new_password.data).decode('utf-8')
            current_user.password = hashed_password
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


@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
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
    bollards = Bollard.query.all()
    return render_template('list.html', title='List', bollards=bollards)

@app.route('/manage')
def manage():
    form = BollardForm()
    return render_template('manage.html', title='Manage', form=form)

@app.route('/add', methods=['GET', 'POST'])
@login_required
def add():
    form = BollardForm()
    if form.validate_on_submit():
        picture_file = "thenamelol.jpeg"
        new_bollard = Bollard(number=form.number.data, b_name=form.b_name.data,
                                comment=form.comment.data, image_file=picture_file)
        db.session.add(new_bollard)
        db.session.commit()
        flash(f'Bollard No {form.number.data} Created', 'success')
        return redirect(url_for('list_bollards'))
    return render_template('manage.html', title='Add', form=form)
