from flask import render_template, request, redirect, url_for, flash
from app import app, db,ld_client
import json
from flask_login import current_user, login_user, login_required, logout_user
from app.models import User
from werkzeug.urls import url_parse

@app.route('/')
@app.route('/index')
@login_required
def index():

    showWidgets = ld_client.variation('show-widgets', current_user.get_ld_user(), False)
    
    if showWidgets:
        display_widgets = True
    else:
        display_widgets = False
        
    '''
    showWidgets = ld_client.variation("switch-feature", {'key': 'user@test.com'}, False)
    if showWidgets == 'Red':
        display_widgets = 'Red'
    elif showWidgets == 'Blue':
        display_widgets = 'Blue'
    elif showWidgets == 'Green':
        display_widgets = 'Green'
    ''' 
    all_flags = json.dumps(ld_client.all_flags(current_user.get_ld_user()))

    beta_features = ld_client.variation('dark-theme', current_user.get_ld_user(), False)
    
    print('here is the value of set_path: ' + current_user.set_path)
    set_theme = '{0}/index.html'.format(current_user.set_path)

    return render_template(set_theme, title='Home',
    display_widgets=display_widgets, all_flags=all_flags, show_beta=beta_features)

@app.route('/updateTheme')
def updateTheme():
    if current_user.set_path == 'default':
        current_user.set_path ='beta'
        print(current_user.set_path)
    else:
        current_user.set_path = 'default'
    db.session.commit()
    return redirect(url_for('index'))

@app.route('/dark')
def darkTheme():
    return render_template(set_theme, title='Dark Theme')

@app.route('/experiments')
def experiments():
    return render_template('default/exp.html', title='Experiments')

@app.route('/operational')
def operational():
    return render_template('default/operation.html', title='Operational')

@app.route('/release')
def release():
    return render_template('default/release.html', title='Dark Theme')

@app.route('/entitlement')
def entitlement():
    return render_template('default/entitlement.html', title='entitlement')

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