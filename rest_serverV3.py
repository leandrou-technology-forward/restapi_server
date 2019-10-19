#!flask/bin/python
import os
import sys
if not (os.path.dirname(__file__) in sys.path): sys.path.append(os.path.dirname(__file__))
print(sys.path)

from flask import Flask, jsonify, abort, request, make_response, url_for,redirect
from flask_httpauth import HTTPBasicAuth
from flask import json
from flask import session, g

from _tokenServices import token_is_valid
from colorama import Fore
import datetime
import secrets
import requests
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

# s = requests.Session()
# # s.auth = ('user', 'pass')
# x = s.headers.get('x-test')
# if not x:
#     s.headers.update({'x-test': 'bobbistarr'})
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
##########################################################################################################################
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
    return make_response(jsonify( { 'error': 'Unauthorized access' } ), 403)
    # return 403 instead of 401 to prevent browsers from displaying the default auth dialog
##########################################################################################################################
##########################################################################################################################
##########################################################################################################################
# app error handlers
##########################################################################################################################
##########################################################################################################################
##########################################################################################################################
@app.errorhandler(400)
def not_found(error):
    return make_response(jsonify( { 'error': 'Bad request' } ), 400)
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 
@app.errorhandler(404)
def not_found1(error):
    return make_response(jsonify( { 'error': 'Not found' } ), 404)
##########################################################################################################################
##########################################################################################################################
##########################################################################################################################
# before_request processing (authenticate each request base on authentication_method stored in request.headers)
##########################################################################################################################
##########################################################################################################################
##########################################################################################################################
@app.before_request
def before_request_func():
    dbsession = db.get_dbsession(debug=99)
    session["foo"] = "bar"
    g.username = "root"
    g.dbsession = dbsession
    caller_info={}
    print(f'{Fore.RED}==>{Fore.RESET} {Fore.LIGHTYELLOW_EX}{request.path}{Fore.RESET}')
    if request.path.upper().find('/openbanking/api/'.upper()) >=0:
        #request_headers_json = get_headers(request)
        # request_params_json=get_params(request)
        application_name = request.headers.get('Registered-Application')
        application_client_id = request.headers.get('Registered-Application-CLIENT-Id')
        application_client_secretKey = request.headers.get('Registered-Application-CLIENT-Secretkey')

        # all lower case from json version of headers
        # application_name = request_headers_json.get('registered_application','')
        # application_client_id = request_headers_json.get('registered_application_client_id', '')
        # application_client_secretKey = request_headers_json.get('registered_application_client_secretkey', '')

        if not application_name or not application_client_id or not application_client_secretKey:
            reply={'status':'error','message':'registered application credentials not provided'}
            return make_response(jsonify(reply), 403)
        caller_info={'application_name':application_name,'application_client_id':application_client_id}
        device_uid = request.headers.get('Device-Uid')
        #device_uid = request_headers_json.get('device_uid')
        if device_uid:
            # geolocation_lat = request_headers_json.get('geolocation_lat')
            # geolocation_lon = request_headers_json.get('geolocation_lon')
            # requestor = 'client' #request_headers_json.get('requestor')
            # client_id = request_headers_json.get('client_id')
            geolocation_lat = request.headers.get('Geolocation-Lat')
            geolocation_lon = request.headers.get('Geolocation-Lon')
            #requestor = 'client' #request.headers.get('Requestor')
            client_id = request.headers.get('CLIENT-Id')
            caller_info.update({'device_uid':device_uid,'geolocation_lat':geolocation_lat,'geolocation_lon':geolocation_lon,'client_id':client_id})

            db.dbapi_device_log(dbsession, device_uid, application_name, geolocation_lat, geolocation_lon, client_id)

        #authentication_method = request_headers_json.get('authentication_method')
        authentication_method = request.headers.get('Authentication-Method')

        if authentication_method == 'access_token':
            #get the access token from the header
            #access_token = request_headers_json.get('access_token')        
            access_token = request.headers.get('Access-Token')        
            if not access_token:
                reply={'status':'error','message':'access token not provided'}
                return make_response(jsonify(reply), 403)
            # local validation first
            # but we need to implement the same in database
            # if not token_is_valid(access_token):
            #     reply={'status':'error','message':'expired access token used for authentication'}
            #     return make_response(jsonify(reply), 403)
            if not db.dbapi_token_is_valid(dbsession,access_token):
                reply={'status':'error','message':'invalid or expired access token'}
                return make_response(jsonify(reply), 403)
            if debug:
                print('authentication_method',authentication_method,'OK')

        elif authentication_method == 'registered_application_credentials':
            if not db.dbapi_application_credentials_are_valid(dbsession,application_name,application_client_id,application_client_secretKey):
                reply={'status':'error','message':'invalid or expired application credentials'}
                return make_response(jsonify(reply), 403)
            if debug:
                print('authentication_method',authentication_method,'OK')

        elif authentication_method == 'none':
            application_name=request_params_json.get('application_name','')
            application_client_id=request_params_json.get('application_client_id','')
            application_client_secretKey = request_params_json.get('application_client_secretKey', '')
            if debug:
                print('authentication_method',authentication_method,'OK')

        else:
            reply={'status':'error','message':'invalid authentication method'}
            #return make_response(jsonify(reply), 403)
            if debug:
                print('authentication_method', authentication_method, 'OK')
                #x=1
