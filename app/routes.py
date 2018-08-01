from flask import render_template, request, redirect, url_for, flash
from app import app, db
import ldclient
import json
import os
from flask_login import current_user, login_user, login_required, logout_user
from app.models import User
from werkzeug.urls import url_parse

ldclient.set_sdk_key(os.getenv("LD_CLIENT_KEY"))
#ldclient.set_config(ldclient.Config(sdk_key='sdk-8929dfb7-7edd-4bec-9856-db3bd80a6661', stream_uri="18.236.106.41:8030"))
ld_client = ldclient.get()

@app.route('/')
@app.route('/index')
@login_required
def index():
    
    user = {
            'key': 'user@test.com',
            "custom": {
                'account_type': 'Standard',
                'user_type': 'Beta_tester',
                'state': 'Ca',
                'theme': 'dark',
            },
            "privateAttributes": ["account_type", "state"],
        }
    

    showWidgets = ld_client.variation("show-widgets", user, False)
    if showWidgets:
        display_widgets = True
    else:
        display_widgets = False
        
    """
    showWidgets = ld_client.variation("switch-feature", {"key": "user@test.com"}, False)
    if showWidgets == 'Red':
        display_widgets = 'Red'
    elif showWidgets == 'Blue':
        display_widgets = 'Blue'
    elif showWidgets == 'Green':
        display_widgets = 'Green'
    """
    
    darkTheme = ld_client.variation("dark-theme", user, False)
    
    all_flags = json.dumps(ld_client.all_flags(user))

    posts = [
        {
            'author': {'username': 'Feature Flag Off'},
            'body': 'Beautiful day in Portland!'
        },
        {
            'author': {'username': 'Susan'},
            'body': 'The avengers movie was great!'
        },        
    ]
    if darkTheme:
        return render_template('index_dark.html', title='Home', user=user,
        posts=posts, display_widgets=display_widgets, all_flags=all_flags)
    else:
        return render_template('index_light.html',title='Home', user=user,
        posts=posts, display_widgets=display_widgets, all_flags=all_flags)

@app.route('/dark')
def darkTheme():
    return render_template('index_dark.html', title='Dark Theme')

# I decided to take out a payday loan on this shit. 
# http://flask.pocoo.org/docs/1.0/quickstart/?highlight=post#http-methods
@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    if request.method == 'POST':
        user = User(email=request.form['userEmail'])
        # check if userName exist
        if User.query.filter_by(email = request.form['userEmail']).first() is not None:
            flash('Email is already taken. Please choose another email')
            return redirect(url_for('register'))
        # check if passwords match
        if request.form['inputPassword'] != request.form['confirmPassword']:
            flash('Passwords must match')
            return redirect(url_for('register'))
        user.set_password(request.form['inputPassword'])
        db.session.add(user)
        db.session.commit()
        flash('Congratulations, you are now a registered user!')
        return redirect(url_for('login'))
    return render_template('auth/register.html', title='Support Request')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    if request.method == 'POST':
        user = User.query.filter_by(email=request.form['userEmail']).first()
        if user is None or not user.check_password(request.form['inputPassword']):
            flash('Invalid username or password')
            return redirect(url_for('login'))
        login_user(user)
        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('index')
        return redirect(next_page)
    return render_template('login.html', title='Sign In')

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))