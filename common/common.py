from flask import render_template
from datetime import datetime
from dateutil.relativedelta import relativedelta
from werkzeug import secure_filename
import pytz
import json
import os
import configparser
import boto3


# read config file
filepath = os.path.abspath(os.path.dirname(__file__))+"/../config.ini"
inifile = configparser.ConfigParser()
inifile.read(filepath, 'UTF-8')

# read error.json
filepath = os.path.abspath(os.path.dirname(__file__))+"/error.json"
f = open(filepath, 'r', encoding='utf-8')
json_data = json.load(f)

# set timezone
timezone = pytz.timezone("Asia/Tokyo")

# init S3
"""
BUCKET_NAME = inifile.get('aws', 'bucket_name')
AWS_ACCESS_KEY_ID = inifile.get('aws', 'aws_access_key_id')
AWS_SECRET_ACCESS_KEY = inifile.get('aws', 'aws_secret_access_key')

session = boto3.Session(
    aws_access_key_id=AWS_ACCESS_KEY_ID,
    aws_secret_access_key=AWS_SECRET_ACCESS_KEY
)
s3 = session.resource('s3')
"""

# file extensions
#ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'gif', 'PNG', 'JPG', 'JPEG', 'GIF'])

# SES setting
SES_REGION_NAME = inifile.get('aws', 'ses_region')
SENDER_ADDRESS = inifile.get('mail', 'sender_address')

# ERROR & SUCCESS Code
ERROR_VALUE = 0
SUCCESS_VALUE = 1


def getTime():
	utc_now = pytz.utc.localize(datetime.utcnow())
	pst_now = utc_now.astimezone(timezone)
	return pst_now.strftime("%Y/%m/%d %H:%M:%S %Z")

def getErr(err_id):
	return json_data[err_id]

def getIniFile():
    return inifile

def sortByCreated(sort_list):
    sort_list.sort(key=lambda x: x["at_created"], reverse=True)
    return sort_list

# send email by SES.
def sendEmail(recipients, sender=None, subject='', text=''):

    if not sender:
        return False

    obj = {}
    try:
        content = render_template('mail/sample.txt', message=text)
        response = ses.send_email(
            Source=sender,
            Destination={'ToAddresses': recipients},
            Message={
                'Subject': {'Data': subject},
                'Body': {
                    'Text': {'Data': content}
                }
            }
        )
    except ClientError as e:
        obj = {"status": 0, "message": e.response['Error']['Message']}
    else:
        obj = {"status": 1}

    return obj