##########################################################################################################################
##########################################################################################################################
##########################################################################################################################
@app.after_request
def after_request_func(response):
    x=session["foo"] 
    username=g.username
    dbsession = g.dbsession
    print(x,username,dbsession.session_id)    
#     print('---------------------------------')
#     print('@app.after_request',response)
#     print('---------------------------------')
    dbsession.close()
    return response

# @app.after_request
# # def set_cookies2():
# #     log_message('-----------------------------------------',msgType='info',msgOffset='+1')
# def apply_caching(response):
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
@app.route('/authorization', methods = ['GET','PUT','POST','PATCH'])
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
# test routes
#############################################################################
#############################################################################
#############################################################################
@app.route('/openbanking/api/v1/underconstruction', methods = ['GET','POST','PUNCH','PUT','DELETE'])
def underconstruction():
    if not request.json:
        reply={'status':'success','message':'under constrcution by leandrou technology forward ltd'}
        return make_response(jsonify(reply), 200)
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
    if not request.json:
        reply={'status':'error','message':'json data Not provided'}
        return make_response(jsonify(reply), 400)
    request_data = request.json
    for k in request_params_json:
        v=request_params_json.get(k)
        request_data.update({k: v})
    res = db.dbapi_token_get_access_token(dbsession, request_data)
    print(res)
    return jsonify( res )
#############################################################################
#############################################################################
#############################################################################
#############################################################################
# subscriptions routes
#############################################################################
#############################################################################
#x############################################################################
@app.route('/openbanking/api/v1/applications', methods = ['PUT','POST'])
#@auth.login_required
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
@app.route('/openbanking/api/v1/applications/<application_id>', methods = ['GET'])
#@auth.login_required
def get_application(application_id):
    dbreply=db.dbapi_application(dbsession, 'get', {'application_id':application_id}, filter_dict={}, caller_dict={}, call_level=-1,debug_level=-1)
    return jsonify( dbreply )
#############################################################################
@app.route('/openbanking/api/v1/applications/<application_id>', methods = ['PUT','POST','PATCH'])
#@auth.login_required
def update_application(application_id):
    if not request.json:
        reply={'status':'error','message':'json data Not provided'}
        return make_response(jsonify(reply), 400)
    update_record = request.json
    update_record.update({'application_id':application_id})
    dbreply=db.dbapi_application(dbsession, 'update', update_record, filter_dict={}, caller_dict={}, call_level=-1,debug_level=-1)
    return jsonify( dbreply )
#############################################################################
@app.route('/openbanking/api/v1/applications/<application_id>/unregister', methods = ['PUT','POST','PATCH'])
#@auth.login_required
def unregister_application(application_id):
    if not request.json:
        reply={'status':'error','message':'json data Not provided'}
        return make_response(jsonify(reply), 400)
    update_record = request.json
    update_record.update({'application_id':application_id})
    dbreply=db.dbapi_application(dbsession, 'unregister', update_record, filter_dict={}, caller_dict={}, call_level=-1,debug_level=-1)
    return jsonify(dbreply)
