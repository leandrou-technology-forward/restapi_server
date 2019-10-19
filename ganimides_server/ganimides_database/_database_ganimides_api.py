# -*- coding: utf-8 -*-
#https://www.pythoncentral.io/series/python-sqlalchemy-database-tutorial/
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

import _database_ganimides_model as dbmodel
#import ganimides_openBankingAPI as bankingapi
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
def dbapi_device(dbsession, action, input_dict, action_filter={}, caller_area={}):
    _api_name = "dbapi_device"
    _api_entity = 'DEVICE'
    _api_action = action
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

    if action.upper in ('REGISTER','UNREGISTER'):
        return dbapi_device_register_unregister(dbsession, action, input_dict, action_filter, caller_area=_process_call_area)
    log_process_input('', 'input_dict', input_dict,**_process_call_area)
    log_process_input('', 'action_filter', action_filter,**_process_call_area)
    log_process_input('', 'caller_area', caller_area,**_process_call_area)
    
    
    action_result = dbsession.table_action(dbmodel.DEVICE, action, input_dict, action_filter, auto_commit=True, caller_area=_process_call_area)
    api_result = action_result
    api_result.update({'api_action': _api_action, 'api_name': _api_name})
        
    log_process_finish(_api_msgID, api_result, **_process_call_area)    
    return api_result
#::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
def dbapi_device_register_unregister(dbsession, action, input_dict, action_filter={}, caller_area={}):
    _api_name="dbapi_device_register_unregister"
    _api_entity = 'DEVICE'
    _api_action = action
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

    log_process_input('', 'input_dict', input_dict,**_process_call_area)
    log_process_input('', 'action_filter', action_filter,**_process_call_area)
    log_process_input('', 'caller_area', caller_area,**_process_call_area)

    actions_supported=('REGISTER', 'UNREGISTER')

    now = datetime.datetime.utcnow()

    if action.upper() not in actions_supported:
        msg = f"action '{action}' not supported. {actions_supported}"
        api_result = {'api_status': 'error', 'api_message': msg, 'api_data': actions_supported, 'api_action': _api_action.upper(), 'api_name': _api_name}
        log_process_finish(_api_msgID, api_result, **_process_call_area)    
        return api_result
    
    device = dbsession.get(dbmodel.DEVICE, input_dict, caller_area=_process_call_area)
    if not device:
        device_record = device.valid_fields_dictionary(input_dict)
        msg = f"invalid device"
        api_result = {'api_status': 'error', 'api_message': msg, 'api_data': device_record, 'api_action': _api_action.upper(), 'api_name': _api_name}
        log_process_finish(_api_msgID, api_result, **_process_call_area)    
        return api_result

    client = dbsession.get(dbmodel.CLIENT, input_dict, caller_area=_process_call_area)
    if not client:
        client_record = client.valid_fields_dictionary(input_dict)
        msg = f"invalid client"
        api_result = {'api_status': 'error', 'api_message': msg, 'api_data': client_record, 'api_action': _api_action.upper(), 'api_name': _api_name}
        log_process_finish(_api_msgID, api_result, **_process_call_area)    
        return api_result

    client_id = client.client_id

    if action.upper() in ('REGISTER'):
        status = 'Registered'
        xx = 'for'
    else:
        status = 'UnRegistered'
        xx = 'from'

    registered_apps=[]
    if input_dict.get('applications', '').upper() in ('*', 'ALL') \
        or input_dict.get('application', '').upper() in ('*', 'ALL') \
        or input_dict.get('application_name', '').upper() in ('*', 'ALL'):
        
        CLIENT_DEVICE = dbmodel.CLIENT_DEVICE
        client_devices = dbsession.query(CLIENT_DEVICE).filter(CLIENT_DEVICE.device_uid == device.device_uid, CLIENT_DEVICE.client_id == client_id, CLIENT_DEVICE.status != status).all()
        if len(client_devices) <= 0:
            client_devices = dbsession.query(CLIENT_DEVICE).filter(CLIENT_DEVICE.device_uid == device.device_uid, CLIENT_DEVICE.client_id == client_id).all()
            client_device_records = dbsession.rows_to_dict(CLIENT_DEVICE, client_devices)
            msg = f"device already {status.upper()} {xx} usage by all applications"
            api_result = {'api_status': 'success', 'api_message': msg, 'api_data': client_device_records, 'api_action': _api_action.upper(), 'api_name': _api_name}
            log_process_finish(_api_msgID, api_result, **_process_call_area)    
            return api_result
     
        for client_device in client_devices:
            client_device.status = status
            application = dbsession.get(dbmodel.APPLICATION, {'application_name': client_device.application_name}, caller_area=_process_call_area)
            registered_apps.append(application.application_name)

        dbsession.commit(**_process_call_area)
        client_device_records = dbsession.rows_to_dict(CLIENT_DEVICE, client_devices)
    else:
        application = dbsession.get(dbmodel.APPLICATION, input_dict, caller_area=_process_call_area)
        if not application:
            application_record = application.valid_fields_dictionary(input_dict)
            msg = f"invalid application"
            api_result = {'api_status': 'error', 'api_message': msg, 'api_data': application_record, 'api_action': _api_action.upper(), 'api_name': _api_name}
            log_process_finish(_api_msgID, api_result, **_process_call_area)    
            return api_result

        client_device_record = {'device_uid': device.device_uid, 'client_id': client_id, 'application_name': application.application_name, 'last_usage_timestamp': now, 'status': status}
        client_device = dbsession.get(dbmodel.CLIENT_DEVICE, client_device_record, caller_area=_process_call_area)
        if client_device:
            if client_device.status == status:
                msg = f"device already {client_device.status.upper()} {xx} usage by application '{client_device.application_name}'"
                client_device_records = [client_device.to_dict()]
                api_result = {'api_status': 'success', 'api_message': msg, 'api_data': client_device_records, 'api_action': _api_action.upper(), 'api_name': _api_name}
                log_process_finish(_api_msgID, api_result, **_process_call_area)    
                return api_result

        client_device = dbsession.refresh(dbmodel.CLIENT_DEVICE, client_device_record, auto_commit=True, caller_area=_process_call_area)
        registered_apps.append(application.application_name)
        client_device_records = [client_device.to_dict()]

    row_count = len(client_device_records)
    x=''
    if row_count > 1:
        x = 's'
        
    msg = f"device {status.upper()} {xx} usage by application{x} {registered_apps}"
    api_result = {'api_status': 'success', 'api_message': msg, 'api_data': client_device_records, 'api_data_rows': row_count, 'api_action': _api_action.upper(), 'api_name':_api_name }
    log_process_finish(_api_msgID, api_result, **_process_call_area)    
    return api_result
#::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
def dbapi_device_usage(dbsession, action, input_dict, action_filter={}, caller_area={}):
    _api_name = "dbapi_device_usage"
    _api_entity = 'DEVICE'
    _api_action = action
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

    log_process_input('', 'input_dict', input_dict,**_process_call_area)
    log_process_input('', 'action_filter', action_filter,**_process_call_area)
    log_process_input('', 'caller_area', caller_area,**_process_call_area)

    action_result = dbsession.table_action(dbmodel.DEVICE_USAGE, action, input_dict, action_filter, auto_commit=True, caller_area=_process_call_area)
    api_result = action_result
    api_result.update({'api_action': _api_action, 'api_name': _api_name})
    
    log_process_finish(_api_msgID, api_result, **_process_call_area)    
    return api_result
#::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
def dbapi_client(dbsession, action, input_dict, action_filter={}, caller_area={}):
    _api_name = "dbapi_cient"
    _api_entity = 'CLIENT'
    _api_action = action
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

    log_process_input('', 'input_dict', input_dict,**_process_call_area)
    log_process_input('', 'action_filter', action_filter,**_process_call_area)
    log_process_input('', 'caller_area', caller_area, **_process_call_area)
    
    if action.upper().replace('_', '-') in ('SEND-CONFIRMATION-EMAIL', 'SEND-CONFIRMATION-SMS'):
        client = dbsession.get(dbmodel.CLIENT, action_filter, caller_area=_process_call_area)
        if not client:
            msg = f'client not found'
            api_result = {'api_status': 'error', 'api_message': msg, 'api_data': input_dict}
            log_process_finish(_api_msgID, api_result, **_process_call_area)    
            return api_result
        
        client_dict=client.to_dict()

        if client.confirmed and client.status=='Active':
            msg = f'client {client.email} already confirmed'
            api_result = {'api_status': 'success', 'api_message': msg, 'api_data': client_dict}
            log_process_finish(_api_msgID, api_result, **_process_call_area)    
            return api_result

        if action.upper().replace('_', '-') in ('SEND-CONFIRMATION-EMAIL'):
            if not client.email:
                msg = f'email is missing'
                api_result = {'api_status': 'error', 'api_message': msg, 'api_data': client_dict}
                log_process_finish(_api_msgID, api_result, **_process_call_area)    
                return api_result
            
            #ok = send_confirmation_email(client.email)
            ok=True
            if ok:
                confirm_filter = {'email': client.email, 'mobile': ''}
                confirmation = dbsession.get(dbmodel.CLIENT_CONFIRMATION, confirm_filter, caller_area=_process_call_area)
                if not confirmation:
                    confirm_dict = {'email': client.email, 'mobile': '', 'status': 'Sent'}
                    xapi_result = dbsession.table_action(dbmodel.CLIENT_CONFIRMATION, 'refresh' , confirm_dict, {}, auto_commit=True, caller_area=_process_call_area)
                if not confirmation.status=='Confirmed':
                    confirm_dict = {'email': client.email, 'mobile': '', 'status': 'Sent', 'send_timestamp': datetime.datetime.utcnow()}
                    xapi_result = dbsession.table_action(dbmodel.CLIENT_CONFIRMATION, 'refresh' , confirm_dict, {}, auto_commit=True, caller_area=_process_call_area)

                msg = f'OK. a confirmation email sent to {client.email}'
                api_result = {'api_status': 'success', 'api_message': msg, 'api_data': client_dict}
                api_result.update({'api_action': _api_action, 'api_name': _api_name})
                log_process_finish(_api_msgID, api_result, **_process_call_area)    
                return api_result
            else:
                msg = f'FAILED to send confirmation email to {client.email}. retry'
                api_result = {'api_status': 'error', 'api_message': msg, 'api_data': client_dict}
                api_result.update({'api_action': _api_action, 'api_name': _api_name})
                log_process_finish(_api_msgID, api_result, **_process_call_area)    
                return api_result

        if action.upper().replace('_', '-') in ('SEND-CONFIRMATION-SMS'):
            if not client.mobile:
                msg = f'mobile has not been defined'
                api_result = {'api_status': 'error', 'api_message': msg, 'api_data': client_dict}
                log_process_finish(_api_msgID, api_result, **_process_call_area)    
                return api_result

            #ok = send_confirmation_sms(client.mobile)
            ok=True
            if ok:
                confirm_filter = {'mobile': client.mobile, 'email': ''}
                confirmation = dbsession.get(dbmodel.CLIENT_CONFIRMATION, confirm_filter, caller_area=_process_call_area)
                if not confirmation:
                    confirm_dict = {'mobile': client.mobile, 'email': '', 'status': 'Sent'}
                    xapi_result = dbsession.table_action(dbmodel.CLIENT_CONFIRMATION, 'refresh' , confirm_dict, {}, auto_commit=True, caller_area=_process_call_area)
                if not confirmation.status=='Confirmed':
                    confirm_dict = {'mobile': client.mobile, 'email': '', 'status': 'Sent', 'send_timestamp': datetime.datetime.utcnow()}
                    xapi_result = dbsession.table_action(dbmodel.CLIENT_CONFIRMATION, 'refresh' , confirm_dict, {}, auto_commit=True, caller_area=_process_call_area)

                msg = f'OK. a confirmation sms sent to {client.mobile}'
                api_result = {'api_status': 'success', 'api_message': msg, 'api_data': client_dict}
                api_result.update({'api_action': _api_action, 'api_name': _api_name})
                log_process_finish(_api_msgID, api_result, **_process_call_area)    
                return api_result
            else:
                msg = f'FAILED to send confirmation sms to {client.mobile}. retry'
                api_result = {'api_status': 'error', 'api_message': msg, 'api_data': client_dict}
                api_result.update({'api_action': _api_action, 'api_name': _api_name})
                log_process_finish(_api_msgID, api_result, **_process_call_area)    
                return api_result

    api_result = dbsession.table_action(dbmodel.CLIENT, action , input_dict, action_filter, auto_commit=True, caller_area=_process_call_area)
    if not api_result.get('api_status') == 'success':
        log_process_finish(_api_msgID, api_result, **_process_call_area)    
        return api_result

    if action.upper() in ('UPDATE', 'REFRESH', 'REGISTER', 'ACTIVATE', 'DEACTIVATE', 'CONFIRM'):
        client_dict = api_result.get('api_data', {})
        client_id = client_dict.get('client_id')
        client_type = client_dict.get('client_type')
        update_dict = {
            #'client_id': client_dict.get('client_id'),
            'status': client_dict.get('status'),
            'email': client_dict.get('email'),
            'confirmed': client_dict.get('confirmed'),
            'client_status': client_dict.get('status'),
            'client_email': client_dict.get('email'),
            'client_mobile': client_dict.get('mobile'),
            'client_name': client_dict.get('name'),
            'client_confirmed': client_dict.get('confirmed'),
            'confirmed_timestamp': client_dict.get('confirmed_timestamp'),
                }
        xaction = 'update_rows'
        action_filter = {'client_id': client_id}
        if client_id and client_type:
            if client_type == 'merchant':
                xapi_result = dbsession.table_action(dbmodel.MERCHANT, xaction , update_dict, action_filter, auto_commit=True, caller_area=_process_call_area)
            elif client_type == 'subscriber':
                xapi_result = dbsession.table_action(dbmodel.SUBSCRIPTION, xaction , update_dict, action_filter, auto_commit=True, caller_area=_process_call_area)
            elif client_type == 'customer_service_assistant':
                xapi_result = dbsession.table_action(dbmodel.CUSTOMER_SERVICE_ASSISTANT, xaction , update_dict, action_filter, auto_commit=True, caller_area=_process_call_area)

        xapi_result = dbsession.table_action(dbmodel.APPLICATION_USER, xaction , update_dict, action_filter, auto_commit=True, caller_area=_process_call_area)

    # if action.upper() in ('CONFIRM'):
    #     if input_dict.get('mobile_confirmation_sms'):
    #         # client_dict = api_result.get('api_data', {})
    #         mobile=client_dict.get('mobile')
    #         confirm_filter = {'mobile': mobile, 'email': ''}
    #         confirmation = dbsession.get(dbmodel.CLIENT_CONFIRMATION, confirm_filter, caller_area=_process_call_area)
    #         if not confirmation:
    #             confirm_dict = {'mobile': mobile, 'email': '', 'status': 'Confirmed', 'confirmed_timestamp': datetime.datetime.utcnow(),'confirmed':1}
    #             xapi_result = dbsession.table_action(dbmodel.CLIENT_CONFIRMATION, 'refresh' , confirm_dict, {}, auto_commit=True, caller_area=_process_call_area)
    #         if not confirmation.status=='Confirmed':
    #             confirm_dict = {'mobile': mobile, 'email': '', 'status': 'Confirmed', 'confirmed_timestamp': datetime.datetime.utcnow(),'confirmed':1}
    #             xapi_result = dbsession.table_action(dbmodel.CLIENT_CONFIRMATION, 'refresh' , confirm_dict, {}, auto_commit=True, caller_area=_process_call_area)
    #     elif input_dict.get('email_confirmation_email'):
    #         # client_dict = api_result.get('api_data', {})
    #         email=client_dict.get('email')
    #         confirm_filter = {'mobile': '', 'email': email}
    #         confirmation = dbsession.get(dbmodel.CLIENT_CONFIRMATION, confirm_filter, caller_area=_process_call_area)
    #         if not confirmation:
    #             confirm_dict = {'mobile': '', 'email': email, 'status': 'Confirmed', 'confirmed_timestamp': datetime.datetime.utcnow(),'confirmed':1}
    #             xapi_result = dbsession.table_action(dbmodel.CLIENT_CONFIRMATION, 'refresh' , confirm_dict, {}, auto_commit=True, caller_area=_process_call_area)
    #         if not confirmation.status=='Confirmed':
    #             confirm_dict = {'mobile': '', 'email': email, 'status': 'Confirmed', 'confirmed_timestamp': datetime.datetime.utcnow(),'confirmed':1}
    #             xapi_result = dbsession.table_action(dbmodel.CLIENT_CONFIRMATION, 'refresh' , confirm_dict, {}, auto_commit=True, caller_area=_process_call_area)
    #     else:
    #         # client_dict = api_result.get('api_data', {})
    #         email=client_dict.get('email')
    #         confirm_filter = {'mobile': '', 'email': email}
    #         confirmation = dbsession.get(dbmodel.CLIENT_CONFIRMATION, confirm_filter, caller_area=_process_call_area)
    #         if not confirmation:
    #             confirm_dict = {'mobile': '', 'email': email, 'status': 'Confirmed', 'confirmed_timestamp': datetime.datetime.utcnow(),'confirmed':1}
    #             xapi_result = dbsession.table_action(dbmodel.CLIENT_CONFIRMATION, 'refresh' , confirm_dict, {}, auto_commit=True, caller_area=_process_call_area)
    #         if not confirmation.status=='Confirmed':
    #             confirm_dict = {'mobile': '', 'email': email, 'status': 'Confirmed', 'confirmed_timestamp': datetime.datetime.utcnow(),'confirmed':1}
    #             xapi_result = dbsession.table_action(dbmodel.CLIENT_CONFIRMATION, 'refresh' , confirm_dict, {}, auto_commit=True, caller_area=_process_call_area)

    api_result.update({'api_action': _api_action, 'api_name': _api_name})
    log_process_finish(_api_msgID, api_result, **_process_call_area)    
    return api_result
