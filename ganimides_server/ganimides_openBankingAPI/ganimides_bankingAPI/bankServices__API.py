import os
import sys
import requests
import json
import time
import datetime
from datetime import timedelta
import webbrowser
from http.server import BaseHTTPRequestHandler, HTTPServer
import urllib
from urllib.parse import urlparse
import configparser

if not (os.path.dirname(os.path.dirname(__file__)) in sys.path): sys.path.append(os.path.dirname(os.path.dirname(__file__)))
if not (os.path.dirname(__file__) in sys.path): sys.path.append(os.path.dirname(__file__))

from _onlineApp import thisApp
from _onlineApp import get_debug_option_as_level, log_message, retrieve_module_configuration, get_globals_from_configuration, save_module_configuration
from _onlineApp import log_process_start, log_process_finish, log_process_message, log_process_result, log_process_data, log_process_input, log_process_output
from _onlineApp import set_process_identity_dict, set_process_caller_area,add_apis_to_configuration,get_module_debug_level
from _onlineApp import build_process_signature, build_process_call_area, get_debug_level, get_debug_files

from bankServices_BOC_api import boc_get_access_tokenV2
from bankServices_BOC_api import boc_get_authorization_token
from bankServices_BOC_api import boc_get_subscription_details
from bankServices_BOC_api import boc_get_subscription_customers
from bankServices_BOC_api import boc_get_account_details
from bankServices_BOC_api import boc_get_account_balances
from bankServices_BOC_api import boc_get_account_transactions
from bankServices_BOC_api import boc_get_account_subscriptions
from bankServices_BOC_api import boc_get_payments
from bankServices_BOC_api import boc_get_payment_status
from bankServices_BOC_api import boc_get_payment_details

from bankServices_BOC_api import boc_create_subscription
from bankServices_BOC_api import boc_commit_subscription
from bankServices_BOC_api import boc_get_customer_authorization
from bankServices_BOC_api import boc_create_authorize_and_commit_subscription
from bankServices_BOC_api import boc_authorize_and_commit_subscription
from bankServices_BOC_api import boc_change_subscription
from bankServices_BOC_api import boc_delete_subscription
from bankServices_BOC_api import boc_get_subscription_accounts
from bankServices_BOC_api import boc_make_payment
from bankServices_BOC_api import boc_delete_payment
from bankServices_BOC_api import boc_authorize_payment

from bankServices_HB_api import hb_get_access_tokenV2
from bankServices_HB_api import hb_get_authorization_token
from bankServices_HB_api import hb_get_subscription_details
from bankServices_HB_api import hb_get_subscription_customers
from bankServices_HB_api import hb_get_account_details
from bankServices_HB_api import hb_get_account_balances
from bankServices_HB_api import hb_get_account_transactions
from bankServices_HB_api import hb_get_account_subscriptions
from bankServices_HB_api import hb_get_payments
from bankServices_HB_api import hb_get_payment_status
from bankServices_HB_api import hb_get_payment_details
from bankServices_HB_api import hb_create_subscription
from bankServices_HB_api import hb_commit_subscription
from bankServices_HB_api import hb_get_customer_authorization
from bankServices_HB_api import hb_create_authorize_and_commit_subscription
from bankServices_HB_api import hb_authorize_and_commit_subscription
from bankServices_HB_api import hb_change_subscription
from bankServices_HB_api import hb_delete_subscription
from bankServices_HB_api import hb_get_subscription_accounts
from bankServices_HB_api import hb_make_payment
from bankServices_HB_api import hb_delete_payment
from bankServices_HB_api import hb_authorize_payment
#::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
#::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
#::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
#module
#::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
#::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
#::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
module_Function = 'openbanking api driver'
module_ProgramName = 'apiDriver'
module_BaseTimeStamp = datetime.datetime.now()
module_folder = os.getcwd()
module_color = thisApp.Fore.LIGHTMAGENTA_EX
module_folder = os.path.dirname(__file__)
module_ProgramName = os.path.splitext(os.path.basename(__file__))[0]
module_id = f'{module_ProgramName}'
module_eyecatch = module_ProgramName
module_version = 0.1
module_log_file_name = module_ProgramName+'.log'
module_errors_file_name = os.path.splitext(os.path.basename(module_log_file_name))[0]+'_errors.log'
module_versionString = f'{module_id} version {module_version}'
module_file = __file__

