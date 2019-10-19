#!flask/bin/python
import os
import sys
if not (os.path.dirname(os.path.dirname(__file__)) in sys.path): sys.path.append(os.path.dirname(os.path.dirname(__file__)))
if not (os.path.dirname(__file__) in sys.path): sys.path.append(os.path.dirname(__file__))
#print(sys.path)
from colorama import Fore
import datetime
# import secrets
# import requests

# from flask import Flask, jsonify, abort, request, make_response, url_for,redirect
# from flask_httpauth import HTTPBasicAuth
# from flask import json
# from flask import session, g

from _onlineApp import thisApp
from _onlineApp import build_process_signature, build_process_call_area, get_debug_level, get_debug_files
from _onlineApp import log_process_start, log_process_finish, log_process_message
from _onlineApp import Fore

import ganimides_database as db
import _ganimides_openBankingAPI as api
#::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
#::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
#::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
#::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
def recreate_tables():
    db.check_table(db.BANK_AUTHORIZATIONS,auto_synchronize=True,synchronization_method='drop',copy_records=True,silent=True)
    db.check_table(db.BANK_SUBSCRIPTIONS,auto_synchronize=True,synchronization_method='drop',copy_records=True,silent=True)
    db.check_table(db.BANK_ACCOUNTS,auto_synchronize=True,synchronization_method='drop',copy_records=True,silent=True)
    db.recreate_tables(db.db_schema_Base,db.engine)
    db.BANK_AUTHORIZATIONS.delete_rows()
    db.BANK_SUBSCRIPTIONS.delete_rows()
    db.BANK_ACCOUNTS.delete_rows()
#::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
def clear_tables():
    db.BANK_AUTHORIZATIONS.clear_table()
    db.BANK_SUBSCRIPTIONS.clear_table()
    db.BANK_ACCOUNTS.clear_table()
#::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
#::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
#::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
#::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
def create_merchant_subscriptions():  #and request client authorization
    print(f'{Fore.LIGHTWHITE_EX}create merchant subscriptions:')
    start_time=datetime.datetime.now()
    
    dbsession = db.get_dbsession(**_process_call_area)
    merchant_id = '6d1d1a14-e91b-11e9-aae5-33b843d61993'
    bank_id = 'bankofcyprus'
    dbreply = db.dbapi_merchant(dbsession,'get',{'merchant_id':merchant_id},caller_area=_process_call_area)
    client_id = dbreply.get('api_data', {}).get('client_id')
    if not client_id:
        msg = f'merchant {merchant_id} not found'
        print(msg)
    else:
        res = api.banksubscription_register(dbsession, 
            client_id=client_id, bank_id=bank_id, application_name=application_name,
            allow_transactionHistory=True, allow_balance=True,
            allow_details=True, allow_checkFundsAvailability=False,
            payments_limit=0, payments_currency='EUR', payments_amount=0
            )
        print(res)

    banks = dbsession.get_rows(db.BANK, {'status':'Active'}, caller_area=_process_call_area)
    merchants = dbsession.get_rows(db.MERCHANT, {}, caller_area=_process_call_area)
    for ix1 in range(0, len(merchants)):
        merchant = merchants[ix1]
        dbreply = db.dbapi_merchant(dbsession,'get',{'merchant_id':merchant.merchant_id},caller_area=_process_call_area)
        client_id = dbreply.get('api_data', {}).get('client_id')
        if not client_id:
            msg = f'merchant {merchant_id} not found'
            print(msg)
        else:
            for ix2 in range(0,len(banks)):
                bank = banks[ix2]
                bank_id = bank.bank_id
                res = api.banksubscription_register(dbsession, 
                    client_id=client_id, bank_id=bank_id, application_name=application_name,
                    allow_transactionHistory=True, allow_balance=True,
                    allow_details=True, allow_checkFundsAvailability=False,
                    payments_limit=0, payments_currency='EUR', payments_amount=0
                    )
                print(res)
    dbsession.close(**_process_call_area)

    diff = datetime.datetime.now() - start_time
    duration = diff.days * 24 * 60 * 60 + diff.seconds
    print(f'{Fore.MAGENTA}duration :',duration)
#::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
def create_client_subscriptions(): #and request client auth
    print(f'{Fore.LIGHTWHITE_EX}create client subscriptions:')
    start_time=datetime.datetime.now()

    dbsession = db.get_dbsession(**_process_call_area)
    emails = ['fermi@gmail.com', 'albert@gmail.com', 'bell@gmail', 'scroedinger@gmail.com']
    for email in emails:
        client = dbsession.get(db.CLIENT, {'email': email}, caller_area=_process_call_area)
        if client:
            client_id = client.client_id
            bank_id = 'bankofcyprus'
            res = api.banksubscription_register(dbsession, 
                client_id=client_id, bank_id=bank_id, application_name=application_name,
                allow_transactionHistory=True, allow_balance=True,
                allow_details=True, allow_checkFundsAvailability=False,
                payments_limit=0, payments_currency='EUR', payments_amount=0
                )
            print(res)
    dbsession.close(**_process_call_area)

    diff = datetime.datetime.now() - start_time
    duration = diff.days * 24 * 60 * 60 + diff.seconds
    print(f'{Fore.MAGENTA}duration :',duration)
