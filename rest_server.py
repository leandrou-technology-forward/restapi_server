#@@@@@# -*- coding: utf-8 -*-
#!flask/bin/python
#@@@@@# -*- coding: utf-8 -*-

import os
import sys
if not (os.path.dirname(__file__) in sys.path): sys.path.append(os.path.dirname(__file__))
#print(sys.path)
import datetime
import secrets
import requests

import random
import time

from flask import Flask, jsonify, abort, request, make_response, url_for,redirect,render_template
from flask_httpauth import HTTPBasicAuth
from flask import json
from flask import session, g

from _onlineApp import thisApp
from _onlineApp import build_process_signature, build_process_call_area, get_debug_level, get_debug_files
from _onlineApp import log_process_start, log_process_finish, log_process_message
from _onlineApp import confirm_token
from _onlineApp import Fore

# from _tokenServices import token_is_valid
# from colorama import Fore
from ganimides_server import  ganimides_database as db
from ganimides_server import  ganimides_api as api
##########################################################################################################################
# ##########################################################################################################################
# Securing Python APIs with Auth0
# Securing Python APIs with Auth0 is very easy and brings a lot of great features to the table. With Auth0, we only have to write a few lines of code to get:

# A solid identity management solution, including single sign-on
#https: // auth0.com / user - management
#https://auth0.com/docs/sso/single-sign-on
# User management
# Support for social identity providers (like Facebook, GitHub, Twitter, etc.)
#https://auth0.com/docs/identityproviders
# Enterprise identity providers (Active Directory, LDAP, SAML, etc.)
#https://auth0.com/enterprise
#  Our own database of users
# For example, to secure Python APIs written with Flask, we can simply create a requires_auth decorator:
##########################################################################################################################
# init
##########################################################################################################################
##########################################################################################################################
##########################################################################################################################
app = Flask(__name__, static_url_path="")
app.secret_key='spithas490px!' # we need it to access g=global and session
#app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite://C:\\Users\\User\\Documents\\my Projects\\Systems_Development\\Development_Environment\\ganimides.db'
#db = SQLAlchemy(app)
# db = SQLAlchemy(app)

auth = HTTPBasicAuth()
request_headers_json = {}
request_params_json = {}

# dbsession = db.get_dbsession(debug=99)
# dbsession.close()
# dbsession=None
#sexy_session = requests.Session()
    #############################################################################################
    # flask config
    #############################################################################################
    # SECRET_KEY = 'my_precious'
    # SECURITY_PASSWORD_SALT = 'my_precious_two'
    # DEBUG = False
    # BCRYPT_LOG_ROUNDS = 13
    # WTF_CSRF_ENABLED = True
    # DEBUG_TB_ENABLED = False
    # DEBUG_TB_INTERCEPT_REDIRECTS = False

##########################################################################################################################
debug=False
##########################################################################################################################
module_ProgramName = os.path.splitext(os.path.basename(__file__))[0]
module_id = '{}'.format(module_ProgramName)
module_version = 0.1
##########################################################################################################################
_process_call_area = {}
##########################################################################################################################
##########################################################################################################################
def get_headers(thisRequest):
    if debug:
        print('\nheaders(request.headers):')
    request_headers_json={}
    ix = 0
    for entry in thisRequest.headers:
        ix = ix + 1
        k = entry[0]
        v = entry[1]
        key=k.lower().replace('-','_')
        request_headers_json.update({key:v})
        if debug:
            msg=f"o header param {ix}: {entry[0]} ({key}) = {v}"
            print('   ',msg)
    #print(request_headers_json)
    return request_headers_json
##########################################################################################################################
def get_params(thisRequest):
    if debug:
        print('\nparams(request.arqs):')
    request_params_json = {}
    # print(request.args)
    ix = 0
    for k in thisRequest.args:
        ix = ix + 1
        v = thisRequest.args.get(k)
        key = k.lower().replace('-', '_')
        request_params_json.update({key: v})
        if debug:
            msg=f"o param {ix}: {k} ({key}) = {v}"
            print('   ',msg)
    #print('request_params_json-->',request_params_json)
    return request_params_json
##########################################################################################################################
def make_token():
    """
    Creates a cryptographically-secure, URL-safe string
    """
    return secrets.token_urlsafe(16)  
# Format error response and append status code
##########################################################################################################################
def quick_log(what):
    rec=f'{datetime.datetime.now()}|{what}'+'\n'
    with open("debug_log.txt", "a") as myfile:
        myfile.write(rec)
##########################################################################################################################
def is_human(parCaptchaResponse):
    """ Validating recaptcha response from google server
        Returns True captcha test passed for submitted form else returns False.
    """
    # log_function_start('is_human')
    # log_param('captcha_response', parCaptchaResponse)

    secret = app.config.get('RECAPTCHA_PRIVATE_KEY')
    # log_variable('RECAPTCHA_PRIVATE_KEY', secret)
    request_url = "https://www.google.com/recaptcha/api/siteverify"
    # log_variable('request_url', request_url)
    payload = {'response':parCaptchaResponse, 'secret':secret}
    # log_variable('payload', payload)
    response = requests.post("https://www.google.com/recaptcha/api/siteverify", payload)
    # log_variable('response', response)
    response_text = json.loads(response.text)
    print('google recaptcha response_text', response_text)
    # log_function_finish('is_human')
    return response_text['success']
##########################################################################################################################
def message_page(message_type='', message='', secondary_message='', message_description='', title='', application_name='', application_color='', application_copywrite='', application_logo='', error_code=0):
    if application_name:
        res = db.dbapi_application(g.dbsession, 'get', {'application_name':application_name}, caller_area=g.caller_area)
        application_rec = res.get('api_data', {})
        application_logo = application_rec.get('application_logo')
        application_color = application_rec.get('application_color')
        application_copywrite = application_rec.get('application_copywrite')
    if not application_logo:
        application_logo = 'ganimides_logo.gif'
    if not application_color:
        application_color = 'blue'
    if not application_copywrite:
        application_copywrite = 'leandrou-technology-forward-ltd, 2019'

    if not title:
        title = 'ganimides'

    message_page = render_template(
        'message_page.html',
        message_type=message_type,
        message=message,
        secondary_message=secondary_message,
        message_description=message_description,
        error_code=error_code,
        title=title,
        application_name=application_name,
        application_color=application_color,
        logo=application_logo,
        copywrite=application_copywrite,
    )
    return message_page    
##########################################################################################################################
def application_page(page_template, message_type='', message='', secondary_message='', message_description='', title='', application_name='', application_color='', application_copywrite='', application_logo='', error_code=0, disable_input=False,errors=[],error=''):
    if application_name:
        res = db.dbapi_application(g.dbsession, 'get', {'application_name':application_name}, caller_area=g.caller_area)
        application_rec = res.get('api_data', {})
        application_logo = application_rec.get('application_logo')
        application_color = application_rec.get('application_color')
        application_copywrite = application_rec.get('application_copywrite')
    if not application_logo:
        application_logo = 'ganimides_logo.gif'
    if not application_color:
        application_color = 'blue'
    if not application_copywrite:
        application_copywrite = 'leandrou-technology-forward-ltd, 2019'

    if not title:
        title = 'ganimides'

    app_page = render_template(
        page_template,
        message_type=message_type,
        message=message,
        secondary_message=secondary_message,
        message_description=message_description,
        error=error,
        errors=errors,
        error_code=error_code,
        title=title,
        application_name=application_name,
        application_color=application_color,
        logo=application_logo,
        copywrite=application_copywrite,
        disable_input=disable_input,
    )
    return app_page    
##########################################################################################################################

# def get_token_auth_header():
#     """Obtains the access token from the Authorization Header
#     """
#     auth = request.headers.get("Authorization", None)
#     if not auth:
#         raise AuthError({"code": "authorization_header_missing",
#                         "description":
#                             "Authorization header is expected"}, 401)

#     parts = auth.split()

#     if parts[0].lower() != "bearer":
#         raise AuthError({"code": "invalid_header",
#                         "description":
#                             "Authorization header must start with"
#                             " Bearer"}, 401)
#     elif len(parts) == 1:
#         raise AuthError({"code": "invalid_header",
#                         "description": "Token not found"}, 401)
#     elif len(parts) > 2:
#         raise AuthError({"code": "invalid_header",
#                         "description":
#                             "Authorization header must be"
#                             " Bearer token"}, 401)

#     token = parts[1]
#     return token

# def requires_auth(f):
#     """Determines if the access token is valid
#     """
#     @wraps(f)
#     def decorated(*args, **kwargs):
#         token = get_token_auth_header()
#         jsonurl = urlopen("https://"+AUTH0_DOMAIN+"/.well-known/jwks.json")
#         jwks = json.loads(jsonurl.read())
#         unverified_header = jwt.get_unverified_header(token)
#         rsa_key = {}
#         for key in jwks["keys"]:
#             if key["kid"] == unverified_header["kid"]:
#                 rsa_key = {
#                     "kty": key["kty"],
#                     "kid": key["kid"],
#                     "use": key["use"],
#                     "n": key["n"],
#                     "e": key["e"]
#                 }
#         if rsa_key:
#             try:
#                 payload = jwt.decode(
#                     token,
#                     rsa_key,
#                     algorithms=ALGORITHMS,
#                     audience=API_AUDIENCE,
#                     issuer="https://"+AUTH0_DOMAIN+"/"
#                 )
#             except jwt.ExpiredSignatureError:
#                 raise AuthError({"code": "token_expired",
#                                 "description": "token is expired"}, 401)
#             except jwt.JWTClaimsError:
#                 raise AuthError({"code": "invalid_claims",
#                                 "description":
#                                     "incorrect claims,"
#                                     "please check the audience and issuer"}, 401)
#             except Exception:
#                 raise AuthError({"code": "invalid_header",
#                                 "description":
#                                     "Unable to parse authentication"
#                                     " token."}, 400)

#             _app_ctx_stack.top.current_user = payload
#             return f(*args, **kwargs)
#         raise AuthError({"code": "invalid_header",
#                         "description": "Unable to find appropriate key"}, 400)
#     return decorated
##########################################################################################################################
##########################################################################################################################
##########################################################################################################################
# authorization
##########################################################################################################################
##########################################################################################################################
##########################################################################################################################
@auth.get_password
def get_password(username):
    if username == 'miguel':
        return 'python'
    return None
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 
@auth.error_handler
def unauthorized():
    message = '403 - Unauthorized access'
    secondary_message=''
    error_code = 403
    result="error"
    return render_template('verification_result_page.html', message=message, secondary_message=secondary_message, result=result, error_code=error_code)
    # return make_response(jsonify( { 'error': 'Unauthorized access' } ), 403)
    # return 403 instead of 401 to prevent browsers from displaying the default auth dialog
    # return render_template('404.html', message=message, secondary_message=secondary_message, result=result, error_code=error_code)
##########################################################################################################################
##########################################################################################################################
##########################################################################################################################
# app error handlers
##########################################################################################################################
##########################################################################################################################
##########################################################################################################################
@app.errorhandler(400)
def not_found_400(error):
    return make_response(jsonify( { 'error': 'Bad request' } ), 400)
    # message = '400 - bad request'
    # secondary_message=''
    # error_code = 404
    # result="error"
    # return render_template('verification_result_page.html', message=message, secondary_message=secondary_message, result=result, error_code=error_code)
    # return render_template('400.html', message=message, secondary_message=secondary_message, result=result, error_code=error_code)
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 
@app.errorhandler(404)
def not_found_404(error):
    return make_response(jsonify( { 'error': 'Page Not found' } ), 404)
    # message = '404 - not found'
    # secondary_message=''
    # error_code = 404
    # result="error"
    # return render_template('verification_result_page.html', message=message, secondary_message=secondary_message, result=result, error_code=error_code)
    # return render_template('404.html', message=message, secondary_message=secondary_message, result=result, error_code=error_code)
