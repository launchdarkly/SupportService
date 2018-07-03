from flask import render_template
from app import app
import ldclient

ldclient.set_sdk_key("sdk-8929dfb7-7edd-4bec-9856-db3bd80a6661")
ld_client = ldclient.get()

@app.route('/')
@app.route('/index')
def index():
    user = {'username': 'Miguel'}
    
    showWidgets = ld_client.variation("show-widgets", {"key": "user@test.com"}, False)
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
    return render_template('index.html',title='Home', user=user,
    posts=posts, display_widgets=display_widgets)

@app.route('/sample_tickets')
def sampleTickets():
    user = {'username': 'Miguel'}
    return render_template('sampleTickets.html', title='Support Request', user=user)