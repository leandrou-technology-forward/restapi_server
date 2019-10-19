#!flask/bin/python
import os
import sys
if not (os.path.dirname(__file__) in sys.path): sys.path.append(os.path.dirname(__file__))
print(sys.path)
from colorama import Fore
import datetime
import secrets
import requests

from flask import Flask, jsonify, abort, request, make_response, url_for,redirect
from flask_httpauth import HTTPBasicAuth
from flask import json
from flask import session, g

from ganimides_server._onlineApp import thisApp
from ganimides_server._onlineApp import build_process_signature, build_process_call_area, get_debug_level, get_debug_files
from ganimides_server._onlineApp import log_process_start, log_process_finish, log_process_message
from ganimides_server._onlineApp import Fore

from _tokenServices import token_is_valid
from ganimides_server import  ganimides_database as db
from ganimides_server import  ganimides_api as api
##########################################################################################################################
# from ganimides_server import client_banksubscription_register
# from ganimides_server import merchant_banksubscription_register
module_ProgramName = os.path.splitext(os.path.basename(__file__))[0]
module_id = '{}'.format(module_ProgramName)
module_version = 0.1
##########################################################################################################################
##########################################################################################################################
##########################################################################################################################
def get_authorization_code_from_boc_client():
    bank_code = 'bankofcyprus'
    application_name = request.headers.get('Registered-Application')
    request_params_json=get_params(request)
    authorization_code = request_params_json.get('code')
    if not authorization_code:
        msg = f'authorization code not received by bank [{bank_code}]'
        print(msg)
        reply = {'api_status': 'error', 'api_message': msg}
        return make_response(jsonify(reply), 400)

    result = api.banksubscription_receive_authorization_from_client(dbsession,bank_code, authorization_code,caller_info={})
    if not result.get('api_status')=='success':
        msg = result.get('api_message', '?')
        msg=f"your authorization for an app use your {bank_code} account(s) FAILED. retry"
        resp = make_response(jsonify(msg), 200)
        resp.headers['Content-type'] = 'text/html'
        return resp
    else:
        application_name=result.get('application_name','?')
        msg=f"you have just authorized app {application_name} to use your {bank_code} account(s)."
        resp = make_response(jsonify(msg), 200)
        resp.headers['Content-type'] = 'text/html'
        app=db.dbapi_application(dbsession, 'get', {'application_name':application_name}, filter_dict={}, caller_dict={}, call_level=-1,debug_level=-1)
        if app:
            app_redirect = app.get('application_redirect_uri')
            if app_redirect:
                if app_redirect.find("http://") != 0 and app_redirect.find("https://") != 0:
                    app_redirect = "http://" + app_redirect.strip()
                    return redirect(app_redirect)
        return resp
#############################################################################
#############################################################################
#############################################################################
#############################################################################
# authorization routes
#############################################################################
#############################################################################
#############################################################################
def get_access_token(request_data={}):
    res = db.dbapi_token_get_access_token(dbsession, request_data)
    return res
#############################################################################
def get_clients_list(action_filter={}):
    dbreply = db.dbapi_client(dbsession,'LIST',action_filter,caller_area=_process_call_area)
    return dbreply
#############################################################################
#############################################################################
#############################################################################
def merchant_banksubscription_register(merchant_id, application_name, bank_id, subscription_options={}):
    dbreply = db.dbapi_merchant(dbsession,'get',{'merchant_id':merchant_id},caller_area=_process_call_area)
    client_id = dbreply.get('api_data', {}).get('client_id')
    if not client_id:
        msg = f'merchant {merchant_id} not found'
        reply = {'api_status': 'error', 'api_message': msg}
        return reply

    # subscription_options = request.json
    allow_transactionHistory = subscription_options.get('allow_transactionHistory', False)
    allow_balance = subscription_options.get('allow_balance', False)
    allow_details = subscription_options.get('allow_details', False)
    allow_checkFundsAvailability = subscription_options.get('allow_checkFundsAvailability', False)
    payments_limit = subscription_options.get('payments_limit', 100)
    payments_currency = subscription_options.get('payments_currency', 'EUR')
    payments_amount = subscription_options.get('payments_amount', 10)
    
    reply = api.banksubscription_register(dbsession, 
        client_id=client_id, bank_id=bank_id, application_name=application_name,
        allow_transactionHistory=allow_transactionHistory, allow_balance=allow_balance,
        allow_details=allow_details, allow_checkFundsAvailability=allow_checkFundsAvailability,
        payments_limit=payments_limit, payments_currency=payments_currency, payments_amount=payments_amount
        )
    return reply
#############################################################################
# subscriptions routes
#############################################################################
#############################################################################
#x############################################################################
def new_application():
    if not request.json:
        reply={'status':'error','message':'json data Not provided'}
        return make_response(jsonify(reply), 400)
    record_data = request.json
    if not record_data.get('name'):
        reply={'status':'error','message':'[name] Not provided'}
        return make_response(jsonify(reply), 401)
    if not record_data.get('email'):
        reply={'status':'error','message':'[email] Not provided'}
        return make_response(jsonify(reply), 401)
    dbreply=db.dbapi_application(dbsession, 'register', record_data, filter_dict={}, caller_dict={}, call_level=-1,debug_level=-1)
    return jsonify( dbreply )
#############################################################################
def get_application(application_id):
    dbreply=db.dbapi_application(dbsession, 'get', {'application_id':application_id}, filter_dict={}, caller_dict={}, call_level=-1,debug_level=-1)
    return jsonify( dbreply )
#############################################################################
def update_application(application_id):
    if not request.json:
        reply={'status':'error','message':'json data Not provided'}
        return make_response(jsonify(reply), 400)
    update_record = request.json
    update_record.update({'application_id':application_id})
    dbreply=db.dbapi_application(dbsession, 'update', update_record, filter_dict={}, caller_dict={}, call_level=-1,debug_level=-1)
    return jsonify( dbreply )