#::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
def dbapi_client_device(dbsession, action, input_dict, action_filter={}, caller_area={}):
    _api_name = "dbapi_client_device"
    _api_entity = 'DEVICE'
    _api_action = action
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

    if action.upper in ('REGISTER','UNREGISTER'):
        return dbapi_device_register_unregister(dbsession, action, input_dict, action_filter, caller_area=_process_call_area)

    log_process_input('', 'input_dict', input_dict,**_process_call_area)
    log_process_input('', 'action_filter', action_filter,**_process_call_area)
    log_process_input('', 'caller_area', caller_area,**_process_call_area)

    action_result = dbsession.table_action(dbmodel.CLIENT_DEVICE, action, input_dict, action_filter, auto_commit=True, caller_area=_process_call_area)
    api_result = action_result
    api_result.update({'api_action': _api_action, 'api_name': _api_name})
    
    log_process_finish(_api_msgID, api_result, **_process_call_area)    
    return api_result
#::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
def dbapi_verification(dbsession, action, input_dict, action_filter={}, caller_area={}):
    _api_name = "dbapi_verification"
    _api_entity = 'VERIFICATION'
    _api_action = action
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

    log_process_input('', 'input_dict', input_dict,**_process_call_area)
    log_process_input('', 'action_filter', action_filter,**_process_call_area)
    log_process_input('', 'caller_area', caller_area,**_process_call_area)

    action_result = dbsession.table_action(dbmodel.VERIFICATION, action, input_dict, action_filter, auto_commit=True, caller_area=_process_call_area)
    api_result = action_result
    api_result.update({'api_action': _api_action, 'api_name': _api_name})
    
    log_process_finish(_api_msgID, api_result, **_process_call_area)    
    return api_result
#::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
#::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
def dbapi_email_confirmation(dbsession, input_dict, action_filter={}, caller_area={}):
    _api_name = "dbapi_email_confirmation"
    _api_entity = 'email'
    _api_action = 'confirm'
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

    log_process_input('', 'input_dict', input_dict,**_process_call_area)
    log_process_input('', 'action_filter', action_filter,**_process_call_area)
    log_process_input('', 'caller_area', caller_area,**_process_call_area)

    verification = dbsession.get(dbmodel.VERIFICATION, input_dict, caller_area=_process_call_area)
    if not verification:
        msg = f'email verification failed'
        api_result = {'api_status': 'error', 'api_message': msg}
        api_result.update({'api_action': _api_action, 'api_name': _api_name})
        log_process_finish(_api_msgID, api_result, **_process_call_area)    
        return api_result
    if not verification.status=='Confirmed':
        action_filter = {'verification_id': verification.verification_id}
        update_dict = {'status': 'Confirmed', 'verified': 1, 'verification_timestamp': datetime.datetime.utcnow()}
        action_result = dbsession.table_action(dbmodel.VERIFICATION,'update', update_dict, action_filter, auto_commit=True, caller_area=_process_call_area)
        api_result = action_result
        api_result.update({'api_action': _api_action, 'api_name': _api_name})

    client_id = verification.client_id
    client=dbsession.get(dbmodel.CLIENT, {'client_id':client_id}, caller_area=_process_call_area)
    if not client:
        msg = f'mobile verification failed (client_id not found)'
        api_result = {'api_status': 'error', 'api_message': msg}
        api_result.update({'api_action': _api_action, 'api_name': _api_name})
        log_process_finish(_api_msgID, api_result, **_process_call_area)    
        return api_result
    
    if not client.email_confirmed or not client.confirmed:
        update_record = {'client_id': client_id, 'email_confirmed': 1, 'email_confirmed_timestamp': datetime.datetime.utcnow(), 'confirmed': 1}
        dbreply = dbsession.table_action(dbmodel.CLIENT, 'update', update_record, {'client_id': client_id}, auto_commit=True, caller_area=_process_call_area)
        client_rec=client.to_dict()
        if not dbreply.get('api_status')=='success':
            msg = f'email verification failed (client update failed)'
            api_result = {'api_status': 'error', 'api_message': msg, 'api_data': client_rec}
            api_result.update({'api_action': _api_action, 'api_name': _api_name})
            log_process_finish(_api_msgID, api_result, **_process_call_area)    
            return api_result
        else:
            msg = f'OK. client email confirmed'
            api_result = {'api_status': 'success', 'api_message': msg,'api_data':client_rec}
            api_result.update({'api_action': _api_action, 'api_name': _api_name})
            log_process_finish(_api_msgID, api_result, **_process_call_area)    
            return api_result
    else:    
        client_rec=client.to_dict()
        msg = f'OK. client email already confirmed'
        api_result = {'api_status': 'success', 'api_message': msg,'api_data':client_rec}
        api_result.update({'api_action': _api_action, 'api_name': _api_name})
        log_process_finish(_api_msgID, api_result, **_process_call_area)    
        return api_result
#::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
def dbapi_mobile_confirmation(dbsession, input_dict, action_filter={}, caller_area={}):
    _api_name = "dbapi_mobile_confirmation"
    _api_entity = 'mobile'
    _api_action = 'confirm'
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

    log_process_input('', 'input_dict', input_dict,**_process_call_area)
    log_process_input('', 'action_filter', action_filter,**_process_call_area)
    log_process_input('', 'caller_area', caller_area,**_process_call_area)

    verification = dbsession.get(dbmodel.VERIFICATION, input_dict, caller_area=_process_call_area)
    if not verification:
        msg = f'mobile verification failed'
        api_result = {'api_status': 'error', 'api_message': msg}
        api_result.update({'api_action': _api_action, 'api_name': _api_name})
        log_process_finish(_api_msgID, api_result, **_process_call_area)    
        return api_result

    if not verification.status=='Confirmed':
        action_filter = {'verification_id': verification.verification_id}
        update_dict = {'status': 'Confirmed', 'verified': 1, 'verification_timestamp': datetime.datetime.utcnow()}
        action_result = dbsession.table_action(dbmodel.VERIFICATION,'update', update_dict, action_filter, auto_commit=True, caller_area=_process_call_area)
        api_result = action_result
        api_result.update({'api_action': _api_action, 'api_name': _api_name})

    client_id = verification.client_id
    client=dbsession.get(dbmodel.CLIENT, {'client_id':client_id}, caller_area=_process_call_area)
    if not client:
        msg = f'mobile verification failed (client_id not found)'
        api_result = {'api_status': 'error', 'api_message': msg}
        api_result.update({'api_action': _api_action, 'api_name': _api_name})
        log_process_finish(_api_msgID, api_result, **_process_call_area)    
        return api_result
    
    if not client.mobile_confirmed or not client.confirmed:
        update_record = {'client_id': client_id, 'mobile_confirmed': 1, 'mobile_confirmed_timestamp': datetime.datetime.utcnow(), 'confirmed': 1}
        dbreply = dbsession.table_action(dbmodel.CLIENT, 'update', update_record, {'client_id': client_id}, auto_commit=True, caller_area=_process_call_area)
        client_rec=client.to_dict()
        if not dbreply.get('api_status')=='success':
            msg = f'mobile verification failed (client update failed)'
            api_result = {'api_status': 'error', 'api_message': msg, 'api_data': client_rec}
            api_result.update({'api_action': _api_action, 'api_name': _api_name})
            log_process_finish(_api_msgID, api_result, **_process_call_area)    
            return api_result
        else:
            msg = f'OK. client mobile confirmed'
            api_result = {'api_status': 'success', 'api_message': msg,'api_data':client_rec}
            api_result.update({'api_action': _api_action, 'api_name': _api_name})
            log_process_finish(_api_msgID, api_result, **_process_call_area)    
            return api_result
    else:    
        client_rec=client.to_dict()
        msg = f'OK. client mobile already confirmed'
        api_result = {'api_status': 'success', 'api_message': msg,'api_data':client_rec}
        api_result.update({'api_action': _api_action, 'api_name': _api_name})
        log_process_finish(_api_msgID, api_result, **_process_call_area)    
        return api_result
#::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
def dbapi_api(dbsession, action, input_dict, action_filter={}, caller_area={}):
    _api_name = "dbapi_api"
    _api_entity = 'API'
    _api_action = action
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

    if action.upper() in ('REGISTER', 'UNREGISTER'):
        api_result = dbapi_api_register_unregister(dbsession, action, input_dict, action_filter, caller_area=_process_call_area)
        log_process_finish(_api_msgID, api_result, **_process_call_area)    
        return api_result    

    log_process_input('', 'input_dict', input_dict,**_process_call_area)
    log_process_input('', 'action_filter', action_filter,**_process_call_area)
    log_process_input('', 'caller_area', caller_area,**_process_call_area)

    action_result = dbsession.table_action(dbmodel.API, action, input_dict, action_filter, auto_commit=True, caller_area=_process_call_area)
    api_result = action_result
    api_result.update({'api_action': _api_action, 'api_name': _api_name})
    
    log_process_finish(_api_msgID, api_result, **_process_call_area)    
    return api_result    
#::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
def dbapi_api_register_unregister(dbsession, action, input_dict, action_filter={}, caller_area={}):
    _api_name = "dbapi_api_register_unregister"
    _api_entity = 'APPLICATION API'
    _api_action = action
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

    if action.upper() not in ('REGISTER','UNREGISTER'):
        msg = f'invalid action [[{action}]] requested. use REGISTER or UNREGISTER'
        api_result = {'api_status': 'error', 'api_message': msg, 'api_data': input_dict}
        log_process_finish(_api_msgID, api_result, **_process_call_area)    
        return api_result

    log_process_input('', 'input_dict', input_dict,**_process_call_area)
    log_process_input('', 'action_filter', action_filter,**_process_call_area)
    log_process_input('', 'caller_area', caller_area,**_process_call_area)

    if _api_action.upper() == 'REGISTER':
        api=dbsession.get(dbmodel.API, input_dict, caller_area=_process_call_area)
        if not api:
            msg = f'api not found'
            api_result = {'api_status': 'error', 'api_message': msg, 'api_data': input_dict}
            log_process_finish(_api_msgID, api_result, **_process_call_area)    
            return api_result
        if not api.status=='Active':
            msg = f'api not Active'
            api_result = {'api_status': 'error', 'api_message': msg, 'api_data': input_dict}
            log_process_finish(_api_msgID, api_result, **_process_call_area)    
            return api_result
        application=dbsession.get(dbmodel.APPLICATION, input_dict, caller_area=_process_call_area)
        if not application:
            msg = f'application not found'
            api_result = {'api_status': 'error', 'api_message': msg, 'api_data': input_dict}
            log_process_finish(_api_msgID, api_result, **_process_call_area)    
            return api_result
        if not application.status=='Active':
            msg = f'application not Active'
            api_result = {'api_status': 'error', 'api_message': msg, 'api_data': input_dict}
            log_process_finish(_api_msgID, api_result, **_process_call_area)    
            return api_result

        input_dict.update({'api_id':api.api_id})
        input_dict.update({'api_name':api.api_name})
        input_dict.update({'application_id': application.application_id})
        input_dict.update({'application_name': application.application_name})
        input_dict.update({'subscription_id': application.subscription_id})

        action_filter={}
        api_registered = dbsession.get(dbmodel.APPLICATION_API, input_dict, caller_area=_process_call_area)
        if api_registered:  
            input_dict.update({'application_api_id': api_registered.application_api_id})
            action_filter = {'application_api_id': api_registered.application_api_id}
            
        input_dict.update({'status': 'Active'})
        action='REFRESH'
        action_result = dbsession.table_action(dbmodel.APPLICATION_API, action , input_dict, action_filter, auto_commit=True, caller_area=_process_call_area)
        api_result = action_result
        api_result.update({'api_action': _api_action, 'api_name': _api_name})
        log_process_finish(_api_msgID, api_result, **_process_call_area)    
        return api_result
    elif _api_action.upper() == 'UNREGISTER':
        api=dbsession.get(dbmodel.API, input_dict, caller_area=_process_call_area)
        if api:
            input_dict.update({'api_id':api.api_id})
            input_dict.update({'api_name':api.api_name})

        application=dbsession.get(dbmodel.APPLICATION, input_dict, caller_area=_process_call_area)
        if application:
            input_dict.update({'application_id': application.application_id})
            input_dict.update({'application_name': application.application_name})

        api_registered = dbsession.get(dbmodel.APPLICATION_API, input_dict, caller_area=_process_call_area)
        if not api_registered:
            msg = f'record not found'
            api_result = {'api_status': 'error', 'api_message': msg, 'api_data': input_dict}
            log_process_finish(_api_msgID, api_result, **_process_call_area)    
            return api_result

        input_dict.update({'application_api_id': api_registered.application_api_id})
        input_dict.update({'status':'Unregistered'})

        action_filter={'application_api_id': api_registered.application_api_id}

        action='UPDATE'
        action_result = dbsession.table_action(dbmodel.APPLICATION_API, action, input_dict, action_filter, auto_commit=True, caller_area=_process_call_area)
        api_result = action_result
        api_result.update({'api_action': _api_action, 'api_name': _api_name})
        log_process_finish(_api_msgID, api_result, **_process_call_area)    
        return api_result
    else:
        msg = f'invalid action [[{action}]] requested. use REGISTER or UNREGISTER'
        api_result = {'api_status': 'error', 'api_message': msg, 'api_data': input_dict}
        log_process_finish(_api_msgID, api_result, **_process_call_area)    
        return api_result
