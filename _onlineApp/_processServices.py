import os
import sys
import datetime
module_ProgramName = os.path.splitext(os.path.basename(__file__))[0]
module_id = '{}'.format(module_ProgramName)
module_version = 0.1
from _appEnvironment import FILELOG_ON,CONSOLE_ON,log_file_name,log_errors_file_name,collect_function_names_from_module
from _debugServices import master_configuration as debug_templates
from _colorServices import colorized_string
#::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
#::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
#::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
#globals
#::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
#::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
#::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
#::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
#::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
#::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
# print services
#::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
#::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
#::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
def set_xprocess_identity_dict(proc_prefix, proc_name, proc_action, proc_entity, proc_msgID, proc_level, proc_dbsession, proc_table_model,proc_table_name,debug_level, print_enabled, filelog_enabled, log_file, errors_file, debug_files, indent_level, indent_method,caller_area):
    _api_debug_level = get_debug_level(debug_level,dbsession=proc_dbsession, table_model=proc_table_model, table_action=proc_action, api_name=proc_name, table_name=proc_table_name, caller_area={})
    _api_debug_files = get_debug_files(_api_debug_level,dbsession=proc_dbsession, table_model=proc_table_model, table_action=proc_action, api_name=proc_name, table_name=proc_table_name, caller_area={})
    process_identification_dict = {
        'process_prefix':proc_prefix,
        'process_name':proc_name,
        'process_action':proc_action,
        'process_entity':proc_entity,
        'process_msgID':proc_msgID,
        'process_level':proc_level,
        'process_session_id':proc_dbsession.session_id,
        'debug_level': _api_debug_level,
        'print_enabled':print_enabled,
        'filelog_enabled':filelog_enabled,
        'log_file':log_file,
        'errors_file':errors_file,
        'debug_files':_api_debug_files,
        'indent_level':indent_level,
        'indent_method':indent_method,
        }
    return process_identification_dict
#::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
def build_process_signature(**kwargs):
    signature = {
    'level': kwargs.get('level',0),
    'name': kwargs.get('name',''),
    'debug_level': kwargs.get('debug_level', -1),
    }
    if kwargs.get('module_file'):
        signature.update({'module_file': kwargs.get('module_file')})
    else:
        if kwargs.get('__file__'):
            signature.update({'module_file': kwargs.get('__file__')})
    if kwargs.get('debug_files'):
        signature.update({'debug_files': kwargs.get('debug_files')})
    if kwargs.get('type'):
        signature.update({'type': kwargs.get('type')})
    if kwargs.get('module'):
        signature.update({'module': kwargs.get('module')})
    if kwargs.get('action'):
        signature.update({'action': kwargs.get('action')})
    if kwargs.get('entity'):
        signature.update({'entity': kwargs.get('entity')})
    if kwargs.get('msgID'):
        signature.update({'msgID': kwargs.get('msgID')})
    if kwargs.get('indent_level'):
        signature.update({'indent_level': kwargs.get('indent_level')})
    if kwargs.get('indent_method'):
        signature.update({'indent_method': kwargs.get('indent_method')})
    if kwargs.get('dbsession'):
        try:
            session_id = dbsession.session_id
        except:
            session_id = None
        if session_id:
            signature.update({'dbsession': session_id})

    return signature
