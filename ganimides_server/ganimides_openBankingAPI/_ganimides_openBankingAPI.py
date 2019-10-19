# -*- coding: utf-8 -*-
import os
import sys
import datetime
if not (os.path.dirname(os.path.dirname(__file__)) in sys.path): sys.path.append(os.path.dirname(os.path.dirname(__file__)))
if not (os.path.dirname(__file__) in sys.path): sys.path.append(os.path.dirname(__file__))

from _onlineApp import thisApp
from _onlineApp import get_debug_option_as_level, log_message, retrieve_module_configuration, get_globals_from_configuration, save_module_configuration
from _onlineApp import log_process_start, log_process_finish, log_process_message, log_process_result, log_process_data, log_process_input, log_process_output
from _onlineApp import set_process_identity_dict, set_process_caller_area,add_apis_to_configuration,get_module_debug_level
from _onlineApp import build_process_signature, build_process_call_area, get_debug_level, get_debug_files

import ganimides_database as db
import ganimides_bankingAPI as bankingAPI
import _database_ganimides_model as dbmodel
#::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
#::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
#::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
#::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
#::: module                                                                                                 :::
#::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
#::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
#::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
module_Function = 'database adapter'
module_ProgramName = 'database api'
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
    }
#::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
#::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
#::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
#::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
#::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
# api services : database apis
#::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
#::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
#::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
#::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
#::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
#::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
# api services : database apis
#::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
#::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
#::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
#banksubscription_create + banksubscription_request_authorization_from_client
def banksubscription_register(dbsession, client_id, bank_id, application_name, allow_transactionHistory=True, allow_balance=True, allow_details=True, allow_checkFundsAvailability=True, payments_limit=1000, payments_currency='EUR', payments_amount=100, caller_area={}):
    _api_name = "banksubscription_register"
    _api_entity = 'BANK_SUBSCRIPTION'
    _api_action = 'register'
    _api_msgID = set_msgID(_api_name, _api_action, _api_entity)

    _process_identity_kwargs = {'type': 'api', 'module': module_id, 'name': _api_name, 'action': _api_action, 'entity': _api_entity, 'msgID': _api_msgID,}
    _process_adapters_kwargs = {'dbsession': dbsession}
    _process_log_kwargs = {'indent_method': 'AUTO', 'indent_level':None}
    _process_debug_level = get_debug_level(caller_area.get('debug_level'), **_process_identity_kwargs, **_process_adapters_kwargs)
    _process_debug_files = get_debug_files(_process_debug_level, **_process_identity_kwargs, **_process_adapters_kwargs)
    _process_debug_kwargs={'debug_level':_process_debug_level,'debug_files':_process_debug_files}

    _process_signature = build_process_signature(**_process_identity_kwargs, **_process_adapters_kwargs, **_process_debug_kwargs, **_process_log_kwargs)
    _process_call_area = build_process_call_area(_process_signature, caller_area)

    log_process_start(_api_msgID,**_process_call_area)

    log_process_input('', 'client_id', client_id, **_process_call_area)
    log_process_input('', 'bank_id', bank_id, **_process_call_area)
    log_process_input('', 'allow_transactionHistory', allow_transactionHistory, **_process_call_area)
    log_process_input('', 'allow_balance', allow_balance, **_process_call_area)
    log_process_input('', 'allow_details', allow_details, **_process_call_area)
    log_process_input('', 'allow_checkFundsAvailability', allow_checkFundsAvailability, **_process_call_area)
    log_process_input('', 'payments_limit', payments_limit, **_process_call_area)
    log_process_input('', 'payments_currency', payments_currency, **_process_call_area)
    log_process_input('', 'payments_amount', payments_amount, **_process_call_area)
    log_process_input('', 'caller_area', caller_area, **_process_call_area)

    application = dbsession.get(dbmodel.APPLICATION, {'application_name': application_name}, caller_area=_process_call_area)
    if not application:
        msg = f'application not found'
        api_result = {'api_status': 'error', 'api_message': msg, 'api_data': {}, 'api_action': _api_action.upper(), 'api_name': _api_name}
        log_process_finish(_api_msgID, api_result, **_process_call_area)    
        return api_result

    client = dbsession.get(dbmodel.CLIENT, {'client_id': client_id}, caller_area=_process_call_area)
    if not client:
        msg = f'client not found'
        api_result = {'api_status': 'error', 'api_message': msg, 'api_data': {}, 'api_action': _api_action.upper(), 'api_name': _api_name}
        log_process_finish(_api_msgID, api_result, **_process_call_area)    
        return api_result
    if not client.status=='Active':
        msg = f"client not Active.(status:{client.status})"
        api_result = {'api_status': 'error', 'api_message': msg, 'api_data': {}, 'api_action': _api_action.upper(), 'api_name': _api_name}
        log_process_finish(_api_msgID, api_result, **_process_call_area)    
        return api_result

    bank = dbsession.get(dbmodel.BANK, {'bank_id': bank_id}, caller_area=_process_call_area)
    if not bank:
        bank = dbsession.get(dbmodel.BANK, {'bank_code': bank_id}, caller_area=_process_call_area)
        if not bank:
            bank = dbsession.get(dbmodel.BANK, {'bank_BIC': bank_id}, caller_area=_process_call_area)
    if not bank:
        msg = f'bank not found'
        api_result = {'api_status': 'error', 'api_message': msg, 'api_data': {}, 'api_action': _api_action.upper(), 'api_name': _api_name}
        log_process_finish(_api_msgID, api_result, **_process_call_area)    
        return api_result
    if not bank.status=='Active':
        msg = f"bank not Active.(status:{bank.status})"
        api_result = {'api_status': 'error', 'api_message': msg, 'api_data': {}, 'api_action': _api_action.upper(), 'api_name': _api_name}
        log_process_finish(_api_msgID, api_result, **_process_call_area)    
        return api_result
        
    application_id = application.application_id
    client_id = client.client_id
    client_email=client.email
    client_type=client.client_type
    bank_code = bank.bank_code
    bank_id = bank.bank_id
    #bank_BIC = bank.bank_BIC

    if allow_transactionHistory:
        allow_transactionHistory = True
    else:
        allow_transactionHistory = False

    if allow_balance:
        allow_balance = True
    else:
        allow_balance = False
    
    if allow_details:
        allow_details = True
    else:
        allow_details = False
    
    if allow_checkFundsAvailability:
        allow_checkFundsAvailability = True
    else:
        allow_checkFundsAvailability = False
    

    #step-1: create a subscription record
    create_result = bankingAPI.create_subscription(bank_code, allow_transactionHistory=allow_transactionHistory, allow_balance=allow_balance, allow_details=allow_details, allow_checkFundsAvailability=allow_checkFundsAvailability, payments_limit=payments_limit, payments_currency=payments_currency, payments_amount=payments_amount)
    if not create_result:
        create_result={}
    if not create_result.get('status')=='success':
        msg = f"{bank_code} subscription not created.(status:{create_result.get('message','?')})"
        api_result = {'api_status': 'error', 'api_message': msg, 'api_action': _api_action.upper(), 'api_name': _api_name}
        log_process_finish(_api_msgID, api_result, **_process_call_area)
        return api_result

    #get the subscription id
    subscription_id=create_result.get('data',{}).get('subscriptionId')
    if not subscription_id:
        msg = f"subscription_id not created.(status:{create_result.get('message','?')})"
        api_result = {'api_status': 'error', 'api_message': msg, 'api_action': _api_action.upper(), 'api_name': _api_name}
        log_process_finish(_api_msgID, api_result, **_process_call_area)
        return api_result
  
    msg='ok.subscription {subscription_id} obtained from bank {bank_code}'
    log_process_message('', 'sucess',msg, **_process_call_area)

    #step-2: get client consent (authorization) from the bank customer
    authorization_result = bankingAPI.authorize_subscription(bank_code, subscription_id)
    if not authorization_result:
        msg='authorization request FAILED'
        api_result = {'api_status': 'error', 'api_message': msg, 'api_action': _api_action.upper(), 'api_name': _api_name}
        log_process_finish(_api_msgID, api_result, **_process_call_area)
        return api_result
    
    #step-23: log the authorization request
    subscription_authorization_request={
        'bank_subscriptionID': subscription_id,
        'application_name': application_name,
        'application_id': application_id,
        'client_id': client_id,
        'client_type': client_type,
        'client_name': client_email,
        'bank_id': bank_id,
        'bank_code': bank_code,
        'status':'Pending',
        }
    log_process_data('', 'subscription_authorization_request', subscription_authorization_request, **_process_call_area)
    
    bank_authorization = dbsession.insert(dbmodel.BANK_AUTHORIZATION, subscription_authorization_request, auto_commit=True, caller_area=_process_call_area)
    if not bank_authorization:
        msg = f'bank_authorization insert failed'
        api_result = {'api_status': 'error', 'api_message': msg, 'api_action': _api_action.upper(), 'api_name': _api_name}
        log_process_finish(_api_msgID, api_result, **_process_call_area)
        return api_result

    bank_authorization_id = bank_authorization.bank_authorization_id
    if not bank_authorization_id:
        msg='authorization request FAILED. (insert request system error)'
        api_result = {'api_status': 'error', 'api_message': msg, 'api_action': _api_action.upper(), 'api_name': _api_name}
        log_process_finish(_api_msgID, api_result, **_process_call_area)
        return api_result

    bank_authorization_record = bank_authorization.to_dict()

    msg=f'authorization requested from client. (ganimides authorization request is {bank_authorization_id})'
    api_result = {'api_status': 'success', 'api_message': msg, 'api_data': bank_authorization_record, 'bank_authorization_id': bank_authorization_id, 'api_action': _api_action.upper(), 'api_name': _api_name}
    log_process_finish(_api_msgID, api_result, **_process_call_area)
    return api_result
