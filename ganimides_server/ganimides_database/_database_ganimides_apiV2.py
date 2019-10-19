# -*- coding: utf-8 -*-
#https://www.pythoncentral.io/series/python-sqlalchemy-database-tutorial/
import os
import sys
import datetime



module_ProgramName = os.path.splitext(os.path.basename(__file__))[0]
module_id = '{}'.format(module_ProgramName)
module_version = 0.1

from _onlineApp import thisApp
from _onlineApp import print_message,print_api_result,log_message,colorized_message
from _database_ganimides_engine import db_session, db_table_action
session = db_session.session
import _database_ganimides_schema as dbschema
import _database_ganimides_model as dbmodel
#::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
#::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
#::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
#::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
#::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
# api services : database apis
#::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
#::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
#::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
def dbapi_device(session, action, input_dict, filter_dict={}, caller_dict={}):
    _api_name = "dbapi_device"
    _api_entity = 'DEVICE'
    _api_action = action
    debug = False
    if action.upper in ('REGISTER','UNREGISTER'):
        dbapi_device_register_unregister(input_dict,action)
        return
        
    msgPrefix=f"#C9#{_api_name}#RESET# [{_api_action.upper()}]#RESET#"

    msgStart=f"{msgPrefix} start: input_dict=[[{input_dict}]]"
    if thisApp.application_configuration.database_api_debug or debug: print_message(msgStart)

    action_result = db_table_action(dbmodel.DEVICE, action, input_dict, filter_dict, caller_dict={}, api_name=_api_name, api_entity=_api_entity, auto_commit=True, call_level=1)
    api_result = action_result
    api_result.update({'api_action': _api_action, 'api_name': _api_name})
    
    if thisApp.application_configuration.database_api_debug or debug: print_api_result(f"{msgPrefix} result:", api_result)
    return api_result
#::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
def dbapi_device_log(session, device_uid, application_name, geolocation_lat, geolocation_lon, client_id):
    #https://www.pythoncentral.io/series/python-sqlalchemy-database-tutorial/
    _api_name="dbapi_device_log"
    _api_action = 'device_log'
    _api_entity = 'DEVICE'
    debug = False
    msgPrefix=f"#C9#{_api_name}#RESET# [{_api_action.upper()}]#RESET#"

    msgStart=f"{msgPrefix} start: device_uid=[[[{device_uid}]]] application_name=[[[{application_name}]]]"
    if thisApp.application_configuration.database_api_debug or debug: print_message(msgStart)

    now = datetime.datetime.utcnow()

    application_id=None
    application=dbschema.APPLICATIONS_TABLE.get({'application_name': application_name})
    if application:
        application_id = application.application_id

    device_record = {'device_uid': device_uid, 'last_usage_geolocation_lat': geolocation_lat, 'last_usage_geolocation_lon': geolocation_lon, 'last_usage_timestamp': now}
    usage_record = {'device_uid': device_uid, 'application_name': application_name, 'geolocation_lat': geolocation_lat, 'geolocation_lon': geolocation_lon, 'client_id': client_id}
    client_device_record = {'device_uid': device_uid, 'client_id': client_id, 'application_name': application_name, 'application_id': application_id, 'last_usage_timestamp': now}

    device = dbschema.DEVICES_TABLE.refresh(device_record,commit=False)
    device_usage = dbschema.DEVICE_USAGE_TABLE.refresh(usage_record,commit=False)
    client_device = dbschema.CLIENT_DEVICES_TABLE.refresh(client_device_record,commit=False)

    session.commit()

    if client_device:
        logged_record = client_device.to_dict()
        if device.times_used <= 1:
            msg=f"OK. new device logged"
        else:
            msg = f"OK. device logged, times_used:{device.times_used}"
        api_result = {'api_status': 'success', 'api_message': msg, 'api_data': logged_record, 'api_action': _api_action.upper(), 'api_name': _api_name}
    else:
        msg = f"device logged FAILED"
        api_result = {'api_status': 'error', 'api_message': msg, 'api_data': {}, 'api_action': _api_action.upper(), 'api_name': _api_name}

    if thisApp.application_configuration.database_api_debug or debug: print_api_result(f"{msgPrefix} result:", api_result)
    return api_result
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
def dbapi_device_logV3(session, device_uid, application_name, geolocation_lat, geolocation_lon, client_id):
    #https://www.pythoncentral.io/series/python-sqlalchemy-database-tutorial/
    #https://www.pythoncentral.io/understanding-python-sqlalchemy-session/
    #https: // www.pythoncentral.io / category / python - related - tools /
    #pythontutorial
    _api_name="dbapi_device_log"
    _api_action='device_log'
    now = datetime.datetime.utcnow()

    msgS=f"#C9#{_api_name}#RESET# start: action=[[{_api_action}]]] device_uid=[[{device_uid}]]] application_name=[[{application_name}]]"
    if thisApp.application_configuration.database_api_debug or debug: print_message(msgS)


    #client=session.query(CLIENT).filter(CLIENT.client_id==client_id).one()
    application = session.query(APPLICATION).filter(APPLICATION.application_name == application_name).one()
    application_id = application.application_id
    try:
        device = session.query(DEVICE).filter(DEVICE.device_uid == device_uid).one()
    except:
        device=None
    if not device:
        device = DEVICE(device_uid=device_uid, last_usage_geolocation_lat=geolocation_lat, last_usage_geolocation_lon=geolocation_lon, last_usage_timestamp=now)
        session.add(device)
    else:
        device.last_usage_geolocation_lat = geolocation_lat
        device.last_usage_geolocation_lon = geolocation_lon
        device.last_usage_timestamp = now
        device.times_used = device.times_used + 1

    try:
        deviceusage = session.query(DEVICE_USAGE).filter(DEVICE_USAGE.device_uid == device_uid, application_name == application_name, geolocation_lat == geolocation_lat, geolocation_lon == geolocation_lon, client_id == client_id).one()
    except:
        deviceusage = None
    if not deviceusage:
        deviceusage = DEVICE_USAGE(device_uid=device_uid, application_name=application_name, geolocation_lat=geolocation_lat, geolocation_lon=geolocation_lon, client_id=client_id)
        session.add(deviceusage)
    else:
        deviceusage = session.query(DEVICE_USAGE).filter(DEVICE_USAGE.device_uid == device_uid, application_name == application_name, geolocation_lat == geolocation_lat, geolocation_lon == geolocation_lon, client_id == client_id).one()
        deviceusage.geolocation_lat = geolocation_lat
        deviceusage.geolocation_lon = geolocation_lon
        deviceusage.last_usage_timestamp = now
        deviceusage.times_used = deviceusage.times_used + 1

    try:
        clientdevice = session.query(CLIENT_DEVICE).filter(CLIENT_DEVICE.device_uid == device_uid, application_id == application_id, client_id == client_id).one()
    except:
        clientdevice = None
    if not clientdevice:
        clientdevice = CLIENT_DEVICE(device_uid=device_uid, client_id=client_id, application_id=application_id, last_usage_timestamp=now)
        session.add(clientdevice)
    else:      
        clientdevice = session.query(CLIENT_DEVICE).filter(CLIENT_DEVICE.device_uid == device_uid, application_id == application_id, client_id == client_id).one()
        clientdevice.last_usage_timestamp = now
        clientdevice.times_used = clientdevice.times_used + 1
    
    session.commit()

    logged_record = deviceusage.to_dict()
    if device.times_used <= 1:
        msg=f"OK. new device logged"
    else:
        msg=f"OK. device logged, times_used:{device.times_used}"
    api_result = {'api_status': 'success', 'api_message': msg, 'api_data': logged_record, 'api_action': _api_action.upper(), 'api_name': _api_name}
    if thisApp.application_configuration.database_api_debug or debug: print_api_result(f"[{_api_name}] result:", api_result)
    return api_result
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
def dbapi_device_register_unregister(session, input_dict, action='Register'):
    _api_name="dbapi_device_register_unregister"
    _api_action = action
    _api_entity = 'DEVICE'
    debug = False
    actions_supported=('REGISTER', 'UNREGISTER')

    msgPrefix=f"#C9#{_api_name}#RESET# [{_api_action.upper()}]#RESET#"
    msgStart=f"{msgPrefix} start: input_dict=[[{input_dict}]]"
    if thisApp.application_configuration.database_api_debug or debug: print_message(msgStart)

    now = datetime.datetime.utcnow()

    if action.upper() not in actions_supported:
        msg = f"action '{action}' not supported. {actions_supported}"
        api_result = {'api_status': 'error', 'api_message': msg, 'api_data': actions_supported, 'api_action': _api_action.upper(), 'api_name': _api_name}
        if thisApp.application_configuration.database_api_debug or debug: print_api_result(f"{msgPrefix} result:", api_result)
        return api_result
    
    device = dbschema.DECICES_TABLE.get(input_dict)
    if not device:
        device_record = device.valid_fields_dictionary(input_dict)
        msg = f"invalid device"
        api_result = {'api_status': 'error', 'api_message': msg, 'api_data': device_record, 'api_action': _api_action.upper(), 'api_name': _api_name}
        if thisApp.application_configuration.database_api_debug or debug: print_api_result(f"{msgPrefix} result:", api_result)
        return api_result

    client = dbschema.CLIENTS_TABLE.get(input_dict)
    if not client:
        client_record = client.valid_fields_dictionary(input_dict)
        msg = f"invalid client"
        api_result = {'api_status': 'error', 'api_message': msg, 'api_data': client_record, 'api_action': _api_action.upper(), 'api_name': _api_name}
        if thisApp.application_configuration.database_api_debug or debug: print_api_result(f"{msgPrefix} result:", api_result)
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
        client_devices = session.query(CLIENT_DEVICE).filter(CLIENT_DEVICE.device_uid == device.device_uid, CLIENT_DEVICE.client_id == client_id, CLIENT_DEVICE.status != status).all()
        if len(client_devices) <= 0:
            client_devices = session.query(CLIENT_DEVICE).filter(CLIENT_DEVICE.device_uid == device.device_uid, CLIENT_DEVICE.client_id == client_id).all()
            client_device_records = db_session.rows_to_dict(CLIENT_DEVICE, client_devices)
            msg = f"device already {status.upper()} {xx} usage by all applications"
            api_result = {'api_status': 'success', 'api_message': msg, 'api_data': client_device_records, 'api_action': _api_action.upper(), 'api_name': _api_name}
            if thisApp.application_configuration.database_api_debug or debug: print_api_result(f"{msgPrefix} result:", api_result)
            return api_result
        for client_device in client_devices:
            client_device.status = status
            application = dbschema.APPLICATIONS_TABLE.get({'application_name': client_device.application_name})
            registered_apps.append(application.application_name)
        session.commit()
        client_device_records = db_session.rows_to_dict(CLIENT_DEVICE, client_devices)
    else:
        application = dbschema.APPLICATIONS_TABLE.get(input_dict)
        if not application:
            application_record = application.valid_fields_dictionary(input_dict)
            msg = f"invalid application"
            api_result = {'api_status': 'error', 'api_message': msg, 'api_data': application_record, 'api_action': _api_action.upper(), 'api_name': _api_name}
            if thisApp.application_configuration.database_api_debug or debug: print_api_result(f"{msgPrefix} result:", api_result)
            return api_result

        client_device_record = {'device_uid': device.device_uid, 'client_id': client_id, 'application_name': application.application_name, 'last_usage_timestamp': now, 'status': status}
        client_device = dbschema.CLIENT_DEVICES_TABLE.get(client_device_record)
        if client_device:
            if client_device.status == status:
                msg = f"device already {client_device.status.upper()} {xx} usage by application '{client_device.application_name}'"
                client_device_records = [client_device.to_dict()]
                api_result = {'api_status': 'success', 'api_message': msg, 'api_data': client_device_records, 'api_action': _api_action.upper(), 'api_name': _api_name}
                if thisApp.application_configuration.database_api_debug or debug: print_api_result(f"{msgPrefix} result:", api_result)
                return api_result

        client_device = dbschema.CLIENT_DEVICES_TABLE.refresh(client_device_record, commit=False)
        registered_apps.append(application.application_name)
        session.commit()
        client_device_records = [client_device.to_dict()]

    row_count = len(client_device_records)
    x=''
    if row_count > 1:
        x = 's'
        
    msg = f"device {status.upper()} {xx} usage by application{x} {registered_apps}"
    api_result = {'api_status': 'success', 'api_message': msg, 'api_data': client_device_records, 'api_data_rows': row_count, 'api_action': _api_action.upper(), 'api_name':_api_name }
    if thisApp.application_configuration.database_api_debug or debug: print_api_result(f"{msgPrefix} result:", api_result)
    return api_result
#::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
def dbapi_device_usage(session, action, input_dict, filter_dict={}, caller_dict={}):
    _api_name = "dbapi_device_usage"
    _api_entity = 'DEVICE'
    _api_action = action
    debug = False

    msgPrefix=f"#C9#{_api_name}#RESET# [{_api_action.upper()}]#RESET#"

    msgStart=f"{msgPrefix} start: input_dict=[[{input_dict}]]"
    if thisApp.application_configuration.database_api_debug or debug: print_message(msgStart)

    action_result = db_table_action(dbmodel.DEVICE_USAGE, action, input_dict, filter_dict, caller_dict={}, api_name=_api_name, api_entity=_api_entity, auto_commit=True, call_level=1)
    api_result = action_result
    api_result.update({'api_action': _api_action, 'api_name': _api_name})
    
    if thisApp.application_configuration.database_api_debug or debug: print_api_result(f"{msgPrefix} result:", api_result)
    return api_result
