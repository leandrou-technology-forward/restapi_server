import os
import sys
if not (os.path.dirname(os.path.dirname(__file__)) in sys.path): sys.path.append(os.path.dirname(os.path.dirname(__file__)))
if not (os.path.dirname(__file__) in sys.path): sys.path.append(os.path.dirname(__file__))

import datetime
import decimal

# #
from _onlineApp import thisApp
from _onlineApp import get_debug_option_as_level, get_debug_files, log_message, retrieve_module_configuration, get_globals_from_configuration, save_module_configuration,get_module_debug_level
from _onlineApp import log_process_start, log_process_finish, log_process_message, log_process_result,log_process_data, log_process_input, log_process_output
from _onlineApp import set_process_identity_dict, set_process_caller_area, add_apis_to_configuration
from _onlineApp import build_process_signature, build_process_call_area, get_debug_level, get_debug_files

import ganimides_database as db
import ganimides_openBankingAPI as bankingapi
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
# mix apis
#::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
#::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
#::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
def xmerchant_banksubscription_register(dbsession, merchant_id, application_name, bank_id, subscription_options={},caller_area={}):
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
        msg = f'merchant [{merchant.name}] not subscribed for application [{application_name}]'
        log_process_message('', 'error', msg, **_process_call_area)
        api_result = {'api_status': 'error', 'api_message': msg, 'api_action': _api_action.upper(), 'api_name': _api_name}
        log_process_finish(_api_msgID, api_result, **_process_call_area)
        return api_result
    if not application_user.status == 'Active':
        msg = f'merchant [{merchant.name}] subscription for application [{application_name}] is not active (status={application_user.status})'
        log_process_message('', 'error', msg, **_process_call_area)
        api_result = {'api_status': 'error', 'api_message': msg, 'api_action': _api_action.upper(), 'api_name': _api_name}
        log_process_finish(_api_msgID, api_result, **_process_call_area)
        return api_result

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
    
    action_result = bankingapi.banksubscription_register(dbsession, 
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
def xclient_banksubscription_register(dbsession, client_id, application_name, bank_id, subscription_options={},caller_area={}):
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
        
    action_result = bankingapi.banksubscription_register(dbsession, 
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
def set_msgID(api_name,api_action,api_entity):
    msgid=f"#C0#api #C9#{api_name}#C0# [{api_entity}]#C0# action [[{api_action.upper()}]]#C0#"
    return msgid
#::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
def geoloc_to_integer(geoloc):
    try:
        d = decimal.Decimal(str(geoloc).replace(",", ".").strip())
    except:
        d = 0
    i = int(d * 1000000000)
    return i
#::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
def integer_to_geoloc(i):
    try:
        d = decimal.Decimal(str(i))
    except:
        d = 0
    geoloc = d / 1000000000
    return geoloc
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
functions_ids=['dbapi_']
exclude_functions_ids = ['set_msgID', 'set_process_debug_level']
thisModuleObj = sys.modules[__name__]
master_configuration.update({'mix_apis':[]})
master_configuration = add_apis_to_configuration('mix_apis', master_configuration, thisModuleObj, functions_ids, exclude_functions_ids)
save_module_configuration(module_identityDictionary, master_configuration, print_enabled=consolelog_enabled, filelog_enabled=filelog_enabled)
thisApp.pair_module_configuration('mix_apis',master_configuration)
#::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
save_module_configuration(module_identityDictionary, master_configuration, print_enabled=consolelog_enabled, filelog_enabled=filelog_enabled)
#::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
if get_module_debug_level(module_id) > 0:
    apis = thisApp.application_configuration.get('database_apis', {})
    for api_name in apis.keys():
        api_entry = apis.get(api_name)
        msg=f'module [[{module_id}]] database api [{api_name} [[[{api_entry}]]]'
        log_message(msg)
#::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
#import commands
apis = thisApp.application_configuration.get('database_apis', {})
for api_name in apis.keys():
    api_entry = apis.get(api_name)
    msg=f'from {module_id} import {api_name}'
    log_message(msg)
#::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
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
    # caller_area={'aaaa': '11111'}
    # print('0caller_area=', caller_area)
    # test_api(caller_area, call_level=-1)
    # print('4caller_area=', caller_area)
#::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
#::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
#::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
