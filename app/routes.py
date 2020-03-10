from flask import render_template, redirect, url_for, request, flash
from app import app
from app.forms import LoginForm, RegisterForm
from flask_login import current_user, login_user, logout_user, login_required
from app.models import User

@app.route('/', methods=['GET', 'POST'])
@app.route('/index', methods=['GET', 'POST'])
def index():
    # REGISTRARION FORM VALIDATION ISSUES!

    if current_user.is_authenticated:
        # If the user is already authenticated go directly to their profile page behind the landing page
        return redirect(url_for('profile', current_user.id))
        pass

    form_register = RegisterForm()
    form_login = LoginForm()
    
    # Form processing
    print(f'validating {form_register}')
    if form_register.validate_on_submit():
        print('passing')
       
   
    return render_template('index.html', form_register=form_register, form_login=form_login)

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))


@app.route('/login', methods=['GET', 'POST'])
def login():
    
    if current_user.is_authenticated:
        return redirect(url_for('profile'))

    form = LoginForm()
    if form.validate_on_submit():
        print('in')
        user = User.query.filter_by(email=form.email.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password.')
            print('invalid')
            return redirect(url_for('index'))
        login_user(user, remember=form.remember_me.data)
        return redirect(url_for('profile'))
    return redirect(url_for('index'))

@app.route('/register', methods=['POST'])
def register():
    print('in reg')
    form = RegisterForm()

    if current_user.is_authenticated:
        print('triggered')
        return redirect(url_for('profile'))

    
    print(f'{form.first_name.data}')
    if form.validate_on_submit():
        print('creating user')
        user = User(first_name=form.first_name.data, last_name=form.last_name.data, phone=form.phone.data, email=form.email.data, time_zone=form.time_zone.data)
        user.set_password(form.password.data)
        return redirect(url_for('index'))
    return redirect(url_for('index'))

    

@login_required
@app.route('/profile')
def profile():
    return render_template('profile.html')