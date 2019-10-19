# -*- coding: utf-8 -*-
#https://www.pythoncentral.io/series/python-sqlalchemy-database-tutorial/
import os
import sys
import datetime
#


module_ProgramName = os.path.splitext(os.path.basename(__file__))[0]
module_id = '{}'.format(module_ProgramName)
module_version = 0.1

from _onlineApp import thisApp
from _onlineApp import get_debug_option_as_level, log_message, retrieve_module_configuration, get_globals_from_configuration, save_module_configuration
from _onlineApp import log_process_start, log_process_finish, log_process_message, log_process_result, log_process_data, log_process_input, log_process_output
#from _database_ganimides_engine import db_session
#session = db_session.session
import _database_ganimides_schema as dbschema
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
    'consolelog_enabled': consolelog_enabled,
    'filelog_enabled': filelog_enabled,
    'log_file':module_log_file_name,
    'errors_file_name': module_errors_file_name,
    }
#::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
#::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
apis_debug_dictionary = {
    'dbapi_xdevice':1,
}
#::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
#::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
#::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
# api services : database apis
#::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
#::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
#::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
def dbapi_device(dbsession, action, input_dict, filter_dict={}, caller_dict={},call_level=-1,debug_level=-1):
    _api_name = "dbapi_device"
    _api_entity = 'DEVICE'
    _api_action = action
    _api_msgID = set_api_msgID(_api_name, _api_action, _api_entity)    
    _api_debug_level = set_api_debug_level(_api_name, debug_level,dbsession)
    _api_level = call_level + 1
    _api_session_id = dbsession.session_id
    _api_indent_level=_api_level
    _api_indent_method='AUTO'

    _process_identity_dict = set_process_identity_dict('api', _api_name, _api_action, _api_entity, _api_msgID, _api_msgID, _api_session_id, _api_debug_level, print_enabled, filelog_enabled, log_file, errors_file, debug_file, _api_indent_level, _api_indent_method)
    _process_call_area = set_process_caller_area(_process_identity_dict, caller_dict)

    log_process_start(_api_msgID,**_process_identity_dict)

    if action.upper in ('REGISTER','UNREGISTER'):
        return dbapi_device_register_unregister(dbsession, action, input_dict, filter_dict, caller_dict, call_level=_api_level-1)

    log_process_input('', 'input_dict', input_dict,**_process_identity_dict)
    log_process_input('', 'filter_dict', filter_dict,**_process_identity_dict)
    log_process_input('', 'caller_dict', caller_dict,**_process_identity_dict)
    
    
    action_result = dbsession.table_action(dbmodel.DEVICE, action, input_dict, filter_dict, caller_dict={}, api_name=_api_name, api_entity=_api_entity, auto_commit=False, call_level=_api_level,debug_level=_api_debug_level-1)
    api_result = action_result
    api_result.update({'api_action': _api_action, 'api_name': _api_name})
        
    log_process_finish(_api_msgID, api_result, **_process_identity_dict)    
    dbsession.commit()
    return api_result
#::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
def dbapi_device_log(dbsession, device_uid, application_name, geolocation_lat, geolocation_lon, client_id,caller_dict={}, call_level=-1,debug_level=-1):
    _api_name="dbapi_device_log"
    _api_action = 'device_log'
    _api_entity = 'DEVICE'
    _api_msgID = set_api_msgID(_api_name, _api_action, _api_entity)    
    _api_debug_level = set_api_debug_level(_api_name, debug_level,dbsession)
    _api_level = call_level + 1
    _api_session_id = dbsession.session_id
    _api_indent_level=_api_level
    _api_indent_method='AUTO'

    _process_identity_dict = set_process_identity_dict('api', _api_name, _api_action, _api_entity, _api_msgID, _api_msgID, _api_session_id, _api_debug_level, print_enabled, filelog_enabled, log_file, errors_file, debug_file, _api_indent_level, _api_indent_method)
    _process_call_area = set_process_caller_area(_process_identity_dict, caller_dict)

    log_process_start(_api_msgID,**_process_identity_dict)

    log_process_input('', 'device_uid', device_uid,**_process_identity_dict)
    log_process_input('', 'application_name', application_name,**_process_identity_dict)
    log_process_input('', 'geolocation_lat', geolocation_lat,**_process_identity_dict)
    log_process_input('', 'geolocation_lon', geolocation_lon,**_process_identity_dict)
    log_process_input('', 'client_id', client_id,**_process_identity_dict)

    now = datetime.datetime.utcnow()

    application_id = None
    if not application_name:
        application_name='?'
    application = dbsession.get(dbmodel.APPLICATION, {'application_name': application_name},call_level=_api_level, debug_level=_api_debug_level-1)
    if application:
        application_id = application.application_id

    device_record = {'device_uid': device_uid, 'last_usage_geolocation_lat': geolocation_lat, 'last_usage_geolocation_lon': geolocation_lon, 'last_usage_timestamp': now}
    usage_record = {'device_uid': device_uid, 'application_name': application_name, 'geolocation_lat': geolocation_lat, 'geolocation_lon': geolocation_lon, 'client_id': client_id}
    client_device_record = {'device_uid': device_uid, 'client_id': client_id, 'application_name': application_name, 'application_id': application_id, 'last_usage_timestamp': now}

    device = dbsession.refresh(dbmodel.DEVICE, device_record, auto_commit=True, call_level=_api_level, debug_level=_api_debug_level-1)
    device_usage = dbsession.refresh(dbmodel.DEVICE_USAGE,usage_record, auto_commit=True, call_level=_api_level, debug_level=_api_debug_level-1)
    client_device = dbsession.refresh(dbmodel.CLIENT_DEVICE,client_device_record, auto_commit=True, call_level=_api_level, debug_level=_api_debug_level-1)
    if client_device:
        logged_record = client_device.to_dict()
        if device.times_used <= 1:
            msg=f"OK. new device logged"
        else:
            msg = f"OK. device logged, times_used:{client_device.times_used}"
        log_process_message('', 'success', msg, **_process_identity_dict)
        api_result = {'api_status': 'success', 'api_message': msg, 'api_data': logged_record, 'api_action': _api_action.upper(), 'api_name': _api_name}
    else:
        msg = f"device logged FAILED"
        api_result = {'api_status': 'error', 'api_message': msg, 'api_data': {}, 'api_action': _api_action.upper(), 'api_name': _api_name}

    log_process_finish(_api_msgID, api_result, **_process_identity_dict)    

    return api_result
#::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
def dbapi_device_register_unregister(dbsession, action, input_dict, filter_dict={}, caller_dict={},call_level=-1,debug_level=-1):
    _api_name="dbapi_device_register_unregister"
    _api_action = action
    _api_entity = 'DEVICE'
    _api_msgID = set_api_msgID(_api_name, _api_action, _api_entity)    
    _api_debug_level = set_api_debug_level(_api_name, debug_level,dbsession)
    _api_level = call_level + 1
    _api_session_id = dbsession.session_id
    _api_indent_level=_api_level
    _api_indent_method='AUTO'

    _process_identity_dict = set_process_identity_dict('api', _api_name, _api_action, _api_entity, _api_msgID, _api_msgID, _api_session_id, _api_debug_level, print_enabled, filelog_enabled, log_file, errors_file, debug_file, _api_indent_level, _api_indent_method)
    _process_call_area = set_process_caller_area(_process_identity_dict, caller_dict)

    log_process_start(_api_msgID,**_process_identity_dict)

    log_process_input('', 'input_dict', input_dict,**_process_identity_dict)
    log_process_input('', 'filter_dict', filter_dict,**_process_identity_dict)
    log_process_input('', 'caller_dict', caller_dict,**_process_identity_dict)

    actions_supported=('REGISTER', 'UNREGISTER')

    now = datetime.datetime.utcnow()

    if action.upper() not in actions_supported:
        msg = f"action '{action}' not supported. {actions_supported}"
        api_result = {'api_status': 'error', 'api_message': msg, 'api_data': actions_supported, 'api_action': _api_action.upper(), 'api_name': _api_name}
        log_process_finish(_api_msgID, api_result, **_process_identity_dict)    
        return api_result
    
    device = dbsession.get(dbmodel.DECICE, input_dict)
    if not device:
        device_record = device.valid_fields_dictionary(input_dict)
        msg = f"invalid device"
        api_result = {'api_status': 'error', 'api_message': msg, 'api_data': device_record, 'api_action': _api_action.upper(), 'api_name': _api_name}
        log_process_finish(_api_msgID, api_result, **_process_identity_dict)    
        return api_result

    client = dbsession.get(dbmodel.CLIENT, input_dict)
    if not client:
        client_record = client.valid_fields_dictionary(input_dict)
        msg = f"invalid client"
        api_result = {'api_status': 'error', 'api_message': msg, 'api_data': client_record, 'api_action': _api_action.upper(), 'api_name': _api_name}
        log_process_finish(_api_msgID, api_result, **_process_identity_dict)    
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
            log_process_finish(_api_msgID, api_result, **_process_identity_dict)    
            return api_result
        for client_device in client_devices:
            client_device.status = status
            application = dbsession.get(dbmodel.APPLICATION, {'application_name': client_device.application_name})
            registered_apps.append(application.application_name)
        dbsession.commit()
        client_device_records = dbsession.rows_to_dict(CLIENT_DEVICE, client_devices)
    else:
        application = dbsession.get(dbmodel.APPLICATION, input_dict)
        if not application:
            application_record = application.valid_fields_dictionary(input_dict)
            msg = f"invalid application"
            api_result = {'api_status': 'error', 'api_message': msg, 'api_data': application_record, 'api_action': _api_action.upper(), 'api_name': _api_name}
            log_process_finish(_api_msgID, api_result, **_process_identity_dict)    
            return api_result

        client_device_record = {'device_uid': device.device_uid, 'client_id': client_id, 'application_name': application.application_name, 'last_usage_timestamp': now, 'status': status}
        client_device = dbsession.get(dbmodel.CLIENT_DEVICE, client_device_record)
        if client_device:
            if client_device.status == status:
                msg = f"device already {client_device.status.upper()} {xx} usage by application '{client_device.application_name}'"
                client_device_records = [client_device.to_dict()]
                api_result = {'api_status': 'success', 'api_message': msg, 'api_data': client_device_records, 'api_action': _api_action.upper(), 'api_name': _api_name}
                log_process_finish(_api_msgID, api_result, **_process_identity_dict)    
                return api_result

        client_device = dbsession.refresh(dbmodel.CLIENT_DEVICE, client_device_record, auto_commit=False)
        registered_apps.append(application.application_name)
        dbsession.commit()
        client_device_records = [client_device.to_dict()]

    row_count = len(client_device_records)
    x=''
    if row_count > 1:
        x = 's'
        
    msg = f"device {status.upper()} {xx} usage by application{x} {registered_apps}"
    api_result = {'api_status': 'success', 'api_message': msg, 'api_data': client_device_records, 'api_data_rows': row_count, 'api_action': _api_action.upper(), 'api_name':_api_name }
    log_process_finish(_api_msgID, api_result, **_process_identity_dict)    
    return api_result
#::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
def dbapi_device_usage(dbsession, action, input_dict, filter_dict={}, caller_dict={},call_level=-1,debug_level=-1):
    _api_name = "dbapi_device_usage"
    _api_entity = 'DEVICE'
    _api_action = action
    _api_msgID = set_api_msgID(_api_name, _api_action, _api_entity)    
    _api_debug_level = set_api_debug_level(_api_name, debug_level,dbsession)
    _api_level = call_level + 1
    _api_session_id = dbsession.session_id
    _api_indent_level=_api_level
    _api_indent_method='AUTO'

    _process_identity_dict = set_process_identity_dict('api', _api_name, _api_action, _api_entity, _api_msgID, _api_msgID, _api_session_id, _api_debug_level, print_enabled, filelog_enabled, log_file, errors_file, debug_file, _api_indent_level, _api_indent_method)
    _process_call_area = set_process_caller_area(_process_identity_dict, caller_dict)

    log_process_start(_api_msgID,**_process_identity_dict)

    log_process_input('', 'input_dict', input_dict,**_process_identity_dict)
    log_process_input('', 'filter_dict', filter_dict,**_process_identity_dict)
    log_process_input('', 'caller_dict', caller_dict,**_process_identity_dict)

    action_result = dbsession.table_action(dbmodel.DEVICE_USAGE, action, input_dict, filter_dict, caller_dict={}, api_name=_api_name, api_entity=_api_entity, auto_commit=True, call_level=_api_level, debug_level=_api_debug_level-1)
    api_result = action_result
    api_result.update({'api_action': _api_action, 'api_name': _api_name})
    
    log_process_finish(_api_msgID, api_result, **_process_identity_dict)    
    return api_result
#::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
def dbapi_client(dbsession, action, input_dict, filter_dict={}, caller_dict={}, call_level=-1,debug_level=-1):
    _api_name = "dbapi_cient"
    _api_entity = 'CLIENT'
    _api_action = action
    _api_msgID = set_api_msgID(_api_name, _api_action, _api_entity)    
    _api_debug_level = set_api_debug_level(_api_name, debug_level,dbsession)
    _api_level = call_level + 1
    _api_session_id = dbsession.session_id
    _api_indent_level=_api_level
    _api_indent_method='AUTO'

    _process_identity_dict = set_process_identity_dict('api', _api_name, _api_action, _api_entity, _api_msgID, _api_msgID, _api_session_id, _api_debug_level, print_enabled, filelog_enabled, log_file, errors_file, debug_file, _api_indent_level, _api_indent_method)
    _process_call_area = set_process_caller_area(_process_identity_dict, caller_dict)

    log_process_start(_api_msgID,**_process_identity_dict)

    log_process_input('', 'input_dict', input_dict,**_process_identity_dict)
    log_process_input('', 'filter_dict', filter_dict,**_process_identity_dict)
    log_process_input('', 'caller_dict', caller_dict,**_process_identity_dict)

    api_result = dbsession.table_action(dbmodel.CLIENT, action , input_dict, filter_dict, caller_dict={}, api_name=_api_name, api_entity=_api_entity, auto_commit=True, call_level=_api_level, debug_level=_api_debug_level-1)
    if not api_result.get('api_status') == 'success':
        log_process_finish(_api_msgID, api_result, **_process_identity_dict)    
        return api_result

    if action.upper() in ('UPDATE', 'REFRESH', 'REGISTER', 'ACTIVATE', 'DEACTIVATE', 'CONFIRM'):
        client_dict = api_result.get('api_data', {})
        client_id = client_dict.get('client_id')
        client_type = client_dict.get('client_type')
        update_dict = {
            'status': client_dict.get('status'),
            'email': client_dict.get('email'),
            'client_id': client_dict.get('client_id'),
            'confirmed': client_dict.get('confirmed'),
            'confirmed_timestamp': client_dict.get('confirmed_timestamp'),
                }
        action = 'update_rows'
        filter_dict = {'client_id': client_id}
        if client_id and client_type:
            if client_type == 'merchant':
                xapi_result = dbsession.table_action(dbmodel.MERCHANT, action , update_dict, filter_dict, caller_dict={}, api_name=_api_name, api_entity=_api_entity, auto_commit=True, call_level=_api_level, debug_level=_api_debug_level-1)
            elif client_type == 'consumer':
                xapi_result = dbsession.table_action(dbmodel.CONSUMER, action , update_dict, filter_dict, caller_dict={}, api_name=_api_name, api_entity=_api_entity, auto_commit=True, call_level=_api_level, debug_level=_api_debug_level-1)
            elif client_type == 'service_provider':
                xapi_result = dbsession.table_action(dbmodel.SERVICE_PROVIDER, action , update_dict, filter_dict, caller_dict={}, api_name=_api_name, api_entity=_api_entity, auto_commit=True, call_level=_api_level, debug_level=_api_debug_level-1)

    api_result.update({'api_action': _api_action, 'api_name': _api_name})
    log_process_finish(_api_msgID, api_result, **_process_identity_dict)    
    return api_result
#::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
def dbapi_client_device(dbsession, action, input_dict, filter_dict={}, caller_dict={},call_level=-1,debug_level=-1):
    _api_name = "dbapi_client_device"
    _api_entity = 'DEVICE'
    _api_action = action
    _api_msgID = set_api_msgID(_api_name, _api_action, _api_entity)    
    _api_debug_level = set_api_debug_level(_api_name, debug_level,dbsession)
    _api_level = call_level + 1
    _api_session_id = dbsession.session_id
    _api_indent_level=_api_level
    _api_indent_method='AUTO'

    _process_identity_dict = set_process_identity_dict('api', _api_name, _api_action, _api_entity, _api_msgID, _api_msgID, _api_session_id, _api_debug_level, print_enabled, filelog_enabled, log_file, errors_file, debug_file, _api_indent_level, _api_indent_method)
    _process_call_area = set_process_caller_area(_process_identity_dict, caller_dict)

    log_process_start(_api_msgID,**_process_identity_dict)

    if action.upper in ('REGISTER','UNREGISTER'):
        return dbapi_device_register_unregister(dbsession, action, input_dict, filter_dict, caller_dict, call_level=_api_level-1)

    log_process_input('', 'input_dict', input_dict,**_process_identity_dict)
    log_process_input('', 'filter_dict', filter_dict,**_process_identity_dict)
    log_process_input('', 'caller_dict', caller_dict,**_process_identity_dict)


    action_result = dbsession.table_action(dbmodel.CLIENT_DEVICE, action, input_dict, filter_dict, caller_dict={}, api_name=_api_name, api_entity=_api_entity, auto_commit=True, call_level=_api_level, debug_level=_api_debug_level-1)
    api_result = action_result
    api_result.update({'api_action': _api_action, 'api_name': _api_name})
    
    log_process_finish(_api_msgID, api_result, **_process_identity_dict)    
    return api_result
#::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
def dbapi_api(dbsession, action, input_dict, filter_dict={}, caller_dict={}, call_level=-1,debug_level=-1):
    _api_name = "dbapi_api"
    _api_entity = 'API'
    _api_action = action
    _api_msgID = set_api_msgID(_api_name, _api_action, _api_entity)    
    _api_debug_level = set_api_debug_level(_api_name, debug_level,dbsession)
    _api_level = call_level + 1
    _api_session_id = dbsession.session_id
    _api_indent_level=_api_level
    _api_indent_method='AUTO'

    _process_identity_dict = set_process_identity_dict('api', _api_name, _api_action, _api_entity, _api_msgID, _api_msgID, _api_session_id, _api_debug_level, print_enabled, filelog_enabled, log_file, errors_file, debug_file, _api_indent_level, _api_indent_method)
    _process_call_area = set_process_caller_area(_process_identity_dict, caller_dict)

    log_process_start(_api_msgID,**_process_identity_dict)

    if action.upper() in ('REGISTER', 'UNREGISTER'):
        return dbapi_api_register_unregister(dbsession, action, input_dict, filter_dict, caller_dict, call_level=_api_level-1)

    log_process_input('', 'input_dict', input_dict,**_process_identity_dict)
    log_process_input('', 'filter_dict', filter_dict,**_process_identity_dict)
    log_process_input('', 'caller_dict', caller_dict,**_process_identity_dict)

    action_result = dbsession.table_action(dbmodel.API, action, input_dict, filter_dict, caller_dict={}, api_name=_api_name, api_entity=_api_entity, auto_commit=True, call_level=_api_level, debug_level=_api_debug_level-1)
    api_result = action_result
    api_result.update({'api_action': _api_action, 'api_name': _api_name})
    
    log_process_finish(_api_msgID, api_result, **_process_identity_dict)    
    return api_result    
