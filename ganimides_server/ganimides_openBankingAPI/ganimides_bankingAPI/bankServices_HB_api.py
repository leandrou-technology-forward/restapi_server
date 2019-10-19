import os
import sys

if not (os.path.dirname(os.path.dirname(__file__)) in sys.path): sys.path.append(os.path.dirname(os.path.dirname(__file__)))
if not (os.path.dirname(__file__) in sys.path): sys.path.append(os.path.dirname(__file__))

import requests
import json
import time
import datetime
import webbrowser
import configparser
import inspect
import urllib
from urllib.parse import urlparse
from http.server import BaseHTTPRequestHandler, HTTPServer

from _onlineApp import thisApp
from _onlineApp import set_debug_ON,set_debug_OFF,set_debug_level
from _onlineApp import log_message, log_result_message, log_module_initialization_message
from _onlineApp import retrieve_module_configuration
from _onlineApp._logServices import log_message,log_message_subprocess_running,log_message_wait,log_message_wait_success,log_message_special_error,log_message_special_success
from _onlineApp._utilities import find_file
from _onlineApp._appEnvironment import Fore,Back,Style
#::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
#::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
#::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
#module
#::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
#::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
#::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
module_Function = 'bank of cyprus open api services'
module_ProgramName = 'bankofcyprusAPI'
module_BaseTimeStamp = datetime.datetime.now()
module_folder = os.getcwd()
module_color = thisApp.Fore.BLUE
module_folder = os.path.dirname(__file__)
module_ProgramName = os.path.splitext(os.path.basename(__file__))[0]
module_id = '{}'.format(module_ProgramName)
module_eyecatch = module_ProgramName
module_version = 0.1
module_log_file_name = module_ProgramName+'.log'
module_errors_file_name = os.path.splitext(os.path.basename(module_log_file_name))[0]+'_errors.log'
module_versionString = f'{module_id} version {module_version}'
module_file = __file__
module_debug_level = 0
module_is_externally_configurable=False
module_identityDictionary = {
    'module_file':__file__,
    'module_Function':module_Function,
    'module_ProgramName':module_ProgramName,
    'module_BaseTimeStamp':module_BaseTimeStamp,
    'module_folder':module_folder,
    'module_color': module_color,
    'module_id':module_id,
    'module_eyecatch':module_eyecatch,
    'module_version':module_version,
    'module_versionString':module_versionString,
    'module_log_file_name':module_log_file_name,
    'module_errors_file_name':module_errors_file_name,
    'module_debug_level':module_debug_level,
    'module_is_externally_configurable':module_is_externally_configurable,
}
#::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
#::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
#::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
#globals
#::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
#::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
#::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
master_api_prefix='HB_'
active_access_token = ''
api = ''
active_api = ''
active_api_prog = f'{master_api_prefix}{active_api}'
active_api_level=''
active_api_keysource=''
active_api_key=''
active_api_standard_reply = {}
active_api_standard_result_output=''
active_api_return_OK = True
active_api_reply_code = 200
active_api_reply_text = ''
active_api_reply_json = {}
active_api_errorDesc = ''
active_api_errorStatus = ''
active_api_errorSeverity = ''
active_api_errorCode = ''
active_api_errorText = ''

api_debug_start = False
api_debug_config_param = False
api_debug_setup_param = False
api_debug_input_param = False
api_debug_output_param = False
api_debug_http_request = False
api_debug_http_request_reply = False
api_debug_result = False
api_debug_interim_result = False
api_debug_output = False
api_debug_finish = False

http_request = {}
master_athorization_code=None
master_debug_models = {
    'output_only': {'start': False, 'config_param': False, 'setup_param': False, 'http_request': False, 'http_request_reply': True, 'output': True, 'result': False, 'interim_result':False,  'input_param': False, 'output_param': False, 'finish': False},
    'request_only': {'start': False, 'config_param': False, 'setup_param': False, 'http_request': True, 'http_request_reply': True, 'output': True, 'result': False, 'interim_result':False, 'input_param': False, 'output_param': False, 'finish': False},
    'full': {'start': True, 'config_param': True, 'setup_param': True, 'http_request': True, 'http_request_reply': True, 'output': True, 'result': True, 'interim_result':True, 'input_param': True, 'output_param': True, 'finish': True},
    'none': {'start': False, 'config_param': False, 'setup_param': False, 'http_request': False, 'http_request_reply': False, 'output': False, 'result': False, 'interim_result':False, 'input_param': False, 'output_param': False, 'finish': False},
    'xdefault': {'start': True, 'config_param': False, 'setup_param': False, 'http_request': True, 'http_request_reply': True, 'output': True, 'result': True, 'interim_result':True, 'input_param': True, 'output_param': True, 'finish': True},
    'default': {'start': False, 'config_param': False, 'setup_param': False, 'http_request': False, 'http_request_reply': False, 'output': False, 'result': False, 'interim_result':False, 'input_param': False, 'output_param': False, 'finish': False},
}
master_api_properties= {
        'get_access_token': {
            'xdebug': {'start': False, 'config_param': False, 'setup_param': False, 'http_request': False, 'http_request_reply': False, 'output': True, 'result': False, 'interim_result':False,  'input_param': False, 'output_param': False, 'finish': False},
            'debug_model': 'none',
            'version':'0.0',
            },
        'get_account_subscriptions': {
            'debug_model': 'none',
            'version':'0.0'
            },
        'get_subscription_details': {
            'debug_model': 'none',
            'version':'0.0'
            },
        'get_subscriptionId': {
            'debug_model': 'none',
            'version':'0.0',
            'function':'create subscription record',
            'return_entity':'subscriptionID',
            'return_entity_locator':'subscriptionId',
            },
        'get_authorization_token': {
            'debug_model': 'none',
            'version':'0.0',
            'function':'get customer authorization token',
            'return_entity':'authorization_token',
            'return_entity_locator':'access_token',
            },
        'get_customer_authorization': {
            'debug_model': 'none',
            'version':'0.0',
            'function':'get customer authorization',
            'return_entity':'authorization_code',
            'return_entity_locator':'access_token',
            },
        'get_customer_Consent': {
            'debug_model': 'none',
            'version':'0.0',
            'function':'get customer consent',
            'return_entity':'',
            'return_entity_locator':'',
            },
        'commit_subscription': {
            'debug_model': 'none',
            'version':'0.0',
            'function':'update customer subscription',
            'return_entity':'subscriptionID',
            'return_entity_locator':'subscriptionId',
            },
        'create_subscription': {
            'debug_model': 'none',
            'version':'0.0',
            'function':'create and authorize customer subscription',
            'return_entity':'subscriptionID',
            'return_entity_locator':'subscriptionId',
            },
        'get_subscription_accounts': {
            'debug_model': 'none',
            'version':'0.0',
            'function':'list subscription accounts',
            'return_entity':'',
            'return_entity_locator':'',
            },
        'get_payment_jws_signature': {
            'debug_model': 'none',
            'version':'0.0',
            'function':'initiate a payment(get signature)',
            'return_entity':'',
            'return_entity_locator':'',
            },

    }
master_api_usage = {}
master_http_ok_code = requests.codes.ok
http_ok_codes = (200,201)
master_configuration = {
'bankID': 'bankofcyprus',
'bankName': 'Bank of Cyprus',
"bankIdString": "BOC",
"BIC":"?????",
'countryCode': 'CY',
'isSepaZone': True,
'isEUROZone': True,
'app_name': 'qrp' ,
"application_name": "qrp",
'client_id': '52ee828e-a18e-4560-bfed-2d5158e9a507' ,
'client_secret': 'iV7dQ4jH7oJ5pX4fT7nM4lR5sT1bN2oJ2bU1kW5vM7mQ4kB7rV',
'api_uri': 'https://sandbox-apis.bankofcyprus.com/' ,
'redirect_uri': 'http://localhost:5555/authorization',
"correlationId": "ganimedes_ABC001",
'tppId': 'singpaymentdata',
'journeyId': '123456789',
'lang': '',
"originUserId": "1524",
"originSourceId": "",
"originChannelId": "",
"originDeptId": "",
"originEmployeeId": "",
"originTerminalId": "",
'debug_level':1,
'http_result_file':'code.txt',
'http_result_folder':1,
}


#response_code=200, response_desc="OK", responce_format="UpdateSubscriptionResponse"
# master_api_replies={


# 200 OK UpdateSubscriptionResponse
# 201 Created UpdateSubscriptionResponse
# 202 Accepted
# 302 Found
# 400 Bad Request ErrorResponse
# 401 Unauthorized ErrorResponse
# 403 Forbidden ErrorResponse
# 404 API URL Not Found ErrorResponse
# 405 Method not Found ErrorResponse
# 406 Not Acceptable ErrorResponse
# 429 Too many Requests ErrorResponse
# 500 Internal Server Error ErrorResponse
# 503 Service Unavailable ErrorResponse
# }
#::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
#::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
#::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
#module services
#::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
#::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
#::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
################################################################
def api_standard_success_reply(msg=None, return_value=None, return_data=None, api=None):
    global active_api
    global active_api_prog
    global master_api_prefix
    
    if not api:
        api = active_api
        api_prog = active_api_prog
    else:
        api = active_api
        api_prog = f'{master_api_prefix}{api}'

    api_version = master_api_properties.get(api,{}).get('version', '0.1')

    if not msg:
        msg = 'ok.{api} executed'

    if not return_data:
        return_data = {}
    if not return_value:
        return_value = ''

    reply = {
        'status': 'success',
        'message': msg,
        'return_value': return_value,
        'data': return_data,
        'error':{},
        'api': api,
        'api_prog': api_prog,
        'api_version': api_version
    }

    return reply
################################################################
def api_standard_fail_reply(errormsg='', return_value=None, errors=None, api=None):
    global active_api
    global active_api_prog
    global master_api_prefix
    
    if not api:
        api = active_api
        api_prog = active_api_prog
    else:
        api = active_api
        api_prog = f'{master_api_prefix}{api}'

    api_version = master_api_properties.get(api,{}).get('version', '0.1')

    if not errormsg:
        errormsg = '{api} executed with ERRORS'

    if not errors:
        errors = {}
    if not return_value:
        return_value = ''

    reply = {
        'status': 'failed',
        'message': errormsg,
        'return_value': None,
        'data': {},
        'error': errors,
        'api': api,
        'api_prog': api_prog,
        'api_version': api_version
    }

    return reply
################################################################
def api_standard_error_reply(errormsg='', return_value=None, errors=None, api=None):
    global active_api
    global active_api_prog
    global master_api_prefix
    
    if not api:
        api = active_api
        api_prog = active_api_prog
    else:
        api = active_api
        api_prog = f'{master_api_prefix}{api}'

    api_version = master_api_properties.get(api,{}).get('version', '0.1')

    if not errormsg:
        errormsg = '{api} executed with ERRORS'

    if not errors:
        errors = {}
    
    reply = {
        'status': 'error',
        'message': errormsg,
        'return_value': return_value,
        'data': {},
        'error': errors,
        'api': api,
        'api_prog': api_prog,
        'api_version': api_version
    }

    return reply
################################################################
# #::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
# async def start_http_server_subprocess():
#     #import subprocess
#     # p = subprocess.Popen('ls', shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
#     # for line in p.stdout.readlines():
#     #     print (line)
#     # retval = p.wait()
#     subprocess.run(["starthttpserver.py", ""]) # Run command
# #::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
# def start_http_server():
#     loop = asyncio.get_event_loop()
#     loop.run_until_complete(start_http_server_subprocess())
#     loop.close()
#::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
#::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
#::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
# actionable apis
#::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
#::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
#::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
################################################################
def hb_create_authorize_and_commit_subscription(access_token, allow_transactionHistory=True, allow_balance=True, allow_details=True, allow_checkFundsAvailability=True, payments_limit=0, payments_currency='EUR', payments_amount=0):

    api='create_authorize_commit_subscription'

    #start
    log_api_start(api)

    #input
    log_api_input_param('allow_transactionHistory',allow_transactionHistory)
    log_api_input_param('allow_balance',allow_balance)
    log_api_input_param('allow_details',allow_details)
    log_api_input_param('allow_checkFundsAvailability',allow_checkFundsAvailability)
    log_api_input_param('payments_limit',payments_limit)
    log_api_input_param('payments_currency',payments_currency)
    log_api_input_param('payments_amount',payments_amount)

    #create subscription record
    create_result = hb_get_subscriptionId(access_token, allow_transactionHistory=allow_transactionHistory, allow_balance=allow_balance, allow_details=allow_details, allow_checkFundsAvailability=allow_checkFundsAvailability, payments_limit=payments_limit, payments_currency=payments_currency, payments_amount=payments_amount)   
    if not create_result.get('status')=='success':
        return create_result

    #get the subscription id
    subscriptionId=create_result.get('return_value')
    # log_api_interim_result('subscriptionId',subscriptionId)
    subscriptionId=create_result.get('data',{}).get('subscriptionId')
    log_api_interim_result('subscriptionId',subscriptionId)

    #get customer consent: (authorization code)
    authorization_code = hb_get_customer_authorization(subscriptionId)
    if not authorization_code:
        error_text=f'authorization NOT received by customer for subscriptionId:{subscriptionId}'
        return api_standard_error_reply(errormsg=error_text)

    log_api_interim_result('authorization_code',authorization_code)


    #refresh access token
    access_token=hb_get_access_token()

    #get authorization token from customer authorization code 
    authorization_token=hb_get_authorization_token(access_token,authorization_code)
    if not authorization_token:
        error_text=f'authorization token for authorization code {authorization_code} NOT retrieved'
        return api_standard_error_reply(errormsg=error_text)

    log_api_interim_result('authorization_token',authorization_token)

    #get subscription details
    SubscriptionDetails=hb_get_subscription_details(access_token,subscriptionId)
    if not SubscriptionDetails:
        error_text=f'subscriptionId {subscriptionId} NOT found'
        return api_standard_error_reply(errormsg=error_text)

    current_selected_accounts=SubscriptionDetails['selectedAccounts']
    current_accounts_options=SubscriptionDetails['accounts']
    current_payments_options=SubscriptionDetails['payments']
    log_api_interim_result('current_selected_accounts=',current_selected_accounts)
    log_api_interim_result('current_accounts_options=',current_accounts_options)
    log_api_interim_result('current_payments_accounts=',current_payments_options)
    current_subscription_data = "{\"selectedAccounts\":"+json.dumps(current_selected_accounts)+",\"accounts\":"+json.dumps(current_accounts_options)+",\"payments\":"+json.dumps(current_payments_options)+"}"
    log_api_interim_result('current_subscription_data', current_subscription_data)

    #update subscription after authorization from the customer
    commit_result = hb_commit_subscription(subscriptionId, authorization_token, current_subscription_data)
    if commit_result.get('status') == 'success':
         create_result = api_standard_success_reply(msg='OK. subscription created', return_value=subscriptionId, return_data=commit_result.get('data'))
    else:
         create_result = api_standard_fail_reply(errormsg='subscription create failed', return_value=subscriptionId, errors=commit_result.get('data'))

    #display result
    log_api_result(f'subscription [{subscriptionId}] create:', create_result)

    #display output
    log_api_output_result(f'subscription [{subscriptionId}] created', create_result.get('message'))

    #finish
    log_api_finish()
    return create_result
################################################################
def hb_create_subscription(access_token, allow_transactionHistory=True, allow_balance=True, allow_details=True, allow_checkFundsAvailability=True, payments_limit=0, payments_currency='EUR', payments_amount=0):
    api='create_subscription'

    #start
    log_api_start(api)

    #input
    log_api_input_param('allow_transactionHistory',allow_transactionHistory)
    log_api_input_param('allow_balance',allow_balance)
    log_api_input_param('allow_details',allow_details)
    log_api_input_param('allow_checkFundsAvailability',allow_checkFundsAvailability)
    log_api_input_param('payments_limit',payments_limit)
    log_api_input_param('payments_currency',payments_currency)
    log_api_input_param('payments_amount',payments_amount)

    #create subscription record
    xcreate_result = hb_get_subscriptionId(access_token, allow_transactionHistory=allow_transactionHistory, allow_balance=allow_balance, allow_details=allow_details, allow_checkFundsAvailability=allow_checkFundsAvailability, payments_limit=payments_limit, payments_currency=payments_currency, payments_amount=payments_amount)   
    subscriptionId = xcreate_result.get('data', {}).get('subscriptionId', None)
    if xcreate_result.get('status') == 'success':
        log_api_interim_result('subscriptionId',subscriptionId)
        create_result = api_standard_success_reply(msg='OK. subscription created', return_value=subscriptionId, return_data=xcreate_result.get('data'))
    else:
         create_result = api_standard_fail_reply(errormsg='subscription create failed', return_value=subscriptionId, errors=xcreate_result.get('data'))

    #display result
    log_api_result(f'subscription [{subscriptionId}] create:', create_result)

    #display output
    log_api_output_result(f'subscription [{subscriptionId}] create message:', create_result.get('message'))

    #finish
    log_api_finish()
    return create_result
