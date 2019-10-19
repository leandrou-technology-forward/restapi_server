# -*- coding: utf-8 -*-
import os
import sys
if not (os.path.dirname(__file__) in sys.path): sys.path.append(os.path.dirname(__file__))

import pyzbar.pyzbar as pyzbar
import numpy as np
import cv2
import pyqrcode
import inspect
#pypng must be installed
from PIL import Image
import datetime
import configparser
import time
import json
#from __future__ import print_function
import subprocess

from _appEnvironment import application_configuration,Fore,CONSOLE_ON
from _printServices import print_message
#::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
#::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
#::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
#module
#::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
#::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
#::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
module_Function = 'debug services'
module_ProgramName = '_debugServices'
module_BaseTimeStamp = datetime.datetime.now()
module_folder = os.getcwd()
module_color = Fore.YELLOW
module_folder = os.path.dirname(__file__)
module_ProgramName = os.path.splitext(os.path.basename(__file__))[0]
module_id = f'{module_ProgramName}'
module_eyecatch = module_ProgramName
module_version = 0.1
module_log_file_name = module_ProgramName+'.log'
module_errors_file_name = os.path.splitext(os.path.basename(module_log_file_name))[0]+'_errors.log'
module_versionString = f'{module_id} version {module_version}'
module_file = __file__
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
}
master_configuration = {
    'debug_template_DEBUG_OFF': {
        'debug_level':0,
        'start_debug':False,
        'input_debug':False,
        'data_debug':False,
        'output_debug':False,
        'message_debug':False,
        'result_debug':False,
        'result_message_debug':False,
        'finish_debug':False,
        'caller_area_input_debug':False,
        'session_result_message_debug':False,
    },        
    'debug_template_SESSION_ONLY': {
        'debug_level':99,
        'start_debug':False,
        'input_debug':False,
        'data_debug':False,
        'output_debug':False,
        'message_debug':False,
        'result_debug':False,
        'result_message_debug':False,
        'finish_debug':False,
        'caller_area_input_debug':False,
        'session_result_message_debug':True,
    },        
    'debug_template_API_RESULT': {
        'debug_level':99,
        'start_debug':False,
        'input_debug':False,
        'data_debug':False,
        'output_debug':False,
        'message_debug':False,
        'result_debug':False,
        'result_message_debug':False,
        'finish_debug':True,
        'caller_area_input_debug':False,
        'session_result_message_debug':False,
    },        
    # 'debug_template_API_RESULT': {
    #     'debug_level':99,
    #     'start_debug':False,
    #     'input_debug':False,
    #     'data_debug':False,
    #     'output_debug':False,
    #     'message_debug':False,
    #     'result_debug':False,
    #     'result_message_debug':False,
    #     'finish_debug':True,
    #     'caller_area_input_debug':False,
    #     'session_result_message_debug':False,
    # },        
    'debug_template_RESULT': {
        'debug_level':99,
        'start_debug':False,
        'input_debug':False,
        'data_debug':False,
        'output_debug':False,
        'message_debug':False,
        'result_debug':False,
        'result_message_debug':True,
        'finish_debug':True,
        'caller_area_input_debug':False,
        'session_result_message_debug':False,
    },        
    'debug_template_STANDARD': {
        'start_debug':True,
        'input_debug':True,
        'data_debug':True,
        'output_debug':True,
        'message_debug':True,
        'result_debug':True,
        'result_message_debug':True,
        'finish_debug':True,
        'caller_area_input_debug':False,
    },        
    'debug_template_FULL': {
        'debug_level':99,
    },        
}
#::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
#::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
#::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
global_debug_level = -1
global_debug_levels = {}
debug_tempates = {
    'debug_template_alpha': {
        'debug_level':99,
        'start_debug':False,
        'input_debug':False,
        'data_debug':False,
        'output_debug':False,
        'result_debug':False,
        'result_message_debug':False,
        'finish_debug':False,
        'caller_area_input_debug':False,
        'session_result_message_debug':False,
    },        
}
#::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
# services
#::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
#::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
#::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
##############################################################
#---------------------------------------------------------------------
# function_level      : 1 2 3 4 5  
# function_debug_level: 9 8 7 6 5    (10-function_level)
#                       x x x x x 9
#                       o x x x x 8
#                       o o x x x 7
#                       o o o x x 6
#                       o o o o x 5
#                       o o o o o 4
#                                 ^--debug_level
#---------------------------------------------------------------------
# def set_function_debug_level(function_level, debug_level, process_name, module_configuration):
#     #function_level=0..10
#     debug_config = module_configuration.get('debug_dictionary', {})
#     if not debug_config:
#         debug_config = module_configuration
    