#::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
def dbapi_api_register_unregister(dbsession, action, input_dict, filter_dict={}, caller_dict={}, call_level=-1,debug_level=-1):
    _api_name = "dbapi_api_register_unregister"
    _api_entity = 'APPLICATION API'
    _api_action = action
    _api_msgID = set_api_msgID(_api_name, _api_action, _api_entity)    
    _api_debug_level = set_api_debug_level(_api_name, debug_level,dbsession)
    _api_level = call_level + 1
    _api_session_id = dbsession.session_id
    _api_indent_level=_api_level
    _api_indent_method='AUTO'

    _process_identity_dict = set_process_identity_dict('api', _api_name, _api_action, _api_entity, _api_msgID, _api_msgID, _api_session_id, _api_debug_level, print_enabled, filelog_enabled, log_file, errors_file, debug_file, _api_indent_level, _api_indent_method)
    _process_call_area = set_process_caller_area(_process_identity_dict, caller_dict)

    log_process_start(_api_msgID,**_process_identity_dict)

    if action.upper not in ('REGISTER','UNREGISTER'):
        msg = f'invalid action [[{action}]] requested. use REGISTER or UNREGISTER'
        api_result = {'api_status': 'error', 'api_message': msg, 'api_data': input_dict}
        log_process_finish(_api_msgID, api_result, **_process_identity_dict)    
        return api_result

    log_process_input('', 'input_dict', input_dict,**_process_identity_dict)
    log_process_input('', 'filter_dict', filter_dict,**_process_identity_dict)
    log_process_input('', 'caller_dict', caller_dict,**_process_identity_dict)

    if _api_action.upper() == 'REGISTER':
        api=dbsession.get(dbmodel.API, input_dict)
        if not api:
            msg = f'api not found'
            api_result = {'api_status': 'error', 'api_message': msg, 'api_data': input_dict}
            log_process_finish(_api_msgID, api_result, **_process_identity_dict)    
            return api_result
        if not api.status=='Active':
            msg = f'api not Active'
            api_result = {'api_status': 'error', 'api_message': msg, 'api_data': input_dict}
            log_process_finish(_api_msgID, api_result, **_process_identity_dict)    
            return api_result
        application=dbsession.get(dbmodel.APPLICATION, input_dict)
        if not application:
            msg = f'application not found'
            api_result = {'api_status': 'error', 'api_message': msg, 'api_data': input_dict}
            log_process_finish(_api_msgID, api_result, **_process_identity_dict)    
            return api_result
        if not application.status=='Active':
            msg = f'application not Active'
            api_result = {'api_status': 'error', 'api_message': msg, 'api_data': input_dict}
            log_process_finish(_api_msgID, api_result, **_process_identity_dict)    
            return api_result

        input_dict.update({'api_id':api.api_id})
        input_dict.update({'api_name':api.api_name})
        input_dict.update({'application_id': application.application_id})
        input_dict.update({'application_name': application.application_name})

        filter_dict={}
        api_registered = dbsession.get(dbmodel.APPLICATION_API, input_dict)
        if api_registered:  
            input_dict.update({'application_api_id': api_registered.application_api_id})
            filter_dict = {'application_api_id': api_registered.application_api_id}
            
        input_dict.update({'status': 'Active'})
        action='REFRESH'
        action_result = dbsession.table_action(dbmodel.APPLICATION_API, action , input_dict, filter_dict, caller_dict={}, api_name=_api_name, api_entity=_api_entity, auto_commit=True, call_level=_api_level, debug_level=_api_debug_level-1)
        api_result = action_result
        api_result.update({'api_action': _api_action, 'api_name': _api_name})
        log_process_finish(_api_msgID, api_result, **_process_identity_dict)    
        return api_result
    elif _api_action.upper() == 'UNREGISTER':
        api=dbsession.get(dbmodel.API, input_dict)
        if api:
            input_dict.update({'api_id':api.api_id})
            input_dict.update({'api_name':api.api_name})

        application=dbsession.get(dbmodel.APPLICATION, input_dict)
        if application:
            input_dict.update({'application_id': application.application_id})
            input_dict.update({'application_name': application.application_name})

        api_registered = dbsession.get(dbmodel.APPLICATION_API, input_dict)
        if not api_registered:
            msg = f'record not found'
            api_result = {'api_status': 'error', 'api_message': msg, 'api_data': input_dict}
            log_process_finish(_api_msgID, api_result, **_process_identity_dict)    
            return api_result

        input_dict.update({'application_api_id': api_registered.application_api_id})
        input_dict.update({'status':'Unregistered'})

        filter_dict={'application_api_id': api_registered.application_api_id}

        action='UPDATE'
        action_result = dbsession.table_action(dbmodel.APPLICATION_API, action, input_dict, filter_dict, caller_dict={}, api_name=_api_name, api_entity=_api_entity, auto_commit=True, call_level=_api_level, debug_level=_api_debug_level-1)
        api_result = action_result
        api_result.update({'api_action': _api_action, 'api_name': _api_name})
        log_process_finish(_api_msgID, api_result, **_process_identity_dict)    
        return api_result
    else:
        msg = f'invalid action [[{action}]] requested. use REGISTER or UNREGISTER'
        api_result = {'api_status': 'error', 'api_message': msg, 'api_data': input_dict}
        log_process_finish(_api_msgID, api_result, **_process_identity_dict)    
        return api_result
#::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
def dbapi_application(dbsession, action, input_dict, filter_dict={}, caller_dict={}, call_level=-1,debug_level=-1):
    _api_name = "dbapi_application"
    _api_entity = 'APPLICATION'
    _api_action = action
    _api_msgID = set_api_msgID(_api_name, _api_action, _api_entity)    
    _api_debug_level = set_api_debug_level(_api_name, debug_level,dbsession)
    _api_level = call_level + 1
    _api_session_id = dbsession.session_id
    _api_indent_level=_api_level
    _api_indent_method='AUTO'

    _process_identity_dict = set_process_identity_dict('api', _api_name, _api_action, _api_entity, _api_msgID, _api_msgID, _api_session_id, _api_debug_level, print_enabled, filelog_enabled, log_file, errors_file, debug_file, _api_indent_level, _api_indent_method)
    _process_call_area = set_process_caller_area(_process_identity_dict, caller_dict)

    log_process_start(_api_msgID,**_process_identity_dict)

    if action.upper() in ('API_REGISTER','API_UNREGISTER'):
        return dbapi_api_register_unregister(dbsession, action, input_dict, filter_dict, caller_dict, call_level=_api_level-1)

    log_process_input('', 'input_dict', input_dict,**_process_identity_dict)
    log_process_input('', 'filter_dict', filter_dict,**_process_identity_dict)
    log_process_input('', 'caller_dict', caller_dict,**_process_identity_dict)

    if action.upper() == 'VALIDATE' or action.upper() == 'VALIDATE_CREDENTIALS':
        application_name=input_dict.get('application_name')
        if not application_name:
            application_name=filter_dict.get('application_name')

        client_id=input_dict.get('client_id')
        if not client_id:
            client_id=input_dict.get('application_client_id')
        if not client_id:
            client_id=filter_dict.get('client_id')
        if not client_id:
            client_id=filter_dict.get('application_client_id')

        client_secretKey = input_dict.get('client_secretKey')
        if not client_secretKey:
            client_secretKey=input_dict.get('application_client_secretKey')
        if not client_secretKey:
            client_secretKey=filter_dict.get('client_secretKey')
        if not client_secretKey:
            client_secretKey=filter_dict.get('application_client_secretKey')

        return dbapi_application_credentials_are_valid(dbsession, application_name, client_id, client_secretKey)

    if action.upper() in ('ADD','INSERT','REGISTER','REFRESH'):
        client=dbsession.get(dbmodel.CLIENT, input_dict)
        if not client:
            msg = f'client not found'
            api_result = {'api_status': 'error', 'api_message': msg, 'api_data': input_dict}
            log_process_finish(_api_msgID, api_result, **_process_identity_dict)    
            return api_result

        if not client.status=='Active':
            msg = f'client not Active'
            api_result = {'api_status': 'error', 'api_message': msg, 'api_data': input_dict}
            log_process_finish(_api_msgID, api_result, **_process_identity_dict)    
            return api_result

        input_dict.update({'client_id': client.client_id}) 
        input_dict.update({'status': 'Active'}) 

    action_result = dbsession.table_action(dbmodel.APPLICATION, action , input_dict, filter_dict, caller_dict={}, api_name=_api_name, api_entity=_api_entity, auto_commit=True, call_level=_api_level, debug_level=_api_debug_level-1)
    api_result = action_result
    api_result.update({'api_action': _api_action, 'api_name': _api_name})
    
    log_process_finish(_api_msgID, api_result, **_process_identity_dict)    
    return api_result
#::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
def dbapi_application_credentials_are_valid(dbsession, application_name, client_id, client_secretKey,caller_dict={}, call_level=-1,debug_level=-1):
    _api_name = "dbapi_application_credentials_are_valid"
    _api_entity = 'APPLICATION'
    _api_action = 'validation'
    _api_msgID = set_api_msgID(_api_name, _api_action, _api_entity)    
    _api_debug_level = set_api_debug_level(_api_name, debug_level,dbsession)
    _api_level = call_level + 1
    _api_session_id = dbsession.session_id
    _api_indent_level=_api_level
    _api_indent_method='AUTO'

    _process_identity_dict = set_process_identity_dict('api', _api_name, _api_action, _api_entity, _api_msgID, _api_msgID, _api_session_id, _api_debug_level, print_enabled, filelog_enabled, log_file, errors_file, debug_file, _api_indent_level, _api_indent_method)
    _process_call_area = set_process_caller_area(_process_identity_dict, caller_dict)

    log_process_start(_api_msgID,**_process_identity_dict)

    log_process_input('', 'application_name', application_name,**_process_identity_dict)
    log_process_input('', 'client_id', client_id,**_process_identity_dict)
    log_process_input('', 'client_secretKey', client_secretKey,**_process_identity_dict)

    application=dbsession.get(dbmodel.APPLICATION, {'application_name': application_name})
    if not application:
        api_result=False
        # return False    
    if not application.client_id == client_id or not application.client_secretKey == client_secretKey:
        api_result=False
        # return False
    api_result=True
    log_process_result(_api_msgID, api_result, data_name='application_credentials_are_valid', **_process_identity_dict)
    return api_result
#::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
def dbapi_application_api(dbsession, action, input_dict, filter_dict={}, caller_dict={}, call_level=-1,debug_level=-1):
    _api_name = "dbapi_application_api"
    _api_entity = 'APPLICATION_API'
    _api_action = action
    _api_msgID = set_api_msgID(_api_name, _api_action, _api_entity)    
    _api_debug_level = set_api_debug_level(_api_name, debug_level,dbsession)
    _api_level = call_level + 1
    _api_session_id = dbsession.session_id
    _api_indent_level=_api_level
    _api_indent_method='AUTO'

    _process_identity_dict = set_process_identity_dict('api', _api_name, _api_action, _api_entity, _api_msgID, _api_msgID, _api_session_id, _api_debug_level, print_enabled, filelog_enabled, log_file, errors_file, debug_file, _api_indent_level, _api_indent_method)
    _process_call_area = set_process_caller_area(_process_identity_dict, caller_dict)

    log_process_start(_api_msgID,**_process_identity_dict)

    log_process_input('', 'input_dict', input_dict,**_process_identity_dict)
    log_process_input('', 'filter_dict', filter_dict,**_process_identity_dict)
    log_process_input('', 'caller_dict', caller_dict,**_process_identity_dict)

    action_result = dbsession.table_action(dbmodel.APPLICATION_API, action , input_dict, filter_dict, caller_dict={}, api_name=_api_name, api_entity=_api_entity, auto_commit=True, call_level=_api_level, debug_level=_api_debug_level-1)
    api_result = action_result
    api_result.update({'api_action': _api_action, 'api_name': _api_name})
    
    log_process_finish(_api_msgID, api_result, **_process_identity_dict)    
    return api_result
#::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
def dbapi_token(dbsession, action, input_dict, filter_dict={}, caller_dict={}, call_level=-1,debug_level=-1):
    _api_name = "dbapi_token"
    _api_entity = 'TOKEN'
    _api_action = action
    _api_msgID = set_api_msgID(_api_name, _api_action, _api_entity)    
    _api_debug_level = set_api_debug_level(_api_name, debug_level,dbsession)
    _api_level = call_level + 1
    _api_session_id = dbsession.session_id
    _api_indent_level=_api_level
    _api_indent_method='AUTO'

    _process_identity_dict = set_process_identity_dict('api', _api_name, _api_action, _api_entity, _api_msgID, _api_msgID, _api_session_id, _api_debug_level, print_enabled, filelog_enabled, log_file, errors_file, debug_file, _api_indent_level, _api_indent_method)
    _process_call_area = set_process_caller_area(_process_identity_dict, caller_dict)

    log_process_start(_api_msgID,**_process_identity_dict)

    log_process_input('', 'input_dict', input_dict,**_process_identity_dict)
    log_process_input('', 'filter_dict', filter_dict,**_process_identity_dict)
    log_process_input('', 'caller_dict', caller_dict,**_process_identity_dict)

    action_result = dbsession.table_action(dbmodel.TOKEN, action , input_dict, filter_dict, caller_dict={}, api_name=_api_name, api_entity=_api_entity, auto_commit=True, call_level=_api_level, debug_level=_api_debug_level-1)
    api_result = action_result
    api_result.update({'api_action': _api_action, 'api_name': _api_name})
    
    log_process_finish(_api_msgID, api_result, **_process_identity_dict)    
    return api_result
#::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
def dbapi_token_is_valid(dbsession, token, caller_dict={}, call_level=-1,debug_level=-1):
    _api_name = "dbapi_token_is_valid"
    _api_entity = 'TOKEN'
    _api_action = 'validation'    
    _api_msgID = set_api_msgID(_api_name, _api_action, _api_entity)    
    _api_debug_level = set_api_debug_level(_api_name, debug_level,dbsession)
    _api_level = call_level + 1
    _api_session_id = dbsession.session_id
    _api_indent_level=_api_level
    _api_indent_method='AUTO'

    _process_identity_dict = set_process_identity_dict('api', _api_name, _api_action, _api_entity, _api_msgID, _api_msgID, _api_session_id, _api_debug_level, print_enabled, filelog_enabled, log_file, errors_file, debug_file, _api_indent_level, _api_indent_method)
    _process_call_area = set_process_caller_area(_process_identity_dict, caller_dict)

    log_process_start(_api_msgID,**_process_identity_dict)

    log_process_input('', 'token', token,**_process_identity_dict)
    log_process_input('', 'caller_dict', caller_dict,**_process_identity_dict)

    if type(token) == type(''):
        input_dict = {'token': token}
    elif type(token) == type({}):
        input_dict = token
    else:
        msg='invalid token provided'
        log_process_message('', 'error', msg, **_process_identity_dict)
        return False

    if not input_dict.get('token'):
        msg='no token provided'
        log_process_message('', 'error', msg, **_process_identity_dict)
        return False

    token_record = dbsession.get(dbmodel.TOKEN, input_dict)
        
    if not token_record:
        msg = f'access token is NOT valid.(not found)'
        log_process_message('', 'error', msg, **_process_identity_dict)
        return False

    expiryDT = token_record.expiryDT
    if not expiryDT:
        msg = f'access token is NOT valid.(no expiryDT)'
        log_process_message('', 'error', msg, **_process_identity_dict)
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
    log_process_result(_api_msgID, api_result, data_name='access_token_is_valid', **_process_identity_dict)
    return api_result
#::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
def dbapi_token_get_access_token(dbsession, token_request, caller_dict={}, call_level=-1,debug_level=-1):
    _api_name = "dbapi_token_get_access_token"
    _api_entity = 'TOKEN'
    _api_action = 'GET_TOKEN'
    _api_msgID = set_api_msgID(_api_name, _api_action, _api_entity)    
    _api_debug_level = set_api_debug_level(_api_name, debug_level,dbsession)
    _api_level = call_level + 1
    _api_session_id = dbsession.session_id
    _api_indent_level=_api_level
    _api_indent_method='AUTO'

    _process_identity_dict = set_process_identity_dict('api', _api_name, _api_action, _api_entity, _api_msgID, _api_msgID, _api_session_id, _api_debug_level, print_enabled, filelog_enabled, log_file, errors_file, debug_file, _api_indent_level, _api_indent_method)
    _process_call_area = set_process_caller_area(_process_identity_dict, caller_dict)

    log_process_start(_api_msgID,**_process_identity_dict)

    log_process_input('', 'token_request', token_request,**_process_identity_dict)
    log_process_input('', 'caller_dict', caller_dict,**_process_identity_dict)

    application_name=token_request.get('application_name')
    client_id=token_request.get('application_client_id')
    client_secretKey=token_request.get('application_client_secretKey')
    application = dbsession.get(dbmodel.APPLICATION, {'application_name': application_name, 'client_id': client_id})
    if not application:
        msg='application not registered'
        api_result={'api_status': 'error', 'api_message': msg,'api_data':{}}
        log_process_finish(_api_msgID, api_result, **_process_identity_dict)    
        return api_result
    if not application.client_id == client_id or not application.client_secretKey == client_secretKey:
        msg='application credentials not valid'
        api_result={'api_status': 'error', 'api_message': msg,'api_data':{}}
        log_process_finish(_api_msgID, api_result, **_process_identity_dict)    
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
    token = dbsession.insert(dbmodel.TOKEN, token_request,auto_commit=True)
    if not token:
        msg='token generation failed'
        api_result={'api_status': 'system error', 'api_message': msg,'api_data':{}}
        log_process_finish(_api_msgID, api_result, **_process_identity_dict)    
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

    log_process_finish(_api_msgID, api_result, **_process_identity_dict)    
    return api_result
#::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
def dbapi_cleanup_tokens(dbsession, caller_dict={}, call_level=-1,debug_level=-1):
    _api_name = "debapi_cleanup_tokens"
    _api_entity = 'TOKEN'
    _api_action = 'CLEANUP'
    _api_msgID = set_api_msgID(_api_name, _api_action, _api_entity)    
    _api_debug_level = set_api_debug_level(_api_name, debug_level,dbsession)
    _api_level = call_level + 1
    _api_session_id = dbsession.session_id
    _api_indent_level=_api_level
    _api_indent_method='AUTO'

    _process_identity_dict = set_process_identity_dict('api', _api_name, _api_action, _api_entity, _api_msgID, _api_msgID, _api_session_id, _api_debug_level, print_enabled, filelog_enabled, log_file, errors_file, debug_file, _api_indent_level, _api_indent_method)
    _process_call_area = set_process_caller_area(_process_identity_dict, caller_dict)

    log_process_start(_api_msgID,**_process_identity_dict)

    where_expression = {'status': 'Expired'}
    deleted_result = dbsession.delete_rows(dbmodel.TOKEN, where_expression, auto_commit=True)
    deleted_rows = deleted_result.get('rows_deleted', 0)

    #nowString = datetime.datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S')
    #where_expression = f"expiryDT<'{datetime.datetime.utcnow()}'"
    where_expression = {'expiryDT': {datetime.datetime.utcnow()}}
    update_dict = {'status': 'Expired'}
    expired_result = dbsession.update_rows(dbmodel.TOKEN, update_dict,where_expression, auto_commit=True)
    expired_rows = expired_result.get('rows_updated', 0)

    msg = f'tokens cleaned with {expired_rows} tokens expired, {deleted_rows} removed.'

    api_result = {'api_status': 'success', 'api_message': msg, 'rows_expired': expired_rows, 'rows_removed': deleted_rows}
    log_process_finish(_api_msgID, api_result, **_process_identity_dict)    
    return api_result
