from flask_wtf import Form
from wtforms.fields import StringField, SubmitField, SelectField
from wtforms.validators import Required


class LoginForm(Form):
    """Accepts a nickname and a room."""
    name = StringField('Name', validators=[Required()])
    room = StringField('Room')
    gender = SelectField( 'gender',choices=[('male','male'),('female','female')])
    submit = SubmitField('Enter Chatroom')