#############################################################################
@app.route('/openbanking/api/v1/applications/<application_id>/apis/<api_name>', methods = ['PUT','POST','PATCH'])
#@auth.login_required
def application_api_register(application_id,api_name):
    update_record = request.json
    update_record.update({'application_id':application_id})
    update_record.update({'api_name':api_name})
    dbreply=db.dbapi_application(dbsession, 'api_register', update_record, filter_dict={}, caller_dict={}, call_level=-1,debug_level=-1)
    return jsonify(dbreply)
#############################################################################
@app.route('/openbanking/api/v1/applications/<application_id>', methods = ['DELETE'])
#@auth.login_required
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
@app.route('/openbanking/api/v1/clients', methods = ['GET'])
#@auth.login_required
def get_clients_list():
    # filterString=f"all"
    dbreply = db.dbapi_client(dbsession, 'LIST', {}, filter_dict={}, caller_dict={}, call_level=-1, debug_level=-1)
    return jsonify( dbreply )
#############################################################################
@app.route('/openbanking/api/v1/clients', methods = ['PUT','POST'])
#@auth.login_required
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
@app.route('/openbanking/api/v1/clients/<client_id>', methods = ['GET'])
#@auth.login_required
def get_client(client_id):
    dbreply=db.dbapi_client(dbsession, 'get', {'client_id':client_id}, filter_dict={}, caller_dict={}, call_level=-1,debug_level=-1)
    return jsonify( dbreply )
#############################################################################
@app.route('/openbanking/api/v1/clients/<client_id>', methods = ['PUT','POST','PATCH'])
#@auth.login_required
def update_client(client_id):
    if not request.json:
        reply={'status':'error','message':'json data Not provided'}
        return make_response(jsonify(reply), 400)
    update_record = request.json
    update_record.update({'client_id':client_id})
    dbreply=db.dbapi_client(dbsession, 'update', update_record, filter_dict={}, caller_dict={}, call_level=-1,debug_level=-1)
    return jsonify( dbreply )
#############################################################################
@app.route('/openbanking/api/v1/clients/<client_id>/confirm', methods = ['PUT','POST','PATCH'])
#@auth.login_required
def confirm_client(client_id):
    update_record = request.json
    update_record.update({'client_id':client_id})
    dbreply=db.dbapi_client(dbsession, 'confirm', update_record, filter_dict={}, caller_dict={}, call_level=-1,debug_level=-1)
    return jsonify( dbreply )
#############################################################################
@app.route('/openbanking/api/v1/clients/<client_id>/unregister', methods = ['PUT','POST','PATCH'])
#@auth.login_required
def unregister_client(client_id):
    update_record = request.json
    update_record.update({'client_id':client_id})
    dbreply=db.dbapi_client(dbsession, 'UnRegister', update_record, filter_dict={}, caller_dict={}, call_level=-1,debug_level=-1)
    return jsonify(dbreply)
#############################################################################
@app.route('/openbanking/api/v1/clients/<client_id>', methods = ['DELETE'])
#@auth.login_required
def delete_client(client_id):
    dbreply=db.dbapi_client(dbsession, 'delete', {'client_id':client_id}, filter_dict={}, caller_dict={}, call_level=-1,debug_level=-1)
    return jsonify( dbreply )
#############################################################################
@app.route('/openbanking/api/v1/clients/<client_id>/applications/<application_name>/banks/<bank_id>/subscriptions', methods = ['PATCH'])
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
@app.route('/openbanking/api/v1/clients/<client_id>/applications/<application_name>/banks/<bank_id>/subscriptions/<subscription_id>/unregister', methods = ['POST',''])
def banksubscription_unregister(client_id,application_name,bank_id,subscription_id):
    reply = api.banksubscription_unregister(dbsession,client_id=client_id, bank_id=bank_id, application_name=application_name, subscription_id=subscription_id)
    return jsonify(reply)