################################################################
def hb_authorize_and_commit_subscription(access_token, subscriptionId):

    api='authorize_and_commit_subscription'

    #start
    log_api_start(api)

    #input
    log_api_input_param('subscriptionID',subscriptionId)

    # #get the subscription id
    # subscriptionId=create_result.get('return_value')
    # # log_api_interim_result('subscriptionId',subscriptionId)
    # subscriptionId=create_result.get('data',{}).get('subscriptionId')
    # log_api_interim_result('subscriptionId',subscriptionId)

    #get customer consent: (authorization code)
    authorization_code = hb_get_customer_authorization(subscriptionId)
    if not authorization_code:
        error_text=f'authorization NOT received by customer for subscriptionId:{subscriptionId}'
        return api_standard_error_reply(errormsg=error_text)

    log_api_interim_result('authorization_code',authorization_code)

    #refresh access token
    access_token=hb_get_access_token()

    #get authorization token from customer authorization code 
    authorization_token=hb_get_authorization_token(access_token,authorization_code)
    if not authorization_token:
        error_text=f'authorization token for authorization code {authorization_code} NOT retrieved'
        return api_standard_error_reply(errormsg=error_text)

    log_api_interim_result('authorization_token',authorization_token)

    #get subscription details
    SubscriptionDetails=hb_get_subscription_details(access_token,subscriptionId)
    if not SubscriptionDetails:
        error_text=f'subscriptionId {subscriptionId} SubscriptionDetails NOT found'
        return api_standard_error_reply(errormsg=error_text)

    current_selected_accounts=SubscriptionDetails['selectedAccounts']
    current_accounts_options=SubscriptionDetails['accounts']
    current_payments_options=SubscriptionDetails['payments']
    log_api_interim_result('current_selected_accounts=',current_selected_accounts)
    log_api_interim_result('current_accounts_options=',current_accounts_options)
    log_api_interim_result('current_payments_accounts=',current_payments_options)
    current_subscription_data = "{\"selectedAccounts\":"+json.dumps(current_selected_accounts)+",\"accounts\":"+json.dumps(current_accounts_options)+",\"payments\":"+json.dumps(current_payments_options)+"}"
    log_api_interim_result('current_subscription_data', current_subscription_data)

    #update subscription after authorization from the customer
    commit_result = hb_commit_subscription(subscriptionId, authorization_token, current_subscription_data)
    if commit_result.get('status') == 'success':
         create_result = api_standard_success_reply(msg='OK. subscription authorized and committed', return_value=subscriptionId, return_data=commit_result.get('data'))
    else:
         create_result = api_standard_fail_reply(errormsg='subscription commit failed', return_value=subscriptionId, errors=commit_result.get('data'))

    #display result
    log_api_result(f'subscription [{subscriptionId}] commit:', create_result)

    #display output
    log_api_output_result(f'subscription [{subscriptionId}] commit message', create_result.get('message'))

    #finish
    log_api_finish()
    return create_result
################################################################
def hb_change_subscription(access_token, changed_subscriptionId, allow_transactionHistory=True, allow_balance=True, allow_details=True, allow_checkFundsAvailability=True, payments_limit=0, payments_currency='EUR', payments_amount=0):

    # global active_api_reply_code
    # global active_api_reply_json
    # global active_api_reply_text
    # global active_api_reply_error_text
    # global active_api_reply_error_code
    # global active_api_errorDesc
    # global active_api_errorStatus
    # global active_api_errorSeverity
    # global active_api_errorCode
    # global active_api_errorText
    # global active_api_return_OK

    api='change_subscription'
    log_api_start(api)

    #input
    log_api_input_param('allow_transactionHistory',allow_transactionHistory)
    log_api_input_param('allow_balance',allow_balance)
    log_api_input_param('allow_details',allow_details)
    log_api_input_param('allow_checkFundsAvailability',allow_checkFundsAvailability)
    log_api_input_param('payments_limit',payments_limit)
    log_api_input_param('payments_currency',payments_currency)
    log_api_input_param('payments_amount',payments_amount)

    #create new subscription record
    create_result = hb_get_subscriptionId(access_token, allow_transactionHistory=allow_transactionHistory, allow_balance=allow_balance, allow_details=allow_details, allow_checkFundsAvailability=allow_checkFundsAvailability, payments_limit=payments_limit, payments_currency=payments_currency, payments_amount=payments_amount)   
    if not create_result.get('status')=='success':
        return create_result

    #get the subscription id
    subscriptionId=create_result.get('return_value')
    # log_api_interim_result('subscriptionId',subscriptionId)
    subscriptionId=create_result.get('data',{}).get('subscriptionId')
    log_api_interim_result('subscriptionId',subscriptionId)

    if not subscriptionId:
        error_text=f'subscriptionId NOT returned by hb_get_subscriptionId'
        return api_standard_error_reply(errormsg=error_text)

    #get customer consent: (authorization code)
    authorization_code = hb_get_customer_authorization(subscriptionId)
    if not authorization_code:
        error_text=f'authorization NOT received by customer for subscriptionId:{subscriptionId}'
        return api_standard_error_reply(errormsg=error_text)

    log_api_interim_result('authorization_code',authorization_code)

    #refresh access token
    access_token=hb_get_access_token()

    #get authorization token from customer authorization code 
    authorization_token=hb_get_authorization_token(access_token,authorization_code)
    if not authorization_token:
        error_text=f'authorization token for authorization code {authorization_code} NOT retrieved'
        return api_standard_error_reply(errormsg=error_text)

    log_api_interim_result('authorization_token',authorization_token)

    #get subscription details
    SubscriptionDetails=hb_get_subscription_details(access_token,subscriptionId)
    if not SubscriptionDetails:
        error_text=f'subscriptionId {subscriptionId} subscription details NOT found'
        return api_standard_error_reply(errormsg=error_text)

    current_selected_accounts=SubscriptionDetails['selectedAccounts']
    current_accounts_options=SubscriptionDetails['accounts']
    current_payments_options=SubscriptionDetails['payments']
    log_api_interim_result('current_selected_accounts=',current_selected_accounts)
    log_api_interim_result('current_accounts_options=',current_accounts_options)
    log_api_interim_result('current_payments_accounts=',current_payments_options)
    current_subscription_data = "{\"selectedAccounts\":"+json.dumps(current_selected_accounts)+",\"accounts\":"+json.dumps(current_accounts_options)+",\"payments\":"+json.dumps(current_payments_options)+"}"
    log_api_interim_result('current_subscription_data', current_subscription_data)

    #update subscription after authorization from the customer
    commit_result = hb_commit_subscription(subscriptionId, authorization_token, current_subscription_data)
    if commit_result.get('status') == 'success':
         change_result = api_standard_success_reply(msg='OK. subscription created', return_value=subscriptionId, return_data=commit_result.get('data'))
    else:
         change_result = api_standard_fail_reply(errormsg='subscription create failed', return_value=subscriptionId, errors=commit_result.get('data'))

    #display result
    log_api_result(f'subscription [{subscriptionId}] create:', change_result)

    #display output
    log_api_output_result(f'subscription [{subscriptionId}] created', change_result.get('message'))

    #delete old subs
    delete_result = hb_delete_subscription(access_token, changed_subscriptionId)
    log_api_output_result(f'subscription [{subscriptionId}] change old subsription delete message', delete_result.get('message','?'))

    #finish
    log_api_finish()
    return change_result


    # #input params
    # log_api_input_param('subscriptionId',subscriptionId)
    # log_api_input_param('allow_transactionHistory',allow_transactionHistory)
    # log_api_input_param('allow_balance',allow_balance)
    # log_api_input_param('allow_details',allow_details)
    # log_api_input_param('allow_checkFundsAvailability',allow_checkFundsAvailability)
    # log_api_input_param('payments_limit',payments_limit)
    # log_api_input_param('payments_currency',payments_currency)
    # log_api_input_param('payments_amount',payments_amount)

    # #transformations
    # allow_transactionHistory_string = str(allow_transactionHistory).lower()
    # allow_balance_string = str(allow_balance).lower()
    # allow_details_string = str(allow_details).lower()
    # allow_checkFundsAvailability_string = str(allow_checkFundsAvailability).lower()

    # # setup subscription options
    # accounts_options_string = f'"transactionHistory": {allow_transactionHistory_string}, "balance": {allow_balance_string}, "details": {allow_details_string}, "checkFundsAvailability": {allow_checkFundsAvailability_string}'
    # payments_options_string = f'"limit": {payments_limit}, "currency": "{payments_currency}", "amount": {payments_amount}'
    # log_api_interim_result('accounts_options_string',accounts_options_string)        
    # log_api_interim_result('payments_options_string',payments_options_string)        

    # subscription_options_string = '"accounts":{'+accounts_options_string+'},"payments":{'+payments_options_string+'}'
    # log_api_interim_result('subscription_options_string',subscription_options_string)
    
    # # print('')
    # # SubscriptionRequestData_string="{\"accounts\":{\"transactionHistory\":true,\"balance\":true,\"details\":true,\"checkFundsAvailability\":false},\"payments\":{\"limit\":0.00,\"currency\":\"EUR\",\"amount\":0.00}}"
    # # print('SubscriptionRequestData_string =',SubscriptionRequestData_string)        
    # # SubscriptionRequestData= json.loads(SubscriptionRequestData_string)
    
    # subscription_data_string = "{"+subscription_options_string+"}"
    # log_api_interim_result('subscription_data_string',subscription_data_string)

    # subscription_data= json.loads(subscription_data_string)
    # log_api_interim_result('subscription_data',subscription_data)

    # #validate input params
    # # if not selected_accounts and not accounts_options and not payments_options:
    # #     error_text='subscription options NOT privided'
    # #     return api_standard_error_reply(errormsg=error_text)


    # #validate subscription
    # SubscriptionDetails=hb_get_subscription_details(access_token,subscriptionId)
    # if not SubscriptionDetails:
    #     error_text=f'subscriptionId {subscriptionId} NOT found'
    #     return api_standard_error_reply(errormsg=error_text)
    # status = SubscriptionDetails.get('status')
    # if status in ('ACTV', 'revoked'):
    #     error_text=f'subscriptionId {subscriptionId} is {status}'
    #     return api_standard_error_reply(errormsg=error_text)
        
    # if xcreate_result.get('status') == 'success':
    #     log_api_interim_result('subscriptionId',subscriptionId)
    #     create_result = api_standard_success_reply(msg='OK. subscription created', return_value=subscriptionId, return_data=xcreate_result.get('data'))
    # else:
    #      create_result = api_standard_fail_reply(errormsg='subscription create failed', return_value=subscriptionId, errors=xcreate_result.get('data'))
    # create_result = hb_create_subscription(access_token, allow_transactionHistory=True, allow_balance=True, allow_details=True, allow_checkFundsAvailability=True, payments_limit=0, payments_currency='EUR', payments_amount=)
    # subscriptionId = create_result.get('data', {}).get('subscriptionId', None)
    # if not create_result.get('status') == 'success':
    #     change_result = api_standard_fail_reply(errormsg='subscription create failed', return_value=subscriptionId, errors=create_result.get('data'))
    #     return change_result


    # #get customer authorization code 
    # authorization_code = hb_get_customer_authorization(subscriptionId)
    # if not authorization_code:
    #     error_text=f'authorization NOT received by customer for subscriptionId:{subscriptionId}'
    #     return api_standard_error_reply(errormsg=error_text)

    # log_api_interim_result('authorization_code',authorization_code)

    # #get authorization token from customer authorization code 
    # access_token=hb_get_access_token()#refresh
    # authorization_token=hb_get_authorization_token(access_token,authorization_code)
    # if not authorization_token:
    #     error_text=f'authorization token for authorization code {authorization_code} NOT retrieved'
    #     return api_standard_error_reply(errormsg=error_text)

    # log_api_interim_result('authorization_token',authorization_token)
    
    # log_api_interim_result('authorization_token',authorization_token)

    # #validate subscription
    # current_selected_accounts=SubscriptionDetails['selectedAccounts']
    # current_accounts_options=SubscriptionDetails['accounts']
    # current_payments_options=SubscriptionDetails['payments']
    # log_api_interim_result('current_selected_accounts=',current_selected_accounts)
    # log_api_interim_result('current_accounts_options=',current_accounts_options)
    # log_api_interim_result('current_payments_options', current_payments_options)
    # log_api_interim_result('changed_payments_options', payments_options_string)

    # current_selected_accounts=SubscriptionDetails['selectedAccounts']
    # current_accounts_options=SubscriptionDetails['accounts']
    # current_payments_options=SubscriptionDetails['payments']
    # log_api_interim_result('current_selected_accounts=',current_selected_accounts)
    # log_api_interim_result('current_accounts_options=',current_accounts_options)
    # log_api_interim_result('current_payments_accounts=',current_payments_options)
    
    
    # current_subscription_data = "{\"selectedAccounts\":"+json.dumps(current_selected_accounts)+",\"accounts\":"+json.dumps(current_accounts_options)+",\"payments\":"+json.dumps(current_payments_options)+"}"
    # log_api_interim_result('current_subscription_data', current_subscription_data)

    # #update subscription after authorization from the customer
    # commit_result = hb_commit_subscription(subscriptionId, authorization_token, current_subscription_data)


    # # #replace with payments_options_string
    # # changed_subscription_data1 = "{\"selectedAccounts\":"+json.dumps(current_selected_accounts)+",\"accounts\":\{"+json.dumps(current_accounts_options)+"\},\"payments\":\{"+json.dumps(payments_options_string)+"\}\}"
    # # log_api_interim_result('changed subscription_data1 =', changed_subscription_data1)
    # # x=json.loads(changed_subscription_data1)
    # # commit_result = hb_commit_subscription(subscriptionId, authorization_token, x)


    # # changed_subscription_data2 = "{\"payments\":{"+json.dumps(payments_options_string)+"\}\}"
    # # log_api_interim_result('changed subscription_data2 =', changed_subscription_data2)
    # # commit_result = hb_commit_subscription(subscriptionId, authorization_token, changed_subscription_data1)


    # # subscription_options_string = '"payments":{'+payments_options_string+'}'
    # # changed_subscription_data3 = "{"+subscription_options_string+"}"
    # # log_api_interim_result('changed subscription_data3 =', changed_subscription_data3)
    # # commit_result = hb_commit_subscription(subscriptionId, authorization_token, changed_subscription_data1)
    # # x=1    

    # # # if not selected_accounts:
    # # #     selected_accounts = current_selected_accounts
    # # # if not accounts_options:
    # # #     accounts_options = current_accounts_options
    # # # if not payments_options:
    # # #     payments_options = current_payments_options

    # # # changed_subscription_data_json = "{\"selectedAccounts\":" + json.dumps(selected_accounts) + ",\"accounts\":" + json.dumps(accounts_options) + ",\"payments\":" + json.dumps(payments_options) + "}"
    # # # changed_subscription_data_json = "{\"payments\":" + json.dumps(payments_options) + "}"


    # # # subscription_options_string = '"accounts":{'+accounts_options_string+'},"payments":{'+payments_options_string+'}'
    # # # log_api_interim_result('subscription_options_string',subscription_options_string)
    
    # # # print('')
    # # # SubscriptionRequestData_string="{\"accounts\":{\"transactionHistory\":true,\"balance\":true,\"details\":true,\"checkFundsAvailability\":false},\"payments\":{\"limit\":0.00,\"currency\":\"EUR\",\"amount\":0.00}}"
    # # # print('SubscriptionRequestData_string =',SubscriptionRequestData_string)        
    # # # SubscriptionRequestData= json.loads(SubscriptionRequestData_string)
    
    # # # subscription_data_string = "{"+subscription_options_string+"}"
    # # # log_api_interim_result('subscription_data_string',subscription_data_string)

    # # # subscription_data= json.loads(subscription_data_string)
    # # # log_api_interim_result('subscription_data',subscription_data)


    # # #changed_subscription_data_string = json.dumps(changed_subscription_data_json)
    # # # changed_subscription_data_string1 = f'"selectedAccounts": {json.dumps(selected_accounts)}, "accounts": {json.dumps(accounts_options)}, "payments": {json.dumps(payments_options)}'
    # # # print('1s',changed_subscription_data_string)
    # # # changed_subscription_data_json = json.loads(changed_subscription_data_string1)
    # # # print('1j',changed_subscription_data_json)
    # # # changed_subscription_data_string = '{'+changed_subscription_data_string1+'}'
    # # # print('2s',changed_subscription_data_string)
    # # # changed_subscription_data_json = json.loads(changed_subscription_data_string)
    # # # print('2j',changed_subscription_data_string)

    # # # log_api_interim_result('changed subscription_data =', changed_subscription_data_json)

    # # #update subscription after authorization from the customer
    # # commit_result = hb_commit_subscription(subscriptionId, authorization_token, subscription_data_string)
    
    # if commit_result.get('status') == 'success':
    #      change_result = api_standard_success_reply(msg='OK. subscription changed', return_value=subscriptionId, return_data=commit_result.get('data'))
    # else:
    #      change_result = api_standard_fail_reply(errormsg='subscription change failed', return_value=subscriptionId, errors=commit_result.get('data'))

    # #display result
    # log_api_result(f'subscription [{subscriptionId}] change:', change_result)

    # #display output
    # log_api_output_result(f'subscription [{subscriptionId}] changed', change_result.get('message'))

    # SubscriptionDetails=hb_get_subscription_details(access_token,subscriptionId)
    # if not SubscriptionDetails:
    #     error_text=f'subscriptionId {subscriptionId} NOT found'
    #     return api_standard_error_reply(errormsg=error_text)
    # print ('--after change--',SubscriptionDetails)

    # #finish
    # log_api_finish()
    # return change_result

    # #update subscription
    # commit_result = hb_commit_subscription(subscriptionId, authorization_token, changed_subscription_data_json)

    # #evaluate result
    # if commit_result.get('status') == 'success':
    #     change_result = api_standard_success_reply(msg='OK. subscription changed', return_value=subscriptionId, return_data=None, api=None)
    # else:
    #     errors = commit_result.get('message')
    #     change_result = api_standard_fail_reply(errormsg='subscription change failed', return_value=subscriptionId, errors=errors, api=None)

    # #display result
    # log_api_result(f'subscription [{subscriptionId}] change:', change_result, api=api)

    # #display result
    # log_api_output_result(f'subscription [{subscriptionId}] change:', change_result, api=api)

    # #finish
    # log_api_finish(api)
    # return change_result
