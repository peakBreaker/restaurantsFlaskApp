from flask import Flask, render_template

app = Flask(__name__)

# Configurations
app.config.from_object('config')

# Sample HTTP error handling
@app.errorhandler(404)
def not_found(error):
    return render_template('404.html'), 404

from app.mod_api.controller import mod as api_module
from app.mod_site import *
from app.mod_auth.controller import mod as auth_module
site_module = mod_site.mod

app.register_blueprint(site_module)
app.register_blueprint(api_module, url_prefix='/api')
app.register_blueprint(auth_module)
