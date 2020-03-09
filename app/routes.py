from flask import render_template, redirect, url_for, request
from app import app
from app.forms import LoginForm, RegisterForm

@app.route('/', methods=['GET', 'POST'])
@app.route('/index', methods=['GET', 'POST'])
def index():

    #if request.method == 'GET':

    form_register = RegisterForm()
    form_login = LoginForm()
    return render_template('index.html', form_register=form_register, form_login=form_login)

@app.route('/login', methods=['GET', 'POST'])
def login():
    
    form = LoginForm()
    return render_template('login.html', title='Log In', form=form)

@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    return render_template('register.html', title='Register', form=form)