log_file=thisApp.log_file_name
print_enabled = thisApp.CONSOLE_ON
consolelog_enabled = thisApp.CONSOLE_ON
filelog_enabled = thisApp.FILELOG_ON

module_is_externally_configurable = True
module_identityDictionary = {
    'module_file':__file__,
    'module_Function':module_Function,
    'module_ProgramName':module_ProgramName,
    'module_BaseTimeStamp':module_BaseTimeStamp,
    'module_folder':module_folder,
    'module_color':module_color,
    'module_id':module_id,
    'module_eyecatch':module_eyecatch,
    'module_version':module_version,
    'module_versionString':module_versionString,
    'module_log_file_name':module_log_file_name,
    'module_errors_file_name': module_errors_file_name,
    'consolelog_enabled': consolelog_enabled,
    'filelog_enabled': filelog_enabled,
    'module_is_externally_configurable':module_is_externally_configurable,
    }
#::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
#::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
#::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
# configuration
#::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
#::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
#::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
master_configuration = {
    'banks':{
        'bankofcyprus':{'status':'active'},
        'hellenicbank':{'status':'Inactive'},
        'TSB':{'status':'Inactive'},
    },
}
#::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
#::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
#::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
#globals
#::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
#::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
#::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
access_tokens={}
#::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
#::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
#::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
#api services
#::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
#::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
#::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
###############################################################################################################
def bank_is_supported(bankID):
    banks = master_configuration.get('banks', {})
    bank = banks.get(bankID, {})
    if bank.get('status', '') == 'active':
        return True
    else:
        return False
###############################################################################################################
def get_access_token(bankID):
    global access_tokens
    access_token = None
    valid = False
    atk=access_tokens.get(bankID,{})
    access_token1 = atk.get('access_token',None)
    if access_token1:
        expires = atk.get('expires',None)
        if expires:
            dt = datetime.datetime.now()
            #print(dt,expires)
            if dt < expires: 
                valid = True
    if valid:
        access_token = access_token1
        #print('xxxxxxxxxx','access token','REUTILIZED')
    else:
        #print('','access token','NEW')
        if bankID=='bankofcyprus':
            access_token_result = boc_get_access_tokenV2()
            if access_token_result.get('status') == 'success':
                access_token_data = access_token_result.get('data')
                dts = datetime.datetime.now()
                expires_in_secs = access_token_data.get('expires_in', 0)
                expires_in_secs = expires_in_secs - 60
                dte = dts + datetime.timedelta(seconds=expires_in_secs)
                access_token_data.update({'obtained':dts})
                access_token_data.update({'expires':dte})
                access_tokens.update({bankID: access_token_data})
                access_token = access_token_data.get('access_token')
        # {
        #     'token_type': 'bearer',
        #     'access_token': 'AAIkNTJlZTgyOGUtYTE4ZS00NTYwLWJmZWQtMmQ1MTU4ZTlhNTA32kgqazwtewn_Vnc0KQd56kiPDFUnv9GyvFcWhyXPmH7Hzn1xWb0GxPMMQ79f9TjnAY89O9nexH3owNNKee6JoBpPfAGpvDwLiRYKxf89pTZPNBCbEpbNiogIAUX8edqXnUMer3fsbpBjPUtOvIosDg',
        #     'expires_in': 3600,
        #     'consented_on': 1559644505,
        #     'scope': 'TPPOAuth2Security'
        # }

        elif bankID=='hellenicbank':
            access_token_result = hb_get_access_tokenV2()
            if access_token_result.get('status') == 'success':
                access_token_data = access_token_result.get('data')
                dts = datetime.datetime.now()
                dte = dts + datetime.timedelta(seconds=3600)
                access_token_data.update({'obtained':dts})
                access_token_data.update({'expires':dte})
                access_tokens.update({bankID: access_token_data})
                access_token = access_token_data.get('access_token')
        else:
            access_token = None
    if not access_token:
        msg = f'get access token from bank {bankID} FAILED. Retry'
        #raise Exception(errorMsg)
        #log_message(msg, msgType='Error')
        print(msg)
    return access_token
#::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::

#::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
#::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
#api services: subscriptions
#::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
#::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
#::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
def get_authorization_token(bankID, authorization_code):
    if not bank_is_supported(bankID):
        return None
    access_token=get_access_token(bankID)
    if not access_token:
        return None

    if bankID=='bankofcyprus':
        return boc_get_authorization_token(access_token, authorization_code)
    elif bankID=='hellenicbank':
        return hb_get_authorization_token(access_token, authorization_code)
    else:
        return None
