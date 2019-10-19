from sqlalchemy import create_engine
from sqlalchemy import MetaData
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from _onlineApp import thisApp
from _onlineApp import log_message
colors = thisApp.Fore

import _database_ganimides_model as db_model
from _database_class_table import leandroutechnologyforward_database_table_class as db_table
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 
from _database_ganimides_engine import db_session
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
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 
db_schema={}
TEST = db_table(db_schema, db_session, db_model.TEST, 'test', 'test')
CLIENTS = db_table(db_schema, db_session, db_model.CLIENT, 'clients', 'client')
USERS = db_table(db_schema, db_session,db_model.Users,'users','user')
APIS = db_table(db_schema, db_session,db_model.API,'apis','api')
APPLICATIONS = db_table(db_schema, db_session,db_model.APPLICATION,'applications','application')
REGISTERED_APIS = db_table(db_schema, db_session,db_model.APPLICATION_API,'registered apis','registered api')
TOKENS = db_table(db_schema, db_session,db_model.TOKEN,'tokens','token')
MERCHANTS = db_table(db_schema, db_session,db_model.MERCHANT,'merchants','merchant')
POINTS_OF_SALES = db_table(db_schema, db_session,db_model.POINT_OF_SALE,'points_of_sale','point_of_sale')
MERCHANT_EMPLOYEES = db_table(db_schema, db_session,db_model.MERCHANT_EMPLOYEE,'merchant_employees','employee')
CONSUMERS = db_table(db_schema, db_session,db_model.CONSUMER,'consumers','consumer')
BANKS = db_table(db_schema, db_session,db_model.BANK,'banks','bank')
BANK_SUBSCRIPTIONS = db_table(db_schema, db_session,db_model.BANK_SUBSCRIPTION,'bank_subscriptions','bank_subscription')
BANK_AUTHORIZATIONS = db_table(db_schema, db_session,db_model.BANK_AUTHORIZATION,'bank_authorizations','bank_authorization')
BANK_ACCOUNTS = db_table(db_schema, db_session,db_model.BANK_ACCOUNT,'BANK_ACCOUNTS','bank_account')
DEVICES = db_table(db_schema, db_session,db_model.DEVICE,'devices','device')
DEVICE_USAGE = db_table(db_schema, db_session, db_model.DEVICE_USAGE, 'device_usage', 'device_usage')
CLIENT_DEVICES = db_table(db_schema, db_session,db_model.CLIENT_DEVICE,'client_devices','client_device')
INTERACTIONS = db_table(db_schema, db_session,db_model.INTERACTION,'interactions','interaction')
INTERACTION_MESSAGES = db_table(db_schema, db_session, db_model.INTERACTION_MESSAGE, 'interaction_messages', 'interaction_message')
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 
t = 0
r = 0
for table_alias in db_schema:
    tableObj = db_schema.get(table_alias)
    if tableObj:
        t = t + 1
        r = r + tableObj.table_rows 
msg=f"database tables schema [ganimides] loaded with [[{t} tables]] and [{r} rows]"
if thisApp.CONSOLE_ON:
    log_message(msg)
else:
    log_message(msg)
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 