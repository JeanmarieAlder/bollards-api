from flask_wtf import FlaskForm
from flask_wtf.file import FileAllowed, FileField
from wtforms import (DecimalField, HiddenField, IntegerField,
                     MultipleFileField, StringField, SubmitField,
                     TextAreaField)
from wtforms.validators import DataRequired, Length

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