#     function_level_debug_is_on = debug_application_configuration.get('function_levels', {}).get(function_level, True)
#     if not function_level_debug_is_on:
#         function_debug_level = debug_level + 999 # make it always greater than debug_level
#     else:
#         if not process_name:
#             function_debug_level = 10 - function_level
#         else:
#             if debug_application_configuration.get('function_levels', {}).get(process_name, -1) >= 0:
#                 function_debug_level = debug_application_configuration.get('function_levels', {}).get(process_name, 0)
#             else:
#                 function_debug_level = 10 - function_level
#     return function_debug_level
#::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
def set_debug_level(debug_level=0, process_name=''):
    global global_debug_level
    global global_debug_levels
    if not process_name:
        global_debug_level = debug_level
        process_name = whosdaddy()
        global_debug_levels.update({process_name:debug_level})
    elif process_name.upper() in ['ALL', '*']:
        for k in global_debug_levels:
            global_debug_levels.update({k:debug_level})
    else:
        global_debug_levels.update({process_name.upper():debug_level})
#::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
def set_debug_ON(process_name=''):
    global global_debug_level
    global global_debug_levels
    debug_level = 999
    if not process_name:
        global_debug_level = debug_level
        process_name = whosdaddy()
        global_debug_levels.update({process_name:debug_level})
    elif process_name.upper() in ['ALL', '*']:
        for k in global_debug_levels:
            global_debug_levels.update({k:debug_level})
    else:
        global_debug_levels.update({process_name.upper():debug_level})
#::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
def set_debug_OFF(process_name=''):
    global global_debug_level
    global global_debug_levels
    debug_level = -1
    if not process_name:
        global_debug_level = debug_level
        process_name = whosdaddy()
        global_debug_levels.update({process_name:debug_level})
    elif process_name.upper() in ['ALL', '*']:
        for k in global_debug_levels:
            global_debug_levels.update({k:debug_level})
    else:
        global_debug_levels.update({process_name.upper():debug_level})
#############################################################################
def whoami():
    return inspect.stack()[1][3]
#############################################################################
def whosdaddy():
    return inspect.stack()[2][3]
#############################################################################
def whosdaddy2():
    return inspect.stack()[3][3]
#############################################################################
def call_chain():
    xcaller = sys._getframe(1)  # Obtain calling frame
    xactive_moduleX = xcaller.f_globals['__name__']
    xcaller = sys._getframe(2)  # Obtain calling frame
    #xactive_moduleX2 = xcaller.f_globals['__name__']
    # xcaller_prog1 = whosdaddy()
    # xcaller_prog2 = whosdaddy2()
    # xcaller_prog = f'{xcaller_prog2}{xcaller_prog1}'
    i=-1
    p = ''
    #xx[0].f_locals.self.name
    for i in range(1,len(inspect.stack())):
        xx = inspect.stack()[i]
        name = inspect.stack()[i][3]
        function = xx.function
        print('-----',i,function,name)

        z = xx[0]

        z1 = z.f_locals
        try:
            n1 = z.get('name')
            if n1:
                print('#####z####name=',n1)
        except:
            pass
        try:
            n1 = z1.get('name')
            if n1:
                print('#####z1####name=',n1)
        except:
            pass
        #.self.name
        #print(z)
        if function in ('<module>'):
            name= xactive_moduleX
        if function not in ('call_chain','_call_with_frames_removed','exec_module','_load_unlocked','_find_and_load_unlocked','_find_and_load'):
            name = inspect.stack()[i][3]
        else:
            name=None
        if name:
            if p:
                p = p + '|' + name
            else:
                p = name
        # if not name:
        #     break
        
    print('chain:',p)
