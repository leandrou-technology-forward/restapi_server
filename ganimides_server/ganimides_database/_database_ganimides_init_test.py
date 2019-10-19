# -*- coding: utf-8 -*-
#
import os
import sys
if not (os.path.dirname(os.path.dirname(os.path.dirname(__file__))) in sys.path): sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))
if not (os.path.dirname(os.path.dirname(__file__)) in sys.path): sys.path.append(os.path.dirname(os.path.dirname(__file__)))
if not (os.path.dirname(__file__) in sys.path): sys.path.append(os.path.dirname(__file__))

import datetime
import time
import random

from _onlineApp import thisApp
from _onlineApp import build_process_signature, build_process_call_area, get_debug_level, get_debug_files
from _onlineApp import log_process_start, log_process_finish, log_process_message
from _onlineApp import Fore

import _database_ganimides_schema as db
import _database_ganimides_api as dbapi
import _database_adminServices as dbadmin
import _database_ganimides_engine as dbengine
import _database_ganimides_model as dbmodel
from ganimides_server import client_banksubscription_register
from ganimides_server import merchant_banksubscription_register
from ganimides_server import banksubscription_receive_authorization_from_client

module_id='dummy'
caller_area={'debug_level':-1,'debug_template':'SESSION_ONLY'}
caller_area={'debug_level':-1,'debug_template':'FULL'}
caller_area = {'debug_level': 0, 'caller_area_input_debug': False,}
#::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
#::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
#::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
#::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
def recreate_tables():
    for table_name in db.db_schema:
        tableObj = db.db_schema.get(table_name)
        if tableObj:
            dbadmin.check_table(tableObj,auto_synchronize=True,synchronization_method='drop',copy_records=True,silent=True)
    dbadmin.recreate_tables(db.db_schema_Base,db.engine)
    for table_name in db.db_schema:
        tableObj = db.db_schema.get(table_name)
        if tableObj:
            tableObj.delete_rows()
#::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
def clear_tables():
    db.APIS.clear_table()
    db.REGISTERED_APIS.clear_table()
    db.APPLICATIONS.clear_table()
    db.TOKENS.clear_table()
    db.CLIENTS.clear_table()
    db.CLIENT_DEVICES.clear_table()
    db.MERCHANTS.clear_table()
    db.POINTS_OF_SALE.clear_table()
    db.MERCHANT_EMPLOYEES.clear_table()
    db.SUBSCRIPTIONS.clear_table()
    db.BANKS.clear_table()
    # db.BANK_AUTHORIZATIONS.clear_table()
    # db.BANK_SUBSCRIPTIONS.clear_table()
    # db.BANK_ACCOUNTS.clear_table()
    db.DEVICES.clear_table()
    db.DEVICE_USAGE.clear_table()
    db.INTERACTIONS.clear_table()
    db.INTERACTION_MESSAGES.clear_table()
#::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
#::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
#::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
#::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
def create_users():
    print(f'{Fore.LIGHTWHITE_EX}users:')
    start_time=datetime.datetime.now()

    dbsession = dbengine.get_dbsession(**_process_call_area)
    users=[
        {'name': 'alphabetagama','email':'xyx@gmail.com','mobile':'998219999'},
        {'name': 'abc','email':'abc@gmail.com','mobile':'189999'},
        {'name': 'natasha','email':'natasha@gmail.com','mobile':'2894444999'},
        {'name': 'ghi','email':'ghi@gmail.com','mobile':'389999'},
        {'name': 'aaaaaaadef','email':'def@gmail.com','mobile':'289999'},
        {'name': 'def','email':'def@gmail.com','mobile':'25799289999'},
    ]
    for ix in range(0, len(users)):
        user_record=users[ix]
        res = dbapi.dbapi_user(dbsession, 'register', user_record, caller_area=_process_call_area)
        res = dbapi.dbapi_user(dbsession, 'confirm', user_record, caller_area=_process_call_area)

    users=[
        {'name': 'bell','email':'bell@gmail.com','mobile':'998219999'},
        {'name': 'scroedinger','email':'schroedinger@gmail.com','mobile':'189999'},
        {'name': 'bohr','email':'bohr@gmail.com','mobile':'2894444999'},
    ]
    for ix in range(0, len(users)):
        user_record=users[ix]
        res = dbapi.dbapi_user(dbsession, 'register', user_record, caller_area=_process_call_area)
        # res = dbapi.dbapi_user(dbsession, 'confirm', user_record, caller_area=_process_call_area)

    dbsession.close(**_process_call_area)

    diff = datetime.datetime.now() - start_time
    duration = diff.days * 24 * 60 * 60 + diff.seconds
    print(f'{Fore.MAGENTA}duration :',duration)           
#::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
def create_apis():
    print(f'{Fore.LIGHTWHITE_EX}apis:')
    start_time=datetime.datetime.now()

    #dbadmin.clear_table(db.APIS_TABLE,silent=False)

    dbsession = dbengine.get_dbsession(debug=0,**_process_call_area)
    dbapi.dbapi_api(dbsession, 'refresh', {'api_name':'bobbi'},caller_area=_process_call_area)
    dbapi.dbapi_api(dbsession, 'refresh', {'api_name':'shalimar'})
    dbapi.dbapi_api(dbsession, 'refresh', {'api_name':'heidi'})
    dbapi.dbapi_api(dbsession, 'refresh', {'api_name':'rain'})
    dbapi.dbapi_api(dbsession, 'refresh', {'api_name':'natasha'})

    dbsession.close(**_process_call_area)

    diff = datetime.datetime.now() - start_time
    duration = diff.days * 24 * 60 * 60 + diff.seconds
    print(f'{Fore.MAGENTA}duration :',duration)           
#::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
def create_subscriptions():
    print(f'{Fore.LIGHTWHITE_EX}subscriptions:')
    start_time=datetime.datetime.now()
    
    dbsession = dbengine.get_dbsession(**_process_call_area)
    user_rec={'email': 'xyx@gmail.com'}
    user = dbsession.get(dbmodel.USER, user_rec, caller_area=_process_call_area)
    if not user:
        user_id = ''
    else:
        user_id = user.user_id
    subs_record = {'user_id': user_id, 'name': 'bell', 'email': 'bell@gmail.com', 'mobile': '998sss219999'}
    res = dbapi.dbapi_subscription(dbsession, 'register', subs_record, caller_area=_process_call_area)
    if res.get('api_status') == 'success':
        subscription_rec = res.get('api_data')
        if not subscription_rec.get('status')=='Active':
            res = dbapi.dbapi_subscription(dbsession, 'confirm', subscription_rec, caller_area=_process_call_area)

    subscribers=[
        {'name': 'bell','email':'bell@gmail.com','mobile':'998219999'},
        {'name': 'scroedinger','email':'schroedinger@gmail.com','mobile':'189999'},
        {'name': 'bohr','email':'bohr@gmail.com','mobile':'2894444999'},
        {'name': 'alphabetagama','email':'xyx@gmail.com','mobile':'998219999'},
        {'name': 'abc','email':'abc@gmail.com','mobile':'189999'},
        {'name': 'natasha','email':'natasha@gmail.com','mobile':'2894444999'},
        {'name': 'ghi','email':'ghi@gmail.com','mobile':'389999'},
        {'name': 'aaaaaaadef','email':'def@gmail.com','mobile':'289999'},
        {'name': 'def','email':'def@gmail.com','mobile':'25799289999'},
    ]
    for ix in range(0, len(subscribers)):
        subs_record=subscribers[ix]
        user_rec=subs_record
        user = dbsession.refresh(dbmodel.USER, user_rec, caller_area=_process_call_area)
        if not user:
            user_id = ''
        else:
            user_id = user.user_id
        
        subs_record.update({'user_id': user_id})
        res = dbapi.dbapi_subscription(dbsession, 'register', subs_record, caller_area=_process_call_area)
        if res.get('api_status') == 'success':
            subscription_rec = res.get('api_data')
            if not subscription_rec.get('status')=='Active':
                res = dbapi.dbapi_subscription(dbsession, 'confirm', subscription_rec, caller_area=_process_call_area)
        
    dbsession.close(**_process_call_area)

    diff = datetime.datetime.now() - start_time
    duration = diff.days * 24 * 60 * 60 + diff.seconds
    print(f'{Fore.MAGENTA}duration :',duration)           