################################################################
def hb_delete_subscription(access_token,subscriptionId):
    # global master_http_ok_code
    # global active_api_errorText
    api='delete_subscription'

    #start
    log_api_start(api)

    #input params
    log_api_input_param('subscriptionId',subscriptionId)

    #init output
    delete_result={}

    #setup httprequest
    api_params=hb_get_parameters(api)
    request_params=hb_prepare_request_standard(access_token,'',api_params,subscriptionId)
    api_url=request_params['url']
    headers=request_params['headers']
    params=request_params['parameters']

    #httprequest
    r = hb_standard_http_requestV2(api=api, function='delete', url=api_url,headers=headers, params=params, data=None)

    if r.get('success'):
        delete_result = api_standard_success_reply(msg=f'OK. subscription {subscriptionId} deleted', return_value=subscriptionId, return_data=r.get('data', {}))
    else:
        if r.get('error_code') == 'MSSUB008':
            delete_result = api_standard_success_reply(msg=f'OK. subscription {subscriptionId} already deleted', return_value=subscriptionId, return_data=r.get('data', {}))
        else:
            delete_result = api_standard_fail_reply(errormsg=f'subscription {subscriptionId} delete failed', return_value=subscriptionId, errors=r.get('data', {}))

    #display result
    log_api_result(f'subscription [{subscriptionId}] delete:', delete_result, api=api)

    #display result
    log_api_output_result(f'subscription [{subscriptionId}] delete:', delete_result.get('message'))

    #finish
    log_api_finish()
    return delete_result
#:::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
#:::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
#:::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
#:::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
################################################################
################################################################
################################################################
### database functions                                       ###
################################################################
################################################################
################################################################
################################################################
def hb_log_usage(api):
    global master_api_usage
    configFile='bankocyprusAPI_apiusage.cfg'
    usageRec=master_api_usage.get(api,{})
    usage = usageRec.get('usage', 0)
    usage = usage + 1
    usageRec.update({'usage':usage})
    master_api_usage.update({api:usageRec})
    master_api_usage_String=json.dumps(master_api_usage)
    with open(configFile, 'w') as cfgFile:
        cfgFile.write(master_api_usage_String)
################################################################
################################################################
################################################################
### log support functions                                    ###
################################################################
################################################################
################################################################

################################################################
def whoami():
    return inspect.stack()[1][3]
################################################################
def whosdaddy():
    return inspect.stack()[2][3]
################################################################
def whosapi(api_prog):
    global master_api_prefix
    prefix_len = len(master_api_prefix) 
    api = api_prog[prefix_len:]
    return api
################################################################
def get_api_debug_levels(api):
    global active_api
    global active_api_prog
    global api_debug_start
    global api_debug_finish
    global api_debug_http_request
    global api_debug_http_request_reply
    global api_debug_result
    global api_debug_input_param
    global api_debug_output_param
    global api_debug_output
    global api_debug_interim_result
    global api_debug_config_param
    global api_debug_setup_param
    global master_api_prefix
    global master_api_properties
    global master_debug_models

    active_api = api
    active_api_prog = f'{master_api_prefix}{active_api}'
    api_debug_levels=master_api_properties.get(api,{}).get('debug',None)
    if not api_debug_levels:
        api_debug_model=master_api_properties.get(api,{}).get('debug_model',None)
        if api_debug_model:
            api_debug_levels = master_debug_models.get(api_debug_model,None)
        if not api_debug_levels:
            api_debug_levels = master_debug_models.get('default')
        api_properties = master_api_properties.get(api,{})
        api_properties.update({'debug': api_debug_levels})
        master_api_properties.update({api:api_properties})

    if not api_debug_levels:
        api_debug_levels={}

    api_debug_start = api_debug_levels.get('start',False)
    api_debug_finish = api_debug_levels.get('finish',False)
    api_debug_http_request = api_debug_levels.get('http_request',False)
    api_debug_http_request_reply = api_debug_levels.get('http_request_reply',False)
    api_debug_result= api_debug_levels.get('result',False)
    api_debug_interim_result= api_debug_levels.get('interim_result',False)
    api_debug_output= api_debug_levels.get('output',False)
    api_debug_output_param = api_debug_levels.get('output_param',False)
    api_debug_input_param = api_debug_levels.get('input_param', False)
    api_debug_config_param = api_debug_levels.get('config_param', False)
    api_debug_setup_param = api_debug_levels.get('setup_param', False)
################################################################
def log_api_start(api=None,msg=''):
    global active_api_prog
    global active_api
    global api_debug_start
    api_prog = whosdaddy()
    if api_prog != active_api_prog:
        api = whosapi(api_prog)
        get_api_debug_levels(api)

    hb_log_usage(active_api)
    if api_debug_start:
        msg = f'{active_api_prog}'
        log_message(msg, msgType='START')
################################################################
def log_api_finish(msg='',api=''):
    global active_api
    global active_api_prog
    global api_debug_finish
    global api_debug_start
    api_prog = whosdaddy()
    if api_prog != active_api_prog:
        api = whosapi(api_prog)
        get_api_debug_levels(api)

    if api_debug_finish:
        if not msg:
            msg = f'{active_api_prog}-finished'
        log_message(msg, msgType='FINISH')
    else:
        if api_debug_start:
            log_message('', msgType='FINISH')
################################################################
def log_http_request(request='',api='',function='', url='',headers='',params='',data=''):
    global active_api
    global active_api_prog
    global api_debug_http_request

    if api_debug_http_request:
        log_message(f'http-request ({function}):',msgType='START',msgColor=Fore.YELLOW)
        if request:
            url=request['url']
            headers=request['headers']
            params=request['parameters']
            data=request['data']
        if url:
            log_message(f'url--{url}',msgType='info-3',msgOffset='+1',msgColor=Fore.LIGHTRED_EX)
        if headers:
            log_message(f'headers--{headers}',msgType='info-2',msgOffset='+1',msgColor=Fore.LIGHTBLUE_EX)
        if params:
            log_message(f'params--{params}',msgType='info-1',msgOffset='+1',msgColor=Fore.WHITE)
        if data:
            log_message(f'data--{data}',msgType='info-3',msgOffset='+1',msgColor=Fore.CYAN)
        log_message('',msgType='FINISH',msgColor=Fore.YELLOW)
################################################################
def log_http_request_reply(reply,api=''):
    global active_api
    global active_api_prog
    global api_debug_http_request_reply
    global master_http_ok_code
    global active_api_standard_reply
    global active_api_reply_code
    global active_api_reply_json
    global active_api_reply_text
    global active_api_reply_error_text
    global active_api_reply_error_code
    global active_api_errorDesc
    global active_api_errorStatus
    global active_api_errorSeverity
    global active_api_errorCode
    global active_api_errorText
    global active_api_return_OK

    if api_debug_http_request_reply:
        log_message(f'http-request reply:',msgType='START',msgColor=Fore.YELLOW)
        if not reply:
            error_text='empty reply from {active_api_prog}'
            log_message(error_text, msgType='error', msgOffset='+1')
        if active_api_return_OK:
            replycolor = Fore.GREEN
        else:
            replycolor = Fore.RED

        log_message(f'status code:{reply.status_code}',msgType='info',msgOffset='+1',msgColor=replycolor)
        log_message(f'return_OK:{active_api_return_OK}',msgType='info',msgOffset='+1',msgColor=replycolor)
        if active_api_reply_code:
            log_message(f'reply_code:{active_api_reply_code}',msgType='info',msgOffset='+1',msgColor=replycolor)
        if active_api_reply_json:
            log_message(f'reply_json:{active_api_reply_json}',msgType='info',msgOffset='+1',msgColor=replycolor)
        if active_api_reply_text:
            log_message(f'reply_text:{active_api_reply_text}',msgType='info',msgOffset='+1',msgColor=replycolor)
        if active_api_reply_error_text:
            log_message(f'error_text:{active_api_reply_error_text}',msgType='info',msgOffset='+1',msgColor=replycolor)
        if active_api_reply_error_code:
            log_message(f'error_code:{active_api_reply_error_code}',msgType='info',msgOffset='+1',msgColor=replycolor)
        if active_api_errorDesc:
            log_message(f'error_desc:{active_api_errorDesc}',msgType='info',msgOffset='+1',msgColor=replycolor)
        if active_api_errorStatus:
            log_message(f'error_status:{active_api_errorStatus}',msgType='info',msgOffset='+1',msgColor=replycolor)
        if active_api_errorSeverity:
            log_message(f'error_severity:{active_api_errorSeverity}',msgType='info',msgOffset='+1',msgColor=replycolor)
        if active_api_errorCode:
            log_message(f'error_code:{active_api_errorCode}',msgType='info',msgOffset='+1',msgColor=replycolor)
        if active_api_errorText:
            log_message(f'error_text:{active_api_errorText}',msgType='info',msgOffset='+1',msgColor=replycolor)
        if active_api_standard_reply:
            log_message(f'standard_reply:{active_api_standard_reply}',msgType='info',msgOffset='+1',msgColor=replycolor)
        if active_api_standard_result_output:
            log_message(f'standard_result_output:{active_api_standard_result_output}',msgType='info',msgOffset='+1',msgColor=Fore.WHITE)

        log_message('', msgType='FINISH', msgColor=Fore.YELLOW)
################################################################
def log_http_requestV2():
    global http_request
    global api_debug_http_request

    if api_debug_http_request:
        api=http_request.get('api',{}).get('api_name')
        api_prog=http_request.get('api',{}).get('api_prog')
        api_version=http_request.get('api',{}).get('api_version')
        api_desc_string=http_request.get('api',{}).get('api_desc_string')

        api_function=http_request.get('api',{}).get('api_function')
        api_return_value_desc=http_request.get('api',{}).get('api_return_value_desc')
        api_return_value_locator=http_request.get('api',{}).get('api_return_value_locator')

        url=http_request.get('input',{}).get('url')
        headers=http_request.get('input',{}).get('headers')
        params=http_request.get('input',{}).get('params')
        data=http_request.get('input',{}).get('data')
        function=http_request.get('input',{}).get('function')
        key=http_request.get('input',{}).get('key')

        log_message(f'http-request ({function}):',msgType='START',msgColor=Fore.YELLOW)
        log_message(f'api: {api_desc_string}',msgType='info-3',msgOffset='+1',msgColor=Fore.WHITE)
        log_message(f'api_function: {api_function}',msgType='info-3',msgOffset='+1',msgColor=Fore.LIGHTBLACK_EX)
        log_message(f'input key: {key}',msgType='info-3',msgOffset='+1',msgColor=Fore.LIGHTBLACK_EX)
        log_message(f'output_value_desc: {api_return_value_desc}',msgType='info-3',msgOffset='+1',msgColor=Fore.LIGHTBLACK_EX)
        log_message(f'output_value_locator: {api_return_value_locator}',msgType='info-3',msgOffset='+1',msgColor=Fore.LIGHTBLACK_EX)

        if url:
            log_message(f'url------{url}',msgType='info-3',msgOffset='+1',msgColor=Fore.LIGHTRED_EX)
        if headers:
            log_message(f'headers--{headers}',msgType='info-2',msgOffset='+1',msgColor=Fore.LIGHTBLUE_EX)
        if params:
            log_message(f'params---{params}',msgType='info-1',msgOffset='+1',msgColor=Fore.WHITE)
        if data:
            log_message(f'data-----{data}',msgType='info-3',msgOffset='+1',msgColor=Fore.CYAN)
        log_message('',msgType='FINISH',msgColor=Fore.YELLOW)
################################################################
def log_http_request_replyV2():
    global http_request
    global api_debug_http_request_reply

    if api_debug_http_request_reply:
        api=http_request.get('api',{}).get('api_name')
        api_prog=http_request.get('api',{}).get('api_prog')
        api_version=http_request.get('api',{}).get('api_version')
        api_desc_string=http_request.get('api',{}).get('api_desc_string')

        api_function=http_request.get('api',{}).get('api_function')
        api_return_value_desc=http_request.get('api',{}).get('api_return_value_desc')
        api_return_value_locator=http_request.get('api',{}).get('api_return_value_locator')

        success=http_request.get('success')
        status_code=http_request.get('status_code')
        message=http_request.get('message')
        output_string=http_request.get('output_string')
        error_message=http_request.get('error_message')
        error_severity=http_request.get('error_severity')
        error_code=http_request.get('error_code')
        error_source=http_request.get('error_source')
        return_value=http_request.get('return_value')
        data=http_request.get('data')
        reply=http_request.get('reply')
        key=http_request.get('output',{}).get('key')

        log_message(f'http-request reply:',msgType='START',msgColor=Fore.YELLOW)

        log_message(f'api: {api_desc_string}',msgType='info-3',msgOffset='+1',msgColor=Fore.WHITE)
        log_message(f'api_function: {api_function}',msgType='info-3',msgOffset='+1',msgColor=Fore.LIGHTBLACK_EX)
        log_message(f'input key: {key}',msgType='info-3',msgOffset='+1',msgColor=Fore.LIGHTBLACK_EX)
        log_message(f'output_value_desc: {api_return_value_desc}',msgType='info-3',msgOffset='+1',msgColor=Fore.LIGHTBLACK_EX)
        log_message(f'output_value_locator: {api_return_value_locator}',msgType='info-3',msgOffset='+1',msgColor=Fore.LIGHTBLACK_EX)

        if http_request.get('success'):
            replycolor = Fore.GREEN
        else:
            replycolor = Fore.RED

        log_message(f'status code:{status_code}',msgType='info',msgOffset='+1',msgColor=Fore.WHITE)
        log_message(f'success:{success}',msgType='info',msgOffset='+1',msgColor=replycolor)
        log_message(f'output key: {key}',msgType='info-3',msgOffset='+1',msgColor=Fore.LIGHTBLACK_EX)

        log_message(f'message:{message}',msgType='info',msgOffset='+1',msgColor=replycolor)
        log_message(f'output_string:{output_string}',msgType='info',msgOffset='+1',msgColor=replycolor)
        log_message(f'return_value:{return_value}',msgType='info',msgOffset='+1',msgColor=replycolor)
        log_message(f'data:{data}',msgType='info',msgOffset='+1',msgColor=replycolor)
        if error_message:
            log_message(f'error_message:{error_message}',msgType='info',msgOffset='+1',msgColor=replycolor)
        if error_severity:
            log_message(f'error_severity:{error_severity}',msgType='info',msgOffset='+1',msgColor=replycolor)
        if error_code:
            log_message(f'error_code:{error_code}',msgType='info',msgOffset='+1',msgColor=replycolor)
        if error_source:
            log_message(f'error_source:{error_source}',msgType='info',msgOffset='+1',msgColor=replycolor)
        log_message(f'reply:{reply}',msgType='info',msgOffset='+1',msgColor=Fore.WHITE)
        log_message('', msgType='FINISH', msgColor=Fore.YELLOW)
################################################################
def log_api_result(what='', val='',api=''):
    global active_api
    global active_api_prog
    global api_debug_result

    api_prog = whosdaddy()
    if api_prog != active_api_prog:
        api = whosapi(api_prog)
        get_api_debug_levels(api)

    if api_debug_result:
        log_message(f'result: {what}={val}',msgType='info',msgOffset='+1',msgColor=Fore.LIGHTGREEN_EX)