#::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
def dbapi_service_provider(dbsession, action, input_dict, filter_dict={}, caller_dict={}, call_level=-1,debug_level=-1):
    _api_name = "dbapi_service_provider"
    _api_entity = 'SERVICE_PROVIDER'
    _api_action = action
    _api_msgID = set_api_msgID(_api_name, _api_action, _api_entity)    
    _api_debug_level = set_api_debug_level(_api_name, debug_level,dbsession)
    _api_level = call_level + 1
    _api_session_id = dbsession.session_id
    _api_indent_level=_api_level
    _api_indent_method='AUTO'

    _process_identity_dict = set_process_identity_dict('api', _api_name, _api_action, _api_entity, _api_msgID, _api_msgID, _api_session_id, _api_debug_level, print_enabled, filelog_enabled, log_file, errors_file, debug_file, _api_indent_level, _api_indent_method)
    _process_call_area = set_process_caller_area(_process_identity_dict, caller_dict)

    log_process_start(_api_msgID,**_process_identity_dict)

    log_process_input('', 'input_dict', input_dict,**_process_identity_dict)
    log_process_input('', 'filter_dict', filter_dict,**_process_identity_dict)
    log_process_input('', 'caller_dict', caller_dict,**_process_identity_dict)

    input_dict.update({'client_type': 'service_provider'})

    if action.upper() in ('REGISTER','ADD','REFRESH'):
        action='REFRESH'
        action_result = dbsession.table_action(dbmodel.CLIENT, action, input_dict,  filter_dict, _api_name, _api_entity,auto_commit=True,call_level=_api_level, debug_level=_api_debug_level-1)
        api_result = action_result
        api_result.update({'api_action': _api_action, 'api_name': _api_name})
        thismsg=action_result.get('api_message')
        if not api_result.get('api_status') == 'success':
            # msg = f"service provider not registered"
            # api_result.update({'api_message':msg})
            log_process_finish(_api_msgID, api_result, **_process_identity_dict)    
            return api_result
        client = api_result.get('api_data')
        client_id = client.get('client_id')
        input_dict.update({'client_id': client_id})
    elif action.upper() in ('CONFIRM', 'ACTIVATE', 'DEACTIVATE', 'DELETE'):
        service_provider_dict = dbsession.get(dbmodel.SERVICE_PROVIDER, input_dict, 'DICT')
        if not service_provider_dict:
            msg = f'service provider not found'
            action_status='error'
            api_result = {'api_status': action_status, 'api_message': msg, 'api_data': input_dict, 'api_action': _api_action.upper(), 'api_name': _api_name}
            log_process_finish(_api_msgID, api_result, **_process_identity_dict)    
            return api_result

        service_provider = dbsession.get(dbmodel.SERVICE_PROVIDER, input_dict)
        client_id = service_provider.client_id
        email = service_provider.email
        client=dbsession.get(dbmodel.CLIENT, {'email':email})
        
        client_dict=dbsession.get(dbmodel.CLIENT, service_provider_dict,'DICT' )
        if not client_dict:
            msg = f'client not found'
            action_status='error'
            api_result = {'api_status': action_status, 'api_message': msg, 'api_data': service_provider_dict, 'api_action': _api_action.upper(), 'api_name': _api_name}
            log_process_finish(_api_msgID, api_result, **_process_identity_dict)    
            return api_result

        #action='CONFIRM'
        action_result = dbsession.table_action(dbmodel.CLIENT, action, input_dict,  filter_dict, _api_name, _api_entity,auto_commit=True,call_level=_api_level, debug_level=_api_debug_level-1)
        api_result = action_result
        api_result.update({'api_action': _api_action, 'api_name': _api_name})
        thismsg=action_result.get('api_message')
        if not api_result.get('api_status') == 'success':
            # msg = f'client confirmation failed'
            # api_result.update({'api_message':msg})
            log_process_finish(_api_msgID, api_result, **_process_identity_dict)    
            return api_result
        service_provider_dict = dbsession.get(dbmodel.SERVICE_PROVIDER, service_provider_dict, 'DICT')
        status=service_provider_dict.get('status')
        client_id=service_provider_dict.get('client_id')
        # if not service_provider_dict.get('status') == 'Active':
        #     msg = f"service provider not confirmed. status={status}"
        #     action_status='error'
        #     api_result = {'api_status': action_status, 'api_message': msg, 'api_data': service_provider_dict, 'messages': messages, 'rows_added': rows_added, 'rows_updated': rows_updated, 'api_action': _api_action.upper(), 'api_name': _api_name}
        #     log_process_finish(_api_msgID, api_result, **_process_identity_dict)    
        #     return api_result
        input_dict.update({'status': status})
        input_dict.update({'client_id': client_id})
    
    action_result = dbsession.table_action(dbmodel.SERVICE_PROVIDER, action, input_dict,  filter_dict, _api_name, _api_entity,auto_commit=True,call_level=_api_level, debug_level=_api_debug_level-1)
    api_result = action_result
    thismsg=thismsg.replace('CLIENT',_api_entity)
    api_result.update({'api_action': _api_action, 'api_name': _api_name,'api_message':thismsg})
    
    log_process_finish(_api_msgID, api_result, **_process_identity_dict)    
    return api_result
#::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
def dbapi_user(dbsession, action, input_dict, filter_dict={}, caller_dict={}, call_level=-1,debug_level=-1):
    _api_name = "dbapi_user"
    _api_entity = 'USER'
    _api_action = action
    _api_msgID = set_api_msgID(_api_name, _api_action, _api_entity)    
    _api_debug_level = set_api_debug_level(_api_name, debug_level,dbsession)
    _api_level = call_level + 1
    _api_session_id = dbsession.session_id
    _api_indent_level=_api_level
    _api_indent_method='AUTO'

    _process_identity_dict = set_process_identity_dict('api', _api_name, _api_action, _api_entity, _api_msgID, _api_msgID, _api_session_id, _api_debug_level, print_enabled, filelog_enabled, log_file, errors_file, debug_file, _api_indent_level, _api_indent_method)
    _process_call_area = set_process_caller_area(_process_identity_dict, caller_dict)

    log_process_start(_api_msgID,**_process_identity_dict)

    log_process_input('', 'input_dict', input_dict,**_process_identity_dict)
    log_process_input('', 'filter_dict', filter_dict,**_process_identity_dict)
    log_process_input('', 'caller_dict', caller_dict,**_process_identity_dict)

    input_dict.update({'client_type': 'user'})

    if action.upper() in ('REGISTER','ADD','REFRESH'):
        action='REFRESH'
        action_result = dbsession.table_action(dbmodel.CLIENT, action, input_dict,  filter_dict, _api_name, _api_entity,auto_commit=True,call_level=_api_level, debug_level=_api_debug_level-1)
        api_result = action_result
        api_result.update({'api_action': _api_action, 'api_name': _api_name})
        thismsg=action_result.get('api_message')
        if not api_result.get('api_status') == 'success':
            # msg = f"service provider not registered"
            # api_result.update({'api_message':msg})
            log_process_finish(_api_msgID, api_result, **_process_identity_dict)    
            return api_result
        client = api_result.get('api_data')
        client_id = client.get('client_id')
        input_dict.update({'client_id': client_id})
    elif action.upper() in ('CONFIRM', 'ACTIVATE', 'DEACTIVATE', 'DELETE'):
        service_provider_dict = dbsession.get(dbmodel.SERVICE_PROVIDER, input_dict, 'DICT')
        if not service_provider_dict:
            msg = f'service provider not found'
            action_status='error'
            api_result = {'api_status': action_status, 'api_message': msg, 'api_data': input_dict, 'api_action': _api_action.upper(), 'api_name': _api_name}
            log_process_finish(_api_msgID, api_result, **_process_identity_dict)    
            return api_result
        client_dict=dbsession.get(dbmodel.CLIENT, service_provider_dict,'DICT' )
        if not client_dict:
            msg = f'client not found'
            action_status='error'
            api_result = {'api_status': action_status, 'api_message': msg, 'api_data': service_provider_dict, 'api_action': _api_action.upper(), 'api_name': _api_name}
            log_process_finish(_api_msgID, api_result, **_process_identity_dict)    
            return api_result

        #action='CONFIRM'
        action_result = dbsession.table_action(dbmodel.CLIENT, action, input_dict,  filter_dict, _api_name, _api_entity,auto_commit=True,call_level=_api_level, debug_level=_api_debug_level-1)
        api_result = action_result
        api_result.update({'api_action': _api_action, 'api_name': _api_name})
        thismsg=action_result.get('api_message')
        if not api_result.get('api_status') == 'success':
            # msg = f'client confirmation failed'
            # api_result.update({'api_message':msg})
            log_process_finish(_api_msgID, api_result, **_process_identity_dict)    
            return api_result
        service_provider_dict = dbsession.get(dbmodel.SERVICE_PROVIDER, service_provider_dict, 'DICT')
        status=service_provider_dict.get('status')
        client_id=service_provider_dict.get('client_id')
        # if not service_provider_dict.get('status') == 'Active':
        #     msg = f"service provider not confirmed. status={status}"
        #     action_status='error'
        #     api_result = {'api_status': action_status, 'api_message': msg, 'api_data': service_provider_dict, 'messages': messages, 'rows_added': rows_added, 'rows_updated': rows_updated, 'api_action': _api_action.upper(), 'api_name': _api_name}
        #     log_process_finish(_api_msgID, api_result, **_process_identity_dict)    
        #     return api_result
        input_dict.update({'status': status})
        input_dict.update({'client_id': client_id})
    
    action_result = dbsession.table_action(dbmodel.SERVICE_PROVIDER, action, input_dict,  filter_dict, _api_name, _api_entity,auto_commit=True,call_level=_api_level, debug_level=_api_debug_level-1)
    api_result = action_result
    thismsg=thismsg.replace('CLIENT',_api_entity)
    api_result.update({'api_action': _api_action, 'api_name': _api_name,'api_message':thismsg})
    
    log_process_finish(_api_msgID, api_result, **_process_identity_dict)    
    return api_result
#::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
def dbapi_consumer(dbsession, action, input_dict, filter_dict={}, caller_dict={}, call_level=-1,debug_level=-1):
    _api_name = "dbapi_consumer"
    _api_entity = 'CONSUMER'
    _api_action = action
    _api_msgID = set_api_msgID(_api_name, _api_action, _api_entity)    
    _api_debug_level = set_api_debug_level(_api_name, debug_level,dbsession)
    _api_level = call_level + 1
    _api_session_id = dbsession.session_id
    _api_indent_level=_api_level
    _api_indent_method='AUTO'

    _process_identity_dict = set_process_identity_dict('api', _api_name, _api_action, _api_entity, _api_msgID, _api_msgID, _api_session_id, _api_debug_level, print_enabled, filelog_enabled, log_file, errors_file, debug_file, _api_indent_level, _api_indent_method)
    _process_call_area = set_process_caller_area(_process_identity_dict, caller_dict)

    log_process_start(_api_msgID,**_process_identity_dict)

    log_process_input('', 'input_dict', input_dict,**_process_identity_dict)
    log_process_input('', 'filter_dict', filter_dict,**_process_identity_dict)
    log_process_input('', 'caller_dict', caller_dict,**_process_identity_dict)

    input_dict.update({'client_type': 'consumer'})

    if action.upper() in ('REGISTER','ADD','REFRESH'):
        action='REFRESH'
        action_result = dbsession.table_action(dbmodel.CLIENT, action, input_dict,  filter_dict, _api_name, _api_entity,auto_commit=True,call_level=_api_level, debug_level=_api_debug_level-1)
        api_result = action_result
        thismsg=action_result.get('api_message')
        api_result.update({'api_action': _api_action, 'api_name': _api_name})
        if not api_result.get('api_status') == 'success':
            # msg = f"consumer not registered"
            # api_result.update({'api_message':msg})
            log_process_finish(_api_msgID, api_result, **_process_identity_dict)    
            return api_result
        client = api_result.get('api_data')
        client_id = client.get('client_id')
        input_dict.update({'client_id': client_id})
    elif action.upper() in ('CONFIRM', 'ACTIVATE', 'DEACTIVATE', 'DELETE'):
        consumer_dict = dbsession.get(dbmodel.CONSUMER, input_dict, 'DICT')
        if not consumer_dict:
            msg = f'consumer not found'
            action_status='error'
            api_result = {'api_status': action_status, 'api_message': msg, 'api_data': input_dict, 'api_action': _api_action.upper(), 'api_name': _api_name}
            log_process_finish(_api_msgID, api_result, **_process_identity_dict)    
            return api_result
        client_dict=dbsession.get(dbmodel.CLIENT, consumer_dict,'DICT' )
        if not client_dict:
            msg = f'client not found'
            action_status='error'
            api_result = {'api_status': action_status, 'api_message': msg, 'api_data': consumer_dict, 'api_action': _api_action.upper(), 'api_name': _api_name}
            log_process_finish(_api_msgID, api_result, **_process_identity_dict)    
            return api_result

        #action='CONFIRM'
        action_result = dbsession.table_action(dbmodel.CLIENT, action, input_dict,  filter_dict, _api_name, _api_entity,auto_commit=True,call_level=_api_level, debug_level=_api_debug_level-1)
        api_result = action_result
        api_result.update({'api_action': _api_action, 'api_name': _api_name})
        thismsg=action_result.get('api_message')
        if not api_result.get('api_status') == 'success':
            # msg = f'client confirmation failed'
            # api_result.update({'api_message':msg})
            log_process_finish(_api_msgID, api_result, **_process_identity_dict)    
            return api_result
        consumer_dict = dbsession.get(dbmodel.CONSUMER, consumer_dict, 'DICT')
        status=consumer_dict.get('status')
        client_id=consumer_dict.get('client_id')
        # if not consumer_dict.get('status') == 'Active':
        #     msg = f"service provider not confirmed. status={status}"
        #     action_status='error'
        #     api_result = {'api_status': action_status, 'api_message': msg, 'api_data': consumer_dict, 'messages': messages, 'rows_added': rows_added, 'rows_updated': rows_updated, 'api_action': _api_action.upper(), 'api_name': _api_name}
        #     log_process_finish(_api_msgID, api_result, **_process_identity_dict)    
        #     return api_result
        input_dict.update({'status': status})
        input_dict.update({'client_id': client_id})
    
    action_result = dbsession.table_action(dbmodel.CONSUMER, action, input_dict,  filter_dict, _api_name, _api_entity,auto_commit=True,call_level=_api_level, debug_level=_api_debug_level-1)
    api_result = action_result
    thismsg=thismsg.replace('CLIENT',_api_entity)
    api_result.update({'api_action': _api_action, 'api_name': _api_name,'api_message':thismsg})
    
    log_process_finish(_api_msgID, api_result, **_process_identity_dict)    
    return api_result
#::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
def dbapi_merchant(dbsession, action, input_dict, filter_dict={}, caller_dict={}, call_level=-1,debug_level=-1):
    _api_name = "dbapi_merchant"
    _api_entity = 'MERCHANT'
    _api_action = action
    _api_msgID = set_api_msgID(_api_name, _api_action, _api_entity)    
    _api_debug_level = set_api_debug_level(_api_name, debug_level,dbsession)
    _api_level = call_level + 1
    _api_session_id = dbsession.session_id
    _api_indent_level=_api_level
    _api_indent_method='AUTO'

    _process_identity_dict = set_process_identity_dict('api', _api_name, _api_action, _api_entity, _api_msgID, _api_msgID, _api_session_id, _api_debug_level, print_enabled, filelog_enabled, log_file, errors_file, debug_file, _api_indent_level, _api_indent_method)
    _process_call_area = set_process_caller_area(_process_identity_dict, caller_dict)

    log_process_start(_api_msgID,**_process_identity_dict)

    if (action.upper().find('BANKACCOUNT') >= 0 and action.upper().find('GET') >= 0) or action.upper() in ('BANKACCOUNTS', 'BANKACCOUNT'):
        return dbapi_merchant_get_bankaccounts(dbsession, input_dict, filter_dict, caller_dict, call_level=_api_level-1)
    elif action.upper().find('BANKACCOUNT') >= 0 and action.upper().find('REGISTER') >= 0:
        return dbapi_merchant_bankaccount_register(dbsession, input_dict, filter_dict, caller_dict, call_level=_api_level-1)


    log_process_input('', 'input_dict', input_dict,**_process_identity_dict)
    log_process_input('', 'filter_dict', filter_dict,**_process_identity_dict)
    log_process_input('', 'caller_dict', caller_dict,**_process_identity_dict)

    input_dict.update({'client_type': 'merchant'})

    if action.upper() in ('REGISTER','ADD','REFRESH'):
        action='REFRESH'
        action_result = dbsession.table_action(dbmodel.CLIENT, action, input_dict,  filter_dict, _api_name, _api_entity,auto_commit=True,call_level=_api_level, debug_level=_api_debug_level-1)
        api_result = action_result
        api_result.update({'api_action': _api_action, 'api_name': _api_name})
        thismsg=action_result.get('api_message')
        if not api_result.get('api_status') == 'success':
            log_process_finish(_api_msgID, api_result, **_process_identity_dict)    
            return api_result
        client = api_result.get('api_data')
        client_id = client.get('client_id')
        input_dict.update({'client_id': client_id})
    elif action.upper() in ('CONFIRM', 'ACTIVATE', 'DEACTIVATE', 'DELETE'):
        merchant_dict = dbsession.get(dbmodel.MERCHANT, input_dict, 'DICT')
        if not merchant_dict:
            msg = f'merchant not found'
            action_status='error'
            api_result = {'api_status': action_status, 'api_message': msg, 'api_data': input_dict, 'api_action': _api_action.upper(), 'api_name': _api_name}
            log_process_finish(_api_msgID, api_result, **_process_identity_dict)    
            return api_result
        client_dict=dbsession.get(dbmodel.CLIENT, merchant_dict,'DICT' )
        if not client_dict:
            msg = f'client not found'
            action_status='error'
            api_result = {'api_status': action_status, 'api_message': msg, 'api_data': merchant_dict, 'api_action': _api_action.upper(), 'api_name': _api_name}
            log_process_finish(_api_msgID, api_result, **_process_identity_dict)    
            return api_result

        #action='CONFIRM'
        action_result = dbsession.table_action(dbmodel.CLIENT, action, input_dict,  filter_dict, _api_name, _api_entity,auto_commit=True,call_level=_api_level, debug_level=_api_debug_level-1)
        api_result = action_result
        api_result.update({'api_action': _api_action, 'api_name': _api_name})
        thismsg=action_result.get('api_message')
        # api_result = dbapi_client_confirm(client_dict)
        if not api_result.get('api_status') == 'success':
            # msg = f'client confirmation failed'
            # api_result.update({'api_message':msg})
            log_process_finish(_api_msgID, api_result, **_process_identity_dict)    
            return api_result
        merchant_dict = dbsession.get(dbmodel.MERCHANT, merchant_dict, 'DICT')
        status=merchant_dict.get('status')
        client_id=merchant_dict.get('client_id')
        # if not merchant_dict.get('status') == 'Active':
        #     msg = f"service provider not confirmed. status={status}"
        #     action_status='error'
        #     api_result = {'api_status': action_status, 'api_message': msg, 'api_data': merchant_dict, 'messages': messages, 'rows_added': rows_added, 'rows_updated': rows_updated, 'api_action': _api_action.upper(), 'api_name': _api_name}
        #     log_process_finish(_api_msgID, api_result, **_process_identity_dict)    
        #     return api_result
        input_dict.update({'status': status})
        input_dict.update({'client_id': client_id})
    
    action_result = dbsession.table_action(dbmodel.MERCHANT, action, input_dict,  filter_dict, _api_name, _api_entity,auto_commit=True,call_level=_api_level, debug_level=_api_debug_level-1)
    api_result = action_result
    thismsg=thismsg.replace('CLIENT',_api_entity)
    api_result.update({'api_action': _api_action, 'api_name': _api_name,'api_message':thismsg})
    
    log_process_finish(_api_msgID, api_result, **_process_identity_dict)    
    return api_result
#::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
def dbapi_merchant_pointofsale(dbsession, action, input_dict, filter_dict={}, caller_dict={}, call_level=-1,debug_level=-1):
    _api_name = "dbapi_merchant_pointofsale"
    _api_entity = 'POINT_OF_SALE'
    _api_action = action
    _api_msgID = set_api_msgID(_api_name, _api_action, _api_entity)    
    _api_debug_level = set_api_debug_level(_api_name, debug_level,dbsession)
    _api_level = call_level + 1
    _api_session_id = dbsession.session_id
    _api_indent_level=_api_level
    _api_indent_method='AUTO'

    _process_identity_dict = set_process_identity_dict('api', _api_name, _api_action, _api_entity, _api_msgID, _api_msgID, _api_session_id, _api_debug_level, print_enabled, filelog_enabled, log_file, errors_file, debug_file, _api_indent_level, _api_indent_method)
    _process_call_area = set_process_caller_area(_process_identity_dict, caller_dict)

    log_process_start(_api_msgID,**_process_identity_dict)

    if action.upper().find('BANKACCOUNT') >= 0 and (action.upper().find('ADD') >= 0 or action.upper().find('REGISTER') >= 0):
        return dbapi_pointofsale_bankaccount_remove(dbsession, input_dict, filter_dict, caller_dict, call_level=_api_level-1)
    elif action.upper().find('BANKACCOUNT') >= 0 and (action.upper().find('REMOVE') >= 0 or action.upper().find('DELETE') >= 0):
        return dbapi_pointofsale_bankaccount_add(dbsession, input_dict, filter_dict, caller_dict, call_level=_api_level-1)

    log_process_input('', 'input_dict', input_dict,**_process_identity_dict)
    log_process_input('', 'filter_dict', filter_dict,**_process_identity_dict)
    log_process_input('', 'caller_dict', caller_dict,**_process_identity_dict)

    action_result = dbsession.table_action(dbmodel.POINT_OF_SALE, action , input_dict, filter_dict, caller_dict={}, api_name=_api_name, api_entity=_api_entity, auto_commit=True, call_level=_api_level, debug_level=_api_debug_level-1)
    api_result = action_result
    api_result.update({'api_action': _api_action, 'api_name': _api_name})
    
    log_process_finish(_api_msgID, api_result, **_process_identity_dict)    
    return api_result
