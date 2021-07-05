from flask_wtf import FlaskForm
from flask_wtf.file import FileAllowed, FileRequired, FileField
from flask_login import current_user
from wtforms import StringField, PasswordField, SubmitField, BooleanField, MultipleFileField
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
    number = StringField('Bollard No',
                            validators=[DataRequired(), Length(min=1, max=10)])
    
    name = StringField('Name',
                            validators=[Length(max=100)])

    comment = StringField('Comment')

    main_image = FileField('Main Image', validators=[FileRequired()])

    images = MultipleFileField('Other Images')

    submit = SubmitField('Submit')
