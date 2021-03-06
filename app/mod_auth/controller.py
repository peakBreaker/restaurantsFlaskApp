"""Has handlers for authentication using OAuth"""

# Imports for flask
from flask import Blueprint, render_template, url_for, flash, request, redirect

# Imports from models
from app.model.model_users import createUser, getUserInfo, getUserID

# Imports for oath2
from oauth2client.client import flow_from_clientsecrets
from oauth2client.client import FlowExchangeError
import httplib2
import json
from flask import make_response
import requests

# Imports for handeling sessions and login state
from flask import session as login_session
import random
import string

mod = Blueprint('auth', __name__)

CLIENT_ID = json.loads(
    open('client_secrets.json', 'r').read())['web']['client_id']
APPLICATION_NAME = "Restaurant Menu Application"

# Login -----------------------------------------------------------------------


@mod.route('/login')
def login():
    """Generates a login session and renders the login.html page"""
    # first we create a random state key and add it to the login session
    state = ''.join(random.choice(string.ascii_uppercase + string.digits)
                    for i in xrange(32))
    login_session['state'] = state
    # Next we return it for debugging purposes
    return render_template('login.html', STATE=state)

# OAuth2 Connect --------------------------------------------------------------


@mod.route('/gconnect', methods=['POST'])
def gconnect():
    """Handles the data sent by the google signin ajax"""
    # First validate state token to protect from CSRF
    if request.args.get('state') != login_session['state']:
        response = make_response(json.dumps('Invalid state parameter.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Next we get the auth code in the request
    code = request.data

    # Then we upgrade the code into the cridentials object
    try:
        oauth_flow = flow_from_clientsecrets('client_secrets.json', scope='')
        oauth_flow.redirect_uri = 'postmessage'
        credentials = oauth_flow.step2_exchange(code)
    except FlowExchangeError:
        response = make_response(
            json.dumps('Failed to upgrade the authorization code.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Next we check the validity of the token
    access_token = credentials.access_token
    url = ('https://www.googleapis.com/oauth2/v1/tokeninfo?access_token=%s'
           % access_token)
    h = httplib2.Http()
    result = json.loads(h.request(url, 'GET')[1])
    # If there was an error in the access token info, abort.
    if result.get('error') is not None:
        response = make_response(json.dumps(result.get('error')), 500)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Verify that the access token is used for the intended user.
    gplus_id = credentials.id_token['sub']
    if result['user_id'] != gplus_id:
        response = make_response(
            json.dumps("Token's user ID doesn't match given user ID."), 401)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Verify that the access token is valid for this app.
    if result['issued_to'] != CLIENT_ID:
        response = make_response(
            json.dumps("Token's client ID does not match app's."), 401)
        response.headers['Content-Type'] = 'application/json'
        return response

    stored_credentials = login_session.get('credentials_token')
    stored_gplus_id = login_session.get('gplus_id')
    if stored_credentials is not None and gplus_id == stored_gplus_id:
        response = make_response(json.dumps(
                                'Current user is already connected.'), 200)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Store the access token in the session for later use.
    login_session['credentials_token'] = credentials.access_token
    login_session['gplus_id'] = gplus_id

    # Get user data
    userinfo_url = "https://www.googleapis.com/oauth2/v1/userinfo"
    params = {'access_token': credentials.access_token, 'alt': 'json'}
    answer = requests.get(userinfo_url, params=params)
    data = answer.json()

    # Puts data into session
    login_session['provider'] = 'google'
    login_session['username'] = data['name']
    login_session['picture'] = data['picture']
    login_session['email'] = data['email']

    user_id = getUserID(login_session['email'])
    if user_id is None:
        # User is not in db -> Create user and return user_id
        user_id = createUser(login_session)
    login_session['user_id'] = user_id

    # Lastly we generate the html and set the flash msg
    output = ''
    output += '<h1>Welcome, '
    output += login_session['username']
    output += '!</h1>'
    output += '<img src="'
    output += login_session['picture']
    output += ''' " style = "width: 300px; height: 300px;border-radius:
            150px;-webkit-border-radius: 150px;-moz-border-radius: 150px;"> '''
    flash("you are now logged in as %s" % login_session['username'])
    return output


@mod.route('/fbconnect', methods=['POST'])
def fbconnect():
    """Connects using facebook OAuth"""
    # First we check the state token
    if request.args.get('state') != login_session['state']:
        response = make_response(json.dumps('Invalid state parameter.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response
    # Next we the auth code in the request
    access_token = request.data
    # Then we upgrade the client token to a long lived server-side token
    # We start by getting our app id and app secret
    app_id = json.loads(open('fb_client_secrets.json', 'r').
                        read())['web']['app_id']
    app_secret = json.loads(open('fb_client_secrets.json', 'r').
                            read())['web']['app_secret']
    # Such that we can get the long lived token from fb graph api
    url = 'https://graph.facebook.com/oauth/access_token?grant_type=fb_exchange_token&client_id=%s&client_secret=%s&fb_exchange_token=%s' \
        % (app_id, app_secret, access_token)
    h = httplib2.Http()
    result = h.request(url, 'GET')[1]
    token = json.loads(result)['access_token']
    # Yay! now we can get data on the user
    url = 'https://graph.facebook.com/v2.9/me?access_token=%s&fields=name,id,email,picture.width(300)' % token
    result = h.request(url, 'GET')[1]
    data = json.loads(result)
    # Gets the data from the request at puts it into session
    login_session['provider'] = 'facebook'
    login_session['facebook_id'] = data['id']
    login_session['username'] = data['name']
    login_session['picture'] = data['picture']['data']['url']
    login_session['email'] = data['email']

    # To properly logout we need to store the access token in session
    login_session['access_token'] = token

    # See if user exists in our db
    user_id = getUserID(login_session['email'])
    if user_id is None:
        # User is not in db -> Create user and return user_id
        user_id = createUser(login_session)
    login_session['user_id'] = user_id

    # Finally we generate the html and set the flash msg
    output = ''
    output += '<h1>Welcome, '
    output += login_session['username']
    output += '!</h1>'
    output += '<img src="'
    output += login_session['picture']
    output += ''' " style = "width: 300px; height: 300px;border-radius:
            150px;-webkit-border-radius: 150px;-moz-border-radius: 150px;"> '''
    flash("you are now logged in as %s" % login_session['username'])
    return output

# OAuth2 Disconnect -----------------------------------------------------------


@mod.route('/gdisconnect')
def gdisconnect():
    """Handler for disconnecting from google auth session"""
    access_token = login_session['credentials_token']
    if access_token is None:
        response = make_response(json.dumps('Current user not connected.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response
    url = 'https://accounts.google.com/o/oauth2/revoke?token=%s' % access_token
    headers = {"Content-type": "application/x-www-form-urlencoded"}
    h = httplib2.Http()
    r = h.request(url, 'GET')[0]
    result = r
    if result['status'] == 200:
        response = make_response(json.dumps('Successfully disconnected.'), 200)
        response.headers['Content-Type'] = 'application/json'
        return response
    else:
        response = make_response(json.dumps(
                'Failed to revoke token for given user.', 400))
        response.headers['Content-Type'] = 'application/json'
        return response


@mod.route('/fbdisconnect')
def fbdisconnect():
    """Handler for disconnecting from fb auth session"""
    facebook_id = login_session['facebook_id']
    access_token = login_session['access_token']
    url = 'https://graph.facebook.com/%s/permissions?access_token=%s' % \
        (facebook_id, access_token)
    h = httplib2.Http()
    h.request(url, 'DELETE')[1]
    return


@mod.route('/disconnect')
def disconnect():
    """Wrapper to disconnect independent of OAuth provider"""
    if 'provider' in login_session:
        if login_session['provider'] == 'google':
            gdisconnect()
            del login_session['gplus_id']
            del login_session['credentials_token']
        if login_session['provider'] == 'facebook':
            fbdisconnect()
            del login_session['facebook_id']
        del login_session['username']
        del login_session['email']
        del login_session['picture']
        del login_session['provider']
        flash("You have successfully logged out!")
        return redirect(url_for('site.show_restaurants'))
    else:
        flash("You werent even logged in")
        return redirect(url_for('auth.login'))