##########################################################################################################################
##########################################################################################################################
##########################################################################################################################
# before_request processing (authenticate each request base on authentication_method stored in request.headers)
##########################################################################################################################
##########################################################################################################################
##########################################################################################################################
@app.before_request
def before_request_func():

    device_uid = request.headers.get('Device-Uid','?')
    user_id = '6701d6a8-e91b-11e9-98c9-79d91b2c4899'
    
    # get a dbsession from ganimides server
    dbsession = db.get_dbsession(debug=-1)

    print('')
    print(f'{Fore.RED}==>{Fore.RESET} device {Fore.YELLOW}{device_uid}{Fore.RESET} dbsession {Fore.YELLOW}{dbsession.session_id}{Fore.RESET}')
    print(f'{Fore.RED}==>{Fore.RESET} {Fore.GREEN}{request.method}{Fore.RESET} {Fore.LIGHTWHITE_EX}{request.path}{Fore.RESET}')

    msg_id = f'{device_uid}|{dbsession.session_id}|{request.method}|{request.path}'

    # try:
    #     prev_session_id = session["session_id"]
    # except:
    #     prev_session_id = "bobbi"
    # session["session_id"] = dbsession.session_id

    g.username = "root"
    g.dbsession = dbsession
    g.msg_id = msg_id
    g.user_id = user_id
    # try:
    #     g.bobbi = g.bobbi + 1
    #     session["bobbi"] = session["bobbi"] + 1
    # except:
    #     g.bobbi = 0
    #     session["bobbi"] = 0
        
    # print(f'{Fore.RED}==>{Fore.RESET} prev_session_id {Fore.YELLOW}{prev_session_id}{Fore.RESET}')
    # print(f'{Fore.RED}==>{Fore.RESET} session["bobbi"] {Fore.YELLOW}{session["bobbi"]}{Fore.RESET}')
    # print(f'{Fore.RED}==>{Fore.RESET} g.bobbi {Fore.YELLOW}{ g.bobbi}{Fore.RESET}')
    # print(f'{Fore.RED}==>{Fore.RESET} sexy_session {Fore.YELLOW}{sexy_session.headers.get("dbsession_id")}{Fore.RESET}')
    # print(f'{Fore.RED}==>{Fore.RESET} session_id {Fore.YELLOW}{session["session_id"]}{Fore.RESET}')

    if debug: quick_log('START :' + g.msg_id)
    
    # randomness=random.randint(0, 5)
    # time.sleep(random.randint(0, randomness))

    #sexy_session.auth = ('user', 'pass')
    # if not sexy_session.headers.get('dbsession'):
    #     sexy_session.headers.update({'dbsession': dbsession})
    # if not sexy_session.headers.get('dbsession_id'):
    #     sexy_session.headers.update({'dbsession_id': dbsession.session_id})
    #     print('ooooooooo','sexy_session_id added to flask session',sexy_session.headers.get('dbsession_id'))

    caller_area={'debug_level':-1,'debug_template':'SESSION_ONLY'}
    caller_area={'debug_level':-1,'debug_template':'FULL'}
    caller_area = {'debug_level': -1, 'caller_area_input_debug': False,}

    g.caller_area = caller_area

    caller_area.update({'user_id':user_id})
    g.caller_area = caller_area

    _process_name = "rest_apiserver"
    _process_entity = ''
    _process_action = 'api_service'
    _process_msgID = 'rest_apiserver'
    _process_type = 'restapi_service'

    #######################
    _process_identity_kwargs = {'type': _process_type, 'module': module_id, 'name': _process_name, 'action': _process_action, 'entity': _process_entity, 'msgID': _process_msgID,}
    _process_adapters_kwargs = {'dbsession': dbsession}
    _process_log_kwargs = {'indent_method': 'AUTO', 'indent_level':None}
    _process_debug_level = get_debug_level(caller_area.get('debug_level'), **_process_identity_kwargs, **_process_adapters_kwargs)
    _process_debug_files = get_debug_files(_process_debug_level, **_process_identity_kwargs, **_process_adapters_kwargs)
    _process_debug_kwargs={'debug_level':_process_debug_level,'debug_files':_process_debug_files}
    _process_signature = build_process_signature(**_process_identity_kwargs, **_process_adapters_kwargs, **_process_debug_kwargs, **_process_log_kwargs)
    _process_call_area = build_process_call_area(_process_signature, caller_area)
    #######################
    g.caller_area = _process_call_area
    #######################
    if request.path.upper().find('/openbanking/api/'.upper()) >=0:
        application_name = request.headers.get('Registered-Application')
        application_client_id = request.headers.get('Registered-Application-CLIENT-Id')
        application_client_secretKey = request.headers.get('Registered-Application-CLIENT-Secretkey')
        client_id = request.headers.get('CLIENT-Id')
        client_secretKey = request.headers.get('CLIENT-Secretkey')

        #from json format
        #request_headers_json = get_headers(request)
        # request_params_json=get_params(request)
        # all lower case from json version of headers
        # application_name = request_headers_json.get('registered_application','')
        # application_client_id = request_headers_json.get('registered_application_client_id', '')
        # application_client_secretKey = request_headers_json.get('registered_application_client_secretkey', '')

        if not application_name or not application_client_id or not application_client_secretKey:
            reply={'api_status':'error','api_message':'registered application credentials not provided'}
            return make_response(jsonify(reply), 403)
        caller_area.update({'application_name': application_name, 'application_client_id': application_client_id})

        if client_id:
            caller_area.update({'client_id': client_id, 'client_secretKey': client_secretKey})
            
        device_uid = request.headers.get('Device-Uid')
        if device_uid:
            caller_area.update({'device_uid':device_uid})
        geolocation_lat = request.headers.get('Geolocation-Lat','0')
        geolocation_lon = request.headers.get('Geolocation-Lon','0')
        if geolocation_lat > '0':
            caller_area.update({'geolocation_lat':geolocation_lat,'geolocation_lon':geolocation_lon})
        ################################
        _process_call_area = build_process_call_area(_process_signature, caller_area)
        g.caller_area = _process_call_area
        ################################

        if device_uid:
            db.dbapi_device_log(dbsession, device_uid, application_name, geolocation_lat, geolocation_lon, client_id, caller_area=_process_call_area)

        authentication_method = request.headers.get('Authentication-Method')
        if authentication_method == 'access_token':
            access_token = request.headers.get('Access-Token')        
            if not access_token:
                reply={'api_status':'error','api_message':'access token not provided'}
                return make_response(jsonify(reply), 403)
            # local validation first
            # but we need to implement the same in database
            # if not token_is_valid(access_token):
            #     reply={'api_status':'error','api_message':'expired access token used for authentication'}
            #     return make_response(jsonify(reply), 403)
            if not db.dbapi_token_is_valid(dbsession,access_token,caller_area=_process_call_area):
                reply={'api_status':'error','api_message':'invalid or expired access token'}
                return make_response(jsonify(reply), 403)
            if debug:
                print('OK, authentication_method:',authentication_method)
        elif authentication_method == 'registered_application_credentials':
            if not db.dbapi_application_credentials_are_valid(dbsession,application_name,application_client_id,application_client_secretKey,caller_area=_process_call_area):
                reply={'api_status':'error','api_message':'invalid or expired application credentials'}
                return make_response(jsonify(reply), 403)
            if debug:
                print('OK, authentication_method:',authentication_method)
        elif authentication_method == 'none':
            application_name=request_params_json.get('application_name','')
            application_client_id=request_params_json.get('application_client_id','')
            application_client_secretKey = request_params_json.get('application_client_secretKey', '')
            if debug:
                print('OK, authentication_method:',authentication_method)
        else:
            reply={'api_status':'error','api_message':'invalid authentication method'}
            if debug:
                print('INVALID authentication_method:',authentication_method)
            return make_response(jsonify(reply), 403)
##########################################################################################################################
##########################################################################################################################
##########################################################################################################################
@app.after_request
def after_request_func(response):
    #x=session["foo"] 
    #username=g.username
    #dbsession = g.dbsession
    #print(g.caller_area)
    #debug_level = g.caller_area.get('debug_level')
    #print('after_request', dbsession.session_id, x, username)
    if debug: quick_log('FINISH:' + g.msg_id)
    dbsession.close()
    return response
#   #apply_caching(response):
#     # ix = 0
#     # for entry in response.headers:
#     #     ix = ix + 1
#     #     k = entry[0]
#     #     v = entry[1]
#     #     key=k.lower().replace('-','_')
#     #     msg=f"o resp header param {ix}: {entry[0]} ({key}) = {v}"
#     #     print('   ',msg)

#     #response.headers["X-Frame-Options"] = "SAMEORIGIN"
#     return response

# # Controllers API
# ##########################################################################################################################
# ##########################################################################################################################
# ##########################################################################################################################
# ##########################################################################################################################
# # This doesn't need authentication
# @app.route("/ping")
# @cross_origin(headers=['Content-Type', 'Authorization'])
# def ping():
#     return "All good. You don't need to be authenticated to call this"

# # This does need authentication
# @app.route("/secured/ping")
# @cross_origin(headers=['Content-Type', 'Authorization'])
# @requires_auth
# def secured_ping():
#     return "All good. You only get this message if you're authenticated"
# ##########################################################################################################################


##########################################################################################################################
##########################################################################################################################
##########################################################################################################################
# services: 
##########################################################################################################################
##########################################################################################################################
##########################################################################################################################


#############################################################
#############################################################
#############################################################
### routes(pages) not requiring authentication: confirmation pages with email link, after send emal or sms etc.+bank authorization web hook
#############################################################
#############################################################
#############################################################
@app.route('/test', methods = ['GET','PUT','POST','PATCH'])
def open_test_page():
    msg_page = message_page(message_type='warning', message='adadadasdsad asdadasdasd', secondary_message='', message_description='', title='zzzzzzzzz', application_name='ganimides', application_color='', application_copywrite='', application_logo='', error_code=111)
    return msg_page
#############################################################################
@app.route('/confirmation/<token>/email1', methods = ['GET','PUT','POST','PATCH'])
def email_confirm1(token):
    try:
        email = confirm_token(token,3600)
    except:
        msg=f'The confirmation link is invalid or has expired(token invalid).Retry'
        resp = make_response(jsonify(msg), 200)
        resp.headers['Content-type'] = 'text/html'
        return resp

    if not(email):
        msg = f'The confirmation link is invalid or has expired (not email).Retry'
        # reply = {'api_status': 'error', 'api_message': msg}
        # resp = make_response(jsonify(reply), 200)
        resp = make_response(jsonify(msg), 200)
        resp.headers['Content-type'] = 'text/html'
        return resp

    _process_call_area=g.caller_area
    dbsession = g.dbsession
    
    conf_record = {'email': email,'token':token}
    confirm_result = db.dbapi_email_confirmation(dbsession, conf_record, caller_area=_process_call_area)
    if not confirm_result.get('api_status')=='success':
        msg = f"confirmation failed:{confirm_result.get('api_message','?')}.Retry"
        resp = make_response(jsonify(msg), 200)
        resp.headers['Content-type'] = 'text/html'
        return resp
    
    client_id = confirm_result.get('api_data', {}).get('client_id')
    update_record = {'client_id': client_id, 'email_confirmed': 1, 'email_confirmed_timestamp': datetime.datetime.utcnow(), 'confirmed': 1}

    dbreply=db.dbapi_client(dbsession, 'confirm', update_record, caller_area=_process_call_area)
    if not dbreply.get('api_status')=='success':
        msg = f"confirmation failed:{dbreply.get('api_message','?')}.Retry"
        resp = make_response(jsonify(msg), 200)
        resp.headers['Content-type'] = 'text/html'
        return resp
    email=dbreply.get('api_data',{}).get('email','?')

    msg = f"you have just confirmed your email [{email}]. Thanks!"
    msg = dbreply.get('api_message')
    resp = make_response(jsonify(msg), 200)
    resp.headers['Content-type'] = 'text/html'
    return resp