#::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
def banksubscription_receive_authorization_from_client(dbsession, bank_code, authorization_code, caller_area={}):
    _api_name = "banksubscription_receive_authorization_from_client"
    _api_entity = 'AUTHORIZATION'
    _api_action = 'receive'
    _api_msgID = set_msgID(_api_name, _api_action, _api_entity)

    _process_identity_kwargs = {'type': 'api', 'module': module_id, 'name': _api_name, 'action': _api_action, 'entity': _api_entity, 'msgID': _api_msgID,}
    _process_adapters_kwargs = {'dbsession': dbsession}
    _process_log_kwargs = {'indent_method': 'AUTO', 'indent_level':None}
    _process_debug_level = get_debug_level(caller_area.get('debug_level'), **_process_identity_kwargs, **_process_adapters_kwargs)
    _process_debug_files = get_debug_files(_process_debug_level, **_process_identity_kwargs, **_process_adapters_kwargs)
    _process_debug_kwargs={'debug_level':_process_debug_level,'debug_files':_process_debug_files}

    _process_signature = build_process_signature(**_process_identity_kwargs, **_process_adapters_kwargs, **_process_debug_kwargs, **_process_log_kwargs)
    _process_call_area = build_process_call_area(_process_signature, caller_area)

    log_process_start(_api_msgID,**_process_call_area)

    simulation_enabled=caller_area.get('simulation_enabled')

    log_process_input('', 'bank_code', bank_code, **_process_call_area)
    log_process_input('', 'authorization_code', authorization_code, **_process_call_area)
    log_process_input('', 'caller_area', caller_area, **_process_call_area)

    log_process_input('', 'simulation_enabled', simulation_enabled, **_process_call_area)

    if simulation_enabled:
        authorization_token = '1212121212121212simulated_authorization_token'
    else:
        authorization_token = get_authorization_token(bank_code, authorization_code)

    if not authorization_token:
        msg = f'authorization token failed for authorization_code={authorization_code}'
        log_process_message('', 'error', msg, **_process_call_area)
        api_result = {'api_status': 'error', 'api_message': msg, 'api_action': _api_action.upper(), 'api_name': _api_name}
        log_process_finish(_api_msgID, api_result, **_process_call_area)
        return api_result

    msg = f'authorization token received from bank {bank_code} for authorization_code {authorization_code} '
    log_process_message('', 'success', msg, **_process_call_area)
    log_process_data('', 'authorization_token', authorization_token, **_process_call_area)
    
    pending_authorizations_filter = {'status': 'Pending', 'bank_code': bank_code}

    pending_authorizations = dbsession.get_rows(dbmodel.BANK_AUTHORIZATION, pending_authorizations_filter, caller_area=_process_call_area)
    if not pending_authorizations:
        msg = f'no pending authorizations for bank [{bank_code}]'
        log_process_message('', 'system error', msg, **_process_call_area)
        api_result = {'api_status': 'error', 'api_message': msg, 'api_action': _api_action.upper(), 'api_name': _api_name}
        log_process_finish(_api_msgID, api_result, **_process_call_area)
        return api_result

    msg=f'[{len(pending_authorizations)} pending_authorizations] for bank [{bank_code}]'
    log_process_message('', 'success', msg, **_process_call_area)

    ix = 0
    failed = 0
    authorized = 0
    app_name=None
    for pending_authorization in pending_authorizations:
        ix = ix + 1
        authorization_rec = pending_authorization.to_dict()
        bank_code = pending_authorization.bank_code
        subscription_id = pending_authorization.bank_subscriptionID
        application_name = pending_authorization.application_name
        if not app_name:
            app_name = application_name
        else:
            if not app_name == application_name:
                application_name=''

        authorization_rec.update({'last_usage_timestamp': datetime.datetime.utcnow()})

        if simulation_enabled:
            commit_result = {'status': 'success'}
        else:
            commit_result = commit_subscription(bank_code, authorization_token, subscription_id)

        if not commit_result.get('status') == 'success':
            errorMsg = commit_result.get('message')
            msg=f"{ix}. subscription [{bank_code} {subscription_id}] COMMIT FAILED:{errorMsg}"
            log_process_message('', 'warning', msg, **_process_call_area)

            if errorMsg.upper().find('already active/revoked'.upper())>=0:
                authorization_rec.update({'status': 'Already_Registered','error': errorMsg})
                pending_authorization = dbsession.update(dbmodel.BANK_AUTHORIZATION, authorization_rec, auto_commit=True, caller_area=_process_call_area)
            else:
                msg='most probable no accounts selected so far'
                log_process_message('', 'warning', msg, **_process_call_area)
            continue

        msg=f"{ix}. subscription [{bank_code}]-[{subscription_id}] committed via commit_subscription"
        log_process_message('', 'success', msg, **_process_call_area)
        
        authorization_rec.update({
            'status': 'Committed',
            'authorization_code': authorization_code,
            'authorization_token': authorization_token,
            })
        res = dbsession.table_action(dbmodel.BANK_AUTHORIZATION, 'UPDATE', authorization_rec, action_filter={}, auto_commit=True, caller_area=_process_call_area)
        if not res.get('api_status')=='success':
            errorMsg = res.get('api_message')
            msg=f"{ix}. subscription [{bank_code} {subscription_id}]: bank_authorizations UPDATE FAILED: {errorMsg}"
            failed = failed + 1
            log_process_message('', 'error', msg, **_process_call_area)
            continue

        authorization_rec=pending_authorization.to_dict()

        bank_subscription_record = authorization_rec
        bank_subscription_record.update({'status': 'Active'})

        result = dbsession.table_action(dbmodel.BANK_SUBSCRIPTION, 'REGISTER', bank_subscription_record, action_filter={}, auto_commit=True, caller_area=_process_call_area)
        if not result.get('api_status')=='success':
            failed = failed + 1
            errorMsg = result.get('api_message')
            msg=f"{ix}. subscription [{bank_code} {subscription_id}]: bank_authorizations UPDATE FAILED: {errorMsg}"
            log_process_message('', 'error', msg, **_process_call_area)
            continue

        bank_subscription_record = result.get('api_data', {})

        authorized = authorized + 1
        msg=f"f{ix}. subscription [{bank_code} {subscription_id}]: bank_subscription REGISTERED: {result.get('api_message')}"
        log_process_message('', 'success', msg, **_process_call_area)

        msg = f'get subscription details from bank {bank_code}. subscription_id: {subscription_id} '
        log_process_message('', 'success', msg, **_process_call_area)
        
        if simulation_enabled:
            subscription_details = {
                'subscriptionId': bank_subscription_record.get('bank_subscriptionID'),
                'status ': ' ACTV ', ' description ': ' SUBSCRIPTION ', 
                'selectedAccounts': [{'accountId':'351012345671'}, {'accountId':'351092345672'},{'accountId':'351012345673'}, {'accountId':'351012345674'}],
                'accounts': {'transactionHistory': True, 'balance': True, 'details': True, 'checkFundsAvailability': True},
                'payments': {'limit': 1000, 'currency': 'EUR', 'amount': 100}
                }
        else:
            subscription_details = get_subscription_details(bank_code, subscription_id)

        log_process_data('', 'subscription_details', subscription_details, **_process_call_area)


        # {'subscriptionId': 'Subid000001-1567594559623',
        # 'status ': ' ACTV ', ' description ': ' SUBSCRIPTION ', 
        # 'selectedAccounts': [{'accountId':'351012345671'}, {'accountId':'351092345672'}],
        # 'accounts': {'transactionHistory': True, 'balance': True, 'details': True, 'checkFundsAvailability': True},
        # 'payments': {'limit': 1000, 'currency': 'EUR', 'amount': 100}}

        payments_limit = subscription_details.get('payments',{}).get('limit',0)
        payments_currency = subscription_details.get('payments', {}).get('currency', 'EUR')
        if payments_currency not in ('EUR', 'USD', 'STG'):
            payments_currency='EUR'
        payments_amount = subscription_details.get('payments', {}).get('amount', 0)

        #'accounts': {'transactionHistory': True, 'balance': True, 'details': True, 'checkFundsAvailability': True},
        account_allow_transactionHistory = int(subscription_details.get('accounts', {}).get('transactionHistory', 0))
        account_allow_balance = int(subscription_details.get('accounts',{}).get('balance',0))
        account_allow_details = int(subscription_details.get('accounts',{}).get('details',0))
        account_allow_checkFundsAvailability = int(subscription_details.get('accounts',{}).get('checkFundsAvailability',0))

        #'selectedAccounts': [{'accountId':'351012345671'}, {'accountId':'351092345672'}],
        selectedAccounts = subscription_details.get('selectedAccounts', [])

        log_process_data('', 'payments_limit', payments_limit, **_process_call_area)
        log_process_data('', 'payments_currency', payments_currency, **_process_call_area)
        log_process_data('', 'payments_amount', payments_amount, **_process_call_area)
        log_process_data('', 'account_allow_transactionHistory', account_allow_transactionHistory, **_process_call_area)
        log_process_data('', 'account_allow_balance', account_allow_balance, **_process_call_area)
        log_process_data('', 'account_allow_details', account_allow_details, **_process_call_area)
        log_process_data('', 'account_allow_checkFundsAvailability', account_allow_checkFundsAvailability, **_process_call_area)
        log_process_data('', 'selectedAccounts', selectedAccounts, **_process_call_area)

        bank_subscription_record.update({
            'payments_limit': payments_limit,
            'payments_currency': payments_currency,
            'payments_amount': payments_amount,
            'account_allow_transactionHistory': account_allow_transactionHistory,
            'account_allow_balance': account_allow_balance,
            'account_allow_details': account_allow_details,
            'account_allow_checkFundsAvailability': account_allow_checkFundsAvailability,
            })

        #again
        result = dbsession.table_action(dbmodel.BANK_SUBSCRIPTION, 'REFRESH', bank_subscription_record, action_filter={}, auto_commit=True, caller_area=_process_call_area)
        if not result.get('api_status')=='success':
            failed = failed + 1
            errorMsg = result.get('api_message')
            msg=f"{ix}. subscription [{bank_code} {subscription_id}]: bank_authorizations UPDATE FAILED: {errorMsg}"
            log_process_message('', 'error', msg, **_process_call_area)
            continue

        if not result.get('api_status')=='success':
            errorMsg = result.get('api_message')
            msg=f"subscription [{bank_code} {subscription_id}]: bank_subscriptions UPDATE FAILED: {errorMsg}"
            log_process_message('', 'error', msg, **_process_call_area)

        bank_account_record = bank_subscription_record
        bank_account_record.update({
            'payments_limit': payments_limit,
            'payments_currency': payments_currency,
            'payments_amount': payments_amount,
            'account_allow_transactionHistory': account_allow_transactionHistory,
            'account_allow_balance': account_allow_balance,
            'account_allow_details': account_allow_details,
            'account_allow_checkFundsAvailability': account_allow_checkFundsAvailability,
            })

        aix=0
        for account in selectedAccounts:
            aix = aix + 1
            account_id = account.get('accountId')
            bank_account_record = bank_subscription_record
            bank_account_record.update({
                'bank_accountID':account_id,
                'payments_limit': payments_limit,
                'payments_currency': payments_currency,
                'payments_amount': payments_amount,
                'account_allow_transactionHistory': account_allow_transactionHistory,
                'account_allow_balance': account_allow_balance,
                'account_allow_details': account_allow_details,
                'account_allow_checkFundsAvailability': account_allow_checkFundsAvailability,
                })

            result = dbsession.table_action(dbmodel.BANK_ACCOUNT, 'REGISTER', bank_account_record, action_filter={}, auto_commit=True, caller_area=_process_call_area)
            if result.get('api_status')=='success':
                msg=f"{aix}. account:{account_id} REGISTERED"
                log_process_message('', 'success', msg, **_process_call_area)
            else:
                msg=f"{aix}. account:{account_id} REGISTRATION FAILED"
                log_process_message('', 'error', msg, **_process_call_area)
        
        #final authorization update
        authorization_rec=pending_authorization.to_dict()
        authorization_rec.update({'status': 'Registered','error':''})
        authorization_rec.update({'last_usage_timestamp': datetime.datetime.utcnow()})
        res = dbsession.table_action(dbmodel.BANK_AUTHORIZATION, 'UPDATE', authorization_rec, action_filter={}, auto_commit=True, caller_area=_process_call_area)
        if not result.get('api_status')=='success':
            errorMsg = res.get('api_message')
            msg=f"{ix}. subscription [{bank_code} {subscription_id}]: bank_authorizations UPDATE FAILED: {errorMsg}"
            failed = failed + 1
            log_process_message('', 'error', msg, **_process_call_area)
            continue
        authorization_rec=pending_authorization.to_dict()
    

    authorization_recs=dbsession.rows_to_dict(dbmodel.BANK_AUTHORIZATION, pending_authorizations, caller_area=_process_call_area)
    
    #db.dbapi_cleanup_bank_authorizations(dbsession)
    
    if authorized > 0:
        msg = f'OK. authorization code received. {authorized} subscriptions authorized, {failed} failed.'
        api_result = {'api_status': 'success', 'api_message': msg, 'application_name': application_name, 'api_data':authorization_recs}
    else:
        msg = f'authorization code NOT received. {authorized} subscriptions authorized, {failed} failed.'
        api_result = {'api_status': 'error', 'api_message': msg, 'application_name': application_name, 'api_data':authorization_recs}
    
    log_process_finish(_api_msgID, api_result, **_process_call_area)
    return api_result
