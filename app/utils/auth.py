"Module for doing authentications for session"
# Imports for flask
from flask import flash, redirect
# Import for session
from flask import session as login_session
# Import for decorator
from functools import wraps


def valid_login_session(f):
    "Decorator for ensuring that user has a valid login session."
    @wraps(f)
    def decorated_function(*args, **kwargs):
        try:
            if 'username' not in login_session:
                flash('You need to be logged in')
                return redirect('/login')
            else:
                if login_session['provider'] == 'google' or \
                login_session['provider'] == 'facebook':
                    print "user logged in with oauth"
                else:
                    flash('Couldnt get login provider')
                    return redirect('/disconnect')
                return f(*args,**kwargs)
        except KeyError:
            flash('No login provider found - automatically disconnected session')
            return redirect("/disconnect")
    return decorated_function
