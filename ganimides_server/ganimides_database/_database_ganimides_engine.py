import os
import sys
import datetime

from sqlalchemy import create_engine
from sqlalchemy import MetaData
from sqlalchemy import inspect
#from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from _onlineApp import thisApp
from _onlineApp import log_message,get_debug_option_as_level,log_process_result_message
#from _onlineApp import print_result, print_message
from _colorServices import colorized_string

#colors = thisApp.Fore
#import _database_ganimides_model as dbmodel
from _database_class_session import leandroutechnologyforward_database_session_class as db_session_class
from _database_class_table import leandroutechnologyforward_database_table_class as db_table_class
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 
import _database_adminServices as dbadmin

# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 
# if thisApp.DEBUG_ON:
# try:
#     database_engine_debug = thisApp.application_configuration.database_engine_debug
# except:
#     database_engine_debug = False
try:
    database_commands_echo = thisApp.application_configuration.database_commands_echo
except:
    database_commands_echo = False
try:
    database_session_debug = thisApp.application_configuration.database_session_debug
except:
    database_session_debug = None
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 
# globals
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 
global_session_counter = -1
engine = None
engine_session = None
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 
# 1: create the engine
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 
database_provider=f"sqlite:///"
database_folder_path=f"C:\\Users\\User\\Documents\\my Projects\\Systems_Development\\Development_Environment"
database_file_name=f"ganimides.db"
database_uri=f"{database_provider}{database_folder_path}\\{database_file_name}"
engine = create_engine(database_uri,echo=database_commands_echo)

inspector = inspect(engine)
table_names = inspector.get_table_names()
tables_modeled = len(table_names)
msg = f"database [ganimides] [[[[engine created]]]]:[[{database_uri}]] with [{tables_modeled} tables]"
if thisApp.CONSOLE_ON:
    log_message(msg)
else:
    log_message(msg)
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 
# 2. import the models
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 
import _database_ganimides_model as dbmodel
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 
# 3. create missing tables (use the Base of the model. Base must be declared only once)
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 
db_engine_Base = dbmodel.Base
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 
dbmodel.Base.metadata.create_all(bind=engine)
# meta = MetaData()
# meta.bind = engine
# meta.create_all(engine)
# meta.create_all()
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 
# build internal dict for check and admin
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 
db_schema = {}
db_schema_tables={}
db_schema_models={}
#print(dbmodel.Base._decl_class_registry.data)
for k in dbmodel.BaseModel.metadata.tables.keys():
    tobj = dbmodel.BaseModel.metadata.tables.get(k)
    db_schema_tables[k] = tobj
    #print(tobj)
tables_mapped = len(db_schema_tables)

for k in dbmodel.BaseModel._decl_class_registry.data.keys():
    #db_schema_models[k] = dbmodel.BaseModel._decl_class_registry.data.get(k)
    mobj = dbmodel.BaseModel._decl_class_registry.data.get(k)
    db_schema_models[k] = mobj
    #print(mobj)
    t = mobj()
    try:
        tobj = t._sa_class_manager.mapper.mapped_table
        #print(mobj)
        table_name = tobj.name
        db_schema_models[k] = tobj
        db_schema[k]={'table_name':table_name,'table_obj':tobj,'model_obj':mobj}
    except:
        pass
models_mapped=len(db_schema_models)

# #::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
# if get_debug_option_as_level(thisApp.application_configuration.database_api_debug) > 0:
#     actions = thisApp.application_configuration.get('database_actions', {})
#     for action_name in actions.keys():
#         action_entry = actions.get(action_name)
#         msg=f'module [[{module_id}]] database action [{action_name} [[[{action_entry}]]]'
#         log_message(msg)
# #::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::

#::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
if not thisApp.application_configuration.get('database_models', {}):
    thisApp.application_configuration.update({'database_models':{}})