#::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
def add_applications():
    print(f'{Fore.LIGHTWHITE_EX}applications:')
    start_time=datetime.datetime.now()


    dbsession = dbengine.get_dbsession(**_process_call_area)
    subscription_id = dbsession.get(dbmodel.SUBSCRIPTION, {'email': 'abc@gmail.com'}).subscription_id
    print('subscription_id:',subscription_id)

    app_record = {'application_name': 'scanandpay', 'application_email': 'ppssdfcfffox2ds.leandrou@outlook.com', 'subscription_id': subscription_id}
    res = dbapi.dbapi_application(dbsession, 'register', app_record, caller_area=_process_call_area)

    client_id = dbsession.get(dbmodel.CLIENT, {'email': 'schroedinger@gmail.com'}).client_id
    print('client_id:',client_id)

    app_record = {'application_name': 'scanandpay_client', 'application_email': 'ppstestsdfcfffox2ds.leandrou@outlook.com', 'client_id': client_id}
    res = dbapi.dbapi_application(dbsession, 'register', app_record, caller_area=_process_call_area)

    app_record = {'application_name': 'scanandpay_merchant', 'application_email': 'test111ppssdfcfffox2ds.leandrou@outlook.com', 'client_id': client_id}
    res = dbapi.dbapi_application(dbsession, 'register',app_record, caller_area=_process_call_area)

    app_record = {'application_name': 'scanandpay_bobbi', 'application_email': 'ppssdfcfffox2ds.leandrou@outlook.com', 'client_id': client_id}
    res = dbapi.dbapi_application(dbsession, 'register',app_record, caller_area=_process_call_area)

    client_id = dbsession.get(dbmodel.CLIENT, {'client_type': 'subscriber', 'email': 'ghi@gmail.com'}).client_id
    print('client_id:', client_id)
    app_record = {'application_name': 'directpay', 'application_email': 'ccccccffox2ds.leandrou@outlook.com', 'client_id': client_id}
    res = dbapi.dbapi_application(dbsession, 'register',app_record, caller_area=_process_call_area)

    app_record = {'application_name': 'scanandpay', 'application_email': 'ccccccffox2ds.leandrou@outlook.com', 'client_id': client_id}
    res = dbapi.dbapi_application(dbsession, 'register',app_record, caller_area=_process_call_area)

    app_record = {'application_name': 'directpay_merchant', 'application_email': 'ccccccffox2ds.leandrou@outlook.com', 'client_id': client_id}
    res = dbapi.dbapi_application(dbsession, 'register',app_record, caller_area=_process_call_area)
    app_record = {'application_name': 'beerhub', 'application_email': 'ccccccffox2ds.leandrou@outlook.com', 'client_id': client_id}
    res = dbapi.dbapi_application(dbsession, 'register',app_record, caller_area=_process_call_area)

    client_id = dbsession.get(dbmodel.CLIENT, {'client_type': 'subscriber', 'email': 'def@gmail.com'}).client_id
    print('client_id:', client_id)
    app_record = {'application_name': 'shalimar', 'application_email': 'ppssdfcfffox2ds.leandrou@outlook.com', 'client_id': client_id}
    res = dbapi.dbapi_application(dbsession, 'register',app_record, caller_area=_process_call_area)

    client_id = dbsession.get(dbmodel.CLIENT, {'client_type': 'subscriber', 'email': 'ghi@gmail.com'}).client_id
    print('client_id:',client_id)
    app_record = {'application_name': 'bobbistar', 'application_email': 'ppssdfcfffox2ds.leandrou@outlook.com', 'client_id': client_id}
    res = dbapi.dbapi_application(dbsession, 'register',app_record, caller_area=_process_call_area)
    app_record = {'application_name': 'letticia', 'application_email': 'ppssdfcfffox2ds.leandrou@outlook.com', 'client_id': client_id}
    res = dbapi.dbapi_application(dbsession, 'register',app_record, caller_area=_process_call_area)

    dbsession.close(**_process_call_area)

    diff = datetime.datetime.now() - start_time
    duration = diff.days * 24 * 60 * 60 + diff.seconds
    print(f'{Fore.MAGENTA}duration :',duration)           
#::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
def add_application_admin_users():
    print(f'{Fore.LIGHTWHITE_EX}application admin users:')
    start_time=datetime.datetime.now()

    dbsession = dbengine.get_dbsession(**_process_call_area)
    apps = dbsession.get_rows(dbmodel.APPLICATION, {}, output_method='DICT', caller_area=_process_call_area)
    for ix1 in range(0, len(apps)):
        app = apps[ix1]
        email='e'+str(random.randint(1000,2000))+'@gmail.com'
        rec={'application_name':app.get('application_name'),'email':email,'user_role':'admin'}
        res = dbapi.dbapi_application_USER(dbsession, 'register',rec, caller_area=_process_call_area)

    dbsession.close(**_process_call_area)

    diff = datetime.datetime.now() - start_time
    duration = diff.days * 24 * 60 * 60 + diff.seconds
    print(f'{Fore.MAGENTA}duration :',duration)           