#::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
def dbapi_application(dbsession, action, input_dict, action_filter={}, caller_area={}):
    _api_name = "dbapi_application"
    _api_entity = 'APPLICATION'
    _api_action = action
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

    if action.upper() in ('API_REGISTER', 'API_UNREGISTER'):
        xaction=action.upper().replace('API_','')
        return dbapi_api_register_unregister(dbsession, xaction, input_dict, action_filter, caller_area=_process_call_area)

    log_process_input('', 'input_dict', input_dict,**_process_call_area)
    log_process_input('', 'action_filter', action_filter,**_process_call_area)
    log_process_input('', 'caller_area', caller_area,**_process_call_area)

    if action.upper() == 'VALIDATE' or action.upper() == 'VALIDATE_CREDENTIALS':
        application_name=input_dict.get('application_name')
        if not application_name:
            application_name=action_filter.get('application_name')

        client_id=input_dict.get('client_id')
        if not client_id:
            client_id=input_dict.get('application_client_id')
        if not client_id:
            client_id=action_filter.get('client_id')
        if not client_id:
            client_id=action_filter.get('application_client_id')

        client_secretKey = input_dict.get('client_secretKey')
        if not client_secretKey:
            client_secretKey=input_dict.get('application_client_secretKey')
        if not client_secretKey:
            client_secretKey=action_filter.get('client_secretKey')
        if not client_secretKey:
            client_secretKey=action_filter.get('application_client_secretKey')

        return dbapi_application_credentials_are_valid(dbsession, application_name, client_id, client_secretKey)

    if action.upper() in ('ADD','INSERT','REGISTER','REFRESH'):
        if not input_dict.get('application_name'):
            msg = f'application name not defined'
            api_result = {'api_status': 'error', 'api_message': msg, 'api_data': input_dict}
            log_process_finish(_api_msgID, api_result, **_process_call_area)    
            return api_result

        if not input_dict.get('subscription_id') and not input_dict.get('client_id'):
            msg = f'subscription not defined'
            api_result = {'api_status': 'error', 'api_message': msg, 'api_data': input_dict}
            log_process_finish(_api_msgID, api_result, **_process_call_area)    
            return api_result

        subscription = dbsession.get(dbmodel.SUBSCRIPTION, input_dict, caller_area=_process_call_area)
        if not subscription:
            client=dbsession.get(dbmodel.CLIENT, input_dict, caller_area=_process_call_area)
            if client:
                input_dict.update({'client_id': client.client_id})
                subscription = dbsession.get(dbmodel.SUBSCRIPTION, input_dict, caller_area=_process_call_area)
        if not subscription:
            msg = f'subscription not found'
            api_result = {'api_status': 'error', 'api_message': msg, 'api_data': input_dict}
            log_process_finish(_api_msgID, api_result, **_process_call_area)    
            return api_result
        if not subscription.status=='Active':
            msg = f'subscription not Active'
            api_result = {'api_status': 'error', 'api_message': msg, 'api_data': input_dict}
            log_process_finish(_api_msgID, api_result, **_process_call_area)    
            return api_result
        
        app_rec={'application_name':input_dict.get('application_name')}
        application = dbsession.get(dbmodel.APPLICATION, app_rec, caller_area=_process_call_area)
        if application:
            if not application.subscription_id == subscription.subscription_id:
                msg = f'application {application.application_name} already in used. try another name'
                api_result = {'api_status': 'error', 'api_message': msg, 'api_data': input_dict}
                log_process_finish(_api_msgID, api_result, **_process_call_area)    
                return api_result

        subscription_record = subscription.to_dict()
        input_dict.update(subscription_record)
        client=dbsession.get(dbmodel.CLIENT, input_dict, caller_area=_process_call_area)
        if not client:
            msg = f'client not found'
            api_result = {'api_status': 'systemerror', 'api_message': msg, 'api_data': input_dict}
            log_process_finish(_api_msgID, api_result, **_process_call_area)    
            return api_result
        if not client.status=='Active':
            msg = f'client not Active'
            api_result = {'api_status': 'system error', 'api_message': msg, 'api_data': input_dict}
            log_process_finish(_api_msgID, api_result, **_process_call_area)    
            return api_result

    action_result = dbsession.table_action(dbmodel.APPLICATION, action , input_dict, action_filter, auto_commit=True, caller_area=_process_call_area)
    api_result = action_result
    api_result.update({'api_action': _api_action, 'api_name': _api_name})
    if api_result.get('api_status') == 'success':
        user_dict=api_result.get('api_data')
        user_dict.update({'user_role':'owner'})
        dbapi_application_USER(dbsession, 'register', user_dict,caller_area=_process_call_area)

    log_process_finish(_api_msgID, api_result, **_process_call_area)    
    return api_result
#::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
def dbapi_application_credentials_are_valid(dbsession, application_name, client_id, client_secretKey ,caller_area={}):
    _api_name = "dbapi_application_credentials_are_valid"
    _api_entity = 'APPLICATION'
    _api_action = 'validation'
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

    log_process_input('', 'application_name', application_name,**_process_call_area)
    log_process_input('', 'client_id', client_id,**_process_call_area)
    log_process_input('', 'client_secretKey', client_secretKey,**_process_call_area)

    application=dbsession.get(dbmodel.APPLICATION, {'application_name': application_name}, caller_area=_process_call_area)
    if not application:
        api_result=False
    else:
        if not application.client_id == client_id or not application.client_secretKey == client_secretKey:
            api_result=False
        else:
            api_result=True
    log_process_result(_api_msgID, api_result, data_name='application_credentials_are_valid', **_process_call_area)
    return api_result
#::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
def dbapi_application_api(dbsession, action, input_dict, action_filter={}, caller_area={}):
    _api_name = "dbapi_application_api"
    _api_entity = 'APPLICATION_API'
    _api_action = action
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

    log_process_input('', 'input_dict', input_dict,**_process_call_area)
    log_process_input('', 'action_filter', action_filter,**_process_call_area)
    log_process_input('', 'caller_area', caller_area,**_process_call_area)

    action_result = dbsession.table_action(dbmodel.APPLICATION_API, action , input_dict, action_filter, auto_commit=True, caller_area=_process_call_area)
    api_result = action_result
    api_result.update({'api_action': _api_action, 'api_name': _api_name})
    
    log_process_finish(_api_msgID, api_result, **_process_call_area)    
    return api_result
#::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
def dbapi_application_USER(dbsession, action, input_dict, action_filter={}, caller_area={}):
    _api_name = "dbapi_application_user"
    _api_entity = 'APPLICATION_USER'
    _api_action = action
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

    log_process_input('', 'input_dict', input_dict,**_process_call_area)
    log_process_input('', 'action_filter', action_filter,**_process_call_area)
    log_process_input('', 'caller_area', caller_area,**_process_call_area)

    if action.upper() in ('REGISTER', 'UNREGISTER', 'ADD', 'REFRESH'):
        if not input_dict.get('user_role'):
            msg = f'user role not defined'
            log_process_message('', 'error', msg, **_process_call_area)
            api_result = {'api_status': 'error', 'api_message': msg, 'api_action': _api_action.upper(), 'api_name': _api_name}
            log_process_finish(_api_msgID, api_result, **_process_call_area)
            return api_result

        client_id = input_dict.get('client_id')
        if client_id:
            client = dbsession.get(dbmodel.CLIENT, {'client_id': client_id}, caller_area=_process_call_area)
        else:
            client = dbsession.refresh(dbmodel.CLIENT, input_dict, auto_commit=True, caller_area=_process_call_area)
            
        if not client:
            msg = f'client not found'
            log_process_message('', 'error', msg, **_process_call_area)
            api_result = {'api_status': 'error', 'api_message': msg, 'api_action': _api_action.upper(), 'api_name': _api_name}
            log_process_finish(_api_msgID, api_result, **_process_call_area)
            return api_result
        
        if not client.status == 'Active':
            msg = f"client not Active.(status:{client.status})"
            log_process_message('', 'warning', msg, **_process_call_area)
            # api_result = {'api_status': 'error', 'api_message': msg, 'api_action': _api_action.upper(), 'api_name': _api_name}
            # log_process_finish(_api_msgID, api_result, **_process_call_area)
            #return api_result

        application_name=input_dict.get('application_name')
        application = dbsession.get(dbmodel.APPLICATION,  {'application_name': application_name}, caller_area=_process_call_area)
        if not application:
            application_id=input_dict.get('application_id')
            application = dbsession.get(dbmodel.APPLICATION,  {'application_id': application_id}, caller_area=_process_call_area)
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

        app_rec = application.to_dict()
        client_rec = client.to_dict()
        input_dict.update(app_rec)
        input_dict.update(client_rec)

        # input_dict.update({'application_name': application.application_name})
        # input_dict.update({'application_id': application.application_id})
        # input_dict.update({'client_id': application.client_id})
        # input_dict.update({'client_id': application.client_id})

        # if not input_dict.get('status'):
        #     input_dict.update({'status': 'Active'})

    action_result = dbsession.table_action(dbmodel.APPLICATION_USER, action , input_dict, action_filter, auto_commit=True, caller_area=_process_call_area)
    api_result = action_result
    api_result.update({'api_action': _api_action, 'api_name': _api_name})
    
    log_process_finish(_api_msgID, api_result, **_process_call_area)    
    return api_result
#::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
def dbapi_application_template(dbsession, action, input_dict, action_filter={}, caller_area={}):
    _api_name = "dbapi_template"
    _api_entity = 'TEMPLATE'
    _api_action = action
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

    log_process_input('', 'input_dict', input_dict,**_process_call_area)
    log_process_input('', 'action_filter', action_filter,**_process_call_area)
    log_process_input('', 'caller_area', caller_area,**_process_call_area)

    action_result = dbsession.table_action(dbmodel.APPLICATION_TEMPLATE, action, input_dict, action_filter, auto_commit=True, caller_area=_process_call_area)
    api_result = action_result
    api_result.update({'api_action': _api_action, 'api_name': _api_name})
    
    log_process_finish(_api_msgID, api_result, **_process_call_area)    
    return api_result
#::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
def dbapi_token(dbsession, action, input_dict, action_filter={}, caller_area={}):
    _api_name = "dbapi_token"
    _api_entity = 'TOKEN'
    _api_action = action
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

    log_process_input('', 'input_dict', input_dict,**_process_call_area)
    log_process_input('', 'action_filter', action_filter,**_process_call_area)
    log_process_input('', 'caller_area', caller_area,**_process_call_area)

    action_result = dbsession.table_action(dbmodel.TOKEN, action , input_dict, action_filter, auto_commit=True, caller_area=_process_call_area)
    api_result = action_result
    api_result.update({'api_action': _api_action, 'api_name': _api_name})
    
    log_process_finish(_api_msgID, api_result, **_process_call_area)    
    return api_result
#::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
def dbapi_subscription(dbsession, action, input_dict, action_filter={}, caller_area={}):
    _api_name = "dbapi_subscription"
    _api_entity = 'SUBSCRIPTION'
    _api_action = action
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

    log_process_input('', 'input_dict', input_dict,**_process_call_area)
    log_process_input('', 'action_filter', action_filter,**_process_call_area)
    log_process_input('', 'caller_area', caller_area,**_process_call_area)

    input_dict.update({'client_type': 'subscriber'})
    if action.upper() in ('REGISTER','ADD','REFRESH'):
        user = dbsession.get(dbmodel.USER, input_dict, caller_area=_process_call_area)
        if not user:
            user_id = ''
        else:
            user_id = user.user_id
        input_dict.update({'user_id': user_id})
        
    if action.upper() in ('REGISTER','ADD','REFRESH'):
        xaction='REFRESH'
        action_result = dbsession.table_action(dbmodel.CLIENT, xaction, input_dict, action_filter, auto_commit=True, caller_area=_process_call_area)
        api_result = action_result
        thismsg=action_result.get('api_message')
        api_result.update({'api_action': _api_action, 'api_name': _api_name})
        if not api_result.get('api_status') == 'success':
            msg = f"subscription not registered. client record create failed"
            log_process_message(_api_msgID, 'error', msg, **_process_call_area)
            log_process_finish(_api_msgID, api_result, **_process_call_area)    
            return api_result
        client = api_result.get('api_data')
        client_id = client.get('client_id')
        client_secretKey = client.get('client_secretKey')
        input_dict.update({'client_id': client_id})
        input_dict.update({'client_secretKey': client_secretKey})

    elif action.upper() in ('CONFIRM', 'ACTIVATE', 'DEACTIVATE', 'DELETE'):
        subscription_dict = dbsession.get(dbmodel.SUBSCRIPTION, input_dict, 'DICT', caller_area=_process_call_area)
        if not subscription_dict:
            msg = f'subscription not found'
            action_status='error'
            api_result = {'api_status': action_status, 'api_message': msg, 'api_data': input_dict, 'api_action': _api_action.upper(), 'api_name': _api_name}
            log_process_finish(_api_msgID, api_result, **_process_call_area)    
            return api_result
        client=dbsession.get(dbmodel.CLIENT, subscription_dict,'', caller_area=_process_call_area)
        if not client:
            msg = f'client not found'
            action_status='error'
            api_result = {'api_status': action_status, 'api_message': msg, 'api_data': subscription_dict, 'api_action': _api_action.upper(), 'api_name': _api_name}
            log_process_finish(_api_msgID, api_result, **_process_call_area)    
            return api_result

        client_id = client.client_id
        client_secretKey = client.client_secretKey
        input_dict.update({'client_id': client_id})
        input_dict.update({'client_secretKey': client_secretKey})

        api_result = dbsession.table_action(dbmodel.CLIENT, action, input_dict,  action_filter, auto_commit=True, caller_area=_process_call_area)
        api_result.update({'api_action': _api_action, 'api_name': _api_name})
        thismsg=api_result.get('api_message')
        if not api_result.get('api_status') == 'success':
            msg = f'action {action.upper()} on client {client_id} failed'
            log_process_message(_api_msgID, 'error', msg, **_process_call_area)
            log_process_finish(_api_msgID, api_result, **_process_call_area)    
            return api_result
        
        client_dict = api_result.get('api_data', {})
        client_status = client_dict.get('status')

        subscription_dict = dbsession.get(dbmodel.SUBSCRIPTION, subscription_dict, 'DICT', caller_area=_process_call_area)
        client_id=subscription_dict.get('client_id')
        input_dict.update({'status': client_status})
        input_dict.update({'client_id': client_id})
    
    action_result = dbsession.table_action(dbmodel.SUBSCRIPTION, action, input_dict,  action_filter, auto_commit=True, caller_area=_process_call_area)
    api_result = action_result
    thismsg=thismsg.replace('CLIENT',_api_entity)
    api_result.update({'api_action': _api_action, 'api_name': _api_name,'api_message':thismsg})
    
    log_process_finish(_api_msgID, api_result, **_process_call_area)    
    return api_result
#::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
def dbapi_user(dbsession, action, input_dict, action_filter={}, caller_area={}):
    _api_name = "dbapi_user"
    _api_entity = 'USER'
    _api_action = action
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

    log_process_input('', 'input_dict', input_dict,**_process_call_area)
    log_process_input('', 'action_filter', action_filter,**_process_call_area)
    log_process_input('', 'caller_area', caller_area,**_process_call_area)

    api_result = dbsession.table_action(dbmodel.USER, action , input_dict, action_filter, auto_commit=True, caller_area=_process_call_area)
    if not api_result.get('api_status') == 'success':
        log_process_finish(_api_msgID, api_result, **_process_call_area)    
        return api_result

    api_result.update({'api_action': _api_action, 'api_name': _api_name})
    log_process_finish(_api_msgID, api_result, **_process_call_area)    
    return api_result
# #::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
def dbapi_merchant(dbsession, action, input_dict, action_filter={}, caller_area={}):
    _api_name = "dbapi_merchant"
    _api_entity = 'MERCHANT'
    _api_action = action
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

    if (action.upper().find('BANKACCOUNT') >= 0 and action.upper().find('GET') >= 0) or action.upper() in ('BANKACCOUNTS', 'BANKACCOUNT'):
        return dbapi_merchant_get_bankaccounts(dbsession, input_dict, action_filter, caller_area=_process_call_area)
    elif action.upper().find('BANKACCOUNT') >= 0 and action.upper().find('REGISTER') >= 0:
        return dbapi_merchant_bankaccount_register(dbsession, input_dict, action_filter, caller_area=_process_call_area)

    log_process_input('', 'input_dict', input_dict,**_process_call_area)
    log_process_input('', 'action_filter', action_filter,**_process_call_area)
    log_process_input('', 'caller_area', caller_area,**_process_call_area)

    input_dict.update({'client_type': 'merchant'})

    if action.upper() in ('REGISTER','ADD','REFRESH'):
        action='REFRESH'
        action_result = dbsession.table_action(dbmodel.CLIENT, action, input_dict,  action_filter, auto_commit=True, caller_area=_process_call_area)
        api_result = action_result
        api_result.update({'api_action': _api_action, 'api_name': _api_name})
        thismsg=action_result.get('api_message')
        if not api_result.get('api_status') == 'success':
            log_process_finish(_api_msgID, api_result, **_process_call_area)    
            return api_result
        client = api_result.get('api_data')
        client_id = client.get('client_id')
        input_dict.update({'client_id': client_id})
    elif action.upper() in ('CONFIRM', 'ACTIVATE', 'DEACTIVATE', 'DELETE'):
        merchant_dict = dbsession.get(dbmodel.MERCHANT, input_dict, 'DICT', caller_area=_process_call_area)
        if not merchant_dict:
            msg = f'merchant not found'
            action_status='error'
            api_result = {'api_status': action_status, 'api_message': msg, 'api_data': input_dict, 'api_action': _api_action.upper(), 'api_name': _api_name}
            log_process_finish(_api_msgID, api_result, **_process_call_area)    
            return api_result
        client_dict=dbsession.get(dbmodel.CLIENT, merchant_dict,'DICT', caller_area=_process_call_area)
        if not client_dict:
            msg = f'client not found'
            action_status='error'
            api_result = {'api_status': action_status, 'api_message': msg, 'api_data': merchant_dict, 'api_action': _api_action.upper(), 'api_name': _api_name}
            log_process_finish(_api_msgID, api_result, **_process_call_area)    
            return api_result

        #action='CONFIRM'
        action_result = dbsession.table_action(dbmodel.CLIENT, action, input_dict,  action_filter, auto_commit=True, caller_area=_process_call_area)
        api_result = action_result
        api_result.update({'api_action': _api_action, 'api_name': _api_name})
        thismsg=action_result.get('api_message')
        # api_result = dbapi_client_confirm(client_dict)
        if not api_result.get('api_status') == 'success':
            # msg = f'client confirmation failed'
            # api_result.update({'api_message':msg})
            log_process_finish(_api_msgID, api_result, **_process_call_area)    
            return api_result
        merchant_dict = dbsession.get(dbmodel.MERCHANT, merchant_dict, 'DICT', caller_area=_process_call_area)
        status=merchant_dict.get('status')
        client_id=merchant_dict.get('client_id')
        # if not merchant_dict.get('status') == 'Active':
        #     msg = f"service provider not confirmed. status={status}"
        #     action_status='error'
        #     api_result = {'api_status': action_status, 'api_message': msg, 'api_data': merchant_dict, 'messages': messages, 'rows_added': rows_added, 'rows_updated': rows_updated, 'api_action': _api_action.upper(), 'api_name': _api_name}
        #     log_process_finish(_api_msgID, api_result, **_process_call_area)    
        #     return api_result
        input_dict.update({'status': status})
        input_dict.update({'client_id': client_id})
    
    action_result = dbsession.table_action(dbmodel.MERCHANT, action, input_dict,  action_filter, auto_commit=True, caller_area=_process_call_area)
    api_result = action_result
    #thismsg=thismsg.replace('CLIENT',_api_entity)
    api_result.update({'api_action': _api_action, 'api_name': _api_name})
    
    log_process_finish(_api_msgID, api_result, **_process_call_area)    
    return api_result
