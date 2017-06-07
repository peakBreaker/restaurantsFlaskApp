from Flask

@app.route('/login')
def login():
    """Generates a login session and renders the login.html page"""
    # first we create a random state key and add it to the login session
    state = ''.join(random.choice(string.ascii_uppercase + string.digits) \
                    for i in xrange(32))
    login_session['state'] = state
    # Next we return it for debugging purposes
    return render_template('login.html', STATE=state)