#::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
def banksubscription_unregister(dbsession, client_id, bank_id, application_name, subscription_id, caller_area={}):
    _api_name = "banksubscription_unregister"
    _api_entity = 'BANK_SUBSCRIPTION'
    _api_action = 'unregister'
    _api_msgID = set_msgID(_api_name, _api_action, _api_entity)

    _process_identity_kwargs = {'type': 'api', 'module': module_id, 'name': _api_name, 'action': _api_action, 'entity': _api_entity, 'msgID': _api_msgID,}
    _process_adapters_kwargs = {'dbsession': dbsession}
    _process_log_kwargs = {'indent_method': 'AUTO', 'indent_level':None}
    _process_debug_level = get_debug_level(caller_area.get('debug_level'), **_process_identity_kwargs, **_process_adapters_kwargs)
    _process_debug_files = get_debug_files(_process_debug_level, **_process_identity_kwargs, **_process_adapters_kwargs)
    _process_debug_kwargs={'debug_level':_process_debug_level,'debug_files':_process_debug_files}

    _process_signature = build_process_signature(**_process_identity_kwargs, **_process_adapters_kwargs, **_process_debug_kwargs, **_process_log_kwargs)
    _process_call_area = build_process_call_area(_process_signature, caller_area)

    log_process_start(_api_msgID,**_process_call_area)

    log_process_input('', 'client_id', client_id, **_process_call_area)
    log_process_input('', 'bank_id', bank_id, **_process_call_area)
    log_process_input('', 'application_name', application_name, **_process_call_area)
    log_process_input('', 'subscription_id', subscription_id, **_process_call_area)
    log_process_input('', 'caller_area', caller_area, **_process_call_area)

    subscriptions_filter={}
    if client_id and client_id not in ('*',''):
        subscriptions_filter.update({'client_id':client_id})

    if subscription_id and subscription_id not in ('*',''):
        subscription = dbsession.get(dbmodel.BANK_SUBSCRIPTION, {'bank_subscription_id': subscription_id}, caller_area=_process_call_area)
        if not subscription:
            subscriptions_filter.update({'bank_subscriptionID':subscription_id})
        else:
            subscriptions_filter.update({'bank_subscription_id':subscription_id})

    if application_name and application_name not in ('*', ''):
        application = dbsession.get(dbmodel.APPLICATION, {'application_name': application_name}, caller_area=_process_call_area)
        if application:
            subscriptions_filter.update({'application_id':application.application_id})
        else:
            application = dbsession.get(dbmodel.APPLICATION, {'application_id': application_name}, caller_area=_process_call_area)
            if application:
                subscriptions_filter.update({'application_id':application.application_id})
            else:
                subscriptions_filter.update({'application_id':'?'})

    if bank_id and bank_id not in ('*', ''):
        bank = dbsession.get(dbmodel.BANK, {'bank_id': bank_id}, caller_area=_process_call_area)
        if not bank:
            bank = dbsession.get(dbmodel.BANK, {'bank_code': bank_id}, caller_area=_process_call_area)
            if not bank:
                bank = dbsession.get(dbmodel.BANK, {'bank_BIC': bank_id}, caller_area=_process_call_area)
        if bank:
            subscriptions_filter.update({'bank_id':bank.bank_id})
            subscriptions_filter.update({'bank_code': bank.bank_code})
        else:
            subscriptions_filter.update({'bank_id':'?'})
            subscriptions_filter.update({'bank_code': '?'})


    subscriptions = dbsession.get_rows(dbmodel.BANK_SUBSCRIPTION, subscriptions_filter, caller_area=_process_call_area)
    if not subscriptions:
        msg = f'no subscriptions found'
        log_process_message('', 'error', msg, **_process_call_area)
        api_result = {'api_status': 'error', 'api_message': msg, 'api_action': _api_action.upper(), 'api_name': _api_name}
        log_process_finish(_api_msgID, api_result, **_process_call_area)
        return api_result

    update_expr={'status':'UnRegistered'}

    subsUnregistered=0       
    acctsUnregistered=0       
    for subscription in subscriptions:
        accounts_filter = {'bank_subscription_id': subscription.bank_subscription_id}
        update_expr={'status':'UnRegistered'}
        api_result = dbsession.table_action(dbmodel.BANK_ACCOUNT, 'UPDATE_ROWS', update_expr, action_filter=accounts_filter, auto_commit=False, caller_area=_process_call_area)
        if not api_result.get('api_status')=='success':
            msg = api_result.get('api_message')
            log_process_message('', 'error',msg, **_process_call_area)
        else:            
            msg = api_result.get('api_message')
            log_process_message('', 'success',msg, **_process_call_area)
            acctsUnregistered = acctsUnregistered + api_result.get('rows_updated', 0)
        sub_filter={'bank_subscription_id': subscription.bank_subscription_id}
        sub_update=update_expr
        sub_update.update({'bank_subscription_id': subscription.bank_subscription_id})
        api_result = dbsession.table_action(dbmodel.BANK_SUBSCRIPTION, 'UPDATE', sub_update, action_filter=sub_filter, auto_commit=False, caller_area=_process_call_area)
        if not api_result.get('api_status')=='success':
            msg = api_result.get('api_message')
            log_process_message('', 'error',msg, **_process_call_area)
        else:            
            msg = api_result.get('api_message')
            log_process_message('', 'success',msg, **_process_call_area)
            subsUnregistered = subsUnregistered + api_result.get('rows_updated', 0)

    dbsession.commit(**_process_call_area)
    subscriptions_rec = dbsession.rows_to_dict(dbmodel.BANK_SUBSCRIPTION, subscriptions, caller_area=_process_call_area)
    
    msg=f'{subsUnregistered} bank subscription(s) unregistered, with {acctsUnregistered} bank account(s)'
    api_result = {'api_status': 'success', 'api_message': msg, 'api_data': subscriptions_rec}
    log_process_finish(_api_msgID, api_result, **_process_call_area)
    return api_result    
