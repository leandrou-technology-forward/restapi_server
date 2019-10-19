import os
import sys
if not (os.path.dirname(__file__) in sys.path): sys.path.append(os.path.dirname(__file__))
import json
import time
import datetime
import configparser
from copy import deepcopy
from _appEnvironment import DEFAULT, CONSOLE_ON, FILELOG_ON, EXECUTION_MODE, Fore
from _appEnvironment import collect_function_names_from_module,collect_method_names_from_class
from _utilities import find_file, file_delete
from _logServices import log_message,log_module_initialization_message
#::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
#::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
#::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
#module
#::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
#::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
#::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
module_Function = 'module configuration services'
module_ProgramName = '_moduleConfigServices'
module_BaseTimeStamp = datetime.datetime.now()
module_folder = os.getcwd()
module_color = Fore.WHITE
module_folder = os.path.dirname(__file__)
module_ProgramName = os.path.splitext(os.path.basename(__file__))[0]
module_id = f'{module_ProgramName}'
module_eyecatch = module_ProgramName
module_version = 0.1
module_log_file_name = module_ProgramName+'.log'
module_errors_file_name = os.path.splitext(os.path.basename(module_log_file_name))[0]+'_errors.log'
module_versionString = f'[{module_id}] version {module_version}'
module_file = __file__
module_is_externally_configurable=False
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
    'module_errors_file_name':module_errors_file_name,
    'module_is_externally_configurable':module_is_externally_configurable,
}
master_configuration = {
}
# log options
log_print_enabled=CONSOLE_ON
log_filelog_enabled=FILELOG_ON
log_file_name = module_log_file_name
log_errors_file_name = module_errors_file_name
#::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
#::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
#::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
# services
#::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
#::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
#::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
def retrieve_module_configuration(module_identityDictionary, module_configuration={}, print_enabled=DEFAULT, filelog_enabled=DEFAULT, handle_as_init=True):
    log_message('', msgType='START')
    module_file = module_identityDictionary.get('module_file', '')
    module_log_file_name = module_identityDictionary.get('module_log_file_name', '')
    module_errors_file_name = module_identityDictionary.get('module_errors_file_name', '')
    module_id = module_identityDictionary.get('module_id', '')
    module_version = module_identityDictionary.get('module_version', '')
    module_color = module_identityDictionary.get('module_color', '')
    module_is_externally_configurable=module_identityDictionary.get('module_is_externally_configurable',True)
    if module_identityDictionary.get('consolelog_enabled', None) == None:
        module_consolelog_enabled = print_enabled
    else:
        module_consolelog_enabled = module_identityDictionary.get('consolelog_enabled')

    if module_identityDictionary.get('filelog_enabled', None) == None:
        module_filelog_enabled = filelog_enabled
    else:
        module_filelog_enabled = module_identityDictionary.get('filelog_enabled')
    module_identityDictionary.update({'consolelog_enabled':module_consolelog_enabled})
    module_identityDictionary.update({'print_enabled':module_consolelog_enabled})
    module_identityDictionary.update({'filelog_enabled':module_filelog_enabled})
    
    file_delete(module_log_file_name,print_enabled=print_enabled,filelog_enabled=filelog_enabled, ignoreWarning=True)
    file_delete(module_errors_file_name,print_enabled=print_enabled,filelog_enabled=filelog_enabled, ignoreWarning=True)

    if not module_is_externally_configurable:
        msg=f'[{module_id}] is not externally configurable. in-module master_configuration will be used and stored.'
        log_message(msg, msgType='', print_enabled=print_enabled, filelog_enabled=filelog_enabled, msgCategory='DEBUG')

    new_module_configuration = retrieve_module_configuration_from_file(module_file, module_configuration, module_identityDictionary, print_enabled=print_enabled, filelog_enabled=filelog_enabled,external_config_enabled=module_is_externally_configurable)
    if not new_module_configuration.get('initialized', None):
        msg=f'[{module_id}] FAILED TO INITIALIZED'
        log_message(msg, msgType='error', print_enabled=print_enabled, filelog_enabled=filelog_enabled)

    #logging options
    new_module_configuration.update({'consolelog_enabled':module_consolelog_enabled})
    new_module_configuration.update({'print_enabled':module_consolelog_enabled})
    new_module_configuration.update({'filelog_enabled':module_filelog_enabled})

    log_message('', msgType='FINISH')
    msg = f'module [{module_id}] [[version {module_version}]] loaded.'
    if handle_as_init:
        log_message('', msgType='FINISH', msgColor=module_color, print_enabled=print_enabled, filelog_enabled=filelog_enabled)
        log_module_initialization_message(module_identityDictionary)
        #log_message(msg, msgType='FINISH', msgColor=module_color, print_enabled=print_enabled, filelog_enabled=filelog_enabled)
    else:
        msg = f'config for module [[{module_id}]] loaded.'
        log_message(msg, msgType='info', msgOffset='', msgColor='', print_enabled=print_enabled, filelog_enabled=filelog_enabled)

    return new_module_configuration