#::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
def add_application_templates():
    print(f'{Fore.LIGHTWHITE_EX}application templates:')
    start_time=datetime.datetime.now()

    dbsession = dbengine.get_dbsession(**_process_call_area)
    apps = dbsession.get_rows(dbmodel.APPLICATION, {}, output_method='DICT', caller_area=_process_call_area)
    for ix1 in range(0, len(apps)):
        app = apps[ix1]

        template = {'application_name':app.get('application_name'), 'template_name': 'mobile_confirmation_sms', 'language': 'En',
        'text':'your otp to confirm your mobile is #OTP#. click #CONFIRMATION_URL#'}
        res=dbapi.dbapi_application_template(dbsession,'refresh',template,caller_area=_process_call_area)

        template = {'application_name':app.get('application_name'), 'template_name': 'mobile_confirmation_sms', 'language': 'Gr',
        'text':'ο κωδικός για επιβεβεβαιωση του κινητου σας ειναι: #OTP#. πατηστε #CONFIRMATION_URL#'}
        res=dbapi.dbapi_application_template(dbsession,'refresh',template,caller_area=_process_call_area)

        template = {'application_name': app.get('application_name'), 'template_name': 'email_confirmation_email', 'language': 'Gr',
        'subject':'επιβεβεβαιωση email','text': 'επιβεβεβαιωστε το email σας. click #CONFIRMATION_URL#','html':''}
        db.dbapi_application_template(dbsession,'refresh',template,caller_area=_process_call_area)

        template = {'application_name': app.get('application_name'), 'template_name': 'email_confirmation_email', 'language': 'En',
        'subject':'email confirmation','text': 'confirm your email. click #CONFIRMATION_URL#','html':''}
        db.dbapi_application_template(dbsession,'refresh',template,caller_area=_process_call_area)


    #default
    template = {'application_name':'', 'template_name': 'mobile_confirmation_sms', 'language': 'En',
    'text':'your otp to confirm your mobile is #OTP#. click #CONFIRMATION_URL#'}
    res=dbapi.dbapi_application_template(dbsession,'refresh',template,caller_area=_process_call_area)

    template = {'application_name': '', 'template_name': 'mobile_confirmation_sms', 'language': 'Gr',
    'text':'ο κωδικός για επιβεβεβαιωση του κινητου σας ειναι: #OTP#. πατηστε #CONFIRMATION_URL#'}
    db.dbapi_application_template(dbsession,'refresh',template,caller_area=_process_call_area)

    template = {'application_name': '', 'template_name': 'email_confirmation_email', 'language': 'Gr',
    'subject':'επιβεβεβαιωση email','text': 'επιβεβεβαιωστε το email σας. click #CONFIRMATION_URL#','html':''}
    db.dbapi_application_template(dbsession,'refresh',template,caller_area=_process_call_area)

    template = {'application_name': '', 'template_name': 'email_confirmation_email', 'language': 'En',
    'subject':'email confirmation','text': 'confirm your email. click #CONFIRMATION_URL#','html':''}
    db.dbapi_application_template(dbsession,'refresh',template,caller_area=_process_call_area)

    diff = datetime.datetime.now() - start_time
    duration = diff.days * 24 * 60 * 60 + diff.seconds
    print(f'{Fore.MAGENTA}duration :',duration)           
#::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
def register_apis():
    print(f'{Fore.LIGHTWHITE_EX}api registration:')
    start_time=datetime.datetime.now()


    dbsession = dbengine.get_dbsession(**_process_call_area)

    res = dbapi.dbapi_api(dbsession, 'register',{'application_name': 'scanandpay', 'api_name': 'bobbi'}, caller_area=_process_call_area)

    apis = dbsession.get_rows(dbmodel.API, {}, output_method='DICT', caller_area=_process_call_area)
    apps = dbsession.get_rows(dbmodel.APPLICATION, {}, output_method='DICT', caller_area=_process_call_area)
    for ix1 in range(0, len(apps)):
        app = apps[ix1]
        for ix2 in range(0, len(apis)):
            api = apis[ix2]
            rec={'application_name':app.get('application_name'),'api_name':api.get('api_name')}
            res = dbapi.dbapi_api(dbsession, 'register',rec, caller_area=_process_call_area)

    for ix1 in range(0, len(apps)):
        app = apps[ix1]
        rec={'application_name':app.get('application_name'),'api_name':'natasha'}
        res = dbapi.dbapi_api(dbsession, 'unregister',rec, caller_area=_process_call_area)

    dbsession.close(**_process_call_area)

    diff = datetime.datetime.now() - start_time
    duration = diff.days * 24 * 60 * 60 + diff.seconds
    print(f'{Fore.MAGENTA}duration :',duration)           
#:::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::: 
def add_banks():
    print(f'{Fore.LIGHTWHITE_EX}banks:')
    start_time=datetime.datetime.now()

    device_uid = 'aaabbbcccdddeeefff'
    user = 'spithas'
    geolocation_lat='123.456789'
    geolocation_lon='987.654321'

    dbsession = dbengine.get_dbsession(**_process_call_area)

    banks=[
        {'bank_name': 'HELLENIC BANK','bank_BIC':'HEBACY2N','bank_code':'hellenicbank','bank_short_code':'HB','status':'Active'},
        {'bank_name': 'BANK OF CYPRUS','bank_BIC':'BICACY2N','bank_code':'bankofcyprus','bank_short_code':'BOC','status':'Active'},
        {'bank_name': 'HELLENIC BANK','bank_BIC':'HEBACY2N','bank_code':'hellenicbank','bank_short_code':'HB','status':'Active'},
        {'bank_name': 'HELLENIC BANK','bank_BIC':'HEBACY2N','bank_code':'hellenicbank','bank_short_code':'HB','status':'Active'},
        {'bank_name': 'TSB','bank_BIC':'TSBACY2N','bank_code':'tsbbank','bank_short_code':'TSB','status':'Active'},
        {'bank_name': 'TSB','bank_BIC':'TSBACY2N','bank_code':'tsbbank','bank_short_code':'TSB','status':'TEST'},
    ]
    for ix in range(0, len(banks)):
        bank_record=banks[ix]
        res = dbapi.dbapi_bank(dbsession, 'register', bank_record, caller_area=_process_call_area)
        
    dbsession.close(**_process_call_area)

    diff = datetime.datetime.now() - start_time
    duration = diff.days * 24 * 60 * 60 + diff.seconds
    print(f'{Fore.MAGENTA}duration :',duration)           
#::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
def test_tokens():
    print(f'{Fore.LIGHTWHITE_EX}tokens:')
    start_time=datetime.datetime.now()

    #db.TOKENS.clear_table()
    device_uid = '123232323232323232323'
    user = 'acccc3333'
    geolocation_lat='34.56789'
    geolocation_lon = '31.654321'
    application_name = 'scanandpay_merchant'

    dbsession = dbengine.get_dbsession(**_process_call_area)

    application = dbsession.get(dbmodel.APPLICATION, {'application_name':application_name})
    client_id = application.client_id
    client_secretKey = application.client_secretKey

    dbapi.dbapi_device_log(dbsession, device_uid, application_name, geolocation_lat, geolocation_lon, client_id)

    res = dbapi.dbapi_application_credentials_are_valid(dbsession,application_name, client_id, client_secretKey)
    print('dbapi_application_credentials_are_valid =',res)

    request = {
        'token_type':"bearer",
        'token_scope':"application_service",
        'grant_type':"client_credentials",
        'device_uid': device_uid,
        'geolocation_lat': geolocation_lat,
        'geolocation_lon': geolocation_lon,
        'subscription_id': "",
        'application_name': application_name,
        'application_client_id': client_id,
        'application_client_secretKey': client_secretKey,
        }
    res = dbapi.dbapi_token_get_access_token(dbsession,request)
    print(res)

    token = res.get('api_data',{}).get('token')
    print(f'{Fore.LIGHTWHITE_EX}token =',token)
    request.update({'token': token})
    res = dbapi.dbapi_token_is_valid(dbsession,request)
    print('token_is_valid =', res)        
    dbsession.close(**_process_call_area)
    
    #2nd token    
    print('')
    dbsession = dbengine.get_dbsession(**_process_call_area)
    dbapi.dbapi_device_log(dbsession, device_uid, application_name, geolocation_lat, geolocation_lon, client_id)
    res = dbapi.dbapi_token_get_access_token(dbsession,request)
    #print(res)
    token = res.get('api_data',{}).get('token')
    print('token =',token)
    request.update({'token': token})
    res = dbapi.dbapi_token_is_valid(dbsession,request)
    print('token_is_valid =', res)
    dbsession.close(**_process_call_area)

    # 3rd token    
    print('')
    dbsession = dbengine.get_dbsession(**_process_call_area)
    dbapi.dbapi_device_log(dbsession, device_uid, application_name, geolocation_lat, geolocation_lon, client_id)
    res = dbapi.dbapi_token_get_access_token(dbsession,request)
    #print(res)
    token = res.get('api_data',{}).get('token')
    print('token =',token)
    request.update({'token': token})
    res = dbapi.dbapi_token_is_valid(dbsession,request)
    print('token_is_valid =', res)
    dbsession.close(**_process_call_area)

    # try to make it expired
    print(f'{Fore.LIGHTWHITE_EX}','try to make it expired after 1 minute')
    dbsession = dbengine.get_dbsession(**_process_call_area)
    res = dbapi.dbapi_token_get_access_token(dbsession,request)
    print(res)
    print('')
    token = res.get('api_data',{}).get('token')
    duration_seconds = res.get('api_data',{}).get('duration_seconds')
    expiryDT = res.get('api_data',{}).get('expiryDT')
    print('duration_seconds:',duration_seconds)
    print('expiryDT:',expiryDT)

    request.update({'token': token})
    if 1==2:
        ix=0
        while ix <= 6:
            ix = ix + 1
            time.sleep(10)
            dbapi.dbapi_device_log(dbsession, device_uid, application_name, geolocation_lat, geolocation_lon, client_id)
            res = dbapi.dbapi_token_is_valid(dbsession,request)
            print(ix, 'token_is_valid =', res,datetime.datetime.utcnow())
            if not res:
                break

    dbsession.close(**_process_call_area)

    diff = datetime.datetime.now() - start_time
    duration = diff.days * 24 * 60 * 60 + diff.seconds
    print(f'{Fore.MAGENTA}duration :',duration)           