###############################################################################################################
def get_subscription_details(bankID, accounts_subscriptionID):
    if not bank_is_supported(bankID):
        return None
    access_token=get_access_token(bankID)
    if not access_token:
        return None

    if bankID=='bankofcyprus':
        return boc_get_subscription_details(access_token, accounts_subscriptionID)
    elif bankID=='hellenicbank':
        return hb_get_subscription_details(access_token, accounts_subscriptionID)
    else:
        return None
###############################################################################################################
def get_subscription_customers(bankID,subscriptionID):
    if not bank_is_supported(bankID):
        return None
    access_token=get_access_token(bankID)
    if not access_token:
        return None

    if bankID=='bankofcyprus':
        return boc_get_subscription_customers(access_token, subscriptionID)
    elif bankID=='hellenicbank':
        return hb_get_subscription_customers(access_token, subscriptionID)
    else:
        return None
###############################################################################################################
def get_subscription_accounts(bankID,subscriptionID):
    if not bank_is_supported(bankID):
        return None
    access_token=get_access_token(bankID)
    if not access_token:
        return None

    if bankID=='bankofcyprus':
        return boc_get_subscription_accounts(access_token, subscriptionID)
    elif bankID=='hellenicbank':
        return hb_get_subscription_accounts(access_token, subscriptionID)
    else:
        return None
###############################################################################################################
def create_authorize_and_commit_subscription(bankID, allow_transactionHistory=True, allow_balance=True, allow_details=True, allow_checkFundsAvailability=True, payments_limit=0, payments_currency='EUR', payments_amount=0):
    if not bank_is_supported(bankID):
        return None
    access_token=get_access_token(bankID)
    if not access_token:
        return None

    if bankID=='bankofcyprus':
        return boc_create_authorize_and_commit_subscription(access_token, allow_transactionHistory, allow_balance, allow_details, allow_checkFundsAvailability, payments_limit, payments_currency, payments_amount)
    elif bankID=='hellenicbank':
        return hb_create_authorize_and_commit_subscription(access_token, allow_transactionHistory, allow_balance, allow_details, allow_checkFundsAvailability, payments_limit, payments_currency, payments_amount)
    else:
        return None
###############################################################################################################
def create_subscription(bankID, allow_transactionHistory=True, allow_balance=True, allow_details=True, allow_checkFundsAvailability=True, payments_limit=0, payments_currency='EUR', payments_amount=0):
    if not bank_is_supported(bankID):
        return None
    access_token=get_access_token(bankID)
    if not access_token:
        return None

    if bankID=='bankofcyprus':
        return boc_create_subscription(access_token, allow_transactionHistory, allow_balance, allow_details, allow_checkFundsAvailability, payments_limit, payments_currency, payments_amount)
    elif bankID=='hellenicbank':
        return hb_create_subscription(access_token, allow_transactionHistory, allow_balance, allow_details, allow_checkFundsAvailability, payments_limit, payments_currency, payments_amount)
    else:
        return None
###############################################################################################################
def authorize_subscription(bankID, subscriptionID):
    if not bank_is_supported(bankID):
        return None
    access_token=get_access_token(bankID)
    if not access_token:
        return None

    if bankID=='bankofcyprus':
        return boc_get_customer_authorization(access_token, subscriptionID)
    elif bankID=='hellenicbank':
        return hb_get_customer_authorization(access_token, subscriptionID)
    else:
        return None
###############################################################################################################
def commit_subscription(bankID,authorization_token,subscriptionID):
    if not bank_is_supported(bankID):
        return None
    # authorization_token=get_authorization_token(bankID,authorization_code)
    if not authorization_token:
        return None
    access_token=get_access_token(bankID)
    if not access_token:
        return None
    subscription_data={}    
    if bankID=='bankofcyprus':
        return boc_commit_subscription(subscriptionID,authorization_token,access_token,subscription_data)
    elif bankID=='hellenicbank':
        return hb_commit_subscription(subscriptionID,authorization_token,access_token,subscription_data)
    else:
        return None
