from datetime import datetime
from pytz import timezone
from flask import render_template, redirect, url_for, request, flash
from app import app, db
from app.forms import LoginForm, RegisterForm, MessageForm
from flask_login import current_user, login_user, logout_user, login_required
from app.models import User, Message
from app.time_utils import get_user_tz, is_dst, local_to_utc, utc_to_local

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

    if form.validate_on_submit():
        # Convert desired daily message process time to UTC to be stored in the Database
        tz = get_user_tz(current_user.time_zone.std_name)
        # Maybe this should be in the models.Message
        utc_process_time = convert_to_utc(form.process_time.data, tz)

        message = Message(message=form.message.data, author=current_user, process_time=utc_process_time, is_dst=is_dst(tz))
        db.session.add(message)
        db.session.commit()
        flash('Message added to database')
        return redirect(url_for('profile'))
    return render_template('profile.html', form=form)

@login_required
@app.route('/message', methods=['GET', 'POST'])
def message():
    form = MessageForm()
    if form.validate_on_submit():
        # Convert desired daily message process time to UTC to be stored in the Database
        tz = get_user_tz(current_user.time_zone.std_name)
        # Maybe this should be in the models.Message
        utc_process_time = local_to_utc(form.process_time.data, tz)

        message = Message(message=form.message.data, author=current_user, process_time=utc_process_time, is_dst=is_dst(tz))
        db.session.add(message)
        db.session.commit()
        flash('Message added to database')
        print('message added to database')
        return redirect(url_for('message'))

    # Build page:
    messages = Message.query.filter_by(user_id=current_user.id).all()


    print(messages)
    return render_template('message.html', form=form, messages=messages)

@app.template_filter(convert_time)
def convert_time(utc_time, loc_tz):
    return utc_to_local(utc_time, loc_tz)
