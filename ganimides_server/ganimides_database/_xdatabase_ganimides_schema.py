# -*- coding: utf-8 -*-
import os
import sys
import datetime

from ._dbORMApp import thisApp
from ._dbORMApp import set_debug_ON,set_debug_OFF,set_debug_level
from ._dbORMApp import log_message, log_result_message, log_module_initialization_message
from ._dbORMApp import retrieve_module_configuration
from ._dbORMApp import database_schema_class
from ._dbORMApp import database_table_class
#::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
#::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
#::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
#module
#::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
#::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
#::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
module_Function = 'database schema definition'
module_ProgramName = '_database_schema_xxxxxxxxx'
module_BaseTimeStamp = datetime.datetime.now()
module_folder = os.getcwd()
module_color = thisApp.Fore.MAGENTA
module_folder = os.path.dirname(__file__)
module_ProgramName = os.path.splitext(os.path.basename(__file__))[0]
module_id = f'{module_ProgramName}'
module_eyecatch = module_ProgramName
module_version = 0.1
module_log_file_name = module_ProgramName+'.log'
module_errors_file_name = os.path.splitext(os.path.basename(module_log_file_name))[0]+'_errors.log'
module_versionString = f'{module_id} version {module_version}'
module_file = __file__
module_debug_level = 0
module_is_externally_configurable=True
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
    'module_debug_level':module_debug_level,
    'module_is_externally_configurable':module_is_externally_configurable,
}
master_configuration = {
    'database_name': 'ganimides',
    'database_folder': 'C:\\Users\\User\\Documents\\my Projects\\Systems_Development\\Development_Environment',
    'database_user': 'admin',
    'database_pass':'spithas22311634'
}
# #::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
# #::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
# #::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
# # api services : database apis
# #::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
# #::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
# #::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
# #::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
def reorganization_process_tokens():
    where_expression = f"status='Expired'"
    result = tokens.delete_rows(where_expression)
    # print(result)
    deleted_rows = result.get('deleted_records', 0)
    nowString = datetime.datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S')
    where_expression = f"expiryDT<'{nowString}'"
    json_record = {'status': 'Expired'}
    result = tokens.update_rows(where_expression, json_record)
    # print(result)
    expired_rows = result.get('changed_records', 0)
    msg=f'tokens reorganized with {expired_rows} tokens expired, {deleted_rows} removed.'
    result = {'api_status': 'success', 'api_message': msg, 'rows_expired': expired_rows, 'rows_removed': deleted_rows}
    # print(result)
    return result
# #::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
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
time_start = datetime.datetime.now()
master_configuration = retrieve_module_configuration(module_identityDictionary, master_configuration, print_enabled=thisApp.CONSOLE_ON, filelog_enabled=thisApp.FILELOG_ON, handle_as_init=False)
moduleObj = sys.modules[__name__]
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 
dbName = master_configuration.get('database_name')
dbUser = master_configuration.get('database_user','')
dbPass = master_configuration.get('database_pass','')
dbFolder = master_configuration.get('database_folder')
if not dbName:
    msg = f'database_name not defined in config file'
    log_message(msg, msgType='error',print_enabled=True, filelog_enabled=True)
    exit(0)
dbFile = dbName.replace('_', '_').replace('-', '_').replace('.','_')
dbFile = dbFile + '.db'    
if not dbFolder:
    dbFolder=os.path.dirname(os.path.realpath(__file__))
    dbFolder = os.getcwd()
    schema_url=f'sqlite:///{dbFile}'
else:
    # package_dir = os.path.abspath(os.path.dirname(__file__))
    # db_dir = os.path.join(package_dir, 'ganimides.db')
    db_dir = dbFolder + '\\'+dbFile
    # NEED 4 /'s to specify absolute for sqlalchemy!
    # ex: sqlite:////asdfaijegoij/aerga.db
    # NEED 3 /'s for relative paths
    # path has a / at the beginning so we have 3 here
    SQLITE_DB = ''.join(['sqlite:///', db_dir])
    schema_url = ''.join(['sqlite:///', db_dir])
    
#print(schema_url)

database_schema_config = {
    #'schema_url': 'sqlite:///ganimides.db',
    'schema_url':schema_url,
    'schema_id' : 'ganimides',
    'schema_name': 'ganimides',
    'version': 2,
    'schema_reorganization_minutes': 15,
        }
#schema_url='sqlite:///ganimides.db'
database_schema = database_schema_class(schema_name='ganimides', schema_url=schema_url, schema=database_schema_config, parent_module=moduleObj, parent_module_file=__file__, user=dbUser, password=dbPass)
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 
apis_table_definition={
        'entity': 'api',
        'table_name': 'api_master',
        'rowid_column': 'api_id',
        'primary_key_columns': ['api_name'],
        'unique_value_columns': [],
        'mandatory_columns': [],
        'table_model_column_bricks':['master'],
        'foreign_keys': {
        },
        'auto_updated_columns':{
            'api_id': {'method': 'ROWID', 'data': ""},
        },
        "table_columns":{
            'api_id'               :{'data_type': 'integer', 'default': ''},
            'api_name'             :{'data_type': 'varchar(255)'},
            'status'               :{'data_type': 'varchar(50)'},
            'last_usage_timestamp' :{'data_type':'datetime', 'default':'default current_timestamp'},
        },
    }
