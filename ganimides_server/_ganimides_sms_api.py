#@@@@# -*- coding: utf-8 -*-

import os
import sys
if not (os.path.dirname(os.path.dirname(__file__)) in sys.path): sys.path.append(os.path.dirname(os.path.dirname(__file__)))
if not (os.path.dirname(__file__) in sys.path): sys.path.append(os.path.dirname(__file__))

import datetime
import decimal
import phonenumbers

# #
from _onlineApp import thisApp
from _onlineApp import get_debug_option_as_level, get_debug_files, log_message, retrieve_module_configuration, get_globals_from_configuration, save_module_configuration,get_module_debug_level
from _onlineApp import log_process_start, log_process_finish, log_process_message, log_process_result,log_process_data, log_process_input, log_process_output
from _onlineApp import set_process_identity_dict, set_process_caller_area, add_apis_to_configuration
from _onlineApp import build_process_signature, build_process_call_area, get_debug_level, get_debug_files
from _onlineApp import utilities,send_sms,generate_confirmation_token,generate_sms_friendly_confirmation_token,generate_otp

import ganimides_database as db
#import ganimides_openBankingAPI as bankingapi
#::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
#::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
#::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
#::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
#::: module                                                                                                 :::
#::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
#::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
#::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
module_Function = 'database adapter'
module_ProgramName = 'database api'
module_BaseTimeStamp = datetime.datetime.now()
module_folder = os.getcwd()
module_color = thisApp.Fore.LIGHTMAGENTA_EX
module_folder = os.path.dirname(__file__)
module_ProgramName = os.path.splitext(os.path.basename(__file__))[0]
module_id = f'{module_ProgramName}'
module_eyecatch = module_ProgramName
module_version = 0.1
module_log_file_name = module_ProgramName+'.log'
module_errors_file_name = os.path.splitext(os.path.basename(module_log_file_name))[0]+'_errors.log'
module_versionString = f'{module_id} version {module_version}'
module_file = __file__

log_file=thisApp.log_file_name
print_enabled = thisApp.CONSOLE_ON
consolelog_enabled = thisApp.CONSOLE_ON
filelog_enabled = thisApp.FILELOG_ON

module_is_externally_configurable = False
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
    'module_errors_file_name': module_errors_file_name,
    'consolelog_enabled': consolelog_enabled,
    'filelog_enabled': filelog_enabled,
    'module_is_externally_configurable':module_is_externally_configurable,
    }
#::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
#::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
#::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
# configuration
#::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
#::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
#::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
master_configuration = {
    }