#::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
def dbapi_client_device(session, action, input_dict, filter_dict={}, caller_dict={}):
    _api_name = "dbapi_client_device"
    _api_entity = 'DEVICE'
    _api_action = action
    debug = False

    if action.upper in ('REGISTER','UNREGISTER'):
        dbapi_device_register_unregister(input_dict,action)
        return

    msgPrefix=f"#C9#{_api_name}#RESET# [{_api_action.upper()}]#RESET#"

    msgStart=f"{msgPrefix} start: input_dict=[[{input_dict}]]"
    if thisApp.application_configuration.database_api_debug or debug: print_message(msgStart)

    action_result = db_table_action(dbmodel.CLIENT_DEVICE, action, input_dict, filter_dict, caller_dict={}, api_name=_api_name, api_entity=_api_entity, auto_commit=True, call_level=1)
    api_result = action_result
    api_result.update({'api_action': _api_action, 'api_name': _api_name})
    
    if thisApp.application_configuration.database_api_debug or debug: print_api_result(f"{msgPrefix} result:", api_result)
    return api_result
#::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
def dbapi_api(session, action, input_dict, filter_dict={}, caller_dict={}):
    _api_name = "dbapi_api"
    _api_entity = 'API'
    _api_action = action
    debug = False
    if action.upper() == 'REGISTER':
        dbapi_api_register(input_dict)
        return
    elif action.upper() == 'UNREGISTER':
        dbapi_api_unregister(input_dict)
        return

    msgPrefix=f"#C9#{_api_name}#RESET# [{_api_action.upper()}]#RESET#"

    msgStart=f"{msgPrefix} start: input_dict=[[{input_dict}]]"
    if thisApp.application_configuration.database_api_debug or debug: print_message(msgStart)

    action_result = db_table_action(dbmodel.BANK, action, input_dict, filter_dict, caller_dict={}, api_name=_api_name, api_entity=_api_entity, auto_commit=True, call_level=1)
    api_result = action_result
    api_result.update({'api_action': _api_action, 'api_name': _api_name})
    
    if thisApp.application_configuration.database_api_debug or debug: print_api_result(f"{msgPrefix} result:", api_result)
    return api_result    
#::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
def dbapi_api_register(session, input_dict):
    _api_name = "dbapi_api_register"
    _api_entity = 'API'
    _api_action = 'REGISTER'
    debug = False

    msgPrefix=f"#C9#{_api_name}#RESET# [{_api_action.upper()}]#RESET#"

    msgStart=f"{msgPrefix} start: input_dict=[[{input_dict}]]"
    if thisApp.application_configuration.database_api_debug or debug: print_message(msgStart)

    api=dbschema.APIS_TABLE.get(input_dict)
    if not api:
        msg = f'api not found'
        api_result = {'api_status': 'error', 'api_message': msg, 'api_data': input_dict}
        if thisApp.application_configuration.database_api_debug or debug: print_api_result(f"{msgPrefix} result:", api_result)
        return api_result
    if not api.status=='Active':
        msg = f'api not Active'
        api_result = {'api_status': 'error', 'api_message': msg, 'api_data': input_dict}
        if thisApp.application_configuration.database_api_debug or debug: print_api_result(f"{msgPrefix} result:", api_result)
        return api_result
    application=dbschema.APPLICATIONS_TABLE.get(input_dict)
    if not application:
        msg = f'application not found'
        api_result = {'api_status': 'error', 'api_message': msg, 'api_data': input_dict}
        if thisApp.application_configuration.database_api_debug or debug: print_api_result(f"{msgPrefix} result:", api_result)
        return api_result
    if not application.status=='Active':
        msg = f'application not Active'
        api_result = {'api_status': 'error', 'api_message': msg, 'api_data': input_dict}
        if thisApp.application_configuration.database_api_debug or debug: print_api_result(f"{msgPrefix} result:", api_result)
        return api_result

    input_dict.update({'api_id':api.api_id})
    input_dict.update({'api_name':api.api_name})
    input_dict.update({'application_id': application.application_id})
    input_dict.update({'application_name': application.application_name})

    filter_dict={}
    api_registered = dbschema.REGISTERED_APIS_TABLE.get(input_dict)
    if api_registered:  
        input_dict.update({'application_api_id': api_registered.application_api_id})
        filter_dict = {'application_api_id': api_registered.application_api_id}
        
    input_dict.update({'status': 'Active'})
    action='REFRESH'
    action_result = db_table_action(dbmodel.APPLICATION_API, action , input_dict, filter_dict, caller_dict={}, api_name=_api_name, api_entity=_api_entity, auto_commit=True, call_level=1)
    api_result = action_result
    api_result.update({'api_action': _api_action, 'api_name': _api_name})
    if thisApp.application_configuration.database_api_debug or debug: print_api_result(f"{msgPrefix} result:", api_result)
    return api_result
#::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
def dbapi_api_unregister(session, input_dict):
    _api_name = "dbapi_api_unregister"
    _api_entity = 'API'
    _api_action = 'UNREGISTER'
    debug = False

    msgPrefix=f"#C9#{_api_name}#RESET# [{_api_action.upper()}]#RESET#"

    msgStart=f"{msgPrefix} start: input_dict=[[{input_dict}]]"
    if thisApp.application_configuration.database_api_debug or debug: print_message(msgStart)

    api=dbschema.APIS_TABLE.get(input_dict)
    if api:
        input_dict.update({'api_id':api.api_id})
        input_dict.update({'api_name':api.api_name})
    
    application=dbschema.APPLICATIONS_TABLE.get(input_dict)
    if application:
        input_dict.update({'application_id': application.application_id})
        input_dict.update({'application_name': application.application_name})

    api_registered = dbschema.REGISTERED_APIS_TABLE.get(input_dict)
    if not api_registered:
        msg = f'record not found'
        api_result = {'api_status': 'error', 'api_message': msg, 'api_data': input_dict}
        if thisApp.application_configuration.database_api_debug or debug: print_api_result(f"{msgPrefix} result:", api_result)
        return api_result
    
    input_dict.update({'application_api_id': api_registered.application_api_id})
    input_dict.update({'status':'Unregistered'})
    
    filter_dict={'application_api_id': api_registered.application_api_id}
    
    action='UPDATE'
    action_result = db_table_action(dbmodel.APPLICATION_API, action, input_dict, filter_dict, caller_dict={}, api_name=_api_name, api_entity=_api_entity, auto_commit=True, call_level=1)
    api_result = action_result
    api_result.update({'api_action': _api_action, 'api_name': _api_name})
    if thisApp.application_configuration.database_api_debug or debug: print_api_result(f"{msgPrefix} result:", api_result)
    return api_result
#::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
def dbapi_application_api(session, action, input_dict, filter_dict={}, caller_dict={}):
    _api_name = "dbapi_application_api"
    _api_entity = 'REGISTERED_API'
    _api_action = action
    debug = False

    msgPrefix=f"#C9#{_api_name}#RESET# [{_api_action.upper()}]#RESET#"

    msgStart=f"{msgPrefix} start: input_dict=[[{input_dict}]]"
    if thisApp.application_configuration.database_api_debug or debug: print_message(msgStart)

    action_result = db_table_action(dbmodel.APPLICATION_API, action , input_dict, filter_dict, caller_dict={}, api_name=_api_name, api_entity=_api_entity, auto_commit=True, call_level=1)
    api_result = action_result
    api_result.update({'api_action': _api_action, 'api_name': _api_name})
    
    if thisApp.application_configuration.database_api_debug or debug: print_api_result(f"{msgPrefix} result:", api_result)
    return api_result
#::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
def dbapi_application(session, action, input_dict, filter_dict={}, caller_dict={}):
    _api_name = "dbapi_application"
    _api_entity = 'APPLICATION'
    _api_action = action
    debug = False

    if action.upper() == 'API_REGISTER':
        dbapi_api_register(input_dict)
        return
    elif action.upper() == 'API_UNREGISTER':
        dbapi_api_unregister(input_dict)
        return
    elif action.upper() == 'VALIDATE' or action.upper() == 'VALIDATE_CREDENTIALS':
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

        return dbapi_application_credentials_are_valid(application_name, client_id, client_secretKey)

    msgPrefix=f"#C9#{_api_name}#RESET# [{_api_action.upper()}]#RESET#"

    msgStart=f"{msgPrefix} start: input_dict=[[{input_dict}]]"
    if thisApp.application_configuration.database_api_debug or debug: print_message(msgStart)

    if action.upper() in ('ADD','INSERT','REGISTER','REFRESH'):
        client=dbschema.CLIENTS_TABLE.get(input_dict)
        if not client:
            msg = f'client not found'
            api_result = {'api_status': 'error', 'api_message': msg, 'api_data': input_dict}
            if thisApp.application_configuration.database_api_debug or debug: print_api_result(f"{msgPrefix} result:", api_result)
            return api_result

        if not client.status=='Active':
            msg = f'client not Active'
            api_result = {'api_status': 'error', 'api_message': msg, 'api_data': input_dict}
            if thisApp.application_configuration.database_api_debug or debug: print_api_result(f"{msgPrefix} result:", api_result)
            return api_result

    input_dict.update({'client_id': client.client_id}) 
    action_result = db_table_action(dbmodel.APPLICATION, action , input_dict, filter_dict, caller_dict={}, api_name=_api_name, api_entity=_api_entity, auto_commit=True, call_level=1)
    api_result = action_result
    api_result.update({'api_action': _api_action, 'api_name': _api_name})
    
    if thisApp.application_configuration.database_api_debug or debug: print_api_result(f"{msgPrefix} result:", api_result)
    return api_result
#::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
def dbapi_application_credentials_are_valid(session, application_name, client_id, client_secretKey):
    debug = False
    application=dbschema.APPLICATIONS_TABLE.get({'application_name': application_name})
    if not application:
        return False    
    if not application.client_id == client_id or not application.client_secretKey == client_secretKey:
        return False
    return True
#::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
def dbapi_token(session, action, input_dict, filter_dict={}, caller_dict={}):
    _api_name = "dbapi_token"
    _api_entity = 'TOKEN'
    _api_action = action
    debug = False

    msgPrefix=f"#C9#{_api_name}#RESET# [{_api_action.upper()}]#RESET#"

    msgStart=f"{msgPrefix} start: input_dict=[[{input_dict}]]"
    if thisApp.application_configuration.database_api_debug or debug: print_message(msgStart)

    action_result = db_table_action(dbmodel.TOKEN, action , input_dict, filter_dict, caller_dict={}, api_name=_api_name, api_entity=_api_entity, auto_commit=True, call_level=1)
    api_result = action_result
    api_result.update({'api_action': _api_action, 'api_name': _api_name})
    
    if thisApp.application_configuration.database_api_debug or debug: print_api_result(f"{msgPrefix} result:", api_result)
    return api_result
#::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
def dbapi_token_is_valid(session, token):
    debug = False
    if type(token) == type(''):
        input_dict = {'token': token}

    if not type(token) == type({}):
        return False
    else:
        input_dict = token

    if not input_dict.get('token'):
        return False

    token_record = dbschema.TOKENS_TABLE.get(input_dict)
        
    if not token_record:
        msg = f'access token is NOT valid.(not found)'
        #log_message(msg,msgType='error')
        return False

    #expiryDT = token_record.get('expiryDT')
    expiryDT = token_record.expiryDT
    if not expiryDT:
        msg = f'access token is NOT valid.(no expiryDT)'
        #log_message(msg,msgType='error')
        return False

    #universal time
    #GMT=Greenwich Mean Time
    #UTC=Coordinated Universal Time
    #There is no time difference between Coordinated Universal Time and Greenwich Mean Time
    nowString = datetime.datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S')
    #now=datetime.datetime.utcnow()
    if expiryDT < datetime.datetime.utcnow():
    #if expiryDT < nowString:
        msg = f'access token is NOT valid.(expired)'
        #log_message(msg,msgType='error')
        return False
    return True
#::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
def dbapi_token_get_access_token(session, token_request):
    debug = False
    application_name=token_request.get('application_name')
    client_id=token_request.get('application_client_id')
    client_secretKey=token_request.get('application_client_secretKey')
    application = dbschema.APPLICATIONS_TABLE.get({'application_name': application_name, 'client_id': client_id})
    if not application:
        return {'api_status': 'error', 'api_message': 'application not registered'}
    if not application.client_id == client_id or not application.client_secretKey == client_secretKey:
        return {'api_status': 'error', 'api_message': 'application credentials not valid'}

    token_duration_secs = 3600
    if token_request.get('token_scope') == 'application_service':
        token_duration_secs = 360
    token_request.update({'duration_seconds':token_duration_secs})
    token_request.update({'status':'Active'})

    expiryDT = datetime.datetime.utcnow() + datetime.timedelta(seconds=token_duration_secs)
    #expiryDT_str = expiryDT.strftime('%Y-%m-%d %H:%M:%S')
    #expiryDT_sqlite=f"DATETIME(CURRENT_TIMESTAMP, '+{token_duration_secs} seconds')
    token_request.update({'expiryDT': expiryDT})
    if 'token' in token_request.keys():
        token_request.pop('token')
    print('')
    print(token_request)
    print('')

    token_record = dbschema.TOKENS_TABLE.insert(token_request,commit=True)
    if not token_record:
        return {}

    print('')
    print(token_record)
    print('')

    token = {
        'token_type': token_record.token_type,
        'token_scope': token_record.token_scope,
        'grant_type': token_record.grant_type,
        'token': token_record.token,
        'duration_seconds': token_record.duration_seconds,
        'expiryDT': token_record.expiryDT,
        }

    return token
