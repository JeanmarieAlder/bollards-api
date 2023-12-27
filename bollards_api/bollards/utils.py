import os
import secrets
import requests

from flask import current_app
from PIL import Image


def get_swiss_coordinates(lat, lng):
    url = f"https://geodesy.geo.admin.ch/reframe/navref?format=json&easting={lng}&northing={lat}&altitude=NaN&input=etrf93-ed&output=lv95"
    try:
        res = requests.get(url).json()
        return res["easting"], res["northing"]
    except:
        #Default value if api doesn't reply
        #Check bollards-scripts if you need to add them later
        return 0, 0


def get_height_from_coordinates(easting, northing):
    url = f"https://api3.geo.admin.ch/rest/services/height?easting={easting}&elevation_model=COMB&northing={northing}&sr=2056"
    try:
        res = requests.get(url).json()
        return int(float(res["height"]))
    except:
        #Default value if api doesn't reply
        return 0


def crop_center(pil_img, crop_width, crop_height):
    img_width, img_height = pil_img.size
    return pil_img.crop(((img_width - crop_width) // 2,
                         (img_height - crop_height) // 2,
                         (img_width + crop_width) // 2,
                         (img_height + crop_height) // 2))


def crop_max_square(pil_img):
    return crop_center(pil_img, min(pil_img.size), min(pil_img.size))


def crop_save_icon_bollard(new_picture, folder_path, fixed_square_size):
    random_hex = secrets.token_hex(8)
    _, file_ext = os.path.splitext(new_picture.filename)
    picture_filename = random_hex + file_ext
    picture_path = os.path.join(current_app.root_path, 'static', 'img', 
                                    folder_path, picture_filename)
    output_size = (fixed_square_size, fixed_square_size)
    i = Image.open(new_picture)

    # Crop image to square
    # print(str(i.width) + " " + str(i.height))
    i_width = i.width
    i_height = i.height
    if i_width > fixed_square_size and i_height > fixed_square_size:
        i = crop_max_square(i)
        
    # Reduce the size of picture
    i.thumbnail(output_size, Image.LANCZOS)

    i.save(picture_path)
    return picture_filename


def crop_save_picture_bollard(new_picture, folder_path):
    MAX_SIZE = 2560
    random_hex = secrets.token_hex(8)
    _, file_ext = os.path.splitext(new_picture.filename)
    picture_filename = random_hex + file_ext
    picture_path = os.path.join(current_app.root_path, 'static', 'img', 
                                    folder_path, picture_filename)
    i = Image.open(new_picture)
    i_width = i.width
    i_height = i.height
    if i_width > MAX_SIZE or i_height > MAX_SIZE:
        if(i_width >= i_height):
            new_width = MAX_SIZE
            new_height = (MAX_SIZE * i_height) // i_width
        else:
            new_height = MAX_SIZE
            new_width = (MAX_SIZE * i_width) // i_height
        output_size = (new_width, new_height)
        # Reduce the size of picture
        i.thumbnail(output_size, Image.LANCZOS)

    i.save(picture_path)
    return picture_filename


# Saves the icon format as well as the full picture
def save_picture_bollard(new_picture):
    fixed_square_size = 250
    folder_path_icon = 'bollards_icon'
    folder_path = 'bollards'
    return crop_save_icon_bollard(new_picture, folder_path_icon, fixed_square_size), crop_save_picture_bollard(new_picture, folder_path)
