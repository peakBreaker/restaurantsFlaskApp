# Imports for flask
from flask import Blueprint, render_template, request

mod = Blueprint('site', __name__, template_folder='templates')

from menuitems_controller import *
from restaurant_controller import *

# HANDLERS FOR PUBLIC PAGES ---------------------------------------------------


@mod.route('/')
def index():
    return render_template('index.html')


@mod.route('/about')
def aboutus():
    return render_template('about.html')


@mod.route('/contact', methods=['GET', 'POST'])
def contactus():
    if request.method == 'POST':
        name = request.form['name']
        q = request.form['about']
        print "%s asked a question" % name
        print "Question is: %s" % q
        return render_template('submitted.html')
    else:
        return render_template('contact.html')