#::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
def add_merchants():
    print(f'{Fore.LIGHTWHITE_EX}merchants:')
    start_time=datetime.datetime.now()

    device_uid = 'aaabbbcccdddeeefff'
    user = 'spithas'
    geolocation_lat='123.456789'
    geolocation_lon='987.654321'
    application_name = 'directpay_merchant'
    client_id = '?'
    
    dbsession = dbengine.get_dbsession(**_process_call_area)
    merchant_record={'name': 'zorbas bakeries','email':'zorbas@gmail.com','mobile':'89999'}
    dbapi.dbapi_device_log(dbsession, device_uid, application_name, geolocation_lat, geolocation_lon, client_id,caller_area=_process_call_area)
    res=dbapi.dbapi_merchant(dbsession, 'register',merchant_record,caller_area=_process_call_area)
    res=dbapi.dbapi_merchant(dbsession, 'confirm',merchant_record,caller_area=_process_call_area)
    dbsession.close(**_process_call_area)

    dbsession = dbengine.get_dbsession(**_process_call_area)
    merchant_record={'name': 'alpha-mega','email':'alphamega@gmail.com','mobile':'8ddddd9999'}
    dbapi.dbapi_device_log(dbsession, device_uid, application_name, geolocation_lat, geolocation_lon, client_id)
    res=dbapi.dbapi_merchant(dbsession, 'register', merchant_record, caller_area=_process_call_area)
    res=dbapi.dbapi_merchant(dbsession, 'confirm', merchant_record, caller_area=_process_call_area)
    dbsession.close(**_process_call_area)

    dbsession = dbengine.get_dbsession(**_process_call_area)
    merchant_record={'name': 'armenias','email':'armenias@gmail.com','mobile':'8ddxxxddd9999'}
    dbapi.dbapi_device_log(dbsession, device_uid, application_name, geolocation_lat, geolocation_lon, client_id)
    res=dbapi.dbapi_merchant(dbsession, 'register', merchant_record, caller_area=_process_call_area)
    res=dbapi.dbapi_merchant(dbsession, 'confirm', merchant_record, caller_area=_process_call_area)
    dbsession.close(**_process_call_area)

    dbsession = dbengine.get_dbsession(**_process_call_area)
    merchant_record={'name': 'exagono','email':'exagono@gmail.com','mobile':'8qqqddd9999'}
    dbapi.dbapi_device_log(dbsession, device_uid, application_name, geolocation_lat, geolocation_lon, client_id)
    res=dbapi.dbapi_merchant(dbsession, 'register', merchant_record, caller_area=_process_call_area)
    res=dbapi.dbapi_merchant(dbsession, 'confirm', merchant_record, caller_area=_process_call_area)
    dbsession.close(**_process_call_area)

    dbsession = dbengine.get_dbsession(**_process_call_area)
    merchant_record={'name': 'metro','email':'metro@gmail.com','mobile':'8qqqddd99ddd99'}
    dbapi.dbapi_device_log(dbsession, device_uid, application_name, geolocation_lat, geolocation_lon, client_id)
    res=dbapi.dbapi_merchant(dbsession, 'register', merchant_record, caller_area=_process_call_area)
    res=dbapi.dbapi_merchant(dbsession, 'confirm', merchant_record, caller_area=_process_call_area)
    dbsession.close(**_process_call_area)

    dbsession = dbengine.get_dbsession(**_process_call_area)
    merchant_record={'name': 'papantoniou','email':'papantoniou@gmail.com','mobile':'8qqqddd99ddd99'}
    dbapi.dbapi_device_log(dbsession, device_uid, application_name, geolocation_lat, geolocation_lon, client_id)
    res=dbapi.dbapi_merchant(dbsession, 'register', merchant_record, caller_area=_process_call_area)
    res=dbapi.dbapi_merchant(dbsession, 'confirm', merchant_record, caller_area=_process_call_area)

    dbsession.close(**_process_call_area)

    diff = datetime.datetime.now() - start_time
    duration = diff.days * 24 * 60 * 60 + diff.seconds
    print(f'{Fore.MAGENTA}duration :',duration)           
#:::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::: 
def add_retail_stores():
    print(f'{Fore.LIGHTWHITE_EX}retail stores:')
    start_time=datetime.datetime.now()

    device_uid = 'aaabbbcccdddeeefff'
    user = 'spithas'
    geolocation_lat='123.456789'
    geolocation_lon='987.654321'
    application_name = 'directpay_merchant'
    client_id = '?'
    # _process_call_area.update({'debug_level':0})
    dbsession = dbengine.get_dbsession(**_process_call_area)
    merchants = dbsession.get_rows(dbmodel.MERCHANT, {}, output_method='DICT', caller_area=_process_call_area)
    for ix1 in range(0, len(merchants)):
        merchant = merchants[ix1]
        for ix2 in range(0, 3):
            store_name='store_'+str(ix2)+'_'+merchant.get('name','')
            geolocation_lat='123.456789'
            geolocation_lon='987.654321'

            n1 = random.randint(1, 101)
            n2 = random.randint(1000000, 9999999)
            geolocation_lat = str(n1) + '.' + str(n2)
            
            n1 = random.randint(1, 101)
            n2 = random.randint(1000000, 9999999)
            geolocation_lon = str(n1) + '.' + str(n2)

            store_rec = {'name': store_name, 'merchant_id': merchant.get('merchant_id'), 'geolocation_lat': geolocation_lat, 'geolocation_lon': geolocation_lon}
            
            res = dbapi.dbapi_retail_store(dbsession, 'register', store_rec, caller_area=_process_call_area)

    dbsession.close(**_process_call_area)

    diff = datetime.datetime.now() - start_time
    duration = diff.days * 24 * 60 * 60 + diff.seconds
    print(f'{Fore.MAGENTA}duration :',duration)           