###############################################################################################################
def retrieve_module_configuration_from_file(this_file, this_configuration={}, module_identityDictionary={}, print_enabled=None, filelog_enabled=None,external_config_enabled=True):
    global EXECUTION_MODE
    module_color = module_identityDictionary.get('module_color', '')
    module_id=module_identityDictionary.get('module_id','')
    if not this_file:
        this_file = __file__
        errorMsg = f'{module_ProgramName}:retrieve_module_configuration_from_file(): module file not provided'
        log_message(errorMsg, msgType='SYSTEM ERROR', msgOffset='', msgColor=module_color)
        raise Exception(errorMsg)

    moduleProgramName = os.path.splitext(os.path.basename(this_file))[0]

    if EXECUTION_MODE.upper().find('PROD') >= 0:
        configFile = f'{moduleProgramName}.cfg'
    else:
        if not external_config_enabled:
            configFile = f'configuration_usedfor_{moduleProgramName}_{EXECUTION_MODE.lower()}.cfg'    
        else:
            configFile = f'configuration_{moduleProgramName}_{EXECUTION_MODE.lower()}.cfg'    

    config_folder = os.path.dirname(this_file)
    if not external_config_enabled:
        if this_configuration:
            configString = json.dumps(this_configuration, sort_keys=True, indent=4)
            with open(configFile, 'w') as cfgFile:
                cfgFile.write(configString)
            msg = f'[{module_id}] a config copy saved in [{configFile}]'
            #log_message(msg, msgType='WARNING', msgOffset='', msgColor=module_color)
        else:
            if os.path.isfile(configFile):
                file_delete(cfgFile, print_enabled=print_enabled, filelog_enabled=filelog_enabled, ignoreWarning=True)

        initTimeStamp = str(datetime.datetime.now())
        this_configuration.update({'initialized':initTimeStamp})
        return this_configuration
    else:
        if not os.path.isfile(configFile) or not external_config_enabled:
            #configString = json.dumps(this_configuration)
            configString = json.dumps(this_configuration, sort_keys=True, indent=4)
            with open(configFile, 'w') as cfgFile:
                cfgFile.write(configString)
            msg = f'{module_id} [config file [[{configFile}]] created]'
            log_message(msg, print_enabled=print_enabled, filelog_enabled=filelog_enabled)
        else:
            try:
                with open(configFile, 'r') as cfgFile:
                    configString = cfgFile.read()
                    msg=f'{module_id} [config file] [[{configFile}]] [retrieved]'
                    log_message(msg, msgCategory='DEBUG',print_enabled=print_enabled, filelog_enabled=filelog_enabled)
            except:
                configString = None
                errorMsg = f'[{module_id}]: config file [[{configFile}]] not found'
                log_message(errorMsg, msgType='ERROR', msgOffset='',msgColor=module_color,print_enabled=print_enabled, filelog_enabled=filelog_enabled)
                raise Exception(errorMsg)
            if configString:
                this_configuration = json.loads(configString)


    msg=f'{module_id} [config folder is [[{config_folder}]] ]'
    log_message(msg, msgCategory='DEBUG', msgType='info', print_enabled=print_enabled, filelog_enabled=filelog_enabled)
        
    configFilePath = find_file(configFile, search_Downwards=1, search_Upwards=0, search_SubFolders=False)
    msg=f'{module_id} [config file path is [[{configFilePath}]] ]'
    log_message(msg, msgCategory='DEBUG', msgType='info', print_enabled=print_enabled, filelog_enabled=filelog_enabled)

    if not configFilePath:
        errorMsg = f'[{module_id}]: config file [{configFile}] not found in config folder [ {config_folder} ]'
        log_message(errorMsg, msgType='SYSTEM ERROR', msgOffset='',msgColor=module_color)
        raise Exception(errorMsg)

    relativePath = configFilePath.lower().replace(config_folder.lower(),'').replace(configFile.lower(),'')
    msg=f'{module_id} [relative configuration path is [[{relativePath}]] ]'
    log_message(msg, msgCategory='DEBUG', msgType='info', print_enabled=print_enabled, filelog_enabled=filelog_enabled)

    this_configuration.update({'configFile': configFile})
    this_configuration.update({'configFilePath': configFilePath})

    msg = f'{module_id} [configuration imported from [[{configFile}]] ]'
    if external_config_enabled:
        log_message(msg, msgCategory='DEBUG', msgType='info', print_enabled=print_enabled, filelog_enabled=filelog_enabled)

    initTimeStamp = str(datetime.datetime.now())
    this_configuration.update({'initialized':initTimeStamp})

    return this_configuration
