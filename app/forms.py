from wtforms.fields import BooleanField, DateField, StringField, SubmitField, TextAreaField, TimeField
from wtforms.validators import DataRequired
from flask_wtf import FlaskForm

class AppointmentForm(FlaskForm):
  name = StringField('Name', validators=[DataRequired()])
  start_date = DateField('Start Date', validators=[DataRequired()])
  start_time = TimeField('Start Time', validators=[DataRequired()])
  end_date = DateField('End Date', validators=[DataRequired()])
  end_time = TimeField('End Time', validators=[DataRequired()])
  description = TextAreaField('Description', validators=[DataRequired()])
  private = BooleanField('Private', validators=[DataRequired()])
  submit = SubmitField('Create an appointment')
