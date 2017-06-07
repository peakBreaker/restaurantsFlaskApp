from flask import Flask, render_template

app = Flask(__name__)

# Import SQLAlchemy
#from flask.ext.sqlalchemy import SQLAlchemy

# Configurations
app.config.from_object('config')

# Define the database object which is imported
# by modules and controllers
#db = SQLAlchemy(app)

# Sample HTTP error handling
@app.errorhandler(404)
def not_found(error):
    return render_template('404.html'), 404

from app.mod_api.controller import mod as api_module
from app.mod_site.controller import mod as site_module

app.register_blueprint(site_module)
app.register_blueprint(api_module, url_prefix='/api')
