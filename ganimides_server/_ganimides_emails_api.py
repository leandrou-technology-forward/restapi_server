import os
import sys
if not (os.path.dirname(os.path.dirname(__file__)) in sys.path): sys.path.append(os.path.dirname(os.path.dirname(__file__)))
if not (os.path.dirname(__file__) in sys.path): sys.path.append(os.path.dirname(__file__))

import datetime
import decimal

# #
from _onlineApp import thisApp
from _onlineApp import get_debug_option_as_level, get_debug_files, log_message, retrieve_module_configuration, get_globals_from_configuration, save_module_configuration,get_module_debug_level
from _onlineApp import log_process_start, log_process_finish, log_process_message, log_process_result,log_process_data, log_process_input, log_process_output
from _onlineApp import set_process_identity_dict, set_process_caller_area, add_apis_to_configuration
from _onlineApp import build_process_signature, build_process_call_area, get_debug_level, get_debug_files
from _onlineApp import utilities, send_email, generate_confirmation_token, generate_otp

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
def emailapi_send_email_confirmation_email(dbsession, client_id, application_name, confirmation_url, caller_area={}):
    _api_name = "emailapi_send_email_confirmation_email"
    _api_entity = 'email'
    _api_action = 'send_email'
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

    log_process_input('', 'client_id', client_id,**_process_call_area)
    log_process_input('', 'application_name', application_name,**_process_call_area)
    log_process_input('', 'confirmation_url', confirmation_url,**_process_call_area)
    log_process_input('', 'caller_area', caller_area,**_process_call_area)

    client = dbsession.get(db.CLIENT, {'client_id':client_id}, caller_area=_process_call_area)
    if not client:
        msg = f'client not found'
        reply = {'api_status': 'error', 'api_message': msg}
        return reply
    if not client.email:
        msg = f'no client email'
        reply = {'api_status': 'error', 'api_message': msg}
        return reply

    if client.email_confirmed:
        msg = f'email already confirmed'
        reply = {'api_status': 'error', 'api_message': msg}
        return reply

    client_id = client.client_id
    client_record = client.to_dict()

    token = generate_confirmation_token(client.email)
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

    email_template='email_confirmation_email'
    language=client_language
    template = dbsession.get(db.APPLICATION_TEMPLATE, {'template_name':email_template,'application_name':application_name,'language':language}, caller_area=_process_call_area)
    if not template:
        msg = f'template [{email_template}] not found for application [{application_name}] language [{language}]'
        log_process_message(_api_msgID, 'waring', msg, **_process_call_area)
        
        language='En'
        template = dbsession.get(db.APPLICATION_TEMPLATE, {'template_name':email_template,'application_name':application_name,'language':language}, caller_area=_process_call_area)
        if not template:
            msg = f'template [{email_template}] not found for application [{application_name}] language [{language}]'
            log_process_message(_api_msgID, 'waring', msg, **_process_call_area)
            language = client_language
            template = dbsession.get(db.APPLICATION_TEMPLATE, {'template_name':email_template,'application_name':'','language':language}, caller_area=_process_call_area)
            if not template:
                msg = f'generic template [{email_template}] not found for client_language {language}'
                log_process_message(_api_msgID, 'error', msg, **_process_call_area)

                language = 'En'
                template = dbsession.get(db.APPLICATION_TEMPLATE, {'template_name':email_template,'application_name':'','language':language}, caller_area=_process_call_area)
                if not template:
                    msg = f'generic template [{email_template}] not found for language {language}'
                    log_process_message(_api_msgID, 'error', msg, **_process_call_area)   
                    email_subject = f'email confirmation'
                    email_content_text = f'please confirm your email by clicking the link below'+'\n'+f'{confirmation_url} and entering the code {otp}'
                    email_content_html = ''

    if template:
        email_subject = template.subject
        email_content_text = template.text
        email_content_html = template.html

    log_process_data('', 'email_subject', email_subject, **_process_call_area)
    log_process_data('', 'email_content_text', email_content_text, **_process_call_area)
    log_process_data('', 'email_content_html', email_content_html, **_process_call_area)

    if email_subject.find('#')>=0:
        email_subject = utilities.string_translate(email_subject, client_record)
        log_process_data('', 'email_subject translated', email_subject, **_process_call_area)
    if email_content_text.find('#')>=0:
        email_content_text = utilities.string_translate(email_content_text, client_record)
        log_process_data('', 'email_content_text translated', email_content_text, **_process_call_area)
    if email_content_html.find('#')>=0:
        email_content_html = utilities.string_translate(email_subject, client_record)
        log_process_data('', 'email_content_html translated', email_content_html, **_process_call_area)

    From = thisApp.application_configuration.get('email_sender')
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
        msg = f'email sender not defined'
        api_result = {'api_status': 'error', 'api_message': msg}
        log_process_finish(_api_msgID, api_result, **_process_call_area)    
        return api_result

    email_result = send_email_service(dbsession, From=From, To=client.email, Subject=email_subject, text_body=email_content_text, html_body=email_content_html, language=language, caller_area=_process_call_area)
    

    #provider_reply = {'provider_reply': reply, 'reply_code': status_code, 'reply_message': reply_message, 'provider': 'SINCH', 'provider_send_id': sms_uid}
    
    if email_result.get('api_status')=='success':
        verification_record = {
            'verification_token': token,
            'verification_code': otp,
            'verification_entity': 'email',
            'client_id': client.client_id,
            'application_name': application_name,
            'email': client.email,
            'status': 'EmailSent',
            'send_method': 'email',
            'send_provider': email_result.get('api_data',{}).get('provider'),
            'send_ticket': email_result.get('api_data',{}).get('provider_send_id'),
            'send_timestamp': datetime.datetime.utcnow(),
            'expiry_timestamp': datetime.datetime.utcnow()+ datetime.timedelta(seconds=3600),
        }

        verification = dbsession.insert(db.VERIFICATION, verification_record, auto_commit=True, caller_area=_process_call_area)
        if not verification:
            msg = f'system error: verification record create failed'
            log_process_message('', 'error', msg,**_process_call_area)

    api_result = email_result
    api_result.update({'api_action': _api_action, 'api_name': _api_name})
    
    log_process_finish(_api_msgID, api_result, **_process_call_area)    
    return api_result