#:::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::: 
def add_pointofsales():
    print(f'{Fore.LIGHTWHITE_EX}points of sale:')
    start_time=datetime.datetime.now()

    device_uid = '000oooiiiwwwqqqeeefff'
    user = 'spithas'
    geolocation_lat='123.456789'
    geolocation_lon='987.654321'
    application_name = 'directpay_merchant'
    client_id = '?'
    # _process_call_area.update({'debug_level':0})
    dbsession = dbengine.get_dbsession(**_process_call_area)
    merchants = dbsession.get_rows(dbmodel.MERCHANT, {}, output_method='DICT', caller_area=_process_call_area)
    for ix1 in range(0, len(merchants)):
        merchant = merchants[ix1]
        merchant_id=merchant.get('merchant_id')
        stores = dbsession.get_rows(dbmodel.RETAIL_STORE, {'merchant_id':merchant_id}, output_method='DICT', caller_area=_process_call_area)
        for ix2 in range(0, len(stores)):
            store = stores[ix2]
            store_id=store.get('retail_store_id')
            for ix3 in range(0, 3):
                pos_name = 'pos_' + str(ix3) + '_' + store.get('name', '')
                n1 = random.randint(1, 101)
                n2 = random.randint(1000000, 9999999)
                geolocation_lat = str(n1) + '.' + str(n2)
                
                n1 = random.randint(1, 101)
                n2 = random.randint(1000000, 9999999)
                geolocation_lon = str(n1) + '.' + str(n2)

                pos_rec={'name':pos_name,'merchant_id':merchant_id,'retail_store_id':store_id, 'geolocation_lat': geolocation_lat, 'geolocation_lon': geolocation_lon}
                res = dbapi.dbapi_pointofsale(dbsession, 'register', pos_rec, caller_area=_process_call_area)

    dbsession.close(**_process_call_area)

    diff = datetime.datetime.now() - start_time
    duration = diff.days * 24 * 60 * 60 + diff.seconds
    print(f'{Fore.MAGENTA}duration :',duration)           
#:::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::: 
def add_service_points():
    print(f'{Fore.LIGHTWHITE_EX}service points:')
    start_time=datetime.datetime.now()

    device_uid = '000oooiiiwwwqqqeeefff'
    user = 'spithas'
    geolocation_lat='123.456789'
    geolocation_lon='987.654321'
    application_name = 'directpay_merchant'
    client_id = '?'
    # _process_call_area.update({'debug_level':0})
    dbsession = dbengine.get_dbsession(**_process_call_area)
    merchants = dbsession.get_rows(dbmodel.MERCHANT, {}, output_method='DICT', caller_area=_process_call_area)
    for ix1 in range(0, len(merchants)):
        merchant = merchants[ix1]
        merchant_id=merchant.get('merchant_id')
        stores = dbsession.get_rows(dbmodel.RETAIL_STORE, {'merchant_id':merchant_id}, output_method='DICT', caller_area=_process_call_area)
        for ix2 in range(0, len(stores)):
            store = stores[ix2]
            store_id=store.get('retail_store_id')
            for ix9 in range(0, 5):
                point_name = 'table_' + str(ix9)
                n1 = random.randint(1, 101)
                n2 = random.randint(1000000, 9999999)
                geolocation_lat = str(n1) + '.' + str(n2)
                
                n1 = random.randint(1, 101)
                n2 = random.randint(1000000, 9999999)
                geolocation_lon = str(n1) + '.' + str(n2)

                point_rec={'name':point_name,'merchant_id':merchant_id,'retail_store_id':store_id, 'geolocation_lat': geolocation_lat, 'geolocation_lon': geolocation_lon}
                res = dbapi.dbapi_service_point(dbsession, 'register', point_rec, caller_area=_process_call_area)

    dbsession.close(**_process_call_area)

    diff = datetime.datetime.now() - start_time
    duration = diff.days * 24 * 60 * 60 + diff.seconds
    print(f'{Fore.MAGENTA}duration :',duration)           
#:::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::: 
def add_customer_service_assistants():
    print(f'{Fore.LIGHTWHITE_EX}customer service assistants:')
    start_time=datetime.datetime.now()

    device_uid = 'xxxzzzcccvasasasasavvbbbnnnmmm'
    user = 'bobbi'
    geolocation_lat='0212.456789'
    geolocation_lon='0122.654321'

    #_process_call_area.update({'debug_level':0})
    dbsession = dbengine.get_dbsession(**_process_call_area)

    merchants = dbsession.get_rows(dbmodel.MERCHANT, {}, output_method='DICT', caller_area=_process_call_area)
    for ix1 in range(0, len(merchants)):
        merchant = merchants[ix1]
        merchant_id=merchant.get('merchant_id')
        merchant_name=str(merchant.get('name'))
        stores = dbsession.get_rows(dbmodel.RETAIL_STORE, {'merchant_id':merchant_id}, output_method='DICT', caller_area=_process_call_area)
        code=0
        for ix2 in range(0, len(stores)):
            store = stores[ix2]
            store_id=store.get('retail_store_id')
            for ix9 in range(0, 5):
                code = code + 1
                employee_name = 'employee_' + str(code)+' '+merchant_name
                codeStr = '00000' + str(code)
                employee_code='E'+codeStr[-4:]
                mobile=''
                email=employee_name+'@gmail.com'

                employee_rec = {'name': employee_name, 'employee_code': employee_code, 'merchant_id': merchant_id, 'retail_store_id': store_id,'email':email,'mobile':mobile}
                res = dbapi.dbapi_customer_service_assistant(dbsession, 'register', employee_rec, caller_area=_process_call_area)
                # print(ix1, ix2, ix9, employee_code, res.get('api_message'))
                # x=1
                #print(res)

    dbsession.close(**_process_call_area)

    diff = datetime.datetime.now() - start_time
    duration = diff.days * 24 * 60 * 60 + diff.seconds
    print(f'{Fore.MAGENTA}duration :',duration)           
#:::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::: 
def register_merchant_bank_subscriptions():
    print(f'{Fore.LIGHTWHITE_EX}register merchant bank subscription:')
    start_time=datetime.datetime.now()

    #_process_call_area.update({'debug_level':0})
    dbsession = dbengine.get_dbsession(**_process_call_area)
    application_name = 'scanandpay_merchant'
    bank_id='bankofcyprus'
    subscription_options={}
    merchants = dbsession.get_rows(dbmodel.MERCHANT, {}, output_method='', caller_area=_process_call_area)
    for ix1 in range(0, len(merchants)):
        merchant = merchants[ix1]
        merchant_id = merchant.merchant_id
        res = merchant_banksubscription_register(dbsession, merchant_id, application_name, bank_id, subscription_options, caller_area=_process_call_area)
        print(res.get('api_message', '?'))

    #SOS#SOS#SOS#SOS#SOS#SOS#SOS#SOS#SOS#SOS#SOS#SOS#SOS#SOS#
    #SOS#SOS#SOS#SOS#SOS#SOS#SOS#SOS#SOS#SOS#SOS#SOS#SOS#SOS#
    #SOS#SOS#SOS#SOS#SOS#SOS#SOS#SOS#SOS#SOS#SOS#SOS#SOS#SOS#
    _process_call_area.update({'simulation_enabled':True})
    #SOS#SOS#SOS#SOS#SOS#SOS#SOS#SOS#SOS#SOS#SOS#SOS#SOS#SOS#
    #SOS#SOS#SOS#SOS#SOS#SOS#SOS#SOS#SOS#SOS#SOS#SOS#SOS#SOS#
    #SOS#SOS#SOS#SOS#SOS#SOS#SOS#SOS#SOS#SOS#SOS#SOS#SOS#SOS#
    authorization_code='dummy'
    res = banksubscription_receive_authorization_from_client(dbsession, bank_id, authorization_code, caller_area=_process_call_area)
    print(res.get('api_message'))

    dbsession.close(**_process_call_area)

    diff = datetime.datetime.now() - start_time
    duration = diff.days * 24 * 60 * 60 + diff.seconds
    print(f'{Fore.MAGENTA}duration :',duration)           