#::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
def bankaccount_remove(dbsession, client_id, bank_id, application_name, account_id, caller_area={}):
    _api_name = "bankaccount_remove"
    _api_entity = 'BANK_ACCOUNT'
    _api_action = 'remove'
    _api_msgID = set_msgID(_api_name, _api_action, _api_entity)

    _process_identity_kwargs = {'type': 'api', 'module': module_id, 'name': _api_name, 'action': _api_action, 'entity': _api_entity, 'msgID': _api_msgID,}
    _process_adapters_kwargs = {'dbsession': dbsession}
    _process_log_kwargs = {'indent_method': 'AUTO', 'indent_level':None}
    _process_debug_level = get_debug_level(caller_area.get('debug_level'), **_process_identity_kwargs, **_process_adapters_kwargs)
    _process_debug_files = get_debug_files(_process_debug_level, **_process_identity_kwargs, **_process_adapters_kwargs)
    _process_debug_kwargs={'debug_level':_process_debug_level,'debug_files':_process_debug_files}

    _process_signature = build_process_signature(**_process_identity_kwargs, **_process_adapters_kwargs, **_process_debug_kwargs, **_process_log_kwargs)
    _process_call_area = build_process_call_area(_process_signature, caller_area)

    log_process_start(_api_msgID,**_process_call_area)

    log_process_input('', 'client_id', client_id, **_process_call_area)
    log_process_input('', 'bank_id', bank_id, **_process_call_area)
    log_process_input('', 'application_name', application_name, **_process_call_area)
    log_process_input('', 'account_id', account_id, **_process_call_area)
    log_process_input('', 'caller_area', caller_area, **_process_call_area)

    accounts_filter={}
    if client_id and client_id not in ('*',''):
        accounts_filter.update({'client_id':client_id})

    if account_id and account_id not in ('*',''):
        account = dbsession.get(dbmodel.BANK_ACCOUNT, {'bank_account_id': account_id}, caller_area=_process_call_area)
        if not account:
            accounts_filter.update({'bank_accountID':account_id})
        else:
            accounts_filter.update({'bank_account_id':account_id})

    if application_name and application_name not in ('*', ''):
        application = dbsession.get(dbmodel.APPLICATION, {'application_name': application_name}, caller_area=_process_call_area)
        if application:
            accounts_filter.update({'application_id':application.application_id})
        else:
            application = dbsession.get(dbmodel.APPLICATION, {'application_id': application_name}, caller_area=_process_call_area)
            if application:
                accounts_filter.update({'application_id':application.application_id})
            else:
                accounts_filter.update({'application_id':'?'})

    if bank_id and bank_id not in ('*', ''):
        bank = dbsession.get(dbmodel.BANK, {'bank_id': bank_id}, caller_area=_process_call_area)
        if not bank:
            bank = dbsession.get(dbmodel.BANK, {'bank_code': bank_id}, caller_area=_process_call_area)
            if not bank:
                bank = dbsession.get(dbmodel.BANK, {'bank_BIC': bank_id}, caller_area=_process_call_area)
        if bank:
            accounts_filter.update({'bank_id':bank.bank_id})
            accounts_filter.update({'bank_code': bank.bank_code})
        else:
            accounts_filter.update({'bank_id':'?'})
            accounts_filter.update({'bank_code': '?'})

    update_expr={'status':'Removed'}
    api_result = dbsession.table_action(dbmodel.BANK_ACCOUNT, 'UPDATE_ROWS', update_expr, action_filter=accounts_filter, auto_commit=True, caller_area=_process_call_area)
    if api_result.get('api_status')=='success':
        upd = api_result.get('changed_records', 0)
        msg=f'{upd} bank account(s) removed'
        api_result.update({'api_message':msg})

    log_process_finish(_api_msgID, api_result, **_process_call_area)
    return api_result