#############################################################################   
def get_api_debug_level(api_name, this_debug=None, module_id=''):
    this_debug_level=get_debug_option_as_level(this_debug)
    if this_debug_level >= 0:
        return this_debug_level

    config_key=module_id+'_debug'
    module_debug = application_configuration.get(config_key, None)
    module_debug_level = get_debug_option_as_level(module_debug)
    if module_debug_level >= 0:
        return module_debug_level

    api_name_debug = master_configuration['apis'].get(api_name, {}).get('debug_level', -1)
    debug_level = get_debug_option_as_level(api_name_debug)

    return debug_level
#############################################################################   
def get_module_debug_level(module_id):
    config_key=module_id+'_debug'
    module_debug = application_configuration.get(config_key, None)
    module_debug_level = get_debug_option_as_level(module_debug)
    return module_debug_level
#::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
def get_debug_option_as_level(debug):
    if type(debug) == type(''):
        try:
            debug = int(debug)
        except:
            debug = -1
    if debug == True:
        debug_level = 99
    elif debug == None:
        debug_level = -1
    else:
        debug_level = int(debug)
    return debug_level
#::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
def get_debug_files(this_debug, **kwargs):
    # caller_area=kwargs.get('caller_area',{})
    # caller_debug_files = caller_area.get('debug_files', [])
    # if caller_debug_files:
    #     if type(caller_debug_files) == type(''):
    #         f_array = caller_debug_files.split(';')
    #         for ix in range(0, len(f_array)):
    #             if f_array[ix]:
    #                 debug_files.append(f_array[ix])
    #                 debug_files_dict.update({f_array[ix]:{}})
    #     elif type(caller_debug_files) == type([]):
    #         for ix in range(0, len(caller_debug_files)):
    #             if caller_debug_files[ix]:
    #                 debug_files.append(caller_debug_files[ix])
    #                 debug_files_dict.update({f_array[ix]:{}})
    this_debug_level = get_debug_option_as_level(this_debug)
    if this_debug_level <= 0:
        return []

    # nowStr = datetime.datetime.utcnow().strftime("%Y-%m-%d-%H-%M")
    # nowStr = datetime.datetime.utcnow().strftime("%Y%m%d")
    nowStr = datetime.datetime.utcnow().strftime("%Y-%m-%d")
    file_prefix=f'_debug_log_{nowStr}_'
    debug_files_dict = {}
    ###################################
    table_model=kwargs.get('table_model')
    if table_model:
        try:
            model_name = table_model.__name__
        except:
            model_name = ''
        if model_name:
            try:
                if hasattr(table_model, "_debug"):
                    debug_lev = get_debug_option_as_level(table_model._debug)
                else:
                    debug_lev = -1
                if debug_lev > 0:
                    debug_file = 'dbmodel_'+table_model.__name__
                    debug_file_name=file_prefix+debug_file.strip()+'.log'
                    debug_files_dict.update({debug_file_name:{'debug_lev':debug_lev,'type':'dbmodel'}})
            except:
                debug_lev = -1
            if debug_lev < 0:
                try:
                    name_debug = application_configuration.get('database_models',{}).get(model_name, {}).get('debug_level', -1)
                    debug_lev = get_debug_option_as_level(name_debug)
                except:
                    debug_lev = -1
                if debug_lev > 0:
                    debug_file = 'model_'+model_name
                    debug_file_name=file_prefix+debug_file.strip()+'.log'
                    debug_files_dict.update({debug_file_name:{'debug_lev':debug_lev,'type':'dbmodel'}})
    ###################################
    dbsession = kwargs.get('dbsession')
    if dbsession:
        try:
            debug_lev = get_debug_option_as_level(dbsession.debug)
        except:
            debug_lev = -1
        if debug_lev > 0:
            debug_file = 'session_'+dbsession.session_id
            debug_file_name=file_prefix+debug_file.strip()+'.log'
            debug_files_dict.update({debug_file_name:{'debug_lev':debug_lev,'type':'dbsession'}})
    ###################################
    name = kwargs.get('name')
    # if not name:
    #     name = kwargs.get('process_name')
    try:
        name_debug = application_configuration.get('apis',{}).get(name, {}).get('debug_level', -1)
        debug_lev = get_debug_option_as_level(name_debug)
    except:
        debug_lev = -1
    if debug_lev > 0:
        debug_file = 'api_'+name
        debug_file_name=file_prefix+debug_file.strip()+'.log'
        debug_files_dict.update({debug_file_name:{'debug_lev':debug_lev,'type':'api'}})
    if debug_lev < 0:
        try:
            name_debug = application_configuration.get('processes',{}).get(name, {}).get('debug_level', -1)
            debug_lev = get_debug_option_as_level(name_debug)
        except:
            debug_lev = -1
        if debug_lev > 0:
            debug_file = 'api_'+name
            debug_file_name=file_prefix+debug_file.strip()+'.log'
            debug_files_dict.update({debug_file_name:{'debug_lev':debug_lev,'type':'process'}})
    ###################################
    table_name = kwargs.get('table_name')
    if table_name:
        try:
            name_debug = application_configuration.get('database_tables',{}).get(table_name, {}).get('debug_level', -1)
            debug_lev = get_debug_option_as_level(name_debug)
        except:
            debug_lev = -1
        if debug_lev > 0:
            debug_file = 'table_'+table_name
            debug_file_name=file_prefix+debug_file.strip()+'.log'
            debug_files_dict.update({debug_file_name:{'debug_lev':debug_lev,'type':'dbtable'}})
    ###################################
    action = kwargs.get('action')
    if action:
        try:
            action_debug = application_configuration.get('database_actions',{}).get(action, {}).get('debug_level', -1)
            debug_lev = get_debug_option_as_level(action_debug)
        except:
            debug_lev = -1
        if debug_lev > 0:
            debug_file = 'database_action_'+action
            debug_file_name=file_prefix+debug_file.strip()+'.log'
            debug_files_dict.update({debug_file_name:{'debug_lev':debug_lev,'type':'dbaction'}})
        if debug_lev<0:
            try:
                action_debug = application_configuration.get('actions',{}).get(action, {}).get('debug_level', -1)
                debug_lev = get_debug_option_as_level(action_debug)
            except:
                debug_lev = -1
            if debug_lev > 0:
                debug_file = 'action_'+action
                debug_file_name=file_prefix+debug_file.strip()+'.log'
                debug_files_dict.update({debug_file_name:{'debug_lev':debug_lev,'type':'process_action'}})
        if debug_lev<0:
            try:
                action_debug = application_configuration.get('methods',{}).get(action, {}).get('debug_level', -1)
                debug_lev = get_debug_option_as_level(action_debug)
            except:
                debug_lev = -1
            if debug_lev > 0:
                debug_file = 'method_'+action
                debug_file_name=file_prefix+debug_file.strip()+'.log'
                debug_files_dict.update({debug_file_name:{'debug_lev':debug_lev,'type':'metod'}})
    ###################################
    entity = kwargs.get('entity')
    if entity:
        try:
            action_debug = application_configuration.get('entities',{}).get(entity, {}).get('debug_level', -1)
            debug_lev = get_debug_option_as_level(action_debug)
        except:
            debug_lev = -1
        if debug_lev > 0:
            debug_file = 'entity_'+entity
            debug_file_name=file_prefix+debug_file.strip()+'.log'
            debug_files_dict.update({debug_file_name:{'debug_lev':debug_lev,'type':'entity'}})
    ###################################
    module = kwargs.get('module')
    if module:
        try:
            config_key=module+'_debug'
            action_debug = application_configuration.get(config_key)
            debug_lev = get_debug_option_as_level(action_debug)
        except:
            debug_lev = -1
        if debug_lev > 0:
            debug_file = 'module_'+module
            debug_file_name=file_prefix+debug_file.strip()+'.log'
            debug_files_dict.update({debug_file_name:{'debug_lev':debug_lev,'type':'module'}})

    debug_files = []
    for k in debug_files_dict.keys():
        debug_files.append(k)

    return debug_files
