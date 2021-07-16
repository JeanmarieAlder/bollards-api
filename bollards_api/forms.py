from flask_wtf import FlaskForm
from flask_wtf.file import FileAllowed, FileRequired, FileField
from flask_login import current_user
from wtforms import StringField, PasswordField, SubmitField, BooleanField, MultipleFileField, TextAreaField, DecimalField, HiddenField, IntegerField
from wtforms.validators import DataRequired, Length, ValidationError, EqualTo

from bollards_api.models import User

class LoginForm(FlaskForm):
    username = StringField('Username',
                            validators=[DataRequired()])
    
    password = PasswordField('Password',
                            validators=[DataRequired(), Length(min=8, max=50)])

    remember = BooleanField('Remember me')

    submit = SubmitField('Log in')


class RegisterForm(FlaskForm):
    username = StringField('Username',
                            validators=[DataRequired(), Length(min=3, max=25)])
    
    password = PasswordField('Password',
                            validators=[DataRequired(), Length(min=8, max=50)])
    confirm_password = PasswordField('Confirm Password',
                            validators=[DataRequired(), EqualTo('password')])

    secret_phrase = PasswordField('Secret',
                            validators=[DataRequired(), Length(min=8, max=255)])

    submit = SubmitField('Register')

    def validate_username(self, username):

        user_exists = User.query.filter_by(username=username.data).first()

        if user_exists:
            raise ValidationError('Username allready taken')


class UpdateAccountForm(FlaskForm):
    username = StringField('Username',
                            validators=[DataRequired(), Length(min=3, max=25)])

    profile_pic = FileField('Profile Picture', validators=[FileAllowed(['jpg', 'jpeg', 'png'])])
    submit_account = SubmitField('Update')

    def validate_username(self, username):
        if username.data != current_user.username:
            user_exists = User.query.filter_by(username=username.data).first()
            if user_exists:
                raise ValidationError('Username allready taken')


class UpdateAccountPasswordForm(FlaskForm):
    old_password = PasswordField('Old Password',
                            validators=[DataRequired(), Length(min=3, max=25)])

    new_password = PasswordField('New Password',
                            validators=[DataRequired(), Length(min=8, max=50)])
    confirm_password = PasswordField('Confirm Password',
                            validators=[DataRequired(), EqualTo('new_password')])

    submit_password = SubmitField('Update Password')


class BollardForm(FlaskForm):
    b_number = IntegerField('Bollard No',
                            validators=[DataRequired()])

    b_letter = StringField('Letter', validators=[Length(max=3)])
    
    b_name = StringField('Name',
                            validators=[Length(max=100)])

    comment = TextAreaField('Comment')

    b_lat = DecimalField('Latitude', places=8, default=46.64692)
    b_lng = DecimalField('Longitude', places=8, default=6.28342)

    main_image = FileField('Main Image', validators=[FileAllowed(['jpg', 'jpeg', 'png'])])

    images = MultipleFileField('Other Images', validators=[FileAllowed(['jpg', 'jpeg', 'png'])])

    zoom_level = HiddenField("Zoom Level", default=9)

    submit = SubmitField('Submit Bollard')
