from flask import Flask, request, jsonify
from flask_bcrypt import Bcrypt
from flask_jwt_extended import get_jwt_identity

# Common function
from common import common as cmn

# Model
from models.User import User

# Setup Bcrypt
bcrypt = Bcrypt()


def checkUserData(data, edit_flg):

    err_list = []
    if 'username' not in data.keys() or not data['username']:
        err_list.append("username")
    if edit_flg == 0: # only signup
        if 'password' not in data.keys() or not data['password']:
            err_list.append("password")
        if 'password_confirm' not in data.keys() or not data['password_confirm']:
            err_list.append("confirm password")

    if len(err_list) > 0:
        msg = cmn.getErr("E000002") + ":" + ','.join(err_list)
        obj = {"status": cmn.ERROR_VALUE, "message": msg}
        return obj

    # check each item length.
    for value in data.keys():
        if value == "username":
            if len(data["username"]) > 20:
                obj = {"status": cmn.ERROR_VALUE, "message": "XXXX"}
                return obj
        if value == "password":
            if len(data["password"]) < 10:
                obj = {"status": cmn.ERROR_VALUE, "message": "XXXX"}
                return obj
        if value == "password_confirm":
            if len(data["password_confirm"]) < 10:
                obj = {"status": cmn.ERROR_VALUE, "message": "XXXX"}
                return obj

    obj = {"status": cmn.SUCCESS_VALUE}
    return obj


def signup():

    if request.method == 'POST' and request.headers['Content-Type'] == 'application/json':
        
        data = request.get_json()
        if not data:
            obj = {"status": cmn.ERROR_VALUE, "message": cmn.getErr("E000001")}
            return jsonify(obj)

        check_obj = checkUserData(data, 0)
        if check_obj['status'] == 0:
            return jsonify(check_obj)

        save_data = {
            'username': data['username'].strip(),
            'email':    data['email'].strip(),
            'password': bcrypt.generate_password_hash(data['password'].strip()).decode('utf-8')
        }

        # check email is unique.
        pe = "user_id"
        fe = "email = :email"
        search_obj = {":email": data['email']}
        user_list = User.findItem(pe, fe, search_obj)
        if isinstance(user_list, list):
            if len(user_list) != 0:
                obj = {"status": cmn.ERROR_VALUE, "message": cmn.getErr("E120001")}
                return jsonify(obj)
        else:
            obj = {"status": cmn.ERROR_VALUE, "message": cmn.getErr("E000002")}
            return jsonify(obj)
        
        # save user data.
        user = User(save_data['username'], save_data['email'], save_data['password'])
        save_user = user.getObj()
        res = User.add(save_user)
        
        obj = {}
        if res['ResponseMetadata']['HTTPStatusCode'] == 200:
            obj = {"status": cmn.SUCCESS_VALUE}
        else:
            obj = {"status": cmn.ERROR_VALUE, "message": cmn.getErr("E000002")}

        return jsonify(obj)


def editUser():
    
    if request.method == 'POST':
        
        user_id = get_jwt_identity()
        data = request.form

        if not data:
            obj = {"status": cmn.ERROR_VALUE, "message": cmn.getErr("E000001")}
            return jsonify(obj)

        check_obj = checkUserData(data, 1)
        if check_obj['status'] == 0:
            return jsonify(check_obj)

        ue = "set username=:un,at_updated=:uptime"
        update_obj = {
            ":un": data['username'].strip(),
            ":uptime": cmn.getTime()
        }

        """
        add logic if user image is changed.
        """

        res = User.update(user_id, ue, update_obj)
        
        obj = {}
        if res['ResponseMetadata']['HTTPStatusCode'] == 200:
            obj = {"status": cmn.SUCCESS_VALUE}
        else:
            obj = {"status": cmn.ERROR_VALUE, "message": cmn.getErr("E000002")}

        return jsonify(obj)


def changeEmail():

    if request.method == 'POST' and request.headers['Content-Type'] == 'application/json':
        
        data = request.get_json()
        if not data:
            obj = {"status": cmn.ERROR_VALUE, "message": cmn.getErr("E000001")}
            return jsonify(obj)

        """
        add logic change user email.
        """

        obj = {}
        return jsonify(obj)