################################################################
def log_api_output(what='', val='', msg='', api=''):
    global active_api
    global active_api_prog
    global api_debug_output

    api_prog = whosdaddy()
    if api_prog != active_api_prog:
        api = whosapi(api_prog)
        get_api_debug_levels(api)

    if api_debug_output:
        if msg:
            log_message(f'output: {msg}', msgType='info', msgOffset='+1', msgColor=Fore.LIGHTYELLOW_EX)
        else:
            log_message(f'output: {what}={val}',msgType='info',msgOffset='+1',msgColor=Fore.LIGHTYELLOW_EX)
################################################################
def log_api_output_result(what='', val='', msg='', api=''):
    global active_api
    global active_api_prog
    global api_debug_output

    api_prog = whosdaddy()
    if api_prog != active_api_prog:
        api = whosapi(api_prog)
        get_api_debug_levels(api)

    if api_debug_output:
        if msg:
            log_message(f'{msg}', msgType='info', msgOffset='+1', msgColor=Fore.LIGHTWHITE_EX)
        else:
            log_message(f'{what} {val}',msgType='info',msgOffset='+1',msgColor=Fore.LIGHTWHITE_EX)
################################################################
def log_api_interim_result(what='', val='', msg='', api=''):
    global active_api
    global active_api_prog
    global api_debug_interim_result

    api_prog = whosdaddy()
    if api_prog != active_api_prog:
        api = whosapi(api_prog)
        get_api_debug_levels(api)

    if api_debug_interim_result:
        if msg:
            log_message(f'{msg}', msgType='info', msgOffset='+1', msgColor=Fore.LIGHTCYAN_EX)
        else:
            log_message(f'{what}={val}',msgType='info',msgOffset='+1',msgColor=Fore.LIGHTCYAN_EX)
################################################################
def log_api_input_param(what='', val='', api=''):
    global active_api
    global active_api_prog
    global api_debug_input_param

    api_prog = whosdaddy()
    if api_prog != active_api_prog:
        api = whosapi(api_prog)
        get_api_debug_levels(api)

    if api_debug_input_param:
        log_message(f'input: {what}={val}',msgType='info',msgOffset='+1',msgColor=Fore.MAGENTA)
################################################################
def log_api_output_param(what='', val='', api=''):
    global active_api
    global active_api_prog
    global api_debug_output_param
    
    api_prog = whosdaddy()
    if api_prog != active_api_prog:
        api = whosapi(api_prog)
        get_api_debug_levels(api)

    if api_debug_output_param:
        log_message(f'output_param: {what}={val}',msgType='info',msgOffset='+1',msgColor=Fore.GREEN)
################################################################
def log_api_config_param(bank, what='', val='', api=''):
    global active_api
    global active_api_prog
    global api_debug_config_param
    
    api_prog = whosdaddy()
    if api_prog != active_api_prog:
        api = whosapi(api_prog)
        get_api_debug_levels(api)

    if api_debug_config_param:
        log_message(f'config_param: {bank} {what}={val}',msgType='info',msgOffset='+1',msgColor=Fore.RED)
################################################################
def log_api_setup_param(what='', val='', api=''):
    global active_api
    global active_api_prog
    global api_debug_setup_param
    
    api_prog = whosdaddy()
    if api_prog != active_api_prog:
        api = whosapi(api_prog)
        get_api_debug_levels(api)

    if api_debug_setup_param:
        log_message(f'setup_param: {what}={val}',msgType='info',msgOffset='+1',msgColor=Fore.WHITE)
################################################################
################################################################
################################################################
### api support functions                                    ###
################################################################
################################################################
################################################################
def hb_get_configuration_param(what, configuration, thisbank):
    #global master_configuration
    process = 'hb_get_configuration_param'
    paramvalue = configuration.get(what, '')
    log_api_config_param(thisbank, what, paramvalue)
    #print(process,thisbank,what,':',paramvalue)
    return paramvalue
################################################################
def hb_get_parameters(api):
    global master_configuration
    global active_api
    global active_api_prog
    global master_api_prefix

    process='get_parameters'
    log_process_start(process)

    active_api = api
    active_api_prog = f'{master_api_prefix}{active_api}'

    # api_prog = whosdaddy()
    # if api_prog != active_api_prog:
    #     api = whosapi(api_prog)
    #     get_api_debug_levels(api)
    #     active_api = api
    #     active_api_prog = api_prog

    log_api_setup_param('active_api_prog',active_api_prog)

    bankCodeName='bankofcyprus'
    log_api_setup_param('bankCodeName',bankCodeName)
    
    ts = time.time()
    currentTimeStamp = datetime.datetime.fromtimestamp(ts).strftime('%Y%m%d%H%M%S')

    bankID=hb_get_configuration_param('bankID',master_configuration,bankCodeName)
    log_api_setup_param('bankID',bankID)

    bankName=hb_get_configuration_param('bankName',master_configuration,bankCodeName)
    redirect_uri=hb_get_configuration_param('redirect_uri',master_configuration,bankCodeName)
    app_name=hb_get_configuration_param('application_name',master_configuration,bankCodeName)
    client_id=hb_get_configuration_param('client_id',master_configuration,bankCodeName)
    client_secret=hb_get_configuration_param('client_secret',master_configuration,bankCodeName)
    api_uri=hb_get_configuration_param('api_uri',master_configuration,bankCodeName)
    journeyId=hb_get_configuration_param('journeyId',master_configuration,bankCodeName)
    originSourceId=hb_get_configuration_param('originSourceId',master_configuration,bankCodeName)
    originChannelId=hb_get_configuration_param('originChannelId',master_configuration,bankCodeName)
    originDeptId=hb_get_configuration_param('originDeptId',master_configuration,bankCodeName)
    originUserId=hb_get_configuration_param('originUserId',master_configuration,bankCodeName)
    originEmployeeId=hb_get_configuration_param('originEmployeeId',master_configuration,bankCodeName)
    originTerminalId=hb_get_configuration_param('originTerminalId',master_configuration,bankCodeName)
    correlationId=hb_get_configuration_param('correlationId',master_configuration,bankCodeName)
    lang=hb_get_configuration_param('lang',master_configuration,bankCodeName)
    tppId=hb_get_configuration_param('tppId',master_configuration,bankCodeName)

    functionRequest = 'get'
    apilevel = ''
    apikeysource = ''
    if api=='get_access_token':
        endpoint = 'df-boc-org-sb/sb/psd2/oauth2/token'
        apilevel = 'access'
        apikeysource = 'result'

    elif api=='get_subscriptionId':
        endpoint = 'df-boc-org-sb/sb/psd2/v1/subscriptions'
        apilevel = 'subscription'
        apikeysource = 'result'
    elif api=='get_subscription_details':
        endpoint = 'df-boc-org-sb/sb/psd2/v1/subscriptions/{}'
        apilevel = 'subscription'
        apikeysource = 'url_param'
    elif api=='commit_subscription':
        endpoint = 'df-boc-org-sb/sb/psd2/v1/subscriptions/{}'
        apilevel = 'subscription'
        apikeysource = 'url_param'
    elif api=='get_account_subscriptions':
        endpoint = 'df-boc-org-sb/sb/psd2/v1/subscriptions/accounts/{}'
        apilevel = 'subscription'
        apikeysource = 'url_param'
    elif api=='delete_subscription':
        endpoint = 'df-boc-org-sb/sb/psd2/v1/subscriptions/{}'
        apilevel = 'subscription'
        apikeysource = 'url_param'
        functionRequest = 'delete'

    elif api=='get_customerConsent':
        endpoint = 'https://sandbox-apis.bankofcyprus.com/df-boc-org-sb/sb/psd2/oauth2/authorize'
        apilevel = 'authorization'
        apikeysource = 'result'
    elif api=='get_authorization_token':
        endpoint = 'df-boc-org-sb/sb/psd2/oauth2/token'
        apilevel = 'authorization'
        apikeysource = 'result'

    elif api=='get_subscription_Accounts':
        endpoint = 'df-boc-org-sb/sb/psd2/v1/accounts'
        apilevel = 'subscription'
        apikeysource = 'header'
    elif api=='get_subscription_customers':
        endpoint = 'df-boc-org-sb/sb/psd2/v1/customers'
        apilevel = 'subscription'
        apikeysource = 'header'
    elif api=='get_Accounts_List':
        endpoint = 'df-boc-org-sb/sb/psd2/v1/accounts'
        apilevel = 'subscription'
        apikeysource = 'header'
    elif api=='get_account_details':
        endpoint = 'df-boc-org-sb/sb/psd2/v1/accounts/{}'
        apilevel = 'account'
        apikeysource = 'url_param'
    elif api=='get_account_transactions':
        endpoint = 'df-boc-org-sb/sb/psd2/v1/accounts/{}/statement'
        apilevel = 'account'
        apikeysource = 'url_param'
    elif api=='get_account_balances':
        endpoint = 'df-boc-org-sb/sb/psd2/v1/accounts/{}/balance'
        apilevel = 'account'
        apikeysource = 'url_param'
    elif api=='get_payments':
        endpoint = 'df-boc-org-sb/sb/psd2/v1/payments/accounts/{}'
        apilevel = 'account'
        apikeysource = 'url_param'

    elif api=='get_payment_jws_signature':
        endpoint = 'df-boc-org-sb/sb/jwssignverifyapi/sign'
        functionRequest = 'post'
        apilevel = 'payment'
        apikeysource = 'result'

    elif api=='payment_create':
        endpoint = 'df-boc-org-sb/sb/psd2/v1/payments'
        functionRequest = 'post'
        apilevel = 'payment'
        apikeysource = 'paymentId'

    elif api=='payment_checkfunds':
        endpoint = 'df-boc-org-sb/sb/psd2/v1/payments/fundAvailability'
        functionRequest = 'post'
        apilevel = 'payment'
        apikeysource = 'result'

    elif api=='authorize_payment':
        endpoint = 'df-boc-org-sb/sb/psd2/v1/payments/{}/authorize'
        functionRequest = 'post'
        apilevel = 'payment'
        apikeysource = 'url_param'

    elif api=='get_payment_details':
        endpoint = 'df-boc-org-sb/sb/psd2/v1/payments/{}'
        functionRequest = 'get'
        apilevel = 'payment'
        apikeysource = 'url_param'
    elif api=='get_payment_status':
        endpoint = 'df-boc-org-sb/sb/psd2/v1/payments/{}/status'
        functionRequest = 'get'
        apilevel = 'payment'
        apikeysource = 'url_param'
    elif api=='delete_payment':
        endpoint = 'df-boc-org-sb/sb/psd2/v1/payments/{}'
        functionRequest = 'delete'
        apilevel = 'payment'
        apikeysource = 'url_param'
    else:
        endpoint = 'df-boc-org-sb/????????????????'
        apilevel = '?'
        apikeysource = '?'
    
    #log_api_value('api',api)

    log_api_setup_param('endpoint',endpoint)

    params={
        'bankCodeName'      :bankCodeName
        ,'bankID'           :bankID   
        ,'bankName'         :bankName
        ,'app_Name'         :app_name
        ,'client_id'        :client_id
        ,'client_secret'    :client_secret
        ,'redirect_uri'     :redirect_uri
        ,'api'              :api
        ,'api_uri'          :api_uri
        ,'endpoint'         :endpoint
        ,'function'         :functionRequest
        ,'tppId'            :tppId
        ,'journeyId'        :journeyId
        ,'originSourceId'   :originSourceId
        ,'originChannelId'  :originChannelId
        ,'originDeptId'     :originDeptId
        ,'originUserId'     :originUserId
        ,'originEmployeeId' :originEmployeeId
        ,'originTerminalId' :originTerminalId
        ,'correlationId'    :correlationId
        ,'lang'             :lang
        ,'currentTimeStamp' :datetime.datetime.fromtimestamp(ts).strftime('%Y%m%d%H%M%S')
        ,'apiLevel'         :apilevel
        ,'apiKeySource'     :apikeysource
        # ,'debuglevel_one'   :debuglevel_one
        # ,'debuglevel_two'   :debuglevel_two
        # ,'debuglevel_three' :debuglevel_three
    }

    log_api_setup_param('api_params',params)

    #log_api_finish()
    return params
################################################################
def hb_prepare_request_standard(access_token,subscriptionId,api_params,url_parameter=''):
    global active_api_level
    global active_api_keysource
    global active_api_key
    global active_api
    global active_api_prog

    process='prepare_standard_request'
    log_process_start(process)

    api_prog = whosdaddy()
    if api_prog != active_api_prog:
        api = whosapi(api_prog)
        get_api_debug_levels(api)
        active_api = api
        active_api_prog = api_prog

    log_api_setup_param('active_api_prog',active_api_prog)
    
    request_function = api_params['function']
    
    headers = {
        'content-type': 'application/json',
        'accept': 'application/json',
        #'app_name': api_params['app_Name'],
        'journeyId': api_params['journeyId'],
        #'originSourceId': api_params['originSourceId'], 
        #'originChannelId': api_params['originChannelId'],
        #'originDeptId': api_params['originDeptId'],
        #'originUserId': api_params['originUserId'],
        #'originEmployeeId':api_params['originEmployeeId'],
        #'originTerminalId': api_params['originTerminalId'],
        #'correlationId': api_params['correlationId'],
        #'lang': api_params['lang'],
        'tppId': api_params['tppId'],
        'timeStamp': api_params['currentTimeStamp'],
        #'Authorization': 'Bearer {}'.format(access_token),
        #'subscriptionId': subscriptionId,
        #'lang': ''
    }
    #log_api_setup_param('headers',headers)

    if subscriptionId:
        if subscriptionId!='':
            header_subscriptionId={'subscriptionId': subscriptionId}
            headers.update(header_subscriptionId)
    if access_token:
        if access_token!='':
            header_token={'Authorization': 'Bearer {}'.format(access_token)}
            headers.update(header_token)
    if api_params['originSourceId'] !='':
        headers.update({'originSourceId': api_params['originSourceId']})
    if api_params['originUserId'] !='':
        headers.update({'originUserId': api_params['originUserId']})
    if api_params['originEmployeeId'] !='':
        headers.update({'originEmployeeId': api_params['originEmployeeId']})
    if api_params['originChannelId'] !='':
        headers.update({'originChannelId': api_params['originChannelId']})
    if api_params['originDeptId'] !='':
        headers.update({'originDeptId': api_params['originDeptId']})
    if api_params['originChannelId'] !='':
        headers.update({'originChannelId': api_params['originChannelId']})
    if api_params['originTerminalId'] !='':
        headers.update({'originTerminalId': api_params['originTerminalId']})
    if api_params['correlationId'] !='':
        headers.update({'correlationId': api_params['correlationId']})
    if api_params['lang'] !='':
        headers.update({'lang': api_params['lang']})
    if api_params['lang'] !='':
        headers.update({'lang': api_params['lang']})

    #log_api_setup_param('headers',headers)

    params = {
        'client_id': api_params['client_id'],
        'client_secret': api_params['client_secret'],
    }
    #log_api_setup_param('params',params)

    active_api_level = api_params['apiLevel']
    active_api_keysource = api_params['apiKeySource']

    log_api_setup_param('active_api_level',active_api_level)
    log_api_setup_param('active_api_keysource',active_api_keysource)
    
    active_api_key = None
    # if active_api_keysource in ('', '?'):
    #     active_api_key = f'{active_api_level}={url_parameter}'
    if active_api_level == 'access':
        active_api_key = api_params['client_id']
    elif active_api_level == 'subscription':
        active_api_key = headers.get('subscriptionId', None)

    if active_api_keysource == 'url_param':
        active_api_key = url_parameter
    
    log_api_setup_param('active_api_key',active_api_key)
    
    url=api_params['api_uri']+api_params['endpoint'].format(url_parameter)
    log_api_setup_param('api_url',url)

    request_params={
        'headers'       :headers
        ,'parameters'   :params
        ,'url'          :url
        ,'function'     :request_function
    }
    #log_api_setup_param('request_params',request_params)

    return request_params
