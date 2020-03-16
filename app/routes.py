from flask import render_template, redirect, url_for, request, flash
from app import app, db
from app.forms import LoginForm, RegisterForm, MessageForm
from flask_login import current_user, login_user, logout_user, login_required
from app.models import User, Message
from app.time_utils import get_user_tz_obj

@app.route('/', methods=['GET', 'POST'])
@app.route('/index', methods=['GET', 'POST'])
def index():
    # If the user is already authenticated go directly to their profile page behind the landing page
    if current_user.is_authenticated:
        return redirect(url_for('profile'))

    return render_template('index.html', register_form=RegisterForm(), login_form=LoginForm())


@app.route('/login', methods=['POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('profile'))

    form = LoginForm()

    if form.validate_on_submit():
        # Validate login form input
        user = User.query.filter_by(email=form.email.data).first()
        
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password.', 'login', )
            return redirect(url_for('index'))
        
        # Login user with Flask-Login
        login_user(user, remember=form.remember_me.data)

        return redirect(url_for('profile'))
    return redirect(url_for('index'))


@app.route('/register', methods=['POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('profile'))

    form = RegisterForm()
    # Debugging
    # print(request.form.to_dict())
    #print(form.is_submitted(), form.validate(), form.errors)
    if not form.validate_on_submit():
        for error_message in form.errors.values():
            flash(error_message[0], "register-error")

    if form.validate_on_submit():
        print('validating registration')
        user = User(first_name=form.first_name.data, last_name=form.last_name.data, phone=form.phone.data, email=form.email.data, time_zone_id=form.time_zone.data, dst_active=form.dst_active.data)
        print(user)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Congratulations, you are now a registered user!', "register-success")
        return redirect(url_for('index'))
    return redirect(url_for('index'))


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))


@login_required
@app.route('/profile', methods=['GET', 'POST'])
def profile():
    form = MessageForm()
    print(request.form.to_dict())
    print(form.is_submitted(), form.validate(), form.errors)

    if form.validate_on_submit():
        print('validating message')
        message = Message(message=form.message.data, author=current_user)

        user_tzinfo = get_user_tz_obj(current_user)
        # Create aware time object with user timezone info.
        process_time = form.process_time.data.replace(tzinfo= user_tzinfo)
        
        # coerce to utc time object
        utc_process_time = process_time + user_tzinfo.utcoffset()
        #print(process_time + datetime.timedelta(hours=-8))
        #utc_process_time = process_time 
        # submit utc time to db

        return redirect('profile')
    return render_template('profile.html', form=form)