#::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
def dbapi_merchant_employee(dbsession, action, input_dict, filter_dict={}, caller_dict={}, call_level=-1,debug_level=-1):
    _api_name = "dbapi_merchant_employee"
    _api_entity = 'MERCHANT_EMPLOYEE'
    _api_action = action
    _api_msgID = set_api_msgID(_api_name, _api_action, _api_entity)    
    _api_debug_level = set_api_debug_level(_api_name, debug_level,dbsession)
    _api_level = call_level + 1
    _api_session_id = dbsession.session_id
    _api_indent_level=_api_level
    _api_indent_method='AUTO'

    _process_identity_dict = set_process_identity_dict('api', _api_name, _api_action, _api_entity, _api_msgID, _api_msgID, _api_session_id, _api_debug_level, print_enabled, filelog_enabled, log_file, errors_file, debug_file, _api_indent_level, _api_indent_method)
    _process_call_area = set_process_caller_area(_process_identity_dict, caller_dict)

    log_process_start(_api_msgID,**_process_identity_dict)

    log_process_input('', 'input_dict', input_dict,**_process_identity_dict)
    log_process_input('', 'filter_dict', filter_dict,**_process_identity_dict)
    log_process_input('', 'caller_dict', caller_dict,**_process_identity_dict)

    if action.upper() in ('REGISTER', 'ADD', 'REFRESH'):
        if not input_dict.get('status'):
            input_dict.update({'status': 'Active'})
        
    action_result = dbsession.table_action(dbmodel.MERCHANT_EMPLOYEE, action , input_dict, filter_dict, caller_dict={}, api_name=_api_name, api_entity=_api_entity, auto_commit=True, call_level=_api_level, debug_level=_api_debug_level-1)
    api_result = action_result
    api_result.update({'api_action': _api_action, 'api_name': _api_name})
    
    log_process_finish(_api_msgID, api_result, **_process_identity_dict)    
    return api_result
#::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
def dbapi_merchant_get_bankaccounts(dbsession, merchant_record, filter_dict={}, caller_dict={}, call_level=-1,debug_level=-1):
    _api_name = "dbapi_merchant_get_bankaccounts"
    _api_entity = 'MERCHANT'
    _api_action = 'get_bank_accounts'
    _api_msgID = set_api_msgID(_api_name, _api_action, _api_entity)    
    _api_debug_level = set_api_debug_level(_api_name, debug_level,dbsession)
    _api_level = call_level + 1
    _api_session_id = dbsession.session_id
    _api_indent_level=_api_level
    _api_indent_method='AUTO'

    _process_identity_dict = set_process_identity_dict('api', _api_name, _api_action, _api_entity, _api_msgID, _api_msgID, _api_session_id, _api_debug_level, print_enabled, filelog_enabled, log_file, errors_file, debug_file, _api_indent_level, _api_indent_method)
    _process_call_area = set_process_caller_area(_process_identity_dict, caller_dict)

    log_process_start(_api_msgID,**_process_identity_dict)

    log_process_input('', 'input_dict', bankaccount_record,**_process_identity_dict)
    log_process_input('', 'filter_dict', filter_dict,**_process_identity_dict)
    log_process_input('', 'caller_dict', caller_dict,**_process_identity_dict)

    merchant = dbsession.get(dbmodel.POINT_OF_SALE, merchant_record, call_level=_api_level, debug_level=_api_debug_level-1)
    if not merchant:
        msg = f'merchant not found'
        log_process_message('', 'error', msg, **_process_identity_dict)
        api_result = {'api_status': 'error', 'api_message': msg, 'api_action': _api_action.upper(), 'api_name': _api_name}
        log_process_finish(_api_msgID, api_result, **_process_identity_dict)
        return api_result
    
    if not merchant.status == 'Active':
        msg = f"merchant not Active.(status:{merchant.status)})"
        log_process_message('', 'error', msg, **_process_identity_dict)
        api_result = {'api_status': 'error', 'api_message': msg, 'api_action': _api_action.upper(), 'api_name': _api_name}
        log_process_finish(_api_msgID, api_result, **_process_identity_dict)
        return api_result

    client_id = merchant.client_id

    merchant_accounts=[]
    filterJson = {"client_id": client_id, "status": 'Active'}
    bank_accounts=dbsession.get_rows(dbmodel.BANK_ACCOUNT, filterJson, call_level=_api_level, debug_level=_api_debug_level-1)
    if bank_accounts:
        msg = f'[{len(bank_accounts)} bank accounts found] for merchant [merchant.name] client_id [{client_id}]'
        log_process_message('', 'success', msg, **_process_identity_dict)
        for bank_account in bank_accounts:
            bank_account_id = bank_account.bank_account_id
            bank_accountID = bank_account.bank_accountID
            merchant_accounts.append(bank_account_id)

    msg = f'OK. [{len(merchant_accounts)} bank accounts]'
    api_result = {'api_status': 'success', 'api_message': msg, 'data_records': {len(merchant_accounts)}, 'api_data': bank_accounts, 'api_action': _api_action.upper(), 'api_name': _api_name}
    log_process_finish(_api_msgID, api_result, **_process_identity_dict)    
    return api_result
#::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
def dbapi_merchant_bankaccount_register(dbsession, bankaccount_record, filter_dict={}, caller_dict={}, call_level=-1,debug_level=-1):
    _api_name = "dbapi_merchant_bankaccount_register"
    _api_entity = 'MERCHANT'
    _api_action = 'register_bank_account'
    _api_msgID = set_api_msgID(_api_name, _api_action, _api_entity)    
    _api_debug_level = set_api_debug_level(_api_name, debug_level,dbsession)
    _api_level = call_level + 1
    _api_session_id = dbsession.session_id
    _api_indent_level=_api_level
    _api_indent_method='AUTO'

    _process_identity_dict = set_process_identity_dict('api', _api_name, _api_action, _api_entity, _api_msgID, _api_msgID, _api_session_id, _api_debug_level, print_enabled, filelog_enabled, log_file, errors_file, debug_file, _api_indent_level, _api_indent_method)
    _process_call_area = set_process_caller_area(_process_identity_dict, caller_dict)

    log_process_start(_api_msgID,**_process_identity_dict)

    log_process_input('', 'input_dict', bankaccount_record,**_process_identity_dict)
    log_process_input('', 'filter_dict', filter_dict,**_process_identity_dict)
    log_process_input('', 'caller_dict', caller_dict,**_process_identity_dict)

    merchant = dbsession.get(dbmodel.POINT_OF_SALE, bankaccount_record, call_level=_api_level, debug_level=_api_debug_level-1)
    if not merchant:
        msg = f'merchant not found'
        log_process_message('', 'error', msg, **_process_identity_dict)
        api_result = {'api_status': 'error', 'api_message': msg, 'api_action': _api_action.upper(), 'api_name': _api_name}
        log_process_finish(_api_msgID, api_result, **_process_identity_dict)
        return api_result
    
    if not merchant.status == 'Active':
        msg = f"merchant not Active.(status:{merchant.status)})"
        log_process_message('', 'error', msg, **_process_identity_dict)
        api_result = {'api_status': 'error', 'api_message': msg, 'api_action': _api_action.upper(), 'api_name': _api_name}
        log_process_finish(_api_msgID, api_result, **_process_identity_dict)
        return api_result

    bank_account_id=None
    account_id = bankaccount_record.get('bank_account_id')
    if account_id:
        bank_account_id = dbapi_get_bank_account_id(dbsession, account_id, caller_area={}, debug_level=-1)
    if not bank_account_id:
        account_id = bankaccount_record.get('bank_accountID')
        if account_id:
            bank_account_id = dbapi_get_bank_account_id(dbsession, account_id, caller_area={}, debug_level=-1)
    if not bank_account_id:
        account_id = bankaccount_record.get('bank_account')
        if account_id:
            bank_account_id = dbapi_get_bank_account_id(dbsession, account_id, caller_area={}, debug_level=-1)
    if not bank_account_id:
        msg = f"bank_account not found"
        log_process_message('', 'error', msg, **_process_identity_dict)
        api_result = {'api_status': 'error', 'api_message': msg, 'api_action': _api_action.upper(), 'api_name': _api_name}
        log_process_finish(_api_msgID, api_result, **_process_identity_dict)
        return api_result

    bankaccount_record.update({'bank_account_id':bank_account_id})
    bankaccount_record.update({'merchant_id':merchant.merchant_id})
    
    bank_account = dbsession.get(dbmodel.BANK_ACCOUNT, {'bank_account_id':bank_account_id}, call_level=_api_level, debug_level=_api_debug_level-1)
    if not bank_account:
        msg = f"bank account not found"
        log_process_message('', 'error', msg, **_process_identity_dict)
        api_result = {'api_status': 'error', 'api_message': msg, 'api_action': _api_action.upper(), 'api_name': _api_name}
        log_process_finish(_api_msgID, api_result, **_process_identity_dict)
        return api_result
    if not bank_account.status == 'Active':
        msg = f"bank account {bank_account_id} not Active (status:{bank_account.status})"
        log_process_message('', 'error', msg, **_process_identity_dict)
        api_result = {'api_status': 'error', 'api_message': msg, 'api_action': _api_action.upper(), 'api_name': _api_name}
        log_process_finish(_api_msgID, api_result, **_process_identity_dict)
        return api_result

    merchant_record = bank_account.to_dict()

    merchant_record.update({'merchant_id': merchant_id})

    api_result = dbsession.table_action(dbmodel.MERCHANT, 'UPDATE', merchant_record, filter_dict, caller_dict={}, api_name=_api_name, api_entity=_api_entity, auto_commit=True, call_level=_api_level,debug_level=_api_debug_level-1)
    api_result.update({'api_action': _api_action, 'api_name': _api_name})
        
    log_process_finish(_api_msgID, api_result, **_process_identity_dict)    

    return api_result
#::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
def dbapi_pointofsale_bankaccount_add(dbsession, bankaccount_record, filter_dict={}, caller_dict={}, call_level=-1,debug_level=-1):
    _api_name = "dbapi_pointofsale_bankaccount_add"
    _api_entity = 'POINT_OF_SALE'
    _api_action = 'add_bank_account'
    _api_msgID = set_api_msgID(_api_name, _api_action, _api_entity)    
    _api_debug_level = set_api_debug_level(_api_name, debug_level,dbsession)
    _api_level = call_level + 1
    _api_session_id = dbsession.session_id
    _api_indent_level=_api_level
    _api_indent_method='AUTO'

    _process_identity_dict = set_process_identity_dict('api', _api_name, _api_action, _api_entity, _api_msgID, _api_msgID, _api_session_id, _api_debug_level, print_enabled, filelog_enabled, log_file, errors_file, debug_file, _api_indent_level, _api_indent_method)
    _process_call_area = set_process_caller_area(_process_identity_dict, caller_dict)

    log_process_start(_api_msgID,**_process_identity_dict)

    log_process_input('', 'input_dict', bankaccount_record,**_process_identity_dict)
    log_process_input('', 'filter_dict', filter_dict,**_process_identity_dict)
    log_process_input('', 'caller_dict', caller_dict,**_process_identity_dict)

    pointofsale = dbsession.get(dbmodel.POINT_OF_SALE, bankaccount_record, call_level=_api_level, debug_level=_api_debug_level-1)
    if not pointofsale:
        msg = f'pointofsale not found'
        log_process_message('', 'error', msg, **_process_identity_dict)
        api_result = {'api_status': 'error', 'api_message': msg, 'api_action': _api_action.upper(), 'api_name': _api_name}
        log_process_finish(_api_msgID, api_result, **_process_identity_dict)
        return api_result
    
    if not pointofsale.status == 'Active':
        msg = f"pointofsale not Active.(status:{pointofsale.status)})"
        log_process_message('', 'error', msg, **_process_identity_dict)
        api_result = {'api_status': 'error', 'api_message': msg, 'api_action': _api_action.upper(), 'api_name': _api_name}
        log_process_finish(_api_msgID, api_result, **_process_identity_dict)
        return api_result

    bank_account_id=None
    account_id = bankaccount_record.get('bank_account_id')
    if account_id:
        bank_account_id = dbapi_get_bank_account_id(dbsession, account_id, caller_area={}, debug_level=-1)
    if not bank_account_id:
        account_id = bankaccount_record.get('bank_accountID')
        if account_id:
            bank_account_id = dbapi_get_bank_account_id(dbsession, account_id, caller_area={}, debug_level=-1)
    if not bank_account_id:
        account_id = bankaccount_record.get('bank_account')
        if account_id:
            bank_account_id = dbapi_get_bank_account_id(dbsession, account_id, caller_area={}, debug_level=-1)
    if not bank_account_id:
        msg = f"bank_account not found"
        log_process_message('', 'error', msg, **_process_identity_dict)
        api_result = {'api_status': 'error', 'api_message': msg, 'api_action': _api_action.upper(), 'api_name': _api_name}
        log_process_finish(_api_msgID, api_result, **_process_identity_dict)
        return api_result

    bankaccount_record.update({'bank_account_id':bank_account_id})
    bankaccount_record.update({'pointofsale_id':pointofsale.pointofsale_id})
    
    bank_account = dbsession.get(dbmodel.BANK_ACCOUNT, {'bank_account_id':bank_account_id}, call_level=_api_level, debug_level=_api_debug_level-1)
    if not bank_account:
        msg = f"bank account not found"
        log_process_message('', 'error', msg, **_process_identity_dict)
        api_result = {'api_status': 'error', 'api_message': msg, 'api_action': _api_action.upper(), 'api_name': _api_name}
        log_process_finish(_api_msgID, api_result, **_process_identity_dict)
        return api_result
    if not bank_account.status == 'Active':
        msg = f"bank account {bank_account_id} not Active (status:{bank_account.status})"
        log_process_message('', 'error', msg, **_process_identity_dict)
        api_result = {'api_status': 'error', 'api_message': msg, 'api_action': _api_action.upper(), 'api_name': _api_name}
        log_process_finish(_api_msgID, api_result, **_process_identity_dict)
        return api_result

    pointofsale_record = bank_account.to_dict()

    pointofsale_record.update({'pointofsale_id': pointofsale_id})

    api_result = dbsession.table_action(dbmodel.POINT_OF_SALE, 'UPDATE', pointofsale_record, filter_dict, caller_dict={}, api_name=_api_name, api_entity=_api_entity, auto_commit=True, call_level=_api_level,debug_level=_api_debug_level-1)
    api_result.update({'api_action': _api_action, 'api_name': _api_name})
        
    log_process_finish(_api_msgID, api_result, **_process_identity_dict)    

    return api_result
#::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
def dbapi_pointofsale_bankaccount_remove(dbsession, pointofsale_record, filter_dict={}, caller_dict={}, call_level=-1,debug_level=-1):
    _api_name = "dbapi_pointofsale_bankaccount_remove"
    _api_entity = 'POINT_OF_SALE'
    _api_action = 'remove_bank_account'
    _api_msgID = set_api_msgID(_api_name, _api_action, _api_entity)    
    _api_debug_level = set_api_debug_level(_api_name, debug_level,dbsession)
    _api_level = call_level + 1
    _api_session_id = dbsession.session_id
    _api_indent_level=_api_level
    _api_indent_method='AUTO'

    _process_identity_dict = set_process_identity_dict('api', _api_name, _api_action, _api_entity, _api_msgID, _api_msgID, _api_session_id, _api_debug_level, print_enabled, filelog_enabled, log_file, errors_file, debug_file, _api_indent_level, _api_indent_method)
    _process_call_area = set_process_caller_area(_process_identity_dict, caller_dict)

    log_process_start(_api_msgID,**_process_identity_dict)

    log_process_input('', 'input_dict', pointofsale_record,**_process_identity_dict)
    log_process_input('', 'filter_dict', filter_dict,**_process_identity_dict)
    log_process_input('', 'caller_dict', caller_dict,**_process_identity_dict)

    pointofsale = dbsession.get(dbmodel.POINT_OF_SALE, pointofsale_record, call_level=_api_level, debug_level=_api_debug_level-1)
    if not pointofsale:
        msg = f'pointofsale not found'
        log_process_message('', 'error', msg, **_process_identity_dict)
        api_result = {'api_status': 'error', 'api_message': msg, 'api_action': _api_action.upper(), 'api_name': _api_name}
        log_process_finish(_api_msgID, api_result, **_process_identity_dict)
        return api_result
    
    if not pointofsale.status == 'Active':
        msg = f"pointofsale not Active.(status:{pointofsale.status)})"
        log_process_message('', 'error', msg, **_process_identity_dict)
        api_result = {'api_status': 'error', 'api_message': msg, 'api_action': _api_action.upper(), 'api_name': _api_name}
        log_process_finish(_api_msgID, api_result, **_process_identity_dict)
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

    api_result = dbsession.table_action(dbmodel.POINT_OF_SALE, 'UPDATE', pointofsale_record, filter_dict, caller_dict={}, api_name=_api_name, api_entity=_api_entity, auto_commit=True, call_level=_api_level,debug_level=_api_debug_level-1)
    api_result.update({'api_action': _api_action, 'api_name': _api_name})
        
    log_process_finish(_api_msgID, api_result, **_process_identity_dict)    

    return api_result
#::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
def dbapi_pointofsale_credit_info(dbsession, pointofsale_record, filter_dict={}, caller_dict={}, call_level=-1,debug_level=-1):
    _api_name = "dbapi_pointofsale_bankaccount_add"
    _api_entity = 'POINT_OF_SALE'
    _api_action = 'add_bank_account'
    _api_msgID = set_api_msgID(_api_name, _api_action, _api_entity)    
    _api_debug_level = set_api_debug_level(_api_name, debug_level,dbsession)
    _api_level = call_level + 1
    _api_session_id = dbsession.session_id
    _api_indent_level=_api_level
    _api_indent_method='AUTO'

    _process_identity_dict = set_process_identity_dict('api', _api_name, _api_action, _api_entity, _api_msgID, _api_msgID, _api_session_id, _api_debug_level, print_enabled, filelog_enabled, log_file, errors_file, debug_file, _api_indent_level, _api_indent_method)
    _process_call_area = set_process_caller_area(_process_identity_dict, caller_dict)

    log_process_start(_api_msgID,**_process_identity_dict)

    log_process_input('', 'input_dict', pointofsale_record,**_process_identity_dict)
    log_process_input('', 'filter_dict', filter_dict,**_process_identity_dict)
    log_process_input('', 'caller_dict', caller_dict,**_process_identity_dict)

    pointofsale = dbsession.get(dbmodel.POINT_OF_SALE, pointofsale_record, call_level=_api_level, debug_level=_api_debug_level-1)
    if not pointofsale:
        msg = f'pointofsale not found'
        log_process_message('', 'error', msg, **_process_identity_dict)
        api_result = {'api_status': 'error', 'api_message': msg, 'api_action': _api_action.upper(), 'api_name': _api_name}
        log_process_finish(_api_msgID, api_result, **_process_identity_dict)
        return api_result
    
    if not pointofsale.status == 'Active':
        msg = f"pointofsale not Active.(status:{pointofsale.status)})"
        log_process_message('', 'error', msg, **_process_identity_dict)
        api_result = {'api_status': 'error', 'api_message': msg, 'api_action': _api_action.upper(), 'api_name': _api_name}
        log_process_finish(_api_msgID, api_result, **_process_identity_dict)
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
        merchant = dbsession.get(dbmodel.MERCHANT, {pointofsale_record}, call_level=_api_level, debug_level=_api_debug_level-1)
        bank_account_id = merchant.bank_account_id
        bank_subscription_id = merchant.bank_subscription_id
        bank_code = merchant.bank_code
        bank_subscriptionID = merchant.bank_subscriptionID
        bank_accountID = merchant.bank_accountID
        payments_currency = merchant.payments_currency
        x=' from merchant'

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
    log_process_message('', 'success', msg, **_process_identity_dict)
    api_result = {'api_status': 'success', 'api_message': msg, 'api_data':credit_info, 'api_action': _api_action.upper(), 'api_name': _api_name}
    log_process_finish(_api_msgID, api_result, **_process_identity_dict)
    return api_result