#############################################################################
def unregister_application(application_id):
    if not request.json:
        reply={'status':'error','message':'json data Not provided'}
        return make_response(jsonify(reply), 400)
    update_record = request.json
    update_record.update({'application_id':application_id})
    dbreply=db.dbapi_application(dbsession, 'unregister', update_record, filter_dict={}, caller_dict={}, call_level=-1,debug_level=-1)
    return jsonify(dbreply)
#############################################################################
def application_api_register(application_id,api_name):
    update_record = request.json
    update_record.update({'application_id':application_id})
    update_record.update({'api_name':api_name})
    dbreply=db.dbapi_application(dbsession, 'api_register', update_record, filter_dict={}, caller_dict={}, call_level=-1,debug_level=-1)
    return jsonify(dbreply)
#############################################################################
def delete_application(application_id):
    dbreply=db.dbapi_application(dbsession, 'delete', {'application_id':application_id}, filter_dict={}, caller_dict={}, call_level=-1,debug_level=-1)
    return jsonify( dbreply )
#############################################################################
##########################################################################################################################
# @app.route('/openbanking/api/v1/subscriptions/device', methods = ['PUT','POST'])
# @auth.login_required
# def new_device():
#     if not request.json:
#         reply={'status':'error','message':'json data Not provided'}
#         return make_response(jsonify(reply), 400)
#     record_data = request.json
#     #basic validations before calling the database api
#     # if not record_data.get('email'):
#     #     reply={'status':'error','message':'[email] Not provided'}
#     #     return make_response(jsonify(reply), 401)
#     # if not record_data.get('name'):
#     #     reply={'status':'error','message':'[name] Not provided'}
#     #     return make_response(jsonify(reply), 401)
#     dbreply = db.dbapi_new_device(record_data)
#     if dbreply.get('status') == 'success':
#         record_data = dbreply.get('data', {})
#         dbreply = db.dbapi_register_device(record_data)
#     return jsonify( dbreply )
#############################################################################
#############################################################################
#############################################################################
# merchant creditinfo routes
#############################################################################
#############################################################################
#############################################################################
#############################################################################
# @app.route('/openbanking/api/v1/pointofsales/code/<pointofsale_code>/creditinfo', methods = ['GET'])
# def get_merchant_creditinfo_from_poscode(pointofsale_code):
#     res = db.dbapi_get_merchant_creditinfo_from_pointofsale(pointofsale_code,'code')
#     return jsonify( res )
# #############################################################################
# @app.route('/openbanking/api/v1/merchants/<merchant_id>/pointofsales/<pos_code>/creditinfo', methods = ['GET'])
# def get_merchant_creditinfo_from_merchantuid_and_poscode(merchant_id,pos_code):
#     res = db.dbapi_get_merchant_creditinfo_smartly(merchant_id,pos_code)
#     return jsonify( res )
# #############################################################################
# @app.route('/openbanking/api/v1/merchants/code/<merchant_code>/pointofsales/<pos_code>/creditinfo', methods = ['GET'])
# def get_merchant_creditinfo_from_merchantcode_and_poscode(merchant_code,pos_code):
#     res = db.dbapi_get_merchant_creditinfo_smartly(merchant_code,pos_code)
#     return jsonify( res )
# #############################################################################

#############################################################################
#############################################################################
#############################################################################
# interactions routes
#############################################################################
#############################################################################
#############################################################################
# @app.route('/openbanking/api/v1/interactions/pointofsales/<pointofsale_id>/originator/<secretKey>/finish', methods = ['PATCH'])
# def finish_interaction(pointofsale_id,secretKey):
#     res = db.dbapi_finish_interaction(pointofsale_id,secretKey)
#     return jsonify( res )
# ##########################################################################################################################
# @app.route('/openbanking/api/v1/interactions/pointofsales/<pointofsale_id>/originator/<secretKey>/checkin', methods = ['PUT','POST'])
# def client_checkin(pointofsale_id,secretKey):
#     res = db.dbapi_client_checkin(secretKey,pointofsale_id)
#     return jsonify( res )
# ##########################################################################################################################
# @app.route('/openbanking/api/v1/interactions/pointofsales/<pointofsale_id>/interactionid', methods = ['GET'])
# def get_active_interactionid(pointofsale_id):
#     res = db.dbapi_get_active_interactionid_on_pointofsale(pointofsale_id,hint='')
#     return jsonify(res)
# ##########################################################################################################################
# @app.route('/openbanking/api/v1/interactions/pointofsales/<pointofsale_id>/originator/<secretKey>/getmessages/from/<from_step>', methods = ['GET'])
# def get_interaction_messages(pointofsale_id, secretKey, from_step):
#     res = db.dbapi_get_interaction_messages(pointofsale_id,secretKey,from_step)
#     return jsonify(res)
# ##########################################################################################################################
# @app.route('/openbanking/api/v1/interactions/pointofsales/<pointofsale_id>/addmessage', methods = ['PUT','POST'])
# def add_interaction_message(pointofsale_id):
#     if not request.json:
#         reply={'status':'error','message':'json data Not provided'}
#         return make_response(jsonify(reply), 400)
#     request_data = request.json
#     res = db.dbapi_add_interaction_message(pointofsale_id, request_data)
#     return jsonify( res )
# ##########################################################################################################################
# @app.route('/openbanking/api/v1/interactions/pointofsales/<pointofsale_id>/originator/<secretKey>/putmessage', methods = ['PUT','POST'])
# def put_interaction_message(pointofsale_id,secretKey):
#     if not request.json:
#         reply={'status':'error','message':'json data Not provided'}
#         return make_response(jsonify(reply), 400)
#     request_data = request.json
#     res = db.dbapi_put_interaction_message(pointofsale_id, secretKey,request_data)
#     return jsonify( res )
# #############################################################################
#############################################################################
#############################################################################
# clients routes
#############################################################################
#############################################################################
#############################################################################
#############################################################################
def new_client():
    if not request.json:
        reply={'status':'error','message':'json data Not provided'}
        return make_response(jsonify(reply), 400)
    record_data = request.json
    if not record_data.get('name'):
        reply={'status':'error','message':'[name] Not provided'}
        return make_response(jsonify(reply), 401)
    if not record_data.get('email'):
        reply={'status':'error','message':'[email] Not provided'}
        return make_response(jsonify(reply), 401)
    dbreply=db.dbapi_client(dbsession, 'register', record_data, filter_dict={}, caller_dict={}, call_level=-1,debug_level=-1)
    return jsonify( dbreply )