apis = database_table_class('apis',database_schema, apis_table_definition, moduleObj, user='', password='')
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 
api_registration_table_definition={
        'entity': 'registered api',
        'table_name': 'application_apis',
        'rowid_column': 'api_id',
        'primary_key_columns': ['application_name','api_name'],
        'unique_value_columns': [],
        'mandatory_columns': [],
        'table_model_column_bricks':['master'],
        'foreign_keys': {
            'application_name': {'reference_table': 'applications', 'columns': 'application_name'},
            'api_name': {'reference_table': 'apis', 'columns': ['api_name']},
        },
        'auto_updated_columns':{
            'application_api_id': {'method': 'ROWID', 'data': ""},
            'application_id' :{'method':'FROM-FOREIGNKEY','data':{'foreign_key':'application_name','from_column':'application_id'}},            
            'api_id' :{'method':'FROM-FOREIGNKEY','data':{'foreign_key':'api_name','from_column':'api_id'}},            
        },
        "table_columns":{
            'application_api_id'  :{'data_type': 'integer', 'default': ''},
            'application_name'     :{'data_type': 'varchar(255)'},
            'api_name'             :{'data_type': 'varchar(255)'},
            'application_id'       :{'data_type': 'integer', 'default': ''},
            'api_id'               :{'data_type': 'integer', 'default': ''},
            'status'               :{'data_type': 'varchar(50)','default': 'Active'},
            'last_usage_timestamp' :{'data_type':'datetime', 'default':'default current_timestamp'},
        },
    }
registered_apis = database_table_class('application_apis',database_schema, api_registration_table_definition, moduleObj, user='', password='')
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 
applications_table_definition={
    'entity': 'application',
    'table_name': 'applications',
    'rowid_column': 'application_id',
    'primary_key_columns': ['application_name','client_id'],
    'unique_value_columns': ['application_name'],
    'mandatory_columns': ['application_name', 'application_email'],
    'table_model_column_bricks':['master'],
    'related_entities': ['account'],
    'foreign_keys': {
        'client_id': {'reference_table': 'accounts', 'columns': 'client_id'},
    },
    'auto_updated_columns':{
        'application_id': {'method': 'ROWID', 'data': ""},
        'client_secretKey': {'method': 'TOKEN', 'data': ""},
    },
    "table_columns":{
        'application_id'               :{'data_type': 'integer', 'default': ''},
        'application_name'             :{'data_type': 'text'},
        'application_email'            :{'data_type': 'text'},
        'application_redirect_uri'     :{'data_type': 'text'},
        'client_id'        :{'data_type': 'varchar(50)'},
        'client_secretKey' :{'data_type': 'varchar(255)'},
        'status'                       :{'data_type': 'text'},
        'rowDT'                        :{'data_type':'datetime', 'default':'default current_timestamp'},
    },}
applications = database_table_class('applications',database_schema, applications_table_definition, moduleObj, user='', password='')
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #     
tokens_table_definition={
        'entity': 'token',
        'table_name': 'tokens',
        'rowid_column': 'token_id',
        'primary_key_columns': [],
        'unique_value_columns': [],
        'mandatory_columns': [],
        'index_columns': ['token_type','token_scope','grant_type','token','application_name','application_client_id','client_secretKey'],
        'table_model_column_bricks':['master'],
        'foreign_keys': {
            'application_name,client_id,client_secretKey':{'reference_table': 'applications', 'columns': ['application_name','client_id','client_secretKey']},
            },
        'auto_updated_columns': {
            'token': {'method': 'TOKEN', 'data': ""},
            'token_id': {'method': 'ROWID', 'data': ""},
        },
        "table_columns":{
            'token_id'   :{'data_type': 'integer', 'default': ''},
            'token_type'  :{'data_type': 'varchar(50)', 'default': "bearer"},
            'token_scope'  :{'data_type': 'varchar(50)', 'default': "application_service"},
            'grant_type'  :{'data_type': 'varchar(50)', 'default': "client_credentials"},
            'token'   :{'data_type': 'varchar(255)', 'default': ''},
            'application_name'  :{'data_type': 'varchar(255)', 'default': ''},
            'application_client_id'  :{'data_type': 'varchar(255)', 'default': ''},
            'client_secretKey'  :{'data_type': 'varchar(255)', 'default': ''},
            'device_uid'  :{'data_type': 'varchar(255)', 'default': ''},
            # 'subscription_id'  :{'data_type': 'varchar(255)', 'default': ''},
            # 'geolocation_lat'   :{'data_type': ' decimal(12,6)', 'default': '0'},
            # 'geolocation_lon'   :{'data_type': ' decimal(12,6)', 'default': '0'},
            'duration_seconds'   :{'data_type': 'integer', 'default': '3600'},
            'expiryDT' :{'data_type':'datetime', 'default':''},
            'status'               :{'data_type': 'varchar(50)','default':"'Active'"},
            'last_usage_timestamp' :{'data_type':'datetime', 'default':'default current_timestamp'},
            'rowDT' :{'data_type':'datetime', 'default':'default current_timestamp'},
            },}
tokens = database_table_class('tokens',database_schema, tokens_table_definition, moduleObj, user='', password='')
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 
clients_table_definition={
        'entity': 'client',
        'table_name': 'clients',
        'rowid_column': 'client_id',
        'primary_key_columns': ['email','client_type'],
        'unique_value_columns': ['client_type,mobile','client_type,phone','client_type,email'],
        'mandatory_columns': ['name'],
        'table_model_column_bricks':['client','master'],
        'foreign_keys': {
        },
        'auto_updated_columns':{
            'id'        : {'method': 'ROWID', 'data': ""},
            'client_id' : {'method': 'UID', 'data': ""},
            'client_secretKey' : {'method': 'TOKEN', 'data': ""},
        },
        "validations": {
            "email":[{"rule":"email","message":"email not valid"}],
            "mobile": [
                {"rule":"telephone", "message":"mobile must be 00(ctry)nnnnnnnn"},
                {"rule": "mobile", "message": "mobile must be 00(ctry)9nnnnnnn"},
            ],
            "phone": [
                {"rule":"telephone", "message":"mobile must be 00(ctry)nnnnnnnn"},
            ],
        },
        "table_columns":{
            'id'          :{'data_type': 'integer', 'default': ''},
            'client_id'   :{'data_type': 'varchar(50)', 'default': ''},
            'client_type'   :{'data_type': 'varchar(50)', 'default': "consumer"},
            'client_secretKey'   :{'data_type': 'varchar(255)', 'default': ''},
            'name'        :{'data_type': 'varchar(255)'},
            'email'       :{'data_type': 'varchar(255)'},
            'mobile'      :{'data_type': 'varchar(50)', 'default': ''},
            'last_name'   :{'data_type': 'varchar(255)', 'default': ''},
            'first_name'  :{'data_type': 'varchar(255)', 'default': ''},
            'birth_date'  :{'data_type': 'varchar(50)', 'default': ''},
            'title'  :{'data_type': 'varchar(50)', 'default': ''},
            'phone'  :{'data_type': 'varchar(50)', 'default': ''},
            'status'      :{'data_type': 'varchar(50)'},
            'confirmed'     :{'data_type': 'Integer'},
            'confirmed_timestamp'   :{'data_type': 'datetime'},
            'password'      :{'data_type': 'varchar(255)'},
            'last_usage_timestamp' :{'data_type':'datetime', 'default':'current_timestamp'},
        },
    }
