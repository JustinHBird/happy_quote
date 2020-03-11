from flask import render_template, redirect, url_for, request, flash
from app import app, db
from app.forms import LoginForm, RegisterForm
from flask_login import current_user, login_user, logout_user, login_required
from app.models import User

@app.route('/', methods=['GET', 'POST'])
@app.route('/index', methods=['GET', 'POST'])
def index():
    if current_user.is_authenticated:
        # If the user is already authenticated go directly to their profile page behind the landing page
        return redirect(url_for('profile', current_user.id))

    
    return render_template('index.html', register_form=RegisterForm(), login_form=LoginForm())


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
        # At this point Time-zone isn't added to the user. Need to save as an offset, but need to research an approach before storing data
        user = User(first_name=form.first_name.data, last_name=form.last_name.data, phone=form.phone.data, email=form.email.data)
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


@app.route('/login', methods=['POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('profile'))

    form = LoginForm()

    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        print(user)
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password.', 'login', )
            return redirect(url_for('index'))
        login_user(user, remember=form.remember_me.data)
        return redirect(url_for('profile'))
    return redirect(url_for('index'))


@app.route('/test', methods=['POST'])
def test():
    pass

@login_required
@app.route('/profile')
def profile():
    return render_template('profile.html')