#############################################################################
@app.route('/openbanking/api/v1/clients/<client_id>/applications/<application_name>/banks/<bank_id>/bankaccounts/<account_id>/remove', methods = ['POST',''])
def bankaccount_remove(client_id,application_name,bank_id,account_id):
    reply = api.bankaccount_remove(dbsession,client_id=client_id, bank_id=bank_id, application_name=application_name, account_id=account_id)
    return jsonify(reply)
#############################################################################
@app.route('/openbanking/api/v1/clients/<client_id>/applications/<application_name>/banks/<bank_id>/subscriptions/<subscription_id>/authorize', methods=['PUT','POST', 'PATCH'])
def banksubscription_request_client_authorization(client_id,application_name,bank_id,subscription_id):
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
@app.route('/openbanking/api/v1/clients/<client_id>/devices/<device_uid>/register', methods = ['PUT','POST','PATCH'])
#@auth.login_required
def client_device_register(client_id,device_uid):
    update_record = request.json
    update_record.update({'client_id':client_id})
    update_record.update({'device_uid':device_uid})
    update_record.update({'status':'Active'})
    dbreply=db.dbapi_client_device(dbsession, 'Register', update_record, filter_dict={}, caller_dict={}, call_level=-1,debug_level=-1)
    return jsonify(dbreply)
#############################################################################
@app.route('/openbanking/api/v1/clients/<client_id>/devices/<device_uid>/unregister', methods = ['PUT','POST','PATCH'])
#@auth.login_required
def client_device_unregister(client_id,device_uid):
    update_record = request.json
    update_record.update({'client_id':client_id})
    update_record.update({'device_uid':device_uid})
    update_record.update({'status':'Unregistered'})
    dbreply=db.dbapi_client_device(dbsession, 'UnRegister', update_record, filter_dict={}, caller_dict={}, call_level=-1,debug_level=-1)
    return jsonify(dbreply)
#############################################################################
@app.route('/openbanking/api/v1/clients/<client_id>/interaction/start', methods = ['PUT','POST'])
def start_client_interactions(client_id):
    interaction_record={'client_id':client_id}
    # result = db.dbapi_interaction_start(record)
    dbreply=db.dbapi_interaction(dbsession, 'start', interaction_record, filter_dict={}, caller_dict={}, call_level=-1,debug_level=-1)
    return jsonify( dbreply )
#############################################################################
@app.route('/openbanking/api/v1/clients/<client_id>/interactions/finish', methods = ['PUT','POST'])
def finish_client_interactions(interaction_id,client_id):
    # record={'client_id':client_id}
    # result = db.dbapi_interaction_finish(record)
    interaction_record={'client_id':client_id}
    # result = db.dbapi_interaction_start(record)
    dbreply=db.dbapi_interaction(dbsession, 'finish', interaction_record, filter_dict={}, caller_dict={}, call_level=-1,debug_level=-1)
    return jsonify( dbreply )
#############################################################################
@app.route('/openbanking/api/v1/clients/<client_id>/interactions/message', methods = ['PUT','POST'])
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
@app.route('/openbanking/api/v1/serviceproviders', methods = ['GET'])
#@auth.login_required
def get_serviceproviders_list():
    # filterString=f"all"
    dbreply = db.dbapi_service_provider(dbsession, 'LIST', {}, filter_dict={}, caller_dict={}, call_level=-1, debug_level=-1)
    return jsonify( dbreply )
#############################################################################
@app.route('/openbanking/api/v1/serviceproviders', methods = ['PUT','POST'])
#@auth.login_required
def new_serviceprovider():
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
    dbreply=db.dbapi_service_provider(dbsession, 'register', record_data, filter_dict={}, caller_dict={}, call_level=-1,debug_level=-1)
    return jsonify( dbreply )
#############################################################################
@app.route('/openbanking/api/v1/serviceproviders/<service_provider_id>', methods = ['GET'])
#@auth.login_required
def get_serviceprovider(service_provider_id):
    dbreply=db.dbapi_service_provider(dbsession, 'get', {'service_provider_id':service_provider_id}, filter_dict={}, caller_dict={}, call_level=-1,debug_level=-1)
    return jsonify( dbreply )