clients = database_table_class('clients',database_schema, clients_table_definition, moduleObj, user='', password='')
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 
merchants_table_definition={
    'entity': 'merchant',
    'table_name': 'merchants',
    'rowid_column': 'merchant_id',
    'primary_key_columns': ['name'],
    'unique_value_columns': ['email'],
    'mandatory_columns': ['email','mobile','client_id'],
    'table_model_column_bricks':['master'],
    'foreign_keys': {
        'client_id': {'reference_table': 'clients', 'columns': ['client_id']},
        # 'application_id': {'reference_table': 'applications', 'columns': ['application_id']},
    },
    'auto_updated_columns':{
        'merchant_id'        :{'method':'UID','data':""},
        'merchant_secretKey': {'method': 'TOKEN', 'data': ""},
        'status' :{'method':'FROM-FOREIGNKEY','data':{'foreign_key':'client_id','from_column':'status'}},            
    },
    "validations": {
        "email":[{"rule":"email","message":"email not valid"}],
        "mobile": [
            {"rule":"telephone", "message":"mobile must be 00(ctry)nnnnnnnn"},
            {"rule": "mobile", "message": "mobile must be 00(ctry)9nnnnnnn"},
        ]
    },
    "table_columns":{
        'merchant_id'         :{'data_type': 'varchar(255)'},
        'merchant_secretKey'         :{'data_type': 'varchar(255)'},
        'merchant_code'         :{'data_type': 'varchar(255)'},
        'name'         :{'data_type': 'varchar(255)'},
        'merchant_store'         :{'data_type': 'varchar(255)'},
        'terminalID'         :{'data_type': 'varchar(255)'},
        'branchID'         :{'data_type': 'varchar(255)'},
        'transactionID'         :{'data_type': 'varchar(255)'},
        'address'         :{'data_type': 'varchar(255)'},
        'email'         :{'data_type': 'varchar(255)'},
        'mobile'         :{'data_type': 'varchar(255)'},
        'phone'         :{'data_type': 'varchar(50)'},
        'shortAddress'         :{'data_type': 'varchar(255)'},
        'client_id'         :{'data_type': 'varchar(50)'},
        'payments_currency'         :{'data_type': 'varchar(3)','default':'EUR'},
        'status'         :{'data_type': 'varchar(50)'},
        'merchant_logo'         :{'data_type': 'text'},
        'merchant_logo_file'         :{'data_type': 'text'},

        'bank_account_id'       :{'data_type': 'varchar(255)'},
        'bank_subscription_id'  :{'data_type': 'varchar(255)'},
        'bank_code'              :{'data_type': 'varchar(50)'},
        'bank_subscriptionID'   :{'data_type': 'varchar(50)'},
        'bank_accountID'        :{'data_type': 'varchar(50)'},
        },
    }
merchants = database_table_class('merchants', database_schema, merchants_table_definition, moduleObj, user='', password='')
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 
pointsofsale_table_definition={
    'entity': 'point of sale',
    'table_name': 'points_of_sale',
    'rowid_column': 'pointofsale_id',
    'primary_key_columns': ['merchant_id','name'],
    'unique_value_columns': [''],
    'mandatory_columns': ['name','terminalID'],
    'table_model_column_bricks':['master'],
    'foreign_keys': {
        'merchant_id': {'reference_table': 'merchants', 'columns': ['merchant_id']},
    },
    'auto_updated_columns':{
        'pointofsale_id'        :{'method':'UID','data':""},
        'pointofsale_secretKey': {'method': 'TOKEN', 'data': ""},
        'merchant_code' :{'method':'FROM-FOREIGNKEY','data':{'foreign_key':'merchant_id','from_column':'merchant_code'}},            
        'merchant_store' :{'method':'FROM-FOREIGNKEY','data':{'foreign_key':'merchant_id','from_column':'merchant_store'}},            
        'merchant_name' :{'method':'FROM-FOREIGNKEY','data':{'foreign_key':'merchant_id','from_column':'name'}},            
    },
    "validations": {
        # "email":[{"rule":"email","message":"email not valid"}],
        # "mobile": [
        #     {"rule":"telephone", "message":"mobile must be 00(ctry)nnnnnnnn"},
        #     {"rule": "mobile", "message": "mobile must be 00(ctry)9nnnnnnn"},
        # ]
    },
    "table_columns":{
        'pointofsale_id'         :{'data_type': 'varchar(50)'},
        'pointofsale_secretKey'         :{'data_type': 'varchar(255)'},
        'pointofsale_code'         :{'data_type': 'varchar(50)'},
        'merchant_id'         :{'data_type': 'varchar(50)'},
        'merchant_code'         :{'data_type': 'varchar(255)'},
        'merchant_store'         :{'data_type': 'varchar(255)'},
        'merchant_name'         :{'data_type': 'varchar(255)'},
        'name'                  :{'data_type': 'varchar(255)'},
        'terminalID'         :{'data_type': 'varchar(255)'},
        'branchID'         :{'data_type': 'varchar(255)'},
        'transactionID'         :{'data_type': 'varchar(255)'},
        'address'         :{'data_type': 'varchar(255)'},
        # 'email'         :{'data_type': 'varchar(255)'},
        # 'mobile'         :{'data_type': 'varchar(255)'},
        'shortAddress'         :{'data_type': 'varchar(255)'},
        'geolocation_lat' :{'data_type':'decimal(12,6)', 'default':'0'},
        'geolocation_lon' :{'data_type':'decimal(12,6)', 'default':'0'},

        'bank_account_id'       :{'data_type': 'varchar(255)'},
        'bank_subscription_id'  :{'data_type': 'varchar(255)'},
        'bank_code'              :{'data_type': 'varchar(50)'},
        'bank_subscriptionID'   :{'data_type': 'varchar(50)'},
        'bank_accountID'        :{'data_type': 'varchar(50)'},
        'payments_currency'         :{'data_type': 'varchar(3)','default':'EUR'},

        'signed_tellerID'         :{'data_type': 'varchar(50)'},
        'signed_tellerID_timestamp' :{'data_type':'datetime', 'default':''},
        'signed_tellerID_expiry_timestamp' :{'data_type':'datetime', 'default':''},
        'signed_tellerID_geolocation_lat' :{'data_type':'decimal(12,6)', 'default':'0'},
        'signed_tellerID_geolocation_lon' :{'data_type':'decimal(12,6)', 'default':'0'},

        'status'         :{'data_type': 'varchar(50)'},
        },
    }
