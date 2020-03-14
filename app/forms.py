import datetime
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, SelectField, TimeField, TextAreaField
from wtforms.validators import DataRequired, Email, EqualTo, ValidationError
from app.models import User, TimeZone


class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Log In')

class RegisterForm(FlaskForm):
    first_name = StringField('First Name', validators=[DataRequired()])
    last_name = StringField('Last Name', validators=[DataRequired()])
    email = StringField('Email Address', validators=[DataRequired(), Email()])
    phone = StringField('Phone Number', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    # Build timezone choices from query store ID as key
    time_zone = SelectField('Time Zone', choices=[(tz.id, f'{tz.std_name}({tz.std_abbr}) UTC{tz.std_offset}') for tz in TimeZone.query.all()], coerce=int)
    dst_active = BooleanField('Daylight Savings')
    submit = SubmitField('Register')
  
    def validate_email(self, email):
        email = User.query.filter_by(email=email.data).first()
        if email is not None:
            raise ValidationError('This email address has an account already.')
    
    #def validate_phone(self, phone):
    #    pass


class MessageForm(FlaskForm):
    process_time =  TimeField('Time', validators=[DataRequired()], format='%I:%M %p')
    message = TextAreaField('Message', validators=[DataRequired()])
    submit = SubmitField('Save')
    