#::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
def dbapi_cleanup_tokens(session):
    _api_name = "debapi_cleanup_tokens"
    _api_entity = 'TOKEN'
    _api_action = 'CLEANUP'
    debug = False

    msgPrefix=f"#C9#{_api_name}#RESET# [{_api_action.upper()}]#RESET#"

    msgStart=f"{msgPrefix} start: action=[[{_api_action}]]"
    if thisApp.application_configuration.database_api_debug or debug: print_message(msgStart)

    where_expression = {'status': 'Expired'}
    deleted_result = dbschema.TOKENS_TABLE.delete_rows(where_expression, commit=True)
    deleted_rows = deleted_result.get('rows_deleted', 0)

    #nowString = datetime.datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S')
    #where_expression = f"expiryDT<'{datetime.datetime.utcnow()}'"
    where_expression = {'expiryDT': {datetime.datetime.utcnow()}}
    update_dict = {'status': 'Expired'}
    expired_result = dbschema.TOKENS_TABLE.update_rows(update_dict,where_expression, commit=True)
    expired_rows = expired_result.get('rows_updated', 0)

    msg = f'tokens cleaned with {expired_rows} tokens expired, {deleted_rows} removed.'

    api_result = {'api_status': 'success', 'api_message': msg, 'rows_expired': expired_rows, 'rows_removed': deleted_rows}
    if thisApp.application_configuration.database_api_debug or debug: print_api_result(f"{msgPrefix} result:", api_result)
    return api_result
#::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
def dbapi_bank(session, action, input_dict, filter_dict={}, caller_dict={}):
    _api_name = "dbapi_bank"
    _api_entity = 'BANK'
    _api_action = action
    debug = False

    msgPrefix=f"#C9#{_api_name}#RESET# [{_api_action.upper()}]#RESET#"

    msgStart=f"{msgPrefix} start: input_dict=[[{input_dict}]]"
    if thisApp.application_configuration.database_api_debug or debug: print_message(msgStart)

    action_result = db_table_action(dbmodel.BANK, action , input_dict, filter_dict, caller_dict={}, api_name=_api_name, api_entity=_api_entity, auto_commit=True, call_level=1)
    api_result = action_result
    api_result.update({'api_action': _api_action, 'api_name': _api_name})
    
    if thisApp.application_configuration.database_api_debug or debug: print_api_result(f"{msgPrefix} result:", api_result)
    return api_result
#::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
def dbapi_client(session, action, input_dict, filter_dict={}, caller_dict={}):
    _api_name = "dbapi_cient"
    _api_entity = 'CLIENT'
    _api_action = action
    debug = False

    msgPrefix=f"#C9#{_api_name}#RESET# [{_api_action.upper()}]#RESET#"

    msgStart=f"{msgPrefix} start: input_dict=[[{input_dict}]]"
    if thisApp.application_configuration.database_api_debug or debug: print_message(msgStart)

    api_result = db_table_action(dbmodel.CLIENT, action , input_dict, filter_dict, caller_dict={}, api_name=_api_name, api_entity=_api_entity, auto_commit=True, call_level=1)
    if not api_result.get('api_status') == 'success':
        if thisApp.application_configuration.database_api_debug or debug: print_api_result(f"{msgPrefix} result:", api_result)
        return api_result
        
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
            xapi_result = db_table_action(dbmodel.MERCHANT, action , update_dict, filter_dict, caller_dict={}, api_name=_api_name, api_entity=_api_entity, auto_commit=True, call_level=1)
        elif client_type == 'consumer':
            xapi_result = db_table_action(dbmodel.CONSUMER, action , update_dict, filter_dict, caller_dict={}, api_name=_api_name, api_entity=_api_entity, auto_commit=True, call_level=1)
        elif client_type == 'service_provider':
            xapi_result = db_table_action(dbmodel.SERVICE_PROVIDER, action , update_dict, filter_dict, caller_dict={}, api_name=_api_name, api_entity=_api_entity, auto_commit=True, call_level=1)

    api_result.update({'api_action': _api_action, 'api_name': _api_name})
    if thisApp.application_configuration.database_api_debug or debug: print_api_result(f"{msgPrefix} result:", api_result)
    return api_result
#::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
def dbapi_service_provider(session, action, input_dict, filter_dict={}, caller_dict={}):
    _api_name = "dbapi_service_provider"
    _api_entity = 'SERVICE_PROVIDER'
    _api_action = action
    debug = False
    input_dict.update({'client_type': 'service_provider'})

    msgPrefix=f"#C9#{_api_name}#RESET# [{_api_action.upper()}]#RESET#"
    msgStart=f"{msgPrefix} start: input_dict=[[{input_dict}]]"
    if thisApp.application_configuration.database_api_debug or debug: print_message(msgStart)

    if action.upper() in ('REGISTER','ADD','REFRESH'):
        action='REFRESH'
        action_result = db_table_action(dbmodel.CLIENT, action, input_dict,  filter_dict, _api_name, _api_entity,auto_commit=True,call_level=1)
        api_result = action_result
        api_result.update({'api_action': _api_action, 'api_name': _api_name})
        thismsg=action_result.get('api_message')
        if not api_result.get('api_status') == 'success':
            # msg = f"service provider not registered"
            # api_result.update({'api_message':msg})
            if thisApp.application_configuration.database_api_debug or debug: print_api_result(f"{msgPrefix} result:", api_result)
            return api_result
        client = api_result.get('api_data')
        client_id = client.get('client_id')
        input_dict.update({'client_id': client_id})
    elif action.upper() in ('CONFIRM', 'ACTIVATE', 'DEACTIVATE', 'DELETE'):
        service_provider_dict = dbschema.SERVICE_PROVIDERS_TABLE.get(input_dict, 'DICT')
        if not service_provider_dict:
            msg = f'service provider not found'
            action_status='error'
            api_result = {'api_status': action_status, 'api_message': msg, 'api_data': input_dict, 'api_action': _api_action.upper(), 'api_name': _api_name}
            if thisApp.application_configuration.database_api_debug or debug: print_api_result(f"{msgPrefix} result:", api_result)
            return api_result

        service_provider = dbschema.SERVICE_PROVIDERS_TABLE.get(input_dict)
        client_id = service_provider.client_id
        email = service_provider.email
        client=dbschema.CLIENTS_TABLE.get({'email':email})
        
        client_dict=dbschema.CLIENTS_TABLE.get(service_provider_dict,'DICT' )
        if not client_dict:
            msg = f'client not found'
            action_status='error'
            api_result = {'api_status': action_status, 'api_message': msg, 'api_data': service_provider_dict, 'api_action': _api_action.upper(), 'api_name': _api_name}
            if thisApp.application_configuration.database_api_debug or debug: print_api_result(f"{msgPrefix} result:", api_result)
            return api_result

        #action='CONFIRM'
        action_result = db_table_action(dbmodel.CLIENT, action, input_dict,  filter_dict, _api_name, _api_entity,auto_commit=True,call_level=1)
        api_result = action_result
        api_result.update({'api_action': _api_action, 'api_name': _api_name})
        thismsg=action_result.get('api_message')
        if not api_result.get('api_status') == 'success':
            # msg = f'client confirmation failed'
            # api_result.update({'api_message':msg})
            if thisApp.application_configuration.database_api_debug or debug: print_api_result(f"{msgPrefix} result:", api_result)
            return api_result
        service_provider_dict = dbschema.SERVICE_PROVIDERS_TABLE.get(service_provider_dict, 'DICT')
        status=service_provider_dict.get('status')
        client_id=service_provider_dict.get('client_id')
        # if not service_provider_dict.get('status') == 'Active':
        #     msg = f"service provider not confirmed. status={status}"
        #     action_status='error'
        #     api_result = {'api_status': action_status, 'api_message': msg, 'api_data': service_provider_dict, 'messages': messages, 'rows_added': rows_added, 'rows_updated': rows_updated, 'api_action': _api_action.upper(), 'api_name': _api_name}
        #     if thisApp.application_configuration.database_api_debug or debug: print_api_result(f"{msgPrefix} result:", api_result)
        #     return api_result
        input_dict.update({'status': status})
        input_dict.update({'client_id': client_id})
    
    action_result = db_table_action(dbmodel.SERVICE_PROVIDER, action, input_dict,  filter_dict, _api_name, _api_entity,auto_commit=True,call_level=1)
    api_result = action_result
    thismsg=thismsg.replace('CLIENT',_api_entity)
    api_result.update({'api_action': _api_action, 'api_name': _api_name,'api_message':thismsg})
    
    if thisApp.application_configuration.database_api_debug or debug: print_api_result(f"{msgPrefix} result:", api_result)
    return api_result
#::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
def dbapi_user(session, action, input_dict, filter_dict={}, caller_dict={}):
    _api_name = "dbapi_user"
    _api_entity = 'USER'
    _api_action = action
    debug = False
    input_dict.update({'client_type': 'user'})

    msgPrefix=f"#C9#{_api_name}#RESET# [{_api_action.upper()}]#RESET#"
    msgStart=f"{msgPrefix} start: input_dict=[[{input_dict}]]"
    if thisApp.application_configuration.database_api_debug or debug: print_message(msgStart)

    if action.upper() in ('REGISTER','ADD','REFRESH'):
        action='REFRESH'
        action_result = db_table_action(dbmodel.CLIENT, action, input_dict,  filter_dict, _api_name, _api_entity,auto_commit=True,call_level=1)
        api_result = action_result
        api_result.update({'api_action': _api_action, 'api_name': _api_name})
        thismsg=action_result.get('api_message')
        if not api_result.get('api_status') == 'success':
            # msg = f"service provider not registered"
            # api_result.update({'api_message':msg})
            if thisApp.application_configuration.database_api_debug or debug: print_api_result(f"{msgPrefix} result:", api_result)
            return api_result
        client = api_result.get('api_data')
        client_id = client.get('client_id')
        input_dict.update({'client_id': client_id})
    elif action.upper() in ('CONFIRM', 'ACTIVATE', 'DEACTIVATE', 'DELETE'):
        service_provider_dict = dbschema.SERVICE_PROVIDERS_TABLE.get(input_dict, 'DICT')
        if not service_provider_dict:
            msg = f'service provider not found'
            action_status='error'
            api_result = {'api_status': action_status, 'api_message': msg, 'api_data': input_dict, 'api_action': _api_action.upper(), 'api_name': _api_name}
            if thisApp.application_configuration.database_api_debug or debug: print_api_result(f"{msgPrefix} result:", api_result)
            return api_result
        client_dict=dbschema.CLIENTS_TABLE.get(service_provider_dict,'DICT' )
        if not client_dict:
            msg = f'client not found'
            action_status='error'
            api_result = {'api_status': action_status, 'api_message': msg, 'api_data': service_provider_dict, 'api_action': _api_action.upper(), 'api_name': _api_name}
            if thisApp.application_configuration.database_api_debug or debug: print_api_result(f"{msgPrefix} result:", api_result)
            return api_result

        #action='CONFIRM'
        action_result = db_table_action(dbmodel.CLIENT, action, input_dict,  filter_dict, _api_name, _api_entity,auto_commit=True,call_level=1)
        api_result = action_result
        api_result.update({'api_action': _api_action, 'api_name': _api_name})
        thismsg=action_result.get('api_message')
        if not api_result.get('api_status') == 'success':
            # msg = f'client confirmation failed'
            # api_result.update({'api_message':msg})
            if thisApp.application_configuration.database_api_debug or debug: print_api_result(f"{msgPrefix} result:", api_result)
            return api_result
        service_provider_dict = dbschema.SERVICE_PROVIDERS_TABLE.get(service_provider_dict, 'DICT')
        status=service_provider_dict.get('status')
        client_id=service_provider_dict.get('client_id')
        # if not service_provider_dict.get('status') == 'Active':
        #     msg = f"service provider not confirmed. status={status}"
        #     action_status='error'
        #     api_result = {'api_status': action_status, 'api_message': msg, 'api_data': service_provider_dict, 'messages': messages, 'rows_added': rows_added, 'rows_updated': rows_updated, 'api_action': _api_action.upper(), 'api_name': _api_name}
        #     if thisApp.application_configuration.database_api_debug or debug: print_api_result(f"{msgPrefix} result:", api_result)
        #     return api_result
        input_dict.update({'status': status})
        input_dict.update({'client_id': client_id})
    
    action_result = db_table_action(dbmodel.SERVICE_PROVIDER, action, input_dict,  filter_dict, _api_name, _api_entity,auto_commit=True,call_level=1)
    api_result = action_result
    thismsg=thismsg.replace('CLIENT',_api_entity)
    api_result.update({'api_action': _api_action, 'api_name': _api_name,'api_message':thismsg})
    
    if thisApp.application_configuration.database_api_debug or debug: print_api_result(f"{msgPrefix} result:", api_result)
    return api_result