#::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
def dbapi_retail_store(dbsession, action, input_dict, action_filter={}, caller_area={}):
    _api_name = "dbapi_retail_store"
    _api_entity = 'RETAIL_STORE'
    _api_action = action
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

    log_process_input('', 'input_dict', input_dict,**_process_call_area)
    log_process_input('', 'action_filter', action_filter,**_process_call_area)
    log_process_input('', 'caller_area', caller_area,**_process_call_area)

    if action.upper() in ('REGISTER', 'ADD', 'REFRESH'):
        merchant_id = input_dict.get('merchant_id')
        merch_rec = {'merchant_id': merchant_id}
        merchant_name = input_dict.get('merchant_name')
        if merchant_name:
            merch_rec.update({'merchant_name':merchant_name})        
        merchant = dbsession.get(dbmodel.MERCHANT, merch_rec, caller_area=_process_call_area)
        if not merchant:
            msg = f'merchant not found'
            log_process_message('', 'error', msg, **_process_call_area)
            api_result = {'api_status': 'error', 'api_message': msg, 'api_action': _api_action.upper(), 'api_name': _api_name}
            log_process_finish(_api_msgID, api_result, **_process_call_area)
            return api_result
        
        if not merchant.status == 'Active':
            msg = f"merchant not Active.(status:{merchant.status})"
            log_process_message('', 'error', msg, **_process_call_area)
            api_result = {'api_status': 'error', 'api_message': msg, 'api_action': _api_action.upper(), 'api_name': _api_name}
            log_process_finish(_api_msgID, api_result, **_process_call_area)
            return api_result

        input_dict.update({'merchant_id': merchant.merchant_id})
        if not input_dict.get('status'):
            input_dict.update({'status': 'Active'})
        
    action_result = dbsession.table_action(dbmodel.RETAIL_STORE, action , input_dict, action_filter, auto_commit=True, caller_area=_process_call_area)
    api_result = action_result
    api_result.update({'api_action': _api_action, 'api_name': _api_name})
    
    log_process_finish(_api_msgID, api_result, **_process_call_area)    
    return api_result
#::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
def dbapi_pointofsale(dbsession, action, input_dict, action_filter={}, caller_area={}):
    _api_name = "dbapi_pointofsale"
    _api_entity = 'POINT_OF_SALE'
    _api_action = action
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

    if action.upper().find('BANKACCOUNT') >= 0 and (action.upper().find('ADD') >= 0 or action.upper().find('REGISTER') >= 0):
        return dbapi_pointofsale_bankaccount_remove(dbsession, input_dict, action_filter, caller_area=_process_call_area)
    elif action.upper().find('BANKACCOUNT') >= 0 and (action.upper().find('REMOVE') >= 0 or action.upper().find('DELETE') >= 0):
        return dbapi_pointofsale_bankaccount_add(dbsession, input_dict, action_filter, caller_area=_process_call_area)

    log_process_input('', 'input_dict', input_dict,**_process_call_area)
    log_process_input('', 'action_filter', action_filter,**_process_call_area)
    log_process_input('', 'caller_area', caller_area,**_process_call_area)

    if action.upper() in ('REGISTER', 'ADD', 'REFRESH'):
        retail_store_id = input_dict.get('retail_store_id')
        store_rec={'retail_store_id':retail_store_id}
        retail_store = dbsession.get(dbmodel.RETAIL_STORE, store_rec, caller_area=_process_call_area)
        if not retail_store:
            msg = f'retail_store not found'
            log_process_message('', 'error', msg, **_process_call_area)
            api_result = {'api_status': 'error', 'api_message': msg, 'api_action': _api_action.upper(), 'api_name': _api_name}
            log_process_finish(_api_msgID, api_result, **_process_call_area)
            return api_result
        
        if not retail_store.status == 'Active':
            msg = f"retail_store not Active.(status:{retail_store.status})"
            log_process_message('', 'error', msg, **_process_call_area)
            api_result = {'api_status': 'error', 'api_message': msg, 'api_action': _api_action.upper(), 'api_name': _api_name}
            log_process_finish(_api_msgID, api_result, **_process_call_area)
            return api_result

        input_dict.update({'retail_store_id': retail_store.retail_store_id})

        merchant_id = retail_store.merchant_id
        merch_rec = {'merchant_id': merchant_id}
        merchant = dbsession.get(dbmodel.MERCHANT, merch_rec, caller_area=_process_call_area)
        if not merchant:
            msg = f'merchant not found'
            log_process_message('', 'error', msg, **_process_call_area)
            api_result = {'api_status': 'error', 'api_message': msg, 'api_action': _api_action.upper(), 'api_name': _api_name}
            log_process_finish(_api_msgID, api_result, **_process_call_area)
            return api_result
        
        if not merchant.status == 'Active':
            msg = f"merchant not Active.(status:{merchant.status})"
            log_process_message('', 'error', msg, **_process_call_area)
            api_result = {'api_status': 'error', 'api_message': msg, 'api_action': _api_action.upper(), 'api_name': _api_name}
            log_process_finish(_api_msgID, api_result, **_process_call_area)
            return api_result

        input_dict.update({'merchant_id': merchant.merchant_id})

        if not input_dict.get('status'):
            input_dict.update({'status': 'Active'})
        
    action_result = dbsession.table_action(dbmodel.POINT_OF_SALE, action , input_dict, action_filter, auto_commit=True, caller_area=_process_call_area)
    api_result = action_result
    api_result.update({'api_action': _api_action, 'api_name': _api_name})
    
    log_process_finish(_api_msgID, api_result, **_process_call_area)    
    return api_result
#::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
def dbapi_service_point(dbsession, action, input_dict, action_filter={}, caller_area={}):
    _api_name = "dbapi_service_point"
    _api_entity = 'SERVICE_POINT'
    _api_action = action
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

    log_process_input('', 'input_dict', input_dict,**_process_call_area)
    log_process_input('', 'action_filter', action_filter,**_process_call_area)
    log_process_input('', 'caller_area', caller_area,**_process_call_area)

    if action.upper() in ('REGISTER', 'ADD', 'REFRESH'):
        retail_store_id = input_dict.get('retail_store_id')
        store_rec={'retail_store_id':retail_store_id}
        retail_store = dbsession.get(dbmodel.RETAIL_STORE, store_rec, caller_area=_process_call_area)
        if not retail_store:
            msg = f'retail_store not found'
            log_process_message('', 'error', msg, **_process_call_area)
            api_result = {'api_status': 'error', 'api_message': msg, 'api_action': _api_action.upper(), 'api_name': _api_name}
            log_process_finish(_api_msgID, api_result, **_process_call_area)
            return api_result
        
        if not retail_store.status == 'Active':
            msg = f"retail_store not Active.(status:{retail_store.status})"
            log_process_message('', 'error', msg, **_process_call_area)
            api_result = {'api_status': 'error', 'api_message': msg, 'api_action': _api_action.upper(), 'api_name': _api_name}
            log_process_finish(_api_msgID, api_result, **_process_call_area)
            return api_result

        input_dict.update({'retail_store_id': retail_store.retail_store_id})

        merchant_id = retail_store.merchant_id
        merch_rec = {'merchant_id': merchant_id}
        merchant = dbsession.get(dbmodel.MERCHANT, merch_rec, caller_area=_process_call_area)
        if not merchant:
            msg = f'merchant not found'
            log_process_message('', 'error', msg, **_process_call_area)
            api_result = {'api_status': 'error', 'api_message': msg, 'api_action': _api_action.upper(), 'api_name': _api_name}
            log_process_finish(_api_msgID, api_result, **_process_call_area)
            return api_result
        
        if not merchant.status == 'Active':
            msg = f"merchant not Active.(status:{merchant.status})"
            log_process_message('', 'error', msg, **_process_call_area)
            api_result = {'api_status': 'error', 'api_message': msg, 'api_action': _api_action.upper(), 'api_name': _api_name}
            log_process_finish(_api_msgID, api_result, **_process_call_area)
            return api_result

        input_dict.update({'merchant_id': merchant.merchant_id})

        if not input_dict.get('status'):
            input_dict.update({'status': 'Active'})

    action_result = dbsession.table_action(dbmodel.SERVICE_POINT, action , input_dict, action_filter, auto_commit=True, caller_area=_process_call_area)
    api_result = action_result
    api_result.update({'api_action': _api_action, 'api_name': _api_name})
    
    log_process_finish(_api_msgID, api_result, **_process_call_area)    
    return api_result
#::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
def dbapi_customer_service_assistant(dbsession, action, input_dict, action_filter={}, caller_area={}):
    _api_name = "dbapi_customer_service_assistant"
    _api_entity = 'CUSTOMER_SERVICE_ASSISTANT'
    _api_action = action
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

    log_process_input('', 'input_dict', input_dict,**_process_call_area)
    log_process_input('', 'action_filter', action_filter,**_process_call_area)
    log_process_input('', 'caller_area', caller_area,**_process_call_area)

    if action.upper() in ('REGISTER', 'ADD', 'REFRESH'):
        merchant_id=input_dict.get('merchant_id')
        merch_rec = {'merchant_id': merchant_id}
        merchant = dbsession.get(dbmodel.MERCHANT, merch_rec, caller_area=_process_call_area)
        if not merchant:
            msg = f'merchant not found'
            log_process_message('', 'error', msg, **_process_call_area)
            api_result = {'api_status': 'error', 'api_message': msg, 'api_action': _api_action.upper(), 'api_name': _api_name}
            log_process_finish(_api_msgID, api_result, **_process_call_area)
            return api_result
        
        if not merchant.status == 'Active':
            msg = f"merchant not Active.(status:{merchant.status})"
            log_process_message('', 'error', msg, **_process_call_area)
            api_result = {'api_status': 'error', 'api_message': msg, 'api_action': _api_action.upper(), 'api_name': _api_name}
            log_process_finish(_api_msgID, api_result, **_process_call_area)
            return api_result

        if not input_dict.get('status'):
            input_dict.update({'status': 'Active'})
        #client
        if input_dict.get('email'):
            action='REFRESH'
            input_dict.update({'client_type': 'customer_service_assistant'})
            action_result = dbsession.table_action(dbmodel.CLIENT, action, input_dict,  action_filter, auto_commit=True, caller_area=_process_call_area)
            api_result = action_result
            api_result.update({'api_action': _api_action, 'api_name': _api_name})
            thismsg=action_result.get('api_message')
            if not api_result.get('api_status') == 'success':
                log_process_finish(_api_msgID, api_result, **_process_call_area)    
                return api_result
            client = api_result.get('api_data')
            client_id = client.get('client_id')
            input_dict.update({'client_id': client_id})
        
    action_result = dbsession.table_action(dbmodel.CUSTOMER_SERVICE_ASSISTANT, action , input_dict, action_filter, auto_commit=True, caller_area=_process_call_area)
    api_result = action_result
    api_result.update({'api_action': _api_action, 'api_name': _api_name})
    
    log_process_finish(_api_msgID, api_result, **_process_call_area)    
    return api_result
#::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
def dbapi_merchant_get_bankaccounts(dbsession, merchant_record, action_filter={}, caller_area={}):
    _api_name = "dbapi_merchant_get_bankaccounts"
    _api_entity = 'MERCHANT'
    _api_action = 'get_bank_accounts'
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

    log_process_input('', 'input_dict', merchant_record,**_process_call_area)
    log_process_input('', 'action_filter', action_filter,**_process_call_area)
    log_process_input('', 'caller_area', caller_area,**_process_call_area)

    merchant = dbsession.get(dbmodel.MERCHANT, merchant_record, caller_area=_process_call_area)
    if not merchant:
        msg = f'merchant not found'
        log_process_message('', 'error', msg, **_process_call_area)
        api_result = {'api_status': 'error', 'api_message': msg, 'api_action': _api_action.upper(), 'api_name': _api_name}
        log_process_finish(_api_msgID, api_result, **_process_call_area)
        return api_result
    
    if not merchant.status == 'Active':
        msg = f"merchant not Active.(status:{merchant.status})"
        log_process_message('', 'error', msg, **_process_call_area)
        api_result = {'api_status': 'error', 'api_message': msg, 'api_action': _api_action.upper(), 'api_name': _api_name}
        log_process_finish(_api_msgID, api_result, **_process_call_area)
        return api_result

    client_id = merchant.client_id

    merchant_accounts=[]
    filterJson = {"client_id": client_id, "status": 'Active'}
    bank_accounts=dbsession.get_rows(dbmodel.BANK_ACCOUNT, filterJson, caller_area=_process_call_area)
    if bank_accounts:
        msg = f'[{len(bank_accounts)} bank accounts found] for merchant [{merchant.name}] client_id [{client_id}]'
        log_process_message('', 'success', msg, **_process_call_area)
        for bank_account in bank_accounts:
            bank_account_id = str(bank_account.bank_account_id)
            bank_accountID = str(bank_account.bank_accountID)
            merchant_accounts.append(bank_account_id)

    msg = f'OK. [{len(merchant_accounts)} bank accounts]'
    api_result = {'api_status': 'success', 'api_message': msg, 'data_records': len(merchant_accounts), 'api_data': merchant_accounts, 'api_action': _api_action.upper(), 'api_name': _api_name}
    log_process_finish(_api_msgID, api_result, **_process_call_area)    
    return api_result
#::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
def dbapi_merchant_bankaccount_register(dbsession, bankaccount_record, action_filter={}, caller_area={}):
    _api_name = "dbapi_merchant_bankaccount_register"
    _api_entity = 'MERCHANT'
    _api_action = 'register_bank_account'
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

    log_process_input('', 'input_dict', bankaccount_record,**_process_call_area)
    log_process_input('', 'action_filter', action_filter,**_process_call_area)
    log_process_input('', 'caller_area', caller_area,**_process_call_area)

    merchant = dbsession.get(dbmodel.MERCHANT, bankaccount_record, caller_area=_process_call_area)
    if not merchant:
        msg = f'merchant not found'
        log_process_message('', 'error', msg, **_process_call_area)
        api_result = {'api_status': 'error', 'api_message': msg, 'api_action': _api_action.upper(), 'api_name': _api_name}
        log_process_finish(_api_msgID, api_result, **_process_call_area)
        return api_result
    
    if not merchant.status == 'Active':
        msg = f"merchant not Active.(status:{merchant.status})"
        log_process_message('', 'error', msg, **_process_call_area)
        api_result = {'api_status': 'error', 'api_message': msg, 'api_action': _api_action.upper(), 'api_name': _api_name}
        log_process_finish(_api_msgID, api_result, **_process_call_area)
        return api_result

    bank_account_id=None
    account_id = bankaccount_record.get('bank_account_id')
    if account_id:
        bank_account_id = dbapi_get_bank_account_id(dbsession, account_id, caller_area={})
    if not bank_account_id:
        account_id = bankaccount_record.get('bank_accountID')
        if account_id:
            bank_account_id = dbapi_get_bank_account_id(dbsession, account_id, caller_area={})
    if not bank_account_id:
        account_id = bankaccount_record.get('bank_account')
        if account_id:
            bank_account_id = dbapi_get_bank_account_id(dbsession, account_id, caller_area={})
    if not bank_account_id:
        msg = f"bank_account not found"
        log_process_message('', 'error', msg, **_process_call_area)
        api_result = {'api_status': 'error', 'api_message': msg, 'api_action': _api_action.upper(), 'api_name': _api_name}
        log_process_finish(_api_msgID, api_result, **_process_call_area)
        return api_result

    bankaccount_record.update({'bank_account_id':bank_account_id})
    bankaccount_record.update({'merchant_id':merchant.merchant_id})
    
    bank_account = dbsession.get(dbmodel.BANK_ACCOUNT, {'bank_account_id':bank_account_id}, caller_area=_process_call_area)
    if not bank_account:
        msg = f"bank account not found"
        log_process_message('', 'error', msg, **_process_call_area)
        api_result = {'api_status': 'error', 'api_message': msg, 'api_action': _api_action.upper(), 'api_name': _api_name}
        log_process_finish(_api_msgID, api_result, **_process_call_area)
        return api_result
    if not bank_account.status == 'Active':
        msg = f"bank account {bank_account_id} not Active (status:{bank_account.status})"
        log_process_message('', 'error', msg, **_process_call_area)
        api_result = {'api_status': 'error', 'api_message': msg, 'api_action': _api_action.upper(), 'api_name': _api_name}
        log_process_finish(_api_msgID, api_result, **_process_call_area)
        return api_result

    merchant_record = bank_account.to_dict()

    merchant_record.update({'merchant_id': merchant.merchant_id})

    api_result = dbsession.table_action(dbmodel.MERCHANT, 'UPDATE', merchant_record, action_filter, auto_commit=True, caller_area=_process_call_area)
    api_result.update({'api_action': _api_action, 'api_name': _api_name})
        
    log_process_finish(_api_msgID, api_result, **_process_call_area)    

    return api_result
