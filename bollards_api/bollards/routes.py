from datetime import datetime

from bollards_api import db
from bollards_api.bollards.utils import save_picture_bollard, save_picture
from bollards_api.bollards.forms import BollardForm
from bollards_api.models import Bimage, Bollard
from flask import Blueprint, flash, redirect, render_template, request, url_for
from flask_login import current_user, login_required

bollards = Blueprint('bollards', __name__)

@bollards.route('/list')
def list_bollards():
    page = request.args.get('page', 1, type=int)
    sort_method = request.args.get('sort', 'latest', type=str)
    if sort_method == 'ndesc':
        bollards = Bollard.query.order_by(Bollard.b_number.desc(), 
                    Bollard.b_letter.desc()).paginate(page=page, per_page=30)
    elif sort_method == 'nasc':
        bollards = Bollard.query.order_by(Bollard.b_number, 
                    Bollard.b_letter).paginate(page=page, per_page=30)
    else:
        bollards = Bollard.query.order_by(Bollard.date_updated.desc()).paginate(page=page, per_page=30)
    return render_template('list.html', title='List', bollards=bollards,
                    sort_method=sort_method)

@bollards.route('/manage/<int:bollard_id>', methods=['GET', 'POST'])
@login_required
def manage(bollard_id):
    form = BollardForm()
    bollard = Bollard.query.filter_by(id=bollard_id).first_or_404()
    if form.validate_on_submit():
        bollard.b_number = form.b_number.data
        bollard.b_letter = form.b_letter.data
        bollard.b_name = form.b_name.data
        bollard.comment = form.comment.data
        bollard.b_lat = form.b_lat.data
        bollard.b_lng = form.b_lng.data
        bollard.date_updated = datetime.utcnow()
        if form.main_image.data:
            picture_file_icon, picture_file = save_picture_bollard(form.main_image.data)
            # print(picture_file_icon)
            # print(picture_file)
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
        return redirect(url_for('bollards.list_bollards'))
    
    form.b_number.data = bollard.b_number
    form.b_letter.data = bollard.b_letter
    form.b_name.data = bollard.b_name
    form.comment.data = bollard.comment
    form.b_lat.data = bollard.b_lat
    form.b_lng.data = bollard.b_lng
    return render_template('manage.html', title='Manage', bollard=bollard, form=form,
        has_map=True, init_lat=bollard.b_lat, init_lng=bollard.b_lng,
        current_url=request.url)


@bollards.route('/add', methods=['GET', 'POST'])
@login_required
def add():
    form = BollardForm()
    if form.validate_on_submit():
        if Bollard.query.filter_by(b_number=form.b_number.data, 
                            b_letter=form.b_letter.data.upper()).first():
            flash(f'Bollard No {form.b_number.data} allready exists', 'danger')
        else:
            # for fs in form.images.data:
            #    print(fs.filename)
            new_bollard = Bollard(b_number=form.b_number.data,
                                    b_letter=form.b_letter.data.upper(), 
                                    b_name=form.b_name.data,
                                    comment=form.comment.data, b_lat=form.b_lat.data,
                                    b_lng=form.b_lng.data)
            if form.main_image.data:
                # print(form.main_image.data)
                # print(form.images.data[0])
                picture_file_icon, picture_file = save_picture_bollard(form.main_image.data)
                # print(picture_file_icon)
                # print(picture_file)
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
            return redirect(url_for('bollards.list_bollards'))
    return render_template('manage.html', title='Add', form=form, has_map=True,
                init_lat=current_user.last_lat, init_lng=current_user.last_lon,
                init_zoom=current_user.last_zoom)


@bollards.route('/delete/<int:bollard_id>', methods=['POST'])
@login_required
def delete_bollard(bollard_id):
    bollard = Bollard.query.filter_by(id=bollard_id).first_or_404()
    db.session.delete(bollard)
    db.session.commit()
    flash('Bollard deleted successfully.', 'info')
    return redirect(url_for('bollards.list_bollards'))


@bollards.route('/delete/image/<int:bimage_id>/<int:bollard_id>', methods=['POST'])
@login_required
def delete_image(bimage_id, bollard_id):
    bimage = Bimage.query.filter_by(id=bimage_id).first_or_404()
    db.session.delete(bimage)
    db.session.commit()
    flash('Image deleted successfully.', 'info')
    # Todo: find a way to redirect to image section
    return redirect(url_for('bollards.manage', bollard_id=bollard_id)) 