points_of_sale = database_table_class('points_of_sale',database_schema, pointsofsale_table_definition, moduleObj, user='', password='')
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 
employees_table_definition={
    'entity': 'employee',
    'table_name': 'employees',
    'rowid_column': 'employee_id',
    'primary_key_columns': ['merchant_id','employee_code'],
    'unique_value_columns': [''],
    'mandatory_columns': ['name','employee_code'],
    'table_model_column_bricks':['master'],
    'foreign_keys': {
        'merchant_id': {'reference_table': 'merchants', 'columns': ['merchant_id']},
        # 'client_id': {'reference_table': 'clients', 'columns': ['client_id']},
    },
    'auto_updated_columns':{
        'id'        :{'method':'ROWID','data':""},
        'employee_id'        :{'method':'UID','data':""},
        'employee_secretKey': {'method': 'TOKEN', 'data': ""},
        'merchant_code' :{'method':'FROM-FOREIGNKEY','data':{'foreign_key':'merchant_id','from_column':'merchant_code'}},            
        'merchant_store' :{'method':'FROM-FOREIGNKEY','data':{'foreign_key':'merchant_id','from_column':'merchant_store'}},            
        'merchant_name' :{'method':'FROM-FOREIGNKEY','data':{'foreign_key':'merchant_id','from_column':'name'}},            
    },
    "validations": {
    },
    "table_columns":{
        'id'        :{'data_type': 'integer', 'default': ''},
        'employee_id'         :{'data_type': 'varchar(50)'},
        'employee_secretKey'         :{'data_type': 'varchar(255)'},
        'employee_code'         :{'data_type': 'varchar(50)'},
        'name'         :{'data_type': 'varchar(255)'},
        'merchant_id'         :{'data_type': 'varchar(50)'},
        'merchant_code'         :{'data_type': 'varchar(255)'},
        'merchant_store'         :{'data_type': 'varchar(255)'},
        'merchant_name'         :{'data_type': 'varchar(255)'},
        # 'client_id'         :{'data_type': 'varchar(50)'},
        'last_signon_pointofsale_id'         :{'data_type': 'varchar(50)'},
        'last_signon_timestamp' :{'data_type':'datetime', 'default':''},
        'last_signoff_timestamp' :{'data_type':'datetime', 'default':''},
        'last_signon_expiry_timestamp' :{'data_type':'datetime', 'default':''},
        'last_signon_geolocation_lat' :{'data_type':'decimal(12,6)', 'default':'0'},
        'last_signon_geolocation_lon' :{'data_type':'decimal(12,6)', 'default':'0'},

        'status'         :{'data_type': 'varchar(50)'},
        },
    }
employees = database_table_class('employees',database_schema, employees_table_definition, moduleObj, user='', password='')
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 
consumers_table_definition={
    'entity': 'consumer',
    'table_name': 'consumers',
    'rowid_column': 'consumer_id',
    'primary_key_columns': ['email'],
    'unique_value_columns': [''],
    'mandatory_columns': ['email','mobile'],
    'table_model_column_bricks':['master'],
    'foreign_keys': {
        'client_id': {'reference_table': 'clients', 'columns': ['client_id']},
    },
    'auto_updated_columns':{
        'consumer_id'        :{'method':'UID','data':""},
        'id'        :{'method':'ROWID','data':""},
        'consumer_secretKey': {'method': 'TOKEN', 'data': ""},
        'status' :{'method':'FROM-FOREIGNKEY','data':{'foreign_key':'client_id','from_column':'status'}},            
    },
    "validations": {
    },
    "table_columns":{
        'id'        :{'data_type': 'integer', 'default': ''},
        'consumer_id'         :{'data_type': 'varchar(255)'},
        'consumer_secretKey'         :{'data_type': 'varchar(255)'},
        'name'         :{'data_type': 'varchar(255)'},
        'email'         :{'data_type': 'varchar(255)'},
        'mobile': {'data_type': 'varchar(255)'},
        'status'         :{'data_type': 'varchar(50)'},
        },
    }