#############################################################################
def get_client(client_id):
    dbreply=db.dbapi_client(dbsession, 'get', {'client_id':client_id}, filter_dict={}, caller_dict={}, call_level=-1,debug_level=-1)
    return jsonify( dbreply )
#############################################################################
def update_client(client_id):
    if not request.json:
        reply={'status':'error','message':'json data Not provided'}
        return make_response(jsonify(reply), 400)
    update_record = request.json
    update_record.update({'client_id':client_id})
    dbreply=db.dbapi_client(dbsession, 'update', update_record, filter_dict={}, caller_dict={}, call_level=-1,debug_level=-1)
    return jsonify( dbreply )
#############################################################################
def confirm_client(client_id):
    update_record = request.json
    update_record.update({'client_id':client_id})
    dbreply=db.dbapi_client(dbsession, 'confirm', update_record, filter_dict={}, caller_dict={}, call_level=-1,debug_level=-1)
    return jsonify( dbreply )
#############################################################################
def unregister_client(client_id):
    update_record = request.json
    update_record.update({'client_id':client_id})
    dbreply=db.dbapi_client(dbsession, 'UnRegister', update_record, filter_dict={}, caller_dict={}, call_level=-1,debug_level=-1)
    return jsonify(dbreply)
#############################################################################
def delete_client(client_id):
    dbreply=db.dbapi_client(dbsession, 'delete', {'client_id':client_id}, filter_dict={}, caller_dict={}, call_level=-1,debug_level=-1)
    return jsonify( dbreply )
#############################################################################
def banksubscription_register(client_id, application_name,bank_id):
    this_application_name = request.headers.get('Registered-Application')
    if not this_application_name == application_name:
        msg = f'app {this_application_name} can not subscribe for app {application_name}'
        reply = {'api_status': 'error', 'api_message': msg}
        return make_response(jsonify(reply), 400)
        
    subscription_options = request.json
    allow_transactionHistory = subscription_options.get('allow_transactionHistory', False)
    allow_balance = subscription_options.get('allow_balance', False)
    allow_details = subscription_options.get('allow_details', False)
    allow_checkFundsAvailability = subscription_options.get('allow_checkFundsAvailability', False)
    payments_limit = subscription_options.get('payments_limit', 100)
    payments_currency = subscription_options.get('payments_currency', 'EUR')
    payments_amount = subscription_options.get('payments_amount', 10)
    
    reply = api.banksubscription_register(dbsession, 
        client_id=client_id, bank_id=bank_id, application_name=application_name,
        allow_transactionHistory=allow_transactionHistory, allow_balance=allow_balance,
        allow_details=allow_details, allow_checkFundsAvailability=allow_checkFundsAvailability,
        payments_limit=payments_limit, payments_currency=payments_currency, payments_amount=payments_amount
        )
    return jsonify(reply)
#############################################################################
def banksubscription_unregister(client_id,application_name,bank_id,subscription_id):
    reply = api.banksubscription_unregister(dbsession,client_id=client_id, bank_id=bank_id, application_name=application_name, subscription_id=subscription_id)
    return jsonify(reply)
#############################################################################
def bankaccount_remove(client_id,application_name,bank_id,account_id):
    reply = api.bankaccount_remove(dbsession,client_id=client_id, bank_id=bank_id, application_name=application_name, account_id=account_id)
    return jsonify(reply)
#############################################################################
def banksubscription_request_client_authorization(client_id,application_name,bank_id,subscription_id):
    this_application_name = request.headers.get('Registered-Application')
    if not this_application_name == application_name:
        msg = f'app {this_application_name} can not subscribe for app {application_name}'
        reply = {'api_status': 'error', 'api_message': msg}
        return make_response(jsonify(reply), 400)
        
    reply = api.banksubscription_request_authorization_from_client(dbsession,client_id, bank_id, subscription_id, application_name)
    return jsonify(reply)