#::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
def dbapi_pointofsale_bankaccount_add(dbsession, bankaccount_record, action_filter={}, caller_area={}):
    _api_name = "dbapi_pointofsale_bankaccount_add"
    _api_entity = 'POINT_OF_SALE'
    _api_action = 'add_bank_account'
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

    log_process_input('', 'input_dict', bankaccount_record,**_process_call_area)
    log_process_input('', 'action_filter', action_filter,**_process_call_area)
    log_process_input('', 'caller_area', caller_area,**_process_call_area)

    pointofsale = dbsession.get(dbmodel.POINT_OF_SALE, bankaccount_record, caller_area=_process_call_area)
    if not pointofsale:
        msg = f'pointofsale not found'
        log_process_message('', 'error', msg, **_process_call_area)
        api_result = {'api_status': 'error', 'api_message': msg, 'api_action': _api_action.upper(), 'api_name': _api_name}
        log_process_finish(_api_msgID, api_result, **_process_call_area)
        return api_result
    
    if not pointofsale.status == 'Active':
        msg = f"pointofsale not Active.(status:{pointofsale.status})"
        log_process_message('', 'error', msg, **_process_call_area)
        api_result = {'api_status': 'error', 'api_message': msg, 'api_action': _api_action.upper(), 'api_name': _api_name}
        log_process_finish(_api_msgID, api_result, **_process_call_area)
        return api_result

    bank_account_id=None
    account_id = bankaccount_record.get('bank_account_id')
    if account_id:
        bank_account_id = dbapi_get_bank_account_id(dbsession, account_id, caller_area={})
    if not bank_account_id:
        account_id = bankaccount_record.get('bank_accountID')
        if account_id:
            bank_account_id = dbapi_get_bank_account_id(dbsession, account_id, caller_area={})
    if not bank_account_id:
        account_id = bankaccount_record.get('bank_account')
        if account_id:
            bank_account_id = dbapi_get_bank_account_id(dbsession, account_id, caller_area={})
    if not bank_account_id:
        msg = f"bank_account not found"
        log_process_message('', 'error', msg, **_process_call_area)
        api_result = {'api_status': 'error', 'api_message': msg, 'api_action': _api_action.upper(), 'api_name': _api_name}
        log_process_finish(_api_msgID, api_result, **_process_call_area)
        return api_result

    bankaccount_record.update({'bank_account_id':bank_account_id})
    bankaccount_record.update({'pointofsale_id':pointofsale.pointofsale_id})
    
    bank_account = dbsession.get(dbmodel.BANK_ACCOUNT, {'bank_account_id':bank_account_id}, caller_area=_process_call_area)
    if not bank_account:
        msg = f"bank account not found"
        log_process_message('', 'error', msg, **_process_call_area)
        api_result = {'api_status': 'error', 'api_message': msg, 'api_action': _api_action.upper(), 'api_name': _api_name}
        log_process_finish(_api_msgID, api_result, **_process_call_area)
        return api_result
    if not bank_account.status == 'Active':
        msg = f"bank account {bank_account_id} not Active (status:{bank_account.status})"
        log_process_message('', 'error', msg, **_process_call_area)
        api_result = {'api_status': 'error', 'api_message': msg, 'api_action': _api_action.upper(), 'api_name': _api_name}
        log_process_finish(_api_msgID, api_result, **_process_call_area)
        return api_result

    pointofsale_record = bank_account.to_dict()

    pointofsale_record.update({'pointofsale_id': pointofsale.pointofsale_id})

    api_result = dbsession.table_action(dbmodel.POINT_OF_SALE, 'UPDATE', pointofsale_record, action_filter, auto_commit=True, caller_area=_process_call_area)
    api_result.update({'api_action': _api_action, 'api_name': _api_name})
        
    log_process_finish(_api_msgID, api_result, **_process_call_area)    

    return api_result
#::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
def dbapi_pointofsale_bankaccount_remove(dbsession, pointofsale_record, action_filter={}, caller_area={}):
    _api_name = "dbapi_pointofsale_bankaccount_remove"
    _api_entity = 'POINT_OF_SALE'
    _api_action = 'remove_bank_account'
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

    log_process_input('', 'input_dict', pointofsale_record,**_process_call_area)
    log_process_input('', 'action_filter', action_filter,**_process_call_area)
    log_process_input('', 'caller_area', caller_area,**_process_call_area)

    pointofsale = dbsession.get(dbmodel.POINT_OF_SALE, pointofsale_record, caller_area=_process_call_area)
    if not pointofsale:
        msg = f'pointofsale not found'
        log_process_message('', 'error', msg, **_process_call_area)
        api_result = {'api_status': 'error', 'api_message': msg, 'api_action': _api_action.upper(), 'api_name': _api_name}
        log_process_finish(_api_msgID, api_result, **_process_call_area)
        return api_result
    
    if not pointofsale.status == 'Active':
        msg = f"pointofsale not Active.(status:{pointofsale.status})"
        log_process_message('', 'error', msg, **_process_call_area)
        api_result = {'api_status': 'error', 'api_message': msg, 'api_action': _api_action.upper(), 'api_name': _api_name}
        log_process_finish(_api_msgID, api_result, **_process_call_area)
        return api_result

    pointofsale_record = pointofsale.to_dict()
    
    pointofsale_record.update({
        'bank_account_id'       : '',
        'bank_subscription_id'  : '',
        'bank_code'             : '',
        'bank_subscriptionID'   : '',
        'bank_accountID'        : '',
        'payments_currency'     : '',
        })

    api_result = dbsession.table_action(dbmodel.POINT_OF_SALE, 'UPDATE', pointofsale_record, action_filter, auto_commit=True, caller_area=_process_call_area)
    api_result.update({'api_action': _api_action, 'api_name': _api_name})
        
    log_process_finish(_api_msgID, api_result, **_process_call_area)    

    return api_result
#::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
def dbapi_pointofsale_credit_info(dbsession, pointofsale_record, action_filter={}, caller_area={}):
    _api_name = "dbapi_pointofsale_credit_info"
    _api_entity = 'POINT_OF_SALE'
    _api_action = 'get_pointofsale_credit_info'
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

    log_process_input('', 'input_dict', pointofsale_record,**_process_call_area)
    log_process_input('', 'action_filter', action_filter,**_process_call_area)
    log_process_input('', 'caller_area', caller_area,**_process_call_area)

    pointofsale = dbsession.get(dbmodel.POINT_OF_SALE, pointofsale_record, caller_area=_process_call_area)
    if not pointofsale:
        msg = f'pointofsale not found'
        log_process_message('', 'error', msg, **_process_call_area)
        api_result = {'api_status': 'error', 'api_message': msg, 'api_action': _api_action.upper(), 'api_name': _api_name}
        log_process_finish(_api_msgID, api_result, **_process_call_area)
        return api_result
    
    if not pointofsale.status == 'Active':
        msg = f"pointofsale not Active.(status:{pointofsale.status})"
        log_process_message('', 'error', msg, **_process_call_area)
        api_result = {'api_status': 'error', 'api_message': msg, 'api_action': _api_action.upper(), 'api_name': _api_name}
        log_process_finish(_api_msgID, api_result, **_process_call_area)
        return api_result

    pointofsale_id=pointofsale.pointofsale_id
    merchant_id=pointofsale.merchant_id
    pointofsale_name = pointofsale.name
    bank_account_id = pointofsale.bank_account_id
    bank_subscription_id = pointofsale.bank_subscription_id
    bank_code = pointofsale.bank_code
    bank_subscriptionID = pointofsale.bank_subscriptionID
    bank_accountID = pointofsale.bank_accountID
    payments_currency = pointofsale.payments_currency
    
    pointofsale_record = pointofsale.to_dict()

    if not bank_accountID:
        merchant = dbsession.get(dbmodel.MERCHANT, {'merchant_id':merchant_id}, caller_area=_process_call_area)
        bank_account_id = merchant.bank_account_id
        bank_subscription_id = merchant.bank_subscription_id
        bank_code = merchant.bank_code
        bank_subscriptionID = merchant.bank_subscriptionID
        bank_accountID = merchant.bank_accountID
        payments_currency = merchant.payments_currency
        x = ' from merchant'
    else:
        x = ' from point_of_sale'

    credit_info = {
        'pointofsale_id': pointofsale_id,
        'pointofsale_name':pointofsale_name,
        'bank_account_id':bank_account_id,
        'bank_subscription_id':bank_subscription_id,
        'bank_code':bank_code,
        'bank_subscriptionID':bank_subscriptionID,
        'bank_accountID':bank_accountID,
        'payments_currency': payments_currency,
        }

    msg = f"OK. pointofsale credit info retrieved [{x}]"
    log_process_message('', 'success', msg, **_process_call_area)
    api_result = {'api_status': 'success', 'api_message': msg, 'api_data':credit_info, 'api_action': _api_action.upper(), 'api_name': _api_name}
    log_process_finish(_api_msgID, api_result, **_process_call_area)
    return api_result
#::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
def dbapi_interaction(dbsession, action, input_dict, action_filter={}, caller_area={}):
    _api_name = "dbapi_interaction"
    _api_entity = 'INTERACTION'
    _api_action = action
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
   
    if action.upper() in ('START','REQUEST'):
        return dbapi_interaction_start(dbsession, input_dict, caller_area=caller_area)
    elif action.upper() == 'ACCEPT':
        return dbapi_interaction_finish(dbsession, input_dict, caller_area=caller_area)
    elif action.upper() == 'FINISH':
        return dbapi_interaction_finish(dbsession, input_dict, caller_area=caller_area)
    elif action.upper() == 'MESSAGE':
        return dbapi_interaction_message_add(dbsession, input_dict, caller_area=caller_area)

    log_process_input('', 'input_dict', input_dict,**_process_call_area)
    log_process_input('', 'action_filter', action_filter,**_process_call_area)
    log_process_input('', 'caller_area', caller_area, **_process_call_area)

    action_result = dbsession.table_action(dbmodel.INTERACTION, action , input_dict, action_filter, auto_commit=True, caller_area=_process_call_area)
    api_result = action_result
    api_result.update({'api_action': _api_action, 'api_name': _api_name})
    
    log_process_finish(_api_msgID, api_result, **_process_call_area)    
    return api_result
#::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
def dbapi_interaction_message(dbsession, action, input_dict, action_filter={}, caller_area={}):
    _api_name = "dbapi_interaction_message"
    _api_entity = 'INTERACTION_MESSAGE'
    _api_action = action
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

    log_process_input('', 'input_dict', input_dict,**_process_call_area)
    log_process_input('', 'action_filter', action_filter,**_process_call_area)
    log_process_input('', 'caller_area', caller_area,**_process_call_area)

    action_result = dbsession.table_action(dbmodel.INTERACTION_MESSAGE, action , input_dict, action_filter, auto_commit=True, caller_area=_process_call_area)
    api_result = action_result
    api_result.update({'api_action': _api_action, 'api_name': _api_name})
    
    log_process_finish(_api_msgID, api_result, **_process_call_area)    
    return api_result
#::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
def dbapi_bank(dbsession, action, input_dict, action_filter={}, caller_area={}):
    _api_name = "dbapi_bank"
    _api_entity = 'BANK'
    _api_action = action
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

    log_process_input('', 'input_dict', input_dict,**_process_call_area)
    log_process_input('', 'action_filter', action_filter,**_process_call_area)
    log_process_input('', 'caller_area', caller_area,**_process_call_area)

    action_result = dbsession.table_action(dbmodel.BANK, action , input_dict, action_filter, auto_commit=True, caller_area=_process_call_area)
    api_result = action_result
    api_result.update({'api_action': _api_action, 'api_name': _api_name})
    
    log_process_finish(_api_msgID, api_result, **_process_call_area)    
    return api_result
#::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
def dbapi_bank_authorization(dbsession, action, input_dict, action_filter={}, caller_area={}):
    _api_name = "dbapi_bank_authorization"
    _api_entity = 'BANK_AUTHORIZATION'
    _api_action = action
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

    log_process_input('', 'input_dict', input_dict,**_process_call_area)
    log_process_input('', 'action_filter', action_filter,**_process_call_area)
    log_process_input('', 'caller_area', caller_area,**_process_call_area)

    action_result = dbsession.table_action(dbmodel.BANK_AUTHORIZATION, action , input_dict, action_filter, auto_commit=True, caller_area=_process_call_area)
    api_result = action_result
    api_result.update({'api_action': _api_action, 'api_name': _api_name})
    
    log_process_finish(_api_msgID, api_result, **_process_call_area)    
    return api_result
#::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
def dbapi_bank_subscription(dbsession, action, input_dict, action_filter={}, caller_area={}):
    _api_name = "dbapi_bank_subscription"
    _api_entity = 'BANK_SUBSCRIPTION'
    _api_action = action
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

    log_process_input('', 'input_dict', input_dict,**_process_call_area)
    log_process_input('', 'action_filter', action_filter,**_process_call_area)
    log_process_input('', 'caller_area', caller_area,**_process_call_area)

    action_result = dbsession.table_action(dbmodel.BANK_SUBSCRIPTION, action , input_dict, action_filter, auto_commit=True, caller_area=_process_call_area)
    api_result = action_result
    api_result.update({'api_action': _api_action, 'api_name': _api_name})
    
    log_process_finish(_api_msgID, api_result, **_process_call_area)    
    return api_result
#::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
def dbapi_bank_account(dbsession, action, input_dict, action_filter={}, caller_area={}):
    _api_name = "dbapi_bank_account"
    _api_entity = 'BANK_ACCOUNT'
    _api_action = action
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

    log_process_input('', 'input_dict', input_dict,**_process_call_area)
    log_process_input('', 'action_filter', action_filter,**_process_call_area)
    log_process_input('', 'caller_area', caller_area,**_process_call_area)

    action_result = dbsession.table_action(dbmodel.BANK_ACCOUNT, action , input_dict, action_filter, auto_commit=True, caller_area=_process_call_area)
    api_result = action_result
    api_result.update({'api_action': _api_action, 'api_name': _api_name})
    
    log_process_finish(_api_msgID, api_result, **_process_call_area)    
    return api_result
