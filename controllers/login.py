from flask import Flask, request, render_template, jsonify
from flask_bcrypt import Bcrypt
from flask_jwt_extended import (
    JWTManager, jwt_required, create_access_token,
    get_jwt_identity
)
import datetime

# Common function
from common import common as cmn

# Model
from models.User import User

# Setup Bcrypt
bcrypt = Bcrypt()

def login():

    if request.method == 'POST' and request.headers['Content-Type'] == 'application/json':

        data = request.get_json()
        email = ""
        password = ""

        if not data:
            obj = {"status": cmn.ERROR_VALUE, "message": cmn.getErr("E000001")}
            return jsonify(obj)

        if 'email' in data.keys():
            email = data['email']

        if 'password' in data.keys():
            password = data['password']

        obj = {}
        if email and password:

            pe = "user_id, password"
            fe = "email = :email"
            search_obj = {":email": email}
            user = User.findItem(pe, fe, search_obj)

            if isinstance(user, list):
                if len(user) == 1 and bcrypt.check_password_hash(user[0]['password'], password):
                    
                    user_id = user[0]['user_id']
                    
                    if res_update['ResponseMetadata']['HTTPStatusCode'] == 200:
                        expires = datetime.timedelta(days=30)
                        access_token = create_access_token(identity=user_id, expires_delta=expires)
                        obj = {"status": cmn.SUCCESS_VALUE, "user_id": user_id, "access_token": access_token}
                    else:
                        obj = {"status": cmn.ERROR_VALUE, "message": cmn.getErr("E000002")}

                else:
                    obj = {"status": cmn.ERROR_VALUE, "message": cmn.getErr("E000002")}
            else:
                obj = {"status": cmn.ERROR_VALUE, "message": cmn.getErr("E000002")}

        else:
            obj = {"status": cmn.ERROR_VALUE, "message": cmn.getErr("E000002")}

        return jsonify(obj)
