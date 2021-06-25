from flask_wtf import FlaskForm
from flask_wtf.file import FileRequired
from wtforms import StringField, PasswordField, SubmitField, BooleanField, FileField, MultipleFileField
from wtforms.validators import DataRequired, Length

class LoginForm(FlaskForm):
    username = StringField('Username',
                            validators=[DataRequired(), Length(min=3, max=25)])
    
    password = PasswordField('Password',
                            validators=[DataRequired(), Length(min=8, max=50)])

    remember = BooleanField('Remember me')

    submit = SubmitField('Log in')


class BollardForm(FlaskForm):
    number = StringField('Bollard No',
                            validators=[DataRequired(), Length(min=1, max=10)])
    
    name = StringField('Name',
                            validators=[Length(max=50)])

    comment = StringField('Comment')

    main_image = FileField('Main Image', validators=[FileRequired()])

    images = MultipleFileField('Other Images')

    submit = SubmitField('Submit')
