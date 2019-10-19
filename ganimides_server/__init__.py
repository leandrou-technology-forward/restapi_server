import os
import sys
if not (os.path.dirname(os.path.dirname(__file__)) in sys.path): sys.path.append(os.path.dirname(os.path.dirname(__file__)))
if not (os.path.dirname(__file__) in sys.path): sys.path.append(os.path.dirname(__file__))
import datetime

from _onlineApp import thisApp
from _onlineApp import log_message
from _onlineApp import retrieve_module_configuration

import ganimides_database as db
import ganimides_openBankingAPI as openBankingAPI
import _ganimides_emails_api as emailsAPI

# #models
# from ganimides_database import TEST
# from ganimides_database import API
# from ganimides_database import APPLICATION_API
# from ganimides_database import APPLICATION
# from ganimides_database import TOKEN
# from ganimides_database import DEVICE
# from ganimides_database import DEVICE_USAGE
# from ganimides_database import Users
# from ganimides_database import CLIENT
# from ganimides_database import CLIENT_DEVICE
# from ganimides_database import MERCHANT
# from ganimides_database import POINT_OF_SALE
# from ganimides_database import MERCHANT_EMPLOYEE
# from ganimides_database import CONSUMER
# from ganimides_database import INTERACTION
# from ganimides_database import INTERACTION_MESSAGE
# from ganimides_database import BANK
# from ganimides_database import BANK_AUTHORIZATION
# from ganimides_database import BANK_SUBSCRIPTION
# from ganimides_database import BANK_ACCOUNT


# #from ganimides_database import database_schema
# #tables
# from ganimides_database import TEST
# from ganimides_database import APIS
# from ganimides_database import REGISTERED_APIS
# from ganimides_database import APPLICATIONS
# from ganimides_database import TOKENS
# from ganimides_database import DEVICES
# from ganimides_database import DEVICE_USAGE
# from ganimides_database import USERS
# from ganimides_database import CLIENTS
# from ganimides_database import CLIENT_DEVICES
# from ganimides_database import MERCHANTS
# from ganimides_database import POINTS_OF_SALES
# from ganimides_database import MERCHANT_EMPLOYEES
# from ganimides_database import CONSUMERS
# from ganimides_database import INTERACTIONS
# from ganimides_database import INTERACTION_MESSAGES
# from ganimides_database import BANKS
# from ganimides_database import BANK_AUTHORIZATIONS
# from ganimides_database import BANK_SUBSCRIPTIONS
# from ganimides_database import BANK_ACCOUNTS

#database apis
# from ganimides_database import dbapi_api_maintenance

# from ganimides_database import retrieve_rows
# from ganimides_database import display_summary
# from ganimides_database import getid

#dbapis
# from ganimides_database import dbapi_api
from ganimides_database import dbapi_api_register_unregister
from ganimides_database import dbapi_application
from ganimides_database import dbapi_application_USER
from ganimides_database import dbapi_application_api
from ganimides_database import dbapi_application_credentials_are_valid
from ganimides_database import dbapi_bank
from ganimides_database import dbapi_bank_account
from ganimides_database import dbapi_bank_authorization
from ganimides_database import dbapi_bank_subscription
from ganimides_database import dbapi_cleanup_tokens
from ganimides_database import dbapi_client
from ganimides_database import dbapi_client_device
from ganimides_database import dbapi_customer_service_assistant
from ganimides_database import dbapi_device
from ganimides_database import dbapi_device_log
from ganimides_database import dbapi_device_register_unregister
from ganimides_database import dbapi_device_usage
from ganimides_database import dbapi_verification
from ganimides_database import dbapi_email_confirmation
from ganimides_database import dbapi_mobile_confirmation
from ganimides_database import dbapi_get_bank_account_id
from ganimides_database import dbapi_get_bank_code
from ganimides_database import dbapi_interaction
from ganimides_database import dbapi_interaction_accept
from ganimides_database import dbapi_interaction_finish
from ganimides_database import dbapi_interaction_message
from ganimides_database import dbapi_interaction_message_add
from ganimides_database import dbapi_interaction_start
from ganimides_database import dbapi_merchant
from ganimides_database import dbapi_merchant_bankaccount_register
from ganimides_database import dbapi_merchant_get_bankaccounts
from ganimides_database import dbapi_pointofsale
from ganimides_database import dbapi_pointofsale_bankaccount_add
from ganimides_database import dbapi_pointofsale_bankaccount_remove
from ganimides_database import dbapi_pointofsale_credit_info
from ganimides_database import dbapi_retail_store
from ganimides_database import dbapi_service_point
from ganimides_database import dbapi_subscription
from ganimides_database import dbapi_token
from ganimides_database import dbapi_token_get_access_token
from ganimides_database import dbapi_token_is_valid
from ganimides_database import dbapi_user
 
