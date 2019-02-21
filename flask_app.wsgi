#flask_app.wsgi
import os,sys

sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))

from myapp import app as application