#############################################################################
@app.route('/confirmation/<token>/email', methods = ['GET','PUT','POST','PATCH'])
def email_confirm(token):
    _process_call_area=g.caller_area
    dbsession = g.dbsession

    page_template = 'email_verification_page.html'
    page_title = 'email verification'
    page_message = 'Please enter the 6-digit verification code we sent via EMAIL'
    page_secondary_message = "(we want to make sure it's you before we commit your subscription)"

    application_name = ""
    msg = ""
    msg2=""
    msg_desc = ""
    error_code = 0
    msg_type = ""
    error = ""
    errors = []
    disable_input = False

    #validate token
    verification_filter = {'verification_token': token,'verification_entity':'email'}
    res = db.dbapi_verification(dbsession, 'get', verification_filter, caller_area=_process_call_area)
    if not res.get('api_status')=='success':
        verification_filter = {'verification_id': token}
        res = db.dbapi_verification(dbsession, 'get', verification_filter, caller_area=_process_call_area)
        if not res.get('api_status')=='success':
            msg = 'invalid access'
            error_code = 599
            msg_type="error"
            msg_page = message_page(message_type=msg_type, message=msg, secondary_message=msg2, message_description=msg_desc, title=page_title, application_name=application_name, error_code=error_code)
            return msg_page
    
    verification_rec = res.get('api_data', {})

    verification_id = verification_rec.get('verification_id')
    client_id = verification_rec.get('client_id')
    application_name = verification_rec.get('application_name', '')
   
    if not client_id:
        msg = 'system error encountered. retry'
        error_code = 501
        msg_type="error"
        msg_page = message_page(message_type=msg_type, message=msg, secondary_message=msg2, message_description=msg_desc, title=page_title, application_name=application_name, error_code=error_code)
        return msg_page

    if verification_rec.get('status') == 'Confirmed':
        msg = 'email already confirmed'
        error_code = 101
        msg_type="warning"
        msg_page = message_page(message_type=msg_type, message=msg, secondary_message=msg2, message_description=msg_desc, title=page_title, application_name=application_name, error_code=error_code)
        return msg_page

    client = dbsession.get(db.CLIENT, {'client_id':client_id}, caller_area=_process_call_area)
    if not client:
        msg = 'system error encountered. retry'
        error_code = 511
        msg_type="error"
        msg_page = message_page(message_type=msg_type, message=msg, secondary_message=msg2, message_description=msg_desc, title=page_title, application_name=application_name, error_code=error_code)
        return msg_page
    if not client.email:
        msg = 'system error encountered. retry'
        error_code = 512
        msg_type="error"
        msg_page = message_page(message_type=msg_type, message=msg, secondary_message=msg2, message_description=msg_desc, title=page_title, application_name=application_name, error_code=error_code)
        return msg_page
    if client.email_confirmed:
        msg = 'email already confirmed'
        error_code = 101
        msg_type="warning"
        msg_page = message_page(message_type=msg_type, message=msg, secondary_message=msg2, message_description=msg_desc, title=page_title, application_name=application_name, error_code=error_code)
        return msg_page

    if request.method == 'GET':
        if not verification_rec.get('expiry_timestamp') or verification_rec.get('expiry_timestamp') < datetime.datetime.utcnow():
            error = 'this verification code is expired. request a new verification code'
            disable_input = True
            this_page = application_page(page_template, error=error, error_code=error_code, errors=errors, disable_input=disable_input, title=page_title, application_name=application_name, message=page_message, secondary_message=page_secondary_message)
            return this_page
        this_page = application_page(page_template, error=error, error_code=error_code, errors=errors, disable_input=disable_input, title=page_title, application_name=application_name, message=page_message, secondary_message=page_secondary_message)
        return this_page        
    elif request.method == 'POST':
        try:
            x = request.form['btn_new_code']
            new_code_requested = True
        except:
            new_code_requested = False
    
        if new_code_requested:
            if verification_rec.get('status') == 'Confirmed':
                msg = 'email already confirmed'
                error_code = 102
                msg_type="warning"
                msg_page = message_page(message_type=msg_type, message=msg, secondary_message=msg2, message_description=msg_desc, title=page_title, application_name=application_name, error_code=error_code)
                return msg_page

            confirmation_url = url_for('email_confirm', token='-token-', _external=True)
            try:
                email_reply = api.emailapi_send_email_confirmation_email(dbsession, client_id, application_name, confirmation_url, caller_area=_process_call_area)
            except Exception as error_text:
                msg = 'system error. fail to send email'
                error_code = 502
                msg_type="error"
                msg_page = message_page(message_type=msg_type, message=msg, secondary_message=msg2, message_description=msg_desc, title=page_title, application_name=application_name, error_code=error_code)
                return msg_page

            if email_reply.get('api_status')=='success':
                msg = "email sent with a new verification code"
                msg_desc = f'open this email, click on the link to go the verificaion page and enter the verification code'
                msg_type="success"
            else:
                error_text = email_reply.get('api_message')
                msg = f'system error. fail to send email'
                msg_desc = f'{error_text}'
                msg_type = 'error'
                error_code=503
            msg_page = message_page(message_type=msg_type, message=msg, secondary_message=msg2, message_description=msg_desc, title=page_title, application_name=application_name, error_code=error_code)
            return msg_page

        #get the input from the form as digits
        try:
            input_code = request.form.get("digit1", "") + request.form.get("digit2", "") + request.form.get("digit3", "") + request.form.get("digit4", "") + request.form.get("digit5", "") + request.form.get("digit6", "")
        except:
            input_code = ""
            
        if not input_code:
            error = 'please enter your verification code'
            error_code=80
            this_page = application_page(page_template, error=error, error_code=error_code, errors=errors, disable_input=disable_input, title=page_title, application_name=application_name, message=page_message, secondary_message=page_secondary_message)
            return this_page        

        if not input_code == verification_rec.get('verification_code'):
            error = 'invalid verification code. retry'
            error_code=81
            this_page = application_page(page_template, error=error, error_code=error_code, errors=errors, disable_input=disable_input, title=page_title, application_name=application_name, message=page_message, secondary_message=page_secondary_message)
            return this_page        

        #ok, verify button pressed
        conf_record = {'verification_code': input_code, 'verification_token': token, 'verification_id': verification_id}
        confirm_result = db.dbapi_email_confirmation(dbsession, conf_record, caller_area=_process_call_area)
        if not confirm_result.get('api_status')=='success':
            error = f"your verification failed. Retry"
            error_code=82
            this_page = application_page(page_template, error=error, error_code=error_code, errors=errors, disable_input=disable_input, title=page_title, application_name=application_name, message=page_message, secondary_message=page_secondary_message)
            return this_page        

        msg = f"you have just confirmed your email. Thanks!"
        msg_desc = f"you can now proceed with your registration"
        msg_type = 'success'
        msg_page = message_page(message_type=msg_type, message=msg, secondary_message=msg2, message_description=msg_desc, title=page_title, application_name=application_name, error_code=error_code)
        return msg_page

    this_page = application_page(page_template, error=error, error_code=error_code, errors=errors, disable_input=disable_input, title=page_title, application_name=application_name, message=page_message, secondary_message=page_secondary_message)
    return this_page        
#############################################################################
@app.route('/confirmation/<token>/mobile', methods = ['GET','PUT','POST','PATCH'])
def mobile_confirm(token):
    _process_call_area=g.caller_area
    dbsession = g.dbsession

    page_template = 'mobile_verification_page.html'
    page_title = 'mobile verification'
    page_message = 'Please enter the 6-digit verification code we sent via SMS'
    page_secondary_message = "(we want to make sure it's you before we commit your subscription)"

    application_name = ""
    msg = ""
    msg2=""
    msg_desc = ""
    error_code = 0
    msg_type = ""
    error = ""
    errors = []
    disable_input = False

    # this_page = application_page(page_template, error=error, error_code=error_code, errors=errors, disable_input=disable_input, title=page_title, application_name=application_name, message=page_message, secondary_message=page_secondary_message)
    # return this_page        

    #validate token
    verification_filter = {'verification_token': token,'verification_entity':'mobile'}
    res = db.dbapi_verification(dbsession, 'get', verification_filter, caller_area=_process_call_area)
    if not res.get('api_status')=='success':
        verification_filter = {'verification_id': token}
        res = db.dbapi_verification(dbsession, 'get', verification_filter, caller_area=_process_call_area)
        if not res.get('api_status')=='success':
            msg = 'invalid access'
            error_code = 599
            msg_type="error"
            msg_page = message_page(message_type=msg_type, message=msg, secondary_message=msg2, message_description=msg_desc, title=page_title, application_name=application_name, error_code=error_code)
            return msg_page
    
    verification_rec = res.get('api_data', {})

    verification_id = verification_rec.get('verification_id')
    client_id = verification_rec.get('client_id')
    application_name = verification_rec.get('application_name', '')
   
    if not client_id:
        msg = 'system error encountered. retry'
        error_code = 501
        msg_type="error"
        msg_page = message_page(message_type=msg_type, message=msg, secondary_message=msg2, message_description=msg_desc, title=page_title, application_name=application_name, error_code=error_code)
        return msg_page

    if verification_rec.get('status') == 'Confirmed':
        msg = 'mobile already confirmed'
        error_code = 101
        msg_type="warning"
        msg_page = message_page(message_type=msg_type, message=msg, secondary_message=msg2, message_description=msg_desc, title=page_title, application_name=application_name, error_code=error_code)
        return msg_page

    client = dbsession.get(db.CLIENT, {'client_id':client_id}, caller_area=_process_call_area)
    if not client:
        msg = 'system error encountered. retry'
        error_code = 511
        msg_type="error"
        msg_page = message_page(message_type=msg_type, message=msg, secondary_message=msg2, message_description=msg_desc, title=page_title, application_name=application_name, error_code=error_code)
        return msg_page
    if not client.mobile:
        msg = 'system error encountered. retry'
        error_code = 512
        msg_type="error"
        msg_page = message_page(message_type=msg_type, message=msg, secondary_message=msg2, message_description=msg_desc, title=page_title, application_name=application_name, error_code=error_code)
        return msg_page
    if client.mobile_confirmed:
        msg = 'mobile already confirmed'
        error_code = 101
        msg_type="warning"
        msg_page = message_page(message_type=msg_type, message=msg, secondary_message=msg2, message_description=msg_desc, title=page_title, application_name=application_name, error_code=error_code)
        return msg_page

    if request.method == 'GET':
        if not verification_rec.get('expiry_timestamp') or verification_rec.get('expiry_timestamp') < datetime.datetime.utcnow():
            error = 'this verification code is expired. request a new verification code'
            disable_input = True
            this_page = application_page(page_template, error=error, error_code=error_code, errors=errors, disable_input=disable_input, title=page_title, application_name=application_name, message=page_message, secondary_message=page_secondary_message)
            return this_page
        this_page = application_page(page_template, error=error, error_code=error_code, errors=errors, disable_input=disable_input, title=page_title, application_name=application_name, message=page_message, secondary_message=page_secondary_message)
        return this_page        
    elif request.method == 'POST':
        try:
            x = request.form['btn_new_code']
            new_code_requested = True
        except:
            new_code_requested = False
    
        if new_code_requested:
            if verification_rec.get('status') == 'Confirmed':
                msg = 'mobile already confirmed'
                error_code = 103
                msg_type="warning"
                msg_page = message_page(message_type=msg_type, message=msg, secondary_message=msg2, message_description=msg_desc, title=page_title, application_name=application_name, error_code=error_code)
                return msg_page

            confirmation_url = url_for('mobile_confirm', token='-token-', _external=True)
            try:
                sms_reply = api.smsapi_send_mobile_confirmation_sms(dbsession, client_id, application_name, confirmation_url, caller_area=_process_call_area)
            except Exception as error_text:
                msg = 'system error. fail to send sms'
                error_code = 504
                msg_type="error"
                msg_page = message_page(message_type=msg_type, message=msg, secondary_message=msg2, message_description=msg_desc, title=page_title, application_name=application_name, error_code=error_code)
                return msg_page

            if sms_reply.get('api_status')=='success':
                msg = "sms sent with a new verification code"
                msg_desc = f'open this sms, click on the link to go the verificaion page and enter the verification code'
                msg_type="success"
            else:
                error_text = sms_reply.get('api_message')
                msg = f'system error. fail to send sms'
                msg_desc = f'{error_text}'
                msg_type = 'error'
                error_code=505
            msg_page = message_page(message_type=msg_type, message=msg, secondary_message=msg2, message_description=msg_desc, title=page_title, application_name=application_name, error_code=error_code)
            return msg_page

        #get the input from the form as digits
        try:
            input_code = request.form.get("digit1", "") + request.form.get("digit2", "") + request.form.get("digit3", "") + request.form.get("digit4", "") + request.form.get("digit5", "") + request.form.get("digit6", "")
        except:
            input_code = ""
            
        if not input_code:
            error = 'please enter your verification code'
            error_code=80
            this_page = application_page(page_template, error=error, error_code=error_code, errors=errors, disable_input=disable_input, title=page_title, application_name=application_name, message=page_message, secondary_message=page_secondary_message)
            return this_page        

        if not input_code == verification_rec.get('verification_code'):
            error = 'invalid verification code. retry'
            error_code=81
            this_page = application_page(page_template, error=error, error_code=error_code, errors=errors, disable_input=disable_input, title=page_title, application_name=application_name, message=page_message, secondary_message=page_secondary_message)
            return this_page        

        #ok, verify button pressed
        conf_record = {'verification_code': input_code, 'verification_token': token, 'verification_id': verification_id}
        confirm_result = db.dbapi_mobile_confirmation(dbsession, conf_record, caller_area=_process_call_area)
        if not confirm_result.get('api_status')=='success':
            error = f"your verification failed. Retry"
            error_code=82
            this_page = application_page(page_template, error=error, error_code=error_code, errors=errors, disable_input=disable_input, title=page_title, application_name=application_name, message=page_message, secondary_message=page_secondary_message)
            return this_page        

        msg = f"you have just confirmed your mobile. Thanks!"
        msg_desc = f"you can now proceed with your registration"
        msg_type = 'success'
        msg_page = message_page(message_type=msg_type, message=msg, secondary_message=msg2, message_description=msg_desc, title=page_title, application_name=application_name, error_code=error_code)
        return msg_page

    this_page = application_page(page_template, error=error, error_code=error_code, errors=errors, disable_input=disable_input, title=page_title, application_name=application_name, message=page_message, secondary_message=page_secondary_message)
    return this_page        