#::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
def dbapi_consumer(session, action, input_dict, filter_dict={}, caller_dict={}):
    _api_name = "dbapi_consumer"
    _api_entity = 'CONSUMER'
    _api_action = action
    debug = False
    input_dict.update({'client_type': 'consumer'})

    msgPrefix=f"#C9#{_api_name}#RESET# [{_api_action.upper()}]#RESET#"
    msgStart=f"{msgPrefix} start: input_dict=[[{input_dict}]]"
    if thisApp.application_configuration.database_api_debug or debug: print_message(msgStart)

    if action.upper() in ('REGISTER','ADD','REFRESH'):
        action='REFRESH'
        action_result = db_table_action(dbmodel.CLIENT, action, input_dict,  filter_dict, _api_name, _api_entity,auto_commit=True,call_level=1)
        api_result = action_result
        thismsg=action_result.get('api_message')
        api_result.update({'api_action': _api_action, 'api_name': _api_name})
        if not api_result.get('api_status') == 'success':
            # msg = f"service provider not registered"
            # api_result.update({'api_message':msg})
            if thisApp.application_configuration.database_api_debug or debug: print_api_result(f"{msgPrefix} result:", api_result)
            return api_result
        client = api_result.get('api_data')
        client_id = client.get('client_id')
        input_dict.update({'client_id': client_id})
    elif action.upper() in ('CONFIRM', 'ACTIVATE', 'DEACTIVATE', 'DELETE'):
        service_provider_dict = dbschema.SERVICE_PROVIDERS_TABLE.get(input_dict, 'DICT')
        if not service_provider_dict:
            msg = f'service provider not found'
            action_status='error'
            api_result = {'api_status': action_status, 'api_message': msg, 'api_data': input_dict, 'api_action': _api_action.upper(), 'api_name': _api_name}
            if thisApp.application_configuration.database_api_debug or debug: print_api_result(f"{msgPrefix} result:", api_result)
            return api_result
        client_dict=dbschema.CLIENTS_TABLE.get(service_provider_dict,'DICT' )
        if not client_dict:
            msg = f'client not found'
            action_status='error'
            api_result = {'api_status': action_status, 'api_message': msg, 'api_data': service_provider_dict, 'api_action': _api_action.upper(), 'api_name': _api_name}
            if thisApp.application_configuration.database_api_debug or debug: print_api_result(f"{msgPrefix} result:", api_result)
            return api_result

        #action='CONFIRM'
        action_result = db_table_action(dbmodel.CLIENT, action, input_dict,  filter_dict, _api_name, _api_entity,auto_commit=True,call_level=1)
        api_result = action_result
        api_result.update({'api_action': _api_action, 'api_name': _api_name})
        thismsg=action_result.get('api_message')
        if not api_result.get('api_status') == 'success':
            # msg = f'client confirmation failed'
            # api_result.update({'api_message':msg})
            if thisApp.application_configuration.database_api_debug or debug: print_api_result(f"{msgPrefix} result:", api_result)
            return api_result
        service_provider_dict = dbschema.SERVICE_PROVIDERS_TABLE.get(service_provider_dict, 'DICT')
        status=service_provider_dict.get('status')
        client_id=service_provider_dict.get('client_id')
        # if not service_provider_dict.get('status') == 'Active':
        #     msg = f"service provider not confirmed. status={status}"
        #     action_status='error'
        #     api_result = {'api_status': action_status, 'api_message': msg, 'api_data': service_provider_dict, 'messages': messages, 'rows_added': rows_added, 'rows_updated': rows_updated, 'api_action': _api_action.upper(), 'api_name': _api_name}
        #     if thisApp.application_configuration.database_api_debug or debug: print_api_result(f"{msgPrefix} result:", api_result)
        #     return api_result
        input_dict.update({'status': status})
        input_dict.update({'client_id': client_id})
    
    action_result = db_table_action(dbmodel.SERVICE_PROVIDER, action, input_dict,  filter_dict, _api_name, _api_entity,auto_commit=True,call_level=1)
    api_result = action_result
    thismsg=thismsg.replace('CLIENT',_api_entity)
    api_result.update({'api_action': _api_action, 'api_name': _api_name,'api_message':thismsg})
    
    if thisApp.application_configuration.database_api_debug or debug: print_api_result(f"{msgPrefix} result:", api_result)
    return api_result
#::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
def dbapi_merchant(session, action, input_dict, filter_dict={}, caller_dict={}):
    _api_name = "dbapi_merchant"
    _api_entity = 'MERCHANT'
    _api_action = action
    debug = False
    input_dict.update({'client_type': 'merchant'})

    msgPrefix=f"#C9#{_api_name}#RESET# [{_api_action.upper()}]#RESET#"
    msgStart=f"{msgPrefix} start: input_dict=[[{input_dict}]]"
    if thisApp.application_configuration.database_api_debug or debug: print_message(msgStart)

    if action.upper() in ('REGISTER','ADD','REFRESH'):
        action='REFRESH'
        action_result = db_table_action(dbmodel.CLIENT, action, input_dict,  filter_dict, _api_name, _api_entity,auto_commit=True,call_level=1)
        api_result = action_result
        api_result.update({'api_action': _api_action, 'api_name': _api_name})
        thismsg=action_result.get('api_message')
        if not api_result.get('api_status') == 'success':
            if thisApp.application_configuration.database_api_debug or debug: print_api_result(f"{msgPrefix} result:", api_result)
            return api_result
        client = api_result.get('api_data')
        client_id = client.get('client_id')
        input_dict.update({'client_id': client_id})
    elif action.upper() in ('CONFIRM', 'ACTIVATE', 'DEACTIVATE', 'DELETE'):
        merchant_dict = dbschema.MERCHANTS_TABLE.get(input_dict, 'DICT')
        if not merchant_dict:
            msg = f'merchant not found'
            action_status='error'
            api_result = {'api_status': action_status, 'api_message': msg, 'api_data': input_dict, 'api_action': _api_action.upper(), 'api_name': _api_name}
            if thisApp.application_configuration.database_api_debug or debug: print_api_result(f"{msgPrefix} result:", api_result)
            return api_result
        client_dict=dbschema.CLIENTS_TABLE.get(merchant_dict,'DICT' )
        if not client_dict:
            msg = f'client not found'
            action_status='error'
            api_result = {'api_status': action_status, 'api_message': msg, 'api_data': merchant_dict, 'api_action': _api_action.upper(), 'api_name': _api_name}
            if thisApp.application_configuration.database_api_debug or debug: print_api_result(f"{msgPrefix} result:", api_result)
            return api_result

        #action='CONFIRM'
        action_result = db_table_action(dbmodel.CLIENT, action, input_dict,  filter_dict, _api_name, _api_entity,auto_commit=True,call_level=1)
        api_result = action_result
        api_result.update({'api_action': _api_action, 'api_name': _api_name})
        thismsg=action_result.get('api_message')
        # api_result = dbapi_client_confirm(client_dict)
        if not api_result.get('api_status') == 'success':
            # msg = f'client confirmation failed'
            # api_result.update({'api_message':msg})
            if thisApp.application_configuration.database_api_debug or debug: print_api_result(f"{msgPrefix} result:", api_result)
            return api_result
        merchant_dict = dbschema.MERCHANTS_TABLE.get(merchant_dict, 'DICT')
        status=merchant_dict.get('status')
        client_id=merchant_dict.get('client_id')
        # if not merchant_dict.get('status') == 'Active':
        #     msg = f"service provider not confirmed. status={status}"
        #     action_status='error'
        #     api_result = {'api_status': action_status, 'api_message': msg, 'api_data': merchant_dict, 'messages': messages, 'rows_added': rows_added, 'rows_updated': rows_updated, 'api_action': _api_action.upper(), 'api_name': _api_name}
        #     if thisApp.application_configuration.database_api_debug or debug: print_api_result(f"{msgPrefix} result:", api_result)
        #     return api_result
        input_dict.update({'status': status})
        input_dict.update({'client_id': client_id})
    
    action_result = db_table_action(dbmodel.MERCHANT, action, input_dict,  filter_dict, _api_name, _api_entity,auto_commit=True,call_level=1)
    api_result = action_result
    thismsg=thismsg.replace('CLIENT',_api_entity)
    api_result.update({'api_action': _api_action, 'api_name': _api_name,'api_message':thismsg})
    
    if thisApp.application_configuration.database_api_debug or debug: print_api_result(f"{msgPrefix} result:", api_result)
    return api_result
#::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
def dbapi_merchant_pointofsale(session, action, input_dict, filter_dict={}, caller_dict={}):
    _api_name = "dbapi_merchant_pointofsale"
    _api_entity = 'POINT_OF_SALE'
    _api_action = action
    debug = False

    msgPrefix=f"#C9#{_api_name}#RESET# [{_api_action.upper()}]#RESET#"

    msgStart=f"{msgPrefix} start: input_dict=[[{input_dict}]]"
    if thisApp.application_configuration.database_api_debug or debug: print_message(msgStart)

    action_result = db_table_action(dbmodel.POINT_OF_SALE, action , input_dict, filter_dict, caller_dict={}, api_name=_api_name, api_entity=_api_entity, auto_commit=True, call_level=1)
    api_result = action_result
    api_result.update({'api_action': _api_action, 'api_name': _api_name})
    
    if thisApp.application_configuration.database_api_debug or debug: print_api_result(f"{msgPrefix} result:", api_result)
    return api_result
#::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
def dbapi_merchant_employee(session, action, input_dict, filter_dict={}, caller_dict={}):
    _api_name = "dbapi_merchant_employee"
    _api_entity = 'MERCHANT_EMPLOYEE'
    _api_action = action
    debug = False

    msgPrefix=f"#C9#{_api_name}#RESET# [{_api_action.upper()}]#RESET#"

    msgStart=f"{msgPrefix} start: input_dict=[[{input_dict}]]"
    if thisApp.application_configuration.database_api_debug or debug: print_message(msgStart)

    action_result = db_table_action(dbmodel.MERCHANT_EMPLOYEE, action , input_dict, filter_dict, caller_dict={}, api_name=_api_name, api_entity=_api_entity, auto_commit=True, call_level=1)
    api_result = action_result
    api_result.update({'api_action': _api_action, 'api_name': _api_name})
    
    if thisApp.application_configuration.database_api_debug or debug: print_api_result(f"{msgPrefix} result:", api_result)
    return api_result
#::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
def dbapi_interaction(session, action, input_dict, filter_dict={}, caller_dict={}):
    _api_name = "dbapi_interaction"
    _api_entity = 'INTERACTION'
    _api_action = action
    debug = False

    msgPrefix=f"#C9#{_api_name}#RESET# [{_api_action.upper()}]#RESET#"

    msgStart=f"{msgPrefix} start: input_dict=[[{input_dict}]]"
    if thisApp.application_configuration.database_api_debug or debug: print_message(msgStart)

    action_result = db_table_action(dbmodel.INTERACTION, action , input_dict, filter_dict, caller_dict={}, api_name=_api_name, api_entity=_api_entity, auto_commit=True, call_level=1)
    api_result = action_result
    api_result.update({'api_action': _api_action, 'api_name': _api_name})
    
    if thisApp.application_configuration.database_api_debug or debug: print_api_result(f"{msgPrefix} result:", api_result)
    return api_result
#::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
def dbapi_interaction_message(session, action, input_dict, filter_dict={}, caller_dict={}):
    _api_name = "dbapi_interaction_message"
    _api_entity = 'INTERACTION_MESSAGE'
    _api_action = action
    debug = False

    msgPrefix=f"#C9#{_api_name}#RESET# [{_api_action.upper()}]#RESET#"

    msgStart=f"{msgPrefix} start: input_dict=[[{input_dict}]]"
    if thisApp.application_configuration.database_api_debug or debug: print_message(msgStart)

    action_result = db_table_action(dbmodel.INTERACTION_MESSAGE, action , input_dict, filter_dict, caller_dict={}, api_name=_api_name, api_entity=_api_entity, auto_commit=True, call_level=1)
    api_result = action_result
    api_result.update({'api_action': _api_action, 'api_name': _api_name})
    
    if thisApp.application_configuration.database_api_debug or debug: print_api_result(f"{msgPrefix} result:", api_result)
    return api_result
#::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
def dbapi_bank_authorization(session, action, input_dict, filter_dict={}, caller_dict={}):
    _api_name = "dbapi_bank_authorization"
    _api_entity = 'BANK_AUTHORIZATION'
    _api_action = action
    debug = False

    msgPrefix=f"#C9#{_api_name}#RESET# [{_api_action.upper()}]#RESET#"

    msgStart=f"{msgPrefix} start: input_dict=[[{input_dict}]]"
    if thisApp.application_configuration.database_api_debug or debug: print_message(msgStart)

    action_result = db_table_action(dbmodel.BANK_AUTHORIZATION, action , input_dict, filter_dict, caller_dict={}, api_name=_api_name, api_entity=_api_entity, auto_commit=True, call_level=1)
    api_result = action_result
    api_result.update({'api_action': _api_action, 'api_name': _api_name})
    
    if thisApp.application_configuration.database_api_debug or debug: print_api_result(f"{msgPrefix} result:", api_result)
    return api_result
#::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
def dbapi_bank_subscription(session, action, input_dict, filter_dict={}, caller_dict={}):
    _api_name = "dbapi_bank_subscription"
    _api_entity = 'BANK_SUBSCRIPTION'
    _api_action = action
    debug = False

    msgPrefix=f"#C9#{_api_name}#RESET# [{_api_action.upper()}]#RESET#"

    msgStart=f"{msgPrefix} start: input_dict=[[{input_dict}]]"
    if thisApp.application_configuration.database_api_debug or debug: print_message(msgStart)

    action_result = db_table_action(dbmodel.BANK_SUBSCRIPTION, action , input_dict, filter_dict, caller_dict={}, api_name=_api_name, api_entity=_api_entity, auto_commit=True, call_level=1)
    api_result = action_result
    api_result.update({'api_action': _api_action, 'api_name': _api_name})
    
    if thisApp.application_configuration.database_api_debug or debug: print_api_result(f"{msgPrefix} result:", api_result)
    return api_result
