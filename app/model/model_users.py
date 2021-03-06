"""Contains functions for doing CRUD on the MenuItems table"""

from restaurants import Base, Users
from makesession import makesession

session = makesession(Base)
# User Helper Functions -------------------------------------------------------


def createUser(login_session):
    """Creates a new user row in the db and returns the user.id created"""
    newUser = Users(name=login_session['username'], email=login_session[
                   'email'], picture=login_session['picture'])
    session.add(newUser)
    session.commit()
    print "created user with email: " + login_session['email']
    user = session.query(Users).filter_by(email=login_session['email']).one()
    return user.id


def getUserInfo(user_id):
    """Gets user object with given user_id"""
    user = session.query(Users).filter_by(id=user_id).one()
    return user


def getUserID(email):
    """Gets user.id by quering with email"""
    try:
        user = session.query(Users).filter_by(email=email).one()
        return user.id
    except:
        return None