################################################################
def hb_standard_http_request(api='',function='get', url='', headers='', params='', data=''):
    global active_api
    global active_api_prog
    global active_api_reply
    global active_api_return_OK
    global active_api_reply_code
    global active_api_reply_text
    global active_api_reply_json
    global active_api_reply_error_text
    global active_api_reply_error_code
    global active_api_errorDesc
    global active_api_errorStatus
    global active_api_errorSeverity
    global active_api_errorCode
    global active_api_errorText
    global active_api_standard_result_output
    global active_api_standard_reply
    global master_http_ok_code
    global api_debug_start
    global api_debug_finish
    global active_api_level
    global active_api_keysource
    global active_api_key

    process='standard_http_request'

    api_prog = whosdaddy()
    if api_prog != active_api_prog:
        api = whosapi(api_prog)
        get_api_debug_levels(api)
        active_api = api
        active_api_prog = api_prog

    #log request
    log_http_request(api=active_api, function=function, url=url,headers=headers,params=params,data=data)

    #http request
    if function=='get':
        r = requests.get(url,headers=headers,params=params,data=data)
    elif function=='post':
        r = requests.post(url,headers=headers,params=params,data=data)
    elif function=='delete':
        r = requests.delete(url,headers=headers,params=params,data=data)
    elif function=='patch':
        r = requests.patch(url,headers=headers,params=params,data=data)
    else:
        r = requests.get(url,headers=headers,params=params,data=data)

    active_api_reply_code=r.status_code
    active_api_reply_text = r.text
    try:
        active_api_reply_json = r.json()
    except:
        active_api_reply_json = {'reply_text':r.text}

    active_api_reply_error_text = ''
    active_api_reply_error_code = 0
    active_api_errorDesc = ''
    active_api_errorStatus = ''
    active_api_errorSeverity =''
    active_api_errorCode = ''
    active_api_errorText = ''

    if active_api_keysource == 'result':
        if not active_api_key:
            active_api_key = 'x'
    # if not active_api_reply_json and not r.text:
    #     active_api_reply_error_text = r.text
    #     active_api_reply_error_code = r.status_code
    #     active_api_errorDesc = f'{active_api_prog} return empty result'
    #     active_api_errorStatus = ''
    #     active_api_errorSeverity = 'error'
    #     active_api_errorCode = 'LTF0001'
    #     active_api_errorText = f'{active_api_errorCode} ({active_api_errorSeverity}) {active_api_errorDesc} ({active_api_errorStatus}) '
    #     #msg=f'{active_api_prog} failed with reply code {r.status_code} error_text:{active_api_reply_text}'
    #     #log_message(msg, msgType='ERROR')

    
    # {
    #     "type": "object",
    #     "properties": {
    #         "fatalError": {
    #             "type": "boolean"
    #         },
    #         "error": {
    #             "$ref": "#\/definitions\/Error"
    #         }
    #     }
    # }

    #check httprequest reply
    if r.status_code == master_http_ok_code:
        active_api_return_OK = True
        active_api_standard_reply = api_standard_success_reply(msg='OK', return_value=active_api_key, return_data=active_api_reply_json, api=api)
    else:
        if not active_api_reply_json.get("error"):
            active_api_return_OK = True
            active_api_standard_reply = api_standard_success_reply(msg='OK', return_value=active_api_key, return_data=active_api_reply_json, api=api)
        else:
            active_api_return_OK = False
            active_api_reply_error_text = active_api_reply_text
            active_api_reply_error_code = r.status_code
            #{ "fatalError":true, "error":{ "code":"400", "severity":"error", "description":"Bad Request", "additionalDetails":[ { "errorCode":"MSSUB008", "severity":"error", "status":"SubscriptionId- Subid000001-1558194968436", "description":"Subscription Status is already revoked" } ] } }
            active_api_errorDesc = r.json().get("error").get("additionalDetails")[0].get("description")
            active_api_errorStatus = r.json().get("error").get("additionalDetails")[0].get("status")
            active_api_errorSeverity = r.json().get("error").get("additionalDetails")[0].get("severity")
            active_api_errorCode = r.json().get("error").get("additionalDetails")[0].get("errorCode")
            active_api_errorText = f'{active_api_errorCode} ({active_api_errorSeverity}) {active_api_errorDesc} ({active_api_errorStatus}) '
            #msg=f'{active_api_prog} failed with reply code {r.status_code} error_text:{active_api_reply_text}'
            #log_message(msg, msgType='ERROR')
            active_api_standard_reply = api_standard_fail_reply(errormsg=active_api_errorText, return_value=active_api_key, errors=active_api_reply_json, api=api)

    s1=active_api_standard_reply.get('status','?')
    s2=active_api_standard_reply.get('message','?')
    s3 = active_api_standard_reply.get('return_value', '?')
    s3=''
    s4=active_api_standard_reply.get('api_prog','?')+' '+active_api_standard_reply.get('api_version','?')
    active_api_standard_result_output = f'{s1}:{s2} {s3} {s4}'
 
    #log reply
    log_http_request_reply(reply=r,api=active_api, )

    return r
################################################################
def hb_standard_http_requestV2(api='',function='get', url='', headers='', params='', data=''):
    global active_api
    global active_api_prog
    global active_api_reply
    global active_api_return_OK
    global active_api_reply_code
    global active_api_reply_text
    global active_api_reply_json
    global active_api_reply_error_text
    global active_api_reply_error_code
    global active_api_errorDesc
    global active_api_errorStatus
    global active_api_errorSeverity
    global active_api_errorCode
    global active_api_errorText
    global active_api_standard_result_output
    global active_api_standard_reply
    global master_http_ok_code
    global api_debug_start
    global api_debug_finish
    global active_api_level
    global active_api_keysource
    global active_api_key
    global http_request

    process='standard_http_request'

    api_prog = whosdaddy()
    if api_prog != active_api_prog:
        api = whosapi(api_prog)
        get_api_debug_levels(api)
        active_api = api
        active_api_prog = api_prog

    api_version = master_api_properties.get(active_api,{}).get('version', '0.1')
    api_function = master_api_properties.get(active_api,{}).get('function', active_api)
    api_desc_string = f'{active_api} version {api_version} {api_prog}'
    api_return_value_desc = master_api_properties.get(active_api,{}).get('return_entity','')
    api_return_value_locator = master_api_properties.get(active_api,{}).get('return_entity_locator','')

    http_request = {}
    http_request.update({'success':False})
    http_request.update({'message':'?'})
    http_request.update({'output_string':'?'})
    http_request.update({'data':{}})
    #http_request.update({'error_message':''})
    #http_request.update({'error_severity':''})
    #http_request.update({'error_code':''})
    #http_request.update({'error_source':''})
    http_request.update({'reply':{}})
    http_request.update({'return_value':''})
    http_request.update({'status_code':000})
    http_request.update({'api':{}})
    http_request.update({'input':{}})
    http_request.update({'output':{}})

    http_request.get('api').update({'api_name':active_api})
    http_request.get('api').update({'api_prog':active_api_prog})
    http_request.get('api').update({'api_version':api_version})
    http_request.get('api').update({'api_function':api_function})
    http_request.get('api').update({'api_desc_string':api_desc_string})
    http_request.get('api').update({'api_return_value_desc':api_return_value_desc})
    http_request.get('api').update({'api_return_value_locator':api_return_value_locator})

    http_request.get('input').update({'url':url})
    http_request.get('input').update({'headers':headers})
    http_request.get('input').update({'params':params})
    http_request.get('input').update({'data':data})
    http_request.get('input').update({'function':function})
    http_request.get('input').update({'key':active_api_key})

    #log request
    log_http_requestV2()

    #http request
    if function=='get':
        r = requests.get(url,headers=headers,params=params,data=data)
    elif function=='post':
        r = requests.post(url,headers=headers,params=params,data=data)
    elif function=='delete':
        r = requests.delete(url,headers=headers,params=params,data=data)
    elif function=='patch':
        r = requests.patch(url,headers=headers,params=params,data=data)
    else:
        r = requests.get(url,headers=headers,params=params,data=data)

    http_request.update({'status_code':r.status_code})
    http_request.get('output').update({'status_code':r.status_code})
    http_request.get('output').update({'text':r.text})
    active_api_reply_code=r.status_code
    active_api_reply_text = r.text
    try:
        active_api_reply_json = r.json()
        http_request.get('output').update({'data':r.json()})
        http_request.update({'data':r.json()})
    except:
        rjson = {'reply_text':r.text}
        active_api_reply_json = rjson
        http_request.get('output').update({'data':rjson})
        http_request.update({'data':{}})

    #check httprequest reply success
    if r.status_code == master_http_ok_code or r.status_code in (201,200):
        http_request.update({'success':True})
        active_api_return_OK = True
    else:
        if not active_api_reply_json.get("error"):
            http_request.update({'success':True})
            active_api_return_OK = True
        else:
            http_request.update({'success':False})
            active_api_return_OK = False

    active_api_reply_error_text = ''
    active_api_reply_error_code = 0
    active_api_errorDesc = ''
    active_api_errorStatus = ''
    active_api_errorSeverity =''
    active_api_errorCode = ''
    active_api_errorText = ''

    if active_api_keysource == 'result':
        if not active_api_key:
            active_api_key = '?'

    ret_value = None
    if active_api_return_OK:
        if api_return_value_locator:
            ret_value = http_request.get('data',{}).get(api_return_value_locator)
    
    if ret_value:
        active_api_key = ret_value
        http_request.update({'return_value':active_api_key})

    http_request.get('output').update({'key':active_api_key})

    # {
    #     "type": "object",
    #     "properties": {
    #         "fatalError": {
    #             "type": "boolean"
    #         },
    #         "error": {
    #             "$ref": "#\/definitions\/Error"
    #         }
    #     }
    # }

    #check httprequest reply
    if active_api_return_OK:
        active_api_standard_reply = api_standard_success_reply(msg='OK', return_value=active_api_key, return_data=active_api_reply_json, api=api)
        http_request.get('output').update({'reply':active_api_standard_reply})
        http_request.update({'message':'OK'})
    else:
            active_api_reply_error_text = active_api_reply_text
            active_api_reply_error_code = r.status_code
            #{ "fatalError":true, "error":{ "code":"400", "severity":"error", "description":"Bad Request", "additionalDetails":[ { "errorCode":"MSSUB008", "severity":"error", "status":"SubscriptionId- Subid000001-1558194968436", "description":"Subscription Status is already revoked" } ] } }
            active_api_errorDesc = r.json().get("error").get("additionalDetails")[0].get("description")
            active_api_errorStatus = r.json().get("error").get("additionalDetails")[0].get("status")
            active_api_errorSeverity = r.json().get("error").get("additionalDetails")[0].get("severity")
            active_api_errorCode = r.json().get("error").get("additionalDetails")[0].get("errorCode")
            active_api_errorText = f'{active_api_errorCode} ({active_api_errorSeverity}) {active_api_errorDesc} ({active_api_errorStatus}) '
            #msg=f'{active_api_prog} failed with reply code {r.status_code} error_text:{active_api_reply_text}'
            #log_message(msg, msgType='ERROR')
            active_api_standard_reply = api_standard_fail_reply(errormsg=active_api_errorText, return_value=active_api_key, errors=active_api_reply_json, api=api)
            http_request.update({'message':active_api_errorText})
            http_request.get('output').update({'reply':active_api_standard_reply})
            http_request.get('output').update({'error_message':active_api_errorText})
            http_request.get('output').update({'error_severity':active_api_errorSeverity})
            http_request.get('output').update({'error_code':active_api_errorCode})
            http_request.get('output').update({'error_source':active_api_errorStatus})
            http_request.update({'error_message':active_api_errorText})
            http_request.update({'error_severity':active_api_errorSeverity})
            http_request.update({'error_code':active_api_errorCode})
            http_request.update({'error_source':active_api_errorStatus})

    http_request.update({'reply':active_api_standard_reply})


    s1=api_function
    s2 = active_api_standard_reply.get('status', '?')
    if not active_api_standard_reply.get('status', '?') == 'success':
        s3 = active_api_standard_reply.get('message', '?')
        s4=''
    else:
        s3 = api_return_value_desc+' ='
        s4 = active_api_standard_reply.get('return_value')
    #s5=active_api_standard_reply.get('api_prog','?')+' '+active_api_standard_reply.get('api_version','?')
    active_api_standard_result_output = f'{s1} {s2} {s3} {s4}'
    http_request.update({'output_string':active_api_standard_result_output})
 
    #log reply
    log_http_request_replyV2()

    return http_request
################################################################

################################################################
################################################################
### bank apis                                                ###
################################################################
################################################################
################################################################

################################################################
### access tokens                                            ###
################################################################
def hb_get_access_tokenV2():
    global master_http_ok_code
    global active_access_token
    global active_api_prog

    api = 'get_access_token'

    #start
    log_api_start(api)

    #init output
    active_access_token = None

    #setup httprequest
    api_params = hb_get_parameters(api)
    request_params = hb_prepare_request_standard('', '', api_params)

    api_url = request_params['url']
    headers = request_params['headers']
    params = request_params['parameters']
    headers = {
        'accept': 'application/json'
    }
    payload = {
        'grant_type': 'client_credentials',
        'client_id': api_params['client_id'],
        'client_secret': api_params['client_secret'],
        'scope': 'TPPOAuth2Security'
    }

    #httprequest
    #r = hb_standard_http_request(api=api, function='post', url=api_url, headers=headers, params=None, data=payload)
    #httprequest
    r = hb_standard_http_requestV2(api=api, function='post', url=api_url,headers=headers, params=None, data=payload)
    if r.get('success'):
        active_access_token = r.get('data',{}).get('access_token',None)
        get_result = api_standard_success_reply(msg='OK. access token received', return_value=active_access_token, return_data=r.get('data',{}))
    else:
        active_access_token=None
        errormsg = 'get_acesss_token failed: '+r.get('error_message')
        get_result = api_standard_fail_reply(errormsg=errormsg, return_value=None, errors=r.get('data', {}))
        log_api_result(errormsg)
        return None

    if active_access_token:
        tokenStr = f'{active_access_token[:20]}...'
    else:
        tokenStr = '***NONE***'

    #setup output
    # if r.json():
    #     active_access_token = r.json().get('access_token')
    # if active_access_token:
    #     tokenStr = f'{active_access_token[:20]}...'
    # else:
    #     tokenStr = '***NONE***'

    #display output
    log_api_output_result('access_token', tokenStr, api=api)

    #finish
    log_api_finish()
    return get_result
#####################################################
def hb_get_access_token():
    global master_http_ok_code
    global active_access_token
    global active_api_prog

    api = 'get_access_token'

    #start
    log_api_start(api)

    #init output
    active_access_token = None

    #setup httprequest
    api_params = hb_get_parameters(api)
    request_params = hb_prepare_request_standard('', '', api_params)

    api_url = request_params['url']
    headers = request_params['headers']
    params = request_params['parameters']
    headers = {
        'accept': 'application/json'
    }
    payload = {
        'grant_type': 'client_credentials',
        'client_id': api_params['client_id'],
        'client_secret': api_params['client_secret'],
        'scope': 'TPPOAuth2Security'
    }

    #httprequest
    r = hb_standard_http_request(api=api, function='post', url=api_url, headers=headers, params=None, data=payload)
    x = r.json()
    print(x)
    {
        'token_type': 'bearer',
        'access_token': 'AAIkNTJlZTgyOGUtYTE4ZS00NTYwLWJmZWQtMmQ1MTU4ZTlhNTA32kgqazwtewn_Vnc0KQd56kiPDFUnv9GyvFcWhyXPmH7Hzn1xWb0GxPMMQ79f9TjnAY89O9nexH3owNNKee6JoBpPfAGpvDwLiRYKxf89pTZPNBCbEpbNiogIAUX8edqXnUMer3fsbpBjPUtOvIosDg',
        'expires_in': 3600,
        'consented_on': 1559644505,
        'scope': 'TPPOAuth2Security'
    }
    
    #setup output
    if r.json():
        active_access_token = r.json().get('access_token')
    if active_access_token:
        tokenStr = f'{active_access_token[:20]}...'
    else:
        tokenStr = '***NONE***'

    #display output
    log_api_output_result('access_token', tokenStr, api=api)

    #finish
    log_api_finish()
    return active_access_token
################################################################
def hb_get_authorization_token(access_token,authorization_code):
    global http_request
    global master_http_ok_code
    global active_access_token
    global active_authorization_token

    api='get_authorization_token'

    #start
    log_api_start(api)

    #input params
    log_api_input_param('authorization_code',authorization_code)

    #init output
    active_authorization_token = None
    authorization_token = None

    #setup httprequest
    api_params=hb_get_parameters(api)
    request_params=hb_prepare_request_standard(access_token,'',api_params)
    api_url=request_params['url']
    headers=request_params['headers']
    params=request_params['parameters']
    headers = {
        'accept': 'application/json'
    }
    payload = {
        'code': authorization_code,
        'client_id': api_params['client_id'],
        'client_secret': api_params['client_secret'],
        'grant_type': 'authorization_code',
        'scope': 'UserOAuth2Security'
    }

    #httprequest
    r = hb_standard_http_requestV2(api=api, function='post', url=api_url,headers=headers, params=None, data=payload)
    if r.get('success'):
        authorization_token = r.get('data',{}).get('access_token',None)
        get_result = api_standard_success_reply(msg='OK. subscription created', return_value=active_authorization_token, return_data=r.get('data',{}))
    else:
        errormsg = 'get_authorization_token failed: '+r.get('error_message')
        get_result = api_standard_fail_reply(errormsg=errormsg, return_value=None, errors=r.get('data', {}))
        log_api_result(errormsg)
        return None

    if authorization_token:
        tokenStr = f'{authorization_token[:20]}...'
    else:
        tokenStr = '***NONE***'

    #display output
    log_api_output_result('authorization_token', tokenStr, api=api)

    #finish
    log_api_finish()
    
    return authorization_token