#::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
def dbapi_bank_account(session, action, input_dict, filter_dict={}, caller_dict={}):
    _api_name = "dbapi_bank_account"
    _api_entity = 'BANK_ACCOUNT'
    _api_action = action
    debug = False

    msgPrefix=f"#C9#{_api_name}#RESET# [{_api_action.upper()}]#RESET#"

    msgStart=f"{msgPrefix} start: input_dict=[[{input_dict}]]"
    if thisApp.application_configuration.database_api_debug or debug: print_message(msgStart)

    action_result = db_table_action(dbmodel.BANK_ACCOUNT, action , input_dict, filter_dict, caller_dict={}, api_name=_api_name, api_entity=_api_entity, auto_commit=True, call_level=1)
    api_result = action_result
    api_result.update({'api_action': _api_action, 'api_name': _api_name})
    
    if thisApp.application_configuration.database_api_debug or debug: print_api_result(f"{msgPrefix} result:", api_result)
    return api_result
#::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
#::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
#::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
#::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
#::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
#::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
#::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
# #::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
def xdbapi_client_confirm(session, input_dict):
    _api_name="dbapi_client_confirm"
    _api_action = 'confirm'
    _api_entity='CLIENT'

    msgPrefix=f"#C9#{_api_name}#RESET# [{_api_action.upper()}]#RESET#"

    msgP=f"{msgPrefix} start: input_dict=[[{input_dict}]]"
    if thisApp.application_configuration.database_api_debug or debug: print_message(msgP)

    action = 'confirm'
    filter_dict={}
    api_result = db_table_action(dbmodel.CLIENT, action , input_dict, filter_dict, caller_dict={}, api_name=_api_name, api_entity=_api_entity, auto_commit=True, call_level=1)
    if not api_result.get('api_status') == 'success':
        if thisApp.application_configuration.database_api_debug or debug: print_api_result(f"[{_api_name}] result:", api_result)
        return api_result
        
    client_id = api_result.get('api_data', {}).get('client_id')
    status = api_result.get('api_data', {}).get('status')
    client_type = api_result.get('api_data', {}).get('client_type')
    if not client_id:
        msg = f'client not found'
        api_result.update({'api_message':msg})
        api_result.update({'api_status':'error'})
        if thisApp.application_configuration.database_api_debug or debug: print_api_result(f"{msgPrefix} result:", api_result)
        return api_result

    action = 'update_rows'
    filter_dict = {'client_id': client_id}
    if client_type == 'merchant':
        update_dict={'status':status}
        api_result = db_table_action(dbmodel.MERCHANT, action , input_dict, filter_dict, caller_dict={}, api_name=_api_name, api_entity=_api_entity, auto_commit=True, call_level=1)
    elif client_type == 'consumer':
        update_dict={'status':status}
        api_result = db_table_action(dbmodel.CONSUMER, action , input_dict, filter_dict, caller_dict={}, api_name=_api_name, api_entity=_api_entity, auto_commit=True, call_level=1)
    elif client_type == 'service_provider':
        update_dict={'status':status}
        api_result = db_table_action(dbmodel.SERVICE_PROVIDER, action , input_dict, filter_dict, caller_dict={}, api_name=_api_name, api_entity=_api_entity, auto_commit=True, call_level=1)

    msg = f'client confirmed'
    api_result.update({'api_message':msg})
    api_result.update({'api_status':'success'})
    if thisApp.application_configuration.database_api_debug or debug: print_api_result(f"{msgPrefix} result:", api_result)
    return api_result
# #::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
# def dbapi_client_update(client_record, user='?', device_uid=None, geolocation_lat=None, geolocation_lon=None):
#     result = clients.try_update(client_record)
#     if not result.get('api_status') == 'success':
#         return result
#     client=result.get('api_data')
#     if not client:
#         msg = f'client not updated. (not found-system error)'
#         ##log_message(msg,msgType='error')
#         return {'api_status': 'error', 'api_message': msg}
#     client_id=client.get('client_id')
#     msg = f'client {client_id} updated.'
#     return {'api_status':'success','api_message':msg,'api_data':client}
# #::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
# def dbapi_client_unregister(client_record, user='?', device_uid=None, geolocation_lat=None, geolocation_lon=None):
#     client_record.update({'status':'UnRegistered'})
#     result = clients.try_update(client_record)
#     if not result.get('api_status') == 'success':
#         return result
#     client=result.get('api_data')
#     if not client:
#         msg = f'client not unregistered (not found-system error)'
#         ##log_message(msg,msgType='error')
#         return {'api_status': 'error', 'api_message': msg}

#     client_id = client.get('client_id')
#     msg=f'client {client_id} Unregistered'

#     where_expression = f"client_id='{client_id}'"
#     if client.get('client_type') == 'merchant':
#         update_expr={'status':'UnRegistered'}
#         res = merchants.update_rows(where_expression, update_expr)
#         merchants_unregistered = res.get('changed_records', 0)
#         msg = f'client {client_id} Unregistered. {merchants_unregistered} merchant(s) Unregistered'
#         merchants
#     if client.get('client_type') == 'consumer':
#         update_expr={'status':'UnRegistered'}
#         res = consumers.update_rows(where_expression, update_expr)
#         consumers_unregistered = res.get('changed_records', 0)
#         msg = f'client {client_id} Unregistered. {consumers_unregistered} consumer(s) Unregistered'

#     update_expr={'status':'UnRegistered'}
#     res = BANK_ACCOUNTS.update_rows(where_expression, update_expr)
#     accounts_unregistered = res.get('changed_records', 0)
#     msg1 = f'{accounts_unregistered} bank account(s) Unregistered'
#     msg=msg+'. '+msg1
#     res = bank_subscriptions.update_rows(where_expression, update_expr)
#     subscriptions_unregistered = res.get('changed_records', 0)
#     msg2 = f'{subscriptions_unregistered} bank subscriptions(s) Unregistered'
#     msg=msg+'. '+msg2

#     return {'api_status':'success','api_message':msg,'api_data':client}
# #::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
def dbapi_client_banksubscription_register(session, bank_subscription_record, user='?', device_uid=None, geolocation_lat=None, geolocation_lon=None):
    debug = False
    bank_subscriptionID = bank_subscription_record.get('bank_subscriptionID')
    if not bank_subscriptionID:
        msg = f'bank_subscriptionID not provided'
        ##log_message(msg,msgType='error')
        return {'api_status': 'error', 'api_message': msg}
    authorization = bank_authorizations.get(bank_subscription_record)
    if not authorization:
        msg = f'no authorization matched in bank_authorizations'
        print(msg)
        return {'api_status': 'error', 'api_message': msg}
    if not authorization.get('status') in ('Committed','Authorized'):
        msg = f"authorization not provided by client. status:{authorization.get('status')}"
        print(msg)
        return {'api_status': 'error', 'api_message': msg}

    bank_subscription_record.update({'bank_authorization_id':authorization.get('bank_authorization_id')})

    client = clients.get(bank_subscription_record,user=user)
    if not client:
        msg = f'client not found'
        ##log_message(msg,msgType='error')
        return {'api_status': 'error', 'api_message': msg}
    
    if not client.get('status')=='Active':
        msg = f"client not Active.(status:{client.get('status','')})"
        ##log_message(msg,msgType='error')
        return {'api_status': 'error', 'api_message': msg}

    client_id=client.get('client_id')
    client_email=client.get('email')
    client_type=client.get('client_type')

    bank_subscription_record.update({'client_id': client_id})
    bank_subscription_record.update({'client_type': client_type})
    bank_subscription_record.update({'client_name': client_email})

    bank = banks.get(bank_subscription_record)
    if not bank:
        msg = f'bank not found'
        ##log_message(msg,msgType='error')
        return {'api_status': 'error', 'api_message': msg}
    
    if not bank.get('status')=='Active':
        msg = f"bank not Active.(status:{bank.get('status','')})"
        ##log_message(msg,msgType='error')
        return {'api_status': 'error', 'api_message': msg}
        
    bank_subscription_record.update({'bank_code': bank.get('bank_code')})
    bank_subscription_record.update({'bank_BIC': bank.get('bank_BIC')})
    bank_subscription_record.update({'bank_id': bank.get('bank_id')})

    #here we need to invoke the bank api to get subscription

    bank_subscription_record.update({'bank_subscriptionID': bank_subscriptionID})
    
    result=dbapi_bank_subscription_register(bank_subscription_record, user=user)
    return result
#::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
#::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
#::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
# def xdbapi_service_provider_confirm(input_dict):
#     _api_name="dbapi_service_provider_confirm"
#     _api_action = 'confirm'
#     messages = []
#     rows_updated = 0
#     rows_added = 0

#     msgPrefix=f"#C9#{_api_name}#RESET# [{_api_action.upper()}]#RESET#"

#     msgP=f"{msgPrefix} start: input_dict=[[{input_dict}]]"
#     if thisApp.application_configuration.database_api_debug or debug: print_message(msgP)

#     service_provider_dict = dbschema.SERVICE_PROVIDERS_TABLE.get(input_dict, 'DICT')
#     if not service_provider_dict:
#         msg = f'service provider not found'
#         action_status='error'
#         api_result = {'api_status': action_status, 'api_message': msg, 'api_data': input_dict, 'messages': messages, 'rows_added': rows_added, 'rows_updated': rows_updated, 'api_action': _api_action.upper(), 'api_name': _api_name}
#         msgP = msgPrefix+" "+colorized_message(msg,"#"+action_status.upper()+"#")
#         if thisApp.application_configuration.database_api_debug or debug: print_api_result(f"{msgPrefix} result:", api_result)
#         return api_result

#     client_dict=dbschema.CLIENTS_TABLE.get(service_provider_dict,'DICT' )
#     if not client_dict:
#         msg = f'client not found'
#         action_status='error'
#         api_result = {'api_status': action_status, 'api_message': msg, 'api_data': service_provider_dict, 'messages': messages, 'rows_added': rows_added, 'rows_updated': rows_updated, 'api_action': _api_action.upper(), 'api_name': _api_name}
#         msgP = msgPrefix+" "+colorized_message(msg,"#"+action_status.upper()+"#")
#         if thisApp.application_configuration.database_api_debug or debug: print_api_result(f"{msgPrefix} result:", api_result)
#         return api_result

#     api_result = dbapi_client_confirm(client_dict)
#     if not api_result.get('api_status') == 'success':
#         msg = f'client confirmation failed'
#         api_result.update({'api_message':msg})
#         if thisApp.application_configuration.database_api_debug or debug: print_api_result(f"{msgPrefix} result:", api_result)
#         return api_result

#     service_provider_dict = dbschema.SERVICE_PROVIDERS_TABLE.get(service_provider_dict, 'DICT')
#     status=service_provider_dict.get('status')
#     if not service_provider_dict.get('status') == 'Active':
#         msg = f"service provider not confirmed. status={status}"
#         action_status='error'
#         api_result = {'api_status': action_status, 'api_message': msg, 'api_data': service_provider_dict, 'messages': messages, 'rows_added': rows_added, 'rows_updated': rows_updated, 'api_action': _api_action.upper(), 'api_name': _api_name}
#         if thisApp.application_configuration.database_api_debug or debug: print_api_result(f"{msgPrefix} result:", api_result)
#         return api_result

#     msg = f"OK. service provider confirmed. status={status}"
#     action_status='success'
#     api_result = {'api_status': action_status, 'api_message': msg, 'api_data': service_provider_dict, 'messages': messages, 'rows_added': rows_added, 'rows_updated': rows_updated, 'api_action': _api_action.upper(), 'api_name': _api_name}
#     if thisApp.application_configuration.database_api_debug or debug: print_api_result(f"{msgPrefix} result:", api_result)
#     return api_result
# #::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
# #::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
# #::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
# def dbapi_merchant_register(merchant_record, user='?', device_uid=None, geolocation_lat=None, geolocation_lon=None):
#     merchant_record.update({'client_type':'merchant'})
#     client = clients.refresh(merchant_record)
#     # if not result.get('api_status') == 'success' and  not result.get('api_data'):
#     #     return result
#     # client=result.get('api_data')
#     if not client:
#         msg = f'client not registered (not found-system error)'
#         ##log_message(msg,msgType='error')
#         return {'api_status': 'error', 'api_message': msg}

#     if not client.get('status')=='Active':
#         msg = f"client not confirmed.(status:{client.get('status','')})"
#         ###log_message(msg,msgType='warning')
#         #return {'api_status': 'error', 'api_message': msg}

#     merchant_record.update({'client_id':client.get('client_id')})
#     merchant_record.update({'status':client.get('status')})
#     merchant = merchants.refresh(merchant_record)
#     # if not result.get('api_status') == 'success':
#     #     if not result.get('api_data'):
#     #         return result
#     #     else:
#     #         merchant = merchants.refresh(merchant_record, user=user)
#     #         msg = f"merchant already registered"
#     #         return {'api_status': 'ok', 'api_message': msg, 'api_data': merchant}
#     # else:
#     #     merchant=result.get('api_data')

#     if not merchant:
#         msg = f'merchant not registered (not found-system error)'
#         #log_message(msg,msgType='error')
#         return {'api_status': 'error', 'api_message': msg}

#     if not merchant.get('status')=='Active':
#         msg = f"merchant registered but not confirmed.(status:{merchant.get('status','')})"
#     else:
#         msg = f"merchant registered"