#############################################################################
@app.route('/authorization', methods = ['GET','PUT','POST','PATCH'])
def get_authorization_code_from_boc_client():
    _process_call_area=g.caller_area
    dbsession = g.dbsession

    bank_code = 'bankofcyprus'
    application_name = request.headers.get('Registered-Application')
    request_params_json=get_params(request)
    authorization_code = request_params_json.get('code')
    if not authorization_code:
        msg = f'authorization code not received by bank [{bank_code}]'
        print(msg)
        reply = {'api_status': 'error', 'api_message': msg}
        return make_response(jsonify(reply), 400)

    result = api.banksubscription_receive_authorization_from_client(dbsession,bank_code, authorization_code, caller_area=_process_call_area)
    if not result.get('api_status')=='success':
        msg = result.get('api_message', '?')
        msg = f"your authorization for an app to use your {bank_code} account(s) FAILED. retry"
        msg_desc=""
        # resp = make_response(jsonify(msg), 200)
        # resp.headers['Content-type'] = 'text/html'
        # return resp
        msg_page = message_page(message_type='error', message=msg, secondary_message='', message_description=msg_desc, title='bank authorization', application_name=application_name,error_code=91)
        return msg_page
    else:
        application_name=result.get('application_name','?')
        msg = f"you have just authorized app {application_name} to use your {bank_code} account(s)."
        msg_desc=f"app {application_name} will never use your account(s) without your permission."
        # resp = make_response(jsonify(msg), 200)
        # resp.headers['Content-type'] = 'text/html'
        app=db.dbapi_application(dbsession, 'get', {'application_name':application_name}, caller_area=_process_call_area)
        if app:
            app_redirect = app.get('application_redirect_uri')
            if app_redirect:
                if app_redirect.find("http://") != 0 and app_redirect.find("https://") != 0:
                    app_redirect = "http://" + app_redirect.strip()
                    return redirect(app_redirect)
        msg_page = message_page(message_type='success', message=msg, secondary_message='', message_description=msg_desc, title='bank authorization', application_name=application_name)
        return msg_page
#############################################################################
#############################################################################
#############################################################################
# test route
#############################################################################
#############################################################################
#############################################################################
@app.route('/openbanking/api/v1/underconstruction', methods = ['GET','POST','PUNCH','PUT','DELETE'])
def underconstruction():
    _process_call_area=g.caller_area
    dbsession = g.dbsession
    if not request.json:
        reply={'api_status':'success','api_message':'under constrcution by leandrou technology forward ltd'}
        return make_response(jsonify(reply), 200)

#############################################################
#############################################################
#############################################################
### routes requiring application authentication: done in before_request
#############################################################
#############################################################
#############################################################



#############################################################################
#############################################################################
#############################################################################
#############################################################################
# authorization routes
#############################################################################
#############################################################################
#############################################################################
@app.route('/openbanking/api/v1/authorization/tokens/access', methods = ['GET'])
def get_access_token():
    _process_call_area=g.caller_area
    dbsession = g.dbsession
    if not request.json:
        reply={'api_status':'error','api_message':'json data Not provided'}
        return make_response(jsonify(reply), 400)
    request_data = request.json
    for k in request_params_json:
        v=request_params_json.get(k)
        request_data.update({k: v})
    res = db.dbapi_token_get_access_token(dbsession, request_data, caller_area=_process_call_area)
    return jsonify( res )
#############################################################################

#############################################################################
#############################################################################
#############################################################################
#############################################################################
# get routes: apis, banks, ...
#############################################################################
#############################################################################
#############################################################################

#############################################################################
@app.route('/openbanking/api/v1/apis/<api_id>', methods = ['GET'])
def get_api(api_id):
    dbreply=db.dbapi_api(dbsession, 'get', {'api_id':api_id}, caller_area=_process_call_area)
    return jsonify( dbreply )
#############################################################################
@app.route('/openbanking/api/v1/banks/<bank_id>', methods = ['GET'])
def get_bank(bank_id):
    dbreply=db.dbapi_bank(dbsession, 'get', {'bank_id':bank_id}, caller_area=_process_call_area)
    return jsonify( dbreply )
#############################################################################

#############################################################################
#############################################################################
#############################################################################
### list routes : requiring application authentication
#############################################################################
#############################################################################
#############################################################################
@app.route('/openbanking/api/v1/apis', methods = ['GET'])
def get_apis_list():
    dbreply = db.dbapi_api(dbsession, 'LIST', {}, caller_area=_process_call_area)
    return jsonify( dbreply )
##############################################################################
@app.route('/openbanking/api/v1/banks', methods = ['GET'])
def get_banks_list():
    dbreply = db.dbapi_bank(dbsession, 'LIST', {}, caller_area=_process_call_area)
    return jsonify( dbreply )
##############################################################################
@app.route('/openbanking/api/v1/clients', methods = ['GET'])
def get_clients_list():
    _process_call_area=g.caller_area
    dbsession = g.dbsession
    # filterString=f"all"
    dbreply = db.dbapi_client(dbsession, 'LIST', {}, caller_area=_process_call_area)
    return jsonify( dbreply )
##############################################################################
@app.route('/openbanking/api/v1/merchants', methods = ['GET'])
def get_merchants_list():
    _process_call_area=g.caller_area
    dbsession = g.dbsession
    # filterString=f"all"
    dbreply = db.dbapi_merchant(dbsession, 'LIST', {}, caller_area=_process_call_area)
    return jsonify( dbreply )
#############################################################################
@app.route('/openbanking/api/v1/pointofsales', methods = ['GET'])
def get_pointofsales_list():
    _process_call_area=g.caller_area
    dbsession = g.dbsession
    # filterString=f"all"
    dbreply = db.dbapi_pointofsale(dbsession, 'LIST', {}, caller_area=_process_call_area)
    return jsonify( dbreply )

#############################################################################
#############################################################################
#############################################################################
# subscription routes: requiring user login
#############################################################################
#############################################################################
#############################################################################


#############################################################################
@app.route('/openbanking/api/v1/subscriptions', methods = ['PUT','POST'])
#@auth.login_required
def new_subscription():
    _process_call_area=g.caller_area
    dbsession = g.dbsession
    if not request.json:
        reply={'api_status':'error','api_message':'json data Not provided'}
        return make_response(jsonify(reply), 400)
    record_data = request.json
    if not record_data.get('name'):
        reply={'api_status':'error','api_message':'[name] Not provided'}
        return make_response(jsonify(reply), 401)
    if not record_data.get('email'):
        reply={'api_status':'error','api_message':'[email] Not provided'}
        return make_response(jsonify(reply), 401)
    dbreply=db.dbapi_subscription(dbsession, 'register', record_data, caller_area=_process_call_area)
    return jsonify( dbreply )
#############################################################################
@app.route('/openbanking/api/v1/subscriptions/<subscription_id>', methods = ['GET'])
#@auth.login_required
def get_subscription(subscription_id):
    _process_call_area=g.caller_area
    dbsession = g.dbsession
    dbreply=db.dbapi_subscription(dbsession, 'get', {'subscription_id':subscription_id}, caller_area=_process_call_area)
    return jsonify( dbreply )
#############################################################################
@app.route('/openbanking/api/v1/subscriptions/<subscription_id>', methods = ['PUT','POST','PATCH'])
#@auth.login_required
def update_subscription(subscription_id):
    _process_call_area=g.caller_area
    if not request.json:
        reply={'api_status':'error','api_message':'json data Not provided'}
        return make_response(jsonify(reply), 400)
    update_record = request.json
    update_record.update({'subscription_id':subscription_id})
    dbreply=db.dbapi_subscription(dbsession, 'update', update_record, caller_area=_process_call_area)
    return jsonify( dbreply )
#############################################################################
@app.route('/openbanking/api/v1/subscriptions/<subscription_id>/unregister', methods = ['PUT','POST','PATCH'])
#@auth.login_required
def unregister_subscription(subscription_id):
    _process_call_area=g.caller_area
    dbsession = g.dbsession
    if not request.json:
        reply={'api_status':'error','api_message':'json data Not provided'}
        return make_response(jsonify(reply), 400)
    update_record = request.json
    update_record.update({'subscription_id':subscription_id})
    dbreply=db.dbapi_subscription(dbsession, 'unregister', update_record, caller_area=_process_call_area)
    return jsonify(dbreply)
#############################################################################
@app.route('/openbanking/api/v1/subscriptions/<subscription_id>', methods = ['DELETE'])
#@auth.login_required
def delete_subscription(subscription_id):
    _process_call_area=g.caller_area
    dbsession = g.dbsession
    dbreply=db.dbapi_subscription(dbsession, 'delete', {'subscription_id':subscription_id}, caller_area=_process_call_area)
    return jsonify( dbreply )
#############################################################################

#############################################################################
#############################################################################
#############################################################################
# admin routes: requiring user login and admin rights
#############################################################################
#############################################################################
#############################################################################
#############################################################################

#APIS

@app.route('/openbanking/api/v1/apis', methods = ['PUT','POST'])
#@auth.login_required
#@auth.admin_required
def new_api():
    if not request.json:
        reply={'api_status':'error','api_message':'json data Not provided'}
        return make_response(jsonify(reply), 400)
    record_data = request.json
    if not record_data.get('api_name'):
        reply={'api_status':'error','api_message':'[name] Not provided'}
        return make_response(jsonify(reply), 401)
    dbreply=db.dbapi_api(dbsession, 'register', record_data, caller_area=_process_call_area)
    return jsonify( dbreply )