consumers = database_table_class('consumers', database_schema, consumers_table_definition, moduleObj, user='', password='')
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 
banks_table_definition={
    'entity': 'bank',
    'table_name': 'banks',
    'rowid_column': 'bank_id',
    'primary_key_columns': ['bank_BIC'],
    'unique_value_columns': ['bank_code'],
    'mandatory_columns': [],
    'table_model_column_bricks':['master'],
    'foreign_keys': {
    },
    'auto_updated_columns':{
        'bank_id'   :{'method':'ROWID','data':""},
    },
    "validations": {
    },
    "table_columns":{
        'bank_id'               :{'data_type': 'integer', 'default': ''},
        'bank_code'             :{'data_type': 'varchar(50)'},
        'bank_BIC'              :{'data_type': 'varchar(50)'},
        'bank_SWIFT'            :{'data_type': 'varchar(50)'},
        'bank_short_code'       :{'data_type': 'varchar(50)'},
        'bank_name'             :{'data_type': 'varchar(255)'},
        'status'                :{'data_type': 'varchar(50)'},
        },
    }
banks = database_table_class('banks', database_schema, banks_table_definition, moduleObj, user='', password='')
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 
bank_subscriptions_table_definition={
    'entity': 'bank subscription',
    'table_name': 'bank_subscriptions',
    'rowid_column': 'bank_subscription_id',
    'primary_key_columns': ['bank_code', 'bank_subscriptionID', 'client_id'],
    'unique_value_columns': [''],
    'mandatory_columns': [],
    'table_model_column_bricks':['master'],
    'foreign_keys': {
        'bank_code': {'reference_table': 'banks', 'columns': ['bank_code']},
        'application_id': {'reference_table': 'applications', 'columns': ['application_id']},
        'client_id': {'reference_table': 'clients', 'columns': ['client_id']},
    },
    'auto_updated_columns':{
        'bank_subscription_id'  :{'method':'UID','data':""},
    },
    "validations": {
    },
    "table_columns":{
        'bank_subscription_id'  :{'data_type': 'varchar(50)'},
        'client_id'              :{'data_type': 'varchar(50)'},
        'application_id'              :{'data_type': 'varchar(50)'},
        'application_name'              :{'data_type': 'varchar(255)'},
        'bank_code'              :{'data_type': 'varchar(50)'},
        'bank_subscriptionID'   :{'data_type': 'varchar(50)'},
        'status'                :{'data_type': 'varchar(50)'},
        'client_type'            :{'data_type': 'varchar(255)'},
        'client_name'            :{'data_type': 'varchar(255)'},
        'authorization_code'   :{'data_type': 'varchar(255)'},
        'authorization_token'   :{'data_type': 'varchar(255)'},
        'payments_limit'        :{'data_type': 'integer','default':'0'},
        'payments_amount'       :{'data_type': 'integer','default':'0'},
        'payments_currency'     :{'data_type': 'VARCHAR(10)'},
        'account_allow_transactionHistory'        :{'data_type': 'integer','default':'0'},
        'account_allow_balance'        :{'data_type': 'integer','default':'0'},
        'account_allow_details'        :{'data_type': 'integer','default':'0'},
        'account_allow_checkFundsAvailability'        :{'data_type': 'integer','default':'0'},
        },
    }
bank_subscriptions = database_table_class('bank_subscriptions', database_schema, bank_subscriptions_table_definition, moduleObj, user='', password='')
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 
bank_authorizations_table_definition={
    'entity': 'bank authorization code',
    'table_name': 'bank_authorizations',
    'rowid_column': 'bank_authorization_id',
    'primary_key_columns': [],
    'unique_value_columns': [''],
    'mandatory_columns': ['bank_code','bank_subscriptionID','client_id','application_id'],
    'table_model_column_bricks':[''],
    'foreign_keys': {
        'bank_code': {'reference_table': 'banks', 'columns': ['bank_code']},
        'application_id': {'reference_table': 'applications', 'columns': ['application_id']},
        'client_id': {'reference_table': 'clients', 'columns': ['client_id']},
    },
    'auto_updated_columns':{
        'bank_authorization_id'  :{'method':'ROWID','data':""},
    },
    "validations": {
    },
    "table_columns":{
        'bank_authorization_id'  :{'data_type': 'integer', 'default': ''},
        'client_id'              :{'data_type': 'varchar(50)'},
        'application_id'              :{'data_type': 'varchar(50)'},
        'application_name'              :{'data_type': 'varchar(255)'},
        'bank_code'              :{'data_type': 'varchar(50)'},
        'bank_subscriptionID'   :{'data_type': 'varchar(50)'},
        'status'                :{'data_type': 'varchar(50)'},
        'client_type'            :{'data_type': 'varchar(255)'},
        'client_name'            :{'data_type': 'varchar(255)'},
        'authorization_code'   :{'data_type': 'varchar(255)'},
        'authorization_token'   :{'data_type': 'varchar(255)'},
        'error'                 :{'data_type': 'varchar(255)','default':''},
        },
    }