#::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
def receive_authorizations_from_clients():
    print(f'{Fore.LIGHTWHITE_EX}receive authorizations from clients:')
    start_time=datetime.datetime.now()

    dbsession = db.get_dbsession(**_process_call_area)
    bank_id = 'bankofcyprus'
    authorization_code = '1212122121simulated_authorization_code2121212112121'
    _process_call_area.update({'simulation_enabled':True})
    reply=api.banksubscription_receive_authorization_from_client(dbsession, bank_id, authorization_code, caller_area=_process_call_area)
    print(reply.get('api_message'))
    dbsession.close(**_process_call_area)

    diff = datetime.datetime.now() - start_time
    duration = diff.days * 24 * 60 * 60 + diff.seconds
    print(f'{Fore.MAGENTA}duration :',duration)
#::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
def create_banksubscription_only():
    print(f'{Fore.LIGHTWHITE_EX}create bank subscription only:')
    start_time=datetime.datetime.now()

    dbsession = db.get_dbsession(**_process_call_area)
    application_name='scanandpay_client'
    emails = ['fermi@gmail.com', 'albert@gmail.com', 'bell@gmail', 'scroedinger@gmail.com']
    for email in emails:
        client = dbsession.get(db.CLIENT, {'email': email}, caller_area=_process_call_area)
        client_id=client.client_id
    # client_id='685e0b46-e91b-11e9-bea1-2db812eac691'
    bank_id = 'bankofcyprus'
    reply=api.banksubscription_create(dbsession, client_id, bank_id, application_name, allow_transactionHistory=True, allow_balance=True, allow_details=True, allow_checkFundsAvailability=True, payments_limit=1000, payments_currency='EUR', payments_amount=100, caller_area=_process_call_area)
    subscription_id = reply.get('bank_subscriptionID')
    print(reply.get('api_message'),'created subscription_id:',subscription_id)
    dbsession.close(**_process_call_area)


    diff = datetime.datetime.now() - start_time
    duration = diff.days * 24 * 60 * 60 + diff.seconds
    print(f'{Fore.MAGENTA}duration :',duration)
#::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
def request_authorization_from_client_only():
    print(f'{Fore.LIGHTWHITE_EX}request athorization from client only:')
    start_time = datetime.datetime.now()
    
    dbsession = db.get_dbsession(**_process_call_area)
    bank_id = 'bankofcyprus'
    application_name='scanandpay_client'
    emails = ['fermi@gmail.com', 'albert@gmail.com', 'bell@gmail', 'scroedinger@gmail.com']
    for email in emails:
        client = dbsession.get(db.CLIENT, {'email': email}, caller_area=_process_call_area)
        client_id=client.client_id
    reply=api.banksubscription_create(dbsession, client_id, bank_id, application_name, allow_transactionHistory=True, allow_balance=True, allow_details=True, allow_checkFundsAvailability=True, payments_limit=1000, payments_currency='EUR', payments_amount=100, caller_area=_process_call_area)
    if not reply.get('api_status') == 'success':
        msg = 'create subs FAILED.'
        print(Fore.RED, msg)
    else:
        api_data = reply.get('api_data', {})        
        subscription_id = api_data.get('bank_subscriptionID')
        client_id = api_data.get('client_id')
        bank_id = api_data.get('bank_id')
        application_name = api_data.get('application_name')
        
        reply = api.banksubscription_request_authorization_from_client(dbsession, client_id, bank_id, subscription_id, application_name, caller_area=_process_call_area)
        print(reply.get('api_message'))

    dbsession.close(**_process_call_area)

    diff = datetime.datetime.now() - start_time
    duration = diff.days * 24 * 60 * 60 + diff.seconds
    print(f'{Fore.MAGENTA}duration :',duration)