#::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
def banksubscription_create(dbsession, client_id, bank_id, application_name='', allow_transactionHistory=True, allow_balance=True, allow_details=True, allow_checkFundsAvailability=True, payments_limit=1000, payments_currency='EUR', payments_amount=100, caller_area={}):
    _api_name = "banksubscription_create"
    _api_entity = 'BANK_SUBSCRIPTION'
    _api_action = 'create'
    _api_msgID = set_msgID(_api_name, _api_action, _api_entity)

    _process_identity_kwargs = {'type': 'api', 'module': module_id, 'name': _api_name, 'action': _api_action, 'entity': _api_entity, 'msgID': _api_msgID,}
    _process_adapters_kwargs = {'dbsession': dbsession}
    _process_log_kwargs = {'indent_method': 'AUTO', 'indent_level':None}
    _process_debug_level = get_debug_level(caller_area.get('debug_level'), **_process_identity_kwargs, **_process_adapters_kwargs)
    _process_debug_files = get_debug_files(_process_debug_level, **_process_identity_kwargs, **_process_adapters_kwargs)
    _process_debug_kwargs={'debug_level':_process_debug_level,'debug_files':_process_debug_files}

    _process_signature = build_process_signature(**_process_identity_kwargs, **_process_adapters_kwargs, **_process_debug_kwargs, **_process_log_kwargs)
    _process_call_area = build_process_call_area(_process_signature, caller_area)

    log_process_start(_api_msgID,**_process_call_area)

    log_process_input('', 'client_id', client_id, **_process_call_area)
    log_process_input('', 'bank_id', bank_id, **_process_call_area)
    log_process_input('', 'allow_transactionHistory', allow_transactionHistory, **_process_call_area)
    log_process_input('', 'allow_balance', allow_balance, **_process_call_area)
    log_process_input('', 'allow_details', allow_details, **_process_call_area)
    log_process_input('', 'allow_checkFundsAvailability', allow_checkFundsAvailability, **_process_call_area)
    log_process_input('', 'payments_limit', payments_limit, **_process_call_area)
    log_process_input('', 'payments_currency', payments_currency, **_process_call_area)
    log_process_input('', 'payments_amount', payments_amount, **_process_call_area)
    log_process_input('', 'caller_area', caller_area, **_process_call_area)
    
    application = dbsession.get(dbmodel.APPLICATION, {'application_name': application_name}, caller_area=_process_call_area)
    if not application:
        msg = f'application not found'
        api_result = {'api_status': 'error', 'api_message': msg, 'api_data': {}, 'api_action': _api_action.upper(), 'api_name': _api_name}
        log_process_finish(_api_msgID, api_result, **_process_call_area)    
        return api_result

    client = dbsession.get(dbmodel.CLIENT, {'client_id': client_id}, caller_area=_process_call_area)
    if not client:
        msg = f'client not found'
        api_result = {'api_status': 'error', 'api_message': msg, 'api_data': {}, 'api_action': _api_action.upper(), 'api_name': _api_name}
        log_process_finish(_api_msgID, api_result, **_process_call_area)    
        return api_result
    if not client.status=='Active':
        msg = f"client not Active.(status:{client.status})"
        api_result = {'api_status': 'error', 'api_message': msg, 'api_data': {}, 'api_action': _api_action.upper(), 'api_name': _api_name}
        log_process_finish(_api_msgID, api_result, **_process_call_area)    
        return api_result

    bank = dbsession.get(dbmodel.BANK, {'bank_id': bank_id}, caller_area=_process_call_area)
    if not bank:
        bank = dbsession.get(dbmodel.BANK, {'bank_code': bank_id}, caller_area=_process_call_area)
        if not bank:
            bank = dbsession.get(dbmodel.BANK, {'bank_BIC': bank_id}, caller_area=_process_call_area)
    if not bank:
        msg = f'bank not found'
        api_result = {'api_status': 'error', 'api_message': msg, 'api_data': {}, 'api_action': _api_action.upper(), 'api_name': _api_name}
        log_process_finish(_api_msgID, api_result, **_process_call_area)    
        return api_result
    if not bank.status=='Active':
        msg = f"bank not Active.(status:{bank.status})"
        api_result = {'api_status': 'error', 'api_message': msg, 'api_data': {}, 'api_action': _api_action.upper(), 'api_name': _api_name}
        log_process_finish(_api_msgID, api_result, **_process_call_area)    
        return api_result
        
    client_id = client.client_id
    bank_code = bank.bank_code
    bank_id = bank.bank_id

    application_id = application.application_id
    client_id = client.client_id
    client_email=client.email
    client_type=client.client_type
    bank_code = bank.bank_code
    bank_id = bank.bank_id
    #bank_BIC = bank.bank_BIC

    create_result = bankingAPI.create_subscription(bank_code, allow_transactionHistory=allow_transactionHistory, allow_balance=allow_balance, allow_details=allow_details, allow_checkFundsAvailability=allow_checkFundsAvailability, payments_limit=payments_limit, payments_currency=payments_currency, payments_amount=payments_amount)
    if not create_result.get('status')=='success':
        msg = f"not created.(status:{create_result.get('message','?')})"
        api_result = {'api_status': 'error', 'api_message': msg, 'api_data': {}, 'api_action': _api_action.upper(), 'api_name': _api_name}
        log_process_finish(_api_msgID, api_result, **_process_call_area)    
        return api_result

    #get the subscription id
    bank_subscriptionID = create_result.get('data', {}).get('subscriptionId')

    if not bank_subscriptionID:
        msg = f"subscription_id not created.(status:{create_result.get('message','?')})"
        api_result = {'api_status': 'error', 'api_message': msg, 'api_data': {}, 'api_action': _api_action.upper(), 'api_name': _api_name}
        log_process_finish(_api_msgID, api_result, **_process_call_area)    
        return api_result
  
    msg=f'ok. subscription obtained from bank [{bank_code}]'
    api_data = {'bank_subscriptionID': bank_subscriptionID, 'client_id': client_id, 'bank_code': bank_code, 'bank_id': bank_id,'application_name':application_name}
    api_result = {'api_status': 'success', 'api_message': msg, 'api_data':api_data,'bank_subscriptionID': bank_subscriptionID, 'bank_code': bank_code, 'bank_id': bank_id,}
    log_process_finish(_api_msgID, api_result, **_process_call_area)    
    return api_result