#
#openbanking apis
from ganimides_openBankingAPI import bankaccount_remove
from ganimides_openBankingAPI import banksubscription_create
from ganimides_openBankingAPI import banksubscription_receive_authorization_from_client
from ganimides_openBankingAPI import banksubscription_register
from ganimides_openBankingAPI import banksubscription_request_authorization_from_client
from ganimides_openBankingAPI import banksubscription_unregister
from ganimides_openBankingAPI import client_banksubscription_register
from ganimides_openBankingAPI import merchant_banksubscription_register

from ganimides_openBankingAPI import authorize_and_commit_subscription
from ganimides_openBankingAPI import authorize_payment
from ganimides_openBankingAPI import authorize_subscription
from ganimides_openBankingAPI import bank_is_supported
from ganimides_openBankingAPI import change_subscription
from ganimides_openBankingAPI import commit_subscription
from ganimides_openBankingAPI import create_authorize_and_commit_subscription
from ganimides_openBankingAPI import create_subscription
from ganimides_openBankingAPI import delete_payment
from ganimides_openBankingAPI import delete_subscription
from ganimides_openBankingAPI import get_access_token
from ganimides_openBankingAPI import get_account_balances
from ganimides_openBankingAPI import get_account_details
from ganimides_openBankingAPI import get_account_payments
from ganimides_openBankingAPI import get_account_subscriptions
from ganimides_openBankingAPI import get_account_transactions
from ganimides_openBankingAPI import get_authorization_token
from ganimides_openBankingAPI import get_payment_details
from ganimides_openBankingAPI import get_payment_status
from ganimides_openBankingAPI import get_subscription_accounts
from ganimides_openBankingAPI import get_subscription_customers
from ganimides_openBankingAPI import get_subscription_details
from ganimides_openBankingAPI import post_payment

# emailing apis
from _ganimides_emails_api import emailapi_send_email_confirmation_email

# sms apis
from _ganimides_sms_api import smsapi_send_mobile_confirmation_sms

#:::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
#:::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
#::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
#::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
#::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
#::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
#::: module                                                                                                 :::
#::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
#::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
#::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
thisfolder =os.path.dirname(__file__)
module_id = 'ganimides_server'
module_version = 0.1

module_Function = 'application server'
module_ProgramName = 'ganimides_server'
module_BaseTimeStamp = datetime.datetime.now()
module_folder = os.getcwd()
module_color = thisApp.Fore.LIGHTMAGENTA_EX
module_folder = os.path.dirname(__file__)
module_ProgramName = os.path.splitext(os.path.basename(__file__))[0]
#module_id = f'{module_ProgramName}'
module_eyecatch = module_id
#module_version = 0.1
module_log_file_name = module_id+'.log'
module_errors_file_name = os.path.splitext(os.path.basename(module_log_file_name))[0]+'_errors.log'
module_versionString = f'{module_id} version {module_version}'
module_file = module_id

# log_file=thisApp.log_file_name
# print_enabled = thisApp.CONSOLE_ON
# consolelog_enabled = thisApp.CONSOLE_ON
# filelog_enabled = thisApp.FILELOG_ON

module_is_externally_configurable = False
module_identityDictionary = {
    'module_file':module_id,
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
    # 'consolelog_enabled': consolelog_enabled,
    # 'filelog_enabled': filelog_enabled,
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
    'mail_sender': 'ganimides@gmail.com',
    "application_id": module_id,
    "application_name": 'ganimidesServer',
    "application_title": 'ganimides server',
    "application_version": module_version,
    "application_function": module_Function,
    "application_ProgramName": module_ProgramName,
    "application_folder": module_folder,
    }
#::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
#::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
#::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
#::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
#::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
#::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
# module initialization
#::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
#::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
#::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
master_configuration = retrieve_module_configuration(module_identityDictionary, master_configuration, handle_as_init=False)
thisApp.pair_application_configuration(master_configuration, module_identityDictionary)
#::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
#::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
#::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::

#:::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
#:::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
#:::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
msg = f'module [{module_id}] [[version {module_version}]] loaded.'
log_message(msg)
#:::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
#:::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
#:::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::