#############################################################################
@app.route('/openbanking/api/v1/apis/<api_id>', methods = ['PUT','POST','PATCH'])
#@auth.login_required
#@auth.admin_required
def update_api(api_id):
    if not request.json:
        reply={'api_status':'error','api_message':'json data Not provided'}
        return make_response(jsonify(reply), 400)
    update_record = request.json
    update_record.update({'api_id':api_id})
    dbreply=db.dbapi_api(dbsession, 'update', update_record, caller_area=_process_call_area)
    return jsonify( dbreply )
#############################################################################
@app.route('/openbanking/api/v1/apis/<api_id>/activate', methods = ['PUT','POST','PATCH'])
#@auth.login_required
#@auth.admin_required
def confirm_api(api_id):
    update_record = request.json
    update_record.update({'api_id':api_id})
    dbreply=db.dbapi_api(dbsession, 'activate', update_record, caller_area=_process_call_area)
    return jsonify( dbreply )
#############################################################################
@app.route('/openbanking/api/v1/apis/<api_id>/deactivate', methods = ['PUT','POST','PATCH'])
#@auth.login_required
#@auth.admin_required
def unregister_api(api_id):
    update_record = request.json
    update_record.update({'api_id':api_id})
    dbreply=db.dbapi_api(dbsession, 'deactivate', update_record, caller_area=_process_call_area)
    return jsonify(dbreply)
#############################################################################
@app.route('/openbanking/api/v1/apis/<api_id>', methods = ['DELETE'])
#@auth.login_required
#@auth.admin_required
def delete_api(api_id):
    dbreply=db.dbapi_api(dbsession, 'delete', {'api_id':api_id}, caller_area=_process_call_area)
    return jsonify( dbreply )
##########################################################################################################################################################

#BANKS

@app.route('/openbanking/api/v1/banks', methods = ['PUT','POST'])
#@auth.login_required
#@auth.admin_required
def new_bank():
    if not request.json:
        reply={'api_status':'error','api_message':'json data Not provided'}
        return make_response(jsonify(reply), 400)
    record_data = request.json
    record_data = request.json
    if not record_data.get('bank_name'):
        reply={'api_status':'error','api_message':'[name] Not provided'}
        return make_response(jsonify(reply), 401)
    if not record_data.get('bank_code'):
        reply={'api_status':'error','api_message':'[bank_code] Not provided'}
        return make_response(jsonify(reply), 401)
    if not record_data.get('bank_BIC'):
        reply={'api_status':'error','api_message':'[bank_BIC] Not provided'}
        return make_response(jsonify(reply), 401)
    dbreply=db.dbapi_bank(dbsession, 'register', record_data, caller_area=_process_call_area)
    return jsonify( dbreply )
#############################################################################
@app.route('/openbanking/api/v1/banks/<bank_id>', methods = ['PUT','POST','PATCH'])
#@auth.login_required
#@auth.admin_required
def update_bank(bank_id):
    if not request.json:
        reply={'api_status':'error','api_message':'json data Not provided'}
        return make_response(jsonify(reply), 400)
    update_record = request.json
    update_record.update({'bank_id':bank_id})
    dbreply=db.dbapi_bank(dbsession, 'update', update_record, caller_area=_process_call_area)
    return jsonify( dbreply )
#############################################################################
@app.route('/openbanking/api/v1/banks/<bank_id>/activate', methods = ['PUT','POST','PATCH'])
#@auth.login_required
#@auth.admin_required
def confirm_bank(bank_id):
    update_record = request.json
    update_record.update({'bank_id':bank_id})
    dbreply=db.dbapi_bank(dbsession, 'activate', update_record, caller_area=_process_call_area)
    return jsonify( dbreply )
#############################################################################
@app.route('/openbanking/api/v1/banks/<bank_id>/deactivate', methods = ['PUT','POST','PATCH'])
#@auth.login_required
#@auth.admin_required
def unregister_bank(bank_id):
    update_record = request.json
    update_record.update({'bank_id':bank_id})
    dbreply=db.dbapi_bank(dbsession, 'deactivate', update_record, caller_area=_process_call_area)
    return jsonify(dbreply)
#############################################################################
@app.route('/openbanking/api/v1/banks/<bank_id>', methods = ['DELETE'])
#@auth.login_required
#@auth.admin_required
def delete_bank(bank_id):
    dbreply=db.dbapi_bank(dbsession, 'delete', {'bank_id':bank_id}, caller_area=_process_call_area)
    return jsonify( dbreply )
##########################################################################################################################################################

#############################################################################
#############################################################################
#############################################################################
# application routes: requiring user login and subscription
#############################################################################
#############################################################################
#############################################################################

@app.route('/openbanking/api/v1/applications', methods = ['PUT','POST'])
#@auth.login_required
def new_application():
    _process_call_area=g.caller_area
    dbsession = g.dbsession
    if not request.json:
        reply={'api_status':'error','api_message':'json data Not provided'}
        return make_response(jsonify(reply), 400)
    record_data = request.json
    if not record_data.get('name'):
        reply={'api_status':'error','api_message':'[name] Not provided'}
        return make_response(jsonify(reply), 401)
    if not record_data.get('email'):
        reply={'api_status':'error','api_message':'[email] Not provided'}
        return make_response(jsonify(reply), 401)
    dbreply=db.dbapi_application(dbsession, 'register', record_data, caller_area=_process_call_area)
    return jsonify( dbreply )
#############################################################################
@app.route('/openbanking/api/v1/applications/<application_id>', methods = ['GET'])
#@auth.login_required
def get_application(application_id):
    _process_call_area=g.caller_area
    dbsession = g.dbsession
    dbreply=db.dbapi_application(dbsession, 'get', {'application_id':application_id}, caller_area=_process_call_area)
    return jsonify( dbreply )
#############################################################################
@app.route('/openbanking/api/v1/applications/<application_id>', methods = ['PUT','POST','PATCH'])
#@auth.login_required
def update_application(application_id):
    _process_call_area=g.caller_area
    if not request.json:
        reply={'api_status':'error','api_message':'json data Not provided'}
        return make_response(jsonify(reply), 400)
    update_record = request.json
    update_record.update({'application_id':application_id})
    dbreply=db.dbapi_application(dbsession, 'update', update_record, caller_area=_process_call_area)
    return jsonify( dbreply )
#############################################################################
@app.route('/openbanking/api/v1/applications/<application_id>/unregister', methods = ['PUT','POST','PATCH'])
#@auth.login_required
def unregister_application(application_id):
    _process_call_area=g.caller_area
    dbsession = g.dbsession
    if not request.json:
        reply={'api_status':'error','api_message':'json data Not provided'}
        return make_response(jsonify(reply), 400)
    update_record = request.json
    update_record.update({'application_id':application_id})
    dbreply=db.dbapi_application(dbsession, 'unregister', update_record, caller_area=_process_call_area)
    return jsonify(dbreply)
#############################################################################
@app.route('/openbanking/api/v1/applications/<application_id>', methods = ['DELETE'])
#@auth.login_required
def delete_application(application_id):
    _process_call_area=g.caller_area
    dbsession = g.dbsession
    dbreply=db.dbapi_application(dbsession, 'delete', {'application_id':application_id}, caller_area=_process_call_area)
    return jsonify( dbreply )
#############################################################################
@app.route('/openbanking/api/v1/applications/<application_id>/apis/<api_name>/register', methods = ['PUT','POST','PATCH'])
#@auth.login_required
def application_api_register(application_id,api_name):
    _process_call_area=g.caller_area
    dbsession = g.dbsession
    update_record = request.json
    update_record.update({'application_id':application_id})
    update_record.update({'api_name':api_name})
    dbreply=db.dbapi_application(dbsession, 'api_register', update_record, caller_area=_process_call_area)
    return jsonify(dbreply)
#############################################################################
@app.route('/openbanking/api/v1/applications/<application_id>/apis/<api_name>/unregister', methods = ['PUT','POST','PATCH'])
#@auth.login_required
def application_api_unregister(application_id,api_name):
    _process_call_area=g.caller_area
    dbsession = g.dbsession
    update_record = request.json
    update_record.update({'application_id':application_id})
    update_record.update({'api_name':api_name})
    dbreply=db.dbapi_application(dbsession, 'api_unregister', update_record, caller_area=_process_call_area)
    return jsonify(dbreply)
#############################################################################




##########################################################################################################################
# @app.route('/openbanking/api/v1/subscriptions/device', methods = ['PUT','POST'])
# @auth.login_required
# def new_device():
#     if not request.json:
#         reply={'api_status':'error','api_message':'json data Not provided'}
#         return make_response(jsonify(reply), 400)
#     record_data = request.json
#     #basic validations before calling the database api
#     # if not record_data.get('email'):
#     #     reply={'api_status':'error','api_message':'[email] Not provided'}
#     #     return make_response(jsonify(reply), 401)
#     # if not record_data.get('name'):
#     #     reply={'api_status':'error','api_message':'[name] Not provided'}
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
#         reply={'api_status':'error','api_message':'json data Not provided'}
#         return make_response(jsonify(reply), 400)
#     request_data = request.json
#     res = db.dbapi_add_interaction_message(pointofsale_id, request_data)
#     return jsonify( res )
# ##########################################################################################################################
# @app.route('/openbanking/api/v1/interactions/pointofsales/<pointofsale_id>/originator/<secretKey>/putmessage', methods = ['PUT','POST'])
# def put_interaction_message(pointofsale_id,secretKey):
#     if not request.json:
#         reply={'api_status':'error','api_message':'json data Not provided'}
#         return make_response(jsonify(reply), 400)
#     request_data = request.json
#     res = db.dbapi_put_interaction_message(pointofsale_id, secretKey,request_data)
#     return jsonify( res )
# #############################################################################

#############################################################################
#############################################################################
#############################################################################
# clients routes: requiring application authentication
#############################################################################
#############################################################################
#############################################################################
@app.route('/openbanking/api/v1/clients', methods = ['PUT','POST'])
def new_client():
    _process_call_area=g.caller_area
    dbsession = g.dbsession
    if not request.json:
        reply={'api_status':'error','api_message':'json data Not provided'}
        return make_response(jsonify(reply), 400)
    record_data = request.json
    if not record_data.get('name'):
        reply={'api_status':'error','api_message':'[name] Not provided'}
        return make_response(jsonify(reply), 401)
    if not record_data.get('email'):
        reply={'api_status':'error','api_message':'[email] Not provided'}
        return make_response(jsonify(reply), 401)
    dbreply=db.dbapi_client(dbsession, 'register', record_data, caller_area=_process_call_area)
    return jsonify( dbreply )
#############################################################################
@app.route('/openbanking/api/v1/clients/<client_id>', methods = ['GET'])
def get_client(client_id):
    _process_call_area=g.caller_area
    dbsession = g.dbsession
    dbreply=db.dbapi_client(dbsession, 'get', {'client_id':client_id}, caller_area=_process_call_area)
    return jsonify( dbreply )
#############################################################################
@app.route('/openbanking/api/v1/clients/<client_id>', methods = ['PUT','POST','PATCH'])
def update_client(client_id):
    _process_call_area=g.caller_area
    dbsession = g.dbsession
    if not request.json:
        reply={'api_status':'error','api_message':'json data Not provided'}
        return make_response(jsonify(reply), 400)
    update_record = request.json
    update_record.update({'client_id':client_id})
    dbreply=db.dbapi_client(dbsession, 'update', update_record, caller_area=_process_call_area)
    return jsonify( dbreply )
#############################################################################
#not used
@app.route('/openbanking/api/v1/clients/<client_id>/confirm', methods = ['PUT','POST','PATCH'])
def confirm_client(client_id):
    _process_call_area=g.caller_area
    dbsession = g.dbsession
    update_record = request.json
    update_record.update({'client_id':client_id})
    dbreply=db.dbapi_client(dbsession, 'confirm', update_record, caller_area=_process_call_area)
    return jsonify( dbreply )
