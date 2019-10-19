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
        action='REFRESH'
        action_result = dbsession.table_action(dbmodel.CLIENT, action, input_dict, action_filter, auto_commit=True, caller_area=_process_call_area)
        api_result = action_result
        thismsg=action_result.get('api_message')
        api_result.update({'api_action': _api_action, 'api_name': _api_name})
        if not api_result.get('api_status') == 'success':
            # msg = f"subscription not registered"
            # api_result.update({'api_message':msg})
            log_process_finish(_api_msgID, api_result, **_process_call_area)    
            return api_result
        client = api_result.get('api_data')
        client_id = client.get('client_id')
        input_dict.update({'client_id': client_id})
    elif action.upper() in ('CONFIRM', 'ACTIVATE', 'DEACTIVATE', 'DELETE'):
        subscription_dict = dbsession.get(dbmodel.SUBSCRIPTION, input_dict, 'DICT', caller_area=_process_call_area)
        if not subscription_dict:
            msg = f'subscription not found'
            action_status='error'
            api_result = {'api_status': action_status, 'api_message': msg, 'api_data': input_dict, 'api_action': _api_action.upper(), 'api_name': _api_name}
            log_process_finish(_api_msgID, api_result, **_process_call_area)    
            return api_result
        client_dict=dbsession.get(dbmodel.CLIENT, subscription_dict,'DICT', caller_area=_process_call_area)
        if not client_dict:
            msg = f'client not found'
            action_status='error'
            api_result = {'api_status': action_status, 'api_message': msg, 'api_data': subscription_dict, 'api_action': _api_action.upper(), 'api_name': _api_name}
            log_process_finish(_api_msgID, api_result, **_process_call_area)    
            return api_result

        #action='CONFIRM'
        action_result = dbsession.table_action(dbmodel.CLIENT, action, input_dict,  action_filter, auto_commit=True, caller_area=_process_call_area)
        api_result = action_result
        api_result.update({'api_action': _api_action, 'api_name': _api_name})
        thismsg=action_result.get('api_message')
        if not api_result.get('api_status') == 'success':
            # msg = f'client confirmation failed'
            # api_result.update({'api_message':msg})
            log_process_finish(_api_msgID, api_result, **_process_call_area)    
            return api_result
        subscription_dict = dbsession.get(dbmodel.SUBSCRIPTION, subscription_dict, 'DICT', caller_area=_process_call_area)
        status=subscription_dict.get('status')
        client_id=subscription_dict.get('client_id')
        # if not subscription_dict.get('status') == 'Active':
        #     msg = f"service provider not confirmed. status={status}"
        #     action_status='error'
        #     api_result = {'api_status': action_status, 'api_message': msg, 'api_data': subscription_dict, 'messages': messages, 'rows_added': rows_added, 'rows_updated': rows_updated, 'api_action': _api_action.upper(), 'api_name': _api_name}
        #     log_process_finish(_api_msgID, api_result, **_process_call_area)    
        #     return api_result
        input_dict.update({'status': status})
        input_dict.update({'client_id': client_id})
    
    action_result = dbsession.table_action(dbmodel.SUBSCRIPTION, action, input_dict,  action_filter, auto_commit=True, caller_area=_process_call_area)
    api_result = action_result
    thismsg=thismsg.replace('CLIENT',_api_entity)
    api_result.update({'api_action': _api_action, 'api_name': _api_name,'api_message':thismsg})
    
    log_process_finish(_api_msgID, api_result, **_process_call_area)    
    return api_result