#############################################################################
def banksubscription_create(client_id,application_name,bank_id):
    this_application_name = request.headers.get('Registered-Application')
    if not this_application_name == application_name:
        msg = f'app {this_application_name} can not subscribe for app {application_name}'
        reply = {'api_status': 'error', 'api_message': msg}
        return make_response(jsonify(reply), 400)
        
    subscription_options = request.json
    allow_transactionHistory = subscription_options.get('allow_transactionHistory', False)
    allow_balance = subscription_options.get('allow_balance', False)
    allow_details = subscription_options.get('allow_details', False)
    allow_checkFundsAvailability = subscription_options.get('allow_checkFundsAvailability', False)
    payments_limit = subscription_options.get('payments_limit', 100)
    payments_currency = subscription_options.get('payments_currency', 'EUR')
    payments_amount = subscription_options.get('payments_amount', 10)
    
    reply = api.banksubscription_create(dbsession,
        client_id=client_id, bank_id=bank_id, application_name=application_name,
        allow_transactionHistory=allow_transactionHistory, allow_balance=allow_balance,
        allow_details=allow_details, allow_checkFundsAvailability=allow_checkFundsAvailability,
        payments_limit=payments_limit, payments_currency=payments_currency, payments_amount=payments_amount
        )
    return jsonify(reply)

    # update_record = request.json
    # update_record.update({'client_id': client_id, 'bank_id': bank_id,'application_name':application_name})
    # client = db.clients.get(update_record)
    # if not client:
    #     msg = f'client not found'
    #     return {'api_status': 'error', 'api_message': msg}
    # if not client.get('status')=='Active':
    #     msg = f"client not Active.(status:{client.get('status','')})"
    #     return {'api_status': 'error', 'api_message': msg}

    # client_id=client.get('client_id')
    # client_email=client.get('email')

    # update_record.update({'owner_type': 'client'})
    # update_record.update({'owner_id': client_id})
    # update_record.update({'owner_name': client_email})

    # bank = db.banks.get(update_record)
    # if not bank:
    #     msg = f'bank not found'
    #     return {'api_status': 'error', 'api_message': msg}
    
    # if not bank.get('status')=='Active':
    #     msg = f"bank not Active.(status:{bank.get('status','')})"
    #     return {'api_status': 'error', 'api_message': msg}
        
    # bank_code = bank.get('bank_code')
    # bank_id = bank.get('bank_id')
    # #bank_BIC = bank.get('bank_BIC')

    # #here we need to invoke the bank api to get subscription
    # # bank_subscriptionID = 'tispaloastavizia'

    # # bank_subscription_record.update({'bank_subscriptionID': bank_subscriptionID})
    
    # # result=dbapi_bank_subscription_register(bank_subscription_record, user=user)
    # # return result

    # session['bank_code'] = bank_code
    # session['client_id'] = client_id
    # session.modified = True

    # create_result = openBankingAPI.create_subscription('bankofcyprus', allow_transactionHistory=True, allow_balance=True, allow_details=True, allow_checkFundsAvailability=True, payments_limit=1000, payments_currency='EUR', payments_amount=100)
    # print(create_result)
    # # #create subscription record
    # # create_result = boc_get_subscriptionId(access_token, allow_transactionHistory=allow_transactionHistory, allow_balance=allow_balance, allow_details=allow_details, allow_checkFundsAvailability=allow_checkFundsAvailability, payments_limit=payments_limit, payments_currency=payments_currency, payments_amount=payments_amount)   
    # if not create_result.get('status')=='success':
    #     return create_result

    # #get the subscription id
    # subscriptionId=create_result.get('return_value')
    # # log_api_interim_result('subscriptionId',subscriptionId)
    # subscriptionId=create_result.get('data',{}).get('subscriptionId')

    # session['subscription_id'] = subscriptionId
    # session.modified = True
    
    # reply = jsonify(create_result)
    # # reply.set_cookie('subscription_id', subscriptionId)
    # # reply.set_cookie('bank_code', bank_code)
    # # reply.set_cookie('client_id', client_id)

    # # dbreply = db.dbapi_client_banksubscription_register(create_result)

    # return reply
#############################################################################
def client_device_register(client_id,device_uid):
    update_record = request.json
    update_record.update({'client_id':client_id})
    update_record.update({'device_uid':device_uid})
    update_record.update({'status':'Active'})
    dbreply=db.dbapi_client_device(dbsession, 'Register', update_record, filter_dict={}, caller_dict={}, call_level=-1,debug_level=-1)
    return jsonify(dbreply)
#############################################################################
def client_device_unregister(client_id,device_uid):
    update_record = request.json
    update_record.update({'client_id':client_id})
    update_record.update({'device_uid':device_uid})
    update_record.update({'status':'Unregistered'})
    dbreply=db.dbapi_client_device(dbsession, 'UnRegister', update_record, filter_dict={}, caller_dict={}, call_level=-1,debug_level=-1)
    return jsonify(dbreply)
#############################################################################
def start_client_interactions(client_id):
    interaction_record={'client_id':client_id}
    # result = db.dbapi_interaction_start(record)
    dbreply=db.dbapi_interaction(dbsession, 'start', interaction_record, filter_dict={}, caller_dict={}, call_level=-1,debug_level=-1)
    return jsonify( dbreply )
#############################################################################
def finish_client_interactions(interaction_id,client_id):
    # record={'client_id':client_id}
    # result = db.dbapi_interaction_finish(record)
    interaction_record={'client_id':client_id}
    # result = db.dbapi_interaction_start(record)
    dbreply=db.dbapi_interaction(dbsession, 'finish', interaction_record, filter_dict={}, caller_dict={}, call_level=-1,debug_level=-1)
    return jsonify( dbreply )
#############################################################################
def add_client_interaction_message(client_id):
    if not request.json:
        reply={'status':'error','message':'json data Not provided'}
        return make_response(jsonify(reply), 400)
    message_record = request.json
    message_record.update({'client_id':client_id})
    dbreply=db.dbapi_interaction(dbsession, 'message', message_record, filter_dict={}, caller_dict={}, call_level=-1,debug_level=-1)
    return jsonify( dbreply )
##########################################################################################################################
#############################################################################
#############################################################################
#############################################################################
#############################################################################
# service providers routes
#############################################################################
#############################################################################
#############################################################################
#############################################################################
#############################################################################
#############################################################################
#############################################################################
# merchants routes
#############################################################################
#############################################################################
#############################################################################
#############################################################################
def get_merchants_list():
    # filterString=f"all"
    dbreply = db.dbapi_merchant(dbsession, 'LIST', {}, filter_dict={}, caller_dict={}, call_level=-1, debug_level=-1)
    return jsonify( dbreply )
#############################################################################
def new_merchant():
    if not request.json:
        reply={'status':'error','message':'json data Not provided'}
        return make_response(jsonify(reply), 400)
    record_data = request.json
    if not record_data.get('name'):
        reply={'status':'error','message':'[name] Not provided'}
        return make_response(jsonify(reply), 401)
    if not record_data.get('email'):
        reply={'status':'error','message':'[email] Not provided'}
        return make_response(jsonify(reply), 401)
    dbreply=db.dbapi_merchant(dbsession, 'register', record_data, filter_dict={}, caller_dict={}, call_level=-1,debug_level=-1)
    return jsonify( dbreply )
#############################################################################
def get_merchant(merchant_id):
    dbreply=db.dbapi_merchant(dbsession, 'get', {'merchant_id':merchant_id}, filter_dict={}, caller_dict={}, call_level=-1,debug_level=-1)
    return jsonify( dbreply )