#::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
def build_process_call_area(this_signature, this_caller_area):
    if type(this_caller_area)==type({}):
        caller_area = this_caller_area.copy()
    else:
        caller_area={}
    if not caller_area.get('call_stack'):
        caller_area.update({'call_stack': []})

    if type(this_signature)==type({}):
        signature = this_signature.copy()
    else:
        signature = {}
    this_indent_level = signature.get('indent_level')

    #remove empty values
    for k in this_signature.keys():
        if this_signature.get(k) == None:
            try:
                del signature[k]
            except KeyError:
                pass

    call_level = caller_area.get('call_level', -1)
    call_stack = caller_area.get('call_stack')
    old_debug_files= caller_area.get('debug_files',[])
    this_debug_files = this_signature.get('debug_files', [])
    new_debug_files = old_debug_files
    for ix in range(0, len(this_debug_files)):
        f = this_debug_files[ix]
        if f and f not in new_debug_files:
            new_debug_files.append(f)
    call_stack.append(this_signature)
    if this_indent_level == None:
        this_indent_level = call_level + 1
        signature.update({'indent_level': this_indent_level})

    debug_template = caller_area.get('debug_template')
    if debug_template:
        template_key='debug_template_'+debug_template
        debug_template_dict = debug_templates.get(template_key, {})
        if debug_template_dict:
            for k in debug_template_dict.keys():
                caller_area.update({k:debug_template_dict.get(k)})
    #new=old
    new_caller_area = caller_area
    #overwrite with new signature
    new_caller_area.update(signature)
    #new values
    new_caller_area.update({'call_level': call_level + 1})
    new_caller_area.update({'call_stack': call_stack})
    new_caller_area.update({'debug_files': new_debug_files})

    return new_caller_area
#::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
def set_process_identity_dict(proc_prefix, proc_name, proc_action, proc_entity, proc_msgID, proc_level, proc_session_id, debug_level, print_enabled, filelog_enabled, log_file, errors_file, debug_files, indent_level, indent_method):
        # #_api_debug_level = get_table_debug_level(table_model, debug_level)
        # _api_debug_level = get_debug_level(debug_level,dbsession=self, table_model=table_model, table_action=_api_action, api_name=_api_name, table_name=_api_tablename, caller_area={})
        # _api_debug_files = get_debug_files(_api_debug_level,dbsession=self, table_model=table_model, table_action=_api_action, api_name=_api_name, table_name=_api_tablename, caller_area={})

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
        'debug_files':debug_files,
        'indent_level':indent_level,
        'indent_method':indent_method,
        }
    return process_identification_dict
#::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
def set_process_caller_area(this_process_identity_dict, _process_call_area):
    if type(_process_call_area)==type({}):
        caller_area = _process_call_area.copy()
    else:
        caller_area={}
    
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
        print_enabled = CONSOLE_ON
    caller_area.update({'print_enabled':print_enabled})

    filelog_enabled = this_process_identity_dict.get('filelog_enabled')
    if filelog_enabled == None:
        filelog_enabled = caller_area.get('filelog_enabled')
    if filelog_enabled == None:
        filelog_enabled = FILELOG_ON
    caller_area.update({'filelog_enabled':filelog_enabled})

    log_file = this_process_identity_dict.get('log_file', '')
    if not log_file:
        log_file = caller_area.get('log_file','')
    if not log_file:
        log_file = log_file_name
    caller_area.update({'log_file':log_file})

    caller_area.update({'module_id':module_id})
    caller_area.update({'module_file':__file__})

    return caller_area
#::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
def add_apis_to_configuration(configuration, thisModuleObj, functions_ids=[], exclude_functions_ids=[]):
    # functions_ids=['dbapi_']
    # exclude_functions_ids = ['set_api_msgID', 'set_api_debug_level']
    # thisModuleObj = sys.modules[__name__]
    dbapis = collect_function_names_from_module(thisModuleObj, functions_ids, exclude_functions_ids)
    dbapis.sort()
    if not configuration.get('apis'):
        configuration.update({'apis': {}})
    for ix in range(0, len(dbapis)):
        api_name=dbapis[ix]
        if not configuration.get('apis',{}).get(api_name):
            api_entry = {dbapis[ix]: {'status': 'Active', 'version':'1.1','debug_level': -1}}
            configuration['apis'].update(api_entry)
    return configuration
#::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
#::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
msg = f'module [{module_id}] [[version {module_version}]] loaded.'
if CONSOLE_ON:
    print(colorized_string(msg))
#::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
#::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
#::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
# main
#::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
#::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
#::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
if __name__ == '__main__':
    print(__file__)