#     return {'api_status': 'success', 'api_message': msg,'api_data':merchant}
# #::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
# def dbapi_merchant_confirm(merchant_record, user='?', device_uid=None, geolocation_lat=None, geolocation_lon=None):
#     merchant_record.update({'client_type':'merchant','status':'Active'})
#     client=clients.get(merchant_record)
#     if not client:
#         msg = f'client not confirmed. (not-found)'
#         #log_message(msg,msgType='error')
#         return {'api_status': 'error', 'api_message': msg}

#     dbapi_client_confirm(client)
#     merchants.update(merchant_record)
# #::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
# def dbapi_merchant_update(merchant_record, user='?', device_uid=None, geolocation_lat=None, geolocation_lon=None):
#     result = merchants.try_update(merchant_record, user=user)
#     if not result.get('api_status') == 'success':
#         return result
#     merchant=result.get('api_data')
#     if not merchant:
#         msg = f'merchant not updated (not found-system error)'
#         #log_message(msg,msgType='error')
#         return {'api_status': 'error', 'api_message': msg}
#     merchant_id=merchant.get('merchant_id')
#     msg = f'merchant {merchant_id} updated.'
#     return {'api_status':'success','api_message':msg,'api_data':merchant}
# #::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
# def dbapi_merchant_unregister(merchant_record, user='?', device_uid=None, geolocation_lat=None, geolocation_lon=None):
#     merchant_record.update({'status':'UnRegistered'})
#     result = merchants.try_update(merchant_record, user=user)
#     if not result.get('api_status') == 'success':
#         return result
#     merchant=result.get('api_data')
#     if not merchant:
#         msg = f'merchant not unregistered (not found-system error)'
#         #log_message(msg,msgType='error')
#         return {'api_status': 'error', 'api_message': msg}
#     merchant_id=merchant.get('merchant_id')
#     msg = f'merchant {merchant_id} unregistered.'

#     client_id=merchant.get('client_id')
#     where_expression = f"client_id='{client_id}'"
#     update_expr={'status':'UnRegistered'}
#     res = BANK_ACCOUNTS.update_rows(where_expression, update_expr)
#     accounts_unregistered = res.get('changed_records', 0)
#     msg1 = f'{accounts_unregistered} bank account(s) Unregistered'
#     msg=msg+'. '+msg1
#     res = bank_subscriptions.update_rows(where_expression, update_expr)
#     subscriptions_unregistered = res.get('changed_records', 0)
#     msg2 = f'{subscriptions_unregistered} bank subscriptions(s) Unregistered'
#     msg=msg+'. '+msg2
#     return {'api_status':'success','api_message':msg,'api_data':merchant}
# #::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
def dbapi_merchant_get_bankaccounts(session, merchant_record, user='?', device_uid=None, geolocation_lat=None, geolocation_lon=None):
    debug = False

    merchant = merchants.get(merchant_record,user=user)
    if not merchant:
        msg = f'merchant not found'
        #log_message(msg,msgType='error')
        return []
    
    if not merchant.get('status')=='Active':
        msg = f"merchant not Active.(status:{merchant.get('status','')})"
        #log_message(msg,msgType='error')
        return []

    # merchant_id=merchant.get('merchant_id')
    # merchant_name=merchant.get('name')
    client_id = merchant.get('client_id')

    where_expression=f"client_id='{client_id}' and status='Active'" 
    accounts = BANK_ACCOUNTS.retrieve_records(where_expression)
    merchant_accounts=[]
    for account in accounts:
        bank_account_id = account.get('bank_account_id')
        if bank_account_id:
            merchant_accounts.append(bank_account_id)
    return accounts
#::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
def dbapi_merchant_bankaccount_register(session, bankaccount_record, user='?', device_uid=None, geolocation_lat=None, geolocation_lon=None):
    debug = False

    merchant = merchants.get(bankaccount_record,user=user)
    if not merchant:
        msg = f'merchant not found'
        #log_message(msg,msgType='error')
        return {'api_status': 'error', 'api_message': msg}
    
    if not merchant.get('status')=='Active':
        msg = f"merchant not Active.(status:{merchant.get('status','')})"
        #log_message(msg,msgType='error')
        return {'api_status': 'error', 'api_message': msg}

    if not bankaccount_record.get('bank_account') and not bankaccount_record.get('bank_account_id'):
        msg = f"bank account not provided"
        return {'api_status': 'error', 'api_message': msg}
    if bankaccount_record.get('bank_account'):
        bank_account_id = bankaccount_record.get('bank_account')
    if bankaccount_record.get('bank_account_id'):
        bank_account_id = bankaccount_record.get('bank_account_id')
    
    merchant_id = merchant.get('merchant_id')
    
    account = BANK_ACCOUNTS.get(bank_account_id)
    if not account:
        msg = f"bank account not found"
        return {'api_status': 'error', 'api_message': msg}
    if not account.get('status')=='Active':
        msg = f"bank account not Active"
        return {'api_status': 'error', 'api_message': msg}

    merchant_record = account
    merchant_record.update({'merchant_id': merchant_id})
    return dbapi_merchant_update(merchant_record)
#::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
#::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
# def dbapi_pointofsale_register(pointofsale_record, user='?', device_uid=None, geolocation_lat=None, geolocation_lon=None):
#     mrec={'merchant_name':pointofsale_record.get('merchant_name'),'merchant_id':pointofsale_record.get('merchant_id')}
#     merchant = merchants.get_one(mrec)
#     if not merchant:
#         msg = f'merchant not found'
#         #log_message(msg,msgType='error')
#         return {'api_status': 'error', 'api_message': msg}
    
#     if not merchant.get('status')=='Active':
#         msg = f"merchant not Active.(status:{merchant.get('status','')})"
#         #log_message(msg,msgType='error')
#         return {'api_status': 'error', 'api_message': msg}

#     pointofsale_record.update({'merchant_id':merchant.get('merchant_id')})
#     pointofsale_record.update({'status':merchant.get('status')})
#     pointofsale = points_of_sale.refresh(pointofsale_record,user=user)
#     # if not result.get('api_status') == 'success':
#     #     if not result.get('api_data'):
#     #         return result
#     #     else:
#     #         pointofsale = points_of_sale.refresh(pointofsale_record, user=user)
#     #         msg = f"pointofsale already registered"
#     #         return {'api_status': 'ok', 'api_message': msg, 'api_data': pointofsale}            
#     # else:
#     #     pointofsale=result.get('api_data')

#     if not pointofsale:
#         msg = f'pointofsale not found. system error'
#         #log_message(msg,msgType='error')
#         return {'api_status': 'error', 'api_message': msg}

#     pointofsale_id=pointofsale.get('pointofsale_id')
#     msg = f'pointofsale {pointofsale_id} registered.'

#     if not pointofsale.get('status')=='Active':
#         msg = f"pointofsale {pointofsale_id} registered but is not active.(status:{pointofsale.get('status','')})"
#     else:
#         msg = f"pointofsale {pointofsale_id} registered."

#     return {'api_status':'success','api_message':msg,'api_data':pointofsale}
# #::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
# def dbapi_pointofsale_update(pointofsale_record, user='?', device_uid=None, geolocation_lat=None, geolocation_lon=None):
#     result = points_of_sale.try_update(pointofsale_record,user=user)
#     if not result.get('api_status') == 'success':
#         return result
#     pointofsale=result.get('api_data')
#     if not pointofsale:
#         msg = f'pointofsale not found.system error'
#         #log_message(msg,msgType='error')
#         return {'api_status': 'error', 'api_message': msg}

#     pointofsale_id=pointofsale.get('pointofsale_id')
#     msg = f'pointofsale {pointofsale_id} updated.'
#     return {'api_status':'success','api_message':msg,'api_data':pointofsale}
# #::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
# def dbapi_pointofsale_unregister(pointofsale_record, user='?', device_uid=None, geolocation_lat=None, geolocation_lon=None):
#     pointofsale_record.update({'status':'UnRegistered'})
#     result = points_of_sale.try_update(pointofsale_record,user=user)
#     if not result.get('api_status') == 'success':
#         return result
#     pointofsale=result.get('api_data')
#     if not pointofsale:
#         msg = f'pointofsale not unregistered. (not found-system error)'
#         #log_message(msg,msgType='error')
#         return {'api_status': 'error', 'api_message': msg}
#     pointofsale_id=pointofsale.get('pointofsale_id')
#     msg = f'pointofsale {pointofsale_id} unregistered.'
#     return {'api_status':'success','api_message':msg,'api_data':pointofsale}
#::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
def dbapi_pointofsale_bankaccount_add(session, bankaccount_record, user='?', device_uid=None, geolocation_lat=None, geolocation_lon=None):
    debug = False

    pointofsale = points_of_sale.get(bankaccount_record,user=user)
    if not pointofsale:
        msg = f'pointofsale not found'
        #log_message(msg,msgType='error')
        return {'api_status': 'error', 'api_message': msg}
    
    if not pointofsale.get('status')=='Active':
        msg = f"pointofsale not Active.(status:{pointofsale.get('status','')})"
        #log_message(msg,msgType='error')
        return {'api_status': 'error', 'api_message': msg}

    if not bankaccount_record.get('bank_account') and not bankaccount_record.get('bank_account_id'):
        msg = f"bank account not provided"
        return {'api_status': 'error', 'api_message': msg}
    if bankaccount_record.get('bank_account'):
        bank_account_id = bankaccount_record.get('bank_account')
    if bankaccount_record.get('bank_account_id'):
        bank_account_id = bankaccount_record.get('bank_account_id')
    
    pointofsale_id = pointofsale.get('pointofsale_id')
    
    account = BANK_ACCOUNTS.get(bank_account_id)
    if not account:
        msg = f"bank account not found"
        return {'api_status': 'error', 'api_message': msg}
    if not account.get('status')=='Active':
        msg = f"bank account not Active"
        return {'api_status': 'error', 'api_message': msg}

    pointofsale_record = account
    pointofsale_record.update({'pointofsale_id': pointofsale_id})
    return dbapi_pointofsale_update(pointofsale_record)
#::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
def dbapi_pointofsale_bankaccount_remove(session, pointofsale_record, user='?', device_uid=None, geolocation_lat=None, geolocation_lon=None):
    debug = False

    pointofsale = points_of_sale.get(pointofsale_record)
    if not pointofsale:
        msg = f'pointofsale not found'
        #log_message(msg,msgType='error')
        return {'api_status': 'error', 'api_message': msg}
    
    if not pointofsale.get('status')=='Active':
        msg = f"pointofsale not Active.(status:{pointofsale.get('status','')})"
        #log_message(msg,msgType='error')
        return {'api_status': 'error', 'api_message': msg}

    pointofsale_record.update({
        'bank_account_id'       :'',
        'bank_subscription_id'  :'',
        'bank_code'             :'',
        'bank_subscriptionID'   :'',
        'bank_accountID'        :'',
        'payments_currency': '',
        })

    return dbapi_pointofsale_update(pointofsale_record)
#::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
# def dbapi_employee_register(employee_record, user='?', device_uid=None, geolocation_lat=None, geolocation_lon=None):
#     mrec={'merchant_name':employee_record.get('merchant_name'),'merchant_id':employee_record.get('merchant_id')}
#     merchant = merchants.get_one(mrec)
#     if not merchant:
#         msg = f'merchant not found'
#         #log_message(msg,msgType='error')
#         return {'api_status': 'error', 'api_message': msg}
        
#     if not merchant.get('status')=='Active':
#         msg = f"merchant not Active.(status:{merchant.get('status','')})"
#         # #log_message(msg,msgType='error')
#         return {'api_status': 'error', 'api_message': msg}

#     employee_record.update({'merchant_id':merchant.get('merchant_id')})
#     employee_record.update({'status': 'Active'})
    
#     employee = employees.refresh(employee_record,user=user)
#     # if not result.get('api_status') == 'success':
#     #     if not result.get('api_data'):
#     #         return result
#     #     else:
#     #         employee = employees.refresh(employee_record, user=user)
#     #         msg = f"employee already registered"
#     #         return {'api_status': 'ok', 'api_message': msg, 'api_data': employee}            
#     # else:
#     #     employee=result.get('api_data')