bank_authorizations = database_table_class('bank_authorizations', database_schema, bank_authorizations_table_definition, moduleObj, user='', password='')
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 
bank_accounts_table_definition={
    'entity': 'bank account',
    'table_name': 'BANK_ACCOUNTS',
    'rowid_column': 'bank_account_id',
    'primary_key_columns': ['bank_subscription_id','bank_accountID'],
    'unique_value_columns': [''],
    'mandatory_columns': [],
    'table_model_column_bricks':[''],
    'foreign_keys': {
        'bank_subscription_id': {'reference_table': 'bank_subscriptions', 'columns': ['bank_subscription_id']},
    },
    'auto_updated_columns':{
        'bank_account_id'      : {'method': 'UID','data':""},
        'status'  : {'method': 'FROM-FOREIGNKEY','data':{'foreign_key':'bank_subscription_id','from_column':'status'}},
        'bank_code': {'method': 'FROM-FOREIGNKEY', 'data': {'foreign_key': 'bank_subscription_id', 'from_column': 'bank_code'}},
        'bank_subscriptionID': {'method': 'FROM-FOREIGNKEY', 'data': {'foreign_key': 'bank_subscription_id', 'from_column': 'bank_subscriptionID'}},
    },
    "validations": {
    },
    "table_columns":{
        'bank_account_id'       :{'data_type': 'varchar(255)'},
        'bank_subscription_id'  :{'data_type': 'varchar(255)'},
        'client_id'              :{'data_type': 'varchar(50)'},
        'application_id'              :{'data_type': 'varchar(50)'},
        'application_name'              :{'data_type': 'varchar(255)'},
        'bank_code'              :{'data_type': 'varchar(50)'},
        'bank_subscriptionID'   :{'data_type': 'varchar(50)'},
        'client_type'            :{'data_type': 'varchar(255)'},
        'client_name'            :{'data_type': 'varchar(255)'},
        'bank_accountID'        :{'data_type': 'varchar(50)'},
        'payments_limit'        :{'data_type': 'integer','default':'0'},
        'payments_amount'       :{'data_type': 'integer','default':'0'},
        'payments_currency'     :{'data_type': 'VARCHAR(10)'},
        'account_allow_transactionHistory'        :{'data_type': 'integer','default':'0'},
        'account_allow_balance'        :{'data_type': 'integer','default':'0'},
        'account_allow_details'        :{'data_type': 'integer','default':'0'},
        'account_allow_checkFundsAvailability'        :{'data_type': 'integer','default':'0'},
        'status'                :{'data_type': 'varchar(50)'},
        },
    }
BANK_ACCOUNTS = database_table_class('BANK_ACCOUNTS', database_schema, bank_accounts_table_definition, moduleObj, user='', password='')
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 
# merchants_bank_subscriptions_table_definition={
#     'entity': 'merchant bank subscription',
#     'table_name': 'merchants_bank_subscriptions',
#     'rowid_column': 'bank_subscription_id',
#     'primary_key_columns': ['merchant_id'],
#     'unique_value_columns': [''],
#     'mandatory_columns': ['subscription_id'],
#     'table_model_column_bricks':['master'],
#     'foreign_keys': {
#         'merchant_id': {'reference_table': 'merchants', 'columns': ['merchant_id']},
#     },
#     'auto_updated_columns':{
#         'bank_subscription_id'        :{'method':'UID','data':""},
#         'id'        :{'method':'ROWID','data':""},
#         #'status' :{'method':'FROM-FOREIGNKEY','data':{'foreign_key':'client_id','from_column':'status'}},            
#     },
#     "validations": {
#     },
#     "table_columns":{
#         'id'        :{'data_type': 'integer', 'default': ''},
#         'bank_subscription_id'         :{'data_type': 'varchar(255)'},
#         'merchant_id'         :{'data_type': 'varchar(255)'},
#         'subscription_id'     :{'data_type': 'varchar(50)'},
#         'bank_id'         :{'data_type': 'varchar(50)'},
#         'bank_accountID'         :{'data_type': 'varchar(50)'},
#         'status'         :{'data_type': 'varchar(50)'},
#         },
#     }
# merchants_bank_subscriptions = database_table_class('merchants_bank_subscriptions', database_schema, merchants_bank_subscriptions_table_definition, moduleObj, user='', password='')
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 
# points_of_sale_bank_subscriptions_table_definition={
#     'entity': 'pointofsale bank subscription',
#     'table_name': 'points_of_sale_bank_subscriptions',
#     'rowid_column': 'bank_subscription_id',
#     'primary_key_columns': ['pointofsale_id'],
#     'unique_value_columns': [''],
#     'mandatory_columns': [],
#     'table_model_column_bricks':['master'],
#     'foreign_keys': {
#         'pointofsale_id': {'reference_table': 'points_of_sale', 'columns': ['pointofsale_id']},
#     },
#     'auto_updated_columns':{
#         'bank_subscription_id'        :{'method':'UID','data':""},
#         'id'        :{'method':'ROWID','data':""},
#         #'status' :{'method':'FROM-FOREIGNKEY','data':{'foreign_key':'client_id','from_column':'status'}},            
#     },
#     "validations": {
#     },
#     "table_columns":{
#         'id'        :{'data_type': 'integer', 'default': ''},
#         'bank_subscription_id'         :{'data_type': 'varchar(255)'},
#         'pointofsale_id'         :{'data_type': 'varchar(255)'},
#         'bank_id'         :{'data_type': 'varchar(50)'},
#         'subscription_id'     :{'data_type': 'varchar(50)'},
#         'bank_accountID'         :{'data_type': 'varchar(50)'},
#         'status'         :{'data_type': 'varchar(50)'},
#         },
#     }
# points_of_sale_bank_subscriptions = database_table_class('points_of_sale_bank_subscriptions', database_schema, points_of_sale_bank_subscriptions_table_definition, moduleObj, user='', password='')
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 
# consumers_bank_subscriptions_table_definition={
#     'entity': 'consumer bank subscription',
#     'table_name': 'consumers_bank_subscriptions',
#     'rowid_column': 'bank_subscription_id',
#     'primary_key_columns': ['consumer_id','subscription_id','bank_id','bank_accountID'],
#     'unique_value_columns': [''],
#     'mandatory_columns': [],
#     'table_model_column_bricks':['master'],
#     'foreign_keys': {
#         'consumer_id': {'reference_table': 'consumers', 'columns': ['consumer_id']},
#     },
#     'auto_updated_columns':{
#         'bank_subscription_id'        :{'method':'UID','data':""},
#         'id'        :{'method':'ROWID','data':""},
#         #'status' :{'method':'FROM-FOREIGNKEY','data':{'foreign_key':'client_id','from_column':'status'}},            
#     },
#     "validations": {
#     },
#     "table_columns":{
#         'id'        :{'data_type': 'integer', 'default': ''},
#         'bank_subscription_id'         :{'data_type': 'varchar(255)'},
#         'consumer_id'         :{'data_type': 'varchar(255)'},
#         'subscription_id'     :{'data_type': 'varchar(50)'},
#         'bank_id'         :{'data_type': 'varchar(50)'},
#         'bank_accountID'         :{'data_type': 'varchar(50)'},
#         'status'         :{'data_type': 'varchar(50)'},
#         },
#     }
# consumers_bank_subscriptions = database_table_class('consumers_bank_subscriptions', database_schema, consumers_bank_subscriptions_table_definition, moduleObj, user='', password='')
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 
devices_table_definition={
        'entity': 'device',
        'table_name': 'devices',
        'rowid_column': 'device_id',
        'primary_key_columns': ['device_uid'],
        'unique_value_columns': [],
        'mandatory_columns': [],
        'table_model_column_bricks':['master'],
        'foreign_keys': {
        },
        'auto_updated_columns':{
            'device_id': {'method': 'ROWID', 'data': ""},
        },
        "table_columns":{
            'device_id'               :{'data_type': 'integer', 'default': ''},
            'device_uid'             :{'data_type': 'varchar(255)'},
            'last_usage_geolocation_lat'            :{'data_type': 'varchar(50)'},
            'last_usage_geolocation_lon'                 :{'data_type': 'varchar(50)'},
            'status'                       :{'data_type': 'text'},
            'last_usage_timestamp'                        :{'data_type':'datetime', 'default':'current_timestamp'},
        },
    }
