from flask import Flask, request, render_template, jsonify

from flask_jwt_extended import JWTManager, jwt_required, get_jwt_identity

# Controller
from controllers import login as lg
from controllers import user

# Common function
from common import common as cmn

import json

app = Flask(__name__)

## Setup for Flask-JWT-Extended extension
# 10MB: max image size for upload.
app.config['MAX_CONTENT_LENGTH'] = 10 * 1024 * 1024
app.config['JWT_SECRET_KEY'] = 'xxxxxxxxxxxxxxxxx'
jwt = JWTManager(app)

# user login
@app.route('/login', methods=['POST'])
def login():
    return lg.login()

# user signup
@app.route('/signup', methods=['POST'])
def signup():
    return user.signup()

# change email
"""
@app.route('/change_email', methods=['POST'])
@jwt_required
def changeEmail():
    return user.changeEmail()
"""

if __name__ == '__main__':
    app.run(use_reloader=True, host='0.0.0.0', port=80)