#::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
def banksubscription_request_authorization_from_client(dbsession, client_id, bank_id, subscription_id, application_name, caller_area={}):
    _api_name = "banksubscription_request_authorization_from_client"
    _api_entity = 'AUTHORIZATION'
    _api_action = 'request'
    _api_msgID = set_msgID(_api_name, _api_action, _api_entity)

    _process_identity_kwargs = {'type': 'api', 'module': module_id, 'name': _api_name, 'action': _api_action, 'entity': _api_entity, 'msgID': _api_msgID,}
    _process_adapters_kwargs = {'dbsession': dbsession}
    _process_log_kwargs = {'indent_method': 'AUTO', 'indent_level':None}
    _process_debug_level = get_debug_level(caller_area.get('debug_level'), **_process_identity_kwargs, **_process_adapters_kwargs)
    _process_debug_files = get_debug_files(_process_debug_level, **_process_identity_kwargs, **_process_adapters_kwargs)
    _process_debug_kwargs={'debug_level':_process_debug_level,'debug_files':_process_debug_files}

    _process_signature = build_process_signature(**_process_identity_kwargs, **_process_adapters_kwargs, **_process_debug_kwargs, **_process_log_kwargs)
    _process_call_area = build_process_call_area(_process_signature, caller_area)

    log_process_start(_api_msgID,**_process_call_area)

    log_process_input('', 'client_id', client_id, **_process_call_area)
    log_process_input('', 'bank_id', bank_id, **_process_call_area)
    log_process_input('', 'subscription_id', subscription_id, **_process_call_area)
    log_process_input('', 'application_name', application_name, **_process_call_area)
    log_process_input('', 'caller_area', caller_area, **_process_call_area)

    application = dbsession.get(dbmodel.APPLICATION, {'application_name': application_name}, caller_area=_process_call_area)
    if not application:
        msg = f'application not found'
        api_result = {'api_status': 'error', 'api_message': msg, 'api_data': {}, 'api_action': _api_action.upper(), 'api_name': _api_name}
        log_process_finish(_api_msgID, api_result, **_process_call_area)    
        return api_result

    client = dbsession.get(dbmodel.CLIENT, {'client_id': client_id}, caller_area=_process_call_area)
    if not client:
        msg = f'client not found'
        api_result = {'api_status': 'error', 'api_message': msg, 'api_data': {}, 'api_action': _api_action.upper(), 'api_name': _api_name}
        log_process_finish(_api_msgID, api_result, **_process_call_area)    
        return api_result
    if not client.status=='Active':
        msg = f"client not Active.(status:{client.status})"
        api_result = {'api_status': 'error', 'api_message': msg, 'api_data': {}, 'api_action': _api_action.upper(), 'api_name': _api_name}
        log_process_finish(_api_msgID, api_result, **_process_call_area)    
        return api_result

    bank = dbsession.get(dbmodel.BANK, {'bank_id': bank_id}, caller_area=_process_call_area)
    if not bank:
        bank = dbsession.get(dbmodel.BANK, {'bank_code': bank_id}, caller_area=_process_call_area)
        if not bank:
            bank = dbsession.get(dbmodel.BANK, {'bank_BIC': bank_id}, caller_area=_process_call_area)
    if not bank:
        msg = f'bank not found'
        api_result = {'api_status': 'error', 'api_message': msg, 'api_data': {}, 'api_action': _api_action.upper(), 'api_name': _api_name}
        log_process_finish(_api_msgID, api_result, **_process_call_area)    
        return api_result
    if not bank.status=='Active':
        msg = f"bank not Active.(status:{bank.status})"
        api_result = {'api_status': 'error', 'api_message': msg, 'api_data': {}, 'api_action': _api_action.upper(), 'api_name': _api_name}
        log_process_finish(_api_msgID, api_result, **_process_call_area)    
        return api_result
        
    application_id = application.application_id
    client_id = client.client_id
    client_email=client.email
    client_type=client.client_type
    bank_code = bank.bank_code
    bank_id = bank.bank_id

    res = bankingAPI.authorize_subscription(bank_code, subscription_id)
    if not res:
        msg='authorization request FAILED'
        api_result = {'api_status': 'error', 'api_message': msg, 'api_data': {}, 'api_action': _api_action.upper(), 'api_name': _api_name}
        log_process_finish(_api_msgID, api_result, **_process_call_area)    
        return api_result
    
    subscription_authorization_request={
        'bank_subscriptionID': subscription_id,
        'application_name': application_name,
        'application_id': application_id,
        'client_id': client_id,
        'client_type': client_type,
        'client_name': client_email,
        'bank_code': bank_code,
        'status':'Pending',
        }

    bank_authorization = dbsession.insert(dbmodel.BANK_AUTHORIZATION, subscription_authorization_request, auto_commit=True, caller_area=_process_call_area)

    if not bank_authorization:
        msg = f'bank_authorization insert failed'
        api_result = {'api_status': 'error', 'api_message': msg, 'api_action': _api_action.upper(), 'api_name': _api_name}
        log_process_finish(_api_msgID, api_result, **_process_call_area)
        return api_result

    bank_authorization_id = bank_authorization.bank_authorization_id
    if not bank_authorization_id:
        msg='authorization request FAILED. (insert request system error)'
        api_result = {'api_status': 'error', 'api_message': msg, 'api_action': _api_action.upper(), 'api_name': _api_name}
        log_process_finish(_api_msgID, api_result, **_process_call_area)
        return api_result

    bank_authorization_record = bank_authorization.to_dict()

    msg=f'authorization requested from client. request:{bank_authorization_id}'
    api_result = {'api_status': 'success', 'api_message': msg, 'api_data': bank_authorization_record, 'bank_authorization_id': bank_authorization_id, 'api_action': _api_action.upper(), 'api_name': _api_name}
    log_process_finish(_api_msgID, api_result, **_process_call_area)

    return api_result
