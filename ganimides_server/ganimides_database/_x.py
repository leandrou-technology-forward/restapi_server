def dbapi_TEST_action(input_dict, action='', filter_dict={}):
    return db_table_action(TEST, input_dict, action, filter_dict, 'dbapi_TEST_action','TEST')
#::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
def dbapi_API_action(input_dict, action='', filter_dict={}):
    return db_table_action(API, input_dict, action, filter_dict, 'dbapi_API_action','API')
#::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
def dbapi_API_REGISTERED_action(input_dict, action='', filter_dict={}):
    return db_table_action(APPLICATION_API, input_dict, action, filter_dict, 'dbapi_API_REGISTERED_action','APPLICATION_API')
#::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
def dbapi_APPLICATION_action(input_dict, action='', filter_dict={}):
    return db_table_action(APPLICATION, input_dict, action, filter_dict, 'dbapi_APPLICATION_action','APPLICATION')
#::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
def dbapi_TOKEN_action(input_dict, action='', filter_dict={}):
    return db_table_action(TOKEN, input_dict, action, filter_dict, 'dbapi_TOKEN_action','TOKEN')
#::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
def dbapi_DEVICE_action(input_dict, action='', filter_dict={}):
    return db_table_action(DEVICE, input_dict, action, filter_dict, 'dbapi_DEVICE_action','DEVICE')
#::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
def dbapi_DEVICE_USAGE_action(input_dict, action='', filter_dict={}):
    return db_table_action(DEVICE_USAGE, input_dict, action, filter_dict, 'dbapi_DEVICE_USAGE_action','DEVICE_USAGE')
#::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
def dbapi_USER_action(input_dict, action='', filter_dict={}):
    return db_table_action(USERS, input_dict, action, filter_dict, 'dbapi_USER_action','USERS')
#::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
def dbapi_CLIENT_action(input_dict, action='', filter_dict={}):
    return db_table_action(CLIENT, input_dict, action, filter_dict, 'dbapi_CLIENT_action','CLIENT')
#::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
def dbapi_CLIENT_DEVICE_action(input_dict, action='', filter_dict={}):
    return db_table_action(CLIENT_DEVICE, input_dict, action, filter_dict, 'dbapi_CLIENT_DEVICE_action','CLIENT_DEVICE')
#::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
def dbapi_MERCHANT_action(input_dict, action='', filter_dict={}):
    return db_table_action(MERCHANT, input_dict, action, filter_dict, 'dbapi_MERCHANT_action','MERCHANT')
#::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
def dbapi_merchant_pointofsale_action(input_dict, action='', filter_dict={}):
    return db_table_action(POINT_OF_SALE, input_dict, action, filter_dict, 'dbapi_merchant_pointofsale_action','POINT_OF_SALE')
#::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
def dbapi_MERCHANT_EMPLOYEE_action(input_dict, action='', filter_dict={}):
    return db_table_action(MERCHANT_EMPLOYEE, input_dict, action, filter_dict, 'dbapi_MERCHANT_EMPLOYEE_action','MERCHANT_EMPLOYEE')
#::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
def dbapi_CONSUMER_action(input_dict, action='', filter_dict={}):
    return db_table_action(CONSUMER, input_dict, action, filter_dict, 'dbapi_CONSUMER_action','CONSUMER')
#::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
def dbapi_INTERACTION_action(input_dict, action='', filter_dict={}):
    return db_table_action(INTERACTION, input_dict, action, filter_dict, 'dbapi_INTERACTION_action','INTERACTION')
#::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
def dbapi_INTERACTION_MESSAGE_action(input_dict, action='', filter_dict={}):
    return db_table_action(INTERACTION_MESSAGE, input_dict, action, filter_dict, 'dbapi_INTERACTION_MESSAGE_action','INTERACTION_MESSAGE')
#::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
def dbapi_BANK_action(input_dict, action='', filter_dict={}):
    return db_table_action(BANK, input_dict, action, filter_dict, 'dbapi_BANK_action','BANK')
#::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
def dbapi_BANK_AUTHORIZATION_action(input_dict, action='', filter_dict={}):
    return db_table_action(BANK_AUTHORIZATION, input_dict, action, filter_dict, 'dbapi_BANK_AUTHORIZATION_action','BANK_AUTHORIZATION')
#::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
def dbapi_BANK_SUBSCRIPTION_action(input_dict, action='', filter_dict={}):
    return db_table_action(BANK_SUBSCRIPTION, input_dict, action, filter_dict, 'dbapi_BANK_SUBSCRIPTION_action','BANK_SUBSCRIPTION')
#::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
def dbapi_BANK_ACCOUNT_action(input_dict, action='', filter_dict={}):
    return db_table_action(BANK_ACCOUNT, input_dict, action, filter_dict, 'dbapi_BANK_ACCOUNT_action','BANK_ACCOUNT')
#::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