################################################################
### subscription apis                                        ###
################################################################
def hb_get_subscription_details(access_token,subscriptionId):   
    global master_http_ok_code

    api='get_subscription_details'

    #start
    log_api_start(api)

    #input params
    log_api_input_param('subscriptionId',subscriptionId)

    #init output
    subscription_details = None

    api_params=hb_get_parameters(api)
    request_params=hb_prepare_request_standard(access_token,'',api_params,subscriptionId)
    api_url=request_params['url']
    headers=request_params['headers']
    params=request_params['parameters']
    payload = None

    #httprequest
    r = hb_standard_http_request(url=api_url, function='get', headers=headers, params=params, data=payload)

    #setup output
    if r.json():
        subscription_details = r.json()[0]
   
    if subscription_details:
        outputStr = json.dumps(subscription_details)
        subscriptionId = subscription_details.get('subscriptionId')
        status = subscription_details.get('status','?')
        key=f'{subscriptionId}-{status}'
        outputStr=f'{subscriptionId}-{status}'
    else:
        outputStr = '***NONE***'

    #display result
    log_api_result('subscription_details', subscription_details, api=api)
    #display output
    log_api_output_result('subscription_details', outputStr, api=api)

    #finish
    log_api_finish()
    return subscription_details
################################################################
def hb_get_subscription_selectedAccounts(access_token,subscriptionId):   ###even if pending
    global master_http_ok_code

    #start
    api='get_subscription_selectedAccounts'
    log_api_start(api)

    #input params
    log_api_input_param('subscriptionId',subscriptionId)

    #init output
    selected_accounts=[]
    outputStr = ''
    
    #httprequest
    subscription_accounts = hb_get_subscription_details(access_token, subscriptionId)
    
    #setup output
    if subscription_accounts:
        selected_accounts=subscription_accounts[0]['selectedAccounts']
    if selected_accounts:
        outputStr = json.dumps(selected_accounts)
    else:
        outputStr = '***NO ACCOUNTS***'

    #display output
    log_api_output('subscription_selected_accounts', selected_accounts, api=api)

    #finish
    log_api_finish()
    return selected_accounts
################################################################
def hb_get_subscription_Accounts(access_token,subscriptionId):   

    api='get_subscription_Accounts'

    #start
    log_api_start(api)

    #input params
    log_api_input_param('subscriptionId',subscriptionId)

    #init output
    subscription_accounts = None
    outputStr = ''

    #setup httprequest
    api_params=hb_get_parameters(api)
    request_params=hb_prepare_request_standard(access_token,subscriptionId,api_params)
    api_url=request_params['url']
    headers=request_params['headers']
    params=request_params['parameters']

    #httprequest
    subscription_accounts = hb_standard_http_request(api=api, function='get', url=api_url,headers=headers,params=params)

    #setup output
    if subscription_accounts:
        outputStr = json.dumps(subscription_accounts)
    else:
        outputStr = '***NO ACCOUNTS***'

    #display output
    log_api_output('subscription_accounts', outputStr, api=api)

    #finish
    log_api_finish()
    return subscription_accounts
################################################################
def hb_get_subscription_customers(access_token,subscriptionId):   
    api='get_subscription_customers'
    log_api_start(api)

    #input params
    log_api_input_param('subscriptionId',subscriptionId)

    #init output
    customers=[]
    outputStr = ''

    #setup httprequest
    api_params=hb_get_parameters(api)
    request_params=hb_prepare_request_standard(access_token,subscriptionId,api_params)
    api_url=request_params['url']
    headers=request_params['headers']
    params=request_params['parameters']

    #httprequest
    #subscription_customers = hb_standard_http_request(api=api, function='get', url=api_url,headers=headers,params=params)
    r = hb_standard_http_requestV2(api=api, function='get', url=api_url,headers=headers, params=params, data=None)
    if r.get('success'):
        xcustomers=r.get('data',{})
        customers = xcustomers.get('customers',[])
        create_result = api_standard_success_reply(msg='OK. get customers', return_value=customers, return_data=r.get('data',{}))
    else:
        errormsg = 'get customers failed: '+r.get('error_message')
        create_result = api_standard_fail_reply(errormsg=errormsg, return_value=None, errors=r.get('data',{}))
        customers = []

    # #setup output
    # if subscription_customers:
    #     customers=subscription_customers[0]['customers']
    if customers:
        outputStr = json.dumps(customers)
    else:
        outputStr = '***NO ACCOUNTS***'

    #display output
    log_api_output_result('subscription_customers', customers, api=api)

    #finish
    log_api_finish()
    return customers
################################################################
################################################################
### accounts apis                                            ###
################################################################
def hb_get_subscription_accounts(access_token,subscriptionId):   

    #start
    api='get_Accounts_List'
    log_api_start(api)

    #input params
    log_api_input_param('subscriptionId',subscriptionId)

    #init output
    subscription_accounts={}
    outputStr = ''


    #setup httprequest
    api_params=hb_get_parameters(api)
    request_params=hb_prepare_request_standard(access_token,subscriptionId,api_params)
    api_url=request_params['url']
    headers=request_params['headers']
    params=request_params['parameters']

    #httprequest
    r = hb_standard_http_request(api=api, function='get', url=api_url,headers=headers,params=params)

    #setup output
    if r.status_code == master_http_ok_code:
        subscription_accounts = r.json()
        outputStr = json.dumps(subscription_accounts)
    else:
        outputStr = '***NO ACCOUNTS***'

    #display output
    log_api_output('subscription {subscriptionId} accounts list', outputStr, api=api)

    #finish
    log_api_finish()
    return subscription_accounts
################################################################
def hb_get_account_details(access_token, subscriptionId, accountId):
    #start
    api='get_account_details'
    log_api_start(api)

    #input params
    log_api_input_param('subscriptionId',subscriptionId)
    log_api_input_param('accountId',accountId)

    #init output
    account_details={}
    outputStr = ''


    #setup httprequest
    api_params=hb_get_parameters(api)
    request_params=hb_prepare_request_standard(access_token,subscriptionId,api_params,accountId)
    api_url=request_params['url']
    headers=request_params['headers']
    params=request_params['parameters']

    #httprequest
    r = hb_standard_http_request(api=api, function='get', url=api_url,headers=headers,params=params)

    #setup output
    if r.status_code == master_http_ok_code:
        account_details = r.json()
        outputStr = json.dumps(account_details)
    else:
        outputStr = '***NONE***'

    #display output
    log_api_output(f'account {accountId} details:', outputStr, api=api)

    #finish
    log_api_finish()
    return account_details
################################################################
def hb_get_account_balances(access_token, subscriptionId, accountId):
    api='get_account_balances'
    log_api_start(api)

    api_params=hb_get_parameters(api)
    request_params=hb_prepare_request_standard(access_token,subscriptionId,api_params,accountId)
    api_url=request_params['url']
    headers=request_params['headers']
    params=request_params['parameters']
    r = hb_standard_http_request(url=api_url,headers=headers,params=params)
    reply_code=r.status_code
    response = r.json()
    if not r.status_code == master_http_ok_code:
        error_text=r.text
        error_code=1
        response=None
    log_api_finish()
    return response
################################################################
def hb_get_account_transactions(access_token, subscriptionId, accountId,sdate='',edate='',ntrans=9999):
    api='get_account_transactions'
    log_api_start(api)

    api_params=hb_get_parameters(api)
    request_params=hb_prepare_request_standard(access_token,subscriptionId,api_params,accountId)
    api_url=request_params['url']
    headers=request_params['headers']
    params_standard=request_params['parameters']
    params_transactions = {
        'startDate': '01/01/2010'
        ,'endDate': '31/12/2018'
        ,'maxCount': ntrans
    }
    params = params_standard.copy()
    params.update(params_transactions)

    r = hb_standard_http_request(url=api_url,headers=headers,params=params)
    reply_code=r.status_code
    response = r.json()
    if not r.status_code == master_http_ok_code:
        error_text=r.text
        error_code=1
        response=None
    log_api_finish()
    return response
################################################################
def hb_get_account_subscriptions(access_token,accountId):
    api='get_account_subscriptions'
    log_api_start(api)

    #input params
    log_api_input_param('accountId',accountId)

    #init output
    account_subscriptions={}
    outputStr = ''

    #setup httprequest
    api_params=hb_get_parameters(api)
    request_params=hb_prepare_request_standard(access_token,'',api_params,accountId)
    api_url=request_params['url']
    headers=request_params['headers']
    params=request_params['parameters']

    #httprequest
    r = hb_standard_http_request(api=api, function='get', url=api_url,headers=headers,params=params,data=None)

    #setup output
    if r.status_code == master_http_ok_code:
        account_subscriptions = r.json()
        resultStr = json.dumps(account_subscriptions)
        outputStr = ''
        if account_subscriptions:
            for ix in range(0, len(account_subscriptions)):
                subscriptionId = account_subscriptions[ix].get('subscriptionId')
                status = account_subscriptions[ix].get('status', '?')
                outputStr=outputStr+f'\n   {ix+1}. {subscriptionId}-{status}'
    else:
        outputStr = '***NONE***'
        resultStr = '***NONE***'


    #display result
    log_api_result(f'account {accountId} subscriptions', resultStr, api=api)

    #display output
    log_api_output_result(f'account {accountId} subscriptions', outputStr, api=api)

    #finish
    log_api_finish()
    return account_subscriptions
################################################################
### payments apis                                            ###
################################################################
def hb_payment_fundsavailability(access_token,subscriptionId,payment):
    api='payment_checkfunds'
    log_api_start(api)

    api_params=hb_get_parameters(api)
    request_params=hb_prepare_request_standard(access_token,subscriptionId,api_params)
    api_url=request_params['url']
    headers=request_params['headers']
    params=request_params['parameters']

    paymentData=json.dumps(payment)

    #r = hb_standard_http_request(url=api_url,headers=headers, params=params, data=paymentData)
    #httprequest
    x= request_params.get('functionRequest')
    r = hb_standard_http_requestV2(api=api, function='post', url=api_url,headers=headers, params=params, data=paymentData)
    if not r.get('status') == 'success':                
        check_result = api_standard_success_reply(msg='OK. funds available', return_value=None, return_data=r.get('data',{}))
    else:
        errormsg = 'funds availavility chaeck failed: '+r.get('error_message')
        check_result = api_standard_fail_reply(errormsg=errormsg, return_value=None, errors=r.get('data',{}))

    #display result
    log_api_result(f'payment_checkfunds:', check_result)

    # #display output
    # log_api_output_result('subscriptionId',check_result.get('return_value'))

    #finish
    log_api_finish()
    
    return check_result

    # reply_code=r.status_code
    # response = r.json()
    # #print (r.text)

    # if not r.status_code == master_http_ok_code:
    #     error_text=r.text
    #     error_code=1
    #     response = None
    #     #print(error_text)
    #     errorDesc = r.json().get("error").get("additionalDetails")[0].get("description")
    #     errorStatus = r.json().get("error").get("additionalDetails")[0].get("status")
    #     errorSeverity = r.json().get("error").get("additionalDetails")[0].get("severity")
    #     errorCode = r.json().get("error").get("additionalDetails")[0].get("errorCode")
    #     response = f'ERROR-{errorSeverity} {errorCode} {errorDesc} {errorStatus} '
    #     # {"fatalError": true,
    #     # "error": {
    #     #     "code": "400", "severity": "error", "description": "Bad Request",
    #     #     "additionalDetails": [
    #     #         {"errorCode": "MSPMT006", "severity": "error", "status": "Account id-351012345671", "description": "Transaction Amount is greater than available balance for given account"}
    #     #         ]
    #     #     }
    #     # }        
    # else:
    #     response='OK'
    
    # log_api_finish()
    # return response
################################################################
def hb_get_payments(access_token, subscriptionId,accountId):
    api='get_payments'
    log_api_start(api)

    api_params=hb_get_parameters(api)
    request_params=hb_prepare_request_standard(access_token,subscriptionId,api_params,accountId)
    api_url=request_params['url']
    headers=request_params['headers']
    params=request_params['parameters']
    r = hb_standard_http_request(url=api_url,headers=headers,params=params)
    reply_code=r.status_code
    response = r.json()
    if not r.status_code == master_http_ok_code:
        error_text=r.text
        error_code=1
        response=None
    log_api_finish()
    return response
################################################################
def hb_get_payment_status(access_token,subscriptionId,payment_id):
    api='get_payment_status'
    log_api_start(api)

    api_params=hb_get_parameters(api)
    request_params=hb_prepare_request_standard(access_token,subscriptionId,api_params,payment_id)
    api_url=request_params['url']
    headers=request_params['headers']
    params=request_params['parameters']
    r = hb_standard_http_request(url=api_url,headers=headers,params=params)
    if not r.status_code == master_http_ok_code:
        raise Exception(r.text)
    payments = r.json()
    #res=print_result('payment_status=',payments)
    log_api_finish()
    return payments
################################################################
def hb_delete_payment(access_token,subscriptionId,payment_id):
    api='delete_payment'
    #start
    log_api_start(api)

    #input
    log_api_input_param('subscriptionId',subscriptionId)
    log_api_input_param('payment_id',payment_id)
    
    #api params
    api_params=hb_get_parameters(api)
    request_params=hb_prepare_request_standard(access_token,subscriptionId,api_params,payment_id)
    api_url=request_params['url']
    headers=request_params['headers']
    params=request_params['parameters']
    request_function = request_params['function']

    r = hb_standard_http_requestV2(api=api, function=request_function, url=api_url, headers=headers, params=params, data=None)
    #r = requests.delete(api_url, headers=headers, params=params)

    if not r.get('success'):
        errormsg = 'payment delete failed: '+r.get('error_message')
        delete_result = api_standard_fail_reply(errormsg=errormsg, return_value=None, errors=r.get('data',{}))
    else:
        delete_result = api_standard_success_reply(msg='OK. payment deleted', return_value=True, return_data=r.get('data',{}))
    # reply_code=r.status_code
    # #response = r.json()
    # if not r.status_code == master_http_ok_code:
    #     error_text=r.text
    #     error_code=1
    #     response=None
    #     response={'result':'ERROR', 'msg':error_text}
    # else:
    #     response={'result':'OK', 'msg':'deleted'}

    log_api_finish()
    return delete_result
################################################################
def hb_get_payment_details(access_token,subscriptionId,payment_id):
    api='get_payment_details'
    log_api_start(api)

    api_params=hb_get_parameters(api)
    request_params=hb_prepare_request_standard(access_token,subscriptionId,api_params,payment_id)
    api_url=request_params['url']
    headers=request_params['headers']
    params=request_params['parameters']
    r = hb_standard_http_request(url=api_url,headers=headers,params=params)
    reply_code=r.status_code
    response = r.json()
    if not r.status_code == master_http_ok_code:
        error_text=r.text
        error_code=1
        response=None
    #payment_details = r.json()
    #res=print_result('payment_details=',payment_details)
    log_api_finish()
    return response
