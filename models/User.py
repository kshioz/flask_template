from boto3.dynamodb.conditions import Key, Attr
from dynamodb import DynamoDB
import uuid

# Common function
from common import common as cmn

# Setup DynamoDB
dynamo = DynamoDB()

class User(object):

    TABLE_NAME = 'Users'

    def __init__(self, username, email, password):
        self.user_id    = str(uuid.uuid1())
        self.username   = username
        self.email      = email
        self.password   = password
        self.imagepath  = "0"
        self.at_created = cmn.getTime()
        self.at_updated = cmn.getTime()

    def __str__(self):
        return "User(id='%s')" % self.user_id

    def findItem(pe, fe, search_obj):

        if not pe:
            pe = "user_id, username, email, image"
        
        res = dynamo.scanAll(User.TABLE_NAME, pe, fe, search_obj)
        return res['Items']

    def getItem(user_id):

        key_obj = {"user_id": user_id}

        res = dynamo.get_item(User.TABLE_NAME, key_obj)
        return res

    def add(data):

        res = dynamo.put_item(User.TABLE_NAME, data)
        return res

    def update(key, ue, update_obj):
        
        res = dynamo.update_item(User.TABLE_NAME, 'user_id', key, ue, update_obj)
        return res

    def getObj(self):

        obj = {
            "user_id":      self.user_id,
            "username":     self.username,
            "email":        self.email,
            "password":     self.password,
            "imagepath":    self.imagepath,
            "at_created":   self.at_created,
            "at_updated":   self.at_updated
        }

        return obj