#::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
#::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
#::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
#::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
def dbapi_get_bank_account_id(dbsession, any_accountid, caller_area={}):
    if not any_accountid:
        return None

    _api_name = "dbapi_get_bank_account_id"
    _api_entity = 'BANK_ACCOUNT'
    _api_action = 'get'
    _api_msgID = set_msgID(_api_name, _api_action, _api_entity)

    _process_identity_kwargs = {'type': 'api', 'module': module_id, 'name': _api_name, 'action': _api_action, 'entity': _api_entity, 'msgID': _api_msgID,}
    _process_adapters_kwargs = {'dbsession': dbsession}
    _process_log_kwargs = {'indent_method': 'AUTO', 'indent_level':None}
    _process_debug_level = get_debug_level(caller_area.get('debug_level'), **_process_identity_kwargs, **_process_adapters_kwargs)
    _process_debug_files = get_debug_files(_process_debug_level, **_process_identity_kwargs, **_process_adapters_kwargs)
    _process_debug_kwargs={'debug_level':_process_debug_level,'debug_files':_process_debug_files}

    _process_signature = build_process_signature(**_process_identity_kwargs, **_process_adapters_kwargs, **_process_debug_kwargs, **_process_log_kwargs)
    _process_call_area = build_process_call_area(_process_signature, caller_area)

    account = dbsession.get(dbmodel.BANK_ACCOUNT, {'bank_account_id': any_accountid}, caller_area=_process_call_area)
    if account:
        bank_account_id = account.bank_account_id
    else:
        account = dbsession.get(dbmodel.BANK_ACCOUNT, {'bank_accountID': any_accountid}, caller_area=_process_call_area)
        if account:
            bank_account_id = account.bank_account_id
        else:
            bank_account_id = None
    return bank_account_id
#::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
def dbapi_get_bank_code(dbsession, any_bank_id, return_field='bank_id', caller_area={}):
    if not any_bank_id:
        return None

    _api_name = "dbapi_get_bank_code"
    _api_entity = 'BANK'
    _api_action = 'get'
    _api_msgID = set_msgID(_api_name, _api_action, _api_entity)

    _process_identity_kwargs = {'type': 'api', 'module': module_id, 'name': _api_name, 'action': _api_action, 'entity': _api_entity, 'msgID': _api_msgID,}
    _process_adapters_kwargs = {'dbsession': dbsession}
    _process_log_kwargs = {'indent_method': 'AUTO', 'indent_level':None}
    _process_debug_level = get_debug_level(caller_area.get('debug_level'), **_process_identity_kwargs, **_process_adapters_kwargs)
    _process_debug_files = get_debug_files(_process_debug_level, **_process_identity_kwargs, **_process_adapters_kwargs)
    _process_debug_kwargs={'debug_level':_process_debug_level,'debug_files':_process_debug_files}

    _process_signature = build_process_signature(**_process_identity_kwargs, **_process_adapters_kwargs, **_process_debug_kwargs, **_process_log_kwargs)
    _process_call_area = build_process_call_area(_process_signature, caller_area)

    bank = dbsession.get(dbmodel.BANK, {'bank_id': any_bank_id}, caller_area=_process_call_area)
    if not bank:
        bank = dbsession.get(dbmodel.BANK, {'bank_code': any_bank_id}, caller_area=_process_call_area)
    if not bank:
        bank = dbsession.get(dbmodel.BANK, {'bank_BIC': any_bank_id}, caller_area=_process_call_area)
    if not bank:
        return None
    if return_field.upper().find('CODE') >=0:
        return bank.bank_code
    elif return_field.upper().find('BIC') >=0:
        return bank.bank_BIC
    else:
        return bank.bank_id
#::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
def dbapi_device_log(dbsession, device_uid, application_name, geolocation_lat, geolocation_lon, client_id, caller_area={}):
    _api_name="dbapi_device_log"
    _api_entity = 'DEVICE'
    _api_action = 'log'
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

    log_process_input('', 'device_uid', device_uid,**_process_call_area)
    log_process_input('', 'application_name', application_name,**_process_call_area)
    log_process_input('', 'geolocation_lat', geolocation_lat,**_process_call_area)
    log_process_input('', 'geolocation_lon', geolocation_lon,**_process_call_area)
    log_process_input('', 'client_id', client_id,**_process_call_area)
    
    # print(geolocation_lat,geolocation_lon)
    # glat=geoloc_to_integer(geolocation_lat)
    # glon = geoloc_to_integer(geolocation_lon)
    # print(glat,glon)
    # glat2=integer_to_geoloc(glat)
    # glon2 = integer_to_geoloc(glon)
    # print(glat2,glon2)

    # geolocation_lat=geoloc_to_integer(geolocation_lat)
    # geolocation_lon=geoloc_to_integer(geolocation_lon)
    
    # print(geolocation_lat,geolocation_lon)
    
    now = datetime.datetime.utcnow()

    application_id = None
    if not application_name:
        application_name='?'
    application = dbsession.get(dbmodel.APPLICATION, {'application_name': application_name}, caller_area=_process_call_area)
    if application:
        application_id = application.application_id

    device_record = {'device_uid': device_uid, 'last_usage_geolocation_lat': geolocation_lat, 'last_usage_geolocation_lon': geolocation_lon, 'last_usage_timestamp': now}
    usage_record = {'device_uid': device_uid, 'application_name': application_name, 'geolocation_lat': geolocation_lat, 'geolocation_lon': geolocation_lon, 'client_id': client_id}
    client_device_record = {'device_uid': device_uid, 'client_id': client_id, 'application_name': application_name, 'application_id': application_id, 'last_usage_timestamp': now}

    device = dbsession.refresh(dbmodel.DEVICE, device_record, auto_commit=False, caller_area=_process_call_area)
    device_usage = dbsession.refresh(dbmodel.DEVICE_USAGE,usage_record, auto_commit=False, caller_area=_process_call_area)
    client_device = dbsession.refresh(dbmodel.CLIENT_DEVICE,client_device_record, auto_commit=False, caller_area=_process_call_area)

    dbsession.commit(**_process_call_area)

    if client_device:
        logged_record = client_device.to_dict()
        if device.times_used <= 1:
            msg=f"OK. new device logged"
        else:
            msg = f"OK. device logged, times_used:{device_usage.times_used}/{client_device.times_used}"
        log_process_message('', 'success', msg, **_process_call_area)
        api_result = {'api_status': 'success', 'api_message': msg, 'api_data': logged_record, 'api_action': _api_action.upper(), 'api_name': _api_name}
    else:
        msg = f"device logged FAILED"
        api_result = {'api_status': 'error', 'api_message': msg, 'api_data': {}, 'api_action': _api_action.upper(), 'api_name': _api_name}

    log_process_finish(_api_msgID, api_result, **_process_call_area)    

    return api_result
#::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
def dbapi_token_is_valid(dbsession, token, caller_area={}):
    _api_name = "dbapi_token_is_valid"
    _api_entity = 'TOKEN'
    _api_action = 'validation'    
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

    log_process_input('', 'token', token,**_process_call_area)
    log_process_input('', 'caller_area', caller_area,**_process_call_area)

    if type(token) == type(''):
        input_dict = {'token': token}
    elif type(token) == type({}):
        input_dict = token
    else:
        msg='invalid token provided'
        log_process_message('', 'error', msg, **_process_call_area)
        return False

    if not input_dict.get('token'):
        msg='no token provided'
        log_process_message('', 'error', msg, **_process_call_area)
        return False

    token_record = dbsession.get(dbmodel.TOKEN, input_dict, caller_area=_process_call_area)
        
    if not token_record:
        msg = f'access token is NOT valid.(not found)'
        log_process_message('', 'error', msg, **_process_call_area)
        return False

    expiryDT = token_record.expiryDT
    if not expiryDT:
        msg = f'access token is NOT valid.(no expiryDT)'
        log_process_message('', 'error', msg, **_process_call_area)
        return False

    #universal time
    #GMT=Greenwich Mean Time
    #UTC=Coordinated Universal Time
    #There is no time difference between Coordinated Universal Time and Greenwich Mean Time
    #nowString = datetime.datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S')
    #now=datetime.datetime.utcnow()
    if expiryDT < datetime.datetime.utcnow():
        msg = f'access token is NOT valid.(expired)'
        api_result = False
    api_result = True
    log_process_result(_api_msgID, api_result, data_name='access_token_is_valid', **_process_call_area)
    return api_result
#::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
def dbapi_token_get_access_token(dbsession, token_request, caller_area={}):
    _api_name = "dbapi_token_get_access_token"
    _api_entity = 'TOKEN'
    _api_action = 'GET_TOKEN'
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

    log_process_input('', 'token_request', token_request,**_process_call_area)
    log_process_input('', 'caller_area', caller_area,**_process_call_area)

    application_name=token_request.get('application_name')
    client_id=token_request.get('application_client_id')
    client_secretKey=token_request.get('application_client_secretKey')
    application = dbsession.get(dbmodel.APPLICATION, {'application_name': application_name, 'client_id': client_id}, caller_area=_process_call_area)
    if not application:
        msg='application not registered'
        api_result={'api_status': 'error', 'api_message': msg,'api_data':{}}
        log_process_finish(_api_msgID, api_result, **_process_call_area)    
        return api_result
    if not application.client_id == client_id or not application.client_secretKey == client_secretKey:
        msg='application credentials not valid'
        api_result={'api_status': 'error', 'api_message': msg,'api_data':{}}
        log_process_finish(_api_msgID, api_result, **_process_call_area)    
        return api_result

    token_duration_secs = 3600 #1 hour
    if token_request.get('token_scope') == 'application_service':
        token_duration_secs = 3600 #1 hour
    token_request.update({'duration_seconds':token_duration_secs})
    token_request.update({'status':'Active'})

    expiryDT = datetime.datetime.utcnow() + datetime.timedelta(seconds=token_duration_secs)
    token_request.update({'expiryDT': expiryDT})
    if 'token' in token_request.keys():
        token_request.pop('token')
    token = dbsession.insert(dbmodel.TOKEN, token_request,auto_commit=True, caller_area=_process_call_area)
    if not token:
        msg='token generation failed'
        api_result={'api_status': 'system error', 'api_message': msg,'api_data':{}}
        log_process_finish(_api_msgID, api_result, **_process_call_area)    
        return api_result

    token_record = {
        'token_type': token.token_type,
        'token_scope': token.token_scope,
        'grant_type': token.grant_type,
        'token': token.token,
        'duration_seconds': token.duration_seconds,
        'expiryDT': token.expiryDT,
        }

    msg='OK. token generated'
    api_result={'api_status': 'success', 'api_message': msg,'api_data':token_record}

    log_process_finish(_api_msgID, api_result, **_process_call_area)    
    return api_result
#::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
def dbapi_cleanup_tokens(dbsession, caller_area={}):
    _api_name = "debapi_cleanup_tokens"
    _api_entity = 'TOKEN'
    _api_action = 'CLEANUP'
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

    where_expression = {'status': 'Expired'}
    deleted_result = dbsession.delete_rows(dbmodel.TOKEN, where_expression, auto_commit=True)
    deleted_rows = deleted_result.get('rows_deleted', 0)

    #nowString = datetime.datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S')
    #where_expression = f"expiryDT<'{datetime.datetime.utcnow()}'"
    where_expression = {'expiryDT': {datetime.datetime.utcnow()}}
    update_dict = {'status': 'Expired'}
    expired_result = dbsession.update_rows(dbmodel.TOKEN, update_dict,where_expression, auto_commit=True, caller_area=_process_call_area)
    expired_rows = expired_result.get('rows_updated', 0)

    msg = f'tokens cleaned with {expired_rows} tokens expired, {deleted_rows} removed.'

    api_result = {'api_status': 'success', 'api_message': msg, 'rows_expired': expired_rows, 'rows_removed': deleted_rows}
    log_process_finish(_api_msgID, api_result, **_process_call_area)    
    return api_result