#::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
#::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
#::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
#::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
#::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
# api services : database apis
#::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
#::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
#::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
#::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
def smsapi_send_mobile_confirmation_sms(dbsession, client_id, application_name, confirmation_url, caller_area={}):
    _api_name = "smsapi_send_mobile_confirmation_sms"
    _api_entity = 'sms'
    _api_action = 'send_sms'
    _api_msgID = set_msgID(_api_name, _api_action, _api_entity)

    _process_identity_kwargs = {'type': 'api', 'module': module_id, 'name': _api_name, 'action': _api_action, 'entity': _api_entity, 'msgID': _api_msgID,}
    _process_adapters_kwargs = {'dbsession': dbsession}
    _process_log_kwargs = {'indent_method': 'AUTO', 'indent_level':None}
    _process_debug_level = get_debug_level(caller_area.get('debug_level'), **_process_identity_kwargs, **_process_adapters_kwargs)
    _process_debug_files = get_debug_files(_process_debug_level, **_process_identity_kwargs, **_process_adapters_kwargs)
    _process_debug_kwargs={'debug_level':_process_debug_level,'debug_files':_process_debug_files}

    _process_signature = build_process_signature(**_process_identity_kwargs, **_process_adapters_kwargs, **_process_debug_kwargs, **_process_log_kwargs)
    _process_call_area = build_process_call_area(_process_signature, caller_area)
    
    #_process_call_area.update({'debug_level': 99})
    
    log_process_start(_api_msgID,**_process_call_area)

    log_process_input('', 'client_id', client_id,**_process_call_area)
    log_process_input('', 'application_name', application_name,**_process_call_area)
    log_process_input('', 'confirmation_url', confirmation_url,**_process_call_area)
    log_process_input('', 'caller_area', caller_area,**_process_call_area)

    client = dbsession.get(db.CLIENT, {'client_id':client_id}, caller_area=_process_call_area)
    if not client:
        msg = f'client not found'
        reply = {'api_status': 'error', 'api_message': msg}
        return reply
    if not client.mobile:
        msg = f'no client mobile'
        reply = {'api_status': 'error', 'api_message': msg}
        return reply

    if client.mobile_confirmed:
        msg = f'mobile already confirmed'
        reply = {'api_status': 'error', 'api_message': msg}
        return reply

    phone_number = get_validated_phone_number(client.mobile)
    if not phone_number.get('api_status') == 'success':
        msg=phone_number.get('api_message','?')
        msg = f'invalid mobile number {client.mobile}. ({msg})'
        api_result = {'api_status': 'error', 'api_message': msg}
        log_process_finish('', api_result, **_process_call_area)    
        return api_result

    token_number = phone_number.get('international_number').replace('+', '')
    token = generate_sms_friendly_confirmation_token(token_number)
    if not token:
        msg = f'token generation failed'
        reply = {'api_status': 'error', 'api_message': msg}
        return reply

    otp = generate_otp()
    if not otp:
        msg = f'otp generation failed'
        reply = {'api_status': 'error', 'api_message': msg}
        return reply
    
    if not confirmation_url:
        msg = f'confirmation_url not provided'
        reply = {'api_status': 'error', 'api_message': msg}
        return reply

    client_record = client.to_dict()
    if len(client.mobile.strip()) < 11:
        client.mobile = '+357' + client.mobile.strip()
        
    confirmation_url = confirmation_url.replace('-token-', token)
    log_process_data('', 'confirmation_url', confirmation_url, **_process_call_area)

    if not confirmation_url:
        msg = f'confirmation_url Failed. system error'
        reply = {'api_status': 'error', 'api_message': msg}
        return reply
    
    client_record.update({'confirmation_url':confirmation_url})
    client_record.update({'otp':otp})

    client_language = client.language
    if not client_language:
        client_language='En'

    sms_template = 'mobile_confirmation_sms'
    language=client_language
    template = dbsession.get(db.APPLICATION_TEMPLATE, {'template_name':sms_template,'application_name':application_name,'language':language}, caller_area=_process_call_area)
    if not template:
        msg = f'template [{sms_template}] not found for application [{application_name}] language [{language}]'
        log_process_message(_api_msgID, 'waring', msg, **_process_call_area)
        
        language='En'
        template = dbsession.get(db.APPLICATION_TEMPLATE, {'template_name':sms_template,'application_name':application_name,'language':language}, caller_area=_process_call_area)
        if not template:
            msg = f'template [{sms_template}] not found for application [{application_name}] language [{language}]'
            log_process_message(_api_msgID, 'waring', msg, **_process_call_area)
            language = client_language
            template = dbsession.get(db.APPLICATION_TEMPLATE, {'template_name':sms_template,'application_name':'','language':language}, caller_area=_process_call_area)
            if not template:
                msg = f'generic template [{sms_template}] not found for client_language {language}'
                log_process_message(_api_msgID, 'error', msg, **_process_call_area)

                language = 'En'
                template = dbsession.get(db.APPLICATION_TEMPLATE, {'template_name':sms_template,'application_name':'','language':language}, caller_area=_process_call_area)
                if not template:
                    msg = f'generic template [{sms_template}] not found for language {language}'
                    log_process_message(_api_msgID, 'error', msg, **_process_call_area)   
                    sms_message = f'the code to confirm your mobile is {otp} click #CONFIRMATION_URL#'

    if template:
        sms_message = template.text

    log_process_data('', 'sms message', sms_message, **_process_call_area)

    if sms_message.find('#')>=0:
        sms_message = utilities.string_translate(sms_message, client_record)
        log_process_data('', 'sms message translated', sms_message, **_process_call_area)
        
    From = thisApp.application_configuration.get('sms_sender')
    log_process_data('', 'From', From, **_process_call_area)
    if not(From):
        From = application_name
        msg = f'From set to application_name [{From}]'
        log_process_message(_api_msgID, 'warning', msg, **_process_call_area)
    # if not(From):
    #     From = 'ganimidesT'
    #     msg = f'From set to [{From}]'
    #     log_process_message(_api_msgID, 'warning', msg, **_process_call_area)
    if not(From):
        msg = f'sms sender not defined'
        api_result = {'api_status': 'error', 'api_message': msg}
        log_process_finish(_api_msgID, api_result, **_process_call_area)    
        return api_result

    _process_call_area.update({'sms_simulation': True})
    
    sms_result = send_sms_service(dbsession, From=From, To=client.mobile, Message=sms_message, caller_area=_process_call_area)
    #provider_reply = {'provider_reply': reply, 'reply_code': status_code, 'reply_message': reply_message, 'provider': 'SINCH', 'provider_send_id': sms_uid}
    if sms_result.get('api_status')=='success':
        verification_record = {
            'verification_token': token,
            'verification_code': otp,
            'verification_entity': 'mobile',
            'client_id': client.client_id,
            'application_name': application_name,
            'mobile': client.mobile,
            'status': 'SmsSent',
            'send_method': 'sms',
            'send_provider': sms_result.get('api_data',{}).get('provider'),
            'send_ticket': sms_result.get('api_data',{}).get('provider_send_id'),
            'send_timestamp': datetime.datetime.utcnow(),
            'expiry_timestamp': datetime.datetime.utcnow()+ datetime.timedelta(seconds=3600),
        }
        verification = dbsession.insert(db.VERIFICATION, verification_record, auto_commit=True, caller_area=_process_call_area)
        if not verification:
            msg = f'system error: verification record create failed'
            log_process_message('', 'error', msg,**_process_call_area)

    api_result = sms_result
    api_result.update({'api_action': _api_action, 'api_name': _api_name})
    
    log_process_finish(_api_msgID, api_result, **_process_call_area)    
    return api_result
