"""This program routes the urls and requests to the correct handlers"""

from flask import Flask, url_for, render_template, request, flash, redirect
# Imports for dbmodels
from model.model_resturants import list_resturants, editname_resturant, delete_resturant
from model.model_menuitems import list_menu
from model.model_users import createUser, getUserInfo, getUserID

# Imports for handeling sessions
from flask import session as login_session
import random, string

#Imports the handlers
from handlers.newresturant import insertresturant, render_newresturant

from handlers.newmenuitem import insertmenuitem, render_newmenuitem
from handlers.altermenuitem import  editmenuitem, render_editmenuitem, \
                                    deletemenuitem, render_deletemenuitem
from handlers.listmenujson import listmenujson, getitemjson

# Imports for oath2
from oauth2client.client import flow_from_clientsecrets
from oauth2client.client import FlowExchangeError
import httplib2
import json
from flask import make_response
import requests

app = Flask(__name__)

# Loading client secret json and setting constants

CLIENT_ID = json.loads(
    open('client_secrets.json', 'r').read())['web']['client_id']
APPLICATION_NAME = "Restaurant Menu Application"

# ROUTES FOR RESTURANTS --------------------------------------------------------

@app.route('/resturants/new', methods=['GET', 'POST'])
def NewResturants():
    """Gets the url resturant id and handles inserting"""
    if 'username' not in login_session:
        return redirect('/login')
    if request.method == 'POST':
        return insertresturant(login_session['user_id'])
    else:
        return render_newresturant()

@app.route('/resturants')
@app.route('/resturants/<int:resturant_id>/')
def ListResturants(resturant_id=None):
    """Gets the url resturant id and lists out info on that or all resturants"""
    # First check if user is logged in
    if 'username' not in login_session:
        return render_template(
                                'publicresturants.html',
                                resturants=list_resturants(resturant_id)
                                )
    # If user is logged in we render resturants.html page with appropriate data
    else:
        r = list_resturants(resturant_id, login_session['user_id'])
        resturant = r[0]
        owner = r[1]
        print "checked resturant in db.. resturant is and user is owner?"
        print resturant
        print owner
        return render_template(
                                'resturants.html',
                                resturants=resturant,
                                owner=owner
                                )

@app.route('/resturants/<int:resturant_id>/edit')
def EditResturants(resturant_id=False):
    """Gets the url resturant id and handles editing"""
    if 'username' not in login_session:
        return redirect('/login')
    output = open("views/editresturant.html", "r")
    output = output.read().format(id=resturant_id)
    return output

@app.route('/resturants/<int:resturant_id>/delete')
def DeleteResturant(resturant_id=0):
    if 'username' not in login_session:
        return redirect('/login')
    output = open("views/deleteresturant.html", "r")
    output = output.read().format(id=resturant_id)
    return output

# CRUD FOR MENUITEMS -----------------------------------------------------------

@app.route('/resturants/<int:resturant_id>/menu/new', methods = ['GET', 'POST'])
def newmenuitem(resturant_id=False):
    if 'username' not in login_session:
        return redirect('/login')
    if request.method == 'POST':
        success = insertnewmenuitem(resturant_id, login_session['user_id'])
        if success:
            flash("New menuitem created!")
            return redirect(url_for("showmenu", resturant_id=resturant_id))
    else:
        return render_newmenuitem(resturant_id)

@app.route('/menu')
@app.route('/resturants/<int:resturant_id>/menu')
def showmenu(resturant_id=False):
    print "got request for resturantmenu"
    items = list_menu(resturant_id)
    resturant = list_resturants(resturant_id)
    return render_template('menu.html', resturant=resturant, items=items)

@app.route('/menu/<int:menuitem_id>/edit', methods = ['GET', 'POST'])
def editmenu(menuitem_id=False):
    if 'username' not in login_session:
        return redirect('/login')
    print "Got request to edit"
    print menuitem_id
    if request.method == 'POST':
        resturant_id = editmenuitem(menuitem_id)
        if resturant_id:
            flash("Menuitem edited!")
            return redirect(url_for("showmenu", resturant_id=resturant_id))
    else:
        return render_editmenuitem(menuitem_id)

@app.route('/menu/<int:menuitem_id>/delete', methods=['GET', 'POST'])
def delmenuitem(menuitem_id=False):
    if 'username' not in login_session:
        return redirect('/login')
    if request.method == 'POST':
        resturant_id = deletemenuitem(menuitem_id)
        if resturant_id:
            flash("Menuitem deleted!")
            return redirect(url_for("showmenu", resturant_id=resturant_id))
    else:
        return render_deletemenuitem(menuitem_id)

# JSON REST API ----------------------------------------------------------------

