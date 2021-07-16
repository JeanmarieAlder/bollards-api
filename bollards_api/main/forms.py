from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField
from wtforms.validators import DataRequired, EqualTo, Length


class ContactForm(FlaskForm):
    contact_name = StringField('Username',
                            validators=[DataRequired()])
    
    contact_email = StringField('Password',
                            validators=[DataRequired(), Length(min=8, max=50)])

    contact_message = TextAreaField('Message')

    secret_word = StringField("""
        Hey, robots are not welcomed here. 
        Would you please kindly write "norobots" in the field below. Thanks
    """, validators=[EqualTo('norobots')])

    submit = SubmitField('Submit')
