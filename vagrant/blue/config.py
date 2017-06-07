# Statement for enabling the development environment
DEBUG = True
# SERVER_NAME = 'example.com:5000'

# Define the application directory
import os
BASE_DIR = os.path.abspath(os.path.dirname(__file__))
print "filepath is: " + str(BASE_DIR)

# Define the database - we are working with
# SQLite for this example
SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(BASE_DIR, 'app.db')
DATABASE_CONNECT_OPTIONS = {}

# Application threads. A common general assumption is
# using 2 per available processor cores - to handle
# incoming requests using one and performing background
# operations using the other.
THREADS_PER_PAGE = 2