@app.route('/resturant/<int:resturant_id>/menu/json')
@app.route('/resturant/<int:resturant_id>/menu/<int:menuitem_id>/json')
def getjsondata(resturant_id=False, menuitem_id=False):
    print "got json request!"
    if menuitem_id == False:
        jsonfied = listmenujson(resturant_id)
        return jsonfied
    else:
        jsonfied = getitemjson(resturant_id, menuitem_id)
        return jsonfied

# Login ------------------------------------------------------------------------



@app.route('/gconnect', methods=['POST'])
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
        print "Token's client ID does not match app's."
        response.headers['Content-Type'] = 'application/json'
        return response

    stored_credentials = login_session.get('credentials_token')
    print "stored credentials is " + str(stored_credentials)
    stored_gplus_id = login_session.get('gplus_id')
    if stored_credentials is not None and gplus_id == stored_gplus_id:
        response = make_response(json.dumps('Current user is already connected.'),
                                 200)
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
    if  user_id == None:
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
    output += ' " style = "width: 300px; height: 300px;border-radius: 150px;-webkit-border-radius: 150px;-moz-border-radius: 150px;"> '
    flash("you are now logged in as %s" % login_session['username'])
    return output

@app.route('/gdisconnect')
def gdisconnect():
    access_token = login_session['credentials_token']
    print 'In gdisconnect access token is %s' % access_token
    print 'User name is: '
    print login_session['username']
    print 'Access token is'
    print access_token
    if access_token is None:
        print 'Access Token is None'
        response = make_response(json.dumps('Current user not connected.'), 401)
        response.headers['Content-Type'] = 'application/json'
    	return response
    print "We will disconnect by using GooglesREST API"
    url = 'https://accounts.google.com/o/oauth2/revoke?token=%s' % access_token
    headers = {"Content-type":"application/x-www-form-urlencoded"}
    print "getting %s" % url
    h = httplib2.Http()
    r = h.request(url, 'GET')[0]
    print r
    result = r
    if result['status'] == 200:
    	response = make_response(json.dumps('Successfully disconnected.'), 200)
    	response.headers['Content-Type'] = 'application/json'
    	return response
    else:
    	response = make_response(json.dumps('Failed to revoke token for given user.', 400))
    	response.headers['Content-Type'] = 'application/json'
    	return response

@app.route('/fbconnect', methods=['POST'])
def fbconnect():
    # First we check the state token
    if request.args.get('state') != login_session['state']:
        response = make_response(json.dumps('Invalid state parameter.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response
    # Next we the auth code in the request
    access_token = request.data
    # Then we upgrade the client token to a long lived server-side token
        # We start by getting our app id and app secret
    app_id = json.loads(open('fb_client_secrets.json', 'r').read())['web']['app_id']
    app_secret = json.loads(open('fb_client_secrets.json', 'r').read())['web']['app_secret']
        # Such that we can get the long lived token from fb graph api
    url = 'https://graph.facebook.com/oauth/access_token?grant_type=fb_exchange_token&client_id=%s&client_secret=%s&fb_exchange_token=%s' \
        % (app_id,app_secret,access_token)
    print url
    h = httplib2.Http()
    result = h.request(url, 'GET')[1]
    print result
    token = json.loads(result)['access_token']
    print "token is %s" % token
    # Yay! now we can get data on the user
    url = 'https://graph.facebook.com/v2.9/me?access_token=%s&fields=name,id,email,picture.width(300)' % token
    result = h.request(url, 'GET')[1]
    print "API JSON results are %s" % result
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
    if  user_id == None:
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
    output += ' " style = "width: 300px; height: 300px;border-radius: 150px;-webkit-border-radius: 150px;-moz-border-radius: 150px;"> '
    flash("you are now logged in as %s" % login_session['username'])
    return output

@app.route('/fbdisconnect')
def fbdisconnect():
    facebook_id = login_session['facebook_id']
    access_token = login_session['access_token']
    url = 'https://graph.facebook.com/%s/permissions?access_token=%s' % (facebook_id, access_token)
    print "sending delete request to %s" % url
    h = httplib2.Http()
    result = h.request(url, 'DELETE')[1]
    print ""
    print result
    return

@app.route('/disconnect')
def disconnect():
    if 'provider' in login_session:
        if login_session['provider'] == 'google':
            gdisconnect()
            del login_session['gplus_id']
            del login_session['credentials_token']
            print "ran gdisconnect function and wiped google cridentials in session"
        if login_session['provider'] == 'facebook':
            fbdisconnect()
            del login_session['facebook_id']
            print "ran fbdisconnect function and wiped fb id in session"
        del login_session['username']
    	del login_session['email']
    	del login_session['picture']
        print "Successfully logged out -------------------------------------- !!"
        flash("You have successfully logged out!")
        return redirect(url_for('ListResturants'))
    else:
        flash("You werent even logged in")
        return redirect(url_for('login'))

if __name__ == "__main__":
    app.secret_key = "my_secret_key"
    app.debug = True
    app.run(host='0.0.0.0', port = 5000)