#::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
def send_email_service(dbsession, From='', To='', Cc='', Bcc='', Subject='', text_body='', html_body='', email_template='', data_record={}, attachments=[], application_name='', language='En', caller_area={}):
    
    _api_name = "send_email_service"
    _api_entity = 'email'
    _api_action = 'send_email'
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
    log_process_input('', 'Subject', Subject, **_process_call_area)
    log_process_input('', 'text_body', text_body, **_process_call_area)
    log_process_input('', 'html_body', html_body, **_process_call_area)
    log_process_input('', 'email_template', email_template, **_process_call_area)
    log_process_input('', 'application_name', application_name, **_process_call_area)
    log_process_input('', 'language', language, **_process_call_area)
    log_process_input('', 'attachments', attachments, **_process_call_area)
    log_process_input('', 'caller_area', caller_area, **_process_call_area)

    email_record = {
            'sender': From,
            'recipient': To,
            'cc': Cc,
            'bcc': Bcc,
            'language':language,
            'subject': Subject,
            'text_body': text_body,
            'html_body': html_body,
            'email_template': email_template,
            'data_record': str(data_record),
            'attachments': str(attachments),
            'application_name': application_name,
        }
    email = dbsession.insert(db.EMAIL, email_record, auto_commit=True, caller_area=_process_call_area)

    email_result = send_email(From=From, To=To, Subject=Subject, text_body=text_body, html_body=html_body, caller_area=caller_area)
    #provider_reply = {'provider_reply': reply, 'reply_code': status_code, 'reply_message': reply_message, 'provider': 'SINCH', 'provider_send_id': sms_uid}
    email_record = {
            'email_id':email.email_id,
            'sender': From,
            'recipient': To,
            'cc': Cc,
            'bcc': Bcc,
            'language':language,
            'subject': Subject,
            'text_body': text_body,
            'html_body': html_body,
            'email_template': email_template,
            # 'data_record': data_record,
            # 'attachments': attachments,
            'application_name': application_name,
            'send_provider': email_result.get('api_data',{}).get('provider'),
            'send_ticket': email_result.get('api_data',{}).get('provider_send_id'),
            'provider_reply': email_result.get('api_data',{}).get('provider_reply'),
            'reply_code': email_result.get('api_data',{}).get('reply_code'),
            'reply_message': email_result.get('api_data',{}).get('reply_message'),
            'send_timestamp': datetime.datetime.utcnow(),
        }
    dbsession.refresh(db.EMAIL, email_record, auto_commit=True, caller_area=_process_call_area)
    
    api_result = email_result
    log_process_finish(_api_msgID, api_result, **_process_call_area)    
    return api_result