#::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
def unregister_banksubscription():
    print(f'{Fore.LIGHTWHITE_EX}unregister bank subscriptions:')
    start_time=datetime.datetime.now()

    dbsession = db.get_dbsession(**_process_call_area)
    sid='6ab80c36-e9de-11e9-8aae-fbff3f03e211'
    res=api.banksubscription_unregister(dbsession, client_id={}, bank_id={}, application_name={}, subscription_id=sid, caller_area={})    
    print(res.get('api_message'))
    sid='28ddd8c6-e9db-11e9-bae8-e105a87466ca'
    res=api.banksubscription_unregister(dbsession, client_id={}, bank_id={}, application_name={}, subscription_id=sid, caller_area={})    
    print(res.get('api_message'))
    dbsession.close(**_process_call_area)

    diff = datetime.datetime.now() - start_time
    duration = diff.days * 24 * 60 * 60 + diff.seconds
    print(f'{Fore.MAGENTA}duration :',duration)
#::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
#:::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::: 
#::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
#::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
#::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
# main
#::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
#::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
#::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
if __name__ == '__main__':
    module_id='dummy'
    caller_area={'debug_level':-1,'debug_template':'SESSION_ONLY'}
    caller_area={'debug_level':-1,'debug_template':'FULL'}
    caller_area = {'debug_level': 99, 'caller_area_input_debug': False,}

    device_uid = 'qeqeqwe213123132213afasfasdffds'
    geolocation_lat = '1212.114213'
    geolocation_lon = '14567.234324234'
    application_name = 'scanandpay_client'
    application_client_id = '67a9fd9a-e91b-11e9-a7f2-75d9d55de53b'
    application_client_secretKey = '90NfwCHA7C74QWBAo8YeIMKCp2g-btM9frpvODfIjEIxby2knXEWMTmypREaWIcTIU1_Y8OaPYEUaASnLoZVIdBdOIH5VxA__TsuHcDEL4L90gW5qfdW5QULwwVpMBb1ufPhZl23pPqRkjVb4Ja6d4qX8YIotuVzneLpkFoJwUQ'
    client_secretKey = '121212112121212'
    client_id = '121212112121212'
    user_id = '6701d6a8-e91b-11e9-98c9-79d91b2c4899'
    caller_area = {
        'application_name': application_name,
        'application_client_id': application_client_id,
        'application_client_secretKey': application_client_secretKey,
        'client_id': client_id,
        'client_secretKey': client_secretKey,
        'user_id': user_id,
        'device_uid': device_uid,
        'geolocation_lat': geolocation_lat,
        'geolocation_lon': geolocation_lon,
        }

    caller_area.update({'debug_level': 0, 'caller_area_input_debug': False,})

    _process_name = "test_openbanking_apis"
    _process_entity = ''
    _process_action = 'test'
    _process_msgID = 'process: test_openbanking_apis'

    _process_identity_kwargs = {'type': 'process', 'module': module_id, 'name': _process_name, 'action': _process_action, 'entity': _process_entity, 'msgID': _process_msgID,}
    _process_adapters_kwargs = {'dbsession': None}
    _process_log_kwargs = {'indent_method': 'AUTO', 'indent_level':None}
    _process_debug_level = get_debug_level(caller_area.get('debug_level'), **_process_identity_kwargs, **_process_adapters_kwargs)
    _process_debug_files = get_debug_files(_process_debug_level, **_process_identity_kwargs, **_process_adapters_kwargs)
    _process_debug_kwargs={'debug_level':_process_debug_level,'debug_files':_process_debug_files}

    _process_signature = build_process_signature(**_process_identity_kwargs, **_process_adapters_kwargs, **_process_debug_kwargs, **_process_log_kwargs)
    _process_call_area = build_process_call_area(_process_signature, caller_area)

    #SOS#SOS#SOS#SOS#SOS#SOS#SOS#SOS#SOS#SOS#SOS#SOS#SOS#SOS#
    #SOS#SOS#SOS#SOS#SOS#SOS#SOS#SOS#SOS#SOS#SOS#SOS#SOS#SOS#
    #SOS#SOS#SOS#SOS#SOS#SOS#SOS#SOS#SOS#SOS#SOS#SOS#SOS#SOS#
    _process_call_area.update({'simulation_enabled':True})
    #SOS#SOS#SOS#SOS#SOS#SOS#SOS#SOS#SOS#SOS#SOS#SOS#SOS#SOS#
    #SOS#SOS#SOS#SOS#SOS#SOS#SOS#SOS#SOS#SOS#SOS#SOS#SOS#SOS#
    #SOS#SOS#SOS#SOS#SOS#SOS#SOS#SOS#SOS#SOS#SOS#SOS#SOS#SOS#
    
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

    create_banksubscription_only()
    request_authorization_from_client_only()
    # create_merchant_subscriptions()
    # create_client_subscriptions()
    receive_authorizations_from_clients()
    unregister_banksubscription()

    diff = datetime.datetime.now() - base_time
    duration = diff.days * 24 * 60 * 60 + diff.seconds
    print(f'{Fore.YELLOW}total duration :',duration)
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 
    log_process_finish(_process_msgID,{},**_process_call_area)
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 