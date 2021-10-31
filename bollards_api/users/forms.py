from bollards_api.models import User
from flask_login import current_user
from flask_wtf import FlaskForm
from flask_wtf.file import FileAllowed, FileField
from wtforms import BooleanField, PasswordField, StringField, SubmitField
from wtforms.validators import DataRequired, EqualTo, Length, ValidationError


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
            raise ValidationError('Username already taken')


class UpdateAccountForm(FlaskForm):
    username = StringField('Username',
                            validators=[DataRequired(), Length(min=3, max=25)])

    profile_pic = FileField('Profile Picture', validators=[FileAllowed(['jpg', 'jpeg', 'png'])])
    submit_account = SubmitField('Update')

    def validate_username(self, username):
        if username.data != current_user.username:
            user_exists = User.query.filter_by(username=username.data).first()
            if user_exists:
                raise ValidationError('Username already taken')


class UpdateAccountPasswordForm(FlaskForm):
    old_password = PasswordField('Old Password',
                            validators=[DataRequired(), Length(min=3, max=25)])

    new_password = PasswordField('New Password',
                            validators=[DataRequired(), Length(min=8, max=50)])
    confirm_password = PasswordField('Confirm Password',
                            validators=[DataRequired(), EqualTo('new_password')])

    submit_password = SubmitField('Update Password')