#::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
def get_debug_level(this_debug, **kwargs):
    this_debug_level = get_debug_option_as_level(this_debug)
    if this_debug_level >= 0:
        return this_debug_level

    debug_level1 = -1
    debug_level2 = -1
    debug_level3 = -1
    debug_level4 = -1
    debug_level5 = -1
    debug_level6 = -1
    debug_level7 = -1
    debug_level8 = -1
    debug_level9 = -1
    debug_level10 = -1

    table_model = kwargs.get('table_model')
    dbsession = kwargs.get('dbsession')

    if table_model or dbsession:
        try:
            debug_level1 = get_debug_option_as_level(application_configuration.get('database_models_debug'))
        except:
            debug_level1 = -1
        try:
            debug_level2 = get_debug_option_as_level(application_configuration.get('database_debug'))
        except:
            debug_level2 = -1
        try:
            debug_level3 = get_debug_option_as_level(application_configuration.get('database_engine_debug'))
        except:
            debug_level3 = -1
        try:
            debug_level4 = get_debug_option_as_level(application_configuration.get('database_tables_debug'))
        except:
            debug_level4 = -1
    ################
    dbengine = kwargs.get('dbengine')
    if dbengine:
        try:
            debug_level2 = get_debug_option_as_level(application_configuration.get('database_debug'))
        except:
            debug_level2 = -1
        try:
            debug_level3 = get_debug_option_as_level(application_configuration.get('database_engine_debug'))
        except:
            debug_level3 = -1
    ################
    if dbsession:
        try:
            debug_level5 = get_debug_option_as_level(dbsession.debug)
        except:
            debug_level5 = -1
    ################
    ###################################
    # table_model=kwargs.get('table_model')
    if table_model:
        try:
            model_name = table_model.__name__
        except:
            model_name = ''

        if model_name:
            try:
                if hasattr(table_model, "_debug"):
                    debug_level5 = get_debug_option_as_level(table_model._debug)
                else:
                    debug_level5 = -1
            except:
                debug_level5 = -1
            if debug_level5 < 0:
                try:
                    name_debug = application_configuration.get('database_models',{}).get(model_name, {}).get('debug_level', -1)
                    debug_level5 = get_debug_option_as_level(name_debug)
                except:
                    debug_level5 = -1
    ###################################
    name = kwargs.get('name')
    # if not name:
    #     name = kwargs.get('process_name')
    try:
        name_debug = application_configuration.get('apis',{}).get(name, {}).get('debug_level', -1)
        debug_level6 = get_debug_option_as_level(name_debug)
    except:
        debug_level6 = -1
    if debug_level6 < 0:
        try:
            name_debug = application_configuration.get('processes',{}).get(name, {}).get('debug_level', -1)
            debug_level6 = get_debug_option_as_level(name_debug)
        except:
            debug_level6 = -1
    ###################################
    table_name = kwargs.get('table_name')
    if table_name:
        try:
            name_debug = application_configuration.get('database_tables',{}).get(table_name, {}).get('debug_level', -1)
            debug_level7 = get_debug_option_as_level(name_debug)
        except:
            debug_level7 = -1
    ###################################
    action = kwargs.get('action')
    if action:
        try:
            action_debug = application_configuration.get('database_actions',{}).get(action, {}).get('debug_level', -1)
            debug_level8 = get_debug_option_as_level(action_debug)
        except:
            debug_level8 = -1
        if debug_level8<0:
            try:
                action_debug = application_configuration.get('actions',{}).get(action, {}).get('debug_level', -1)
                debug_level8 = get_debug_option_as_level(action_debug)
            except:
                debug_level8 = -1
        if debug_level8<0:
            try:
                action_debug = application_configuration.get('methods',{}).get(action, {}).get('debug_level', -1)
                debug_level8 = get_debug_option_as_level(action_debug)
            except:
                debug_level8 = -1
    ###################################
    entity = kwargs.get('entity')
    if entity:
        try:
            action_debug = application_configuration.get('entities',{}).get(entity, {}).get('debug_level', -1)
            debug_level9 = get_debug_option_as_level(action_debug)
        except:
            debug_level9 = -1
    ###################################
    module = kwargs.get('module')
    if module:
        try:
            config_key=module+'_debug'
            action_debug = application_configuration.get(config_key)
            debug_level10 = get_debug_option_as_level(action_debug)
        except:
            debug_level10 = -1

    return max(debug_level1,debug_level2,debug_level3,debug_level4,debug_level5,debug_level6,debug_level7,debug_level8,debug_level9,debug_level10)
#::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
#::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
# module initialization
#::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
#::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
#::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
module_Config_Initialized = True
msg = f'module [{module_id}] [[version {module_version}]] loaded.'
if CONSOLE_ON: 
    print_message(msg)
#::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
#::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
#::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
# main
#::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
#::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
#::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
if __name__ == '__main__':
    print(__file__)