#############################################################################
@app.route('/openbanking/api/v1/serviceproviders/<service_provider_id>', methods = ['PUT','POST','PATCH'])
#@auth.login_required
def update_serviceprovider(service_provider_id):
    if not request.json:
        reply={'status':'error','message':'json data Not provided'}
        return make_response(jsonify(reply), 400)
    update_record = request.json
    update_record.update({'service_provider_id':service_provider_id})
    dbreply=db.dbapi_service_provider(dbsession, 'update', update_record, filter_dict={}, caller_dict={}, call_level=-1,debug_level=-1)
    return jsonify( dbreply )
#############################################################################
@app.route('/openbanking/api/v1/serviceproviders/<service_provider_id>/confirm', methods = ['PUT','POST','PATCH'])
#@auth.login_required
def confirm_serviceprovider(service_provider_id):
    update_record = request.json
    update_record.update({'service_provider_id':service_provider_id})
    dbreply=db.dbapi_service_provider(dbsession, 'confirm', update_record, filter_dict={}, caller_dict={}, call_level=-1,debug_level=-1)
    return jsonify( dbreply )
#############################################################################
@app.route('/openbanking/api/v1/serviceproviders/<service_provider_id>/unregister', methods = ['PUT','POST','PATCH'])
#@auth.login_required
def unregister_serviceprovider(service_provider_id):
    update_record = request.json
    update_record.update({'service_provider_id':service_provider_id})
    dbreply=db.dbapi_service_provider(dbsession, 'UnRegister', update_record, filter_dict={}, caller_dict={}, call_level=-1,debug_level=-1)
    return jsonify(dbreply)
#############################################################################
@app.route('/openbanking/api/v1/serviceproviders/<service_provider_id>', methods = ['DELETE'])
#@auth.login_required
def delete_serviceprovider(service_provider_id):
    dbreply=db.dbapi_service_provider(dbsession, 'delete', {'service_provider_id':service_provider_id}, filter_dict={}, caller_dict={}, call_level=-1,debug_level=-1)
    return jsonify( dbreply )#############################################################################
#############################################################################
#############################################################################
#############################################################################
# merchants routes
#############################################################################
#############################################################################
#############################################################################
#############################################################################
@app.route('/openbanking/api/v1/merchants', methods = ['GET'])
#@auth.login_required
def get_merchants_list():
    # filterString=f"all"
    dbreply = db.dbapi_merchant(dbsession, 'LIST', {}, filter_dict={}, caller_dict={}, call_level=-1, debug_level=-1)
    return jsonify( dbreply )
#############################################################################
@app.route('/openbanking/api/v1/merchants', methods = ['PUT','POST'])
#@auth.login_required
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
@app.route('/openbanking/api/v1/merchants/<merchant_id>', methods = ['GET'])
#@auth.login_required
def get_merchant(merchant_id):
    dbreply=db.dbapi_merchant(dbsession, 'get', {'merchant_id':merchant_id}, filter_dict={}, caller_dict={}, call_level=-1,debug_level=-1)
    return jsonify( dbreply )
#############################################################################
@app.route('/openbanking/api/v1/merchants/<merchant_id>', methods = ['PUT','POST','PATCH'])
#@auth.login_required
def update_merchant(merchant_id):
    if not request.json:
        reply={'status':'error','message':'json data Not provided'}
        return make_response(jsonify(reply), 400)
    update_record = request.json
    update_record.update({'merchant_id':merchant_id})
    dbreply=db.dbapi_merchant(dbsession, 'update', update_record, filter_dict={}, caller_dict={}, call_level=-1,debug_level=-1)
    return jsonify( dbreply )
#############################################################################
@app.route('/openbanking/api/v1/merchants/<merchant_id>/confirm', methods = ['PUT','POST','PATCH'])
#@auth.login_required
def confirm_merchant(merchant_id):
    update_record = request.json
    update_record.update({'merchant_id':merchant_id})
    dbreply=db.dbapi_merchant(dbsession, 'confirm', update_record, filter_dict={}, caller_dict={}, call_level=-1,debug_level=-1)
    return jsonify( dbreply )