#::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
def dbapi_interaction(dbsession, action, input_dict, filter_dict={}, caller_dict={}, call_level=-1,debug_level=-1):
    _api_name = "dbapi_interaction"
    _api_entity = 'INTERACTION'
    _api_action = action
    _api_msgID = set_api_msgID(_api_name, _api_action, _api_entity)    
    _api_debug_level = set_api_debug_level(_api_name, debug_level,dbsession)
    _api_level = call_level + 1
    _api_session_id = dbsession.session_id
    _api_indent_level=_api_level
    _api_indent_method='AUTO'

    _process_identity_dict = set_process_identity_dict('api', _api_name, _api_action, _api_entity, _api_msgID, _api_msgID, _api_session_id, _api_debug_level, print_enabled, filelog_enabled, log_file, errors_file, debug_file, _api_indent_level, _api_indent_method)
    _process_call_area = set_process_caller_area(_process_identity_dict, caller_dict)

    log_process_start(_api_msgID,**_process_identity_dict)
   
    if action.upper() in ('START','REQUEST'):
        return dbapi_interaction_start(dbsession, input_dict, filter_dict=filter_dict, caller_dict=caller_dict, call_level=call_level,debug_level=debug_level)
    elif action.upper() == 'ACCEPT':
        return dbapi_interaction_finish(dbsession, input_dict, filter_dict=filter_dict, caller_dict=caller_dict, call_level=call_level,debug_level=debug_level)
    elif action.upper() == 'FINISH':
        return dbapi_interaction_finish(dbsession, input_dict, filter_dict=filter_dict, caller_dict=caller_dict, call_level=call_level,debug_level=debug_level)
    elif action.upper() == 'MESSAGE':
        return dbapi_interaction_message_add(dbsession, input_dict, filter_dict=filter_dict, caller_dict=caller_dict, call_level=call_level,debug_level=debug_level)

    log_process_input('', 'input_dict', input_dict,**_process_identity_dict)
    log_process_input('', 'filter_dict', filter_dict,**_process_identity_dict)
    log_process_input('', 'caller_dict', caller_dict, **_process_identity_dict)

    action_result = dbsession.table_action(dbmodel.INTERACTION, action , input_dict, filter_dict, caller_dict={}, api_name=_api_name, api_entity=_api_entity, auto_commit=True, call_level=_api_level, debug_level=_api_debug_level-1)
    api_result = action_result
    api_result.update({'api_action': _api_action, 'api_name': _api_name})
    
    log_process_finish(_api_msgID, api_result, **_process_identity_dict)    
    return api_result
#::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
def dbapi_interaction_message(dbsession, action, input_dict, filter_dict={}, caller_dict={}, call_level=-1,debug_level=-1):
    _api_name = "dbapi_interaction_message"
    _api_entity = 'INTERACTION_MESSAGE'
    _api_action = action
    _api_msgID = set_api_msgID(_api_name, _api_action, _api_entity)    
    _api_debug_level = set_api_debug_level(_api_name, debug_level,dbsession)
    _api_level = call_level + 1
    _api_session_id = dbsession.session_id
    _api_indent_level=_api_level
    _api_indent_method='AUTO'

    _process_identity_dict = set_process_identity_dict('api', _api_name, _api_action, _api_entity, _api_msgID, _api_msgID, _api_session_id, _api_debug_level, print_enabled, filelog_enabled, log_file, errors_file, debug_file, _api_indent_level, _api_indent_method)
    _process_call_area = set_process_caller_area(_process_identity_dict, caller_dict)

    log_process_start(_api_msgID,**_process_identity_dict)

    log_process_input('', 'input_dict', input_dict,**_process_identity_dict)
    log_process_input('', 'filter_dict', filter_dict,**_process_identity_dict)
    log_process_input('', 'caller_dict', caller_dict,**_process_identity_dict)

    action_result = dbsession.table_action(dbmodel.INTERACTION_MESSAGE, action , input_dict, filter_dict, caller_dict={}, api_name=_api_name, api_entity=_api_entity, auto_commit=True, call_level=_api_level, debug_level=_api_debug_level-1)
    api_result = action_result
    api_result.update({'api_action': _api_action, 'api_name': _api_name})
    
    log_process_finish(_api_msgID, api_result, **_process_identity_dict)    
    return api_result
#::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
def dbapi_interaction_start(dbsession, input_dict, filter_dict={}, caller_dict={}, call_level=-1,debug_level=-1):
    _api_name = "dbapi_interaction_start"
    _api_entity = 'INTERACTION'
    _api_action = 'START'
    _api_msgID = set_api_msgID(_api_name, _api_action, _api_entity)    
    _api_debug_level = set_api_debug_level(_api_name, debug_level,dbsession)
    _api_level = call_level + 1
    _api_session_id = dbsession.session_id
    _api_indent_level=_api_level
    _api_indent_method='AUTO'

    _process_identity_dict = set_process_identity_dict('api', _api_name, _api_action, _api_entity, _api_msgID, _api_msgID, _api_session_id, _api_debug_level, print_enabled, filelog_enabled, log_file, errors_file, debug_file, _api_indent_level, _api_indent_method)
    _process_call_area = set_process_caller_area(_process_identity_dict, caller_dict)

    log_process_start(_api_msgID,**_process_identity_dict)

    log_process_input('', 'input_dict', input_dict,**_process_identity_dict)
    log_process_input('', 'filter_dict', filter_dict,**_process_identity_dict)
    log_process_input('', 'caller_dict', caller_dict,**_process_identity_dict)

    #////////////////////////////////////////
    originator = None
    originator_id = None
    originator_name = None
    corresponder = None
    corresponder_id = None
    corresponder_name = None
    #////////////////////////////////////////

    #step-1: originator
    originator_id = input_dict.get('originator_id')
    if originator_id:
        xid = dbsession.get(dbmodel.CONSUMER, {'consumer_id':originator_id},call_level=_api_level, debug_level=_api_debug_level-1)
        if xid:
            originator = 'consumer'
            originator_name = xid.email
        else:
            xid = dbsession.get(dbmodel.POINT_OF_SALE, {'pointofsale_id':originator_id}, call_level=_api_level, debug_level=_api_debug_level-1)
            if xid:
                originator='pointofsale'
                originator_name = xid.name
            else:
                xid = dbsession.get(dbmodel.CLIENT, {'client_id':originator_id}, call_level=_api_level, debug_level=_api_debug_level-1)
                if xid:
                    originator='client'
                    originator_name = xid.email
                else:
                    msg = f'originator not valid'
                    api_result = {'api_status': 'error', 'api_message': msg, 'api_action': _api_action.upper(), 'api_name': _api_name}
                    log_process_finish(_api_msgID, api_result, **_process_identity_dict)
                    return api_result

        xoriginator = input_dict.get('originator')
        if xoriginator and not xoriginator == originator:
            msg = f'originator_id not valid for originator {xoriginator}'
            api_result = {'api_status': 'error', 'api_message': msg, 'api_action': _api_action.upper(), 'api_name': _api_name}
            log_process_finish(_api_msgID, api_result, **_process_identity_dict)
            return api_result
    else:
        consumer_id = input_dict.get('consumer_id')
        if consumer_id:
            consumer=dbsession.get(dbmodel.CONSUMER, {'consumer_id':consumer_id}, call_level=_api_level, debug_level=_api_debug_level-1)
            if not consumer:
                msg = f'consumer not found'
                api_result = {'api_status': 'error', 'api_message': msg, 'api_action': _api_action.upper(), 'api_name': _api_name}
                log_process_finish(_api_msgID, api_result, **_process_identity_dict)
                return api_result
            originator='consumer'
            originator_id=consumer_id
            originator_name = consumer.email
        else:
            pointofsale_id = input_dict.get('pointofsale_id')
            if pointofsale_id:
                pointofsale=dbsession.get(dbmodel.POINT_OF_SALE, {'pointofsale_id':pointofsale_id}, call_level=_api_level, debug_level=_api_debug_level-1)
                if not pointofsale:
                    msg = f'pointofsale not found'
                    api_result = {'api_status': 'error', 'api_message': msg, 'api_action': _api_action.upper(), 'api_name': _api_name}
                    log_process_finish(_api_msgID, api_result, **_process_identity_dict)
                    return api_result
                originator='pointofsale'
                originator_id=pointofsale_id
                originator_name = pointofsale.name
            else:
                client_id = input_dict.get('client_id')
                if client_id:
                    client=dbsession.get(dbmodel.CLIENT, {'client_id':client_id}, call_level=_api_level, debug_level=_api_debug_level-1)
                    if not client:
                        msg = f'client not found'
                        api_result = {'api_status': 'error', 'api_message': msg, 'api_action': _api_action.upper(), 'api_name': _api_name}
                        log_process_finish(_api_msgID, api_result, **_process_identity_dict)
                        return api_result
                    originator='client'
                    originator_id=client_id
                    originator_name = client.email
                else:
                    msg = f'no pointofsale or consumer or client defined'
                    api_result = {'api_status': 'error', 'api_message': msg, 'api_action': _api_action.upper(), 'api_name': _api_name}
                    log_process_finish(_api_msgID, api_result, **_process_identity_dict)
                    return api_result

    if not originator or not originator_id:
        msg = f'originator not defined (pointofsale or consumer or client)'
        api_result = {'api_status': 'error', 'api_message': msg, 'api_action': _api_action.upper(), 'api_name': _api_name}
        log_process_finish(_api_msgID, api_result, **_process_identity_dict)
        return api_result

    input_dict.update({'originator': originator})
    input_dict.update({'originator_id': originator_id})
    input_dict.update({'originator_name': originator_name})
    
    msg = f'originator set to [{originator_name}]'
    log_process_message('', 'success', msg, **_process_identity_dict)
    
    #step-2: corresponder
    corresponder_id = input_dict.get('corresponder_id')
    if not corresponder_id:
        msg = f'no corresponder specified'
        api_result = {'api_status': 'error', 'api_message': msg, 'api_action': _api_action.upper(), 'api_name': _api_name}
        log_process_finish(_api_msgID, api_result, **_process_identity_dict)
        return api_result
    pointofsale = dbsession.get(dbmodel.POINT_OF_SALE, {'pointofsale_id':corresponder_id}, call_level=_api_level, debug_level=_api_debug_level-1)
    if pointofsale:
        corresponder='pointofsale'
        corresponder_id = pointofsale.pointofsale_id
        corresponder_name = pointofsale.name
    else:
        xid = dbsession.get(dbmodel.CONSUMER, {'consumer_id':corresponder_id}, call_level=_api_level, debug_level=_api_debug_level-1)
        if xid:
            corresponder='consumer'
            corresponder_id = xid.consumer_id
            corresponder_name = xid.email           
        else:
            xid = dbsession.get(dbmodel.CLIENT, {'client_id':corresponder_id}, call_level=_api_level, debug_level=_api_debug_level-1)
            if xid:
                corresponder='client'
                corresponder_id=xid.client_id
                corresponder_name = xid.email          
            else:
                msg = f'corresponder not valid'
                api_result = {'api_status': 'error', 'api_message': msg, 'api_action': _api_action.upper(), 'api_name': _api_name}
                log_process_finish(_api_msgID, api_result, **_process_identity_dict)
                return api_result
    xcorresponder = input_dict.get('corresponder')
    if xcorresponder and not xcorresponder == corresponder:
        msg = f'corresponder_id not valid for corresponder {xcorresponder}'
        api_result = {'api_status': 'error', 'api_message': msg, 'api_action': _api_action.upper(), 'api_name': _api_name}
        log_process_finish(_api_msgID, api_result, **_process_identity_dict)
        return api_result
    
    input_dict.update({'corresponder': corresponder})
    input_dict.update({'corresponder_id': corresponder_id})
    input_dict.update({'corresponder_name': corresponder_name})

    msg = f'corresponder set to [{corresponder_name}]'
    log_process_message('', 'success', msg, **_process_identity_dict)

    #step-3: already active
    filterJson = {"originator": originator, "originator_id": originator_id, "status": 'Active'}
    active_interactions=dbsession.get_rows(dbmodel.INTERACTION, filterJson, call_level=_api_level, debug_level=_api_debug_level-1)
    if active_interactions:
        msg = f'[{len(active_interactions)} active interactions found] for originator [{originator_name}]'
        log_process_message('', 'warning', msg, **_process_identity_dict)
        for active_interaction in active_interactions:
            interaction_id = active_interaction.interaction_id
            time_start = active_interaction.row_timestamp
            time_end = datetime.datetime.utcnow()
            diff = time_end - time_start
            duration = diff.days * 24 * 60 * 60 + diff.seconds
            interaction_rec = active_interaction.to_dict()
            interaction_rec.update({'status':'finished','completed_timestamp':time_end,'duration':duration})
            active_interaction = dbsession.update(dbmodel.INTERACTION, interaction_rec, auto_commit=True, call_level=_api_level, debug_level=_api_debug_level - 1)

    #step-4: corresponder 
    filterJson = {"corresponder": corresponder, "corresponder_id": corresponder_id, "status": 'Active'}
    active_interactions=dbsession.get_rows(dbmodel.INTERACTION, filterJson, call_level=_api_level, debug_level=_api_debug_level-1)
    if active_interactions:
        msg = f'corresponder {corresponder_name} is not available'
        log_process_message('', 'error', msg, **_process_identity_dict)
        api_result = {'api_status': 'error', 'api_message': msg, 'api_action': _api_action.upper(), 'api_name': _api_name}
        log_process_finish(_api_msgID, api_result, **_process_identity_dict)
        return api_result

    #step-5: insert
    input_dict.update({'status': 'Requested'})
    interaction = dbsession.insert(dbmodel.INTERACTION, input_dict, auto_commit=True, call_level=_api_level, debug_level=_api_debug_level-1)
    if not interaction:
        msg = f'interaction start failed'
        api_result = {'api_status': 'error', 'api_message': msg, 'api_action': _api_action.upper(), 'api_name': _api_name}
        log_process_finish(_api_msgID, api_result, **_process_identity_dict)
        return api_result

    interaction_id = interaction.interaction_id

    #step-6: message
    interaction_message = {
        'interaction_id':interaction_id,
        'originator_id':interaction.originator_id,
        'originator':interaction.originator,
        'message_type':'start',
        'message_record':f"hi. i am {interaction.originator} {originator_name}",
        'content_type':'text',
        'format':'',
        'geolocation_lat':input_dict.get('geolocation_lat'),
        'geolocation_lon':input_dict.get('geolocation_lon'),
        }
    start_message = dbsession.insert(dbmodel.INTERACTION_MESSAGE, interaction_message, auto_commit=True, call_level=_api_level, debug_level=_api_debug_level-1)
    if not start_message:
        msg = f'start message insert failed'
        log_process_message('', 'error', msg, **_process_identity_dict)
        msg = f'interaction start failed (message insert failed)'
        api_result = {'api_status': 'error', 'api_message': msg, 'api_action': _api_action.upper(), 'api_name': _api_name}
        log_process_finish(_api_msgID, api_result, **_process_identity_dict)
        return api_result
    #shalimar
    #step-6: result
    interaction_record = interaction.to_dict()
    msg=f'OK. interaction established between You and {corresponder.upper()} {corresponder_name}'
    api_result = {'api_status': 'success', 'api_message': msg, 'interaction_id': interaction_id, 'api_data': interaction_record, 'api_action': _api_action.upper(), 'api_name': _api_name}
    log_process_finish(_api_msgID, api_result, **_process_identity_dict)    
    return api_result
#::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
def dbapi_interaction_accept(dbsession, input_dict, filter_dict={}, caller_dict={}, call_level=-1,debug_level=-1):
    _api_name = "dbapi_interaction_accept"
    _api_entity = 'INTERACTION'
    _api_action = 'ACCEPT'
    _api_msgID = set_api_msgID(_api_name, _api_action, _api_entity)    
    _api_debug_level = set_api_debug_level(_api_name, debug_level,dbsession)
    _api_level = call_level + 1
    _api_session_id = dbsession.session_id
    _api_indent_level=_api_level
    _api_indent_method='AUTO'

    _process_identity_dict = set_process_identity_dict('api', _api_name, _api_action, _api_entity, _api_msgID, _api_msgID, _api_session_id, _api_debug_level, print_enabled, filelog_enabled, log_file, errors_file, debug_file, _api_indent_level, _api_indent_method)
    _process_call_area = set_process_caller_area(_process_identity_dict, caller_dict)

    log_process_start(_api_msgID,**_process_identity_dict)

    log_process_input('', 'input_dict', input_dict,**_process_identity_dict)
    log_process_input('', 'filter_dict', filter_dict,**_process_identity_dict)
    log_process_input('', 'caller_dict', caller_dict,**_process_identity_dict)

    interaction_id = input_dict.get('interaction_id')
    if not interaction_id:
        msg = f'interaction not defined'
        log_process_message('', 'error', msg, **_process_identity_dict)
        api_result = {'api_status': 'error', 'api_message': msg}
        log_process_finish(_api_msgID, api_result, **_process_identity_dict)
        return

    interaction = dbsession.get(dbmodel.INTERACTION, {'interaction_id':interaction_id}, call_level=_api_level, debug_level=_api_debug_level-1)
    if not interaction:
        msg = f'interaction not found'
        api_result = {'api_status': 'error', 'api_message': msg}
        log_process_finish(_api_msgID, api_result, **_process_identity_dict)
        return

    if interaction.status == 'Active':
        msg = f'interaction is already Active'
        api_result = {'api_status': 'error', 'api_message': msg}
        log_process_finish(_api_msgID, api_result, **_process_identity_dict)
        return

    if not interaction.status=='Requested':
        msg = f'interaction is already [{interaction.status}]'
        api_result = {'api_status': 'error', 'api_message': msg}
        log_process_finish(_api_msgID, api_result, **_process_identity_dict)
        return

    #////////////////////////////////////////
    originator = None
    originator_id = None
    originator_name = None
    corresponder = None
    corresponder_id = None
    corresponder_name = None
    #////////////////////////////////////////

    #step-1: originator
    originator_id = input_dict.get('originator_id')
    if originator_id:
        xid = dbsession.get(dbmodel.CONSUMER, {'consumer_id':originator_id},call_level=_api_level, debug_level=_api_debug_level-1)
        if xid:
            originator = 'consumer'
            originator_name = xid.email
        else:
            xid = dbsession.get(dbmodel.POINT_OF_SALE, {'pointofsale_id':originator_id}, call_level=_api_level, debug_level=_api_debug_level-1)
            if xid:
                originator='pointofsale'
                originator_name = xid.name
            else:
                xid = dbsession.get(dbmodel.CLIENT, {'client_id':originator_id}, call_level=_api_level, debug_level=_api_debug_level-1)
                if xid:
                    originator='client'
                    originator_name = xid.email
                else:
                    msg = f'originator not valid'
                    api_result = {'api_status': 'error', 'api_message': msg, 'api_action': _api_action.upper(), 'api_name': _api_name}
                    log_process_finish(_api_msgID, api_result, **_process_identity_dict)
                    return api_result

        xoriginator = input_dict.get('originator')
        if xoriginator and not xoriginator == originator:
            msg = f'originator_id not valid for originator {xoriginator}'
            log_process_message('', 'error', msg, **_process_identity_dict)
            api_result = {'api_status': 'error', 'api_message': msg, 'api_action': _api_action.upper(), 'api_name': _api_name}
            log_process_finish(_api_msgID, api_result, **_process_identity_dict)
            return api_result
    else:
        consumer_id = input_dict.get('consumer_id')
        if consumer_id:
            consumer=dbsession.get(dbmodel.CONSUMER, {'consumer_id':consumer_id}, call_level=_api_level, debug_level=_api_debug_level-1)
            if not consumer:
                msg = f'consumer not found'
                api_result = {'api_status': 'error', 'api_message': msg, 'api_action': _api_action.upper(), 'api_name': _api_name}
                log_process_finish(_api_msgID, api_result, **_process_identity_dict)
                return api_result
            originator='consumer'
            originator_id=consumer_id
            originator_name = consumer.email
        else:
            pointofsale_id = input_dict.get('pointofsale_id')
            if pointofsale_id:
                pointofsale=dbsession.get(dbmodel.POINT_OF_SALE, {'pointofsale_id':pointofsale_id}, call_level=_api_level, debug_level=_api_debug_level-1)
                if not pointofsale:
                    msg = f'pointofsale not found'
                    api_result = {'api_status': 'error', 'api_message': msg, 'api_action': _api_action.upper(), 'api_name': _api_name}
                    log_process_finish(_api_msgID, api_result, **_process_identity_dict)
                    return api_result
                originator='pointofsale'
                originator_id=pointofsale_id
                originator_name = pointofsale.name
            else:
                client_id = input_dict.get('client_id')
                if client_id:
                    client=dbsession.get(dbmodel.CLIENT, {'client_id':client_id}, call_level=_api_level, debug_level=_api_debug_level-1)
                    if not client:
                        msg = f'client not found'
                        api_result = {'api_status': 'error', 'api_message': msg, 'api_action': _api_action.upper(), 'api_name': _api_name}
                        log_process_finish(_api_msgID, api_result, **_process_identity_dict)
                        return api_result
                    originator='client'
                    originator_id=client_id
                    originator_name = client.email
                else:
                    msg = f'no pointofsale or consumer or client defined'
                    api_result = {'api_status': 'error', 'api_message': msg, 'api_action': _api_action.upper(), 'api_name': _api_name}
                    log_process_finish(_api_msgID, api_result, **_process_identity_dict)
                    return api_result

    if not originator or not originator_id:
        msg = f'originator not defined (pointofsale or consumer or client)'
        log_process_message('', 'succerroress', msg, **_process_identity_dict)
        api_result = {'api_status': 'error', 'api_message': msg, 'api_action': _api_action.upper(), 'api_name': _api_name}
        log_process_finish(_api_msgID, api_result, **_process_identity_dict)
        return api_result

    if originator_id == interaction.originator_id:
        msg = f'originator [{originator_name}] same as corresponder'
        log_process_message('', 'error', msg, **_process_identity_dict)
        api_result = {'api_status': 'error', 'api_message': msg, 'api_action': _api_action.upper(), 'api_name': _api_name}
        log_process_finish(_api_msgID, api_result, **_process_identity_dict)
        return api_result

    if interaction.corresponder_id:
        if not originator_id == interaction.corresponder_id:
            msg = f'interaction must be accepted by [{interaction.corresponder}] {interaction.corresponder_name} [not] by  [{originator}] {originator_name} '
            api_result = {'api_status': 'error', 'api_message': msg}
            log_process_finish(_api_msgID, api_result, **_process_identity_dict)
            return

    input_dict.update({'corresponder': originator})
    input_dict.update({'corresponder_id': originator_id})
    input_dict.update({'corresponder_name': originator_name})

    msg=f'corresponder: [{originator}] [[{originator_name}]]'
    log_process_message('', 'success', msg, **_process_identity_dict)

    interaction_message = {
        'interaction_id':interaction_id,
        'originator_id':originator_id,
        'originator':originator,
        'originator_name':originator_name,
        'content_type':input_dict.get('content_type','text'),
        'format':input_dict.get('format',''),
        'message_type':'accept',
        'message_record':f"hi. i am {input_dict.get('originator')} {input_dict.get('originator_id')}. how can i help you?",
        'geolocation_lat':input_dict.get('geolocation_lat'),
        'geolocation_lon':input_dict.get('geolocation_lon'),
        }

    message = dbsession.insert(dbmodel.INTERACTION_MESSAGE, interaction_message, auto_commit=True, call_level=_api_level, debug_level=_api_debug_level - 1)
    if not message:
        msg = f'interaction message add failed'
        log_process_message('', 'error', msg, **_process_identity_dict)

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
    interaction = dbsession.update(dbmodel.INTERACTION, interaction_rec, auto_commit=True, call_level=_api_level, debug_level=_api_debug_level - 1)
    if not interaction:
        msg = f'interaction accept failed'
        api_result = {'api_status': 'error', 'api_message': msg, 'api_action': _api_action.upper(), 'api_name': _api_name}
        log_process_message('', 'error', msg, **_process_identity_dict)
        return api_result
    
    #step-6: result
    interaction_rec = interaction.to_dict()
    msg=f'OK. interaction accepted'
    api_result = {'api_status': 'success', 'api_message': msg, 'interaction_id': interaction.interaction_id, 'api_data': interaction_rec, 'api_action': _api_action.upper(), 'api_name': _api_name}
    log_process_finish(_api_msgID, api_result, **_process_identity_dict)    
    return api_result