##############################################################################
@app.route('/openbanking/api/v1/clients/<client_id>/confirmation_email', methods = ['GET','PUT','POST','PATCH'])
def send_client_confirmation_email(client_id):
    _process_call_area=g.caller_area
    dbsession = g.dbsession
    application_name = thisApp.application_name
    confirmation_url = url_for('email_confirm', token='#TOKEN#', _external=True)
    try:
        reply = api.emailapi_send_email_confirmation_email(dbsession, client_id, application_name, confirmation_url, caller_area=_process_call_area)
        if not reply.get('api_status') == 'success':
            print (reply)
    except Exception as error_text:
        msg = f'send email system error: {error_text}'
        log_process_message('', 'error', msg,**_process_call_area)
        reply = {'api_status': 'error', 'api_message': msg}
    return jsonify( reply )
#############################################################################
@app.route('/openbanking/api/v1/clients/<client_id>/applications/<application_name>/confirmation_email', methods = ['GET','PUT','POST','PATCH'])
def send_application_client_confirmation_email(client_id,application_name):
    _process_call_area = g.caller_area
    dbsession = g.dbsession
    confirmation_url = url_for('email_confirm', token='-token-', _external=True)
    try:
        reply = api.emailapi_send_email_confirmation_email(dbsession, client_id, application_name, confirmation_url, caller_area=_process_call_area)
        if not reply.get('api_status') == 'success':
            print (reply)
    except Exception as error_text:
        msg = f'send email system error: {error_text}'
        log_process_message('', 'error', msg,**_process_call_area)
        reply = {'api_status': 'error', 'api_message': msg}
    return jsonify( reply )
#############################################################################
@app.route('/openbanking/api/v1/clients/<client_id>/confirmation_sms', methods = ['GET','PUT','POST','PATCH'])
def send_client_confirmation_sms(client_id):
    _process_call_area=g.caller_area
    dbsession = g.dbsession
    application_name=thisApp.application_name
    confirmation_url = url_for('mobile_confirm', token='-token-', _external=True)
    try:
        reply = api.smsapi_send_mobile_confirmation_sms(dbsession, client_id, application_name, confirmation_url,caller_area=_process_call_area)
    except Exception as error_text:
        msg = f'send sms system error: {error_text}'
        log_process_message('', 'error', msg,**_process_call_area)
        reply = {'api_status': 'error', 'api_message': msg}
    return jsonify( reply )
#############################################################################
@app.route('/openbanking/api/v1/clients/<client_id>/applications/<application_name>/confirmation_sms', methods = ['GET','PUT','POST','PATCH'])
def send_application_client_confirmation_sms(client_id,application_name):
    _process_call_area=g.caller_area
    dbsession = g.dbsession
    confirmation_url = url_for('mobile_confirm', token='-token-', _external=True)
    try:
        reply = api.smsapi_send_mobile_confirmation_sms(dbsession, client_id, application_name, confirmation_url,caller_area=_process_call_area)
    except Exception as error_text:
        msg = f'send sms system error: {error_text}'
        log_process_message('', 'error', msg,**_process_call_area)
        reply = {'api_status': 'error', 'api_message': msg}
    return jsonify( reply )
#############################################################################
@app.route('/openbanking/api/v1/clients/<client_id>/unregister', methods = ['PUT','POST','PATCH'])
def unregister_client(client_id):
    _process_call_area=g.caller_area
    dbsession = g.dbsession
    update_record = request.json
    update_record.update({'client_id':client_id})
    dbreply=db.dbapi_client(dbsession, 'UnRegister', update_record, caller_area=_process_call_area)
    return jsonify(dbreply)
#############################################################################
@app.route('/openbanking/api/v1/clients/<client_id>', methods = ['DELETE'])
def delete_client(client_id):
    _process_call_area=g.caller_area
    dbsession = g.dbsession
    dbreply=db.dbapi_client(dbsession, 'delete', {'client_id':client_id}, caller_area=_process_call_area)
    return jsonify( dbreply )
#############################################################################
@app.route('/openbanking/api/v1/clients/<client_email>/subscriptions', methods = ['GET'])
def client_subscriptions(client_email):
    _process_call_area=g.caller_area
    dbsession = g.dbsession
    dbreply=db.dbapi_application_USER(dbsession, 'list', {},{'email':client_email}, caller_area=_process_call_area)
    return jsonify( dbreply )
#############################################################################
@app.route('/openbanking/api/v1/clients/<client_id>/applications/<application_name>/register', methods = ['PUT','POST','PATCH'])
def client_application_register(client_id, application_name):
    _process_call_area=g.caller_area
    dbsession = g.dbsession
    action_filter = {'client_id': client_id, 'application_name': application_name, 'user_role': 'user'}
    input_dict = {'status': 'Active'}
 
    reply = api.dbapi_application_USER(dbsession, 'refresh', input_dict, action_filter, caller_area=_process_call_area)

    return jsonify(reply)
#############################################################################
@app.route('/openbanking/api/v1/clients/<client_id>/applications/<application_name>/unregister', methods = ['PUT','POST','PATCH'])
def client_application_unregister(client_id, application_name):
    _process_call_area=g.caller_area
    dbsession = g.dbsession
    action_filter = {'client_id': client_id, 'application_name': application_name, 'user_role': 'user'}
    input_dict = {'status': 'InActive'}

    reply = api.dbapi_application_USER(dbsession, 'deactivate', input_dict, action_filter, caller_area=_process_call_area)

    return jsonify(reply)
#############################################################################
@app.route('/openbanking/api/v1/clients/<client_id>/applications/<application_name>/banks/<bank_id>/subscriptions', methods = ['PATCH'])
def banksubscription_register(client_id, application_name,bank_id):
    _process_call_area=g.caller_area
    dbsession = g.dbsession
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
@app.route('/openbanking/api/v1/clients/<client_id>/applications/<application_name>/banks/<bank_id>/subscriptions/<subscription_id>/unregister', methods = ['POST',''])
def banksubscription_unregister(client_id,application_name,bank_id,subscription_id):
    _process_call_area=g.caller_area
    dbsession = g.dbsession
    reply = api.banksubscription_unregister(dbsession,client_id=client_id, bank_id=bank_id, application_name=application_name, subscription_id=subscription_id)
    return jsonify(reply)
#############################################################################
@app.route('/openbanking/api/v1/clients/<client_id>/applications/<application_name>/banks/<bank_id>/bankaccounts/<account_id>/remove', methods = ['POST',''])
def bankaccount_remove(client_id,application_name,bank_id,account_id):
    _process_call_area=g.caller_area
    dbsession = g.dbsession
    reply = api.bankaccount_remove(dbsession,client_id=client_id, bank_id=bank_id, application_name=application_name, account_id=account_id)
    return jsonify(reply)
#############################################################################
@app.route('/openbanking/api/v1/clients/<client_id>/applications/<application_name>/banks/<bank_id>/subscriptions/<subscription_id>/authorize', methods=['PUT','POST', 'PATCH'])
def banksubscription_request_client_authorization(client_id,application_name,bank_id,subscription_id):
    _process_call_area=g.caller_area
    dbsession = g.dbsession
    this_application_name = request.headers.get('Registered-Application')
    if not this_application_name == application_name:
        msg = f'app {this_application_name} can not subscribe for app {application_name}'
        reply = {'api_status': 'error', 'api_message': msg}
        return make_response(jsonify(reply), 400)
        
    reply = api.banksubscription_request_authorization_from_client(dbsession,client_id, bank_id, subscription_id, application_name)
    return jsonify(reply)
#############################################################################
@app.route('/openbanking/api/v1/clients/<client_id>/applications/<application_name>/banks/<bank_id>/subscriptions/create', methods = ['PATCH'])
def banksubscription_create(client_id,application_name,bank_id):
    _process_call_area=g.caller_area
    dbsession = g.dbsession
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
#############################################################################
@app.route('/openbanking/api/v1/clients/<client_id>/devices/<device_uid>/register', methods = ['PUT','POST','PATCH'])
def client_device_register(client_id,device_uid):
    _process_call_area=g.caller_area
    dbsession = g.dbsession
    update_record = request.json
    update_record.update({'client_id':client_id})
    update_record.update({'device_uid':device_uid})
    update_record.update({'status':'Active'})
    dbreply=db.dbapi_client_device(dbsession, 'Register', update_record, caller_area=_process_call_area)
    return jsonify(dbreply)
#############################################################################
@app.route('/openbanking/api/v1/clients/<client_id>/devices/<device_uid>/unregister', methods = ['PUT','POST','PATCH'])
def client_device_unregister(client_id,device_uid):
    _process_call_area=g.caller_area
    update_record = request.json
    update_record.update({'client_id':client_id})
    update_record.update({'device_uid':device_uid})
    update_record.update({'status':'Unregistered'})
    dbreply=db.dbapi_client_device(dbsession, 'UnRegister', update_record, caller_area=_process_call_area)
    return jsonify(dbreply)
#############################################################################
@app.route('/openbanking/api/v1/clients/<client_id>/interaction/start', methods = ['PUT','POST'])
def start_client_interactions(client_id):
    _process_call_area=g.caller_area
    interaction_record={'client_id':client_id}
    dbreply=db.dbapi_interaction(dbsession, 'start', interaction_record, caller_area=_process_call_area)
    return jsonify( dbreply )
#############################################################################
@app.route('/openbanking/api/v1/clients/<client_id>/interactions/finish', methods = ['PUT','POST'])
def finish_client_interactions(interaction_id,client_id):
    _process_call_area=g.caller_area
    interaction_record={'client_id':client_id}
    dbreply=db.dbapi_interaction(dbsession, 'finish', interaction_record, caller_area=_process_call_area)
    return jsonify( dbreply )
#############################################################################
@app.route('/openbanking/api/v1/clients/<client_id>/interactions/message', methods = ['PUT','POST'])
def add_client_interaction_message(client_id):
    _process_call_area=g.caller_area
    if not request.json:
        reply={'api_status':'error','api_message':'json data Not provided'}
        return make_response(jsonify(reply), 400)
    message_record = request.json
    message_record.update({'client_id':client_id})
    dbreply=db.dbapi_interaction(dbsession, 'message', message_record, caller_area=_process_call_area)
    return jsonify( dbreply )
#############################################################################

# #############################################################################
# #############################################################################
# #############################################################################
# # service providers routes
# #############################################################################
# #############################################################################
# #############################################################################
# #############################################################################
# @app.route('/openbanking/api/v1/serviceproviders', methods = ['GET'])
# #@auth.login_required
# def get_serviceproviders_list():
#     # filterString=f"all"
#     dbreply = db.dbapi_service_provider(dbsession, 'LIST', {}, caller_area=_process_call_area)
#     return jsonify( dbreply )
# #############################################################################
# @app.route('/openbanking/api/v1/serviceproviders', methods = ['PUT','POST'])
# #@auth.login_required
# def new_serviceprovider():
#     if not request.json:
#         reply={'api_status':'error','api_message':'json data Not provided'}
#         return make_response(jsonify(reply), 400)
#     record_data = request.json
#     if not record_data.get('name'):
#         reply={'api_status':'error','api_message':'[name] Not provided'}
#         return make_response(jsonify(reply), 401)
#     if not record_data.get('email'):
#         reply={'api_status':'error','api_message':'[email] Not provided'}
#         return make_response(jsonify(reply), 401)
#     dbreply=db.dbapi_service_provider(dbsession, 'register', record_data, caller_area=_process_call_area)
#     return jsonify( dbreply )
# #############################################################################
# @app.route('/openbanking/api/v1/serviceproviders/<service_provider_id>', methods = ['GET'])
# #@auth.login_required
# def get_serviceprovider(service_provider_id):
#     dbreply=db.dbapi_service_provider(dbsession, 'get', {'service_provider_id':service_provider_id}, caller_area=_process_call_area)
#     return jsonify( dbreply )
# #############################################################################
# @app.route('/openbanking/api/v1/serviceproviders/<service_provider_id>', methods = ['PUT','POST','PATCH'])
# #@auth.login_required
# def update_serviceprovider(service_provider_id):
#     if not request.json:
#         reply={'api_status':'error','api_message':'json data Not provided'}
#         return make_response(jsonify(reply), 400)
#     update_record = request.json
#     update_record.update({'service_provider_id':service_provider_id})
#     dbreply=db.dbapi_service_provider(dbsession, 'update', update_record, caller_area=_process_call_area)
#     return jsonify( dbreply )
# #############################################################################
# @app.route('/openbanking/api/v1/serviceproviders/<service_provider_id>/confirm', methods = ['PUT','POST','PATCH'])
# #@auth.login_required
# def confirm_serviceprovider(service_provider_id):
#     update_record = request.json
#     update_record.update({'service_provider_id':service_provider_id})
#     dbreply=db.dbapi_service_provider(dbsession, 'confirm', update_record, caller_area=_process_call_area)
#     return jsonify( dbreply )
# #############################################################################
# @app.route('/openbanking/api/v1/serviceproviders/<service_provider_id>/unregister', methods = ['PUT','POST','PATCH'])
# #@auth.login_required
# def unregister_serviceprovider(service_provider_id):
#     update_record = request.json
#     update_record.update({'service_provider_id':service_provider_id})
#     dbreply=db.dbapi_service_provider(dbsession, 'UnRegister', update_record, caller_area=_process_call_area)
#     return jsonify(dbreply)
# #############################################################################
# @app.route('/openbanking/api/v1/serviceproviders/<service_provider_id>', methods = ['DELETE'])
# #@auth.login_required
# def delete_serviceprovider(service_provider_id):
#     dbreply=db.dbapi_service_provider(dbsession, 'delete', {'service_provider_id':service_provider_id}, caller_area=_process_call_area)
#     return jsonify( dbreply )#############################################################################

