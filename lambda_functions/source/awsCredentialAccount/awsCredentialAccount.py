########################################################################
# Copyright NetApp, Inc. or its affiliates. All Rights Reserved.
# SPDX-License-Identifier: MIT-0
########################################################################

import json
import base64
import boto3
import urllib.request
import urllib.parse
import threading
import logging

logger = logging.getLogger()
logger.setLevel(logging.INFO)

def lambda_handler(event, context):
    response = None
    timer = threading.Timer((context.get_remaining_time_in_millis() / 1000.00) - 0.5, timeout, args=[event, context])
    timer.start()
    try:
        if event['RequestType'] == 'Delete':
            send_response(event, context, 'SUCCESS', {'Message': 'Resource deletion completed'})
        else:
            resource_properties = event['ResourceProperties']
            APIKey = resource_properties['pAPIKey']
            APISecret = resource_properties['pAPISecret']
            Environment = event['ResourceProperties']['pEnvironment']
            customerNumber = resource_properties['pCustomerNumber']
            accountNumber = resource_properties['AccountNumber']
            RoleArn = resource_properties['RoleArn']
            bearerToken = get_access_token("https://auth-"+Environment+".cloudcheckr.com/auth/connect/token", APIKey, APISecret)



            response = credentialAccount(customerNumber, accountNumber, RoleArn, bearerToken, Environment)

        
    except Exception as e:
        timer.cancel()
        logger.error(f"Error: {e}")
        sendResponse = send_response(event, context, 'FAILED', {'Error': 'An error occurred during the Lambda execution: ' + str(e)})
        return {
            'statusCode': 500,
            'body': 'An error occurred during the Lambda execution: ' + str(e)
        }

    finally:
        timer.cancel()
        sendResponse = send_response(event, context, 'SUCCESS', {'Success': response})
        return response

def timeout(event, context):
    logging.error('Execution is about to time out, sending failure response to CloudFormation')
    send_response(event, context, 'FAILED', {'Error': 'Execution is about to time out'})

def credentialAccount(customerNumber, accountNumber, RoleArn, bearerToken, Environment):
    url = f"https://api-"+Environment+".cloudcheckr.com/credential/v1/customers/"+customerNumber+"/accounts/"+accountNumber+"/credentials/aws"   
    aws_partition = get_aws_partition()
    if aws_partition == "aws-us-gov":
        regionGroup = "GovUs"
    else:
        regionGroup = "Commercial"
    payload = json.dumps({
        "item": {
            "regionGroup": regionGroup,
            "crossAccountRole": {
                "roleArn": RoleArn
            }
        }
    })

    headers = {
        'Accept': 'application/json',
        'Content-Type': 'application/json',
        'Authorization': f'Bearer {bearerToken}'
    }

    request = urllib.request.Request(url, headers=headers, data=payload.encode(), method='PUT')
    try:
        response = urllib.request.urlopen(request, timeout=15)
    except urllib.error.HTTPError as e:
        raise

    response_text = response.read().decode()

    return {
        'statusCode': 200,
        'body': 'completed!',
    }


def send_response(event, context, response_status, response_data):
    response_body = json.dumps({
        'Status': response_status,
        'Reason': f'See the details in CloudWatch Log Stream: {context.log_stream_name}',
        'PhysicalResourceId': context.log_stream_name,
        'StackId': event['StackId'],
        'RequestId': event['RequestId'],
        'LogicalResourceId': event['LogicalResourceId'],
        'Data': response_data
    })

    headers = {
        'Content-Type': '',
        'Content-Length': str(len(response_body))
    }

    request = urllib.request.Request(event['ResponseURL'], data=response_body.encode('utf-8'), headers=headers, method='PUT')
    with urllib.request.urlopen(request) as f:
        pass


def get_access_token(url, client_id, client_secret):
    auth_header = base64.b64encode(f"{client_id}:{client_secret}".encode("utf-8")).decode("utf-8")
    data = urllib.parse.urlencode({"grant_type": "client_credentials"}).encode("utf-8")

    request = urllib.request.Request(
        url,
        data=data,
        headers={
            "Authorization": f"Basic {auth_header}",
            "Content-Type": "application/x-www-form-urlencoded"
        },
        method='POST'
    )

    response = urllib.request.urlopen(request)
    response_json = json.loads(response.read().decode())
    return response_json["access_token"]

def get_aws_partition():
    session = boto3.session.Session()
    region_name = session.region_name
    partition = session.get_partition_for_region(region_name)
    return partition