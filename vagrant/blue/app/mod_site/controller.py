from flask import Blueprint, render_template, url_for

# Import module models (i.e. User)
# from app.mod_site.models import Users

# Our sample helperfunction
from app.mod_site.maths import add
from app.common.common import sayhello

print "saying hello world.."
sayhello("world")

mod = Blueprint('site', __name__)

@mod.route('/')
def homepage():
    return render_template('home/homepage.html', answer=add(2,3))