devices = database_table_class('devices',database_schema, devices_table_definition, moduleObj, user='', password='')
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 
device_usage_table_definition={
        'entity': 'device usage',
        'table_name': 'device_usage',
        'rowid_column': 'id',
        'primary_key_columns': ['device_uid','owner_type','owner_id','geolocation_lat','geolocation_lon'],
        'unique_value_columns': [],
        'mandatory_columns': [],
        'table_model_column_bricks':['master'],
        'foreign_keys': {
            'device_uid': {'reference_table': 'devices', 'columns': ['device_uid']},
        },
        'auto_updated_columns':{
            'id': {'method': 'ROWID', 'data': ""},
        },
        "table_columns":{
            'id'                    : {'data_type': 'integer'       , 'default': ''},
            'device_uid'            : {'data_type': 'varchar(255)'  , 'default': ''},
            'application_id'        : {'data_type': 'varchar(50)'   , 'default': ''},
            'owner_type'            : {'data_type': 'varchar(50)'   , 'default': 'client'},
            'owner_id'              : {'data_type': 'varchar(50)'   , 'default': ''},
            'owner_name'            : {'data_type': 'varchar(255)'  , 'default': ''},
            'geolocation_lat'       : {'data_type': 'decimal(12,6)' , 'default': '0'},
            'geolocation_lon'       : {'data_type': 'decimal(12,6)' , 'default': '0'},
            'status'                : {'data_type': 'varchar(50)'   , 'default': 'Active'},
            'last_usage_timestamp'  : {'data_type': 'datetime'      , 'default':'current_timestamp'},
        },
    }
device_usage = database_table_class('device_usage',database_schema, device_usage_table_definition, moduleObj, user='', password='')
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 
client_devices_table_definition={
        'entity': 'client device',
        'table_name': 'client_devices',
        'rowid_column': 'client_device_id',
        'primary_key_columns': ['device_uid','client_id','geolocation_lat','geolocation_lon'],
        'unique_value_columns': [],
        'mandatory_columns': [],
        'table_model_column_bricks':['master'],
        'foreign_keys': {
            'device_uid': {'reference_table': 'devices', 'columns': ['device_uid']},
            'client_id': {'reference_table': 'clients', 'columns': ['client_id']},
        },
        'auto_updated_columns':{
            'client_device_id': {'method': 'ROWID', 'data': ""},
            'client_email' :{'method':'FROM-FOREIGNKEY','data':{'foreign_key':'client_id','from_column':'email'}},            
        },
        "table_columns":{
            'client_device_id'      :{'data_type': 'integer', 'default': ''},
            'device_uid'            :{'data_type': 'varchar(255)', 'default': ''},
            'client_id'             :{'data_type': 'varchar(50)', 'default': ''},
            'client_email'          :{'data_type': 'varchar(255)', 'default': ''},
            'geolocation_lat'       :{'data_type':'decimal(12,6)', 'default':'0'},
            'geolocation_lon'       :{'data_type':'decimal(12,6)', 'default':'0'},
            'status'                :{'data_type': 'varchar(50)', 'default': 'Active'},
            'last_usage_timestamp'  :{'data_type':'datetime', 'default':'current_timestamp'},
        },
    }