#############################################################################
@app.route('/openbanking/api/v1/merchants/<merchant_id>/unregister', methods = ['PUT','POST','PATCH'])
#@auth.login_required
def unregister_merchant(merchant_id):
    update_record = request.json
    update_record.update({'merchant_id':merchant_id})
    dbreply=db.dbapi_merchant(dbsession, 'UnRegister', update_record, filter_dict={}, caller_dict={}, call_level=-1,debug_level=-1)
    return jsonify(dbreply)
#############################################################################
@app.route('/openbanking/api/v1/merchants/<merchant_id>', methods = ['DELETE'])
#@auth.login_required
def delete_merchant(merchant_id):
    dbreply=db.dbapi_merchant(dbsession, 'delete', {'merchant_id':merchant_id}, filter_dict={}, caller_dict={}, call_level=-1,debug_level=-1)
    return jsonify(dbreply)
#############################################################################
@app.route('/openbanking/api/v1/merchants/<merchant_id>/banksubscription', methods = ['PUT','POST','PATCH'])
#@auth.login_required
def merchant_banksubscription_register(merchant_id):
    if not request.json:
        reply={'status':'error','message':'json data Not provided'}
        return make_response(jsonify(reply), 400)
    update_record = request.json
    update_record.update({'merchant_id':merchant_id})
    dbreply = db.dbapi_merchant_bankaccount_register(update_record)
    return jsonify(dbreply)
#############################################################################
#############################################################################
#############################################################################
@app.route('/openbanking/api/v1/merchnants/<merchant_id>/pointofsales', methods = ['PUT','POST'])
#@auth.login_required
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
@app.route('/openbanking/api/v1/merchnants/<merchant_id>/employees', methods = ['PUT','POST'])
#@auth.login_required
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
@app.route('/openbanking/api/v1/pointofsales', methods = ['GET'])
#@auth.login_required
def get_pointofsales_list():
    filterString=f"all"
    dbreply=db.retrieve_rows('pointofsales',filterString)
    return jsonify( dbreply )
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
        reply={'status':'error','message':'json data Not provided'}
        return make_response(jsonify(reply), 400)
    update_record = request.json
    update_record.update({'pointofsale_id':pointofsale_id})
    dbreply = db.dbapi_pointofsale_update(update_record)
    return jsonify( dbreply )
#############################################################################
@app.route('/openbanking/api/v1/pointofsales/<pointofsale_id>/unregister', methods = ['PUT','POST','PATCH'])
#@auth.login_required
def unregister_pointofsale(pointofsale_id):
    if not request.json:
        reply={'status':'error','message':'json data Not provided'}
        return make_response(jsonify(reply), 400)
    update_record = request.json
    update_record.update({'pointofsale_id':pointofsale_id})
    dbreply = db.dbapi_pointofsale_unregister(update_record)
    return jsonify(dbreply)
#############################################################################
#############################################################################
#############################################################################
#############################################################################
#############################################################################
@app.route('/openbanking/api/v1/pointofsales/<pointofsale_id>/bankaccount/add', methods = ['PUT','POST','PATCH'])
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
@app.route('/openbanking/api/v1/pointofsales/<pointofsale_id>/bankaccount/remove', methods = ['PUT','POST','DELETE'])
def pointofsale_bankaccount_remove(pointofsale_id):
    if not pointofsale_id:
        reply={'status':'error','message':'pointofsale_id Not provided'}
        return make_response(jsonify(reply), 400)
    pos={'pointofsale_id':pointofsale_id}
    dbreply = db.dbapi_pointofsale_bankaccount_remove(pos)
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
    res = db.dbapi_pointofsale_credit_info(pointofsale_id)
    return jsonify( res )
#############################################################################
@app.route('/openbanking/api/v1/pointofsales/<pointofsale_id>/interactions/start', methods = ['PUT','POST'])
def start_pointofsale_interactions(pointofsale_id):
    record={'pointofsale_id':pointofsale_id}
    result = db.dbapi_interaction_start(record)
    return jsonify( result )