#::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
def register_client_bank_subscriptions():
    print(f'{Fore.LIGHTWHITE_EX}register client bank subscription:')
    start_time=datetime.datetime.now()

    #_process_call_area.update({'debug_level':0})
    dbsession = dbengine.get_dbsession(**_process_call_area)
    application_name = 'scanandpay_client'
    bank_id='bankofcyprus'
    subscription_options={}
    clients = dbsession.get_rows(dbmodel.CLIENT, {'client_type':'user','status':'Active'}, output_method='', caller_area=_process_call_area)
    for ix1 in range(0, len(clients)):
        client = clients[ix1]
        client_id = client.client_id
        res = client_banksubscription_register(dbsession, client_id, application_name, bank_id, subscription_options, caller_area=_process_call_area)
        print(res.get('api_message', '?'))

       #SOS#SOS#SOS#SOS#SOS#SOS#SOS#SOS#SOS#SOS#SOS#SOS#SOS#SOS#
    #SOS#SOS#SOS#SOS#SOS#SOS#SOS#SOS#SOS#SOS#SOS#SOS#SOS#SOS#
    #SOS#SOS#SOS#SOS#SOS#SOS#SOS#SOS#SOS#SOS#SOS#SOS#SOS#SOS#
    _process_call_area.update({'simulation_enabled':True})
    #SOS#SOS#SOS#SOS#SOS#SOS#SOS#SOS#SOS#SOS#SOS#SOS#SOS#SOS#
    #SOS#SOS#SOS#SOS#SOS#SOS#SOS#SOS#SOS#SOS#SOS#SOS#SOS#SOS#
    #SOS#SOS#SOS#SOS#SOS#SOS#SOS#SOS#SOS#SOS#SOS#SOS#SOS#SOS#
    authorization_code='dummy'
    res=banksubscription_receive_authorization_from_client(dbsession, bank_id, authorization_code,  caller_area=_process_call_area)
    print(res.get('api_message'))

    dbsession.close(**_process_call_area)

    diff = datetime.datetime.now() - start_time
    duration = diff.days * 24 * 60 * 60 + diff.seconds
    print(f'{Fore.MAGENTA}duration :',duration)           
#::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
def add_bank_accounts():
    print(f'{Fore.LIGHTWHITE_EX}merchant bank account:')
    start_time=datetime.datetime.now()

    device_uid = 'aaabbbcccdddeeefff'
    user = 'spithas'
    geolocation_lat='123.456789'
    geolocation_lon='987.654321'

    #_process_call_area.update({'debug_level':0})
    dbsession = dbengine.get_dbsession(**_process_call_area)
    merchants = dbsession.get_rows(dbmodel.MERCHANT, {}, output_method='', caller_area=_process_call_area)
    pointofsales = dbsession.get_rows(dbmodel.POINT_OF_SALE, {}, output_method='', caller_area=_process_call_area)
    accts = ['351012345671', '351092345672', '351012345673', '351012345674']
    if 1 == 2:            
        for ix1 in range(0, len(merchants)):
            merchant = merchants[ix1]
            merchant_id = merchant.merchant_id
            ix2=random.randint(0, len(accts)-1)
            acct = accts[ix2]
            
            acct_rec={
            'merchant_id':merchant_id,
            'bank_account_id':acct,}
            res = dbapi.dbapi_merchant_bankaccount_register(dbsession, acct_rec, caller_area=_process_call_area)

        print(f'{Fore.LIGHTWHITE_EX}pointofsale bank account:')
        # pointofsales = dbsession.get_rows(dbmodel.POINT_OF_SALE, {}, output_method='', caller_area=_process_call_area)
        # accts = ['351012345671', '351092345672', '351012345673', '351012345674']
        for ix1 in range(0, len(pointofsales)):
            pointofsale = pointofsales[ix1]
            pointofsale_id = pointofsale.pointofsale_id
            ix2=random.randint(0, len(accts)-1)
            acct = accts[ix2]
            
            acct_rec={
            'pointofsale_id':pointofsale_id,
            'bank_account_id':acct,}
            res = dbapi.dbapi_pointofsale_bankaccount_add(dbsession, acct_rec, caller_area=_process_call_area)
            ix3 = random.randint(0, 10)
            if ix3 < 2:
                acct_rec={
                'pointofsale_id':pointofsale_id,}
                res = dbapi.dbapi_pointofsale_bankaccount_remove(dbsession, acct_rec, caller_area=_process_call_area)

    #_process_call_area.update({'debug_level':0})
    for ix1 in range(0, len(merchants)):
        merchant = merchants[ix1]
        merchant_id = merchant.merchant_id
        res = dbapi.dbapi_merchant_get_bankaccounts(dbsession, {'merchant_id': merchant_id}, caller_area=_process_call_area)
        print(res)

    for ix1 in range(0, len(pointofsales)):
        pointofsale = pointofsales[ix1]
        pointofsale_id = pointofsale.pointofsale_id
        res = dbapi.dbapi_pointofsale_credit_info(dbsession, {'pointofsale_id': pointofsale_id}, caller_area=_process_call_area)
        print(res)

    dbsession.close(**_process_call_area)

    diff = datetime.datetime.now() - start_time
    duration = diff.days * 24 * 60 * 60 + diff.seconds
    print(f'{Fore.MAGENTA}duration :',duration)           
#::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
def register_application_users():
    print(f'{Fore.LIGHTWHITE_EX}application users:')
    start_time=datetime.datetime.now()

    device_uid = '111222333444555666777'
    user = 'degray'
    geolocation_lat='3.456789'
    geolocation_lon='3.654321'

    # _process_call_area.update({'debug_level':0})

    dbsession = dbengine.get_dbsession(**_process_call_area)
    # dbapi.dbapi_device_log(dbsession, device_uid, application_name, geolocation_lat, geolocation_lon, client_id)
    # consumer_record={'name': 'fermi','email':'fermi@gmail.com','mobile':'89999'}
    # res = dbapi.dbapi_consumer(dbsession, 'register', consumer_record)
    # res = dbapi.dbapi_consumer(dbsession, 'confirm', consumer_record)
    # dbsession.close(**_process_call_area)

    apps = dbsession.get_rows(dbmodel.APPLICATION, {}, output_method='DICT', caller_area=_process_call_area)
    for ix1 in range(0, len(apps)):
        app = apps[ix1]
        for ix9 in range(0,1):
            cid=str(random.randint(1000,2000))
            email='client'+cid+'@gmail.com'
            name='client'+cid
            mobile='client'+'35799'+cid+cid
            n1 = random.randint(1, 101)
            n2 = random.randint(1000000, 9999999)
            geolocation_lat = str(n1) + '.' + str(n2)
            
            n1 = random.randint(1, 101)
            n2 = random.randint(1000000, 9999999)
            geolocation_lon = str(n1) + '.' + str(n2)

            rec = {'application_name': app.get('application_name'), 'email': email, 'name': name, 'mobile': mobile, 'client_type': 'user', 'user_role': 'user', 'geolocation_lat': geolocation_lat, 'geolocation_lon': geolocation_lon}

        emails=['fermi@gmail.com','albert@gmail.com','bell@gmail']
        for ix9 in range(0,len(emails)):
            email = emails[ix9]
            name = email
            mobile=''
            n1 = random.randint(1, 101)
            n2 = random.randint(1000000, 9999999)
            geolocation_lat = str(n1) + '.' + str(n2)
            
            n1 = random.randint(1, 101)
            n2 = random.randint(1000000, 9999999)
            geolocation_lon = str(n1) + '.' + str(n2)

            rec = {'application_name': app.get('application_name'), 'email': email, 'name': name, 'mobile': mobile, 'client_type': 'user', 'user_role': 'user', 'geolocation_lat': geolocation_lat, 'geolocation_lon': geolocation_lon}
    
            res = dbapi.dbapi_application_USER(dbsession, 'register', rec, caller_area=_process_call_area)
    
    dbsession.close(**_process_call_area)

    diff = datetime.datetime.now() - start_time
    duration = diff.days * 24 * 60 * 60 + diff.seconds
    print(f'{Fore.MAGENTA}duration :',duration)           