#############################################################################
#############################################################################
#############################################################################
# merchants routes: requiring user login
#############################################################################
#############################################################################
#############################################################################
# @app.route('/openbanking/api/v1/merchants', methods = ['GET'])
# #@auth.login_required
# def get_merchants_list():
#     # filterString=f"all"
#     dbreply = db.dbapi_merchant(dbsession, 'LIST', {}, caller_area=_process_call_area)
#     return jsonify( dbreply )
#############################################################################
@app.route('/openbanking/api/v1/merchants', methods = ['PUT','POST'])
#@auth.login_required
def new_merchant():
    if not request.json:
        reply={'api_status':'error','api_message':'json data Not provided'}
        return make_response(jsonify(reply), 400)
    record_data = request.json
    if not record_data.get('name'):
        reply={'api_status':'error','api_message':'[name] Not provided'}
        return make_response(jsonify(reply), 401)
    if not record_data.get('email'):
        reply={'api_status':'error','api_message':'[email] Not provided'}
        return make_response(jsonify(reply), 401)
    dbreply=db.dbapi_merchant(dbsession, 'register', record_data, caller_area=_process_call_area)
    return jsonify( dbreply )
#############################################################################
@app.route('/openbanking/api/v1/merchants/<merchant_id>', methods = ['GET'])
#@auth.login_required
def get_merchant(merchant_id):
    dbreply=db.dbapi_merchant(dbsession, 'get', {'merchant_id':merchant_id}, caller_area=_process_call_area)
    return jsonify( dbreply )
#############################################################################
@app.route('/openbanking/api/v1/merchants/<merchant_id>', methods = ['PUT','POST','PATCH'])
#@auth.login_required
def update_merchant(merchant_id):
    if not request.json:
        reply={'api_status':'error','api_message':'json data Not provided'}
        return make_response(jsonify(reply), 400)
    update_record = request.json
    update_record.update({'merchant_id':merchant_id})
    dbreply=db.dbapi_merchant(dbsession, 'update', update_record, caller_area=_process_call_area)
    return jsonify( dbreply )
#############################################################################
@app.route('/openbanking/api/v1/merchants/<merchant_id>/confirm', methods = ['PUT','POST','PATCH'])
#@auth.login_required
def confirm_merchant(merchant_id):
    update_record = request.json
    update_record.update({'merchant_id':merchant_id})
    dbreply=db.dbapi_merchant(dbsession, 'confirm', update_record, caller_area=_process_call_area)
    return jsonify( dbreply )
#############################################################################
@app.route('/openbanking/api/v1/merchants/<merchant_id>/unregister', methods = ['PUT','POST','PATCH'])
#@auth.login_required
def unregister_merchant(merchant_id):
    update_record = request.json
    update_record.update({'merchant_id':merchant_id})
    dbreply=db.dbapi_merchant(dbsession, 'UnRegister', update_record, caller_area=_process_call_area)
    return jsonify(dbreply)
#############################################################################
@app.route('/openbanking/api/v1/merchants/<merchant_id>', methods = ['DELETE'])
#@auth.login_required
def delete_merchant(merchant_id):
    dbreply=db.dbapi_merchant(dbsession, 'delete', {'merchant_id':merchant_id}, caller_area=_process_call_area)
    return jsonify(dbreply)
#############################################################################
@app.route('/openbanking/api/v1/merchants/<merchant_id>/banksubscription', methods = ['PUT','POST','PATCH'])
#@auth.login_required
def merchant_banksubscription_register(merchant_id):
    if not request.json:
        reply={'api_status':'error','api_message':'json data Not provided'}
        return make_response(jsonify(reply), 400)
    update_record = request.json
    update_record.update({'merchant_id':merchant_id})
    dbreply = db.dbapi_merchant_bankaccount_register(dbsession,update_record, caller_area=_process_call_area)
    return jsonify(dbreply)
#############################################################################
#############################################################################
#############################################################################
@app.route('/openbanking/api/v1/merchnants/<merchant_id>/pointofsales', methods = ['PUT','POST'])
#@auth.login_required
def new_pointofsale(merchant_id):
    if not request.json:
        reply={'api_status':'error','api_message':'json data Not provided'}
        return make_response(jsonify(reply), 400)
    record_data = request.json
    if not record_data.get('name'):
        reply={'api_status':'error','api_message':'[name] Not provided'}
        return make_response(jsonify(reply), 401)
    record_data.update({'merchant_id':merchant_id}) 
    dbreply = db.dbapi_pointofsale_register(dbsession,record_data, caller_area=_process_call_area)
    return jsonify( dbreply )
#############################################################################
@app.route('/openbanking/api/v1/merchnants/<merchant_id>/employees', methods = ['PUT','POST'])
#@auth.login_required
def new_employee(merchant_id):
    if not request.json:
        reply={'api_status':'error','api_message':'json data Not provided'}
        return make_response(jsonify(reply), 400)
    record_data = request.json
    if not record_data.get('name'):
        reply={'api_status':'error','api_message':'[name] Not provided'}
        return make_response(jsonify(reply), 401)
    record_data.update({'merchant_id':merchant_id}) 
    dbreply = db.dbapi_employee_register(dbsession,record_data, caller_area=_process_call_area)
    return jsonify( dbreply )
#############################################################################
#############################################################################
#############################################################################
# pointofsales routes
#############################################################################
#############################################################################
#############################################################################
# @app.route('/openbanking/api/v1/pointofsales', methods = ['GET'])
# #@auth.login_required
# def get_pointofsales_list():
#     filterString=f"all"
#     dbreply=db.retrieve_rows('pointofsales',filterString)
#     return jsonify( dbreply )
#############################################################################
@app.route('/openbanking/api/v1/pointofsales/<pointofsale_id>', methods = ['GET'])
#@auth.login_required
def get_pointofsale(pointofsale_id):
    dbreply=db.points_of_sale.get(pointofsale_id)
    return jsonify( dbreply )
#############################################################################
@app.route('/openbanking/api/v1/pointofsales/codes/<pointofsale_code>', methods = ['GET'])
#@auth.login_required
def get_pointofsale_with_code(pointofsale_code):
    filterJson={'pointofsale_code':pointofsale_code}
    dbreply=db.points_of_sale.get(filterJson)
    return jsonify( dbreply )
#############################################################################
@app.route('/openbanking/api/v1/pointofsales/<pointofsale_id>', methods = ['PUT','POST','PATCH'])
#@auth.login_required
def update_pointofsale(pointofsale_id):
    if not request.json:
        reply={'api_status':'error','api_message':'json data Not provided'}
        return make_response(jsonify(reply), 400)
    update_record = request.json
    update_record.update({'pointofsale_id':pointofsale_id})
    dbreply = db.dbapi_pointofsale_update(dbsession,update_record, caller_area=_process_call_area)
    return jsonify( dbreply )
#############################################################################
@app.route('/openbanking/api/v1/pointofsales/<pointofsale_id>/unregister', methods = ['PUT','POST','PATCH'])
#@auth.login_required
def unregister_pointofsale(pointofsale_id):
    if not request.json:
        reply={'api_status':'error','api_message':'json data Not provided'}
        return make_response(jsonify(reply), 400)
    update_record = request.json
    update_record.update({'pointofsale_id':pointofsale_id})
    dbreply = db.dbapi_pointofsale_unregister(dbsession,update_record, caller_area=_process_call_area)
    return jsonify(dbreply)
#############################################################################
#############################################################################
#############################################################################
#############################################################################
#############################################################################
@app.route('/openbanking/api/v1/pointofsales/<pointofsale_id>/bankaccount/add', methods = ['PUT','POST','PATCH'])
def pointofsale_bankaccount_add(pointofsale_id,bank_account_id):
    if not request.json:
        reply={'api_status':'error','api_message':'json data Not provided'}
        return make_response(jsonify(reply), 400)
    update_record = request.json
    if not pointofsale_id:
        reply={'api_status':'error','api_message':'pointofsale_id Not provided'}
        return make_response(jsonify(reply), 400)
    if not update_record.get('bank_account_id'):
        reply={'api_status':'error','api_message':'bank_account_id Not provided'}
        return make_response(jsonify(reply), 400)
    update_record.update({'pointofsale_id':pointofsale_id})
    dbreply = db.dbapi_pointofsale_bankaccount_add(dbsession,update_record, caller_area=_process_call_area)
    return jsonify(dbreply)
#############################################################################
@app.route('/openbanking/api/v1/pointofsales/<pointofsale_id>/bankaccount/remove', methods = ['PUT','POST','DELETE'])
def pointofsale_bankaccount_remove(pointofsale_id):
    if not pointofsale_id:
        reply={'api_status':'error','api_message':'pointofsale_id Not provided'}
        return make_response(jsonify(reply), 400)
    pos={'pointofsale_id':pointofsale_id}
    dbreply = db.dbapi_pointofsale_bankaccount_remove(dbsession,pos, caller_area=_process_call_area)
    return jsonify(dbreply)
#############################################################################
@app.route('/openbanking/api/v1/pointofsales/<pointofsale_id>', methods = ['DELETE'])
#@auth.login_required
def delete_pointofsale(pointofsale_id):
    dbreply=db.points_of_sale.delete(pointofsale_id)
    return jsonify( dbreply )
#############################################################################
@app.route('/openbanking/api/v1/pointofsales/<pointofsale_id>/creditinfo', methods = ['GET'])
def get_pointofsale_creditinfo_from_posuid(pointofsale_id):
    res = db.dbapi_pointofsale_credit_info(dbsession,pointofsale_id, caller_area=_process_call_area)
    return jsonify( res )
#############################################################################
@app.route('/openbanking/api/v1/pointofsales/<pointofsale_id>/interactions/start', methods = ['PUT','POST'])
def start_pointofsale_interactions(pointofsale_id):
    record={'pointofsale_id':pointofsale_id}
    result = db.dbapi_interaction_start(dbsession,record, caller_area=_process_call_area)
    return jsonify( result )
#############################################################################
@app.route('/openbanking/api/v1/pointofsales/<pointofsale_id>/interactions/finish', methods = ['PUT','POST'])
def finish_pointofsale_interactions(pointofsale_id):
    record={'pointofsale_id':pointofsale_id}
    result = db.dbapi_interaction_finish(dbsession,record, caller_area=_process_call_area)
    return jsonify( result )
#############################################################################
@app.route('/openbanking/api/v1/pointofsales/<pointofsale_id>/interactions/messages', methods = ['PUT','POST'])
def add_pointofsale_interaction_message(pointofsale_id):
    if not request.json:
        reply={'api_status':'error','api_message':'json data Not provided'}
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
@app.route('/openbanking/api/v1/employees/<employee_id>', methods = ['GET'])
#@auth.login_required
def get_employee(employee_id):
    dbreply=db.employees.get(employee_id)
    return jsonify( dbreply )