#############################################################################
@app.route('/openbanking/api/v1/pointofsales/<pointofsale_id>/interactions/finish', methods = ['PUT','POST'])
def finish_pointofsale_interactions(pointofsale_id):
    record={'pointofsale_id':pointofsale_id}
    result = db.dbapi_interaction_finish(record)
    return jsonify( result )
#############################################################################
@app.route('/openbanking/api/v1/pointofsales/<pointofsale_id>/interactions/messages', methods = ['PUT','POST'])
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
        reply={'status':'error','message':'json data Not provided'}
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
        reply={'status':'error','message':'json data Not provided'}
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
@app.route('/openbanking/api/v1/consumers', methods = ['GET'])
#@auth.login_required
def get_consumers_list():
    # filterString=f"all"
    dbreply = db.dbapi_consumer(dbsession, 'LIST', {}, filter_dict={}, caller_dict={}, call_level=-1, debug_level=-1)
    return jsonify( dbreply )
#############################################################################
@app.route('/openbanking/api/v1/consumers', methods = ['PUT','POST'])
#@auth.login_required
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
@app.route('/openbanking/api/v1/consumers/<consumer_id>', methods = ['GET'])
#@auth.login_required
def get_consumer(consumer_id):
    dbreply=db.dbapi_consumer(dbsession, 'get', {'consumer_id':consumer_id}, filter_dict={}, caller_dict={}, call_level=-1,debug_level=-1)
    return jsonify( dbreply )
#############################################################################
@app.route('/openbanking/api/v1/consumers/<consumer_id>', methods = ['PUT','POST','PATCH'])
#@auth.login_required
def update_consumer(consumer_id):
    if not request.json:
        reply={'status':'error','message':'json data Not provided'}
        return make_response(jsonify(reply), 400)
    update_record = request.json
    update_record.update({'consumer_id':consumer_id})
    dbreply=db.dbapi_consumer(dbsession, 'update', update_record, filter_dict={}, caller_dict={}, call_level=-1,debug_level=-1)
    return jsonify( dbreply )
#############################################################################
@app.route('/openbanking/api/v1/consumers/<consumer_id>/confirm', methods = ['PUT','POST','PATCH'])
#@auth.login_required
def confirm_consumer(consumer_id):
    update_record = request.json
    update_record.update({'consumer_id':consumer_id})
    dbreply=db.dbapi_consumer(dbsession, 'confirm', update_record, filter_dict={}, caller_dict={}, call_level=-1,debug_level=-1)
    return jsonify( dbreply )
#############################################################################
@app.route('/openbanking/api/v1/consumers/<consumer_id>/unregister', methods = ['PUT','POST','PATCH'])
#@auth.login_required
def unregister_consumer(consumer_id):
    update_record = request.json
    update_record.update({'consumer_id':consumer_id})
    dbreply=db.dbapi_consumer(dbsession, 'UnRegister', update_record, filter_dict={}, caller_dict={}, call_level=-1,debug_level=-1)
    return jsonify(dbreply)
#############################################################################
@app.route('/openbanking/api/v1/consumers/<consumer_id>', methods = ['DELETE'])
#@auth.login_required
def delete_consumer(consumer_id):
    dbreply=db.dbapi_consumer(dbsession, 'delete', {'consumer_id':consumer_id}, filter_dict={}, caller_dict={}, call_level=-1,debug_level=-1)
    return jsonify(dbreply)
#############################################################################
@app.route('/openbanking/api/v1/consumers/<consumer_id>/banksubscription', methods = ['PUT','POST','PATCH'])
#@auth.login_required
def consumer_banksubscription_register(consumer_id):
    if not request.json:
        reply={'status':'error','message':'json data Not provided'}
        return make_response(jsonify(reply), 400)
    update_record = request.json
    update_record.update({'consumer_id':consumer_id})
    dbreply = db.dbapi_consumer_banksubscription_register(update_record)
    return jsonify(dbreply)
#############################################################################
@app.route('/openbanking/api/v1/consumers/<consumer_id>/interaction/start', methods = ['PUT','POST'])
def start_consumer_interactions(consumer_id):
    record={'consumer_id':consumer_id}
    result = db.dbapi_interaction_start(record)
    return jsonify( result )