#     if not employee:
#         msg = f'employee not registered (not found-system error)'
#         #log_message(msg,msgType='error')
#         return {'api_status': 'error', 'api_message': msg}
#     if not employee.get('status')=='Active':
#         msg = f"employee registered but not Active.(status:{employee.get('status','')})"
#         ##log_message(msg,msgType='error')
#         return {'api_status': 'error', 'api_message': msg}
#     else:
#         msg='employee registered'
#     return {'api_status': 'success', 'api_message': msg,'api_data':employee}
# #::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
# def dbapi_employee_update(employee_record, user='?', device_uid=None, geolocation_lat=None, geolocation_lon=None):
#     result = employees.try_update(employee_record,user=user)
#     if not result.get('api_status') == 'success':
#         return result
#     employee=result.get('api_data')
#     if not employee:
#         msg = f'employee not updated. (not found-system error)'
#         #log_message(msg,msgType='error')
#         return {'api_status': 'error', 'api_message': msg}
#     employee_id=employee.get('employee_id')
#     msg = f'employee {employee_id} updated.'
#     return {'api_status':'success','api_message':msg,'api_data':employee}
# #::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
# def dbapi_employee_unregister(employee_record, user='?', device_uid=None, geolocation_lat=None, geolocation_lon=None):
#     employee_record.update({'status':'UnRegistered'})
#     result = employees.try_update(employee_record,user=user)
#     if not result.get('api_status') == 'success':
#         return result
#     employee=result.get('api_data')
#     if not employee:
#         msg = f'employee not unregistered (not found-system error)'
#         #log_message(msg,msgType='error')
#         return {'api_status': 'error', 'api_message': msg}
#     employee_id=employee.get('employee_id')
#     msg = f'employee {employee_id} unregistered.'
#     return {'api_status':'success','api_message':msg,'api_data':employee}
# #::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
def dbapi_pointofsale_credit_info(session, pointofsale_record, user='?', device_uid=None, geolocation_lat=None, geolocation_lon=None):
    debug = False

    pointofsale = points_of_sale.get(pointofsale_record,user=user)
    if not pointofsale:
        msg = f'pointofsale not found'
        #log_message(msg,msgType='error')
        return {'api_status': 'error', 'api_message': msg}
    
    if not pointofsale.get('status')=='Active':
        msg = f"pointofsale not Active.(status:{pointofsale.get('status','')})"
        #log_message(msg,msgType='error')
        return {'api_status': 'error', 'api_message': msg}

    pointofsale_id=pointofsale.get('pointofsale_id')
    merchant_id=pointofsale.get('merchant_id')
    pointofsale_name=pointofsale.get('name')
    merchant = merchants.get(merchant_id)
    #client_id = merchant.get('client_id')
    bank_account_id = pointofsale.get('bank_account_id')
    bank_subscription_id = pointofsale.get('bank_subscription_id')
    bank_code = pointofsale.get('bank_code')
    bank_subscriptionID = pointofsale.get('bank_subscriptionID')
    bank_accountID = pointofsale.get('bank_accountID')
    payments_currency = pointofsale.get('payments_currency')

    if not bank_accountID:
        bank_account_id = merchant.get('bank_account_id')
        bank_subscription_id = merchant.get('bank_subscription_id')
        bank_code = merchant.get('bank_code')
        bank_subscriptionID = merchant.get('bank_subscriptionID')
        bank_accountID = merchant.get('bank_accountID')
        payments_currency = merchant.get('payments_currency')
        

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
    return credit_info
#::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
#::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
#::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
# def dbapi_consumer_register(consumer_record, user='?', device_uid=None, geolocation_lat=None, geolocation_lon=None):
#     consumer_record.update({'client_type':'consumer'})
#     client = clients.refresh(consumer_record,user=user)
#     # if not result.get('api_status') == 'success' and  not result.get('api_data'):
#     #     return result
#     # client=result.get('api_data')
#     if not client:
#         msg = f'consumer not registered (not found-system error)'
#         #log_message(msg,msgType='error')
#         return {'api_status': 'error', 'api_message': msg}


#     if not client.get('status')=='Active':
#         msg = f"client not confirmed.(status:{client.get('status','')})"
#         ##log_message(msg,msgType='error')
#         #return {'api_status': 'error', 'api_message': msg}

#     consumer_record.update({'client_id':client.get('client_id')})
#     consumer_record.update({'status':client.get('status')})
#     consumer = consumers.refresh(consumer_record,user=user)
#     # if not result.get('api_status') == 'success':
#     #     if not result.get('api_data'):
#     #         return result
#     #     else:
#     #         consumer = consumers.refresh(consumer_record, user=user)
#     #         msg = f"consumer already registered"
#     #         return {'api_status': 'ok', 'api_message': msg, 'api_data': consumer}            
#     # else:
#     #     consumer=result.get('api_data')

#     if not consumer:
#         msg = f'consumer not registered (not found)'
#         #log_message(msg,msgType='error')
#         return {'api_status': 'error', 'api_message': msg}

#     consumer_id=consumer.get('consumer_id')
#     msg = f'consumer {consumer_id} registered.'

#     if not consumer.get('status')=='Active':
#         msg = f"consumer {consumer_id} registered but not Active.(status:{consumer.get('status','')})"
#     else:
#         msg='consumer {consumer_id} registered'

#     return {'api_status':'success','api_message':msg,'api_data':consumer}
# #::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
# def dbapi_consumer_confirm(consumer_record, user='?', device_uid=None, geolocation_lat=None, geolocation_lon=None):
#     consumer_record.update({'client_type':'consumer'})
#     client=clients.get(consumer_record,user=user)
#     if not client:
#         msg = f'client not found. system error'
#         #log_message(msg,msgType='error')
#         return {'api_status': 'error', 'api_message': msg}


#     consumer_record.update({'status': 'Active'})
#     client = clients.update(consumer_record)
#     if not client.get('status')=='Active':
#         msg = f"client not confirmed.(status:{client.get('status','')})"
#         #log_message(msg,msgType='error')
#         return {'api_status': 'error', 'api_message': msg}

#     consumer_record.update({'client_id':client.get('client_id')})
#     consumer_record.update({'status':client.get('status')})
#     consumer = consumers.get(consumer_record, user=user)
#     if not consumer:
#         msg = f"consumer not found"
#         #log_message(msg,msgType='error')
#         return {'api_status': 'error', 'api_message': msg}
#     else:
#         if consumer.get('status')=='Active':
#             msg = f"consumer already confirmed"
#             return {'api_status': 'ok', 'api_message': msg, 'api_data': consumer}            

#     consumer = consumers.refresh(consumer_record, user=user)
#     # if not result.get('api_status') == 'success':
#     #     if not result.get('api_data'):
#     #         return result
    
#     # consumer=result.get('api_data')

#     if not consumer:
#         msg = f'consumer not confirmed (not found-system error)'
#         #log_message(msg,msgType='error')
#         return {'api_status': 'error', 'api_message': msg}

#     if not consumer.get('status')=='Active':
#         msg = f"consumer not confirmed.(status:{consumer.get('status','')})"
#         #log_message(msg,msgType='error')
#         return {'api_status': 'error', 'api_message': msg}

#     return {'api_status': 'success', 'api_data': consumer}
# #::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
# def dbapi_consumer_update(consumer_record, user='?', device_uid=None, geolocation_lat=None, geolocation_lon=None):
#     result = consumers.try_update(consumer_record,user=user)
#     if not result.get('api_status') == 'success':
#         return result
#     consumer=result.get('api_data')
#     if not consumer:
#         msg = f'consumer not updated. (not found-system error)'
#         #log_message(msg,msgType='error')
#         return {'api_status': 'error', 'api_message': msg}

#     return result
# #::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
# def dbapi_consumer_unregister(consumer_record, user='?', device_uid=None, geolocation_lat=None, geolocation_lon=None):
#     consumer_record.update({'status':'UnRegistered'})
#     result = consumers.try_update(consumer_record,user=user)
#     if not result.get('api_status') == 'success':
#         return result
#     consumer=result.get('api_data')
#     if not consumer:
#         msg = f'consumer not unregistered. (not found-system error)'
#         #log_message(msg,msgType='error')
#         return {'api_status': 'error', 'api_message': msg}

#     return result
#::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
def dbapi_consumer_banksubscription_register(session, bank_subscription_record, user='?', device_uid=None, geolocation_lat=None, geolocation_lon=None):
    debug = False

    consumer = consumers.get(bank_subscription_record,user=user)
    if not consumer:
        msg = f'consumer not found'
        #log_message(msg,msgType='error')
        return {'api_status': 'error', 'api_message': msg}
    
    if not consumer.get('status')=='Active':
        msg = f"consumer not Active.(status:{consumer.get('status','')})"
        #log_message(msg,msgType='error')
        return {'api_status': 'error', 'api_message': msg}

    consumer_id=consumer.get('consumer_id')
    consumer_name=consumer.get('name')

    bank_subscription_record.update({'owner_type': 'consumer'})
    bank_subscription_record.update({'owner_id': consumer_id})
    bank_subscription_record.update({'owner_name': consumer_name})

    result=dbapi_bank_subscription_register(bank_subscription_record, user=user)
    return result
#::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::

#::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
#::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
#::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
def dbapi_interaction_start(session, interaction_record, user='?', device_uid=None, geolocation_lat=None, geolocation_lon=None):
    debug = False

    consumer_id = interaction_record.get('consumer_id')
    if consumer_id:
        consumer = consumers.get(interaction_record)
        if not consumer:
            msg = f'consumer not found'
            #log_message(msg,msgType='error')
            return {'api_status': 'error', 'api_message': msg}
        originator='consumer'
        originator_id=consumer_id
    else:
        pointofsale_id = interaction_record.get('pointofsale_id')
        if pointofsale_id:
            pointofsale = points_of_sale.get(interaction_record)
            if not pointofsale:
                msg = f'pointofsale not found'
                #log_message(msg,msgType='error')
                return {'api_status': 'error', 'api_message': msg}
            originator='pointofsale'
            originator_id=pointofsale_id
        else:
            client_id = interaction_record.get('client_id')
            if client_id:
                client = clients.get(interaction_record)
                if not client:
                    msg = f'client not found'
                    #log_message(msg,msgType='error')
                    return {'api_status': 'error', 'api_message': msg}
                originator='client'
                originator_id=client_id
            else:
                msg = f'no pointofsale or consumer or client defined'
                #log_message(msg,msgType='error')
                return {'api_status': 'error', 'api_message': msg}

    interaction_record.update({'originator': originator})
    interaction_record.update({'originator_id': originator_id})

    xcorresponder = interaction_record.get('corresponder')
    corresponder_id = interaction_record.get('corresponder_id')
    if not corresponder_id:
        msg = f'no corresponder specified'
        #log_message(msg,msgType='error')
        return {'api_status': 'error', 'api_message': msg}

    xid = consumer.get(corresponder_id)
    if xid:
        corresponder='consumer'
        corresponder_id=xid
    else:
        xid = points_of_sale.get(corresponder_id)
        if xid:
            corresponder='pointofsale'
            corresponder_id=xid
        else:
            xid = clients.get(corresponder_id)
            if xid:
                corresponder='client'
                corresponder_id=xid
            else:
                msg = f'corresponder not valid'
                #log_message(msg,msgType='error')
                return {'api_status': 'error', 'api_message': msg}

    if not xcorresponder == corresponder:
        msg = f'corresponder_id not valid for corresponder {xcorresponder}'
        #log_message(msg,msgType='error')
        return {'api_status': 'error', 'api_message': msg}
        
    interaction_record.update({'corresponder': corresponder})
    interaction_record.update({'corresponder_id': corresponder_id})

    filterJson = f"originator='{originator}' AND originator_id='{originator_id}' and status=Active'"
    active_interactions = interactions.retrieve_rows(filterJson)
    if len(active_interactions) > 0:
        msg = f'already active interactions'
        #log_message(msg,msgType='error')
        #return {'api_status': 'error', 'api_message': msg}
        for active_interaction in active_interactions:
            interaction_id = active_interaction.get('interaction_id')
            #interaction_record.update('interaction_id':interaction_id)
            dbapi_interaction_finish(interaction_record)

    result = interactions.try_insert(interaction_record,user=user)
    if not result.get('api_status') == 'success' and  not result.get('api_data'):
        return result
    interaction = result.get('api_data')
    if not interaction:
        msg = f'interaction start failed (not found-system error)'
        #log_message(msg,msgType='error')
        return {'api_status': 'error', 'api_message': msg}
    interaction_id = interaction.get('interaction_id')
    if not interaction_id:
        msg = f'interaction start failed (interaction_id not found-system error)'
        #log_message(msg,msgType='error')
        return {'api_status': 'error', 'api_message': msg}

    interaction_message = {
        'interaction_id':interaction_id,
        'originator_id':interaction_record.get('originator_id'),
        'originator':interaction_record.get('originator'),
        'message_type':'start',
        'message_record':f"hi. i am {interaction_record.get('originator')} {interaction_record.get('originator_id')}",
        'content_type':'text',
        'format':'',
        }
    xresult = interaction_messages.try_insert(interaction_message,user=user)
    if not xresult.get('api_status') == 'success' and  not xresult.get('api_data'):
        return xresult
    interaction_message = xresult.get('api_data')
    if not interaction_message:
        msg = f'interaction start failed (message insert failed)'
        #log_message(msg,msgType='error')
        return {'api_status': 'error', 'api_message': msg}
    interaction_message_id = interaction_message.get('interaction_message_id')
    if not interaction_message_id:
        msg = f'interaction start failed (interaction_message_id not found-system error)'
        #log_message(msg,msgType='error')
        return {'api_status': 'error', 'api_message': msg}

    return result