#############################################################################
def update_merchant(merchant_id):
    if not request.json:
        reply={'status':'error','message':'json data Not provided'}
        return make_response(jsonify(reply), 400)
    update_record = request.json
    update_record.update({'merchant_id':merchant_id})
    dbreply=db.dbapi_merchant(dbsession, 'update', update_record, filter_dict={}, caller_dict={}, call_level=-1,debug_level=-1)
    return jsonify( dbreply )
#############################################################################
def confirm_merchant(merchant_id):
    update_record = request.json
    update_record.update({'merchant_id':merchant_id})
    dbreply=db.dbapi_merchant(dbsession, 'confirm', update_record, filter_dict={}, caller_dict={}, call_level=-1,debug_level=-1)
    return jsonify( dbreply )
#############################################################################
def unregister_merchant(merchant_id):
    update_record = request.json
    update_record.update({'merchant_id':merchant_id})
    dbreply=db.dbapi_merchant(dbsession, 'UnRegister', update_record, filter_dict={}, caller_dict={}, call_level=-1,debug_level=-1)
    return jsonify(dbreply)
#############################################################################
def delete_merchant(merchant_id):
    dbreply=db.dbapi_merchant(dbsession, 'delete', {'merchant_id':merchant_id}, filter_dict={}, caller_dict={}, call_level=-1,debug_level=-1)
    return jsonify(dbreply)
#############################################################################
# def merchant_banksubscription_register(merchant_id):
#     if not request.json:
#         reply={'status':'error','message':'json data Not provided'}
#         return make_response(jsonify(reply), 400)
#     update_record = request.json
#     update_record.update({'merchant_id':merchant_id})
#     dbreply = db.dbapi_merchant_bankaccount_register(update_record)
#     return jsonify(dbreply)
#############################################################################
#############################################################################
#############################################################################
def new_pointofsale(merchant_id):
    if not request.json:
        reply={'status':'error','message':'json data Not provided'}
        return make_response(jsonify(reply), 400)
    record_data = request.json
    if not record_data.get('name'):
        reply={'status':'error','message':'[name] Not provided'}
        return make_response(jsonify(reply), 401)
    record_data.update({'merchant_id':merchant_id}) 
    dbreply = db.dbapi_pointofsale_register(record_data)
    return jsonify( dbreply )
#############################################################################
def new_employee(merchant_id):
    if not request.json:
        reply={'status':'error','message':'json data Not provided'}
        return make_response(jsonify(reply), 400)
    record_data = request.json
    if not record_data.get('name'):
        reply={'status':'error','message':'[name] Not provided'}
        return make_response(jsonify(reply), 401)
    record_data.update({'merchant_id':merchant_id}) 
    dbreply = db.dbapi_employee_register(record_data)
    return jsonify( dbreply )
#############################################################################
#############################################################################
#############################################################################
# pointofsales routes
#############################################################################
#############################################################################
#############################################################################
def get_pointofsales_list():
    filterString=f"all"
    dbreply=db.retrieve_rows('pointofsales',filterString)
    return jsonify( dbreply )
#############################################################################
def get_pointofsale(pointofsale_id):
    dbreply=db.points_of_sale.get(pointofsale_id)
    return jsonify( dbreply )
#############################################################################
def get_pointofsale_with_code(pointofsale_code):
    filterJson={'pointofsale_code':pointofsale_code}
    dbreply=db.points_of_sale.get(filterJson)
    return jsonify( dbreply )
#############################################################################
def update_pointofsale(pointofsale_id):
    if not request.json:
        reply={'status':'error','message':'json data Not provided'}
        return make_response(jsonify(reply), 400)
    update_record = request.json
    update_record.update({'pointofsale_id':pointofsale_id})
    dbreply = db.dbapi_pointofsale_update(update_record)
    return jsonify( dbreply )
#############################################################################
def unregister_pointofsale(pointofsale_id):
    if not request.json:
        reply={'status':'error','message':'json data Not provided'}
        return make_response(jsonify(reply), 400)
    update_record = request.json
    update_record.update({'pointofsale_id':pointofsale_id})
    dbreply = db.dbapi_pointofsale_unregister(update_record)
    return jsonify(dbreply)
#############################################################################
def pointofsale_bankaccount_add(pointofsale_id,bank_account_id):
    if not request.json:
        reply={'status':'error','message':'json data Not provided'}
        return make_response(jsonify(reply), 400)
    update_record = request.json
    if not pointofsale_id:
        reply={'status':'error','message':'pointofsale_id Not provided'}
        return make_response(jsonify(reply), 400)
    if not update_record.get('bank_account_id'):
        reply={'status':'error','message':'bank_account_id Not provided'}
        return make_response(jsonify(reply), 400)
    update_record.update({'pointofsale_id':pointofsale_id})
    dbreply = db.dbapi_pointofsale_bankaccount_add(update_record)
    return jsonify(dbreply)
#############################################################################
def pointofsale_bankaccount_remove(pointofsale_id):
    if not pointofsale_id:
        reply={'status':'error','message':'pointofsale_id Not provided'}
        return make_response(jsonify(reply), 400)
    pos={'pointofsale_id':pointofsale_id}
    dbreply = db.dbapi_pointofsale_bankaccount_remove(pos)
    return jsonify(dbreply)
#############################################################################
def delete_pointofsale(pointofsale_id):
    dbreply=db.points_of_sale.delete(pointofsale_id)
    return jsonify( dbreply )
#############################################################################
def get_pointofsale_creditinfo_from_posuid(pointofsale_id):
    res = db.dbapi_pointofsale_credit_info(pointofsale_id)
    return jsonify( res )
#############################################################################
def start_pointofsale_interactions(pointofsale_id):
    record={'pointofsale_id':pointofsale_id}
    result = db.dbapi_interaction_start(record)
    return jsonify( result )
#############################################################################
def finish_pointofsale_interactions(pointofsale_id):
    record={'pointofsale_id':pointofsale_id}
    result = db.dbapi_interaction_finish(record)
    return jsonify( result )