for model_name in db_schema_models.keys():
    if not thisApp.application_configuration['database_models'].get(model_name,{}):
        model_entry = {model_name: {'status': 'Active', 'version': '1.1', 'debug_level': -1}}
        thisApp.application_configuration['database_models'].update({model_name:model_entry})
#::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
if not thisApp.application_configuration.get('database_tables', {}):
    thisApp.application_configuration.update({'database_tables':{}})
for table_name in db_schema_tables.keys():
    if not thisApp.application_configuration['database_tables'].get(table_name,{}):
        table_entry = {table_name: {'status': 'Active', 'version': '1.1', 'debug_level': -1}}
        thisApp.application_configuration['database_tables'].update({table_name:table_entry})
#::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
#::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
if not thisApp.application_configuration.get('database_actions', {}):
    thisApp.application_configuration.update({'database_actions': {}})
if not thisApp.application_configuration['database_actions'].get('get_dbsession',{}):
    action_entry = {model_name: {'status': 'Active', 'version': '1.1', 'debug_level': -1}}
    thisApp.application_configuration['database_actions'].update({'get_dbsession':action_entry})
#::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
# t = 0
# r = 0
# ix=0
# silent = False
# for k in db_schema_tables:
#     ix=ix+1
#     tableObj = db_schema_tables[k]
#     # print(ix, k, obj)
#     try:
#         table_name = tableObj.name
#     except:
#         table_name = None 
# #     # if table_name:
# #     #     build_command = f"{table_name.upper()}_TABLE = db_table_class(db_model.{k},db_schema,engine,session,debug=database_engine_debug)"
# #     #     print(build_command)


# # for table_name in db_schema:
#     # tableObj = db_schema.get(table_name)
#     if table_name:
#         t = t + 1
#         try:
#             dbadmin.check_table(tableObj, auto_synchronize=True, synchronization_method='add-columns', copy_records=True, silent=silent)
#         except Exception as error_text:
#             print(error_text)
#             try:
#                 dbadmin.check_table(tableObj, auto_synchronize=True, synchronization_method='drop-create', copy_records=True, silent=silent)
#             except:
#                 try:
#                     dbadmin.check_table(tableObj, auto_synchronize=True, synchronization_method='recreate', copy_records=True, silent=silent)
#                 except:
#                     msg=f"database [ganimides] table [[{table_name}]]#ERROR# Synchronization FAILED. #RESET#"
#                     log_message(msg)
#         r = r + tableObj.rowCount()

# dbadmin.recreate_tables(db_schema_Base,engine,debug_level)

# msg=f"database [ganimides] [[[[tables schema loaded with]]]] [[{t} tables]] and [{r} rows]"


# ix=0
# for k in db_schema_tables:
#     ix=ix+1
#     obj = db_schema_tables[k]
#     print(ix, k, obj)

# ix=0
# for k in db_schema_models:
#     ix=ix+1
#     obj = db_schema_models[k]
#     # print(ix, k, obj)
#     try:
#         table_name = obj.name
#     except:
#         table_name = None 
#     # if table_name:
#     #     build_command = f"{table_name.upper()}_TABLE = db_table_class(db_model.{k},db_schema,engine,session,debug=database_engine_debug)"
#     #     print(build_command)

# ix=0
# for k in db_schema:
#     ix=ix+1
#     obj = db_schema_models[k]
#     print(ix, k, obj)

# tt = db_schema['TEST']
# t1 = tt.get('table_obj')
# t2 = tt.get('model_obj')