#::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
def dbapi_interaction_finish(session, interaction_record, user='?', device_uid=None, geolocation_lat=None, geolocation_lon=None):
    debug = False

    consumer_id = interaction_record.get('consumer_id')
    if consumer_id:
        consumer = consumers.get(interaction_record)
        if not consumer:
            msg = f'consumer not found'
            #log_message(msg,msgType='error')
            return {'api_status': 'error', 'api_message': msg}
        originator='consumer'
        originator_id=consumer_id
        interaction_record.update({'originator': originator})
        interaction_record.update({'originator_id': originator_id})
    else:
        pointofsale_id = interaction_record.get('pointofsale_id')
        if pointofsale_id:
            pointofsale = points_of_sale.get(interaction_record)
            if not pointofsale:
                msg = f'pointofsale not found'
                #log_message(msg,msgType='error')
                return {'api_status': 'error', 'api_message': msg}
            originator='pointofsale'
            originator_id=pointofsale_id
            interaction_record.update({'originator': originator})
            interaction_record.update({'originator_id': originator_id})
        else:
            client_id = interaction_record.get('client_id')
            if client_id:
                client = clients.get(interaction_record)
                if not client:
                    msg = f'client not found'
                    #log_message(msg,msgType='error')
                    return {'api_status': 'error', 'api_message': msg}
                interaction_record.update({'originator': 'client'})
                interaction_record.update({'originator_id': client_id})
            else:
                msg = f'no pointofsale or consumer or client defined'
                #log_message(msg,msgType='error')
                return {'api_status': 'error', 'api_message': msg}

    if not interaction.get('corresponder') and  not interaction.get('originator_id')==originator_id:
        interaction.update({'corresponder': originator})
        interaction.update({'corresponder_id': originator_id})
        interaction=interactions.refresh(interaction,user=user)

    # filterJson={'originator':originator,'originator_id':originator_id,'status':'Active'}
    filterJson = f"originator='{originator}' AND originator_id='{originator_id}' and status=Active'"
    active_interactions = interactions.retrieve_rows(filterJson)
    if len(active_interactions) <= 0:
        msg = f'no active interactions'
        #log_message(msg,msgType='error')
        return {'api_status': 'error', 'api_message': msg}
        
    for active_interaction in active_interactions:
        interaction_id = active_interaction.get('interaction_id')
        interaction_message = {
            'interaction_id':interaction_id,
            'originator_id':interaction_record.get('originator_id'),
            'originator':interaction_record.get('originator'),
            'message_type':'finish',
            'message_record':f"goodbye. i am {interaction_record.get('originator')} {interaction_record.get('originator_id')}",
            'content_type':'text',
            'format':'',
            }
        result = interaction_messages.try_insert(interaction_message,user=user)
        # if not result.get('api_status') == 'success' and  not result.get('api_data'):
        #     return result
        interaction_message = result.get('api_data')
        if not interaction_message:
            msg = f'interaction finish failed (message insert failed)'
            #log_message(msg,msgType='error')
            #return {'api_status': 'error', 'api_message': msg}
        interaction_message_id = interaction_message.get('interaction_message_id')
        if not interaction_message_id:
            msg = f'interaction finish failed (interaction_message_id not found-system error)'
            #log_message(msg,msgType='error')
            #return {'api_status': 'error', 'api_message': msg}

        time_start_str = interaction.get('row_timestamp')
        time_start = datetime.datetime.strptime(time_start_str, '%Y-%m-%d %H:%M:%S')
        time_end = datetime.datetime.utcnow()
        diff = time_end - time_start  #this is a timedelta obj
        duration = diff.days * 24 * 60 * 60 + diff.seconds

        interaction.update({'status':'completed','completed_timestamp':time_end,'duration':duration})
        result = interactions.try_update(interaction,user=user)
        if not result.get('api_status') == 'success' and  not result.get('api_data'):
            return result
        interaction = result.get('api_data')
        if not interaction:
            msg = f'interaction finish failed (not found-system error)'
            #log_message(msg,msgType='error')
            return {'api_status': 'error', 'api_message': msg}
        interaction_id = interaction.get('interaction_id')
        if not interaction_id:
            msg = f'interaction finish failed (interaction_id not found-system error)'
            #log_message(msg,msgType='error')
            return {'api_status': 'error', 'api_message': msg}

    interaction_id = interaction_record.get('interaction_id')
    if not interaction_id:
        msg = f'interaction not defined'
        #log_message(msg,msgType='error')
        return {'api_status': 'error', 'api_message': msg}

    interaction = interactions.get(interaction_id)
    if not interaction:
        msg = f'interaction not found'
        #log_message(msg,msgType='error')
        return {'api_status': 'error', 'api_message': msg}


    return result
#::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
def dbapi_interaction_message_add(session, interaction_record, user='?', device_uid=None, geolocation_lat=None, geolocation_lon=None):
    debug = False

    interaction_id = interaction_record.get('interaction_id')
    if not interaction_id:
        msg = f'interaction not defined'
        #log_message(msg,msgType='error')
        return {'api_status': 'error', 'api_message': msg}

    interaction = interactions.get(interaction_id)
    if not interaction:
        msg = f'interaction not found'
        #log_message(msg,msgType='error')
        return {'api_status': 'error', 'api_message': msg}


    consumer_id = interaction_record.get('consumer_id')
    if consumer_id:
        consumer = consumers.get(interaction_record)
        if not consumer:
            msg = f'consumer not found'
            #log_message(msg,msgType='error')
            return {'api_status': 'error', 'api_message': msg}
        originator='consumer'
        originator_id=consumer_id
        interaction_record.update({'originator': originator})
        interaction_record.update({'originator_id': originator_id})
    else:
        pointofsale_id = interaction_record.get('pointofsale_id')
        if pointofsale_id:
            pointofsale = points_of_sale.get(interaction_record)
            if not pointofsale:
                msg = f'pointofsale not found'
                #log_message(msg,msgType='error')
                return {'api_status': 'error', 'api_message': msg}
            originator='pointofsale'
            originator_id=pointofsale_id
            interaction_record.update({'originator': originator})
            interaction_record.update({'originator_id': originator_id})
        else:
            msg = f'no pointofsale or consumer defined'
            #log_message(msg,msgType='error')
            return {'api_status': 'error', 'api_message': msg}

    if not interaction.get('corresponder') and  not interaction.get('originator_id')==originator_id:
    # if not interaction.get('originator') == originator and not interaction.get('corresponder'):
        interaction.update({'corresponder': originator})
        interaction.update({'corresponder_id': originator_id})
        interaction=interactions.refresh(interaction,user=user)

    interaction_message = {
        'interaction_id':interaction_id,
        'originator_id':interaction_record.get('originator_id',''),
        'originator':interaction_record.get('originator',''),
        'message_type':interaction_record.get('message_type','message'),
        'message_record':interaction_record.get('message_record',''),
        'content_type':interaction_record.get('content_type','text'),
        'format':interaction_record.get('format',''),
        }
    result = interaction_messages.try_insert(interaction_message,user=user)
    # if not result.get('api_status') == 'success' and  not result.get('api_data'):
    #     return result
    interaction_message = result.get('api_data')
    if not interaction_message:
        msg = f'interaction finish failed (message insert failed)'
        #log_message(msg,msgType='error')
        #return {'api_status': 'error', 'api_message': msg}
    interaction_message_id = interaction_message.get('interaction_message_id')
    if not interaction_message_id:
        msg = f'interaction finish failed (interaction_message_id not found-system error)'
        #log_message(msg,msgType='error')
        #return {'api_status': 'error', 'api_message': msg}

    # time_start_str = interaction.get('row_timestamp')
    # time_start = datetime.datetime.strptime(time_start_str, '%Y-%m-%d %H:%M:%S')
    # time_end = datetime.datetime.utcnow()
    # diff = time_end - time_start  #this is a timedelta obj
    # duration = diff.days * 24 * 60 * 60 + diff.seconds


    return result
#::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
#::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
#::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
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
def dbapi_bank_subscription_register(session, bank_subscription_record, user='?', device_uid=None, geolocation_lat=None, geolocation_lon=None):
    debug = False

    result = bank_subscriptions.refresh(bank_subscription_record)
    return result
    # bank_subscription = bank_subscriptions.refresh(bank_subscription_record, user=user)
    # if not bank_subscription:
    #     msg = f'bank_subscription not registered (not found)'
    #     #log_message(msg,msgType='error')
    #     return {'api_status': 'error', 'api_message': msg}

    # if not bank_subscription.get('status')=='Active':
    #     msg = f"bank_subscription is not Active.(status:{bank_subscription.get('status','')})"
    #     #log_message(msg,msgType='error')
    #     return {'api_status': 'error', 'api_message': msg,'api_data':bank_subscription}

    # msg = f"bank_subscription registered.(status:{bank_subscription.get('status','')})"
    # return {'api_status': 'success', 'api_message': msg,'api_data':bank_subscription}
#::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
def dbapi_bank_account_register(session, bank_account_record, user='?', device_uid=None, geolocation_lat=None, geolocation_lon=None):
    debug = False

    bank_subscription = bank_subscriptions.get(bank_account_record)
    if not bank_subscription:
        merchant_id = bank_account_record.get('merchant_id')
        if merchant_id:
            bank_account_record.update({'owner_type': 'merchant', 'owner_id': merchant_id})
            bank_subscription = bank_subscriptions.get(bank_account_record)
            if not bank_subscription:
                pointofsale_id = bank_account_record.get('pointofsale_id')
                if pointofsale_id:
                    bank_account_record.update({'owner_type': 'pointofsale', 'owner_id': pointofsale_id})
                    bank_subscription = bank_subscriptions.get(bank_account_record)
                    if not bank_subscription:
                        consumer_id = bank_account_record.get('consumer_id')
                        if consumer_id:
                            bank_account_record.update({'owner_type': 'consumer', 'owner_id': consumer_id})
                            bank_subscription = bank_subscriptions.get(bank_account_record)
                            if not bank_subscription:
                                client_id = bank_account_record.get('client_id')
                                if client_id:
                                    bank_account_record.update({'owner_type': 'client', 'owner_id': client_id})
                                    bank_subscription = bank_subscriptions.get(bank_account_record)
    if not bank_subscription:
        msg = f'bank_subscription not found'
        #log_message(msg,msgType='error')
        return {'api_status': 'error', 'api_message': msg}
    
    if not bank_subscription.get('status')=='Active':
        msg = f"bank_subscription not Active.(status:{bank_subscription.get('status','')})"
        #log_message(msg,msgType='error')
        return {'api_status': 'error', 'api_message': msg}

    bank_subscription_id=bank_subscription.get('bank_subscription_id')
    bank_subscription_name=bank_subscription.get('owner_name')
    bank_subscription_type=bank_subscription.get('owner_type')

    bank_account_record.update({'owner_type':bank_subscription_type})
    bank_account_record.update({'owner_id': bank_subscription_id})
    bank_account_record.update({'owner_name': bank_subscription_name})
    
    result=BANK_ACCOUNTS.insert_or_update(bank_account_record, user=user)
    return result
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
#                 bank_subscription_record = pending_authorization
#                 bank_subscription_record.update({'status': 'Active'})
#                 result=dbapi_client_banksubscription_register(bank_subscription_record)
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
def dbapi_cleanup_bank_authorizations(session):
    _api_name = "dbapi_cleanup_bank_authorizations"
    _api_entity = 'BANK_AUTHORIZATION'
    _api_action = 'CLEANUP'
    debug = False
    msgPrefix=f"#C9#{_api_name}#RESET# [{_api_action.upper()}]#RESET#"

    msgStart=f"{msgPrefix} start: action=[[{_api_action}]]"
    if thisApp.application_configuration.database_api_debug or debug: print_message(msgStart)

    where_expression = {'status': 'Expired'}
    deleted_result = dbschema.BANK_AUTHORIZATIONS_TABLE.delete_rows(where_expression, commit=True)
    deleted_rows = deleted_result.get('rows_deleted', 0)

    cutoff_timestamp = datetime.datetime.utcnow() - datetime.timedelta(seconds=60*60*60)
    cutoff_timestamp_str= cutoff_timestamp.strftime('%Y-%m-%d %H:%M:%S')
    where_expression = f"status='Pending' and row_timestamp<'{cutoff_timestamp_str}'"

    #nowString = datetime.datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S')
    #where_expression = f"expiryDT<'{datetime.datetime.utcnow()}'"
    where_expression = {'expiryDT': {datetime.datetime.utcnow()}}
    update_dict = {'status': 'Expired'}

    expired_result = dbschema.BANK_AUTHORIZATIONS_TABLE.update_rows(update_dict,where_expression, commit=True)
    expired_rows = expired_result.get('rows_updated', 0)

    msg = f'bank_authorizations cleaned with {expired_rows} authorizations expired, {deleted_rows} removed.'

    api_result = {'api_status': 'success', 'api_message': msg, 'rows_expired': expired_rows, 'rows_removed': deleted_rows}
    if thisApp.application_configuration.database_api_debug or debug: print_api_result(f"{msgPrefix} result:", api_result)
    return api_result
#::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::

#::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
# sample_token_request = {
#         'device_uid': 'adasdade1323423424234234242',
#         'geolocation_lat': '12.34',
#         'geolocation_lon': "1222.32224",
#         'token_type':"bearer",
#         'token_scope':"application_service",
#         'grant_type':"client_credentials",
#         'token':"DkdK_ixIcTlCc5d8EE17FFegrJInZnR9JhDdClrM03wWthx2__uRypo2Sr-VlPC20CDQQY8RPiPrSy-2fqwYYPG0Jq1JK8-6h4D2prx2W6xeWh6qBIvQfPZG0P6igW82Bdvk-cpPatNNEsxyEVL4Q3bHMGsLvrwNN8DYn3nj5Lg",
#         'subscription_id': "",
#         'application_name': 'scanandpay_merchant',
#         'client_id': 'e9036f56-8d46-5318-9fca-488f467bc7e1',
#         'client_secretKey': 'mzbSD4FmRBtBQQpu-HWXITfWOvfrLwK2sHaE0q92uLepJtSrylBRfZ-wqS9NPKEJhrgiZtfpY3akjRF6ZcRrnnKJIlxFpJJ2x5XQs4XY9j59FSaoUJ_KQouNrFk3H7MQCZ97SHqz8J7wZCKwvFi2fqv0RzvAKrdtNy5JYbRrGqY',
#         }
#::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
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
#master_configuration = retrieve_module_configuration(module_identityDictionary, master_configuration, print_enabled=thisApp.CONSOLE_ON, filelog_enabled=thisApp.FILELOG_ON, handle_as_init=True)
#::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
#::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
#::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
msg = f'database [ganimides] [[[[module [{module_id}] loaded]]]] with [[version {module_version}]]'
if thisApp.CONSOLE_ON:
    log_message(msg)
else:
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