#############################################################################
def add_pointofsale_interaction_message(pointofsale_id):
    if not request.json:
        reply={'status':'error','message':'json data Not provided'}
        return make_response(jsonify(reply), 400)
    message_record = request.json
    message_record.update({'pointofsale_id':pointofsale_id})
    result = db.dbapi_interaction_message_add(message_record)
    return jsonify( result )
#############################################################################
#############################################################################
# employee routes
#############################################################################
#############################################################################
#############################################################################
#############################################################################
#############################################################################
#############################################################################
#############################################################################
#############################################################################
# consumers routes
#############################################################################
#############################################################################
#############################################################################
#############################################################################
def get_consumers_list():
    # filterString=f"all"
    dbreply = db.dbapi_consumer(dbsession, 'LIST', {}, filter_dict={}, caller_dict={}, call_level=-1, debug_level=-1)
    return jsonify( dbreply )
#############################################################################
def new_consumer():
    if not request.json:
        reply={'status':'error','message':'json data Not provided'}
        return make_response(jsonify(reply), 400)
    record_data = request.json
    if not record_data.get('name'):
        reply={'status':'error','message':'[name] Not provided'}
        return make_response(jsonify(reply), 401)
    if not record_data.get('email'):
        reply={'status':'error','message':'[email] Not provided'}
        return make_response(jsonify(reply), 401)
    dbreply=db.dbapi_consumer(dbsession, 'register', record_data, filter_dict={}, caller_dict={}, call_level=-1,debug_level=-1)
    return jsonify( dbreply )
#############################################################################
def get_consumer(consumer_id):
    dbreply=db.dbapi_consumer(dbsession, 'get', {'consumer_id':consumer_id}, filter_dict={}, caller_dict={}, call_level=-1,debug_level=-1)
    return jsonify( dbreply )
#############################################################################
def update_consumer(consumer_id):
    if not request.json:
        reply={'status':'error','message':'json data Not provided'}
        return make_response(jsonify(reply), 400)
    update_record = request.json
    update_record.update({'consumer_id':consumer_id})
    dbreply=db.dbapi_consumer(dbsession, 'update', update_record, filter_dict={}, caller_dict={}, call_level=-1,debug_level=-1)
    return jsonify( dbreply )
#############################################################################
def confirm_consumer(consumer_id):
    update_record = request.json
    update_record.update({'consumer_id':consumer_id})
    dbreply=db.dbapi_consumer(dbsession, 'confirm', update_record, filter_dict={}, caller_dict={}, call_level=-1,debug_level=-1)
    return jsonify( dbreply )
#############################################################################
def unregister_consumer(consumer_id):
    update_record = request.json
    update_record.update({'consumer_id':consumer_id})
    dbreply=db.dbapi_consumer(dbsession, 'UnRegister', update_record, filter_dict={}, caller_dict={}, call_level=-1,debug_level=-1)
    return jsonify(dbreply)
#############################################################################
def delete_consumer(consumer_id):
    dbreply=db.dbapi_consumer(dbsession, 'delete', {'consumer_id':consumer_id}, filter_dict={}, caller_dict={}, call_level=-1,debug_level=-1)
    return jsonify(dbreply)
#############################################################################
def consumer_banksubscription_register(consumer_id):
    if not request.json:
        reply={'status':'error','message':'json data Not provided'}
        return make_response(jsonify(reply), 400)
    update_record = request.json
    update_record.update({'consumer_id':consumer_id})
    dbreply = db.dbapi_consumer_banksubscription_register(update_record)
    return jsonify(dbreply)
#############################################################################
def start_consumer_interactions(consumer_id):
    record={'consumer_id':consumer_id}
    result = db.dbapi_interaction_start(record)
    return jsonify( result )
##########################################################################################################################
#############################################################################
def finish_consumer_interactions(consumer_id):
    record={'consumer_id':consumer_id}
    result = db.dbapi_interaction_finish(record)
    return jsonify( result )
##########################################################################################################################
#############################################################################
#############################################################################
def add_consumer_interaction_message(consumer_id):
    if not request.json:
        reply={'status':'error','message':'json data Not provided'}
        return make_response(jsonify(reply), 400)
    message_record = request.json
    message_record.update({'consumer_id':consumer_id})
    result = db.dbapi_interaction_message_add(message_record)
    return jsonify( result )
#############################################################################

#############################################################################
#############################################################################
#############################################################################
# banks routes
#############################################################################
#############################################################################
#############################################################################
def get_banks_list():
    dbreply = db.dbapi_bank(dbsession, 'LIST', {}, filter_dict={}, caller_dict={}, call_level=-1, debug_level=-1)
    return jsonify( dbreply )
#############################################################################
def new_bank():
    if not request.json:
        reply={'status':'error','message':'json data Not provided'}
        return make_response(jsonify(reply), 400)
    record_data = request.json
    record_data = request.json
    if not record_data.get('bank_name'):
        reply={'status':'error','message':'[name] Not provided'}
        return make_response(jsonify(reply), 401)
    if not record_data.get('bank_code'):
        reply={'status':'error','message':'[bank_code] Not provided'}
        return make_response(jsonify(reply), 401)
    if not record_data.get('bank_BIC'):
        reply={'status':'error','message':'[bank_BIC] Not provided'}
        return make_response(jsonify(reply), 401)
    dbreply=db.dbapi_bank(dbsession, 'register', record_data, filter_dict={}, caller_dict={}, call_level=-1,debug_level=-1)
    return jsonify( dbreply )
#############################################################################
def get_bank(bank_id):
    dbreply=db.dbapi_bank(dbsession, 'get', {'bank_id':bank_id}, filter_dict={}, caller_dict={}, call_level=-1,debug_level=-1)
    return jsonify( dbreply )
#############################################################################
def update_bank(bank_id):
    if not request.json:
        reply={'status':'error','message':'json data Not provided'}
        return make_response(jsonify(reply), 400)
    update_record = request.json
    update_record.update({'bank_id':bank_id})
    dbreply=db.dbapi_bank(dbsession, 'update', update_record, filter_dict={}, caller_dict={}, call_level=-1,debug_level=-1)
    return jsonify( dbreply )