# print(t1,t2)
# exit(0)
msg = f"database [ganimides] [[[[schema loaded]]]] with [[{tables_mapped} tables]] mapped by [[{models_mapped} models]]"
# if thisApp.CONSOLE_ON:
#     log_message(msg)
# else:
#     log_message(msg)
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 
def get_session_id():
    global global_session_counter
    global_session_counter = global_session_counter + 1
    timestamp_str= datetime.datetime.utcnow().strftime('%Y%m%d-%H%M%S-%f')
    session_id = timestamp_str + '-' + str(global_session_counter)
    return session_id
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 
# 4. create session (use sessionmaker) and bind it to the engine
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 
# Session = sessionmaker(bind=engine)
# session = Session()
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 
# 5. define engine level services
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 
def get_dbsession(**kwargs):
    xSession = sessionmaker(bind=engine)
    xsession = xSession()
    if 'debug' in kwargs.keys():
        debug = kwargs.get('debug', -1)
    else:
        debug = kwargs.get('debug_level', -1)
    debug_level = get_debug_option_as_level(debug)
    try:
        session_id = get_session_id()
        dbsession = db_session_class(engine, xsession, db_schema_models, session_id, debug_level)
    except:
        dbsession = None
        msg = f"FAILED to create database session for [database ganimides]"
        log_message(msg, msgType='error',msgColor=thisApp.Fore.RED)
        #exit(0)
    if dbsession:
        process_id = kwargs.get('process_msgID', '')
        if debug_level >= 0:
            kwargs.update({'debug_level':debug_level})
        if not kwargs.get('indent_method'):
            kwargs.update({'indent_method':'CALL_LEVEL'})

        msg = f"[session] [[{dbsession.session_id}]] [CREATED]"
        if process_id:
            msg=msg+'#C0# in #C0#'+process_id
        log_process_result_message('','session',msg,**kwargs)

    return dbsession
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 
def get_session():
    xSession = sessionmaker(bind=engine)
    xsession = xSession()
    return xsession
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 
def db_table_action(table_model, action, input_dict, filter_dict={}, caller_area={}):
    return engine_session.table_action(table_model, action, input_dict, filter_dict, caller_area=caller_area)    
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
def print_table_definition_commands():
    ix=0
    for k in db_schema_models:
        ix=ix+1
        obj = db_schema_models[k]
        # print(ix, k, obj)
        try:
            table_name = obj.name
        except:
            table_name = None 
        if table_name:
            build_command = f"{table_name.upper()}_TABLE = db_table_class(db_model.{k},db_schema,engine,session,debug=None)"
            print(build_command)
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 
# 5. create a customized session and bind it to the session
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 
engine_session = get_dbsession()
if engine_session:
    msg = f"database [ganimides] [[[[engine session created]]]] with session_id [{engine_session.session_id}]"
    if thisApp.CONSOLE_ON:
        log_message(msg)
    else:
        log_message(msg)
else:
    msg = f"FAILED to create database engine session for [[database ganimides]]"
    log_message(msg, msgType='info',msgColor=thisApp.Fore.RED)
    exit(0)
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 
# master_configuration={}
# #::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
# (print_enabled, filelog_enabled, log_file, errors_file,consolelog_enabled)=get_globals_from_configuration(master_configuration)
# #::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
# master_configuration = add_methods_to_configuration('database_actions', master_configuration, leandroutechnologyforward_database_session_class, ['ALL'], ['_init_'])
# #::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
# # methods == collect_method_names_from_class(leandroutechnologyforward_database_session_class, methods_ids=['ALL'])
# # print(methods)
# # exit(0)

# # master_configuration = add_apis_to_configuration('database_actions', master_configuration, thisModuleObj, functions_ids, exclude_functions_ids)

# #save_module_configuration(module_identityDictionary, master_configuration, print_enabled=consolelog_enabled, filelog_enabled=filelog_enabled)
# thisApp.pair_module_configuration('database_actions',master_configuration)
# #::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
# if get_debug_option_as_level(thisApp.application_configuration.database_api_debug) > 0:
#     actions = thisApp.application_configuration.get('database_actions', {})
#     for action_name in actions.keys():
#         action_entry = actions.get(action_name)
#         msg=f'module [[{module_id}]] database action [{action_name} [[[{action_entry}]]]'
#         log_message(msg)
# #::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
# #::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