##########################################################################################################################
#############################################################################
@app.route('/openbanking/api/v1/consumers/<consumer_id>/interactions/finish', methods = ['PUT','POST'])
def finish_consumer_interactions(consumer_id):
    record={'consumer_id':consumer_id}
    result = db.dbapi_interaction_finish(record)
    return jsonify( result )
##########################################################################################################################
#############################################################################
#############################################################################
@app.route('/openbanking/api/v1/consumers/<consumer_id>/interactions/messages', methods = ['PUT','POST'])
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
@app.route('/openbanking/api/v1/banks', methods = ['GET'])
def get_banks_list():
    dbreply = db.dbapi_bank(dbsession, 'LIST', {}, filter_dict={}, caller_dict={}, call_level=-1, debug_level=-1)
    return jsonify( dbreply )
# #############################################################################
# @app.route('/openbanking/api/v1/banks', methods = ['PUT','POST'])
# def new_bank():
#     if not request.json:
#         reply={'status':'error','message':'json data Not provided'}
#         return make_response(jsonify(reply), 400)
#     record_data = request.json
#     if not record_data.get('bank_name'):
#         reply={'status':'error','message':'[name] Not provided'}
#         return make_response(jsonify(reply), 401)
#     if not record_data.get('bank_code'):
#         reply={'status':'error','message':'[bank_code] Not provided'}
#         return make_response(jsonify(reply), 401)
#     if not record_data.get('bank_BIC'):
#         reply={'status':'error','message':'[bank_BIC] Not provided'}
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
#         reply={'status':'error','message':'json data Not provided'}
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
#         reply={'status':'error','message':'json data Not provided'}
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
@app.route('/openbanking/api/v1/banks', methods = ['PUT','POST'])
#@auth.login_required
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
@app.route('/openbanking/api/v1/banks/<bank_id>', methods = ['GET'])
#@auth.login_required
def get_bank(bank_id):
    dbreply=db.dbapi_bank(dbsession, 'get', {'bank_id':bank_id}, filter_dict={}, caller_dict={}, call_level=-1,debug_level=-1)
    return jsonify( dbreply )
#############################################################################
@app.route('/openbanking/api/v1/banks/<bank_id>', methods = ['PUT','POST','PATCH'])
#@auth.login_required
def update_bank(bank_id):
    if not request.json:
        reply={'status':'error','message':'json data Not provided'}
        return make_response(jsonify(reply), 400)
    update_record = request.json
    update_record.update({'bank_id':bank_id})
    dbreply=db.dbapi_bank(dbsession, 'update', update_record, filter_dict={}, caller_dict={}, call_level=-1,debug_level=-1)
    return jsonify( dbreply )
#############################################################################
@app.route('/openbanking/api/v1/banks/<bank_id>/activate', methods = ['PUT','POST','PATCH'])
#@auth.login_required
def confirm_bank(bank_id):
    update_record = request.json
    update_record.update({'bank_id':bank_id})
    dbreply=db.dbapi_bank(dbsession, 'activate', update_record, filter_dict={}, caller_dict={}, call_level=-1,debug_level=-1)
    return jsonify( dbreply )
#############################################################################
@app.route('/openbanking/api/v1/banks/<bank_id>/deactivate', methods = ['PUT','POST','PATCH'])
#@auth.login_required
def unregister_bank(bank_id):
    update_record = request.json
    update_record.update({'bank_id':bank_id})
    dbreply=db.dbapi_bank(dbsession, 'deactivate', update_record, filter_dict={}, caller_dict={}, call_level=-1,debug_level=-1)
    return jsonify(dbreply)
#############################################################################
@app.route('/openbanking/api/v1/banks/<bank_id>', methods = ['DELETE'])
#@auth.login_required
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
    dbsession = db.get_dbsession(debug=99)
    dbsession.close()

    #db.database_schema.connect()
    #app.run(debug=False)
    # app.run(host='0.0.0.0', port=5555)
    #app.run(host='127.0.0.1', port=5555)
    #app.run(debug=False,port=5555,threaded=True)
    app.run(debug=False,port=5555,threaded=False)
