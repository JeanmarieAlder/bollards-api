from datetime import datetime
import secrets
import os
from PIL import Image
from flask import render_template, url_for, flash, redirect, request
from flask_migrate import current
from bollards_api import app, db, bcrypt
from bollards_api.models import Bimage, User, Bollard
from bollards_api.forms import LoginForm, BollardForm, RegisterForm, UpdateAccountForm, UpdateAccountPasswordForm
from flask_login import login_user, logout_user , current_user, login_required


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
    random_hex = secrets.token_hex(8)
    _, file_ext = os.path.splitext(new_picture.filename)
    picture_filename = random_hex + file_ext
    picture_path = os.path.join(app.root_path, 'static', 'img', 
                                    folder_path, picture_filename)
    i = Image.open(new_picture)
    i.save(picture_path)
    return picture_filename


def crop_save_picture(new_picture, folder_path, fixed_square_size):
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


def save_picture_profile(new_picture):
    fixed_square_size = 150
    folder_path = 'profile_pics'
    return crop_save_picture(new_picture, folder_path, fixed_square_size)

# Saves the icon format as well as the full picture
def save_picture_bollard(new_picture):
    fixed_square_size = 250
    folder_path_icon = 'bollards_icon'
    folder_path = 'bollards'
    return crop_save_picture(new_picture, folder_path_icon, fixed_square_size), save_picture(new_picture, folder_path)


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
            picture_file = save_picture_profile(form_account.profile_pic.data)
            print(picture_file)
            current_user.profile_pic = picture_file
        current_user.username = form_account.username.data
        current_user.date_updated = datetime.utcnow()
        db.session.commit()
        flash(f'Accound updated, your username is now {form_account.username.data}.', 'success')
    elif form_password_submitted and form_password.validate_on_submit():
        existing_user = User.query.filter_by(username=current_user.username).first()
        if existing_user and bcrypt.check_password_hash(existing_user.password, form_password.old_password.data):
            hashed_password = bcrypt.generate_password_hash(form_password.new_password.data).decode('utf-8')
            current_user.password = hashed_password
            current_user.date_updated = datetime.utcnow()
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

@app.route('/manage/<int:bollard_id>', methods=['GET', 'POST'])
@login_required
def manage(bollard_id):
    form = BollardForm()
    bollard = Bollard.query.filter_by(id=bollard_id).first_or_404()
    if form.validate_on_submit():
        bollard.b_number = form.b_number.data
        bollard.b_name = form.b_name.data
        bollard.comment = form.comment.data
        bollard.b_lat = form.b_lat.data
        bollard.b_lng = form.b_lng.data
        bollard.date_updated = datetime.utcnow()
        if form.main_image.data:
            picture_file_icon, picture_file = save_picture_bollard(form.main_image.data)
            print(picture_file_icon)
            print(picture_file)
            bollard.image_icon = picture_file_icon
            bollard.main_image = picture_file
        
        # fs is a FileStorage type
        if form.images.data[0].filename != '':
            for fs in form.images.data:    
                picture_file = save_picture(new_picture=fs, folder_path='bollards')
                new_bimage = Bimage(uri=picture_file)
                bollard.images.append(new_bimage)
        current_user.last_lat = form.b_lat.data
        current_user.last_lon = form.b_lng.data
        current_user.last_zoom = form.zoom_level.data
        db.session.commit()
        flash(f'Bollard No {form.b_number.data} has been updated', 'success')
        return redirect(url_for('list_bollards'))
    
    form.b_number.data = bollard.b_number
    form.b_name.data = bollard.b_name
    form.comment.data = bollard.comment
    form.b_lat.data = bollard.b_lat
    form.b_lng.data = bollard.b_lng
    return render_template('manage.html', title='Manage', bollard=bollard, form=form,
        has_map=True, init_lat=bollard.b_lat, init_lng=bollard.b_lng)


@app.route('/add', methods=['GET', 'POST'])
@login_required
def add():
    form = BollardForm()
    if form.validate_on_submit():
        if Bollard.query.filter_by(b_number=form.b_number.data).first():
            flash(f'Bollard No {form.b_number.data} allready exists', 'danger')
        else:
            # for fs in form.images.data:
            #    print(fs.filename)
            new_bollard = Bollard(b_number=form.b_number.data, b_name=form.b_name.data,
                                    comment=form.comment.data, b_lat=form.b_lat.data,
                                    b_lng=form.b_lng.data)
            if form.main_image.data:
                print(form.main_image.data)
                print(form.images.data[0])
                picture_file_icon, picture_file = save_picture_bollard(form.main_image.data)
                print(picture_file_icon)
                print(picture_file)
                new_bollard.image_icon = picture_file_icon
                new_bollard.main_image = picture_file
            
            # fs is a FileStorage type
            for fs in form.images.data:
                if fs.filename != '':
                    picture_file = save_picture(new_picture=fs, folder_path='bollards')
                    new_bimage = Bimage(uri=picture_file)
                    new_bollard.images.append(new_bimage)

            current_user.last_lat = form.b_lat.data
            current_user.last_lon = form.b_lng.data
            current_user.last_zoom = form.zoom_level.data
            db.session.add(new_bollard)
            db.session.commit()
            flash(f'Bollard No {form.b_number.data} Created', 'success')
            return redirect(url_for('list_bollards'))
    return render_template('manage.html', title='Add', form=form, has_map=True,
                init_lat=current_user.last_lat, init_lng=current_user.last_lon,
                init_zoom=current_user.last_zoom)


@app.route('/delete/<int:bollard_id>', methods=['POST'])
@login_required
def delete_bollard(bollard_id):
    bollard = Bollard.query.filter_by(id=bollard_id).first_or_404()
    db.session.delete(bollard)
    db.session.commit()
    flash('Bollard deleted successfully.', 'info')
    return redirect(url_for('list_bollards'))