################################################################
### create payment apis                                      ###
################################################################
def hb_get_payment_jws_signature(access_token, subscriptionId, DBaccountId ,CRaccountId,Amount,Currency,Details,endToEndId,terminalId,branch,refNumber,CRaccountBankId,CraccountName,CraccountAddress):
    api='get_payment_jws_signature'

    #start
    log_api_start(api)

    #input
    log_api_input_param('subscriptionId',subscriptionId)
    log_api_input_param('DBaccountId',DBaccountId)
    log_api_input_param('CRaccountBankId',CRaccountBankId)
    log_api_input_param('CRaccountId',CRaccountId)
    log_api_input_param('CraccountName',CraccountName)
    log_api_input_param('CraccountAddress',CraccountAddress)
    log_api_input_param('Amount',Amount)
    log_api_input_param('Currency',Currency)
    log_api_input_param('refNumber',refNumber)
    log_api_input_param('endToEndId',endToEndId)
    log_api_input_param('terminalId',terminalId)
    log_api_input_param('branch',branch)
    log_api_input_param('Details',Details)

    api_params=hb_get_parameters(api)
    request_params=hb_prepare_request_standard(access_token,subscriptionId,api_params)
    api_url=request_params['url']
    headers=request_params['headers']
    params=request_params['parameters']
    params.update({'subscriptionId': subscriptionId})    

    payment_request_json = {
        "debtor":{"bankId":"","accountId":DBaccountId},
        "creditor":{"bankId":CRaccountBankId,"accountId":CRaccountId,"name":CraccountName,"address":CraccountAddress},
        "transactionAmount":{"amount":Amount,"currency":Currency,"currencyRate":""},
        "paymentDetails":Details,
        "endToEndId":endToEndId,
        "terminalId":terminalId,
        "branch":branch,
        "executionDate":"",
        "valueDate":"",
        #"RUB":{"voCode":"lezeidne","BIK":"ublepipunzokcevjozejkedhanticew","INN":"topajimpopcuvirobil","correspondentAccount":"6226014357403233"}
        #"totalDebitAmount":{"amount":Amount,"currency":Currency,"currencyRate":""},
        "refNumber":refNumber
        }

    paymentRequest=json.dumps(payment_request_json)
    #the reverse is: payment_request_json=json.loads(paymentRequest)

    # if api_params.get('debuglevel_two',1)>0:
    #     print('url-----',api_url)
    #     print('params----',params)
    #     print('headers---',headers)
    #     print('data------',paymentRequest)

    #bobbi
    #functionRequest
    r = hb_standard_http_requestV2(api=api,function='post', url=api_url,headers=headers, params=params, data=paymentRequest)
    if r.get('success'):
        # response = r.json()
        # #{
        # #'payload': '...',
        # #'signatures': [
        #     #    {'protected': 'eyJhbGciOiJSUzI1NiJ9''signature': '...'}
        #     #]
        # #}
        response=r.get('data',{})
        payload = response['payload']
        signatures = response['signatures']
        log_api_output_result('payload =', payload)
        log_api_output_result('signatures =', signatures)
        signature_result = api_standard_success_reply(msg='OK. payment_jws_signature received', return_value=signatures, return_data=r.get('data',{}))
        log_api_result('init payment data =', r.get('data'))
    else:
        errormsg = 'init payement failed: '+r.get('error_message')
        signature_result = api_standard_fail_reply(errormsg=errormsg, return_value=None, errors=r.get('data',{}))
        # errormsg = 'subscription update failed: '+r.get('error_message')
        # log_api_result('update data', r.get('data'))
        # commit_result = api_standard_fail_reply(errormsg=errormsg, return_value=None, errors=r.get('data', {}))
        # errormsg = 'subscription create failed: '+r.get('error_message')
        # create_result = api_standard_fail_reply(errormsg=errormsg, return_value=None, errors=r.get('data',{}))

    #print(r)
    #reply_code=r.status_code
    #response = r.json()
    # if api_params.get('debuglevel_two',1)>0:
    #     print('results---',r.status_code,r.text)
    
    # if not r.get('success'):
    # #if not r.status_code == master_http_ok_code:
    #     error_text=r.text
    #     error_code=1
    #     response=None
    #     errorDesc = r.json().get("error").get("additionalDetails")[0].get("description")
    #     errorStatus = r.json().get("error").get("additionalDetails")[0].get("status")
    #     errorSeverity = r.json().get("error").get("additionalDetails")[0].get("severity")
    #     errorCode = r.json().get("error").get("additionalDetails")[0].get("errorCode")
    #     msg = f'ERROR- {errorSeverity} {errorCode} {errorStatus} {errorDesc}'
    #     response = {"error":msg}
    # else:
    #     response = r.json()
    #     #{
    #     #'payload': '...',
    #     #'signatures': [
    #         #    {'protected': 'eyJhbGciOiJSUzI1NiJ9''signature': '...'}
    #         #]
    #     #}
    #     payload = response['payload']

    #     print('payload=',payload)
    #     signatures = response['signatures']
    #     print('signatures=', signatures)
    #     print('response=',response)

    log_api_finish()
    return signature_result
################################################################
def hb_payment_create(access_token, subscriptionId, payload):
    api='payment_create'

    #start
    log_api_start(api)

    #input
    log_api_input_param('subscriptionId',subscriptionId)
    log_api_input_param('payload',payload)

    api_params=hb_get_parameters(api)
    request_params=hb_prepare_request_standard(access_token,subscriptionId,api_params)
    api_url=request_params['url']
    headers=request_params['headers']
    params=request_params['parameters']
    params.update({'subscriptionId': subscriptionId})    
    request_function = request_params['function']
    paymentData=json.dumps(payload)

    r = hb_standard_http_requestV2(api=api,function=request_function, url=api_url,headers=headers, params=params, data=paymentData)

    if not r.get('success'):
        errormsg = 'payment failed: '+r.get('error_message')
        payment_result = api_standard_fail_reply(errormsg=errormsg, return_value=None, errors=r.get('data',{}))
    else:
        payment_data = r.get('data',{})
        paymAuthNeeded=payment_data['authCodeNeeded']
        payment=payment_data['payment']
        paymentId=payment['paymentId']
        payment_result = api_standard_success_reply(msg='OK. payment created', return_value=paymentId, return_data=r.get('data',{}))
        log_api_result('payment result =', r.get('data'))
        log_api_output_result('paymentId =', paymentId)
        log_api_output_result('paymAuthNeeded =', paymAuthNeeded)
        #{
        #   "authCodeNeeded": true,
        #    "payment": {
        #        "paymentId": "PmtId000001_1518607567498",
        #        "transactionTime": "1511779237",
        #        "status": {
        #            "code": "PNDG",
        #            "description": [
        #                "Payment in pending status"
        #            ],
        #            "refNumber": "CYP12345"
        #        },
        #        "debtor": {
        #            "bankId": "",
        #            "accountId": "351012345671"
        #        },
        #        "creditor": {
        #            "bankId": "",
        #            "accountId": "351092345672",
        #            "name": null,
        #            "address": null
        #        },
        #        "transactionAmount": {
        #            "amount": 3.55,
        #            "currency": "EUR",
        #            "currencyRate": "string"
        #        },
        #        "charges": null,
        #        "totalCharges": "1100.00",
        #        "endToEndId": "string",
        #        "paymentDetails": "test sandbox ",
        #        "terminalId": "string",
        #        "branch": "",
        #        "RUB": null,
        #        "executionDate": "14/02/2018",
        #        "valueDate": "14/02/2018",
        #        "totalDebitAmount": null
        #    }
        #}

    log_api_finish()

    return payment_result
################################################################
def hb_authorize_payment(access_token, subscriptionId, paymentId,authorization_code):
    api='authorize_payment'

    #start
    log_api_start(api)

    #input
    log_api_input_param('subscriptionId',subscriptionId)
    log_api_input_param('paymentId',paymentId)
    log_api_input_param('paymentId',authorization_code)


    api_params=hb_get_parameters(api)
    request_params=hb_prepare_request_standard(access_token,subscriptionId,api_params,paymentId)
    api_url=request_params['url']
    headers=request_params['headers']
    params=request_params['parameters']
    params.update({'subscriptionId': subscriptionId})    

    auth = {"transactionTime": api_params['currentTimeStamp'],"authCode": authorization_code}
    authData=json.dumps(auth)
    
    request_function = request_params['function']

    r = hb_standard_http_requestV2(api=api, function=request_function, url=api_url, headers=headers, params=params, data=authData)
    if not r.get('success'):
        errormsg = 'payment authorization failed: '+r.get('error_message')
        payment_authorization_result = api_standard_fail_reply(errormsg=errormsg, return_value=None, errors=r.get('data',{}))
    else:
        log_api_result('payment result =', r.get('data'))
        response = r.get('data',{})
        paymRefNum=response['refNumber']
        paymStatus=response['code']
        paymStatusDesc=response['description']
        #result = {'result':'OK', 'msg':response}
        payment_authorization_result = api_standard_success_reply(msg='OK. payment authorized', return_value=paymRefNum, return_data=r.get('data',{}))

        log_api_output_result('paymRefNum =', paymRefNum)
        log_api_output_result('paymStatus =', paymStatus)
        log_api_output_result('paymStatusDesc =', paymStatusDesc)

    # reply_code=r.status_code
    # if api_params.get('debuglevel_two',1)>0:
    #     print('results---',r.status_code,r.text)

    # if not r.status_code == master_http_ok_code:
    #     response = r.json()
    #     error_code=1
    #     paymStatus = r.text
    #     result = {'result':'ERROR', 'msg':response}
    # else:
        #response = r.json()
        #{
        #  "code": "CLPT",
        #  "description": [
        #    " The transaction has passed all validations and was successfully posted in bank systems"
        #  ],
        #  "refNumber": "1524485123473408"
        #}
        # reply_code=r.status_code
        # response = r.json()

    log_api_finish()
    return payment_authorization_result
################################################################
def hb_make_payment(access_token, subscriptionId, DBaccountId, CRaccountId, Amount, Currency, Details, endToEndId, terminalId, branch, refNumber, CRaccountBankId,CraccountName,CraccountAddress):
    api='make_payment'
    #start
    log_api_start(api)

    #input
    log_api_input_param('subscriptionId',subscriptionId)
    log_api_input_param('DBaccountId',DBaccountId)
    log_api_input_param('CRaccountBankId',CRaccountBankId)
    log_api_input_param('CRaccountId',CRaccountId)
    log_api_input_param('CraccountName',CraccountName)
    log_api_input_param('CraccountAddress',CraccountAddress)
    log_api_input_param('Amount',Amount)
    log_api_input_param('Currency',Currency)
    log_api_input_param('refNumber',refNumber)
    log_api_input_param('endToEndId',endToEndId)
    log_api_input_param('terminalId',terminalId)
    log_api_input_param('branch',branch)
    log_api_input_param('Details',Details)

    paymentId=None    
    api_params = hb_get_parameters(api)
    
    #Amount = 0.01 #for test
    payment_request={'bankId':'','accountId':DBaccountId,'transaction':{'amount':Amount,'currency':Currency,'currencyRate':''}}

    #bobbi    
    fundsavail_Result=hb_payment_fundsavailability(access_token,subscriptionId,payment_request)
    if not fundsavail_Result.get('status') == 'success':
        errormsg = 'No funds available: '+fundsavail_Result.get('message')
        payment_result = api_standard_fail_reply(errormsg=errormsg, return_value=None, errors=fundsavail_Result.get('data',{}))
        return payment_result

    get_signature_result = hb_get_payment_jws_signature(access_token, subscriptionId, DBaccountId ,CRaccountId,Amount,Currency,Details,endToEndId,terminalId,branch,refNumber,CRaccountBankId,CraccountName,CraccountAddress)
    if not get_signature_result.get('status') == 'success':
        errormsg = 'get payment signature failed: '+get_signature_result.get('message')
        payment_result = api_standard_fail_reply(errormsg=errormsg, return_value=None, errors=get_signature_result.get('data',{}))
        return payment_result
    
    signature=get_signature_result.get('data')
    
    create_result=hb_payment_create(access_token, subscriptionId, signature)
    if not create_result.get('status') == 'success':
        errormsg = 'payment create failed: '+create_result.get('message')
        payment_result = api_standard_fail_reply(errormsg=errormsg, return_value=None, errors=create_result.get('data',{}))
        return payment_result

    paymentresult = create_result.get('data',{})
    log_api_result('paymentresult =', paymentresult)
    # {
    #     'authCodeNeeded': True,
    #     'payment': {
    #         'paymentId': 'string_1559630734280',
    #         'transactionTime': 'string',
    #         'status': {'code': 'PNDG', 'description':['Payment in pending status'], 'refNumber': 'string'},
    #         'debtor': {'bankId': '', 'accountId': '351012345671'},
    #         'creditor': {'bankId': '', 'accountId': '351012345673', 'name': 'metro', 'address': 'platy'},
    #         'transactionAmount': {'amount': 3.54, 'currency': 'EUR', 'currencyRate': ''},
    #         'charges': None,
    #         'totalCharges': 'string',
    #         'endToEndId': '283238',
    #         'paymentDetails': 'metro zzzz zzzz',
    #         'terminalId': 'ltf003',
    #         'branch': '8003',
    #         'RUB': None,
    #         'executionDate': '04/06/2019',
    #         'valueDate': '04/06/2019',
    #         'totalDebitAmount': None,
    #         'attachments': None}
    #     }
    paymAuthNeeded=paymentresult['authCodeNeeded']
    payment = paymentresult.get("payment")    
    paymentId = payment['paymentId']
    paymstatus = payment['status']
    paymentRefNum=paymstatus['refNumber']
    paymentStatusCode=paymstatus['code']
    paymentStatusDesc=paymstatus['description'][0]
    paymentCharges=payment['charges']
    paymentTotalChargesString=payment['totalCharges']
    paymenttotalDebitAmount=payment['totalDebitAmount']

    log_api_output_result('paymAuthNeeded =', paymAuthNeeded)
    log_api_output_result('paymentId =', paymentId)
    log_api_output_result('paymentRefNum =', paymentRefNum)
    log_api_output_result('paymentStatusCode =', paymentStatusCode)
    log_api_output_result('paymentStatusDesc =', paymentStatusDesc)
    log_api_output_result('paymentCharges =', paymentCharges)
    log_api_output_result('paymentTotalChargesString =', paymentTotalChargesString)
    log_api_output_result('paymenttotalDebitAmount =', paymenttotalDebitAmount)

    #print('\n','payment_result=', create_result,'\n')
    payment_result = api_standard_success_reply(msg='OK. payment created', return_value=paymentId, return_data=create_result.get('data',{}))
    log_api_finish()
    return payment_result
################################################################
################################################################
### create subscription apis                                 ###
################################################################
def hb_get_subscriptionId(access_token, allow_transactionHistory=True, allow_balance=True, allow_details=True, allow_checkFundsAvailability=True, payments_limit=0, payments_currency='EUR', payments_amount=0):
    global http_request

    api='get_subscriptionId'

    #start
    log_api_start(api)

    #input
    log_api_input_param('allow_transactionHistory',allow_transactionHistory)
    log_api_input_param('allow_balance',allow_balance)
    log_api_input_param('allow_details',allow_details)
    log_api_input_param('allow_checkFundsAvailability',allow_checkFundsAvailability)
    log_api_input_param('payments_limit',payments_limit)
    log_api_input_param('payments_currency',payments_currency)
    log_api_input_param('payments_amount',payments_amount)

    #transformations
    allow_transactionHistory_string = str(allow_transactionHistory).lower()
    allow_balance_string = str(allow_balance).lower()
    allow_details_string = str(allow_details).lower()
    allow_checkFundsAvailability_string = str(allow_checkFundsAvailability).lower()

    # setup subscription options
    accounts_options_string = f'"transactionHistory": {allow_transactionHistory_string}, "balance": {allow_balance_string}, "details": {allow_details_string}, "checkFundsAvailability": {allow_checkFundsAvailability_string}'
    payments_options_string = f'"limit": {payments_limit}, "currency": "{payments_currency}", "amount": {payments_amount}'
    log_api_interim_result('accounts_options_string',accounts_options_string)        
    log_api_interim_result('payments_options_string',payments_options_string)        

    subscription_options_string = '"accounts":{'+accounts_options_string+'},"payments":{'+payments_options_string+'}'
    log_api_interim_result('subscription_options_string',subscription_options_string)
    
    # print('')
    # SubscriptionRequestData_string="{\"accounts\":{\"transactionHistory\":true,\"balance\":true,\"details\":true,\"checkFundsAvailability\":false},\"payments\":{\"limit\":0.00,\"currency\":\"EUR\",\"amount\":0.00}}"
    # print('SubscriptionRequestData_string =',SubscriptionRequestData_string)        
    # SubscriptionRequestData= json.loads(SubscriptionRequestData_string)
    
    subscription_data_string = "{"+subscription_options_string+"}"
    log_api_interim_result('subscription_data_string',subscription_data_string)

    subscription_data= json.loads(subscription_data_string)
    log_api_interim_result('subscription_data',subscription_data)

    #setup httprequest
    api_params=hb_get_parameters(api)
    request_params=hb_prepare_request_standard(access_token,'',api_params)
    api_url=request_params['url']
    headers=request_params['headers']
    headers.update({'app_name': api_params['app_Name']})
    params=request_params['parameters']

    #init output
    subscriptionId = None

    #httprequest
    r = hb_standard_http_requestV2(api=api, function='post', url=api_url,headers=headers, params=params, data=subscription_data_string)
    if r.get('success'):
        subscriptionId = r.get('output',{}).get('data',{}).get('subscriptionId',None)
        create_result = api_standard_success_reply(msg='OK. subscription created', return_value=subscriptionId, return_data=r.get('data',{}))
    else:
        errormsg = 'subscription create failed: '+r.get('error_message')
        create_result = api_standard_fail_reply(errormsg=errormsg, return_value=None, errors=r.get('data',{}))

    #display result
    log_api_result(f'subscription create:', create_result)

    #display output
    log_api_output_result('subscriptionId',create_result.get('return_value'))

    #finish
    log_api_finish()
    
    return create_result
