from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, SubmitField#,EmailField,PasswordField



class AddForm(FlaskForm):

    name = StringField('Name of Employee:')
    email=StringField("E-Mail Id Of Employee")
    dbPass=StringField('Enter DBA Password')
    submit = SubmitField('Add Employee')

class DelForm(FlaskForm):

    id = IntegerField('EmployeeId of Employee To be Deleted')
    deleteOne = SubmitField('Delete')
    deleteAll = SubmitField('Delete all Employee Records ?')
