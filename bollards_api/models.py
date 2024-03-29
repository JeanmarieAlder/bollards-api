from datetime import datetime, timezone

from bollards_api import db, login_manager
from flask_login import UserMixin

@login_manager.user_loader
def load_user(user_id):
    # return User.query.get(int(user_id))
    return db.session.get(User, int(user_id))

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(25), unique=True, nullable=False)
    password = db.Column(db.String(100), nullable=False)
    profile_pic = db.Column(db.String(25), nullable=False, default='default_profile.jpeg')

    last_lat = db.Column(db.Numeric(8,5), nullable=False, default=46.64692)
    last_lon = db.Column(db.Numeric(8,5), nullable=False, default=6.28342)
    last_zoom = db.Column(db.Integer, nullable=False, default=9)

    date_created = db.Column(db.DateTime, nullable=False, default=datetime.now(timezone.utc))
    date_modified = db.Column(db.DateTime, nullable=False, default=datetime.now(timezone.utc))

    def __repr__(self):
        return f"User('{self.username}')"


class Bollard(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    b_number = db.Column(db.Integer, nullable=False)
    b_letter = db.Column(db.String(3), default="")
    b_type = db.Column(db.String(50), default="Forest")
    b_name = db.Column(db.String(50), default="")
    comment = db.Column(db.Text(), default="")
    b_lat = db.Column(db.Numeric(8,5), nullable=False, default=46.64692)
    b_lng = db.Column(db.Numeric(8,5), nullable=False, default=6.28342)
    b_easting = db.Column(db.Numeric(9,1), nullable=True, default=2511562.9)
    b_northing = db.Column(db.Numeric(9,1), nullable=True, default=1166839.3)
    b_height = db.Column(db.Integer, nullable=True)
    image_icon = db.Column(db.String(25), nullable=False, default='default_bollard.jpeg')
    images = db.relationship("Bimage", backref='bollard', lazy=True,
            cascade="all, delete-orphan")
    informations = db.relationship("Information", backref='bollard', 
            lazy=True, cascade="all, delete-orphan")

    date_created = db.Column(db.DateTime, nullable=False, default=datetime.now(timezone.utc))
    date_updated = db.Column(db.DateTime, nullable=False, default=datetime.now(timezone.utc))

    def __repr__(self):
        return f"Bollard('{self.b_number}', '{self.b_name}', '{self.comment}', '{self.image_icon}')"


class Bimage(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    uri = db.Column(db.String(25), nullable=False, default='default_bollard.jpeg')
    bollard_id = db.Column(db.Integer, db.ForeignKey('bollard.id'))

    def __repr__(self):
        return f"Bimage('{self.uri}', '{self.bollard_id}')"


class Information(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    information = db.Column(db.String(100), nullable=False, default='default_bollard.jpeg')
    bollard_id = db.Column(db.Integer, db.ForeignKey('bollard.id'))

    def __repr__(self):
        return f"Information('{self.information}', '{self.bollard_id}')"