###############################################################################################################
def authorize_and_commit_subscription(bankID, subscriptionID):
    if not bank_is_supported(bankID):
        return None
    access_token=get_access_token(bankID)
    if not access_token:
        return None

    if bankID=='bankofcyprus':
        return boc_authorize_and_commit_subscription(access_token, subscriptionID)
    elif bankID=='hellenicbank':
        return hb_authorize_and_commit_subscription(access_token, subscriptionID)
    else:
        return None
###############################################################################################################
def change_subscription(bankID, subscriptionID, allow_transactionHistory=True, allow_balance=True, allow_details=True, allow_checkFundsAvailability=True, payments_limit=0, payments_currency='EUR', payments_amount=0):
    if not bank_is_supported(bankID):
        return None
    access_token=get_access_token(bankID)
    if not access_token:
        return None

    if bankID=='bankofcyprus':
        return boc_change_subscription(access_token, subscriptionID, allow_transactionHistory, allow_balance, allow_details, allow_checkFundsAvailability, payments_limit, payments_currency, payments_amount)
    elif bankID=='hellenicbank':
        return hb_change_subscription(access_token, subscriptionID, allow_transactionHistory, allow_balance, allow_details, allow_checkFundsAvailability, payments_limit, payments_currency, payments_amount)
    else:
        return None
###############################################################################################################
def delete_subscription(bankID,subscriptionID):   
    if not bank_is_supported(bankID):
        return None
    access_token=get_access_token(bankID)
    if not access_token:
        return None

    if bankID=='bankofcyprus':
        return boc_delete_subscription(access_token, subscriptionID)
    elif bankID=='hellenicbank':
        return hb_delete_subscription(access_token, subscriptionID)
    else:
        return None
#::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
#::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
#::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
#api services: accounts
#::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
#::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
#::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
def get_account_details(bankID,subscriptionID,accountID):
    if not bank_is_supported(bankID):
        return None
    access_token=get_access_token(bankID)
    if not access_token:
        return None

    if bankID=='bankofcyprus':
        return boc_get_account_details(access_token, subscriptionID,accountID)
    elif bankID=='hellenicbank':
        return hb_get_account_details(access_token, subscriptionID,accountID)
    else:
        return None
###############################################################################################################
def get_account_balances(bankID,subscriptionID,accountID):
    if not bank_is_supported(bankID):
        return None
    access_token=get_access_token(bankID)
    if not access_token:
        return None

    if bankID=='bankofcyprus':
        return boc_get_account_balances(access_token, subscriptionID,accountID)
    elif bankID=='hellenicbank':
        return hb_get_account_balances(access_token, subscriptionID,accountID)
    else:
        return None
###############################################################################################################
def get_account_payments(bankID,subscriptionID,accountID):
    if not bank_is_supported(bankID):
        return None
    access_token=get_access_token(bankID)
    if not access_token:
        return None

    if bankID=='bankofcyprus':
        return boc_get_payments(access_token, subscriptionID,accountID)
    elif bankID=='hellenicbank':
        return hb_get_payments(access_token, subscriptionID,accountID)
    else:
        return None
###############################################################################################################
def get_account_transactions(bankID, subscriptionId, accountId,sdate='',edate='',ntrans=9999):
    if not bank_is_supported(bankID):
        return None
    access_token=get_access_token(bankID)
    if not access_token:
        return None

    if bankID=='bankofcyprus':
        return boc_get_account_transactions(access_token, subscriptionId, accountId,sdate=sdate,edate=edate,ntrans=ntrans)
    elif bankID=='hellenicbank':
        return hb_get_account_transactions(access_token, subscriptionId, accountId,sdate=sdate,edate=edate,ntrans=ntrans)
    else:
        return None
###############################################################################################################
def get_account_subscriptions(bankID,accountID):
    if not bank_is_supported(bankID):
        return None
    access_token=get_access_token(bankID)
    if not access_token:
        return None

    if bankID=='bankofcyprus':
        return boc_get_account_subscriptions(access_token,accountID)
    elif bankID=='hellenicbank':
        return hb_get_account_subscriptions(access_token,accountID)
    else:
        return None
#::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
#::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
#::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
#api services: payments
#::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
#::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
#::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
def get_payment_status(bankID,subscriptionID,paymentID):
    if not bank_is_supported(bankID):
        return None
    access_token=get_access_token(bankID)
    if not access_token:
        return None

    if bankID=='bankofcyprus':
        return boc_get_payment_status(access_token, subscriptionID, paymentID)
    elif bankID=='hellenicbank':
        return hb_get_payment_status(access_token, subscriptionID, paymentID)
    else:
        return None
