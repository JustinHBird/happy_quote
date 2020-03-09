from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, SelectField
from wtforms.validators import DataRequired, Email
# NEEDS VALIDATION...Look into writing custom validators for phone
class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Log In')

TIME_ZONES = [
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

class RegisterForm(FlaskForm):
    first_name = StringField('First Name', validators=[DataRequired()])
    last_name = StringField('Last Name', validators=[DataRequired()])
    email = StringField('Email Address', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    # Validate passwords match
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired()])
    phone = StringField('Phone Number', validators=[DataRequired()])
    time_zone = SelectField('Time Zone', choices=[(i, " ".join(t)) for i,t in enumerate(TIME_ZONES)])
    submit = SubmitField('Register')