#::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
#::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
#::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
def dbapi_interaction_start(dbsession, input_dict, caller_area={}):
    _api_name = "dbapi_interaction_start"
    _api_entity = 'INTERACTION'
    _api_action = 'START'
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

    log_process_input('', 'input_dict', input_dict,**_process_call_area)
    log_process_input('', 'caller_area', caller_area,**_process_call_area)

    #////////////////////////////////////////
    originator = None
    originator_id = None
    originator_name = None
    corresponder = None
    corresponder_id = None
    corresponder_name = None
    #////////////////////////////////////////

    #step-1: originator
    (originator, originator_id, originator_name) = find_originator(dbsession, input_dict, _process_call_area)
    # originator_id = input_dict.get('originator_id')
    # if originator_id:
    #     xid = dbsession.get(dbmodel.CLIENT, {'client_id':originator_id}, caller_area=_process_call_area)
    #     if xid:
    #         originator='client'
    #         originator_name = xid.email
    #     else:
    #         xid = dbsession.get(dbmodel.POINT_OF_SALE, {'pointofsale_id':originator_id}, caller_area=_process_call_area)
    #         if xid:
    #             originator='pointofsale'
    #             originator_name = xid.name
    #         else:
    #             msg = f'originator not valid'
    #             api_result = {'api_status': 'error', 'api_message': msg, 'api_action': _api_action.upper(), 'api_name': _api_name}
    #             log_process_finish(_api_msgID, api_result, **_process_call_area)
    #             return api_result
    #     xoriginator = input_dict.get('originator')
    #     if xoriginator and not xoriginator == originator:
    #         msg = f'originator_id not valid for originator {xoriginator}'
    #         api_result = {'api_status': 'error', 'api_message': msg, 'api_action': _api_action.upper(), 'api_name': _api_name}
    #         log_process_finish(_api_msgID, api_result, **_process_call_area)
    #         return api_result
    # else:
    #     client_id = input_dict.get('client_id')
    #     if client_id:
    #         client=dbsession.get(dbmodel.CLIENT, {'client_id':client_id}, caller_area=_process_call_area)
    #         if not client:
    #             msg = f'client not found'
    #             api_result = {'api_status': 'error', 'api_message': msg, 'api_action': _api_action.upper(), 'api_name': _api_name}
    #             log_process_finish(_api_msgID, api_result, **_process_call_area)
    #             return api_result
    #         originator='client'
    #         originator_id=client_id
    #         originator_name = client.email
    #     else:
    #         pointofsale_id = input_dict.get('pointofsale_id')
    #         if pointofsale_id:
    #             pointofsale=dbsession.get(dbmodel.POINT_OF_SALE, {'pointofsale_id':pointofsale_id}, caller_area=_process_call_area)
    #             if not pointofsale:
    #                 msg = f'pointofsale not found'
    #                 api_result = {'api_status': 'error', 'api_message': msg, 'api_action': _api_action.upper(), 'api_name': _api_name}
    #                 log_process_finish(_api_msgID, api_result, **_process_call_area)
    #                 return api_result
    #             originator='pointofsale'
    #             originator_id=pointofsale_id
    #             originator_name = pointofsale.name
    #         else:
    #             msg = f'no pointofsale or consumer or client defined'
    #             api_result = {'api_status': 'error', 'api_message': msg, 'api_action': _api_action.upper(), 'api_name': _api_name}
    #             log_process_finish(_api_msgID, api_result, **_process_call_area)
    #             return api_result

    if not originator_id:
        msg = f'originator not defined (pointofsale or client or service_point)'
        api_result = {'api_status': 'error', 'api_message': msg, 'api_action': _api_action.upper(), 'api_name': _api_name}
        log_process_finish(_api_msgID, api_result, **_process_call_area)
        return api_result

    xoriginator = input_dict.get('originator')
    if xoriginator and not xoriginator == originator:
        msg = f'originator_id not valid for originator {xoriginator}'
        api_result = {'api_status': 'error', 'api_message': msg, 'api_action': _api_action.upper(), 'api_name': _api_name}
        log_process_finish(_api_msgID, api_result, **_process_call_area)
        return api_result

    input_dict.update({'originator': originator})
    input_dict.update({'originator_id': originator_id})
    input_dict.update({'originator_name': originator_name})
    
    msg = f'originator set to [{originator_name}]'
    log_process_message('', 'success', msg, **_process_call_area)
    
    #step-2: corresponder
    (corresponder, corresponder_id, corresponder_name) = find_corresponder(dbsession, input_dict, _process_call_area)
    # corresponder_id = input_dict.get('corresponder_id')
    # if not corresponder_id:
    #     msg = f'no corresponder specified'
    #     api_result = {'api_status': 'error', 'api_message': msg, 'api_action': _api_action.upper(), 'api_name': _api_name}
    #     log_process_finish(_api_msgID, api_result, **_process_call_area)
    #     return api_result
    # pointofsale = dbsession.get(dbmodel.POINT_OF_SALE, {'pointofsale_id':corresponder_id}, caller_area=_process_call_area)
    # if pointofsale:
    #     corresponder='pointofsale'
    #     corresponder_id = pointofsale.pointofsale_id
    #     corresponder_name = pointofsale.name
    # else:
    #     xid = dbsession.get(dbmodel.CLIENT, {'client_id':corresponder_id}, caller_area=_process_call_area)
    #     if xid:
    #         corresponder='client'
    #         corresponder_id=xid.client_id
    #         corresponder_name = xid.email          
    #     else:
    #         msg = f'corresponder not valid'
    #         api_result = {'api_status': 'error', 'api_message': msg, 'api_action': _api_action.upper(), 'api_name': _api_name}
    #         log_process_finish(_api_msgID, api_result, **_process_call_area)
    #         return api_result
    if not corresponder_id:
        msg = f'corresponder not valid'
        api_result = {'api_status': 'error', 'api_message': msg, 'api_action': _api_action.upper(), 'api_name': _api_name}
        log_process_finish(_api_msgID, api_result, **_process_call_area)
        return api_result

    xcorresponder = input_dict.get('corresponder')
    if xcorresponder and not xcorresponder == corresponder:
        msg = f'corresponder_id not valid for corresponder {xcorresponder}'
        api_result = {'api_status': 'error', 'api_message': msg, 'api_action': _api_action.upper(), 'api_name': _api_name}
        log_process_finish(_api_msgID, api_result, **_process_call_area)
        return api_result
    
    input_dict.update({'corresponder': corresponder})
    input_dict.update({'corresponder_id': corresponder_id})
    input_dict.update({'corresponder_name': corresponder_name})

    msg = f'corresponder set to [{corresponder_name}]'
    log_process_message('', 'success', msg, **_process_call_area)

    #step-3: already active
    filterJson = {"originator": originator, "originator_id": originator_id, "status": 'Active'}
    active_interactions=dbsession.get_rows(dbmodel.INTERACTION, filterJson, caller_area=_process_call_area)
    if active_interactions:
        msg = f'[{len(active_interactions)} active interactions found] for originator [{originator_name}]'
        log_process_message('', 'warning', msg, **_process_call_area)
        for active_interaction in active_interactions:
            interaction_id = active_interaction.interaction_id
            time_start = active_interaction.row_timestamp
            time_end = datetime.datetime.utcnow()
            diff = time_end - time_start
            duration = diff.days * 24 * 60 * 60 + diff.seconds
            interaction_rec = active_interaction.to_dict()
            interaction_rec.update({'status':'canceled','completed_timestamp':time_end,'duration':duration})
            active_interaction = dbsession.update(dbmodel.INTERACTION, interaction_rec, auto_commit=True, caller_area=_process_call_area)

    #step-4: corresponder is available (not active) 
    filterJson = {"corresponder": corresponder, "corresponder_id": corresponder_id, "status": 'Active'}
    active_interactions=dbsession.get_rows(dbmodel.INTERACTION, filterJson, caller_area=_process_call_area)
    if active_interactions:
        msg = f'[{len(active_interactions)} active interaction(s) found] for corresponder [{corresponder_name}]'
        log_process_message('', 'warning', msg, **_process_call_area)
        for active_interaction in active_interactions:
            interaction_id = active_interaction.interaction_id
            time_start = active_interaction.row_timestamp
            time_end = datetime.datetime.utcnow()
            diff = time_end - time_start
            duration = diff.days * 24 * 60 * 60 + diff.seconds
            if duration>5*60: # 5 minutes
                interaction_rec = active_interaction.to_dict()
                interaction_rec.update({'status':'canceled-timeout','completed_timestamp':time_end,'duration':duration})
                active_interaction = dbsession.update(dbmodel.INTERACTION, interaction_rec, auto_commit=True, caller_area=_process_call_area)
                msg = f'corresponder {corresponder_name} interaction {interaction_id} timed-out and canceled after {duration/60} minutes'
                log_process_message('', 'warning', msg, **_process_call_area)

        filterJson = {"corresponder": corresponder, "corresponder_id": corresponder_id, "status": 'Active'}
        active_interactions=dbsession.get_rows(dbmodel.INTERACTION, filterJson, caller_area=_process_call_area)
        if active_interactions:
            msg = f'corresponder {corresponder_name} is not available'
            log_process_message('', 'error', msg, **_process_call_area)
            api_result = {'api_status': 'error', 'api_message': msg, 'api_action': _api_action.upper(), 'api_name': _api_name}
            log_process_finish(_api_msgID, api_result, **_process_call_area)
            return api_result

    #step-5: insert
    input_dict.update({'status': 'Requested'})
    interaction = dbsession.insert(dbmodel.INTERACTION, input_dict, auto_commit=True, caller_area=_process_call_area)
    if not interaction:
        msg = f'interaction start failed'
        api_result = {'api_status': 'error', 'api_message': msg, 'api_action': _api_action.upper(), 'api_name': _api_name}
        log_process_finish(_api_msgID, api_result, **_process_call_area)
        return api_result

    interaction_id = interaction.interaction_id

    #step-6: message
    interaction_message = {
        'interaction_id':interaction_id,
        'originator_id':interaction.originator_id,
        'originator': interaction.originator,
        'originator_name': interaction.originator_name,
        'message_type':'start',
        'message_record':f"hi. i am {interaction.originator} {interaction.originator_name} and i want to interact with {interaction.corresponder} {interaction.corresponder_name}",
        'content_type':'text',
        'format':'',
        'application_name': input_dict.get('application_name'),
        'geolocation_lat': input_dict.get('geolocation_lat'),
        'geolocation_lon': input_dict.get('geolocation_lon'),
        }
    start_message = dbsession.insert(dbmodel.INTERACTION_MESSAGE, interaction_message, auto_commit=True, caller_area=_process_call_area)
    if not start_message:
        msg = f'start message insert failed'
        log_process_message('', 'error', msg, **_process_call_area)
        msg = f'interaction start failed (message insert failed)'
        api_result = {'api_status': 'error', 'api_message': msg, 'api_action': _api_action.upper(), 'api_name': _api_name}
        log_process_finish(_api_msgID, api_result, **_process_call_area)
        return api_result
    #shalimar
    #step-6: result
    interaction_record = interaction.to_dict()
    msg=f'OK. interaction established between You and {corresponder.upper()} {corresponder_name}'
    api_result = {'api_status': 'success', 'api_message': msg, 'interaction_id': interaction_id, 'api_data': interaction_record, 'api_action': _api_action.upper(), 'api_name': _api_name}
    log_process_finish(_api_msgID, api_result, **_process_call_area)    
    return api_result
#::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
def dbapi_interaction_accept(dbsession, input_dict, caller_area={}):
    _api_name = "dbapi_interaction_accept"
    _api_entity = 'INTERACTION'
    _api_action = 'ACCEPT'
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

    log_process_input('', 'input_dict', input_dict,**_process_call_area)
    log_process_input('', 'caller_area', caller_area,**_process_call_area)

    interaction_id = input_dict.get('interaction_id')
    if not interaction_id:
        msg = f'interaction not defined'
        log_process_message('', 'error', msg, **_process_call_area)
        api_result = {'api_status': 'error', 'api_message': msg}
        log_process_finish(_api_msgID, api_result, **_process_call_area)
        return

    interaction = dbsession.get(dbmodel.INTERACTION, {'interaction_id':interaction_id}, caller_area=_process_call_area)
    if not interaction:
        msg = f'interaction not found'
        api_result = {'api_status': 'error', 'api_message': msg}
        log_process_finish(_api_msgID, api_result, **_process_call_area)
        return

    if interaction.status == 'Active':
        msg = f'interaction is already Active'
        api_result = {'api_status': 'error', 'api_message': msg}
        log_process_finish(_api_msgID, api_result, **_process_call_area)
        return

    if not interaction.status=='Requested':
        msg = f'interaction is already [{interaction.status}]'
        api_result = {'api_status': 'error', 'api_message': msg}
        log_process_finish(_api_msgID, api_result, **_process_call_area)
        return

    #////////////////////////////////////////
    originator = None
    originator_id = None
    originator_name = None
    #////////////////////////////////////////
    # #step-1: originator
    # originator_id = input_dict.get('originator_id')
    # if originator_id:
    #     xid = dbsession.get(dbmodel.CLIENT, {'client_id':originator_id}, caller_area=_process_call_area)
    #     if xid:
    #         originator='client'
    #         originator_name = xid.email
    #     else:
    #         xid = dbsession.get(dbmodel.POINT_OF_SALE, {'pointofsale_id':originator_id}, caller_area=_process_call_area)
    #         if xid:
    #             originator='pointofsale'
    #             originator_name = xid.name
    #         else:
    #             msg = f'originator not valid'
    #             api_result = {'api_status': 'error', 'api_message': msg, 'api_action': _api_action.upper(), 'api_name': _api_name}
    #             log_process_finish(_api_msgID, api_result, **_process_call_area)
    #             return api_result
    #     xoriginator = input_dict.get('originator')
    #     if xoriginator and not xoriginator == originator:
    #         msg = f'originator_id not valid for originator {xoriginator}'
    #         log_process_message('', 'error', msg, **_process_call_area)
    #         api_result = {'api_status': 'error', 'api_message': msg, 'api_action': _api_action.upper(), 'api_name': _api_name}
    #         log_process_finish(_api_msgID, api_result, **_process_call_area)
    #         return api_result
    # else:
    #     client_id = input_dict.get('client_id')
    #     if client_id:
    #         client=dbsession.get(dbmodel.CLIENT, {'client_id':client_id}, caller_area=_process_call_area)
    #         if not client:
    #             msg = f'client not found'
    #             api_result = {'api_status': 'error', 'api_message': msg, 'api_action': _api_action.upper(), 'api_name': _api_name}
    #             log_process_finish(_api_msgID, api_result, **_process_call_area)
    #             return api_result
    #         originator='client'
    #         originator_id=client_id
    #         originator_name = client.email
    #     else:
    #         pointofsale_id = input_dict.get('pointofsale_id')
    #         if pointofsale_id:
    #             pointofsale=dbsession.get(dbmodel.POINT_OF_SALE, {'pointofsale_id':pointofsale_id}, caller_area=_process_call_area)
    #             if not pointofsale:
    #                 msg = f'pointofsale not found'
    #                 api_result = {'api_status': 'error', 'api_message': msg, 'api_action': _api_action.upper(), 'api_name': _api_name}
    #                 log_process_finish(_api_msgID, api_result, **_process_call_area)
    #                 return api_result
    #             originator='pointofsale'
    #             originator_id=pointofsale_id
    #             originator_name = pointofsale.name
    #         else:
    #             msg = f'no pointofsale or client defined'
    #             api_result = {'api_status': 'error', 'api_message': msg, 'api_action': _api_action.upper(), 'api_name': _api_name}
    #             log_process_finish(_api_msgID, api_result, **_process_call_area)
    #             return api_result
    (originator, originator_id, originator_name) = find_originator(dbsession, input_dict, _process_call_area)
    if not originator_id:
        msg = f'originator not defined (pointofsale or client or service_point)'
        api_result = {'api_status': 'error', 'api_message': msg, 'api_action': _api_action.upper(), 'api_name': _api_name}
        log_process_finish(_api_msgID, api_result, **_process_call_area)
        return api_result

    xoriginator = input_dict.get('originator')
    if xoriginator and not xoriginator == originator:
        msg = f'originator_id not valid for originator {xoriginator}'
        api_result = {'api_status': 'error', 'api_message': msg, 'api_action': _api_action.upper(), 'api_name': _api_name}
        log_process_finish(_api_msgID, api_result, **_process_call_area)
        return api_result
    # if not originator or not originator_id:
    #     msg = f'originator(as corresponder) not defined (pointofsale or client)'
    #     log_process_message('', 'error', msg, **_process_call_area)
    #     api_result = {'api_status': 'error', 'api_message': msg, 'api_action': _api_action.upper(), 'api_name': _api_name}
    #     log_process_finish(_api_msgID, api_result, **_process_call_area)
    #     return api_result

    if originator_id == interaction.originator_id:
        msg = f'accepter [{originator_name}] same as requestor'
        log_process_message('', 'error', msg, **_process_call_area)
        api_result = {'api_status': 'error', 'api_message': msg, 'api_action': _api_action.upper(), 'api_name': _api_name}
        log_process_finish(_api_msgID, api_result, **_process_call_area)
        return api_result

    if interaction.corresponder_id:
        if not originator_id == interaction.corresponder_id:
            msg = f'interaction must be accepted by [{interaction.corresponder}] {interaction.corresponder_name} [not] by  [{originator}] {originator_name} '
            api_result = {'api_status': 'error', 'api_message': msg}
            log_process_finish(_api_msgID, api_result, **_process_call_area)
            return

    input_dict.update({'corresponder': originator})
    input_dict.update({'corresponder_id': originator_id})
    input_dict.update({'corresponder_name': originator_name})

    msg=f'corresponder: [{originator}] [[{originator_name}]]'
    log_process_message('', 'success', msg, **_process_call_area)

    interaction_message = {
        'interaction_id': interaction_id,
        'originator_id': originator_id,
        'originator': originator,
        'originator_name': originator_name,
        'message_type':'accept',
        'message_record':f"hi. i am {originator} {originator_name}. how can i help you Mr. {interaction.originator} {interaction.originator_name}",
        'content_type':input_dict.get('content_type','text'),
        'format':input_dict.get('format',''),
        'application_name': input_dict.get('application_name'),
        'geolocation_lat': input_dict.get('geolocation_lat'),
        'geolocation_lon': input_dict.get('geolocation_lon'),
        }

    message = dbsession.insert(dbmodel.INTERACTION_MESSAGE, interaction_message, auto_commit=True, caller_area=_process_call_area)
    if not message:
        msg = f'interaction message add failed'
        log_process_message('', 'error', msg, **_process_call_area)

    time_start = interaction.row_timestamp
    time_end = datetime.datetime.utcnow()
    diff = time_end - time_start
    duration = diff.days * 24 * 60 * 60 + diff.seconds

    interaction_rec = interaction.to_dict()
    interaction_rec.update({
        'corresponder': originator,
        'corresponder_id': originator_id,
        'corresponder_name': originator_name,
        'status': 'Active',
        'last_usage_timestamp': datetime.datetime.utcnow(),
        'accept_geolocation_lat':input_dict.get('geolocation_lat'),
        'accept_geolocation_lon':input_dict.get('geolocation_lon'),
        })
    interaction = dbsession.update(dbmodel.INTERACTION, interaction_rec, auto_commit=True, caller_area=_process_call_area)
    if not interaction:
        msg = f'interaction accept failed'
        api_result = {'api_status': 'error', 'api_message': msg, 'api_action': _api_action.upper(), 'api_name': _api_name}
        log_process_message('', 'error', msg, **_process_call_area)
        return api_result
    
    #step-6: result
    interaction_rec = interaction.to_dict()
    msg=f'OK. interaction accepted'
    api_result = {'api_status': 'success', 'api_message': msg, 'interaction_id': interaction.interaction_id, 'api_data': interaction_rec, 'api_action': _api_action.upper(), 'api_name': _api_name}
    log_process_finish(_api_msgID, api_result, **_process_call_area)    
    return api_result
