import json
import logging

import ldclient
from flask import (Blueprint, current_app, flash, redirect, render_template,
                   request, url_for)
from flask_login import current_user, login_required, login_user, logout_user
from werkzeug.urls import url_parse

from app.factory import CACHE_TIMEOUT, CachingDisabled, cache, db
from app.models import User

core = Blueprint('core', __name__)

@core.route('/')
@core.route('/index')
@cache.cached(timeout=CACHE_TIMEOUT(), unless=CachingDisabled())
@login_required
def index():
    theme = request.args.get("theme")
    if theme:
        updateTheme(theme)
    
    showWidgets = ldclient.get().variation('show-widgets', current_user.get_ld_user(), False)
    
    if showWidgets:
        display_widgets = True
    else:
        display_widgets = False
        
    user = current_user.get_ld_user()
    
    all_flags = json.dumps(ldclient.get().all_flags(user))

    beta_features = ldclient.get().variation('dark-theme', user, False)
    
    set_theme = '{0}/index.html'.format(current_user.set_path)

    return render_template(set_theme, title='Home',
    display_widgets=display_widgets, all_flags=all_flags, show_beta=beta_features, user=user)


def updateTheme(theme):

    if theme == "dark":
        current_user.set_path = 'beta'
    else:
        current_user.set_path = 'default'

    db.session.commit()

@core.route('/dark')
def darkTheme():
    return render_template(set_theme, title='Dark Theme')

@core.route('/experiments')
def experiments():
    
    generate_user = User()
    user = generate_user.get_ld_user(random=True)

    all_flags = json.dumps(ldclient.get().all_flags(user))
    
    theme = request.args.get("theme")
    if theme:
        updateTheme(theme)
    
    set_theme = '{0}/exp.html'.format(current_user.set_path)

    show_nps = ldclient.get().variation('show-nps-survery', user, False)
  
    return render_template(set_theme, title='Experiments', show_nps=show_nps, user=user, all_flags=all_flags)

@core.route('/operational')
def operational():
    theme = request.args.get("theme")
    if theme:
        updateTheme(theme)
    
    set_theme = '{0}/operation.html'.format(current_user.set_path)
 
    return render_template(set_theme, title='Operational')

@core.route('/release')
def release():
    theme = request.args.get("theme")
    if theme:
        updateTheme(theme)
    
    set_theme = '{0}/release.html'.format(current_user.set_path)

    return render_template(set_theme, title='Dark Theme')

@core.route('/entitlement')
def entitlement():
    theme = request.args.get("theme")
    if theme:
        updateTheme(theme)
    
    set_theme = '{0}/entitlement.html'.format(current_user.set_path)

    return render_template(set_theme, title='entitlement')

# I decided to take out a payday loan on this shit. 
# http://flask.pocoo.org/docs/1.0/quickstart/?highlight=post#http-methods
@core.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('core.index'))
    if request.method == 'POST':
        user = User(email=request.form['userEmail'])
        # check if userName exist
        if User.query.filter_by(email = request.form['userEmail']).first() is not None:
            flash('Email is already taken. Please choose another email')
            return redirect(url_for('core.register'))
        # check if passwords match
        if request.form['inputPassword'] != request.form['confirmPassword']:
            flash('Passwords must match')
            return redirect(url_for('core.register'))
        user.set_password(request.form['inputPassword'])
        db.session.add(user)
        db.session.commit()
        flash('Congratulations, you are now a registered user!')
        return redirect(url_for('core.login'))
    return render_template('beta/auth/register.html', title='Support Request')

@core.route('/login', methods=['GET', 'POST'])
def login(theme='default'):
    if current_user.is_authenticated:
        return redirect(url_for('core.index'))
    if request.method == 'POST':
        user = User.query.filter_by(email=request.form['userEmail']).first()
        if user is None or not user.check_password(request.form['inputPassword']):
            flash('Invalid username or password')
            return redirect(url_for('core.login'))
        login_user(user)
        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('core.index')
        return redirect(next_page)
    '''

    '''
    return render_template('beta/auth/login.html', title='Sign In')

@core.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('core.index'))