#::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
#::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
def send_sms_service(dbsession, From='', To='', Cc='', Bcc='', Message='', language='En', sms_template='', data_record={}, application_name='', caller_area={}):
    _api_name = "send_sms_service"
    _api_entity = 'sms'
    _api_action = 'send_sms'
    _api_msgID = set_msgID(_api_name, _api_action, _api_entity)

    _process_identity_kwargs = {'type': 'api', 'module': module_id, 'name': _api_name, 'action': _api_action, 'entity': _api_entity, 'msgID': _api_msgID,}
    _process_adapters_kwargs = {'dbsession': dbsession}
    _process_log_kwargs = {'indent_method': 'AUTO', 'indent_level':None}
    _process_debug_level = get_debug_level(caller_area.get('debug_level'), **_process_identity_kwargs, **_process_adapters_kwargs)
    _process_debug_files = get_debug_files(_process_debug_level, **_process_identity_kwargs, **_process_adapters_kwargs)
    _process_debug_kwargs={'debug_level':_process_debug_level,'debug_files':_process_debug_files}

    _process_signature = build_process_signature(**_process_identity_kwargs, **_process_adapters_kwargs, **_process_debug_kwargs, **_process_log_kwargs)
    _process_call_area = build_process_call_area(_process_signature, caller_area)

    log_process_start(_api_msgID,**_process_call_area)

    log_process_input('', 'From', From,**_process_call_area)
    log_process_input('', 'To', To,**_process_call_area)
    log_process_input('', 'Cc', Cc,**_process_call_area)
    log_process_input('', 'Bcc', Bcc,**_process_call_area)
    log_process_input('', 'Message', Message, **_process_call_area)
    log_process_input('', 'language', language, **_process_call_area)
    log_process_input('', 'sms_template', sms_template, **_process_call_area)
    log_process_input('', 'application_name', application_name, **_process_call_area)
    log_process_input('', 'caller_area', caller_area, **_process_call_area)

    sms_record = {
            'sender': From,
            'recipient': To,
            'cc': Cc,
            'bcc': Bcc,
            'message': Message,
            'language': language,
            'data_record': str(data_record),
            'application_name': application_name,
        }
    sms = dbsession.insert(db.SMS, sms_record, auto_commit=True, caller_area=_process_call_area)

    sms_result = send_sms(From=From, To=To, Message=Message, language=language, sms_template=sms_template, data_record=data_record, application_name=application_name, caller_area=caller_area)
    #provider_reply = {'provider_reply': reply, 'reply_code': status_code, 'reply_message': reply_message, 'provider': 'SINCH', 'provider_send_id': sms_uid}
    sms_record = {
            'sms_id':sms.sms_id,
            'sender': From,
            'recipient': To,
            'cc': Cc,
            'bcc': Bcc,
            'message': Message,
            'language': language,
            'data_record': str(data_record),
            'application_name': application_name,
            'sms_template': sms_template,
            'application_name': application_name,
            'send_provider': sms_result.get('api_data',{}).get('provider'),
            'send_ticket': sms_result.get('api_data',{}).get('provider_send_id'),
            'provider_reply': sms_result.get('api_data',{}).get('provider_reply'),
            'reply_code': sms_result.get('api_data',{}).get('reply_code'),
            'reply_message': sms_result.get('api_data',{}).get('reply_message'),
            'send_timestamp': datetime.datetime.utcnow(),
        }
    dbsession.refresh(db.SMS, sms_record, auto_commit=True, caller_area=_process_call_area)
    
    api_result = sms_result
    log_process_finish(_api_msgID, api_result, **_process_call_area)    
    return api_result
#::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
def set_msgID(api_name,api_action,api_entity):
    msgid=f"#C0#api #C9#{api_name}#C0# [{api_entity}]#C0# action [[{api_action.upper()}]]#C0#"
    return msgid
