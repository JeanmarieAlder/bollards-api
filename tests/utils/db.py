from bollards_api import bcrypt
from flask import current_app
from bollards_api import db
from bollards_api.models import Bimage, Bollard, User

def reset_db():
    app = current_app
    with app.app_context():
        db.drop_all()
        db.create_all()

def add_default_user():
    app = current_app
    with app.app_context():
        user1 = User(username='noob', password=bcrypt.generate_password_hash('password').decode('utf-8'))
        user2 = User(username='user2', password=bcrypt.generate_password_hash('password2').decode('utf-8'))
        db.session.add(user1)
        db.session.add(user2)
        db.session.commit()

def add_default_bollards():
    app = current_app
    with app.app_context():
        bimage1 = Bimage(uri="test_bollard_1.jpeg")
        bimage2 = Bimage(uri="test_bollard_2.jpeg")
        bimage3 = Bimage(uri="test_bollard_3.jpeg")
        bimage4 = Bimage(uri="test_bollard_4.jpeg")
        bimage5 = Bimage(uri="test_bollard_5.jpeg")
        bollard1 = Bollard(
            b_number=1, 
            b_name="Test Bollard 1", 
            comment="Test comment for bollard 1.", 
            image_icon="test_bollard_icon_1.jpeg")
        bollard2 = Bollard(
            b_number=2, 
            b_name="Test Bollard 2", 
            comment="Test comment for bollard 2.", 
            image_icon="test_bollard_icon_2.jpeg")
        bollard3 = Bollard(
            b_number=3,
            image_icon="test_bollard_icon_3.jpeg",
            b_lat=46.69420,
            b_lng=6.42069)
        bollard3a = Bollard(
            b_number=3,
            b_letter="a",
            image_icon="test_bollard_icon_3.jpeg",
            b_lat=46.601,
            b_lng=6.401)

        bollard1.images.append(bimage1)
        bollard1.images.append(bimage2)
        bollard2.images.append(bimage2)
        bollard2.images.append(bimage3)
        bollard3.images.append(bimage4)
        bollard3a.images.append(bimage5)

        db.session.add(bollard1)
        db.session.add(bollard2)
        db.session.add(bollard3)
        db.session.add(bollard3a)
        db.session.commit()
