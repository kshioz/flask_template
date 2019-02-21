import boto3
import botocore.exceptions
from boto3.dynamodb.conditions import Key, Attr
import configparser
import os

# Set up AWS
filepath = os.path.abspath(os.path.dirname(__file__))+"/config.ini"
inifile = configparser.ConfigParser()
inifile.read(filepath, 'UTF-8')

aws_access_key_id = inifile.get('aws', 'aws_access_key_id')
aws_secret_access_key = inifile.get('aws', 'aws_secret_access_key')
region_name = inifile.get('aws', 'region')

class DynamoDB:

    def __init__(self):
        self.dynamodb = boto3.resource('dynamodb',
            aws_access_key_id=aws_access_key_id,
            aws_secret_access_key=aws_secret_access_key,
            region_name=region_name)

    def create_table(self, table_name):
        try:
            res = self.dynamodb.create_table(
                AttributeDefinitions = [
                    {
                        'AttributeName': 'name',
                        'AttributeType': 'S'
                    },
                ],
                TableName = table_name,
                KeySchema = [
                    {
                        'AttributeName': 'name',
                        'KeyType': 'HASH'
                    },
                ],
                ProvisionedThroughput = {
                    'ReadCapacityUnits': 1,
                    'WriteCapacityUnits': 1
                }
            )
            return res
        except botocore.exceptions.ClientError as e:
            return e.response

    def tables(self):
        try:
            res = self.dynamodb.tables.all()
            return res
        except botocore.exceptions.ClientError as e:
            return e.response

    def get_item(self, table_name, key_value):
        table = self.dynamodb.Table(table_name)
        try:
            res = table.get_item(
                 Key = key_value
            )
            return res
        except botocore.exceptions.ClientError as e:
            return e.response

    def put_item(self, table_name, save_item):
        table = self.dynamodb.Table(table_name)
        try:
            res = table.put_item(
                 Item = save_item
            )
            return res
        except botocore.exceptions.ClientError as e:
            return e.response

    def scanAll(self, table_name, pe, fe, search_obj):
        table = self.dynamodb.Table(table_name)
        try:
            res = table.scan(
                ProjectionExpression = pe,
                FilterExpression = fe,
                ExpressionAttributeValues = search_obj
            )
            
            data = {}
            data['Items'] = res['Items']

            while 'LastEvaluatedKey' in res:
                res = table.scan(
                    ProjectionExpression = pe,
                    FilterExpression = fe,
                    ExpressionAttributeValues = search_obj,
                    ExclusiveStartKey=res['LastEvaluatedKey']
                )
                data['Items'].extend(res['Items'])

            return data
        except botocore.exceptions.ClientError as e:
            return e.response

    def update_item(self, table_name, key_obj, ue, up_obj):
        table = self.dynamodb.Table(table_name)
        try:
            res = table.update_item(
                Key = key_obj,
                UpdateExpression = ue,
                ExpressionAttributeValues = up_obj,
                ReturnValues = 'UPDATED_NEW'
            )
            return res
        except botocore.exceptions.ClientError as e:
            return e.response

    def delete_item(self, table_name, key_obj, ce, del_obj):
        table = self.dynamodb.Table(table_name)
        try:
            res = table.delete_item(
                Key = key_obj,
                ConditionExpression = ce,
                ExpressionAttributeValues = del_obj
            )

            return res
        except botocore.exceptions.ClientError as e:
            return e.response