#############################################################################
@app.route('/openbanking/api/v1/employees/codes/<employee_code>', methods = ['GET'])
#@auth.login_required
def get_employee_with_code(employee_code):
    filterJson={'employee_code':employee_code}
    dbreply=db.employees.get(filterJson)
    return jsonify( dbreply )
#############################################################################
@app.route('/openbanking/api/v1/employees/<employee_id>', methods = ['PUT','POST','PATCH'])
#@auth.login_required
def update_employee(employee_id):
    if not request.json:
        reply={'api_status':'error','api_message':'json data Not provided'}
        return make_response(jsonify(reply), 400)
    update_record = request.json
    update_record.update({'employee_id':employee_id})
    dbreply = db.dbapi_employee_update(update_record)
    return jsonify( dbreply )
#############################################################################
@app.route('/openbanking/api/v1/employees/<employee_id>/unregister', methods = ['PUT','POST','PATCH'])
#@auth.login_required
def unregister_employee(employee_id):
    if not request.json:
        reply={'api_status':'error','api_message':'json data Not provided'}
        return make_response(jsonify(reply), 400)
    update_record = request.json
    update_record.update({'employee_id':employee_id})
    dbreply = db.dbapi_employee_unregister(update_record)
    return jsonify(dbreply)
#############################################################################
@app.route('/openbanking/api/v1/employees/<employee_id>', methods = ['DELETE'])
#@auth.login_required
def delete_employee(employee_id):
    dbreply=db.employees.delete(employee_id)
    return jsonify( dbreply )
#############################################################################
#############################################################################
#############################################################################
#############################################################################
# consumers routes
#############################################################################
#############################################################################
#############################################################################
#############################################################################
# @app.route('/openbanking/api/v1/consumers', methods = ['GET'])
# #@auth.login_required
# def get_consumers_list():
#     # filterString=f"all"
#     dbreply = db.dbapi_consumer(dbsession, 'LIST', {}, caller_area=_process_call_area)
#     return jsonify( dbreply )
# #############################################################################
# @app.route('/openbanking/api/v1/consumers', methods = ['PUT','POST'])
# #@auth.login_required
# def new_consumer():
#     if not request.json:
#         reply={'api_status':'error','api_message':'json data Not provided'}
#         return make_response(jsonify(reply), 400)
#     record_data = request.json
#     if not record_data.get('name'):
#         reply={'api_status':'error','api_message':'[name] Not provided'}
#         return make_response(jsonify(reply), 401)
#     if not record_data.get('email'):
#         reply={'api_status':'error','api_message':'[email] Not provided'}
#         return make_response(jsonify(reply), 401)
#     dbreply=db.dbapi_consumer(dbsession, 'register', record_data, caller_area=_process_call_area)
#     return jsonify( dbreply )
# #############################################################################
# @app.route('/openbanking/api/v1/consumers/<consumer_id>', methods = ['GET'])
# #@auth.login_required
# def get_consumer(consumer_id):
#     dbreply=db.dbapi_consumer(dbsession, 'get', {'consumer_id':consumer_id}, caller_area=_process_call_area)
#     return jsonify( dbreply )
# #############################################################################
# @app.route('/openbanking/api/v1/consumers/<consumer_id>', methods = ['PUT','POST','PATCH'])
# #@auth.login_required
# def update_consumer(consumer_id):
#     if not request.json:
#         reply={'api_status':'error','api_message':'json data Not provided'}
#         return make_response(jsonify(reply), 400)
#     update_record = request.json
#     update_record.update({'consumer_id':consumer_id})
#     dbreply=db.dbapi_consumer(dbsession, 'update', update_record, caller_area=_process_call_area)
#     return jsonify( dbreply )
# #############################################################################
# @app.route('/openbanking/api/v1/consumers/<consumer_id>/confirm', methods = ['PUT','POST','PATCH'])
# #@auth.login_required
# def confirm_consumer(consumer_id):
#     update_record = request.json
#     update_record.update({'consumer_id':consumer_id})
#     dbreply=db.dbapi_consumer(dbsession, 'confirm', update_record, caller_area=_process_call_area)
#     return jsonify( dbreply )
# #############################################################################
# @app.route('/openbanking/api/v1/consumers/<consumer_id>/unregister', methods = ['PUT','POST','PATCH'])
# #@auth.login_required
# def unregister_consumer(consumer_id):
#     update_record = request.json
#     update_record.update({'consumer_id':consumer_id})
#     dbreply=db.dbapi_consumer(dbsession, 'UnRegister', update_record, caller_area=_process_call_area)
#     return jsonify(dbreply)
# #############################################################################
# @app.route('/openbanking/api/v1/consumers/<consumer_id>', methods = ['DELETE'])
# #@auth.login_required
# def delete_consumer(consumer_id):
#     dbreply=db.dbapi_consumer(dbsession, 'delete', {'consumer_id':consumer_id}, caller_area=_process_call_area)
#     return jsonify(dbreply)
# #############################################################################
# @app.route('/openbanking/api/v1/consumers/<consumer_id>/banksubscription', methods = ['PUT','POST','PATCH'])
# #@auth.login_required
# def consumer_banksubscription_register(consumer_id):
#     if not request.json:
#         reply={'api_status':'error','api_message':'json data Not provided'}
#         return make_response(jsonify(reply), 400)
#     update_record = request.json
#     update_record.update({'consumer_id':consumer_id})
#     dbreply = db.dbapi_consumer_banksubscription_register(update_record)
#     return jsonify(dbreply)
# #############################################################################
# @app.route('/openbanking/api/v1/consumers/<consumer_id>/interaction/start', methods = ['PUT','POST'])
# def start_consumer_interactions(consumer_id):
#     record={'consumer_id':consumer_id}
#     result = db.dbapi_interaction_start(record)
#     return jsonify( result )
# ##########################################################################################################################
# #############################################################################
# @app.route('/openbanking/api/v1/consumers/<consumer_id>/interactions/finish', methods = ['PUT','POST'])
# def finish_consumer_interactions(consumer_id):
#     record={'consumer_id':consumer_id}
#     result = db.dbapi_interaction_finish(record)
#     return jsonify( result )
##########################################################################################################################
# @app.route('/openbanking/api/v1/consumers/<consumer_id>/interactions/messages', methods = ['PUT','POST'])
# def add_consumer_interaction_message(consumer_id):
#     if not request.json:
#         reply={'api_status':'error','api_message':'json data Not provided'}
#         return make_response(jsonify(reply), 400)
#     message_record = request.json
#     message_record.update({'consumer_id':consumer_id})
#     result = db.dbapi_interaction_message_add(message_record)
#     return jsonify( result )
#############################################################################

#############################################################################
#############################################################################
#############################################################################
# banks routes
#############################################################################
#############################################################################
#############################################################################
# @app.route('/openbanking/api/v1/banks', methods = ['PUT','POST'])
# def new_bank():
#     if not request.json:
#         reply={'api_status':'error','api_message':'json data Not provided'}
#         return make_response(jsonify(reply), 400)
#     record_data = request.json
#     if not record_data.get('bank_name'):
#         reply={'api_status':'error','api_message':'[name] Not provided'}
#         return make_response(jsonify(reply), 401)
#     if not record_data.get('bank_code'):
#         reply={'api_status':'error','api_message':'[bank_code] Not provided'}
#         return make_response(jsonify(reply), 401)
#     if not record_data.get('bank_BIC'):
#         reply={'api_status':'error','api_message':'[bank_BIC] Not provided'}
#         return make_response(jsonify(reply), 401)
#     dbreply = db.dbapi_bank_register(record_data)
#     # if dbreply.get('status') == 'success':
#     #     record_data = dbreply.get('data',{})
#     #     dbreply = db.dbapi_register_bank(record_data)
#     return jsonify( dbreply )
# #############################################################################
# @app.route('/openbanking/api/v1/banks/<bank_id>', methods = ['GET'])
# def get_bank(bank_id):
#     dbreply=db.banks.get(bank_id)
#     return jsonify( dbreply )
# #############################################################################
# @app.route('/openbanking/api/v1/banks/<bank_id>', methods = ['PUT','POST','PATCH'])
# def update_bank(bank_id):
#     if not request.json:
#         reply={'api_status':'error','api_message':'json data Not provided'}
#         return make_response(jsonify(reply), 400)
#     update_record = request.json
#     update_record.update({'bank_id':bank_id})
#     dbreply = db.dbapi_bank_update(update_record)
#     return jsonify( dbreply )
# #############################################################################
# @app.route('/openbanking/api/v1/banks/<bank_id>/deactivate', methods = ['PUT','POST','PATCH'])
# #@auth.login_required
# def deactivate_bank(bank_id):
#     if not request.json:
#         reply={'api_status':'error','api_message':'json data Not provided'}
#         return make_response(jsonify(reply), 400)
#     update_record = request.json
#     update_record.update({'bank_id':bank_id})
#     update_record.update({'status':'Inactive'})
#     dbreply = db.dbapi_bank_update(update_record)
#     return jsonify( dbreply )
# #############################################################################
# @app.route('/openbanking/api/v1/banks/<bank_id>/activate', methods = ['PUT','POST','PATCH'])
# #@auth.login_required
# def activate_bank(bank_id):
#     update_record = request.json
#     update_record.update({'bank_id':bank_id})
#     update_record.update({'status':'Active'})
#     dbreply = db.dbapi_bank_update(update_record)
#     return jsonify( dbreply )
# #############################################################################
# @app.route('/openbanking/api/v1/banks/<bank_id>', methods = ['DELETE'])
# #@auth.login_required
# def delete_bank(bank_id):
#     dbreply=db.banks.delete(bank_id)
#     return jsonify( dbreply )
# #############################################################################
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
#         reply={'api_status':'error','api_message':'json data Not provided'}
#         return make_response(jsonify(reply), 400)
#         #abort(400)
#     request_data = request.json
#     #basic validations before calling the database api
#     if not request_data.get('merchant_email'):
#         reply={'api_status':'error','api_message':'[merchant_email] Not provided'}
#         return make_response(jsonify(reply), 401)
#     if not request_data.get('merchant_name'):
#         reply={'api_status':'error','api_message':'[merchant_name] Not provided'}
#         return make_response(jsonify(reply), 401)
#     if not request_data.get('merchant_code'):
#         reply={'api_status':'error','api_message':'[merchant_code] Not provided'}
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
#         reply={'api_status':'error','api_message':'json data Not provided'}
#         return make_response(jsonify(reply), 400)
#         #abort(400)
#     request_data = request.json
#     # #basic validations before calling the database api
#     # if not request_data.get('email'):
#     #     reply={'api_status':'error','api_message':'[email] Not provided'}
#     #     return make_response(jsonify(reply), 401)
#     # if not request_data.get('name'):
#     #     reply={'api_status':'error','api_message':'[name] Not provided'}
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
#         reply={'api_status':'error','api_message':'json data Not provided'}
#         return make_response(jsonify(reply), 400)
#         #abort(400)
#     request_data = request.json
#     #basic validations before calling the database api
#     if not request_data.get('pos_code'):
#         reply={'api_status':'error','api_message':'[pos_code] Not provided'}
#         return make_response(jsonify(reply), 401)
#     if not request_data.get('merchant_code'):
#         reply={'api_status':'error','api_message':'[merchant_code] Not provided'}
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
    dbsession = db.get_dbsession(debug=99)
    dbsession.close()

    #db.database_schema.connect()
    #app.run(debug=False)
    # app.run(host='0.0.0.0', port=5555)
    #app.run(host='127.0.0.1', port=5555)
    #app.run(debug=False,port=5555,threaded=True)
    #app.run(debug=False, port=5555, threaded=False, processes=3) #'Your platform does not support forking.'
    app.run(debug=False, port=5555, threaded=True)
    
    #threaded=False, processes=3