################################################################
def read_client_configuration_dictionary_from_file(configFile, module_identityDictionary = {}, print_enabled = None, filelog_enabled = None):
    module_color = module_identityDictionary.get('module_color', '')
    module_id=module_identityDictionary.get('module_id','')
    if not os.path.isfile(configFile):
        msg = f'client config file [[{configFile}]] not found...'
        log_message(msg, msgType='WARNING', msgOffset='+1',msgColor=module_color)
        return {}
    else:
        try:
            with open(configFile, 'r') as cfgFile:
                configString=cfgFile.read()
            msg=(f'{module_id} [client config file] [[{configFile}]] [retrieved]')
            log_message(msg, msgCategory='DEBUG', msgType='info', print_enabled=print_enabled, filelog_enabled=filelog_enabled)
            configDict=json.loads(configString)
            return configDict
        except:
            configString = None
            msg = f'[{module_id}]: client config file [[{configFile}]] can not be read'
            log_message(msg, msgType='SYSTEM ERROR', msgOffset='+1',msgColor=module_color)
            return {}
            #raise Exception(errorMsg)
###############################################################################################################
def module_version_string(module_id='', module_version=1.1, module_BaseTimeStamp='', config_version=None, config_versrionString=''):
    msg1 = ''
    msg2 = ''
    msg3 = ''
    if module_id:
        msg1 = '{} version {}'.format(module_id, module_version)
    if config_version:
        msg2 = 'config version {}'.format(config_version)
        if config_versrionString:
            msg2 = 'config version {} ({})'.format(config_version, config_versrionString)
    else:
        if config_versrionString:
            msg2 = 'config version 0 ({})'.format(config_versrionString)
    if module_BaseTimeStamp:
        msg3 = 'baseTimeStamp:{}'.format(module_BaseTimeStamp)
    versionStr = '{} {} {}'.format(msg1, msg2, msg3).strip()
    return versionStr
###############################################################################################################
def config_version_string(config_version=None, config_versrionString='', module_BaseTimeStamp=''):
    msg1 = ''
    msg2 = ''
    msg3 = ''
    if config_version:
        msg2 = 'config version {}'.format(config_version)
        if config_versrionString:
            msg2 = 'config version {} ({})'.format(config_version, config_versrionString)
    else:
        if config_versrionString:
            msg2 = 'config version 0 ({})'.format(config_versrionString)
    if module_BaseTimeStamp:
        msg3 = 'baseTimeStamp:{}'.format(module_BaseTimeStamp)
    versionStr = '{} {} {}'.format(msg1, msg2, msg3).strip()
    return versionStr