#::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
def get_validated_phone_number(number):
    if not (number):
        return({'api_status':'error','api_message':'empty'})

    number = number.strip()
    while number[0] == '0' and len(number)>1:
        number = number[1:]
    while number[0] == '+' and len(number)>1:
        number = number[1:]    
    if len(number) < 11:
        return({'api_status':'error','api_message':'length error. not an international phone number'})

    number = '+' + number

    try:
        phone_number = phonenumbers.parse(number)
    except:
        phone_number = None

    if not phone_number:
        return({'api_status':'error','api_message':'phone number validation failed'})

    inumber = '+' + str(phone_number.country_code) + str(phone_number.national_number)
    return {'api_status': 'success', 'api_message': 'OK', 'country_code': str(phone_number.country_code), 'national_number': str(phone_number.national_number), 'international_number': inumber}
#:::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::

#::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
#::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
# module initialization
#::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
#::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
#::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
master_configuration = retrieve_module_configuration(module_identityDictionary, master_configuration, print_enabled=consolelog_enabled, filelog_enabled=filelog_enabled, handle_as_init=False)
#::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
functions_ids=['ALL']
exclude_functions_ids = ['set_msgID']
thisModuleObj = sys.modules[__name__]
master_configuration.update({'sms_apis':[]})
master_configuration = add_apis_to_configuration('sms_apis', master_configuration, thisModuleObj, functions_ids, exclude_functions_ids)
save_module_configuration(module_identityDictionary, master_configuration, print_enabled=consolelog_enabled, filelog_enabled=filelog_enabled)
thisApp.pair_module_configuration('sms_apis',master_configuration)
#::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
save_module_configuration(module_identityDictionary, master_configuration, print_enabled=consolelog_enabled, filelog_enabled=filelog_enabled)
#::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
if get_module_debug_level(module_id) > 0:
    apis = thisApp.application_configuration.get('sms_apis', {})
    for api_name in apis.keys():
        api_entry = apis.get(api_name)
        msg=f'module [[{module_id}]] sms api [{api_name} [[[{api_entry}]]]'
        log_message(msg)
#::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
#import commands
apis = thisApp.application_configuration.get('sms_apis', {})
for api_name in apis.keys():
    api_entry = apis.get(api_name)
    msg=f'from {module_id} import {api_name}'
    log_message(msg)
#::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
#::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
msg = f'module [{module_id}] [[version {module_version}]] loaded.'
log_message(msg)
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
    # caller_area={'aaaa': '11111'}
    # print('0caller_area=', caller_area)
    # test_api(caller_area, call_level=-1)
    # print('4caller_area=', caller_area)
    # sms_message='hi. confirm http://127.0.0.1:5555/confirmation/71CD00E6C50F/mobile'
    # sms_message='hi. confirm 127.0.0.5555confirmation71CD00E6C50Fmobile'
    # sms_result = send_sms(From='', To=client.mobile, Message=sms_message, data_record=client_record, caller_area=_process_call_area)
    # print(smsapi_send_mobile_confirmation_sms(dbsession, client_id, application_name, confirmation_url, caller_area={}))

    _process_call_area={'debug_level':99}
    dbsession = db.get_dbsession(**_process_call_area)
    application_name = 'scanandpay'
    # template = {'application_name': application_name, 'template_name': 'mobile_confirmation_sms', 'language': 'En',
    # 'text':'your otp to confirm your mobile is #OTP#. click #CONFIRMATION_URL#'}
    # db.dbapi_application_template(dbsession,'refresh',template,caller_area=_process_call_area)

    # template = {'application_name': application_name, 'template_name': 'mobile_confirmation_sms', 'language': 'Gr',
    # 'text':'ο κωδικός για επιβεβεβαιωση του κινητου σας ειναι: #OTP#. πατηστε #CONFIRMATION_URL#'}
    # db.dbapi_application_template(dbsession,'refresh',template,caller_area=_process_call_area)

    # template = {'application_name': '', 'template_name': 'mobile_confirmation_sms', 'language': 'En',
    # 'text':'your otp to confirm your mobile is #OTP#. click #CONFIRMATION_URL#'}
    # db.dbapi_application_template(dbsession,'refresh',template,caller_area=_process_call_area)

    # template = {'application_name': '', 'template_name': 'mobile_confirmation_sms', 'language': 'Gr',
    # 'text':'ο κωδικός για επιβεβεβαιωση του κινητου σας ειναι: #OTP#. πατηστε #CONFIRMATION_URL#'}
    # db.dbapi_application_template(dbsession,'refresh',template,caller_area=_process_call_area)

    client_id = dbsession.get(db.CLIENT, {'email': 'schroedinger@gmail.com'}).client_id
    print('client_id:',client_id)
    confirmation_url = 'http://127.0.0.1:5555/confirmation/-token-/mobile'
    print(smsapi_send_mobile_confirmation_sms(dbsession, client_id, application_name, confirmation_url, caller_area=_process_call_area))
#::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
#::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
#::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::