#############################################################################
def confirm_bank(bank_id):
    update_record = request.json
    update_record.update({'bank_id':bank_id})
    dbreply=db.dbapi_bank(dbsession, 'activate', update_record, filter_dict={}, caller_dict={}, call_level=-1,debug_level=-1)
    return jsonify( dbreply )
#############################################################################
def unregister_bank(bank_id):
    update_record = request.json
    update_record.update({'bank_id':bank_id})
    dbreply=db.dbapi_bank(dbsession, 'deactivate', update_record, filter_dict={}, caller_dict={}, call_level=-1,debug_level=-1)
    return jsonify(dbreply)
#############################################################################
def delete_bank(bank_id):
    dbreply=db.dbapi_bank(dbsession, 'delete', {'bank_id':bank_id}, filter_dict={}, caller_dict={}, call_level=-1,debug_level=-1)
    return jsonify( dbreply )
##########################################################################################################################################################
#############################################################################
#############################################################################
#############################################################################
#############################################################################
#############################################################################
#############################################################################

# @app.route('/openbanking/api/v1/merchants', methods = ['PUT','POST'])
# #@auth.login_required
# def new_merchant():
#     if not request.json:
#         reply={'status':'error','message':'json data Not provided'}
#         return make_response(jsonify(reply), 400)
#         #abort(400)
#     request_data = request.json
#     #basic validations before calling the database api
#     if not request_data.get('merchant_email'):
#         reply={'status':'error','message':'[merchant_email] Not provided'}
#         return make_response(jsonify(reply), 401)
#     if not request_data.get('merchant_name'):
#         reply={'status':'error','message':'[merchant_name] Not provided'}
#         return make_response(jsonify(reply), 401)
#     if not request_data.get('merchant_code'):
#         reply={'status':'error','message':'[merchant_code] Not provided'}
#         return make_response(jsonify(reply), 401)
#     dbreply = db.insert_row('merchants', request_data)
#     # print('dbreply =',dbreply)
#     # print('jsonify( dbreply ) =',jsonify( dbreply ))
#     return jsonify( dbreply )
# #############################################################################
# @app.route('/openbanking/api/v1/merchants/pos/<merchant_code>/<pos_code>', methods = ['GET'])
# #@auth.login_required
# def get_merchant_pos_by_code(merchant_code,pos_code):
#     dbreply=db.retrieve_row('pointsofsale',f"merchant_code='{merchant_code}' and pos_code='{pos_code}'")
#     print('/openbanking/api/v1/merchants/pos/<merchant_code>/<pos_code>',dbreply)
#     return jsonify( dbreply )
# #############################################################################
# @app.route('/openbanking/api/v1/merchants/pos/<merchant_code>/<pos_code>', methods = ['PATCH'])
# #@auth.login_required
# def change_merchant_pos_by_code(merchant_code,pos_code):
#     if not request.json:
#         reply={'status':'error','message':'json data Not provided'}
#         return make_response(jsonify(reply), 400)
#         #abort(400)
#     request_data = request.json
#     # #basic validations before calling the database api
#     # if not request_data.get('email'):
#     #     reply={'status':'error','message':'[email] Not provided'}
#     #     return make_response(jsonify(reply), 401)
#     # if not request_data.get('name'):
#     #     reply={'status':'error','message':'[name] Not provided'}
#     #     return make_response(jsonify(reply), 401)
#     dbreply = db.update_row('pointsofsale', f"merchant_code='{merchant_code}' and pos_code='{pos_code}'", request_data)
#     # print('dbreply =',dbreply)
#     # print('jsonify( dbreply ) =',jsonify( dbreply ))
#     return jsonify( dbreply )
# #############################################################################
# @app.route('/openbanking/api/v1/merchants/pos', methods = ['PUT','POST'])
# #@auth.login_required
# def new_pointofsale():
#     if not request.json:
#         reply={'status':'error','message':'json data Not provided'}
#         return make_response(jsonify(reply), 400)
#         #abort(400)
#     request_data = request.json
#     #basic validations before calling the database api
#     if not request_data.get('pos_code'):
#         reply={'status':'error','message':'[pos_code] Not provided'}
#         return make_response(jsonify(reply), 401)
#     if not request_data.get('merchant_code'):
#         reply={'status':'error','message':'[merchant_code] Not provided'}
#         return make_response(jsonify(reply), 401)
#     dbreply = db.insert_row('pointsofsale', request_data)
#     # print('dbreply =',dbreply)
#     # print('jsonify( dbreply ) =',jsonify( dbreply ))
#     return jsonify( dbreply )
# #############################################################################
# @app.route('/openbanking/api/v1/merchants/pos/<merchant_code>', methods = ['GET'])
# #@auth.login_required
# def list_merchant_pos(merchant_code):
#     dbreply=db.retrieve_row('pointsofsale',f"merchant_code='{merchant_code}'")
#     print('/openbanking/api/v1/merchants/pos/<merchant_code>',dbreply)
#     return jsonify( dbreply )
# #############################################################################
#############################################################################
#############################################################################
#############################################################################
# @app.route('/openbanking/api/v1/test', methods = ['PUT','POST'])
# #@auth.login_required
# def create_test():
#     try:
#         if not request.json:
#             print('@@@@@@ no json=============')
#         else:
#             print('request.json =',json.dumps(request.json))
#     except:
#         print('@@@@@@request.json failed============')
#         pass
#     # try:    
#     #     x=request.get_json(force=True)
#     #     print('===new=request.get_json()==',x)
#     # except:
#     #     row_data={}
#     #     print('3333333-request.get_json() FAILED')
#     #     pass

#     try:    
#         row_data=request.json
#         print('===new=request.json==',row_data)
#     except:
#         print('3333333-request.json FAILED')
#         pass