#::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
def dbapi_interaction_finish(dbsession, input_dict, filter_dict={}, caller_dict={}, call_level=-1,debug_level=-1):
    _api_name = "dbapi_interaction_finish"
    _api_entity = 'INTERACTION'
    _api_action = 'FINISH'
    _api_msgID = set_api_msgID(_api_name, _api_action, _api_entity)    
    _api_debug_level = set_api_debug_level(_api_name, debug_level,dbsession)
    _api_level = call_level + 1
    _api_session_id = dbsession.session_id
    _api_indent_level=_api_level
    _api_indent_method='AUTO'

    _process_identity_dict = set_process_identity_dict('api', _api_name, _api_action, _api_entity, _api_msgID, _api_msgID, _api_session_id, _api_debug_level, print_enabled, filelog_enabled, log_file, errors_file, debug_file, _api_indent_level, _api_indent_method)
    _process_call_area = set_process_caller_area(_process_identity_dict, caller_dict)

    log_process_start(_api_msgID,**_process_identity_dict)

    log_process_input('', 'input_dict', input_dict,**_process_identity_dict)
    log_process_input('', 'filter_dict', filter_dict,**_process_identity_dict)
    log_process_input('', 'caller_dict', caller_dict,**_process_identity_dict)

    interaction_id = input_dict.get('interaction_id')
    if not interaction_id:
        msg = f'interaction not defined'
        log_process_message('', 'error', msg, **_process_identity_dict)
        api_result = {'api_status': 'error', 'api_message': msg}
        log_process_finish(_api_msgID, api_result, **_process_identity_dict)
        return

    interaction = dbsession.get(dbmodel.INTERACTION, {'interaction_id':interaction_id}, call_level=_api_level, debug_level=_api_debug_level-1)
    if not interaction:
        msg = f'interaction not found'
        api_result = {'api_status': 'error', 'api_message': msg}
        log_process_finish(_api_msgID, api_result, **_process_identity_dict)
        return

    if not interaction.status=='Active':
        msg = f'interaction not Active'
        api_result = {'api_status': 'error', 'api_message': msg}
        log_process_finish(_api_msgID, api_result, **_process_identity_dict)
        return

    #////////////////////////////////////////
    originator = None
    originator_id = None
    originator_name = None
    corresponder = None
    corresponder_id = None
    corresponder_name = None
    #////////////////////////////////////////

    #step-1: originator
    originator_id = input_dict.get('originator_id')
    if originator_id:
        xid = dbsession.get(dbmodel.CONSUMER, {'consumer_id':originator_id},call_level=_api_level, debug_level=_api_debug_level-1)
        if xid:
            originator = 'consumer'
            originator_name = xid.email
        else:
            xid = dbsession.get(dbmodel.POINT_OF_SALE, {'pointofsale_id':originator_id}, call_level=_api_level, debug_level=_api_debug_level-1)
            if xid:
                originator='pointofsale'
                originator_name = xid.name
            else:
                xid = dbsession.get(dbmodel.CLIENT, {'client_id':originator_id}, call_level=_api_level, debug_level=_api_debug_level-1)
                if xid:
                    originator='client'
                    originator_name = xid.email
                else:
                    msg = f'originator not valid'
                    api_result = {'api_status': 'error', 'api_message': msg, 'api_action': _api_action.upper(), 'api_name': _api_name}
                    log_process_finish(_api_msgID, api_result, **_process_identity_dict)
                    return api_result

        xoriginator = input_dict.get('originator')
        if xoriginator and not xoriginator == originator:
            msg = f'originator_id not valid for originator {xoriginator}'
            log_process_message('', 'error', msg, **_process_identity_dict)
            api_result = {'api_status': 'error', 'api_message': msg, 'api_action': _api_action.upper(), 'api_name': _api_name}
            log_process_finish(_api_msgID, api_result, **_process_identity_dict)
            return api_result
    else:
        consumer_id = input_dict.get('consumer_id')
        if consumer_id:
            consumer=dbsession.get(dbmodel.CONSUMER, {'consumer_id':consumer_id}, call_level=_api_level, debug_level=_api_debug_level-1)
            if not consumer:
                msg = f'consumer not found'
                api_result = {'api_status': 'error', 'api_message': msg, 'api_action': _api_action.upper(), 'api_name': _api_name}
                log_process_finish(_api_msgID, api_result, **_process_identity_dict)
                return api_result
            originator='consumer'
            originator_id=consumer_id
            originator_name = consumer.email
        else:
            pointofsale_id = input_dict.get('pointofsale_id')
            if pointofsale_id:
                pointofsale=dbsession.get(dbmodel.POINT_OF_SALE, {'pointofsale_id':pointofsale_id}, call_level=_api_level, debug_level=_api_debug_level-1)
                if not pointofsale:
                    msg = f'pointofsale not found'
                    api_result = {'api_status': 'error', 'api_message': msg, 'api_action': _api_action.upper(), 'api_name': _api_name}
                    log_process_finish(_api_msgID, api_result, **_process_identity_dict)
                    return api_result
                originator='pointofsale'
                originator_id=pointofsale_id
                originator_name = pointofsale.name
            else:
                client_id = input_dict.get('client_id')
                if client_id:
                    client=dbsession.get(dbmodel.CLIENT, {'client_id':client_id}, call_level=_api_level, debug_level=_api_debug_level-1)
                    if not client:
                        msg = f'client not found'
                        api_result = {'api_status': 'error', 'api_message': msg, 'api_action': _api_action.upper(), 'api_name': _api_name}
                        log_process_finish(_api_msgID, api_result, **_process_identity_dict)
                        return api_result
                    originator='client'
                    originator_id=client_id
                    originator_name = client.email
                else:
                    msg = f'no pointofsale or consumer or client defined'
                    api_result = {'api_status': 'error', 'api_message': msg, 'api_action': _api_action.upper(), 'api_name': _api_name}
                    log_process_finish(_api_msgID, api_result, **_process_identity_dict)
                    return api_result

    if not originator or not originator_id:
        msg = f'originator not defined (pointofsale or consumer or client)'
        log_process_message('', 'succerroress', msg, **_process_identity_dict)
        api_result = {'api_status': 'error', 'api_message': msg, 'api_action': _api_action.upper(), 'api_name': _api_name}
        log_process_finish(_api_msgID, api_result, **_process_identity_dict)
        return api_result

    input_dict.update({'originator': originator})
    input_dict.update({'originator_id': originator_id})

    if not originator_id == interaction.originator_id or originator_id == interaction.corresponder_id:
        msg = f'invalid originator [{originator_name}] for interaction [{interaction.interaction_id}]'
        log_process_message('', 'error', msg, **_process_identity_dict)
        api_result = {'api_status': 'error', 'api_message': msg, 'api_action': _api_action.upper(), 'api_name': _api_name}
        log_process_finish(_api_msgID, api_result, **_process_identity_dict)
        return api_result

    msg=f'originator: [{originator}] [[{originator_name}]]'
    log_process_message('', 'success', msg, **_process_identity_dict)
    
    #step-2: corresponder
    # corresponder_id = input_dict.get('corresponder_id')
    # if not corresponder_id:
    #     msg = f'no corresponder specified'
    #     if _api_debug_level > 0: log_process_message(_api_name, _api_entity, _api_action, 'warning',msg, call_level=_api_level, session_id=dbsession.session_id,filelog_enabled=thisApp.FILELOG_ON,print_enabled=thisApp.CONSOLE_ON)
    # else:
    #     pointofsale = dbsession.get(dbmodel.POINT_OF_SALE, {'pointofsale_id':corresponder_id}, call_level=_api_level, debug_level=_api_debug_level-1)
    #     if pointofsale:
    #         corresponder='pointofsale'
    #         corresponder_id = pointofsale.pointofsale_id
    #         corresponder_name = pointofsale.name
    #     else:
    #         xid = dbsession.get(dbmodel.CONSUMER, {'consumer_id':corresponder_id}, call_level=_api_level, debug_level=_api_debug_level-1)
    #         if xid:
    #             corresponder='consumer'
    #             corresponder_id = xid.consumer_id
    #             corresponder_name = xid.email           
    #         else:
    #             xid = dbsession.get(dbmodel.CLIENT, {'client_id':corresponder_id}, call_level=_api_level, debug_level=_api_debug_level-1)
    #             if xid:
    #                 corresponder='client'
    #                 corresponder_id=xid.client_id
    #                 corresponder_name = xid.email          
    #     xcorresponder = input_dict.get('corresponder')
    #     if xcorresponder and not xcorresponder == corresponder:
    #         msg = f'corresponder_id not valid for corresponder {xcorresponder}'
    #         api_result = {'api_status': 'error', 'api_message': msg, 'api_action': _api_action.upper(), 'api_name': _api_name}
    #         if _api_debug_level > 0: log_process_message(_api_name, _api_entity, _api_action, 'warning',msg, call_level=_api_level, session_id=dbsession.session_id,filelog_enabled=thisApp.FILELOG_ON,print_enabled=thisApp.CONSOLE_ON)

    # if corresponder_id:
    #     input_dict.update({'corresponder': corresponder})
    #     input_dict.update({'corresponder_id': corresponder_id})
    #     msg=f'corresponder: [{corresponder}] [[{corresponder_name}]]'
    #     log_process_message('', 'success', msg, **_process_identity_dict)

    # if not interaction.corresponder and not interaction.originator_id==originator_id:
    #     interaction_rec=interaction.to_dict()
    #     interaction.update({'corresponder': originator})
    #     interaction.update({'corresponder_id': originator_id})
    #     interaction = dbsession.insert(dbmodel.INTERACTION, interaction_rec, auto_commit=True, call_level=_api_level, debug_level=_api_debug_level - 1)

    interaction_message = {
        'interaction_id':interaction_id,
        'originator_id':input_dict.get('originator_id',''),
        'originator':input_dict.get('originator',''),
        'content_type':input_dict.get('content_type','text'),
        'format':input_dict.get('format',''),
        'message_type':'finish',
        'message_record':f"goodbye. i am {input_dict.get('originator')} {input_dict.get('originator_id')}",
        }

    message = dbsession.insert(dbmodel.INTERACTION_MESSAGE, interaction_message, auto_commit=True, call_level=_api_level, debug_level=_api_debug_level - 1)
    if not message:
        msg = f'interaction message add failed'
        log_process_message('', 'error', msg, **_process_identity_dict)

    time_start = interaction.row_timestamp
    time_end = datetime.datetime.utcnow()
    diff = time_end - time_start
    duration = diff.days * 24 * 60 * 60 + diff.seconds

    interaction_rec = interaction.to_dict()
    interaction_rec.update({'status':'completed','completed_timestamp':time_end,'duration':duration})
    interaction = dbsession.update(dbmodel.INTERACTION, interaction_rec, auto_commit=True, call_level=_api_level, debug_level=_api_debug_level - 1)
    if not interaction:
        msg = f'interaction finish failed'
        api_result = {'api_status': 'error', 'api_message': msg, 'api_action': _api_action.upper(), 'api_name': _api_name}
        log_process_message('', 'error', msg, **_process_identity_dict)
        return api_result
    
    #step-6: result
    interaction_rec = interaction.to_dict()
    msg=f'OK. interaction finish'
    api_result = {'api_status': 'success', 'api_message': msg, 'interaction_id': interaction.interaction_id, 'api_data': interaction_rec, 'api_action': _api_action.upper(), 'api_name': _api_name}
    log_process_finish(_api_msgID, api_result, **_process_identity_dict)    
    return api_result
#::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
def dbapi_interaction_message_add(dbsession, input_dict, filter_dict={}, caller_dict={}, call_level=-1,debug_level=-1):
    _api_name = "dbapi_interaction_message_add"
    _api_entity = 'INTERACTION_MESSAGE'
    _api_action = 'ADD'
    _api_msgID = set_api_msgID(_api_name, _api_action, _api_entity)
    _api_debug_level = set_api_debug_level(_api_name, debug_level,dbsession)
    _api_level = call_level + 1
    _api_indent_level=_api_level
    _api_indent_method='AUTO'

    _process_identity_dict = set_process_identity_dict('api', _api_name, _api_action, _api_entity, _api_msgID, _api_msgID, dbsession.session_id, _api_debug_level, print_enabled, filelog_enabled, log_file, errors_file, indent_level, indent_method)
    _process_call_area = set_process_caller_area(_process_identity_dict, caller_dict)
    
    log_process_start(_api_msgID,**_process_identity_dict)

    log_process_input('', 'input_dict', input_dict,**_process_identity_dict)
    log_process_input('', 'filter_dict', filter_dict,**_process_identity_dict)
    log_process_input('', 'caller_dict', caller_dict,**_process_identity_dict)

    interaction_id = input_dict.get('interaction_id')
    if not interaction_id:
        msg = f'interaction not defined'
        log_process_message('', 'error', msg, **_process_identity_dict)
        api_result = {'api_status': 'error', 'api_message': msg}
        log_process_finish(_api_msgID, api_result, **_process_identity_dict)
        return

    interaction = dbsession.get(dbmodel.INTERACTION, {'interaction_id':interaction_id}, call_level=_api_level, debug_level=_api_debug_level-1)
    if not interaction:
        msg = f'interaction not found'
        api_result = {'api_status': 'error', 'api_message': msg}
        log_process_finish(_api_msgID, api_result, **_process_identity_dict)
        return

    if not interaction.status=='Active':
        msg = f'interaction not Active'
        api_result = {'api_status': 'error', 'api_message': msg}
        log_process_finish(_api_msgID, api_result, **_process_identity_dict)
        return

    #////////////////////////////////////////
    originator = None
    originator_id = None
    originator_name = None
    corresponder = None
    corresponder_id = None
    corresponder_name = None
    #////////////////////////////////////////

    #step-1: originator
    originator_id = input_dict.get('originator_id')
    if originator_id:
        xid = dbsession.get(dbmodel.CONSUMER, {'consumer_id':originator_id},call_level=_api_level, debug_level=_api_debug_level-1)
        if xid:
            originator = 'consumer'
            originator_name = xid.email
        else:
            xid = dbsession.get(dbmodel.POINT_OF_SALE, {'pointofsale_id':originator_id}, call_level=_api_level, debug_level=_api_debug_level-1)
            if xid:
                originator='pointofsale'
                originator_name = xid.name
            else:
                xid = dbsession.get(dbmodel.CLIENT, {'client_id':originator_id}, call_level=_api_level, debug_level=_api_debug_level-1)
                if xid:
                    originator='client'
                    originator_name = xid.email
                else:
                    msg = f'originator not valid'
                    api_result = {'api_status': 'error', 'api_message': msg, 'api_action': _api_action.upper(), 'api_name': _api_name}
                    log_process_finish(_api_msgID, api_result, **_process_identity_dict)
                    return api_result

        xoriginator = input_dict.get('originator')
        if xoriginator and not xoriginator == originator:
            msg = f'originator_id not valid for originator {xoriginator}'
            log_process_message('', 'error', msg, **_process_identity_dict)
            api_result = {'api_status': 'error', 'api_message': msg, 'api_action': _api_action.upper(), 'api_name': _api_name}
            log_process_finish(_api_msgID, api_result, **_process_identity_dict)
            return api_result
    else:
        consumer_id = input_dict.get('consumer_id')
        if consumer_id:
            consumer=dbsession.get(dbmodel.CONSUMER, {'consumer_id':consumer_id}, call_level=_api_level, debug_level=_api_debug_level-1)
            if not consumer:
                msg = f'consumer not found'
                api_result = {'api_status': 'error', 'api_message': msg, 'api_action': _api_action.upper(), 'api_name': _api_name}
                log_process_finish(_api_msgID, api_result, **_process_identity_dict)
                return api_result
            originator='consumer'
            originator_id=consumer_id
            originator_name = consumer.email
        else:
            pointofsale_id = input_dict.get('pointofsale_id')
            if pointofsale_id:
                pointofsale=dbsession.get(dbmodel.POINT_OF_SALE, {'pointofsale_id':pointofsale_id}, call_level=_api_level, debug_level=_api_debug_level-1)
                if not pointofsale:
                    msg = f'pointofsale not found'
                    api_result = {'api_status': 'error', 'api_message': msg, 'api_action': _api_action.upper(), 'api_name': _api_name}
                    log_process_finish(_api_msgID, api_result, **_process_identity_dict)
                    return api_result
                originator='pointofsale'
                originator_id=pointofsale_id
                originator_name = pointofsale.name
            else:
                client_id = input_dict.get('client_id')
                if client_id:
                    client=dbsession.get(dbmodel.CLIENT, {'client_id':client_id}, call_level=_api_level, debug_level=_api_debug_level-1)
                    if not client:
                        msg = f'client not found'
                        api_result = {'api_status': 'error', 'api_message': msg, 'api_action': _api_action.upper(), 'api_name': _api_name}
                        log_process_finish(_api_msgID, api_result, **_process_identity_dict)
                        return api_result
                    originator='client'
                    originator_id=client_id
                    originator_name = client.email
                else:
                    msg = f'no pointofsale or consumer or client defined'
                    api_result = {'api_status': 'error', 'api_message': msg, 'api_action': _api_action.upper(), 'api_name': _api_name}
                    log_process_finish(_api_msgID, api_result, **_process_identity_dict)
                    return api_result

    if not originator or not originator_id:
        msg = f'originator not defined (pointofsale or consumer or client)'
        log_process_message('', 'error', msg, **_process_identity_dict)
        api_result = {'api_status': 'error', 'api_message': msg, 'api_action': _api_action.upper(), 'api_name': _api_name}
        log_process_finish(_api_msgID, api_result, **_process_identity_dict)
        return api_result

    input_dict.update({'originator': originator})
    input_dict.update({'originator_id': originator_id})

    if not originator_id == interaction.originator_id or originator_id == interaction.corresponder_id:
        msg = f'invalid originator [{originator_name}] for interaction [{interaction.interaction_id}]'
        api_result = {'api_status': 'error', 'api_message': msg, 'api_action': _api_action.upper(), 'api_name': _api_name}
        log_process_finish(_api_msgID, api_result, **_process_identity_dict)
        return api_result

    msg=f'originator: [{originator}] [[{originator_name}]]'
    log_process_message('', 'success', msg, **_process_identity_dict)

    #step-2: corresponder
    # corresponder_id = input_dict.get('corresponder_id')
    # if not corresponder_id:
    #     msg = f'no corresponder specified'
    #     if _api_debug_level > 0: log_process_message(_api_name, _api_entity, _api_action, 'warning',msg, call_level=_api_level, session_id=dbsession.session_id,filelog_enabled=thisApp.FILELOG_ON,print_enabled=thisApp.CONSOLE_ON)
    # else:
    #     pointofsale = dbsession.get(dbmodel.POINT_OF_SALE, {'pointofsale_id':corresponder_id}, call_level=_api_level, debug_level=_api_debug_level-1)
    #     if pointofsale:
    #         corresponder='pointofsale'
    #         corresponder_id = pointofsale.pointofsale_id
    #         corresponder_name = pointofsale.name
    #     else:
    #         xid = dbsession.get(dbmodel.CONSUMER, {'consumer_id':corresponder_id}, call_level=_api_level, debug_level=_api_debug_level-1)
    #         if xid:
    #             corresponder='consumer'
    #             corresponder_id = xid.consumer_id
    #             corresponder_name = xid.email           
    #         else:
    #             xid = dbsession.get(dbmodel.CLIENT, {'client_id':corresponder_id}, call_level=_api_level, debug_level=_api_debug_level-1)
    #             if xid:
    #                 corresponder='client'
    #                 corresponder_id=xid.client_id
    #                 corresponder_name = xid.email          
    #     xcorresponder = input_dict.get('corresponder')
    #     if xcorresponder and not xcorresponder == corresponder:
    #         msg = f'corresponder_id not valid for corresponder {xcorresponder}'
    #         api_result = {'api_status': 'error', 'api_message': msg, 'api_action': _api_action.upper(), 'api_name': _api_name}
    #         if _api_debug_level > 0: log_process_message(_api_name, _api_entity, _api_action, 'warning',msg, call_level=_api_level, session_id=dbsession.session_id,filelog_enabled=thisApp.FILELOG_ON,print_enabled=thisApp.CONSOLE_ON)

    # if corresponder_id:
    #     input_dict.update({'corresponder': corresponder})
    #     input_dict.update({'corresponder_id': corresponder_id})
    #     msg=f'corresponder: [{corresponder}] [[{corresponder_name}]]'
    #     log_process_message('', 'success', msg, **_process_identity_dict)

    # if not interaction.corresponder and not interaction.originator_id==originator_id:
    #     interaction_rec=interaction.to_dict()
    #     interaction.update({'corresponder': originator})
    #     interaction.update({'corresponder_id': originator_id})
    #     interaction = dbsession.insert(dbmodel.INTERACTION, interaction_rec, auto_commit=True, call_level=_api_level, debug_level=_api_debug_level - 1)

    interaction_message = {
        'interaction_id':interaction_id,
        'originator_id':input_dict.get('originator_id',''),
        'originator':input_dict.get('originator',''),
        'message_type':input_dict.get('message_type','message'),
        'message_record':input_dict.get('message_record',''),
        'content_type':input_dict.get('content_type','text'),
        'format':input_dict.get('format',''),
        'application_name':input_dict.get('application_name'),
        'geolocation_lat':input_dict.get('geolocation_lat'),
        'geolocation_lon':input_dict.get('geolocation_lon'),
        }

    message = dbsession.insert(dbmodel.INTERACTION_MESSAGE, interaction_message, auto_commit=True, call_level=_api_level, debug_level=_api_debug_level - 1)
    if not message:
        msg = f'interaction message add failed'
        api_result = {'api_status': 'error', 'api_message': msg, 'api_action': _api_action.upper(), 'api_name': _api_name}
        log_process_finish(_api_msgID, api_result, **_process_identity_dict)
        return api_result

    #step-6: result
    message_record = message.to_dict()
    msg=f'OK. interaction message added'
    api_result = {'api_status': 'success', 'api_message': msg, 'interaction_message_id': message.interaction_message_id, 'api_data': message_record, 'api_action': _api_action.upper(), 'api_name': _api_name}
    log_process_finish(_api_msgID, api_result, **_process_identity_dict)    
    return api_result