#::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
def merchant_banksubscription_register(dbsession, merchant_id, application_name, bank_id, subscription_options={},caller_area={}):
    _api_name = "merchant_banksubscription_register"
    _api_entity = 'BANK_SUBSCRIPTION'
    _api_action = 'register'
    _api_msgID = set_msgID(_api_name, _api_action, _api_entity)

    _process_identity_kwargs = {'type': 'api', 'module': module_id, 'name': _api_name, 'action': _api_action, 'entity': _api_entity, 'msgID': _api_msgID,}
    _process_adapters_kwargs = {'dbsession': dbsession}
    _process_log_kwargs = {'indent_method': 'AUTO', 'indent_level':None}
    _process_debug_level = get_debug_level(caller_area.get('debug_level'), **_process_identity_kwargs, **_process_adapters_kwargs)
    _process_debug_files = get_debug_files(_process_debug_level, **_process_identity_kwargs, **_process_adapters_kwargs)
    _process_debug_kwargs={'debug_level':_process_debug_level,'debug_files':_process_debug_files}

    _process_signature = build_process_signature(**_process_identity_kwargs, **_process_adapters_kwargs, **_process_debug_kwargs, **_process_log_kwargs)
    _process_call_area = build_process_call_area(_process_signature, caller_area)

    log_process_start(_api_msgID,**_process_call_area)

    log_process_input('', 'merchant_id', merchant_id,**_process_call_area)
    log_process_input('', 'bank_id', bank_id,**_process_call_area)
    log_process_input('', 'application_name', application_name,**_process_call_area)
    log_process_input('', 'subscription_options', subscription_options,**_process_call_area)
    log_process_input('', 'caller_area', caller_area,**_process_call_area)

    merchant = dbsession.get(db.MERCHANT, {'merchant_id':merchant_id}, caller_area=_process_call_area)
    client_id = merchant.client_id
    if not client_id:
        msg = f'merchant {merchant_id} not found'
        reply = {'api_status': 'error', 'api_message': msg}
        return reply
    if not merchant.status=='Active':
        msg = f'merchant not active. (status={merchant.status})'
        reply = {'api_status': 'error', 'api_message': msg}
        return reply
    client = dbsession.get(db.CLIENT, {'client_id':client_id}, caller_area=_process_call_area)
    if not client.status=='Active':
        msg = f'client not active. (status={client.status})'
        reply = {'api_status': 'error', 'api_message': msg}
        return reply

    # application = dbsession.get(db.APPLICATION,  {'application_name': application_name}, caller_area=_process_call_area)
    # if not application:
    #     msg = f'application not found'
    #     log_process_message('', 'error', msg, **_process_call_area)
    #     api_result = {'api_status': 'error', 'api_message': msg, 'api_action': _api_action.upper(), 'api_name': _api_name}
    #     log_process_finish(_api_msgID, api_result, **_process_call_area)
    #     return api_result
    # if not application.status == 'Active':
    #     msg = f"application not Active.(status:{application.status})"
    #     log_process_message('', 'error', msg, **_process_call_area)
    #     api_result = {'api_status': 'error', 'api_message': msg, 'api_action': _api_action.upper(), 'api_name': _api_name}
    #     log_process_finish(_api_msgID, api_result, **_process_call_area)
    #     return api_result

    # app_user_spec = {'application_name': application_name,'client_id':client_id,'user_role':None}
    # application_user = dbsession.get(db.APPLICATION_USER, app_user_spec, caller_area=_process_call_area)
    # if not application_user:
    #     msg = f'merchant [{merchant.name}] not subscribed for application [{application_name}]'
    #     log_process_message('', 'error', msg, **_process_call_area)
    #     api_result = {'api_status': 'error', 'api_message': msg, 'api_action': _api_action.upper(), 'api_name': _api_name}
    #     log_process_finish(_api_msgID, api_result, **_process_call_area)
    #     return api_result
    # if not application_user.status == 'Active':
    #     msg = f'merchant [{merchant.name}] subscription for application [{application_name}] is not active (status={application_user.status})'
    #     log_process_message('', 'error', msg, **_process_call_area)
    #     api_result = {'api_status': 'error', 'api_message': msg, 'api_action': _api_action.upper(), 'api_name': _api_name}
    #     log_process_finish(_api_msgID, api_result, **_process_call_area)
    #     return api_result

    # subscription_options = request.json
    allow_transactionHistory = subscription_options.get('allow_transactionHistory', False)
    allow_balance = subscription_options.get('allow_balance', False)
    allow_details = subscription_options.get('allow_details', False)
    allow_checkFundsAvailability = subscription_options.get('allow_checkFundsAvailability', False)
    payments_limit = subscription_options.get('payments_limit', 100)
    payments_currency = subscription_options.get('payments_currency', 'EUR')
    payments_amount = subscription_options.get('payments_amount', 10)

    log_process_data('', 'allow_transactionHistory', allow_transactionHistory,**_process_call_area)
    log_process_data('', 'allow_balance', allow_balance,**_process_call_area)
    log_process_data('', 'allow_details', allow_details,**_process_call_area)
    log_process_data('', 'allow_checkFundsAvailability', allow_checkFundsAvailability,**_process_call_area)
    log_process_data('', 'payments_limit', payments_limit,**_process_call_area)
    log_process_data('', 'payments_currency', payments_currency,**_process_call_area)
    log_process_data('', 'payments_amount', payments_amount,**_process_call_area)
    
    action_result = banksubscription_register(dbsession, 
        client_id=client_id, bank_id=bank_id, application_name=application_name,
        allow_transactionHistory=allow_transactionHistory, allow_balance=allow_balance,
        allow_details=allow_details, allow_checkFundsAvailability=allow_checkFundsAvailability,
        payments_limit=payments_limit, payments_currency=payments_currency, payments_amount=payments_amount
        )
    api_result = action_result
    msg = api_result.get('api_message', '?')
    msg = msg.replace('client', 'merchant')
    api_result.update({'api_action': _api_action, 'api_name': _api_name, 'api_message': msg})
    
    log_process_finish(_api_msgID, api_result, **_process_call_area)    
    return api_result