#     try:    
#         data=request.data
#         print('===new=request.data==', data)
#     except:
#         print('3333333-request.data FAILED')
#         pass
#     # if not request.json or not 'title' in request.json:
#     #     abort(400)
    
#     #  row_data= {
#     #     'id': tasks[-1]['id'] + 1,
#     #     'title': request.json['title'],
#     #     'description': request.json.get('description', ""),
#     #     'done': False
#     # }
#     res = db.insert_row('clients', row_data)
#     print('res =',res)
#     print('jsonify( res ) =',jsonify( res ))
#     #return jsonify( { 'task': make_public_task(task) } ), 201
#     return jsonify( res )

# @app.route('/openbanking/api/v1/tasks/<int:task_id>', methods = ['PUT'])
# @auth.login_required
# def update_task(task_id):
#     task = filter(lambda t: t['id'] == task_id, tasks)
#     if len(task) == 0:
#         abort(404)
#     if not request.json:
#         abort(400)
#     if 'title' in request.json and type(request.json['title']) != unicode:
#         abort(400)
#     if 'description' in request.json and type(request.json['description']) is not unicode:
#         abort(400)
#     if 'done' in request.json and type(request.json['done']) is not bool:
#         abort(400)
#     task[0]['title'] = request.json.get('title', task[0]['title'])
#     task[0]['description'] = request.json.get('description', task[0]['description'])
#     task[0]['done'] = request.json.get('done', task[0]['done'])
#     return jsonify( { 'task': make_public_task(task[0]) } )
    
# @app.route('/openbanking/api/v1/tasks/<int:task_id>', methods = ['DELETE'])
# @auth.login_required
# def delete_task(task_id):
#     task = filter(lambda t: t['id'] == task_id, tasks)
#     if len(task) == 0:
#         abort(404)
#     tasks.remove(task[0])
#     return jsonify( { 'result': True } )
##########################################################################################################################
##########################################################################################################################
##########################################################################################################################
##########################################################################################################################
# server start: 
##########################################################################################################################
##########################################################################################################################
##########################################################################################################################
##########################################################################################################################
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
    # user_rec = {'email': 'xyx@gmail.com'}
    # res=db.dbapi_user(dbsession, 'get', user_rec, action_filter={}, caller_area={})
    # user = res.get('api_data', {})
    # if not user:
    #     user_id = ''
    # else:
    #     user_id = user.get('user_id')
    # print('user =', user_id)
    
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

    caller_area.update({'debug_level': 99, 'caller_area_input_debug': False,})

    _process_name = "_test_ganimides_server"
    _process_entity = ''
    _process_action = 'test'
    _process_msgID = 'process:_test_ganimides_server'

    _process_identity_kwargs = {'type': 'process', 'module': module_id, 'name': _process_name, 'action': _process_action, 'entity': _process_entity, 'msgID': _process_msgID,}
    _process_adapters_kwargs = {'dbsession': None}
    _process_log_kwargs = {'indent_method': 'AUTO', 'indent_level':None}
    _process_debug_level = get_debug_level(caller_area.get('debug_level'), **_process_identity_kwargs, **_process_adapters_kwargs)
    _process_debug_files = get_debug_files(_process_debug_level, **_process_identity_kwargs, **_process_adapters_kwargs)
    _process_debug_kwargs={'debug_level':_process_debug_level,'debug_files':_process_debug_files}

    _process_signature = build_process_signature(**_process_identity_kwargs, **_process_adapters_kwargs, **_process_debug_kwargs, **_process_log_kwargs)
    _process_call_area = build_process_call_area(_process_signature, caller_area)

    dbsession = db.get_dbsession(**_process_call_area)
    
    res = db.dbapi_device_log(dbsession, device_uid, application_name, geolocation_lat, geolocation_lon, client_id,caller_area=_process_call_area)
    # print('dbapi_device_log',res)

    res = db.dbapi_application_credentials_are_valid(dbsession, application_name, application_client_id, application_client_secretKey,caller_area=_process_call_area)
    # print('dbapi_application_credentials_are_valid',res)

    access_token = 'xxxxxxxxxxxxxxxx'
    res = db.dbapi_token_is_valid(dbsession, access_token,caller_area=_process_call_area)
    # print('dbapi_token_is_valid',res)

    token_request = caller_area
    token_request.update({'token_scope':'application_service','token_type':''})
    res = get_access_token(token_request)
    token = res.get('api_data', {}).get('token')
    if not token:
        print('token get failed')
        exit(0)
    print('token =', token)

    res = get_clients_list({'client_type':'merchant'})
    print(res)

    merchant_id = '6d1d1a14-e91b-11e9-aae5-33b843d61993'
    bank_id = 'bankofcyprus'
    subscription_options={}
    res = merchant_banksubscription_register(merchant_id, application_name, bank_id, subscription_options)
    print(res)

    # banks = dbsession.get_rows(db.BANK, {'status':'Active'}, caller_area=_process_call_area)
    # merchants = dbsession.get_rows(db.MERCHANT, {}, caller_area=_process_call_area)
    # for ix1 in range(0, len(merchants)):
    #     merchant = merchants[ix1]
    #     for ix2 in range(0,len(banks)):
    #         bank = banks[ix2]
    #         subscription_options={}
    #         res = merchant_banksubscription_register(merchant.merchant_id, application_name, bank.bank_id, subscription_options)
    #         print(res)

    bank_id = 'bankofcyprus'
    authorization_code = '1212122121simulated_authorization_code2121212112121'
    _process_call_area.update({'simulation_enabled':True})
    reply=api.banksubscription_receive_authorization_from_client(dbsession, bank_id, authorization_code, caller_area=_process_call_area)
    print(reply)

    dbsession.close(**_process_call_area)

        # #db.database_schema.connect()
        # #app.run(debug=False)
        # # app.run(host='0.0.0.0', port=5555)
        # #app.run(host='127.0.0.1', port=5555)
        # #app.run(debug=False,port=5555,threaded=True)
        # app.run(debug=False,port=5555,threaded=False)
