import os
import sys
if not (os.path.dirname(__file__) in sys.path): sys.path.append(os.path.dirname(__file__))

module_ProgramName = os.path.splitext(os.path.basename(__file__))[0]
module_id = '{}'.format(module_ProgramName)
module_version = 0.1

# thisfolder =os.path.dirname(__file__)
# module_id = os.path.basename(thisfolder)
# module_version = 0.1

# from sqlalchemy import create_engine
# from sqlalchemy import MetaData
# from sqlalchemy.ext.declarative import declarative_base
# from sqlalchemy.orm import sessionmaker

from _onlineApp import thisApp
from _onlineApp import log_message

from _database_ganimides_schema import db_schema
from _database_ganimides_engine import engine_session
session = engine_session.session
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 
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
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 
# schema_dictionary={}
# clients = dbtable(schema_dictionary, session, dbmodel.CLIENT, 'clients', 'client')
# users = dbtable(schema_dictionary, session,dbmodel.Users,'users','user')
# apis = dbtable(schema_dictionary, session,dbmodel.API,'apis','api')
# applications = dbtable(schema_dictionary, session,dbmodel.APPLICATION,'applications','application')
# registered_apis = dbtable(schema_dictionary, session,dbmodel.APPLICATION_API,'registered apis','registered api')
# tokens = dbtable(schema_dictionary, session,dbmodel.tokens,'tokens','token')
# merchants = dbtable(schema_dictionary, session,dbmodel.MERCHANT,'merchants','merchant')
# points_of_sale = dbtable(schema_dictionary, session,dbmodel.POINT_OF_SALE,'points_of_sale','point_of_sale')
# merchant_employees = dbtable(schema_dictionary, session,dbmodel.MERCHANT_EMPLOYEE,'merchant_employees','employee')
# consumers = dbtable(schema_dictionary, session,dbmodel.CONSUMER,'consumers','consumer')
# banks = dbtable(schema_dictionary, session,dbmodel.BANK,'banks','bank')
# bank_subscriptions = dbtable(schema_dictionary, session,dbmodel.BANK_SUBSCRIPTION,'bank_subscriptions','bank_subscription')
# bank_authorizations = dbtable(schema_dictionary, session,dbmodel.BANK_AUTHORIZATION,'bank_authorizations','bank_authorization')
# BANK_ACCOUNTS = dbtable(schema_dictionary, session,dbmodel.BANK_ACCOUNT,'BANK_ACCOUNTS','bank_account')
# devices = dbtable(schema_dictionary, session,dbmodel.DEVICE,'devices','device')
# device_usage = dbtable(schema_dictionary, session, dbmodel.DEVICE_USAGE, 'device_usage', 'device_usage')
# client_devices = dbtable(schema_dictionary, session,dbmodel.CLIENT_DEVICE,'client_devices','client_device')
# interactions = dbtable(schema_dictionary, session,dbmodel.INTERACTION,'interactions','interaction')
# interaction_messages = dbtable(schema_dictionary, session, dbmodel.INTERACTION_MESSAGE, 'interaction_messages', 'interaction_message')
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 
# t = 0
# r = 0
# for table_alias in schema_dictionary:
#     tableObj = schema_dictionary.get(table_alias)
#     if tableObj:
#         t = t + 1
#         r = r + tableObj.table_rows 
# msg = f"database [ganimides] loaded"
msg = f'database [ganimides] [[[[module [{module_id}] loaded]]]] with [[version {module_version}]]'
if thisApp.CONSOLE_ON:
    log_message(msg)
else:
    log_message(msg)
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 