#############################################################################
def application_paired_configuration(application_configuration,module_configuration,module_identityDictionary):
    client_configuration={}
    client_configuration_paired = None
    changed=False
    if application_configuration:
        for key in application_configuration:
            valnew = application_configuration.get('key','')
            valold = client_configuration.get('key', '')
            if valnew != valold:
                changed=True        
            client_configuration.update({key: application_configuration.get(key)})

    module_ProgramName = module_identityDictionary.get('module_ProgramName')
    module_color = module_identityDictionary.get('module_color')

    # print(module_ProgramName,'1',application_configuration.get('application_ProgramName', ''))
    # print(module_ProgramName,'2',application_configuration.get('configModuleProgramName', ''))
    # print(module_ProgramName,'3',client_configuration.get('application_ProgramName', ''))
    # print(module_ProgramName,'4',client_configuration.get('configModuleProgramName', ''))

    client_applicationID = None
    client_application_title = None
    client_application_name = None
    paired_module_name = client_configuration.get('application_ProgramName', '')
    # if not paired_module_name:
    #     paired_module_name = client_configuration.get('configModuleProgramName', '')
    if client_configuration.get('application_name'):
        client_application_name = client_configuration.get('application_name')
    if client_configuration.get('application_title'):
        client_application_title = client_configuration.get('application_title')
    if client_configuration.get('application_id'):
        client_applicationID = client_configuration.get('application_id')
    
    if client_applicationID and client_application_title and client_application_name and paired_module_name:
        client_configuration_paired = True
        msg = f'application config paired: [{paired_module_name}] --> [{module_ProgramName}]'
        log_message(msg,msgType='info-1',msgOffset='+1',msgColor=module_color)
    else:
        msg = f'failed to pair application config:[{paired_module_name}] --> [{module_ProgramName}]'
        #log_message(msg,msgType='error',msgOffset='+1')

    for key in module_configuration:
        if key not in ('application_name','application_title','application_id','application_ProgramName'):
            valnew = module_configuration.get('key','')
            valold = client_configuration.get('key', '')
            if valnew != valold:
                changed=True        
            client_configuration.update({key: module_configuration.get(key)})

    client_configuration.update({'client_configuration_paired': client_configuration_paired})
    client_configuration.update({'client_configuration_changed': changed})

    return client_configuration
#############################################################################
def save_module_configuration(module_identityDictionary, module_configuration={}, print_enabled=DEFAULT, filelog_enabled=DEFAULT):
    global EXECUTION_MODE
    module_file = module_identityDictionary.get('module_file', '')
    module_id = module_identityDictionary.get('module_id', '')
    if not module_file:
        errorMsg = f'{module_id}:retrieve_module_configuration_from_file(): module file not provided'
        log_message(errorMsg, msgType='SYSTEM ERROR', msgOffset='', msgColor=module_color)
        return
    if not module_configuration:
        msg = f'empty configuration can not be saved'
        log_message(msg, msgType='', msgOffset='', msgColor=module_color,print_enabled=print_enabled, filelog_enabled=filelog_enabled)
        return

    moduleProgramName = os.path.splitext(os.path.basename(module_file))[0]
    if EXECUTION_MODE.upper().find('PROD') >= 0:
        configFile = f'{moduleProgramName}.cfg'
    else:
        configFile = f'configuration_{moduleProgramName}_{EXECUTION_MODE.lower()}.cfg'    

    # config_folder = os.path.dirname(module_file)

    configString = json.dumps(module_configuration, sort_keys=True, indent=4)
    with open(configFile, 'w') as cfgFile:
        cfgFile.write(configString)
    msg = f'module [{module_id}] configuration saved in [{configFile}]'
    log_message(msg, msgType='info',print_enabled=print_enabled, filelog_enabled=filelog_enabled)
