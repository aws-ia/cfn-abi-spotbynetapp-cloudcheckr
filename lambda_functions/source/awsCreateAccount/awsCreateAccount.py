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
    response = {'accountId': None}
    timer = threading.Timer((context.get_remaining_time_in_millis() / 1000.00) - 0.5, timeout, args=[event, context])
    timer.start()
    try:
        APIKey = event['ResourceProperties']['pAPIKey']
        APISecret = event['ResourceProperties']['pAPISecret']
        Environment = event['ResourceProperties']['pEnvironment']
        customerNumber = event['ResourceProperties']['pCustomerNumber']

        if event['RequestType'] == 'Delete':
            send_response(event, context, 'SUCCESS', {'Message': 'Resource deletion completed'})
        else:
            account_aliases, account_number = get_account_name()
            accountName = account_aliases[0] if account_aliases else account_number
            bearerToken = get_access_token("https://auth-"+Environment+".cloudcheckr.com/auth/connect/token", APIKey, APISecret)
            existingAccountId = check_existing_account(customerNumber, bearerToken, account_number, Environment)
            if existingAccountId:
                response['accountId'] = existingAccountId
                logger.info(f"Account already exists. CloudCheckr Account ID: {existingAccountId}")
            else:
                response = createAccount(customerNumber, accountName, bearerToken, Environment)
                if response.get('accountId') is None:
                    send_response(event, context, 'FAILED', {'Error': 'An error occurred during the Lambda execution: ' + response['body']})
                    return {'statusCode': 500, 'body': 'An error occurred during the Lambda execution: ' + response['body']}
            
    except Exception as e:
        logger.error(f"Lambda execution error: {e}")
        timer.cancel()
        send_response(event, context, 'FAILED', {'Error': str(e)})
        return {'statusCode': 500, 'body': str(e)}

    finally:
        timer.cancel()
        send_response(event, context, 'SUCCESS', {'accountNumber': response['accountId']})

def timeout(event, context):
    logger.error('Execution is about to time out, sending failure response to CloudFormation')
    send_response(event, context, 'FAILED', {'Error': 'Execution is about to time out'})

def send_response(event, context, response_status, response_data):
    response_body = json.dumps({
        'Status': response_status,
        'Reason': 'See the details in CloudWatch Log Stream: ' + context.log_stream_name,
        'PhysicalResourceId': context.log_stream_name,
        'StackId': event['StackId'],
        'RequestId': event['RequestId'],
        'LogicalResourceId': event['LogicalResourceId'],
        'Data': response_data
    })

    headers = {
        'Content-Type': 'application/json',
        'Content-Length': str(len(response_body))
    }

    req = urllib.request.Request(event['ResponseURL'], data=response_body.encode('utf-8'), headers=headers, method='PUT')
    with urllib.request.urlopen(req) as f:
        pass

def check_existing_account(customer_number, bearer_token, provider_identifier, Environment):
    url = f"https://api-"+Environment+".cloudcheckr.com/customer/v1/customers/"+customer_number+"/account-management/accounts?search="+provider_identifier
    headers = {
        'Accept': 'application/json',
        'Content-Type': 'application/json',
        'Authorization': 'Bearer ' + bearer_token
    }
    try:
        request = urllib.request.Request(url, headers=headers, method='GET')
        with urllib.request.urlopen(request, timeout=15) as response:
            response_json = json.loads(response.read().decode())
            for item in response_json.get('items', []):
                if item.get('providerIdentifier') == provider_identifier:
                    return item.get('id')
            return None
    except Exception as e:
        logger.error(f"Error checking existing accounts: {e}")
        return None

def createAccount(customer_number, accountName, bearer_token, Environment):
    url = f"https://api-"+Environment+".cloudcheckr.com/customer/v1/customers/"+customer_number+"/account-management/accounts"
    payload = json.dumps({"item": {"name": accountName, "provider": "AWS"}})
    headers = {'Accept': 'application/json', 'Content-Type': 'application/json', 'Authorization': 'Bearer ' + bearer_token}
    try:
        request = urllib.request.Request(url, data=payload.encode(), headers=headers, method='POST')
        with urllib.request.urlopen(request, timeout=15) as response:
            response_json = json.loads(response.read().decode())
            return {'statusCode': 200, 'body': 'Account created!', 'accountId': response_json.get('id'), 'bearerToken': bearer_token}
    except Exception as e:
        logger.error(f"Error creating account: {e}")
        return {'statusCode': 500, 'body': str(e), 'accountId': None}

def get_access_token(url, client_id, client_secret):
    auth_header = base64.b64encode(f"{client_id}:{client_secret}".encode("utf-8")).decode("utf-8")
    data = urllib.parse.urlencode({"grant_type": "client_credentials"}).encode("utf-8")
    req = urllib.request.Request(url, data=data, headers={"Authorization": f"Basic {auth_header}", "Content-Type": "application/x-www-form-urlencoded"}, method='POST')
    with urllib.request.urlopen(req) as response:
        return json.loads(response.read().decode())["access_token"]

def get_account_name():
    iam = boto3.client('iam')
    account_aliases = iam.list_account_aliases().get('AccountAliases', [])
    account_number = boto3.client('sts').get_caller_identity()['Account']
    logger.info(f"Account aliases: {account_aliases}, Account number: {account_number}")
    return account_aliases, account_number