#::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
def client_banksubscription_register(dbsession, client_id, application_name, bank_id, subscription_options={},caller_area={}):
    _api_name = "client_banksubscription_register"
    _api_entity = 'BANK_SUBSCRIPTION'
    _api_action = 'register'
    _api_msgID = set_msgID(_api_name, _api_action, _api_entity)

    _process_identity_kwargs = {'type': 'api', 'module': module_id, 'name': _api_name, 'action': _api_action, 'entity': _api_entity, 'msgID': _api_msgID,}
    _process_adapters_kwargs = {'dbsession': dbsession}
    _process_log_kwargs = {'indent_method': 'AUTO', 'indent_level':None}
    _process_debug_level = get_debug_level(caller_area.get('debug_level'), **_process_identity_kwargs, **_process_adapters_kwargs)
    _process_debug_files = get_debug_files(_process_debug_level, **_process_identity_kwargs, **_process_adapters_kwargs)
    _process_debug_kwargs={'debug_level':_process_debug_level,'debug_files':_process_debug_files}

    _process_signature = build_process_signature(**_process_identity_kwargs, **_process_adapters_kwargs, **_process_debug_kwargs, **_process_log_kwargs)
    _process_call_area = build_process_call_area(_process_signature, caller_area)

    log_process_start(_api_msgID,**_process_call_area)

    log_process_input('', 'client_id', client_id,**_process_call_area)
    log_process_input('', 'bank_id', bank_id,**_process_call_area)
    log_process_input('', 'application_name', application_name,**_process_call_area)
    log_process_input('', 'subscription_options', subscription_options,**_process_call_area)
    log_process_input('', 'caller_area', caller_area,**_process_call_area)

    client = dbsession.get(db.CLIENT, {'client_id':client_id}, caller_area=_process_call_area)
    if not client.status=='Active':
        msg = f'client not active. (status={client.status})'
        reply = {'api_status': 'error', 'api_message': msg}
        return reply

    application = dbsession.get(db.APPLICATION,  {'application_name': application_name}, caller_area=_process_call_area)
    if not application:
        msg = f'application not found'
        log_process_message('', 'error', msg, **_process_call_area)
        api_result = {'api_status': 'error', 'api_message': msg, 'api_action': _api_action.upper(), 'api_name': _api_name}
        log_process_finish(_api_msgID, api_result, **_process_call_area)
        return api_result
    if not application.status == 'Active':
        msg = f"application not Active.(status:{application.status})"
        log_process_message('', 'error', msg, **_process_call_area)
        api_result = {'api_status': 'error', 'api_message': msg, 'api_action': _api_action.upper(), 'api_name': _api_name}
        log_process_finish(_api_msgID, api_result, **_process_call_area)
        return api_result

    app_user_spec = {'application_name': application_name,'client_id':client_id,'user_role':None}
    application_user = dbsession.get(db.APPLICATION_USER, app_user_spec, caller_area=_process_call_area)
    if not application_user:
        msg = f'client [{client.email}] not subscribed for application [{application_name}]'
        log_process_message('', 'error', msg, **_process_call_area)
        api_result = {'api_status': 'error', 'api_message': msg, 'api_action': _api_action.upper(), 'api_name': _api_name}
        log_process_finish(_api_msgID, api_result, **_process_call_area)
        return api_result
    if not application_user.status == 'Active':
        msg = f'client [{client.name}] subscription for application [{application_name}] is not active (status={application_user.status})'
        log_process_message('', 'error', msg, **_process_call_area)
        api_result = {'api_status': 'error', 'api_message': msg, 'api_action': _api_action.upper(), 'api_name': _api_name}
        log_process_finish(_api_msgID, api_result, **_process_call_area)
        return api_result

    allow_transactionHistory = subscription_options.get('allow_transactionHistory', True)
    allow_balance = subscription_options.get('allow_balance', True)
    allow_details = subscription_options.get('allow_details', True)
    allow_checkFundsAvailability = subscription_options.get('allow_checkFundsAvailability', True)
    payments_limit = subscription_options.get('payments_limit', 100)
    payments_currency = subscription_options.get('payments_currency', 'EUR')
    payments_amount = subscription_options.get('payments_amount', 10)

    log_process_data('', 'allow_transactionHistory', allow_transactionHistory,**_process_call_area)
    log_process_data('', 'allow_balance', allow_balance,**_process_call_area)
    log_process_data('', 'allow_details', allow_details,**_process_call_area)
    log_process_data('', 'allow_checkFundsAvailability', allow_checkFundsAvailability,**_process_call_area)
    log_process_data('', 'payments_limit', payments_limit,**_process_call_area)
    log_process_data('', 'payments_currency', payments_currency,**_process_call_area)
    log_process_data('', 'payments_amount', payments_amount,**_process_call_area)
        
    action_result = banksubscription_register(dbsession, 
        client_id=client_id, bank_id=bank_id, application_name=application_name,
        allow_transactionHistory=allow_transactionHistory, allow_balance=allow_balance,
        allow_details=allow_details, allow_checkFundsAvailability=allow_checkFundsAvailability,
        payments_limit=payments_limit, payments_currency=payments_currency, payments_amount=payments_amount
        )
    api_result = action_result
    api_result.update({'api_action': _api_action, 'api_name': _api_name})
    
    log_process_finish(_api_msgID, api_result, **_process_call_area)    
    return api_result
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
master_configuration = add_apis_to_configuration('openbanking_apis', master_configuration, thisModuleObj, functions_ids, exclude_functions_ids)
save_module_configuration(module_identityDictionary, master_configuration, print_enabled=consolelog_enabled, filelog_enabled=filelog_enabled)
thisApp.pair_module_configuration('openbanking_apis',master_configuration)
#::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
if get_module_debug_level(module_id) > 0:
    apis = thisApp.application_configuration.get('openbanking_apis', {})
    for api_name in apis.keys():
        api_entry = apis.get(api_name)
        msg=f'module [[{module_id}]] openbanking api [{api_name} [[[{api_entry}]]]'
        log_message(msg)
#::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
msg = f'database [ganimides] [[[[module [{module_id}] loaded]]]] with [[version {module_version}]]'
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