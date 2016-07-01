from __future__ import print_function

import boto3
import json
import requests
from conf import google_conf

print('Loading function')


def oauth_callback(event, context):
    dynamo_table = boto3.resource('dynamodb').Table('DekkiSpekkiDemo')
    code = event['code']  # Param passed from URL

    # Exchange access_token with code
    token_req = requests.post(google_conf['token_api'], data={
        'code': code,
        'client_id': google_conf['client_id'],
        'client_secret': google_conf['client_secret'],
        'redirect_uri': google_conf['redirect_uri'],
        'grant_type': 'authorization_code',
    })

    token_rslt = token_req.json()
    dynamo_rcd = token_rslt

    # Get user profile info
    user_profile_req = requests.get(google_conf['me_api'], params={
        'access_token': token_rslt['access_token']
    })

    user_profile = user_profile_req.json()

    try:
        dynamo_rcd['displayName'] = user_profile.get('displayName', '')
        dynamo_rcd['email'] = user_profile['emails'][0]['value']
    except KeyError:
        print('KeyError')

    # Upsert record
    dynamo_table.update_item(
        Key={'email': dynamo_rcd['email']},
        UpdateExpression='SET displayName = :displayName, access_token = :atoken, id_token = :id_token',
        ExpressionAttributeValues={
            ':displayName': dynamo_rcd['displayName'],
            ':atoken': dynamo_rcd['access_token'],
            ':id_token': dynamo_rcd['id_token'],
        }
    )

    rcd = dynamo_table.get_item(
        Key={'email': dynamo_rcd['email']},
    )

    return rcd

