import datetime
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, SelectField, TimeField, TextAreaField
from wtforms.validators import DataRequired, Email, EqualTo, ValidationError
from app.models import User

class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Log In')

class RegisterForm(FlaskForm):
    TIME_ZONES = [
        ("--", "Select Time Zone", "--"),
        ("AST", "ATLANTIC STANDARD TIME", "UTC - 4"),
        ("EST", "EASTERN STANDARD TIME", "UTC - 5"),
        ("EDT", "EASTERN DAYLIGHT TIME", "UTC - 4"),
        ("CST", "CENTRAL STANDARD TIME", "UTC - 6"),
        ("CDT", "CENTRAL DAYLIGHT TIME", "UTC - 5"),
        ("MST", "MOUNTAIN STANDARD TIME", "UTC - 7"),
        ("MDT", "MOUNTAIN DAYLIGHT TIME", "UTC - 6"),
        ("PST", "PACIFIC STANDARD TIME", "UTC - 8"),
        ("PDT", "PACIFIC DAYLIGHT TIME", "UTC - 7"),
        ("AKST", "ALASKA TIME", "UTC - 9"),
        ("AKDT", "ALASKA DAYLIGHT TIME", "UTC - 8"),
        ("HST", "HAWAII STANDARD TIME", "UTC - 10"),
        ("HAST", "HAWAII-ALEUTIAN STANDARD TIME", "UTC - 10"),
        ("HADT", "HAWAII-ALEUTIAN DAYLIGHT TIME", "UTC - 9"),
        ("SST", "SAMOA STANDARD TIME", "UTC - 11"),
        ("SDT", "SAMOA DAYLIGHT TIME", "UTC - 10"),
        ("CHST", "CHAMORRO STANDARD TIME", "UTC +10"),
    ]

    first_name = StringField('First Name', validators=[DataRequired()])
    last_name = StringField('Last Name', validators=[DataRequired()])
    email = StringField('Email Address', validators=[DataRequired(), Email()])
    phone = StringField('Phone Number', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    time_zone = SelectField('Time Zone', choices=[(i, " ".join(t)) for i,t in enumerate(TIME_ZONES)], coerce=int)
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
    '''
    def time_options(self):
        times = []
        for h in range(24):
            for m in range(0, 60, 15):
                t = datetime.time(h, m)
    '''