#::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::

#::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
#::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
def set_msgID(api_name,api_action,api_entity):
    msgid=f"#C0#api #C9#{api_name}#C0# [{api_entity}]#C0# action [[{api_action.upper()}]]#C0#"
    return msgid
#::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
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
master_configuration.update({'email_apis':[]})
master_configuration = add_apis_to_configuration('email_apis', master_configuration, thisModuleObj, functions_ids, exclude_functions_ids)
save_module_configuration(module_identityDictionary, master_configuration, print_enabled=consolelog_enabled, filelog_enabled=filelog_enabled)
thisApp.pair_module_configuration('email_apis',master_configuration)
#::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
save_module_configuration(module_identityDictionary, master_configuration, print_enabled=consolelog_enabled, filelog_enabled=filelog_enabled)
#::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
if get_module_debug_level(module_id) > 0:
    apis = thisApp.application_configuration.get('email_apis', {})
    for api_name in apis.keys():
        api_entry = apis.get(api_name)
        msg=f'module [[{module_id}]] email api [{api_name} [[[{api_entry}]]]'
        log_message(msg)
#::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
#import commands
apis = thisApp.application_configuration.get('email_apis', {})
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
    _process_call_area={'debug_level':99}
    dbsession = db.get_dbsession(**_process_call_area)
    application_name = 'scanandpay'

    template = {'application_name': application_name, 'template_name': 'email_confirmation_email', 'language': 'En',
    'subject':'email confirmation','text': 'confirm your email. click #CONFIRMATION_URL#','html':''
    }
    db.dbapi_application_template(dbsession,'refresh',template,caller_area=_process_call_area)

    template = {'application_name': application_name, 'template_name': 'email_confirmation_email', 'language': 'Gr',
    'subject':'επιβεβεβαιωση email','text': 'επιβεβεβαιωστε το email σας. click #CONFIRMATION_URL#','html':''}
    db.dbapi_application_template(dbsession,'refresh',template,caller_area=_process_call_area)

    template = {'application_name': '', 'template_name': 'email_confirmation_email', 'language': 'En',
    'subject':'email confirmation','text': 'confirm your email. click #CONFIRMATION_URL#','html':''}
    db.dbapi_application_template(dbsession,'refresh',template,caller_area=_process_call_area)

    template = {'application_name': '', 'template_name': 'email_confirmation_email', 'language': 'Gr',
    'subject':'επιβεβεβαιωση email','text': 'επιβεβεβαιωστε το email σας. click #CONFIRMATION_URL#','html':''}
    db.dbapi_application_template(dbsession,'refresh',template,caller_area=_process_call_area)

    client_id = dbsession.get(db.CLIENT, {'email': 'schroedinger@gmail.com'}).client_id
    print('client_id:',client_id)
    confirmation_url = 'http://127.0.0.1:5555/confirmation/-token-/email'
    print(emailapi_send_email_confirmation_email(dbsession, client_id, application_name, confirmation_url, caller_area=_process_call_area))
#::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
#::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
#::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::