################################################################
def hb_xget_subscriptionId(access_token,SubscriptionRequest):   

    api='get_subscriptionId'

    #paola

    #start
    log_api_start(api)

    #input
    log_api_input_param('SubscriptionRequest',SubscriptionRequest)

    if isinstance(SubscriptionRequest, str):
        SubscriptionRequest = json.loads(SubscriptionRequest)

    selected_accounts=SubscriptionRequest.get('selectedAccounts')
    accounts_options=SubscriptionRequest.get('accounts')
    payments_options=SubscriptionRequest.get('payments')

    log_api_input_param('SubscriptionData',SubscriptionRequest)
    log_api_input_param('--selected_accounts',selected_accounts)
    log_api_input_param('--accounts_options',accounts_options)
    log_api_input_param('--payments_options',payments_options)



    #init output
    subscription_accounts={}
    outputStr = ''

    #setup httprequest
    api_params=hb_get_parameters(api)
    request_params=hb_prepare_request_standard(access_token,'',api_params)
    api_url=request_params['url']
    headers=request_params['headers']
    headers.update({'app_name': api_params['app_Name']})
    params=request_params['parameters']

    subscription_data_json = "{\"selectedAccounts\":" + json.dumps(selected_accounts) + ",\"accounts\":" + json.dumps(accounts_options) + ",\"payments\":" + json.dumps(payments_options) + "}"
    #subscription_data = f'"selectedAccounts": "{json.dumps(selected_accounts)}", "accounts": "{json.dumps(accounts_options)}", "payments": "{json.dumps(payments_options)}"'
    #print('subscription_data =', subscription_data)
    selected_accounts = [{"accountId":"351012345671"},{"accountId":"351012345671"}]


    SubscriptionRequest="{\"accounts\":{\"transactionHistory\":true,\"balance\":true,\"details\":true,\"checkFundsAvailability\":false},\"payments\":{\"limit\":0.00,\"currency\":\"EUR\",\"amount\":0.00}}"
    SubscriptionRequest="{\"accounts\":{\"transactionHistory\":false,\"balance\":true,\"details\":true,\"checkFundsAvailability\":true},\"payments\":{\"limit\":220.00,\"currency\":\"EUR\",\"amount\":110.00}}"

    SubscriptionRequest="{\"selectedAccounts\":[{\"accountId\":\"351012345671\"},{\"accountId\":\"351012345671\"}], \"accounts\":{\"transactionHistory\":false,\"balance\":true,\"details\":true,\"checkFundsAvailability\":true},\"payments\":{\"limit\":220.00,\"currency\":\"EUR\",\"amount\":110.00}}"
    log_api_interim_result('subscription_request =', SubscriptionRequest)

    #httprequest
    r = hb_standard_http_request(api=api, function='post', url=api_url,headers=headers, params=params, data=SubscriptionRequest)

    #setup output
    # reply_code=r.status_code
    subscriptionId = None
    response = r.json()    
    if not ((r.status_code == master_http_ok_code) or (r.status_code == 201)):
        create_result = api_standard_fail_reply(errormsg='subscription create failed', return_value=None, errors=active_api_reply_json, api=None)
    else:
        subscriptionId = response['subscriptionId']
        create_result = api_standard_success_reply(msg='OK. subscription created', return_value=subscriptionId, return_data=active_api_reply_json, api=None)

    #display result
    log_api_result(f'subscription create:', create_result, api=api)

    log_api_output('subscriptionId',subscriptionId)

    #finish
    # log_api_finish()
    # return create_result

    #finsih
    log_api_finish()
    return subscriptionId
################################################################
def hb_get_customer_authorization(access_token, subscriptionId):
    global master_configuration
    secs_to_wait =  master_configuration.get('secs_to_wait_for_authorization',120)
    
    #start
    api='get_customer_authorization'
    
    
    log_api_start(api)

    log_api_input_param('subscriptionId',subscriptionId)
    log_api_input_param('secs_to_wait_for_authorization',secs_to_wait)

    bankID = master_configuration.get('bankID')
    http_result_file = master_configuration.get('http_result_file','code.txt')
    http_result_folder = master_configuration.get('http_result_folder','')
    log_api_input_param('bankID',bankID)
    log_api_input_param('http_result_file',http_result_file)
    log_api_input_param('http_result_folder',http_result_folder)

    #init output
    authorization_code = None

    # #prepare for http wait code
    # codefile = r'''c:\users\user\documents\code.txt'''
    # try:
    #     os.remove(codefile)
    # except:
    #     dummy = 1
    # #3BOBBI-DEGRAY

    #start_http_server()
    #res = _httpServices.start_httpserver(bankID=bankID,subscriptionID=subscriptionId,result_file=http_result_file,result_folder=http_result_folder)
    #res = start_a_simple_webserver()
    # if not res:
    #     error_text='httpserver not started. retry'
    #     log_api_result(error_text)
    #     return None


    #invoke the banks login page
    clear_authorization_result_file()
    hb_get_customer_Consent(subscriptionId)

    #wait for authorization code thru http
    #authorization_code = _httpServices.wait_for_authorization(bankID=bankID,subscriptionID=subscriptionId,result_file=http_result_file,result_folder=http_result_folder)
    authorization_code = wait_for_authorization(secs_to_wait=secs_to_wait)
    if not authorization_code:
        error_text='authorization NOT received after {secs_to_wait} secs'
        log_api_result(error_text)
        return None

    log_api_output_result('authorization_code',authorization_code)

    #finish
    log_api_finish()
    return authorization_code
################################################################
def hb_get_customer_Consent(subscriptionId):
    api='get_customerConsent'

    log_api_start(api)

    api_params=hb_get_parameters(api)

    url=api_params['endpoint']+"?"
    url=url+"response_type=code"
    url=url+"&redirect_uri="+api_params['redirect_uri']
    url=url+"&scope=UserOAuth2Security"
    url=url+"&client_id="+api_params['client_id']
    url=url+"&subscriptionid="+subscriptionId
    #url=url+"&state="+'tis paolas tavizia'

    webbrowser.open(url, new=0)
    log_api_finish()
    return 1
################################################################
################################################################
def hb_commit_subscription(subscriptionId,authorization_token,subscription_data):   
    global htttp_request
    global active_api_errorText
    global active_api_standard_result_output
    global active_api_standard_reply

    api='commit_subscription'

    #start
    log_api_start(api)

    #input params
    log_api_input_param('subscriptionId',subscriptionId)
    log_api_input_param('authorization_token',authorization_token)
    log_api_input_param('subscription_data',subscription_data)

    #init output

    #setup httprequest
    api_params=hb_get_parameters(api)
    request_params=hb_prepare_request_standard(authorization_token,'',api_params,subscriptionId)
    api_url=request_params['url']
    params=request_params['parameters']
    params.update({'subscriptionId': subscriptionId})    
    headers=request_params['headers']
    data=subscription_data

    #httprequest
    r = hb_standard_http_requestV2(api=api, function='patch', url=api_url,headers=headers,params=params,data=subscription_data)
    # log_api_result('update message', r.get('message'))
    # log_api_result('update output', r.get('output_string'))
    if r.get('success'):
        subscriptionId = r.get('data',{}).get('subscriptionId',None)
        commit_result = api_standard_success_reply(msg='OK. subscription created', return_value=subscriptionId, return_data=r.get('data',{}))
        log_api_result('update data', r.get('data'))
    else:
        errormsg = 'subscription update failed: '+r.get('error_message')
        log_api_result('update data', r.get('data'))
        commit_result = api_standard_fail_reply(errormsg=errormsg, return_value=None, errors=r.get('data', {}))

    #display result
    # log_api_result('update result', r.message)

    #display output
    #log_api_output(f'subscription {subscriptionId} update result', active_api_standard_result_output, api=api)
    log_api_output_result('', r.get('output_string'))

    #finish
    log_api_finish()
    return commit_result
################################################################
### _utilities                                                ###
################################################################
def hb_clear_pending_subscriptions(accounts):
    api='clear_pending_subscriptions'
    log_api_start(api)

    api_params=hb_get_parameters(api)
    customer_subscriptions=[]
    customer_accounts=set([])
    access_token=hb_get_access_token()
    a=0
    deleted=0
    failed=0
    for accountId in accounts:
        a=a+1
        #print('@@@customer account@@@',a,'accountId=',accountId,'-----')
        subscriptions=hb_get_account_subscriptions(access_token,accountId)
        if subscriptions:
            n=0
            for subscription in subscriptions:
                n=n+1
                subscription_id=subscription['subscriptionId']
                subscription_status=subscription['status']
                if subscription_status=='pending':
                    res = hb_delete_subscription(access_token, subscription_id)
                    if res.get('status') == 'success':                
                        deleted = deleted + 1
                    else:
                        failed = failed + 1                        
    msg=f'{deleted} pending subscriptions deleted, {failed} failed'
    log_api_finish()
    return msg
################################################################
def hb_clear_all_subscriptions(accounts):
    api='clear_active_subscriptions'
    log_api_start(api)

    api_params=hb_get_parameters(api)
    customer_subscriptions=[]
    customer_accounts=set([])
    access_token=hb_get_access_token()
    a=0
    deleted=0
    failed=0
    for accountId in accounts:
        a=a+1
        #print('@@@customer account@@@',a,'accountId=',accountId,'-----')
        subscriptions=hb_get_account_subscriptions(access_token,accountId)
        if subscriptions:
            n=0
            for subscription in subscriptions:
                n=n+1
                subscription_id=subscription['subscriptionId']
                subscription_status=subscription['status']
                #if subscription_status=='pending':
                res = hb_delete_subscription(access_token, subscription_id)
                if res.get('status') == 'success':
                    deleted=deleted+1
                else:
                    failed = failed + 1                        
    msg=f'{deleted} subscriptions deleted, {failed} failed'
    log_api_finish()
    return msg
################################################################
def hb_get_customer_subscriptions(accounts,resultoption=''):
    api='get_customer_subscriptions'
    log_api_start(api)

    api_params=hb_get_parameters(api)
    customer_subscriptions=set([])
    customer_accounts=set([])
    customer_subscriptionsaccountsxref=set([])
    access_token=hb_get_access_token()
    a=0
    for accountId in accounts:
        a=a+1
        #print('@@@customer account@@@',a,'accountId=',accountId,'-----')
        subscriptions=hb_get_account_subscriptions(access_token,accountId)
        if subscriptions:
            #n=0
            #for subscription in subscriptions:
            #    n=n+1
            #    subscription_id=subscription['subscriptionId']
            #    subscription_status=subscription['status']
            #    subscription_accounts=hb_get_subscription_selectedAccounts(access_token,subscription_id)
            #    #print('   ',a,accountId,n,subscription_id,subscription_status,len(subscription_accounts))
            n=0
            for subscription in subscriptions:
                n=n+1
                subscription_id=subscription['subscriptionId']
                subscription_status=subscription['status']
                customer_subscriptions.add(subscription_id)
                subscription_accounts=hb_get_subscription_selectedAccounts(access_token,subscription_id)
                #print('      ',a,accountId,n,subscription_id,subscription_status,len(subscription_accounts))
                an=0
                for account in subscription_accounts:
                    an=an+1
                    #print('         ',a,n,an,'acct=',account['accountId'])
                    customer_accounts.add(account['accountId'])
                    xref=account['accountId']+'-->'+subscription_id+'-->'+subscription_status
                    customer_subscriptionsaccountsxref.add(xref)
                    
    if api_params.get('debuglevel_three',1)>0:
        print('#1#customer_accounts:')
        #print('#1#customer_accounts=',customer_accounts)
        n=0
        for account in sorted(customer_accounts):
            n=n+1
            print('   ',n,account)

        #print('#2#customer_subscriptions=',customer_subscriptions)
        print('#2#customer_subscriptions:')
        n=0
        for subscriptionid in sorted(customer_subscriptions):
            n=n+1
            #print('   ',n,subscriptionid)

        #print('#3#customer_subscriptionsaccountsxref=',customer_subscriptionsaccountsxref)
        print('#3#customer_subscriptionsaccountsxref:')
        n=0
        for xref in sorted(customer_subscriptionsaccountsxref):
            n=n+1
            #print('   ',n,xref)

    log_api_finish()
	
    if resultoption=='subscriptions':    
        return customer_subscriptions
    if resultoption=='accounts':    
        return customer_accounts
    if resultoption=='xref':    
        return customer_subscriptionsaccountsxref

    return customer_subscriptions
################################################################
def hb_check_subscription(subscriptionId):
    process='check_subscription'
    log_api_start(process)
    log_api_input_param('subscriptionId',subscriptionId)
    access_token=hb_get_access_token()
    if not access_token:
        error_text='access token not obtained'
        raise Exception(error_text)
    subscription = hb_get_subscription_details(access_token, subscriptionId)
    log_api_finish(process)
    return subscription
#::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
#::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
#::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
# httpservices utilities
#::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
#::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
#::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
#################################################################################################
def clear_authorization_result_file():
    global master_configuration
    global module_id
    result_file_name =  master_configuration.get('authorization_code_result_file','code.txt')

    process='clear_authorization_result_file'
    
    log_message_subprocess_running('authorization_code_result_file =',result_file_name,caller_module=module_id,caller_function=process)

    ix = 0
    while True:
        ix = ix + 1
        if ix > 100:
            break
        codeFile = find_file(result_file_name, thisDir='', search_Downwards=1, search_Upwards=2, search_SubFolders=False)
        if not codeFile:
            break
        else:
            try:
                os.remove(codeFile)
                log_message_subprocess_running(f'result_file removed:{codeFile}',caller_module=module_id,caller_function=process)
            except:
                log_message_special_error(f'failed to remove result_file:{codeFile}',caller_module=module_id,caller_function=process)
                pass
################################################################
def wait_for_authorization(secs_to_wait=120):
    global master_configuration
    global module_id
    process='wait_for_client_authorization'
    
    result_file_name =  master_configuration.get('authorization_code_result_file','code.txt')

    log_message_subprocess_running('authorization_code_result_file =',result_file_name,caller_module=module_id,caller_function=process)
    log_message_subprocess_running('secs_to_wait =',secs_to_wait,caller_module=module_id,caller_function=process)

    authorization_code=None
    n=0
    while n<secs_to_wait:
        if ((n % 10) == 0):
            log_message_wait(f'waiting for {result_file_name}...{secs_to_wait-n}',caller_module=module_id,caller_function=process)
        time.sleep(1) # Delay for 1 sec
        n=n+1
        ok=0
        codeFile = find_file(result_file_name, thisDir='', search_Downwards=1, search_Upwards=1, search_SubFolders=False)
        if codeFile:
            try:
                thefile = open(codeFile, 'r')
                ok=1
            except:
                ok=0
            if ok==1:
                authorization_code=thefile.read()
                thefile.close
                log_message_special_success('code_received---|',authorization_code+'|',caller_module=module_id,caller_function=process)
                break
    return authorization_code
#::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
#::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
#::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
# module initialization
#::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
#::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
#::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
master_configuration = retrieve_module_configuration(module_identityDictionary, master_configuration, print_enabled=None, filelog_enabled=None, handle_as_init=False)
msg = f'openBanking module [{module_id}] [[version {module_version}]] loaded.'
log_message(msg)
#::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
#::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
#::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
# main (for test)
#::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
#::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
#::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
if __name__ == '__main__':
    print(__file__)
    log_message_subprocess_running(msg1='xxxxxxxxxx', msg2='zzzzzzzzzzzzzzzz', msg3='aaaaaaaaaaaaaaaa',caller_module=module_id,caller_function='subprocess_run')
    log_message_subprocess_running(msg1='xxxxxxxxxx', msg2='zzzzzzzzzzzzzzzz', msg3='aaaaaaaaaaaaaaaa',caller_module=module_id,caller_function='subprocess_run')
    log_message_subprocess_running(msg1='xxxxxxxxxx', msg2='zzzzzzzzzzzzzzzz', msg3='aaaaaaaaaaaaaaaa',caller_module=module_id,caller_function='subprocess_run')
    log_message_wait(msg1='xxxxxxxxxx', msg2='zzzzzzzzzzzzzzzz', msg3='aaaaaaaaaaaaaaaa',caller_module=module_id,caller_function='wait')
    log_message_wait(msg1='xxxxxxxxxx', msg2='zzzzzzzzzzzzzzzz', msg3='aaaaaaaaaaaaaaaa',caller_module=module_id,caller_function='wait')
    log_message_wait(msg1='xxxxxxxxxx', msg2='zzzzzzzzzzzzzzzz', msg3='aaaaaaaaaaaaaaaa',caller_module=module_id,caller_function='wait')
    log_message_special_error(msg1='xxxxxxxxxx', msg2='zzzzzzzzzzzzzzzz', msg3='aaaaaaaaaaaaaaaa',caller_module=module_id,caller_function='special_error')
    log_message_special_success(msg1='xxxxxxxxxx', msg2='zzzzzzzzzzzzzzzz', msg3='aaaaaaaaaaaaaaaa',caller_module=module_id,caller_function='special_success')
    log_message_wait_success(msg1='xxxxxxxxxx', msg2='zzzzzzzzzzzzzzzz', msg3='aaaaaaaaaaaaaaaa',caller_module=module_id,caller_function='wait_success')
    log_message_wait_success(msg1='xxxxxxxxxx', msg2='zzzzzzzzzzzzzzzz', msg3='aaaaaaaaaaaaaaaa',caller_module=module_id,caller_function='wait_success')
    log_message_wait_success(msg1='xxxxxxxxxx', msg2='zzzzzzzzzzzzzzzz', msg3='aaaaaaaaaaaaaaaa',caller_module=module_id,caller_function='wait_success')