#:::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::: 
def test_interactions():
    print(f'{Fore.LIGHTWHITE_EX}interactions test:')
    start_time=datetime.datetime.now()

    geolocation_lat='33.456789'
    geolocation_lon = '34.654321'
    application_name='scanandpay_client'
    db.INTERACTIONS_TABLE.delete_rows()
    db.INTERACTIONS_MESSAGE_TABLE.delete_rows()
    
    #_process_call_area.update({'debug_level':0})
    dbsession = dbengine.get_dbsession(**_process_call_area)
    #create dummy application users
    emails=['fermi@gmail.com','albert@gmail.com','bell@gmail','scroedinger@gmail.com']
    apps = dbsession.get_rows(dbmodel.APPLICATION, {}, caller_area=_process_call_area)
    for ix1 in range(0, len(apps)):
        app = apps[ix1]
        for ix9 in range(0,len(emails)):
            email = emails[ix9]
            name = email
            mobile=''
            n1 = random.randint(1, 101)
            n2 = random.randint(1000000, 9999999)
            geolocation_lat = str(n1) + '.' + str(n2)
            
            n1 = random.randint(1, 101)
            n2 = random.randint(1000000, 9999999)
            geolocation_lon = str(n1) + '.' + str(n2)

            rec = {'application_name': app.application_name, 'email': email, 'name': name, 'mobile': mobile, 'client_type': 'user', 'user_role': 'user', 'geolocation_lat': geolocation_lat, 'geolocation_lon': geolocation_lon}

            dbsession = dbengine.get_dbsession(**_process_call_area)
            res = dbapi.dbapi_application_USER(dbsession, 'register', rec, caller_area=_process_call_area)
            dbsession.close(**_process_call_area)   

    #_process_call_area.update({'debug_level':0})
    email = 'abc@gmail.com'
    consumer = dbsession.get(dbmodel.CLIENT, {'email':email})
    prev_client_id = consumer.client_id
    pointofsales = dbsession.get_rows(dbmodel.POINT_OF_SALE, {}, caller_area=_process_call_area)
    #for ix1 in range(0, len(apps)):
    for ix1 in range(0, 2):
        app = apps[ix1]
        application_name = app.application_name
        #for ix2 in range(0, len(emails)):
        for ix2 in range(0, 2):
            email = emails[ix2]            
            consumer = dbsession.get(dbmodel.CLIENT, {'email':email})
            client_id = consumer.client_id
            # print('client_id:', client_id)
            #for ix3 in range(0, len(pointofsales))):
            for ix3 in range(0, 2):
                pointofsale = pointofsales[ix3]
                # merchant_id=pointofsale.merchant_id
                pointofsale_id = pointofsale.pointofsale_id
                pointofsale_name = pointofsale.name
                # print('merchant_id:',merchant_id)
                print('client_id:', client_id, '--->', pointofsale_name, 'pointofsale_id:', pointofsale_id)
                
                interaction_record = {
                    'client_id': client_id,
                    'corresponder_id': pointofsale_id,
                    'geolocation_lat': geolocation_lat,
                    'geolocation_lon': geolocation_lon,
                    'application_name': application_name,
                }
                res = dbapi.dbapi_interaction_start(dbsession,interaction_record, caller_area=_process_call_area)
                print(res.get('api_status'),res.get('api_message'))

                interaction_id = res.get('interaction_id')
                print('------', 'interaction_id: ', interaction_id)
                if not interaction_id:
                    print(f'{Fore.RED}interaction start failed.......')
                    exit(0)

                interaction_record = {
                    'interaction_id': interaction_id,
                    'originator_id': pointofsale_id,
                    'geolocation_lat': geolocation_lat,
                    'geolocation_lon': geolocation_lon,
                    'application_name': application_name,
                }
                res = dbapi.dbapi_interaction_accept(dbsession,interaction_record,caller_area=_process_call_area)
                print(res.get('api_status'),res.get('api_message'))
                
                interaction_record = {
                    'interaction_id': interaction_id,
                    'originator_id': client_id,
                    'message_record':'hello shalimar....',
                    'geolocation_lat': geolocation_lat,
                    'geolocation_lon': geolocation_lon,
                    'application_name': application_name,
                }
                res = dbapi.dbapi_interaction_message_add(dbsession,interaction_record,caller_area=_process_call_area)
                print(res.get('api_status'),res.get('api_message'))

                #test security viloation
                interaction_record = {
                    'interaction_id': interaction_id,
                    'originator_id': prev_client_id,
                    'message_record':'hello xxxxxx....',
                    'geolocation_lat': geolocation_lat,
                    'geolocation_lon': geolocation_lon,
                    'application_name': application_name,
                }
                res = dbapi.dbapi_interaction_message_add(dbsession,interaction_record,caller_area=_process_call_area)
                print(res.get('api_status'),res.get('api_message'))

                interaction_record = {
                    'interaction_id': interaction_id,
                    'originator_id': pointofsale_id,
                    'message_record':'hello raindegray....',
                    'geolocation_lat': geolocation_lat,
                    'geolocation_lon': geolocation_lon,
                    'application_name': application_name,
                }
                res = dbapi.dbapi_interaction_message_add(dbsession,interaction_record,caller_area=_process_call_area)
                print(res.get('api_status'),res.get('api_message'))

                res = dbapi.dbapi_interaction_finish(dbsession,interaction_record,caller_area=_process_call_area)
                print(res.get('api_status'),res.get('api_message'))
                
            prev_client_id = client_id
        
    dbsession.close(**_process_call_area)

    diff = datetime.datetime.now() - start_time
    duration = diff.days * 24 * 60 * 60 + diff.seconds
    print(f'{Fore.MAGENTA}duration :',duration)