#::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
def dbapi_bank(dbsession, action, input_dict, filter_dict={}, caller_dict={}, call_level=-1,debug_level=-1):
    _api_name = "dbapi_bank"
    _api_entity = 'BANK'
    _api_action = action
    _api_msgID = set_api_msgID(_api_name, _api_action, _api_entity)    
    _api_debug_level = set_api_debug_level(_api_name, debug_level,dbsession)
    _api_level = call_level + 1
    _api_session_id = dbsession.session_id
    _api_indent_level=_api_level
    _api_indent_method='AUTO'

    _process_identity_dict = set_process_identity_dict('api', _api_name, _api_action, _api_entity, _api_msgID, _api_msgID, _api_session_id, _api_debug_level, print_enabled, filelog_enabled, log_file, errors_file, debug_file, _api_indent_level, _api_indent_method)
    _process_call_area = set_process_caller_area(_process_identity_dict, caller_dict)

    log_process_start(_api_msgID,**_process_identity_dict)

    log_process_input('', 'input_dict', input_dict,**_process_identity_dict)
    log_process_input('', 'filter_dict', filter_dict,**_process_identity_dict)
    log_process_input('', 'caller_dict', caller_dict,**_process_identity_dict)

    action_result = dbsession.table_action(dbmodel.BANK, action , input_dict, filter_dict, caller_dict={}, api_name=_api_name, api_entity=_api_entity, auto_commit=True, call_level=_api_level, debug_level=_api_debug_level-1)
    api_result = action_result
    api_result.update({'api_action': _api_action, 'api_name': _api_name})
    
    log_process_finish(_api_msgID, api_result, **_process_identity_dict)    
    return api_result
#::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
def dbapi_bank_authorization(dbsession, action, input_dict, filter_dict={}, caller_dict={}, call_level=-1,debug_level=-1):
    _api_name = "dbapi_bank_authorization"
    _api_entity = 'BANK_AUTHORIZATION'
    _api_action = action
    _api_msgID = set_api_msgID(_api_name, _api_action, _api_entity)    
    _api_debug_level = set_api_debug_level(_api_name, debug_level,dbsession)
    _api_level = call_level + 1
    _api_session_id = dbsession.session_id
    _api_indent_level=_api_level
    _api_indent_method='AUTO'

    _process_identity_dict = set_process_identity_dict('api', _api_name, _api_action, _api_entity, _api_msgID, _api_msgID, _api_session_id, _api_debug_level, print_enabled, filelog_enabled, log_file, errors_file, debug_file, _api_indent_level, _api_indent_method)
    _process_call_area = set_process_caller_area(_process_identity_dict, caller_dict)

    log_process_start(_api_msgID,**_process_identity_dict)

    log_process_input('', 'input_dict', input_dict,**_process_identity_dict)
    log_process_input('', 'filter_dict', filter_dict,**_process_identity_dict)
    log_process_input('', 'caller_dict', caller_dict,**_process_identity_dict)

    action_result = dbsession.table_action(dbmodel.BANK_AUTHORIZATION, action , input_dict, filter_dict, caller_dict={}, api_name=_api_name, api_entity=_api_entity, auto_commit=True, call_level=_api_level, debug_level=_api_debug_level-1)
    api_result = action_result
    api_result.update({'api_action': _api_action, 'api_name': _api_name})
    
    log_process_finish(_api_msgID, api_result, **_process_identity_dict)    
    return api_result
#::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
def dbapi_bank_subscription(dbsession, action, input_dict, filter_dict={}, caller_dict={}, call_level=-1,debug_level=-1):
    _api_name = "dbapi_bank_subscription"
    _api_entity = 'BANK_SUBSCRIPTION'
    _api_action = action
    _api_msgID = set_api_msgID(_api_name, _api_action, _api_entity)    
    _api_debug_level = set_api_debug_level(_api_name, debug_level,dbsession)
    _api_level = call_level + 1
    _api_session_id = dbsession.session_id
    _api_indent_level=_api_level
    _api_indent_method='AUTO'

    _process_identity_dict = set_process_identity_dict('api', _api_name, _api_action, _api_entity, _api_msgID, _api_msgID, _api_session_id, _api_debug_level, print_enabled, filelog_enabled, log_file, errors_file, debug_file, _api_indent_level, _api_indent_method)
    _process_call_area = set_process_caller_area(_process_identity_dict, caller_dict)

    log_process_start(_api_msgID,**_process_identity_dict)

    log_process_input('', 'input_dict', input_dict,**_process_identity_dict)
    log_process_input('', 'filter_dict', filter_dict,**_process_identity_dict)
    log_process_input('', 'caller_dict', caller_dict,**_process_identity_dict)

    action_result = dbsession.table_action(dbmodel.BANK_SUBSCRIPTION, action , input_dict, filter_dict, caller_dict={}, api_name=_api_name, api_entity=_api_entity, auto_commit=True, call_level=_api_level, debug_level=_api_debug_level-1)
    api_result = action_result
    api_result.update({'api_action': _api_action, 'api_name': _api_name})
    
    log_process_finish(_api_msgID, api_result, **_process_identity_dict)    
    return api_result
#::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
def dbapi_bank_account(dbsession, action, input_dict, filter_dict={}, caller_dict={}, call_level=-1,debug_level=-1):
    _api_name = "dbapi_bank_account"
    _api_entity = 'BANK_ACCOUNT'
    _api_action = action
    _api_msgID = set_api_msgID(_api_name, _api_action, _api_entity)    
    _api_debug_level = set_api_debug_level(_api_name, debug_level,dbsession)
    _api_level = call_level + 1
    _api_session_id = dbsession.session_id
    _api_indent_level=_api_level
    _api_indent_method='AUTO'

    _process_identity_dict = set_process_identity_dict('api', _api_name, _api_action, _api_entity, _api_msgID, _api_msgID, _api_session_id, _api_debug_level, print_enabled, filelog_enabled, log_file, errors_file, debug_file, _api_indent_level, _api_indent_method)
    _process_call_area = set_process_caller_area(_process_identity_dict, caller_dict)

    log_process_start(_api_msgID,**_process_identity_dict)

    log_process_input('', 'input_dict', input_dict,**_process_identity_dict)
    log_process_input('', 'filter_dict', filter_dict,**_process_identity_dict)
    log_process_input('', 'caller_dict', caller_dict,**_process_identity_dict)

    action_result = dbsession.table_action(dbmodel.BANK_ACCOUNT, action , input_dict, filter_dict, caller_dict={}, api_name=_api_name, api_entity=_api_entity, auto_commit=True, call_level=_api_level, debug_level=_api_debug_level-1)
    api_result = action_result
    api_result.update({'api_action': _api_action, 'api_name': _api_name})
    
    log_process_finish(_api_msgID, api_result, **_process_identity_dict)    
    return api_result
#::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
#::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
#::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
#::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
def dbapi_get_bank_account_id(dbsession, any_accountid,caller_area={},debug_level=-1):
    if not any_accountid:
        return None

    _api_name = "dbapi_get_bank_account_id"
    _api_entity = 'BANK_ACCOUNT'
    _api_action = 'get'
    _api_msgID = set_api_msgID(_api_name, _api_action, _api_entity)    
    _api_debug_level = set_api_debug_level(_api_name, debug_level,dbsession)
    _api_level = caller_area.get('call_level',0)
    _api_session_id = dbsession.session_id
    _api_indent_level=_api_level
    _api_indent_method='AUTO'

    _process_identity_dict = set_process_identity_dict('api', _api_name, _api_action, _api_entity, _api_msgID, _api_msgID, _api_session_id, _api_debug_level, print_enabled, filelog_enabled, log_file, errors_file, debug_file, _api_indent_level, _api_indent_method)
    _process_call_area = set_process_caller_area(_process_identity_dict, caller_dict)

    account = dbsession.get(dbmodel.BANK_ACCOUNT, {'bank_account_id': any_accountid}, caller_info=caller_area, call_level=_api_level, debug_level=_api_debug_level - 1)
    if account:
        bank_account_id = account.bank_account_id
    else:
        account = dbsession.get(dbmodel.BANK_ACCOUNT, {'bank_accountID': any_accountid}, caller_info=_process_call_area, call_level=_api_level, debug_level=_api_debug_level - 1)
        if account:
            bank_account_id = account.bank_account_id
        else:
            bank_account_id = None
    return bank_account_id
#::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
#::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
#::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
#::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
#::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
# #::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
# def dbapi_consumer_banksubscription_register(dbsession, input_dict, filter_dict={}, caller_dict={}, call_level=-1,debug_level=-1):
#     _api_name = "dbapi_bank_subscription"
#     _api_entity = 'BANK_SUBSCRIPTION'
#     _api_action = action
#     _api_msgID = set_api_msgID(_api_name, _api_action, _api_entity)    
#     _api_debug_level = set_api_debug_level(_api_name, debug_level,dbsession)
#     _api_level = call_level + 1
#     _api_session_id = dbsession.session_id
#     _api_indent_level=_api_level
#     _api_indent_method='AUTO'

#     _process_identity_dict = set_process_identity_dict('api', _api_name, _api_action, _api_entity, _api_msgID, _api_msgID, _api_session_id, _api_debug_level, print_enabled, filelog_enabled, log_file, errors_file, debug_file, _api_indent_level, _api_indent_method)
#     _process_call_area = set_process_caller_area(_process_identity_dict, caller_dict)

#     log_process_start(_api_msgID,**_process_identity_dict)

#     log_process_input('', 'input_dict', input_dict,**_process_identity_dict)
#     log_process_input('', 'filter_dict', filter_dict,**_process_identity_dict)
#     log_process_input('', 'caller_dict', caller_dict,**_process_identity_dict)

#     consumer = consumers.get(input_dict,user=user)
#     if not consumer:
#         msg = f'consumer not found'
#         #log_message(msg,msgType='error')
#         return {'api_status': 'error', 'api_message': msg}
    
#     if not consumer.get('status')=='Active':
#         msg = f"consumer not Active.(status:{consumer.get('status','')})"
#         #log_message(msg,msgType='error')
#         return {'api_status': 'error', 'api_message': msg}

#     consumer_id=consumer.get('consumer_id')
#     consumer_name=consumer.get('name')

#     input_dict.update({'owner_type': 'consumer'})
#     input_dict.update({'owner_id': consumer_id})
#     input_dict.update({'owner_name': consumer_name})

#     result=dbapi_bank_subscription_register(input_dict, user=user)
#     return result
############################
# def dbapi_bank_register(bank_record, user='?', device_uid=None, geolocation_lat=None, geolocation_lon=None):
#     bank = banks.refresh(bank_record)
#     return bank
#     # bank = banks.refresh(bank_record, user=user)
#     # if not bank:
#     #     msg = f'bank not registered (not found)'
#     #     #log_message(msg,msgType='error')
#     #     return {'api_status': 'error', 'api_message': msg}

#     # if not bank.get('status')=='Active':
#     #     msg = f"bank is not Active.(status:{bank.get('status','')})"
#     #     #log_message(msg,msgType='warning')
#     #     #return {'api_status': 'error', 'api_message': msg,'api_data':bank_subscription}

#     # msg = f"bank registered.(status:{bank.get('status','')})"
#     # return {'api_status': 'success', 'api_message': msg,'api_data':bank}
# #::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
# def dbapi_bank_update(bank_record, user='?', device_uid=None, geolocation_lat=None, geolocation_lon=None):
#     result = banks.try_update(bank_record,user=user)
#     if not result.get('api_status') == 'success':
#         return result
#     bank=result.get('api_data')
#     if not bank:
#         msg = f'bank not updated. (not found-system error)'
#         #log_message(msg,msgType='error')
#         return {'api_status': 'error', 'api_message': msg}

#     return result
# #::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
# def dbapi_bank_subscription_register(dbsession, input_dict, filter_dict={}, caller_dict={}, call_level=-1,debug_level=-1):
#     _api_name = "dbapi_bank_subscription"
#     _api_entity = 'BANK_SUBSCRIPTION'
#     _api_action = action
#     _api_msgID = set_api_msgID(_api_name, _api_action, _api_entity)    
#     _api_debug_level = set_api_debug_level(_api_name, debug_level,dbsession)
#     _api_level = call_level + 1
#     _api_session_id = dbsession.session_id
#     _api_indent_level=_api_level
#     _api_indent_method='AUTO'

#     _process_identity_dict = set_process_identity_dict('api', _api_name, _api_action, _api_entity, _api_msgID, _api_msgID, _api_session_id, _api_debug_level, print_enabled, filelog_enabled, log_file, errors_file, debug_file, _api_indent_level, _api_indent_method)
#     _process_call_area = set_process_caller_area(_process_identity_dict, caller_dict)

#     log_process_start(_api_msgID,**_process_identity_dict)

#     log_process_input('', 'input_dict', input_dict,**_process_identity_dict)
#     log_process_input('', 'filter_dict', filter_dict,**_process_identity_dict)
#     log_process_input('', 'caller_dict', caller_dict,**_process_identity_dict)

#     result = bank_subscriptions.refresh(input_dict)
#     return result
#     # bank_subscription = bank_subscriptions.refresh(input_dict, user=user)
#     # if not bank_subscription:
#     #     msg = f'bank_subscription not registered (not found)'
#     #     #log_message(msg,msgType='error')
#     #     return {'api_status': 'error', 'api_message': msg}

#     # if not bank_subscription.get('status')=='Active':
#     #     msg = f"bank_subscription is not Active.(status:{bank_subscription.get('status','')})"
#     #     #log_message(msg,msgType='error')
#     #     return {'api_status': 'error', 'api_message': msg,'api_data':bank_subscription}

#     # msg = f"bank_subscription registered.(status:{bank_subscription.get('status','')})"
#     # return {'api_status': 'success', 'api_message': msg,'api_data':bank_subscription}
# #::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
# def dbapi_bank_account_register(dbsession, bank_account_record, filter_dict={}, caller_dict={}, call_level=-1,debug_level=-1):
#     _api_name = "dbapi_bank_subscription"
#     _api_entity = 'BANK_SUBSCRIPTION'
#     _api_action = action
#     _api_msgID = set_api_msgID(_api_name, _api_action, _api_entity)    
#     _api_debug_level = set_api_debug_level(_api_name, debug_level,dbsession)
#     _api_level = call_level + 1
#     _api_session_id = dbsession.session_id
#     _api_indent_level=_api_level
#     _api_indent_method='AUTO'

#     _process_identity_dict = set_process_identity_dict('api', _api_name, _api_action, _api_entity, _api_msgID, _api_msgID, _api_session_id, _api_debug_level, print_enabled, filelog_enabled, log_file, errors_file, debug_file, _api_indent_level, _api_indent_method)
#     _process_call_area = set_process_caller_area(_process_identity_dict, caller_dict)

#     log_process_start(_api_msgID,**_process_identity_dict)

#     log_process_input('', 'input_dict', input_dict,**_process_identity_dict)
#     log_process_input('', 'filter_dict', filter_dict,**_process_identity_dict)
#     log_process_input('', 'caller_dict', caller_dict,**_process_identity_dict)

#     bank_subscription = bank_subscriptions.get(bank_account_record)
#     if not bank_subscription:
#         merchant_id = bank_account_record.get('merchant_id')
#         if merchant_id:
#             bank_account_record.update({'owner_type': 'merchant', 'owner_id': merchant_id})
#             bank_subscription = bank_subscriptions.get(bank_account_record)
#             if not bank_subscription:
#                 pointofsale_id = bank_account_record.get('pointofsale_id')
#                 if pointofsale_id:
#                     bank_account_record.update({'owner_type': 'pointofsale', 'owner_id': pointofsale_id})
#                     bank_subscription = bank_subscriptions.get(bank_account_record)
#                     if not bank_subscription:
#                         consumer_id = bank_account_record.get('consumer_id')
#                         if consumer_id:
#                             bank_account_record.update({'owner_type': 'consumer', 'owner_id': consumer_id})
#                             bank_subscription = bank_subscriptions.get(bank_account_record)
#                             if not bank_subscription:
#                                 client_id = bank_account_record.get('client_id')
#                                 if client_id:
#                                     bank_account_record.update({'owner_type': 'client', 'owner_id': client_id})
#                                     bank_subscription = bank_subscriptions.get(bank_account_record)
#     if not bank_subscription:
#         msg = f'bank_subscription not found'
#         #log_message(msg,msgType='error')
#         return {'api_status': 'error', 'api_message': msg}
    
