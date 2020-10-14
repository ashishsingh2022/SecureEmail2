from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, SubmitField,TextAreaField,FileField
from wtforms.validators import DataRequired, Email





class Subject_and_Body(FlaskForm):
    subject = StringField('Subject', validators=[DataRequired()])
    body= TextAreaField('Email Body')
    next=SubmitField("Next")

class Files(FlaskForm):
    file=FileField('Click Here To Upload The Files')
    deleteAll=SubmitField('Click here to remove all selected files')
    next=SubmitField('Next')

class sendingForm(FlaskForm):
    send = SubmitField('Send')
    cancel=SubmitField('Cancel and Discard')