#:::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::: 
def test_device_log():
    print(f'{Fore.LIGHTWHITE_EX}device log test:')
    start_time=datetime.datetime.now()

    #_process_call_area.update({'debug_level':0})
    dbsession = dbengine.get_dbsession(**_process_call_area)
    device_uid = '1qqqqq112223zzzzzzzzzzzzzz33444555666777'
    geolocation_lat='313.456789'
    geolocation_lon = '314.654321'
    client_id = '0000zzzz0111100000000'
    application_name='scanandsssspay_merchant'

    dbapi.dbapi_device_log(dbsession, device_uid, application_name, geolocation_lat, geolocation_lon, client_id,caller_area=_process_call_area)

    dbsession.close(**_process_call_area)

    diff = datetime.datetime.now() - start_time
    duration = diff.days * 24 * 60 * 60 + diff.seconds
    print(f'{Fore.MAGENTA}duration :',duration)
#:::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::: 
#::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
#::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
#::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
# main
#::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
#::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
#::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
if __name__ == '__main__':
    _process_name = "_database_ganimides_init"
    _process_entity = ''
    _process_action = 'init'
    _process_msgID = 'process:database_init_test'

    application_name = 'shalimar'
    client_id='letticia'

    _process_identity_kwargs = {'type': 'process', 'module': module_id, 'name': _process_name, 'action': _process_action, 'entity': _process_entity, 'msgID': _process_msgID,}
    _process_adapters_kwargs = {'dbsession': None}
    _process_log_kwargs = {'indent_method': 'AUTO', 'indent_level':None}
    _process_debug_level = get_debug_level(caller_area.get('debug_level'), **_process_identity_kwargs, **_process_adapters_kwargs)
    _process_debug_files = get_debug_files(_process_debug_level, **_process_identity_kwargs, **_process_adapters_kwargs)
    _process_debug_kwargs={'debug_level':_process_debug_level,'debug_files':_process_debug_files}

    _process_signature = build_process_signature(**_process_identity_kwargs, **_process_adapters_kwargs, **_process_debug_kwargs, **_process_log_kwargs)
    _process_call_area = build_process_call_area(_process_signature, caller_area)

    if 1 == 2:
        print('test-indentation')
        log_process_start(_process_msgID,**_process_call_area)

        device_uid = '1qqqqq112223zzzzzzzzzzzzzz33444555666777'
        user = 'pqqqqa'
        geolocation_lat='313.456789'
        geolocation_lon = '314.654321'
        client_id = '0000zzzz0111100000000'
        application_name='scanandsssspay_merchant'

        dbsession = dbengine.get_dbsession(debug=99,**_process_call_area)
        dbapi.dbapi_device_log(dbsession, device_uid, application_name, geolocation_lat, geolocation_lon, client_id,caller_area=_process_call_area)
        dbapi.dbapi_api(dbsession, 'refresh', {'api_name':'bobbi'},caller_area=_process_call_area)
        dbsession.close(**_process_call_area)

        log_process_finish(_process_msgID,'',**_process_call_area)

    if 1 == 2:
        print('test-debug-options')
        _process_call_area.update({'input_debug':False})
        _process_call_area.update({'data_debug':False})
        _process_call_area.update({'start_debug':False})
        _process_call_area.update({'result_debug':False})
        _process_call_area.update({'finish_debug':False})
        #negative 
        _process_call_area.update({'success_message_debug':False})
        _process_call_area.update({'_message_debug':False})
        #positive
        _process_call_area.update({'message_debug':False})
        _process_call_area.update({'warning_message_debug':True})
        _process_call_area.update({'error_message_debug':True})
        #all messages
        _process_call_area.update({'message_debug':False})
        #results on
        _process_call_area.update({'result_debug':True})
        #finish on
        _process_call_area.update({'result_debug':False})
        _process_call_area.update({'finish_debug':True})
        #start on
        _process_call_area.update({'result_debug':False})
        _process_call_area.update({'finish_debug':False})
        _process_call_area.update({'session_result_message_debug':False})
        _process_call_area.update({'start_debug':True})
        #input on
        _process_call_area.update({'result_debug':False})
        _process_call_area.update({'finish_debug':False})
        _process_call_area.update({'session_result_message_debug':False})
        _process_call_area.update({'start_debug':True})
        _process_call_area.update({'input_debug':True})

        #input on caller off
        _process_call_area.update({'result_debug':False})
        _process_call_area.update({'finish_debug':False})
        _process_call_area.update({'session_result_message_debug':False})
        _process_call_area.update({'start_debug':True})
        _process_call_area.update({'input_debug':False})
        _process_call_area.update({'caller_area_input_debug':False})
        _process_call_area.update({'result_message_debug':False})
        _process_call_area.update({'session_result_message_debug':True})

        log_process_start(_process_msgID,**_process_call_area)

        device_uid = '1qqqqq112223zzzzzzzzzzzzzz33444555666777'
        user = 'pqqqqa'
        geolocation_lat='313.456789'
        geolocation_lon = '314.654321'
        client_id = '0000zzzz0111100000000'
        application_name='scanandsssspay_merchant'

        dbsession = dbengine.get_dbsession(debug=99,**_process_call_area)
        dbapi.dbapi_device_log(dbsession, device_uid, application_name, geolocation_lat, geolocation_lon, client_id,caller_area=_process_call_area)
        dbapi.dbapi_api(dbsession, 'refresh', {'api_name':'bobbi'},caller_area=_process_call_area)
        dbsession.close(**_process_call_area)

        log_process_finish(_process_msgID,'',**_process_call_area)

    if 1 == 2: #test-debug-templates
        print('test-debug-templates')
        log_process_start(_process_msgID,**_process_call_area)

        device_uid = '1qqqqq112223zzzzzzzzzzzzzz33444555666777'
        user = 'pqqqqa'
        geolocation_lat='313.456789'
        geolocation_lon = '314.654321'
        client_id = '0000zzzz0111100000000'
        application_name='scanandsssspay_merchant'

        dbsession = dbengine.get_dbsession(debug=99,**_process_call_area)
        dbapi.dbapi_device_log(dbsession, device_uid, application_name, geolocation_lat, geolocation_lon, client_id,caller_area=_process_call_area)
        dbapi.dbapi_api(dbsession, 'refresh', {'api_name':'bobbi'},caller_area=_process_call_area)
        dbsession.close(**_process_call_area)

        log_process_finish(_process_msgID,'',**_process_call_area)
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 
    log_process_start(_process_msgID,**_process_call_area)
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 
    base_time = datetime.datetime.now()
    #recreate_tables()
    #clear_tables()
    # test_device_log()
    # create_users()
    # create_apis()
    # add_banks()
    # create_subscriptions()
    # add_applications()
    # add_application_templates()
    # add_application_admin_users()

    # register_apis()
    # register_application_users()
    register_client_bank_subscriptions()
    # add_merchants()
    # add_retail_stores()
    # add_pointofsales()
    # add_service_points()
    # add_customer_service_assistants()
    register_merchant_bank_subscriptions()
    # add_bank_accounts()
    # test_device_log()
    # test_tokens()
    # test_interactions()

    diff = datetime.datetime.now() - base_time
    duration = diff.days * 24 * 60 * 60 + diff.seconds
    print(f'{Fore.YELLOW}total duration :',duration)
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 
    if 1==2:#display tables
        db.CLIENTS.display_summary(include_columns='mobile,email,name')
        db.CLIENT_DEVICES.display_summary(include_columns='mobile,email,name')
        db.DEVICES.display_summary(include_columns='mobile,email,name')
        db.DEVICE_USAGE.display_summary(include_columns='*')
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 
    log_process_finish(_process_msgID,{},**_process_call_area)
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 