client_devices = database_table_class('client_devices',database_schema, client_devices_table_definition, moduleObj, user='', password='')
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 
# merchant_devices_table_definition={
#         'entity': 'merchant device',
#         'table_name': 'merchant_devices',
#         'rowid_column': 'merchant_device_id',
#         'primary_key_columns': ['device_uid','merchant_id','geolocation_lat','geolocation_lon'],
#         'unique_value_columns': [],
#         'mandatory_columns': [],
#         'table_model_column_bricks':['master'],
#         'foreign_keys': {
#             'device_uid': {'reference_table': 'devices', 'columns': ['device_uid']},
#             'merchant_id': {'reference_table': 'merchants', 'columns': ['merchant_id']},
#         },
#         'auto_updated_columns':{
#             'merchant_device_id': {'method': 'ROWID', 'data': ""},
#             'merchant_name' :{'method':'FROM-FOREIGNKEY','data':{'foreign_key':'merchant_id','from_column':'name'}},            
#         },
#         "table_columns":{
#             'client_device_id'      :{'data_type': 'integer', 'default': ''},
#             'device_uid'            :{'data_type': 'varchar(255)', 'default': ''},
#             'merchant_id'           :{'data_type': 'varchar(50)', 'default': ''},
#             'merchant_name'         :{'data_type': 'varchar(255)', 'default': ''},
#             'geolocation_lat'       :{'data_type':'decimal(12,6)', 'default':'0'},
#             'geolocation_lon'       :{'data_type':'decimal(12,6)', 'default':'0'},
#             'status'                :{'data_type': 'varchar(50)', 'default': 'Active'},
#             'last_usage_timestamp'  :{'data_type':'datetime', 'default':'current_timestamp'},
#         },
#     }
# merchant_devices = database_table_class('merchant_devices',database_schema, merchant_devices_table_definition, moduleObj, user='', password='')
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 
# pointofsale_devices_table_definition={
#         'entity': 'pointofsale device',
#         'table_name': 'pointofsale_devices',
#         'rowid_column': 'pointofsale_device_id',
#         'primary_key_columns': ['device_uid','pointofsale_id','geolocation_lat','geolocation_lon'],
#         'unique_value_columns': [],
#         'mandatory_columns': [],
#         'table_model_column_bricks':['master'],
#         'foreign_keys': {
#             'device_uid': {'reference_table': 'devices', 'columns': ['device_uid']},
#             'pointofsale_id': {'reference_table': 'points_of_sale', 'columns': ['pointofsale_id']},
#         },
#         'auto_updated_columns':{
#             'pointofsale_device_id': {'method': 'ROWID', 'data': ""},
#             'pointofsale_name' :{'method':'FROM-FOREIGNKEY','data':{'foreign_key':'pointofsale_id','from_column':'name'}},            
#         },
#         "table_columns":{
#             'client_device_id'      : {'data_type': 'integer', 'default': ''},
#             'device_uid'            : {'data_type': 'varchar(255)', 'default': ''},
#             'pointofsale_id'        : {'data_type': 'varchar(50)', 'default': ''},
#             'pointofsale_name'      : {'data_type': 'varchar(255)', 'default': ''},
#             'geolocation_lat'       : {'data_type': 'decimal(12,6)', 'default': '0'},
#             'geolocation_lon'       : {'data_type': 'decimal(12,6)', 'default': '0'},
#             'status'                : {'data_type': 'varchar(50)', 'default': 'Active'},
#             'last_usage_timestamp'  : {'data_type':'datetime', 'default':'current_timestamp'},
#         },
#     }
# pointofsale_devices = database_table_class('pointofsale_devices',database_schema, pointofsale_devices_table_definition, moduleObj, user='', password='')
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 
interactions_table_definition={
    'entity': 'interaction',
    'table_name': 'interactions',
    'rowid_column': 'interaction_id',
    'primary_key_columns': [],
    'unique_value_columns': [],
    'mandatory_columns': [],
    'table_model_column_bricks':['master'],
    'foreign_keys': {
        'consumer_id': {'reference_table': 'consumers', 'columns': ['consumer_id']},
    },
    'auto_updated_columns':{
        'interaction_id'        :{'method':'UID','data':""},
        'id'        :{'method':'ROWID','data':""},
        #'status' :{'method':'FROM-FOREIGNKEY','data':{'foreign_key':'client_id','from_column':'status'}},            
    },
    "validations": {
    },
    "table_columns":{
        'id'        :{'data_type': 'integer', 'default': ''},
        'interaction_id'         :{'data_type': 'varchar(255)'},
        'originator'     :{'data_type': 'varchar(50)'},
        'corresponder'     :{'data_type': 'varchar(50)'},
        'originator_id'         :{'data_type': 'varchar(50)'},
        'corresponder_id'         :{'data_type': 'varchar(50)'},
        'status'         :{'data_type': 'varchar(50)','default':'Active'},
        'completed_timestamp'         :{'data_type':'datetime', 'default':''},
        'duration'         :{'data_type':'integer', 'default':'0'},
        },
    }
interactions = database_table_class('interactions', database_schema, interactions_table_definition, moduleObj, user='', password='')
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 
interaction_messages_table_definition={
    'entity': 'interaction message',
    'table_name': 'interaction_messages',
    'rowid_column': 'interaction_message_id',
    'primary_key_columns': [],
    'unique_value_columns': [],
    'mandatory_columns': [],
    'table_model_column_bricks':['transactions'],
    'foreign_keys': {
        'interaction_id': {'reference_table': 'interactions', 'columns': ['interaction_id']},
    },
    'auto_updated_columns':{
        'interaction_message_id'        :{'method':'UID','data':""},
        'id'        :{'method':'ROWID','data':""},
        #'status' :{'method':'FROM-FOREIGNKEY','data':{'foreign_key':'client_id','from_column':'status'}},            
    },
    "validations": {
    },
    "table_columns":{
        'id'        :{'data_type': 'integer', 'default': ''},
        'interaction_message_id'         :{'data_type': 'varchar(50)'},
        'interaction_id'         :{'data_type': 'varchar(255)'},
        'originator_id'         :{'data_type': 'varchar(50)'},
        'originator'     :{'data_type': 'varchar(50)'},
        'message_type'         :{'data_type': 'varchar(50)'},
        'message_record'         :{'data_type': 'varchar(1024)'},
        'content_type'         :{'data_type': 'varchar(50)'},
        'format'         :{'data_type': 'varchar(50)'},
        },
    }
interaction_messages = database_table_class('interaction_messages', database_schema, interaction_messages_table_definition, moduleObj, user='', password='')
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 

# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 
database_schema.finish_loading()

# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 
time_end = datetime.datetime.now()
diff = time_end - time_start  #this is a timedelta obj
duration = diff.days * 24 * 60 * 60 + diff.seconds
msg = f'[{database_schema.reference}] version {database_schema.version} loaded with [[{len(database_schema.tables)} tables]] in [[[{duration} seconds]]].'
log_message(msg, msgType='OK', msgColor=module_color, print_enabled=True, filelog_enabled=True)

log_module_initialization_message(module_identityDictionary)
#::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
#::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
#::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
print('===========================================')
print(database_schema.sqlalchemy_table_classes_def)
print('===========================================')
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