from sqlalchemy import create_engine
from sqlalchemy import MetaData
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from _onlineApp import thisApp
from _onlineApp import log_message,get_debug_option_as_level
colors = thisApp.Fore

import _database_ganimides_model as db_model
from _database_class_table import leandroutechnologyforward_database_table_class as db_table_class
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 
from _database_ganimides_engine import engine,engine_session
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 
import _database_adminServices as dbadmin
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 

#::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
#::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
#::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
# globals
#::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
#::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
#::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
try:
    silent = thisApp.application_configuration.database_schema_silent_loading
except:
    silent = False
#::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
try:
    debug_level1 = get_debug_option_as_level(thisApp.application_configuration.database_models_debug)
except:
    debug_level1 = -1
try:
    debug_level2 = get_debug_option_as_level(thisApp.application_configuration.database_debug)
except:
    debug_level2 = -1
try:
    debug_level3 = get_debug_option_as_level(thisApp.application_configuration.database_tables_debug)
except:
    debug_level3 = -1
try:
    debug_level4 = get_debug_option_as_level(thisApp.application_configuration.database_engine_debug)
except:
    debug_level4 = -1
silent_debug = (not (silent))
silent_debug_level = get_debug_option_as_level(silent_debug)

debug_level = max(debug_level1, debug_level2, debug_level3, debug_level4, silent_debug_level)
#::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
# database_provider=f"sqlite:///"
# database_folder_path=f"C:\\Users\\User\\Documents\\my Projects\\Systems_Development\\Development_Environment"
# database_file_name=f"ganimides.db"
# database_uri=f"{database_provider}{database_folder_path}\\{database_file_name}"
# engine = create_engine(database_uri,echo=False)
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 
# meta = MetaData()
# meta.create_all(engine)
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 
# Session = sessionmaker(bind=engine)
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 
# session = Session()
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 
db_schema_Base = db_model.Base
db_schema={}
USERS_TABLE = db_table_class(db_model.USER, db_model.Base, db_schema, engine, engine_session.session, debug=None)
SUBSCRIPTIONS_TABLE = db_table_class(db_model.SUBSCRIPTION, db_model.Base, db_schema, engine, engine_session.session, debug=None)
APIS_TABLE = db_table_class(db_model.API, db_model.Base, db_schema, engine, engine_session.session, debug=None)
APPLICATIONS_TABLE = db_table_class(db_model.APPLICATION, db_model.Base, db_schema, engine, engine_session.session, debug=None)
CLIENTS_TABLE = db_table_class(db_model.CLIENT, db_model.Base, db_schema, engine, engine_session.session, debug=None)
#SERVICE_PROVIDERS_TABLE = db_table_class(db_model.SERVICE_PROVIDER, db_model.Base, db_schema, engine, engine_session.session, debug=None)
REGISTERED_APIS_TABLE = db_table_class(db_model.APPLICATION_API, db_model.Base, db_schema, engine, engine_session.session, debug=None)
TOKENS_TABLE = db_table_class(db_model.TOKEN, db_model.Base, db_schema, engine, engine_session.session, debug=None)
MERCHANTS_TABLE = db_table_class(db_model.MERCHANT, db_model.Base, db_schema, engine, engine_session.session, debug=None)
POINTS_OF_SALE_TABLE = db_table_class(db_model.POINT_OF_SALE, db_model.Base, db_schema, engine, engine_session.session, debug=None)
MERCHANT_EMPLOYEES_TABLE = db_table_class(db_model.MERCHANT_EMPLOYEE, db_model.Base, db_schema, engine, engine_session.session, debug=None)
CONSUMERS_TABLE = db_table_class(db_model.CONSUMER, db_model.Base, db_schema, engine, engine_session.session, debug=None)
BANKS_TABLE = db_table_class(db_model.BANK, db_model.Base, db_schema, engine, engine_session.session, debug=None)
BANK_SUBSCRIPTIONS_TABLE = db_table_class(db_model.BANK_SUBSCRIPTION, db_model.Base, db_schema, engine, engine_session.session, debug=None)
BANK_AUTHORIZATIONS_TABLE = db_table_class(db_model.BANK_AUTHORIZATION, db_model.Base, db_schema, engine, engine_session.session, debug=None)
BANK_ACCOUNTS_TABLE = db_table_class(db_model.BANK_ACCOUNT, db_model.Base, db_schema, engine, engine_session.session, debug=None)
DEVICES_TABLE = db_table_class(db_model.DEVICE, db_model.Base, db_schema, engine, engine_session.session, debug=None)
DEVICE_USAGE_TABLE = db_table_class(db_model.DEVICE_USAGE, db_model.Base, db_schema, engine, engine_session.session, debug=None)
CLIENT_DEVICES_TABLE = db_table_class(db_model.CLIENT_DEVICE, db_model.Base, db_schema, engine, engine_session.session, debug=None)
INTERACTIONS_TABLE = db_table_class(db_model.INTERACTION, db_model.Base, db_schema, engine, engine_session.session, debug=None)
INTERACTIONS_MESSAGE_TABLE = db_table_class(db_model.INTERACTION_MESSAGE, db_model.Base, db_schema, engine, engine_session.session, debug=None)
DEPARTMENTS_TABLE = db_table_class(db_model.DEPARTMENT, db_model.Base, db_schema, engine, engine_session.session, debug=None)
EMPLOYEES_TABLE = db_table_class(db_model.EMPLOYEE, db_model.Base, db_schema, engine, engine_session.session, debug=None)
DEPARTMENT_EMPLOYEE_LINKS_TABLE = db_table_class(db_model.DEPARTMENT_EMPLOYEE_LINK, db_model.Base, db_schema, engine, engine_session.session, debug=None)
TEST_TABLE = db_table_class(db_model.TEST, db_model.Base, db_schema, engine, engine_session.session, debug=None)
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 
t = 0
r = 0
for table_name in db_schema:
    tableObj = db_schema.get(table_name)
    if tableObj:
        t = t + 1
        try:
            dbadmin.check_table(tableObj, auto_synchronize=True, synchronization_method='add-columns', copy_records=True, silent=silent)
        except:
            try:
                dbadmin.check_table(tableObj, auto_synchronize=True, synchronization_method='drop-create', copy_records=True, silent=silent)
            except:
                try:
                    dbadmin.check_table(tableObj, auto_synchronize=True, synchronization_method='recreate', copy_records=True, silent=silent)
                except:
                    msg=f"database [ganimides] table [[{table_name}]]#ERROR# Synchronization FAILED. #RESET#"
                    log_message(msg)
        r = r + tableObj.rowCount()

dbadmin.recreate_tables(db_schema_Base,engine,debug_level)

msg=f"database [ganimides] [[[[tables schema loaded with]]]] [[{t} tables]] and [{r} rows]"
if thisApp.CONSOLE_ON:
    log_message(msg)
else:
    log_message(msg)
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 