###############################################################################################################
def get_payment_details(bankID,subscriptionID,paymentID):
    if not bank_is_supported(bankID):
        return None
    access_token=get_access_token(bankID)
    if not access_token:
        return None

    if bankID=='bankofcyprus':
        return boc_get_payment_details(access_token, subscriptionID,paymentID)
    elif bankID=='hellenicbank':
        return hb_get_payment_details(access_token, subscriptionID,paymentID)
    else:
        return None
###############################################################################################################
def post_payment(bankID,subscriptionID, DBaccountId, CRaccountId, Amount, Currency, Details, endToEndId, terminalId, branch, refNumber, CRaccountBankId,CraccountName,CraccountAddress):
    if not bank_is_supported(bankID):
        return None
    access_token=get_access_token(bankID)
    if not access_token:
        return None

    if bankID=='bankofcyprus':
        return boc_make_payment(access_token, subscriptionID, DBaccountId, CRaccountId, Amount, Currency, Details, endToEndId, terminalId, branch, refNumber, CRaccountBankId, CraccountName, CraccountAddress)
    elif bankID=='hellenicbank':
        return hb_make_payment(access_token,subscriptionID, DBaccountId, CRaccountId, Amount, Currency, Details, endToEndId, terminalId, branch, refNumber, CRaccountBankId,CraccountName,CraccountAddress)
    else:
        return None
###############################################################################################################
def delete_payment(bankID,subscriptionID,paymentID):
    if not bank_is_supported(bankID):
        return None
    access_token=get_access_token(bankID)
    if not access_token:
        return None

    if bankID=='bankofcyprus':
        return boc_delete_payment(access_token, subscriptionID, paymentID)
    elif bankID=='hellenicbank':
        return hb_delete_payment(access_token, subscriptionID, paymentID)
    else:
        return None
###############################################################################################################
def authorize_payment(bankID,subscriptionID,paymentID,authorization_code):
    if not bank_is_supported(bankID):
        return None
    access_token=get_access_token(bankID)
    if not access_token:
        return None

    if bankID=='bankofcyprus':
        return boc_authorize_payment(access_token, subscriptionID, paymentID,authorization_code)
    elif bankID=='hellenicbank':
        return hb_authorize_payment(access_token, subscriptionID, paymentID,authorization_code)
    else:
        return None
#::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
#::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
#::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
#::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
#::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
#::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
#::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
#::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
#::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
#::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
#::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
#::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
#::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
#::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
#::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
#::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
def set_msgID(api_name,api_action,api_entity):
    msgid=f"#C0#api #C9#{api_name}#C0# [{api_entity}]#C0# action [[{api_action.upper()}]]#C0#"
    return msgid
#::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
#::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
#::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
#::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
# module initialization
#::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
#::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
#::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
master_configuration = retrieve_module_configuration(module_identityDictionary, master_configuration, print_enabled=consolelog_enabled, filelog_enabled=filelog_enabled, handle_as_init=False)
#::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
(print_enabled, filelog_enabled, log_file, errors_file,consolelog_enabled)=get_globals_from_configuration(master_configuration)
#::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
functions_ids=['ALL']
exclude_functions_ids = ['set_msgID']
thisModuleObj = sys.modules[__name__]
master_configuration = add_apis_to_configuration('banks_apis', master_configuration, thisModuleObj, functions_ids, exclude_functions_ids)
save_module_configuration(module_identityDictionary, master_configuration, print_enabled=consolelog_enabled, filelog_enabled=filelog_enabled)
thisApp.pair_module_configuration('banks_apis',master_configuration)
#::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
if get_module_debug_level(module_id) > 0:
    apis = thisApp.application_configuration.get('banks_apis', {})
    for api_name in apis.keys():
        api_entry = apis.get(api_name)
        msg=f'module [[{module_id}]] bank api [{api_name} [[[{api_entry}]]]'
        log_message(msg)
#::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
#::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
msg = f'openBanking module [{module_id}] [[version {module_version}]] loaded.'
log_message(msg)
#::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
#::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
#::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
# main
#::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
#::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
#::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
if __name__ == '__main__':
    #tests/research
    print(__file__)
#::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
#::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
#::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::