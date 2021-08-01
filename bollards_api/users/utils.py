import os
import secrets

from flask import current_app
from PIL import Image

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
    picture_path = os.path.join(current_app.root_path, 'static', 'img', 
                                    folder_path, picture_filename)
    i = Image.open(new_picture)
    i.save(picture_path)
    return picture_filename


def crop_save_picture(new_picture, folder_path, fixed_square_size):
    random_hex = secrets.token_hex(8)
    _, file_ext = os.path.splitext(new_picture.filename)
    picture_filename = random_hex + file_ext
    picture_path = os.path.join(current_app.root_path, 'static', 'img', 
                                    folder_path, picture_filename)
    output_size = (fixed_square_size, fixed_square_size)
    i = Image.open(new_picture)

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
