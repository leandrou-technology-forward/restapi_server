import os
import sys

module_ProgramName = os.path.splitext(os.path.basename(__file__))[0]
module_id = '{}'.format(module_ProgramName)
module_version = 0.1

from _onlineApp import thisApp
from _onlineApp import log_message
#:::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
#:::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
#:::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
# dbapis
#:::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
#:::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
#:::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
# #from ganimides_database import dbapi_api
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
from ganimides_database import dbapi_verification
from ganimides_database import dbapi_email_confirmation
from ganimides_database import dbapi_mobile_confirmation
from ganimides_database import dbapi_customer_service_assistant
from ganimides_database import dbapi_device
from ganimides_database import dbapi_device_log
from ganimides_database import dbapi_device_register_unregister
from ganimides_database import dbapi_device_usage
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

#:::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
#:::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
#:::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
# openbanking apis
#:::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
#:::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
#:::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
from ganimides_openBankingAPI import client_banksubscription_register
from ganimides_openBankingAPI import merchant_banksubscription_register

from ganimides_openBankingAPI import bankaccount_remove
from ganimides_openBankingAPI import banksubscription_create
from ganimides_openBankingAPI import banksubscription_receive_authorization_from_client
from ganimides_openBankingAPI import banksubscription_register
from ganimides_openBankingAPI import banksubscription_request_authorization_from_client
from ganimides_openBankingAPI import banksubscription_unregister

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
#:::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
#:::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
#:::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
# mix apis
#:::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
#:::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
#:::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
#from _ganimides_mix_api import xclient_banksubscription_register
#from _ganimides_mix_api import xmerchant_banksubscription_register

#:::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
#:::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
#:::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
# email apis
#:::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
#:::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
#:::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
from _ganimides_emails_api import emailapi_send_email_confirmation_email
#:::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
#:::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
#:::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
# sms apis
#:::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
#:::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
#:::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
from _ganimides_sms_api import smsapi_send_mobile_confirmation_sms
#:::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
#:::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
#:::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
thisfolder =os.path.dirname(__file__)
module_id = os.path.basename(thisfolder)
module_version = 0.1
msg = f'module [{module_id}] [[version {module_version}]] loaded.'
log_message(msg)
#:::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
#:::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
#:::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::