#     if not bank_subscription.get('status')=='Active':
#         msg = f"bank_subscription not Active.(status:{bank_subscription.get('status','')})"
#         #log_message(msg,msgType='error')
#         return {'api_status': 'error', 'api_message': msg}

#     bank_subscription_id=bank_subscription.get('bank_subscription_id')
#     bank_subscription_name=bank_subscription.get('owner_name')
#     bank_subscription_type=bank_subscription.get('owner_type')

#     bank_account_record.update({'owner_type':bank_subscription_type})
#     bank_account_record.update({'owner_id': bank_subscription_id})
#     bank_account_record.update({'owner_name': bank_subscription_name})
    
#     result=BANK_ACCOUNTS.insert_or_update(bank_account_record, user=user)
#     return result
#::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
# def xdbapi_bank_authorizations_process(bank_code, authorization_code,authorization_token, user='?', device_uid=None, geolocation_lat=None, geolocation_lon=None):
#     cutoff_timestamp = datetime.datetime.utcnow() - datetime.timedelta(seconds=60*60)
#     cutoff_timestamp_str= cutoff_timestamp.strftime('%Y-%m-%d %H:%M:%S')

#     pending_authorizations_filter=f"status='Pending' and bank_code='{bank_code}' and row_timestamp>'{cutoff_timestamp_str}'"
#     pending_authorizations = bank_authorizations.retrieve_records(pending_authorizations_filter)
#     if len(pending_authorizations) <= 0:
#         msg = f'no pending authorizations for bank [{bank_code}]'
#         print(msg)
#         reply = {'api_status': 'error', 'api_message': msg}
#         return reply
        
#     print(f'{len(pending_authorizations)} pending_authorizations in bank [{bank_code}]')
#     ix = 0
#     failed = 0
#     authorized = 0
#     for pending_authorization in pending_authorizations:
#         ix = ix + 1
#         subscription_id = pending_authorization.get('bank_subscriptionID')
#         # client_id=pending_authorization.get('client_id')
#         bank_code = pending_authorization.get('bank_code')
#         # print(f'{ix}. subscription {bank_code} {subscription_id} client:{client_id}')
#         commit_result = openBankingAPI.commit_subscription(bank_code, authorization_token, subscription_id)
#         if commit_result.get('status') == 'success':
#             print(f'ok-{subscription_id}')
#             pending_authorization.update({'status': 'Committed'})
#             pending_authorization.update({'authorization_code': authorization_code})
#             pending_authorization.update({'authorization_token': authorization_token})
#             res = bank_authorizations.try_update(pending_authorization)
#             if not res.get('api_status')=='success':
#                 errorMsg = res.get('api_message')
#                 msg=f"{ix}. subscription [{bank_code} {subscription_id}]: bank_authorizations UPDATE FAILED: {errorMsg}"
#                 print(msg)
#                 failed = failed + 1
#                 # pending_authorization.update({'status': 'NotCommitted'})
#                 # pending_authorization.update({'authorization_code': authorization_code})
#                 # pending_authorization.update({'authorization_token': authorization_token})
#                 # pending_authorization.update({'error': errorMsg})
#                 # res = db.bank_authorizations.try_update(pending_authorization)
#             else:
#                 input_dict = pending_authorization
#                 input_dict.update({'status': 'Active'})
#                 result=dbapi_client_banksubscription_register(input_dict)
#                 if not result.get('api_status')=='success':
#                     failed = failed + 1
#                     errorMsg = result.get('api_message')
#                     msg=f"{ix}. subscription [{bank_code} {subscription_id}]: bank_authorizations UPDATE FAILED: {errorMsg}"
#                     print(msg)
#                 else:
#                     authorized = authorized + 1
#                     msg=f"f{ix}. subscription [{bank_code} {subscription_id}]: bank_subscription REGISTERED: {result.get('api_message')}"
#                     print(msg)
#                     #register accounts
#                     pending_authorization.update({'status': 'Registered','error':''})
#                     # pending_authorization.update({'authorization_code': authorization_code})
#                     # pending_authorization.update({'authorization_token': authorization_token})
#                     # pending_authorization.update({'error': ''})
#                     res = bank_authorizations.try_update(pending_authorization)
#         else:
#             errorMsg = commit_result.get('message')
#             msg='no accounts selected so far'
#             print(f"{ix}. subscription [{bank_code} {subscription_id}] COMMIT FAILED:{errorMsg}")
#             if errorMsg.upper().find('already active/revoked'.upper())>=0:
#                 #failed = failed + 1
#                 pending_authorization.update({'status': 'Already_Registered','error': errorMsg})
#                 #pending_authorization.update({'authorization_code': authorization_code})
#                 #pending_authorization.update({'authorization_token': authorization_token})
#                 res = bank_authorizations.try_update(pending_authorization)

#     # msg=f'OK.authorization code received ({authorization_code}). {authorized} subscriptions authorized, {failed} failed.'
#     # reply = {'api_status': 'success', 'api_message': msg}
#     # return jsonify( reply )

#     #delete expired
#     delete_where_expression = f"status='Expired'"
#     result = bank_authorizations.delete_rows(delete_where_expression)
#     deleted_rows = result.get('deleted_records', 0)

#     #mark expired pending authorizations
#     cutoff_timestamp = datetime.datetime.utcnow() - datetime.timedelta(seconds=60*60*60)
#     cutoff_timestamp_str= cutoff_timestamp.strftime('%Y-%m-%d %H:%M:%S')
#     where_expression = f"status='Pending' and row_timestamp<'{cutoff_timestamp_str}'"
#     update_expr={'status':'Expired'}
#     result = bank_authorizations.update_rows(where_expression, update_expr)
#     expired_rows = result.get('changed_records', 0)

#     msg=f'authorizations reorganized with {expired_rows} authorizations expired, {deleted_rows} removed.'
#     print(msg)
    
#     if authorized>0:
#         msg = f'OK.authorization code received. {authorized} subscriptions authorized, {failed} failed.'
#     else:
#         msg = f'authorization code NOT received. {authorized} subscriptions authorized, {failed} failed.'
#     # return msg
#     # msg = f'OK.authorization code received. {authorized} subscriptions authorized, {failed} failed.'
#::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
# def dbapi_bank_authorizations_reorganization(user='?', device_uid=None, geolocation_lat=None, geolocation_lon=None):
#     #delete expired
#     delete_where_expression = f"status='Expired'"
#     result = bank_authorizations.delete_rows(delete_where_expression)
#     deleted_rows = result.get('deleted_records', 0)

#     #mark expired pending authorizations
#     cutoff_timestamp = datetime.datetime.utcnow() - datetime.timedelta(seconds=60*60*60)
#     cutoff_timestamp_str= cutoff_timestamp.strftime('%Y-%m-%d %H:%M:%S')
#     where_expression = f"status='Pending' and row_timestamp<'{cutoff_timestamp_str}'"
#     update_expr={'status':'Expired'}
#     result = bank_authorizations.update_rows(where_expression, update_expr)
#     expired_rows = result.get('changed_records', 0)

#     msg=f'authorizations reorganized with {expired_rows} authorizations expired, {deleted_rows} removed.'
#     print(msg)
#     return {'api_status':'success','api_message':msg,'expired_records':expired_rows,'deleted_records':deleted_rows}
#::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
def dbapi_cleanup_bank_authorizations(dbsession, caller_dict={}, call_level=-1,debug_level=-1):
    _api_name = "dbapi_cleanup_bank_authorizations"
    _api_entity = 'BANK_AUTHORIZATION'
    _api_action = 'CLEANUP'
    _api_msgID = set_api_msgID(_api_name, _api_action, _api_entity)    
    _api_debug_level = set_api_debug_level(_api_name, debug_level,dbsession)
    _api_level = call_level + 1
    _api_session_id = dbsession.session_id
    _api_indent_level=_api_level
    _api_indent_method='AUTO'

    _process_identity_dict = set_process_identity_dict('api', _api_name, _api_action, _api_entity, _api_msgID, _api_msgID, _api_session_id, _api_debug_level, print_enabled, filelog_enabled, log_file, errors_file, debug_file, _api_indent_level, _api_indent_method)
    _process_call_area = set_process_caller_area(_process_identity_dict, caller_dict)

    log_process_start(_api_msgID,**_process_identity_dict)

    deleted_rows = 0
    expired_rows = 0
    #under construction


    where_expression = {'status': 'Expired'}
    # deleted_result = dbsession.delete_rows(dbmodel.BANK_AUTHORIZATION, where_expression, auto_commit=True)
    # deleted_rows = deleted_result.get('rows_deleted', 0)
    
    cutoff_timestamp = datetime.datetime.utcnow() - datetime.timedelta(seconds=60*60*60)
    cutoff_timestamp_str= cutoff_timestamp.strftime('%Y-%m-%d %H:%M:%S')
    where_expression = f"status='Pending' and row_timestamp<'{cutoff_timestamp_str}'"

    # rows = City.query.filter(sw_lat <= City.latitude, City.latitude <= ne_lat,
    #                         sw_lng <= City.longitude, City.longitude <= ne_lng)...cont....
    # #nowString = datetime.datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S')
    # #where_expression = f"expiryDT<'{datetime.datetime.utcnow()}'"
    # where_expression = {'expiryDT': {datetime.datetime.utcnow()}}
    update_dict = {'status': 'Expired'}

    # expired_result = dbsession.update_rows(dbmodel.BANK_AUTHORIZATION, update_dict,where_expression, auto_commit=True)
    # expired_rows = expired_result.get('rows_updated', 0)
    
    msg = f'bank_authorizations cleaned with {expired_rows} authorizations expired, {deleted_rows} removed.'

    api_result = {'api_status': 'success', 'api_message': msg, 'rows_expired': expired_rows, 'rows_removed': deleted_rows}
    log_process_finish(_api_msgID, api_result, **_process_identity_dict)    
    return api_result
#::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
# def dbapi_client_banksubscription_register(dbsession, input_dict, filter_dict={}, caller_dict={}, call_level=-1,debug_level=-1):
#     _api_name = "dbapi_bank_subscription"
#     _api_entity = 'BANK_SUBSCRIPTION'
#     _api_action = 'register'
#     _api_msgID = set_api_msgID(_api_name, _api_action, _api_entity)    
#     _api_debug_level = set_api_debug_level(_api_name, debug_level,dbsession)
#     _api_level = call_level + 1
#     _api_session_id = dbsession.session_id
#     _api_indent_level=_api_level
#     _api_indent_method='AUTO'

#     _process_identity_dict = set_process_identity_dict('api', _api_name, _api_action, _api_entity, _api_msgID, _api_msgID, _api_session_id, _api_debug_level, print_enabled, filelog_enabled, log_file, errors_file, debug_file, _api_indent_level, _api_indent_method)
#     _process_call_area = set_process_caller_area(_process_identity_dict, caller_dict)

#     log_process_start(_api_msgID,**_process_identity_dict)

#     log_process_input('', 'input_dict', input_dict,**_process_identity_dict)
#     log_process_input('', 'filter_dict', filter_dict,**_process_identity_dict)
#     log_process_input('', 'caller_dict', caller_dict,**_process_identity_dict)

#     bank_subscriptionID = input_dict.get('bank_subscriptionID')
#     if not bank_subscriptionID:
#         msg = f'bank_subscriptionID not provided'
#         api_result={'api_status': 'error', 'api_message': msg}
#         log_process_finish(_api_msgID, api_result, **_process_identity_dict)    
#         return api_result

#     client = dbsession.get(dbmodel.CLIENT, input_dict,call_level=_api_level-1, debug_level=_api_debug_level-1)
#     if not client:
#         msg = f'client not found'
#         api_result={'api_status': 'error', 'api_message': msg}
#         log_process_finish(_api_msgID, api_result, **_process_identity_dict)    
#         return api_result

#     if not client.get('status')=='Active':
#         msg = f"client not Active.(status:{client.get('status','')})"
#         api_result={'api_status': 'error', 'api_message': msg}
#         log_process_finish(_api_msgID, api_result, **_process_identity_dict)    
#         return api_result

#     bank = dbsession.get(dbmodel.BANK, input_dict,call_level=_api_level-1, debug_level=_api_debug_level-1)
#     if not bank:
#         msg = f'bank not found'
#         api_result={'api_status': 'error', 'api_message': msg}
#         log_process_finish(_api_msgID, api_result, **_process_identity_dict)    
#         return api_result
    
#     if not bank.get('status')=='Active':
#         msg = f"bank not Active.(status:{bank.get('status','')})"
#         api_result={'api_status': 'error', 'api_message': msg}
#         log_process_finish(_api_msgID, api_result, **_process_identity_dict)    
#         return api_result

#     authorization = dbsession.get(dbmodel.BANK_AUTHORIZATION, input_dict,call_level=_api_level-1, debug_level=_api_debug_level-1)
#     if not authorization:
#         msg = f'no authorization matched in bank_authorizations'
#         api_result={'api_status': 'error', 'api_message': msg}
#         log_process_finish(_api_msgID, api_result, **_process_identity_dict)    
#         return api_result

#     if not authorization.get('status') in ('Committed','Authorized'):
#         msg = f"authorization not provided by client. status:{authorization.get('status')}"
#         api_result={'api_status': 'error', 'api_message': msg}
#         log_process_finish(_api_msgID, api_result, **_process_identity_dict)    
#         return api_result

#     bank_authorization_id = authorization.bank_authorization_id
#     client_id=client.get('client_id')
#     client_email=client.get('email')
#     client_type=client.get('client_type')

#     input_dict.update({'client_id': client_id})
#     input_dict.update({'client_type': client_type})
#     input_dict.update({'client_name': client_email})
#     input_dict.update({'bank_authorization_id':bank_authorization_id})        
#     input_dict.update({'bank_code': bank.bank_code})
#     input_dict.update({'bank_BIC': bank.bank_BIC})
#     input_dict.update({'bank_id': bank.bank_id})
#     #input_dict.update({'bank_subscriptionID': bank_subscriptionID})
#     input_dict.update({'status': 'Active'})
    
#     # result=dbapi_bank_subscription_register(input_dict, user=user)
#     # api_result=dbapi_bank_subscription(dbsession, action, input_dict, filter_dict={}, caller_dict={}, call_level=-1,debug_level=-1):
#     # return result

#     api_result = dbsession.table_action(dbmodel.BANK_SUBSCRIPTION, 'REGISTER' , input_dict, filter_dict, caller_dict={}, api_name=_api_name, api_entity=_api_entity, auto_commit=True, call_level=_api_level, debug_level=_api_debug_level-1)
#     log_process_finish(_api_msgID, api_result, **_process_identity_dict)    
#     return api_result
#::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::

#::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
#::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
#::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
def set_api_msgID(api_name,api_action,api_entity):
    msgid=f"#C0#api #C9#{api_name}#C0# [{api_entity}]#C0# action [[{api_action.upper()}]]#C0#"
    return msgid
#::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
def set_api_debug_level(api_name, this_debug=None,dbsession=None):
    this_debug_level=get_debug_option_as_level(this_debug)
    if this_debug_level >= 0:
        return this_debug_level

    if dbsession:
        session_debug_level = get_debug_option_as_level(dbsession.debug)
    else:
        session_debug_level = -1

    api_name_debug = master_configuration['apis'].get(api_name, {}).get('debug_level', -1)
    debug_level1 = get_debug_option_as_level(api_name_debug)

    try:
        debug_level2 = get_debug_option_as_level(thisApp.application_configuration.database_api_debug)
    except:
        debug_level2 = -1
    return max(debug_level1,debug_level2,session_debug_level)
#::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
def set_process_identity_dict(proc_prefix, proc_name, proc_action, proc_entity, proc_msgID, proc_level, proc_session_id, debug_level, print_enabled, filelog_enabled, log_file, errors_file, indent_level, indent_method):
    process_identification_dict = {
        'process_prefix':proc_prefix,
        'process_name':proc_name,
        'process_action':proc_action,
        'process_entity':proc_entity,
        'process_msgID':proc_msgID,
        'process_level':proc_level,
        'process_session_id':proc_session_id,
        'debug_level': debug_level,
        'print_enabled':print_enabled,
        'filelog_enabled':filelog_enabled,
        'log_file':log_file,
        'errors_file':errors_file,
        'indent_level':indent_level,
        'indent_method':indent_method,
        }
    return process_identification_dict
#::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
def set_process_caller_area(this_process_identity_dict, _process_call_area):
    caller_area = _process_call_area.copy()
    
    call_level = caller_area.get('call_level', -1)
    call_level = call_level + 1
    caller_area.update({'call_level':call_level})

    if not caller_area.get('call_stack'):
        caller_area.update({'call_stack': []})
    caller_area['call_stack'].append(this_process_identity_dict)

    caller_area.update(this_process_identity_dict)

    print_enabled = this_process_identity_dict.get('print_enabled')
    if print_enabled == None:
        print_enabled = caller_area.get('print_enabled')
    if print_enabled == None:
        print_enabled = thisApp.CONSOLE_ON
    caller_area.update({'print_enabled':print_enabled})

    filelog_enabled = this_process_identity_dict.get('filelog_enabled')
    if filelog_enabled == None:
        filelog_enabled = caller_area.get('filelog_enabled')
    if filelog_enabled == None:
        filelog_enabled = thisApp.FILELOG_ON
    caller_area.update({'filelog_enabled':filelog_enabled})

    log_file = this_process_identity_dict.get('log_file', '')
    if not log_file:
        log_file = caller_area.get('log_file','')
    if not log_file:
        log_file = thisApp.log_file_name
    caller_area.update({'log_file':log_file})

    caller_area.update({'module_id':module_id})
    caller_area.update({'module_file':__file__})

    return caller_area
#::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
def test_api(caller_dict={}, call_level=-1,debug_level=-1):
    _api_name = "dbapi_interaction_message_add"
    _api_entity = 'INTERACTION_MESSAGE'
    _api_action = 'ADD'
    _api_msgID = set_api_msgID(_api_name, _api_action, _api_entity)
    _api_debug_level = set_api_debug_level(_api_name, debug_level,None)
    _api_level = call_level + 1
    _process_identity_dict = {
        'process_name':_api_name,
        'process_action':_api_action,
        'process_entity':_api_entity,
        'process_prefix':'table',
        'process_msgID':_api_msgID,
        'process_level':_api_level,
        'process_session_id':'dbsession.session_id',
        'process_logfile':'',
        'debug_level': _api_debug_level,
        'indent_level':_api_level,
        'indent_method':'AUTO',
        'print_enabled':None,
        'filelog_enabled':None,
        }

    print('1caller_dict=',caller_dict)
    caller_area = set_process_caller_area(_process_identity_dict, caller_dict)
    print('2caller_area=',caller_area)
    print('3caller_dict=', caller_dict)
    return
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

#build the api configuration
functions_ids=['dbapi_']
thisModuleObj = sys.modules[__name__]
dbapis = thisApp.collect_function_names_from_module(thisModuleObj, functions_ids)
dbapis.sort()

if not master_configuration.get('apis'):
    master_configuration.update({'apis': {}})
    
for ix in range(0, len(dbapis)):
    api_name=dbapis[ix]
    if not master_configuration.get('apis',{}).get(api_name):
        api_entry = {dbapis[ix]: {'status': 'Active', 'version':'1.1','debug_level': -1}}
        master_configuration['apis'].update(api_entry)

if get_debug_option_as_level(thisApp.application_configuration.database_api_debug) > 0:
    for ix in range(0, len(dbapis)):
        if dbapis[ix] in ('set_api_msgID', 'set_api_debug_level'):
            continue
        msg=f'from [[{module_id}]] import [{dbapis[ix]}]'
        log_message(msg)
#::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
save_module_configuration(module_identityDictionary, master_configuration, print_enabled=consolelog_enabled, filelog_enabled=filelog_enabled)
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
    caller_dict={'aaaa': '11111'}
    print('0caller_dict=', caller_dict)
    test_api(caller_dict, call_level=-1, debug_level=-1)
    print('4caller_dict=', caller_dict)
#::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
#::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
#::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
