from flask_wtf import Form
from wtforms import TextAreaField, TextField, SubmitField
from wtforms.validators import DataRequired
 
class ContactForm(Form):
  name = TextField("Name", validators=[DataRequired()])
  email = TextField("Email address", validators=[DataRequired()])
  subject = TextField("Subject", validators=[DataRequired()])
  message = TextAreaField("Your message", validators=[DataRequired()])
  submit = SubmitField("Send")