#::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
def get_globals_from_configuration(master_configuration):
    print_enabled = None
    filelog_enabled = None
    consolelog_enabled = None
    log_file = ''
    errors_file=''
    if not master_configuration.get('filelog_enabled') == None:
        filelog_enabled = master_configuration.get('filelog_enabled')
    if not master_configuration.get('print_enabled') == None:
        print_enabled = master_configuration.get('print_enabled')
    if not master_configuration.get('consolelog_enabled') == None:
        print_enabled = master_configuration.get('consolelog_enabled')
    if not master_configuration.get('console_on') == None:
        print_enabled = master_configuration.get('console_on')
    consolelog_enabled = print_enabled
    if master_configuration.get('log_file'):
        if master_configuration.get('log_file').upper()=='MODULE':
            log_file = module_log_file_name
        else:
            log_file = master_configuration.get('log_file')
    if master_configuration.get('errors_file'):
        if master_configuration.get('errors_file').upper() == 'MODULE':
            errors_file = module_errors_file_name
        else:
            errors_file = master_configuration.get('errors_file')
    return (print_enabled, filelog_enabled, log_file, errors_file, consolelog_enabled)
#::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
#::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
def add_apis_to_configuration(config_key,configuration, thisModuleObj, functions_ids=[], exclude_functions_ids=[]):
    # functions_ids=['dbapi_']
    # exclude_functions_ids = ['set_api_msgID', 'set_api_debug_level']
    # thisModuleObj = sys.modules[__name__]
    dbapis = collect_function_names_from_module(thisModuleObj, functions_ids, exclude_functions_ids)
    dbapis.sort()
    if not config_key:
        config_key='apis'
    if not configuration.get(config_key):
        configuration.update({config_key: {}})
    for ix in range(0, len(dbapis)):
        api_name=dbapis[ix]
        if not configuration.get(config_key,{}).get(api_name):
            api_entry = {dbapis[ix]: {'status': 'Active', 'version':'1.1','debug_level': -1}}
            configuration[config_key].update(api_entry)
    
    config_key='apis'
    if not configuration.get(config_key):
        configuration.update({config_key: {}})
    for ix in range(0, len(dbapis)):
        api_name=dbapis[ix]
        if not configuration.get(config_key,{}).get(api_name):
            api_entry = {dbapis[ix]: {'status': 'Active', 'version':'1.1','debug_level': -1}}
            configuration[config_key].update(api_entry)

    return configuration
#::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
def add_methods_to_configuration(config_key,configuration, classObj, functions_ids=[], exclude_functions_ids=[]):
    methods = collect_method_names_from_class(classObj, functions_ids, exclude_functions_ids)
    methods.sort()
    if not config_key:
        config_key='methods'
    if not configuration.get(config_key):
        configuration.update({config_key: {}})
    for ix in range(0, len(methods)):
        method_name=methods[ix]
        if not configuration.get(config_key,{}).get(method_name):
            api_entry = {methods[ix]: {'status': 'Active', 'version':'1.1','debug_level': -1}}
            configuration[config_key].update(api_entry)
    
    config_key='actions'
    if not configuration.get(config_key):
        configuration.update({config_key: {}})
    for ix in range(0, len(methods)):
        method_name=methods[ix]
        if not configuration.get(config_key,{}).get(method_name):
            api_entry = {methods[ix]: {'status': 'Active', 'version':'1.1','debug_level': -1}}
            configuration[config_key].update(api_entry)

    return configuration
#::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
#::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
#::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
# utilities
#::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
#::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
#::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
def dict_of_dicts_merge(x, y):
    z = {}
    overlapping_keys = x.keys() & y.keys()
    for key in overlapping_keys:
        z[key] = dict_of_dicts_merge(x[key], y[key])
    for key in x.keys() - overlapping_keys:
        z[key] = deepcopy(x[key])
    for key in y.keys() - overlapping_keys:
        z[key] = deepcopy(y[key])
    return z
#::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
#::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
#::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
# module inititialization
#::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
#::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
#::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
master_configuration = retrieve_module_configuration(module_identityDictionary, master_configuration, print_enabled=CONSOLE_ON, filelog_enabled=FILELOG_ON)
#::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
#::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
#::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
# main (for testing)
#::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
#::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
#::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
#::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
if __name__ == '__main__':
    print(__file__)