#::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
def dbapi_interaction_finish(dbsession, input_dict, caller_area={}):
    _api_name = "dbapi_interaction_finish"
    _api_entity = 'INTERACTION'
    _api_action = 'FINISH'
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

    log_process_input('', 'input_dict', input_dict,**_process_call_area)
    log_process_input('', 'caller_area', caller_area,**_process_call_area)

    interaction_id = input_dict.get('interaction_id')
    if not interaction_id:
        msg = f'interaction not defined'
        log_process_message('', 'error', msg, **_process_call_area)
        api_result = {'api_status': 'error', 'api_message': msg}
        log_process_finish(_api_msgID, api_result, **_process_call_area)
        return

    interaction = dbsession.get(dbmodel.INTERACTION, {'interaction_id':interaction_id}, caller_area=_process_call_area)
    if not interaction:
        msg = f'interaction not found'
        api_result = {'api_status': 'error', 'api_message': msg}
        log_process_finish(_api_msgID, api_result, **_process_call_area)
        return

    if not interaction.status=='Active':
        msg = f'interaction not Active'
        api_result = {'api_status': 'error', 'api_message': msg}
        log_process_finish(_api_msgID, api_result, **_process_call_area)
        return

    #////////////////////////////////////////
    originator = None
    originator_id = None
    originator_name = None
    #////////////////////////////////////////

    #step-1: originator
    # originator_id = input_dict.get('originator_id')
    # if originator_id:
    #     xid = dbsession.get(dbmodel.CLIENT, {'client_id':originator_id}, caller_area=_process_call_area)
    #     if xid:
    #         originator='client'
    #         originator_name = xid.email
    #     else:
    #         xid = dbsession.get(dbmodel.POINT_OF_SALE, {'pointofsale_id':originator_id}, caller_area=_process_call_area)
    #         if xid:
    #             originator='pointofsale'
    #             originator_name = xid.name
    #         else:
    #             msg = f'originator not valid'
    #             api_result = {'api_status': 'error', 'api_message': msg, 'api_action': _api_action.upper(), 'api_name': _api_name}
    #             log_process_finish(_api_msgID, api_result, **_process_call_area)
    #             return api_result
    #     xoriginator = input_dict.get('originator')
    #     if xoriginator and not xoriginator == originator:
    #         msg = f'originator_id not valid for originator {xoriginator}'
    #         log_process_message('', 'error', msg, **_process_call_area)
    #         api_result = {'api_status': 'error', 'api_message': msg, 'api_action': _api_action.upper(), 'api_name': _api_name}
    #         log_process_finish(_api_msgID, api_result, **_process_call_area)
    #         return api_result
    # else:
    #     client_id = input_dict.get('client_id')
    #     if client_id:
    #         client=dbsession.get(dbmodel.CLIENT, {'client_id':client_id}, caller_area=_process_call_area)
    #         if not client:
    #             msg = f'client not found'
    #             api_result = {'api_status': 'error', 'api_message': msg, 'api_action': _api_action.upper(), 'api_name': _api_name}
    #             log_process_finish(_api_msgID, api_result, **_process_call_area)
    #             return api_result
    #         originator='client'
    #         originator_id=client_id
    #         originator_name = client.email
    #     else:
    #         pointofsale_id = input_dict.get('pointofsale_id')
    #         if pointofsale_id:
    #             pointofsale=dbsession.get(dbmodel.POINT_OF_SALE, {'pointofsale_id':pointofsale_id}, caller_area=_process_call_area)
    #             if not pointofsale:
    #                 msg = f'pointofsale not found'
    #                 api_result = {'api_status': 'error', 'api_message': msg, 'api_action': _api_action.upper(), 'api_name': _api_name}
    #                 log_process_finish(_api_msgID, api_result, **_process_call_area)
    #                 return api_result
    #             originator='pointofsale'
    #             originator_id=pointofsale_id
    #             originator_name = pointofsale.name
    #         else:
    #             msg = f'no pointofsale or client defined'
    #             api_result = {'api_status': 'error', 'api_message': msg, 'api_action': _api_action.upper(), 'api_name': _api_name}
    #             log_process_finish(_api_msgID, api_result, **_process_call_area)
    #             return api_result

    (originator, originator_id, originator_name) = find_originator(dbsession, input_dict, _process_call_area)
    if not originator_id:
        msg = f'originator not defined (pointofsale or client or service_point)'
        api_result = {'api_status': 'error', 'api_message': msg, 'api_action': _api_action.upper(), 'api_name': _api_name}
        log_process_finish(_api_msgID, api_result, **_process_call_area)
        return api_result

    xoriginator = input_dict.get('originator')
    if xoriginator and not xoriginator == originator:
        msg = f'originator_id not valid for originator {xoriginator}'
        api_result = {'api_status': 'error', 'api_message': msg, 'api_action': _api_action.upper(), 'api_name': _api_name}
        log_process_finish(_api_msgID, api_result, **_process_call_area)
        return api_result

    # if not originator or not originator_id:
    #     msg = f'originator not defined (pointofsale or client)'
    #     log_process_message('', 'error', msg, **_process_call_area)
    #     api_result = {'api_status': 'error', 'api_message': msg, 'api_action': _api_action.upper(), 'api_name': _api_name}
    #     log_process_finish(_api_msgID, api_result, **_process_call_area)
    #     return api_result

    if not (originator_id == interaction.originator_id or originator_id == interaction.corresponder_id):
        msg = f'invalid originator [{originator_name}] for interaction [{interaction.interaction_id}]'
        log_process_message('', 'error', msg, **_process_call_area)
        api_result = {'api_status': 'error', 'api_message': msg, 'api_action': _api_action.upper(), 'api_name': _api_name}
        log_process_finish(_api_msgID, api_result, **_process_call_area)
        return api_result

    input_dict.update({'originator': originator})
    input_dict.update({'originator_id': originator_id})
    input_dict.update({'originator_name': originator_name})

    msg=f'originator: [{originator}] [[{originator_name}]]'
    log_process_message('', 'success', msg, **_process_call_area)
    
    interaction_message = {
        'interaction_id': interaction_id,
        'originator_id': input_dict.get('originator_id', ''),
        'originator': input_dict.get('originator', ''),
        'originator_name': input_dict.get('originator_name', ''),
        'content_type': input_dict.get('content_type', 'text'),
        'format': input_dict.get('format', ''),
        'application_name': input_dict.get('application_name'),
        'geolocation_lat': input_dict.get('geolocation_lat'),
        'geolocation_lon': input_dict.get('geolocation_lon'),
        'message_type': 'finish',
        'message_record':f"goodbye. Thank you for interacting with us.{input_dict.get('originator')} {input_dict.get('originator_name')}",
        }

    message = dbsession.insert(dbmodel.INTERACTION_MESSAGE, interaction_message, auto_commit=True, caller_area=_process_call_area)
    if not message:
        msg = f'interaction message add failed'
        log_process_message('', 'error', msg, **_process_call_area)

    time_start = interaction.row_timestamp
    time_end = datetime.datetime.utcnow()
    diff = time_end - time_start
    duration = diff.days * 24 * 60 * 60 + diff.seconds

    interaction_rec = interaction.to_dict()
    interaction_rec.update({'status':'completed','completed_timestamp':time_end,'duration':duration})
    interaction = dbsession.update(dbmodel.INTERACTION, interaction_rec, auto_commit=True, caller_area=_process_call_area)
    if not interaction:
        msg = f'interaction finish failed'
        api_result = {'api_status': 'error', 'api_message': msg, 'api_action': _api_action.upper(), 'api_name': _api_name}
        log_process_message('', 'error', msg, **_process_call_area)
        return api_result
    
    #step-6: result
    interaction_rec = interaction.to_dict()
    msg=f'OK. interaction finish'
    api_result = {'api_status': 'success', 'api_message': msg, 'interaction_id': interaction.interaction_id, 'api_data': interaction_rec, 'api_action': _api_action.upper(), 'api_name': _api_name}
    log_process_finish(_api_msgID, api_result, **_process_call_area)    
    return api_result
#::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
def dbapi_interaction_message_add(dbsession, input_dict, caller_area={}):
    _api_name = "dbapi_interaction_message_add"
    _api_entity = 'INTERACTION_MESSAGE'
    _api_action = 'ADD'
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

    log_process_input('', 'input_dict', input_dict,**_process_call_area)
    log_process_input('', 'caller_area', caller_area,**_process_call_area)

    interaction_id = input_dict.get('interaction_id')
    if not interaction_id:
        msg = f'interaction not defined'
        log_process_message('', 'error', msg, **_process_call_area)
        api_result = {'api_status': 'error', 'api_message': msg}
        log_process_finish(_api_msgID, api_result, **_process_call_area)
        return

    interaction = dbsession.get(dbmodel.INTERACTION, {'interaction_id':interaction_id}, caller_area=_process_call_area)
    if not interaction:
        msg = f'interaction not found'
        api_result = {'api_status': 'error', 'api_message': msg}
        log_process_finish(_api_msgID, api_result, **_process_call_area)
        return

    if not interaction.status=='Active':
        msg = f'interaction not Active'
        api_result = {'api_status': 'error', 'api_message': msg}
        log_process_finish(_api_msgID, api_result, **_process_call_area)
        return

    #////////////////////////////////////////
    originator = None
    originator_id = None
    originator_name = None
    #////////////////////////////////////////

    #step-1: originator
    # originator_id = input_dict.get('originator_id')
    # if originator_id:
    #     xid = dbsession.get(dbmodel.CLIENT, {'client_id':originator_id}, caller_area=_process_call_area)
    #     if xid:
    #         originator='client'
    #         originator_name = xid.email
    #     else:
    #         xid = dbsession.get(dbmodel.POINT_OF_SALE, {'pointofsale_id':originator_id}, caller_area=_process_call_area)
    #         if xid:
    #             originator='pointofsale'
    #             originator_name = xid.name
    #         else:
    #             msg = f'originator not valid'
    #             api_result = {'api_status': 'error', 'api_message': msg, 'api_action': _api_action.upper(), 'api_name': _api_name}
    #             log_process_finish(_api_msgID, api_result, **_process_call_area)
    #             return api_result
    #     xoriginator = input_dict.get('originator')
    #     if xoriginator and not xoriginator == originator:
    #         msg = f'originator_id not valid for originator {xoriginator}'
    #         log_process_message('', 'error', msg, **_process_call_area)
    #         api_result = {'api_status': 'error', 'api_message': msg, 'api_action': _api_action.upper(), 'api_name': _api_name}
    #         log_process_finish(_api_msgID, api_result, **_process_call_area)
    #         return api_result
    # else:
    #     client_id = input_dict.get('client_id')
    #     if client_id:
    #         client=dbsession.get(dbmodel.CLIENT, {'client_id':client_id}, caller_area=_process_call_area)
    #         if not client:
    #             msg = f'client not found'
    #             api_result = {'api_status': 'error', 'api_message': msg, 'api_action': _api_action.upper(), 'api_name': _api_name}
    #             log_process_finish(_api_msgID, api_result, **_process_call_area)
    #             return api_result
    #         originator='client'
    #         originator_id=client_id
    #         originator_name = client.email
    #     else:
    #         pointofsale_id = input_dict.get('pointofsale_id')
    #         if pointofsale_id:
    #             pointofsale=dbsession.get(dbmodel.POINT_OF_SALE, {'pointofsale_id':pointofsale_id}, caller_area=_process_call_area)
    #             if not pointofsale:
    #                 msg = f'pointofsale not found'
    #                 api_result = {'api_status': 'error', 'api_message': msg, 'api_action': _api_action.upper(), 'api_name': _api_name}
    #                 log_process_finish(_api_msgID, api_result, **_process_call_area)
    #                 return api_result
    #             originator='pointofsale'
    #             originator_id=pointofsale_id
    #             originator_name = pointofsale.name
    #         else:
    #             msg = f'no pointofsale or client defined'
    #             api_result = {'api_status': 'error', 'api_message': msg, 'api_action': _api_action.upper(), 'api_name': _api_name}
    #             log_process_finish(_api_msgID, api_result, **_process_call_area)
    #             return api_result

    # if not originator or not originator_id:
    #     msg = f'originator not defined (pointofsale or client)'
    #     log_process_message('', 'error', msg, **_process_call_area)
    #     api_result = {'api_status': 'error', 'api_message': msg, 'api_action': _api_action.upper(), 'api_name': _api_name}
    #     log_process_finish(_api_msgID, api_result, **_process_call_area)
    #     return api_result

    (originator, originator_id, originator_name) = find_originator(dbsession, input_dict, _process_call_area)
    if not originator_id:
        msg = f'originator not defined (pointofsale or client or service_point)'
        api_result = {'api_status': 'error', 'api_message': msg, 'api_action': _api_action.upper(), 'api_name': _api_name}
        log_process_finish(_api_msgID, api_result, **_process_call_area)
        return api_result

    xoriginator = input_dict.get('originator')
    if xoriginator and not xoriginator == originator:
        msg = f'originator_id not valid for originator {xoriginator}'
        api_result = {'api_status': 'error', 'api_message': msg, 'api_action': _api_action.upper(), 'api_name': _api_name}
        log_process_finish(_api_msgID, api_result, **_process_call_area)
        return api_result

    input_dict.update({'originator': originator})
    input_dict.update({'originator_id': originator_id})
    input_dict.update({'originator_name': originator_name})

    if not (originator_id == interaction.originator_id or originator_id == interaction.corresponder_id):
        msg = f'invalid originator [{originator_name}] for interaction [{interaction.interaction_id}]'
        api_result = {'api_status': 'error', 'api_message': msg, 'api_action': _api_action.upper(), 'api_name': _api_name}
        log_process_finish(_api_msgID, api_result, **_process_call_area)
        return api_result

    msg=f'originator: [{originator}] [[{originator_name}]]'
    log_process_message('', 'success', msg, **_process_call_area)

    interaction_message = {
        'interaction_id': interaction_id,
        'originator_id': originator_id,
        'originator': originator,
        'originator_name': originator_name,
        'message_type': input_dict.get('message_type', 'message'),
        'message_record': input_dict.get('message_record', ''),
        'content_type': input_dict.get('content_type', 'text'),
        'format': input_dict.get('format', ''),
        'application_name': input_dict.get('application_name'),
        'geolocation_lat': input_dict.get('geolocation_lat'),
        'geolocation_lon': input_dict.get('geolocation_lon'),
        }

    message = dbsession.insert(dbmodel.INTERACTION_MESSAGE, interaction_message, auto_commit=True, caller_area=_process_call_area)
    if not message:
        msg = f'interaction message add failed'
        api_result = {'api_status': 'error', 'api_message': msg, 'api_action': _api_action.upper(), 'api_name': _api_name}
        log_process_finish(_api_msgID, api_result, **_process_call_area)
        return api_result

    #step-6: result
    message_record = message.to_dict()
    msg=f'OK. interaction message added'
    api_result = {'api_status': 'success', 'api_message': msg, 'interaction_message_id': message.interaction_message_id, 'api_data': message_record, 'api_action': _api_action.upper(), 'api_name': _api_name}
    log_process_finish(_api_msgID, api_result, **_process_call_area)    
    return api_result
#::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
def find_originator(dbsession,input_dict={},caller_area={}):
    originator = None
    originator_id = None
    originator_name = None
    originator_id = input_dict.get('originator_id')
    if originator_id:
        client = dbsession.get(dbmodel.CLIENT, {'client_id':originator_id}, caller_area=caller_area)
        if client:
            originator='client'
            originator_name = client.email
        else:
            pointofsale = dbsession.get(dbmodel.POINT_OF_SALE, {'pointofsale_id': originator_id}, caller_area=caller_area)
            if pointofsale:
                originator='pointofsale'
                originator_name = pointofsale.name
            else:
                service_point=dbsession.get(dbmodel.SERVICE_POINT, {'servicepoint_id':originator_id}, caller_area=caller_area)
                if service_point:
                    originator='service_point'
                    originator_id=service_point.service_point_id
                    originator_name = service_point.name
    else:
        client_id = input_dict.get('client_id')
        if client_id:
            client=dbsession.get(dbmodel.CLIENT, {'client_id':client_id}, caller_area=caller_area)
            if client:
                originator='client'
                originator_id=client_id
                originator_name = client.email
        else:
            pointofsale_id = input_dict.get('pointofsale_id')
            if pointofsale_id:
                pointofsale=dbsession.get(dbmodel.POINT_OF_SALE, {'pointofsale_id':pointofsale_id}, caller_area=caller_area)
                if pointofsale:
                    originator='pointofsale'
                    originator_id=pointofsale_id
                    originator_name = pointofsale.name
            else:
                servicepoint_id = input_dict.get('servicepoint_id')
                if servicepoint_id:
                    service_point=dbsession.get(dbmodel.SERVICE_POINT, {'servicepoint_id':pointofsale_id}, caller_area=caller_area)
                    if service_point:
                        originator='service_point'
                        originator_id=service_point.service_point_id
                        originator_name = service_point.name
    return (originator, originator_id, originator_name)
#::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
def find_corresponder(dbsession,input_dict={},caller_area={}):
    corresponder = None
    corresponder_id = None
    corresponder_name = None
    corresponder_id = input_dict.get('corresponder_id')
    if corresponder_id:
        client = dbsession.get(dbmodel.CLIENT, {'client_id':corresponder_id}, caller_area=caller_area)
        if client:
            corresponder='client'
            corresponder_name = client.email
        else:
            pointofsale = dbsession.get(dbmodel.POINT_OF_SALE, {'pointofsale_id': corresponder_id}, caller_area=caller_area)
            if pointofsale:
                corresponder='pointofsale'
                corresponder_name = pointofsale.name
            else:
                service_point=dbsession.get(dbmodel.SERVICE_POINT, {'servicepoint_id':corresponder_id}, caller_area=caller_area)
                if service_point:
                    corresponder='service_point'
                    corresponder_id=service_point.service_point_id
                    corresponder_name = service_point.name
    return (corresponder, corresponder_id, corresponder_name)
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
master_configuration.update({'database_apis':[]})
master_configuration = add_apis_to_configuration('database_apis', master_configuration, thisModuleObj, functions_ids, exclude_functions_ids)
save_module_configuration(module_identityDictionary, master_configuration, print_enabled=consolelog_enabled, filelog_enabled=filelog_enabled)
thisApp.pair_module_configuration('database_apis',master_configuration)
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
# apis = thisApp.application_configuration.get('database_apis', {})
# for api_name in apis.keys():
#     api_entry = apis.get(api_name)
#     msg=f'from {module_id} import {api_name}'
#     log_message(msg)
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
