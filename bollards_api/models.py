from datetime import datetime
from bollards_api import db, login_manager
from flask_login import UserMixin

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(25), unique=True, nullable=False)
    password = db.Column(db.String(100), nullable=False)
    profile_pic = db.Column(db.String(25), nullable=False, default='default_profile.jpeg')
    date_created = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    def __repr__(self):
        return f"User('{self.username}')"

class Bollard(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    number = db.Column(db.String(10), unique=True, nullable=False)
    b_name = db.Column(db.String(50))
    comment = db.Column(db.Text())
    image_icon = db.Column(db.String(25), nullable=False, default='default_bollard.jpeg')
    main_image = db.Column(db.String(25), nullable=False, default='default_bollard.jpeg')
    date_created = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    date_updated = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    def __repr__(self):
        return f"Bollard('{self.number}', '{self.b_name}', '{self.comment}', '{self.image_icon}', '{self.main_image}')"