# Imports for flask
from flask import Blueprint, render_template, url_for, request, flash, redirect
# Imports for handeling sessions
from flask import session as login_session


mod = Blueprint('site', __name__, template_folder='templates')

from menuitems_controller import *
from restaurant_controller import *

# HANDLER FOR LANDING PAGE -----------------------------------------------------

print "site init running"

@mod.route('/')
def index():
    return render_template('index.html')
