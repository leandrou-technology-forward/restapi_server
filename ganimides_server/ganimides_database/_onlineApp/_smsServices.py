#@@@ # -*- coding: utf-8 -*-
#https://www.cyta.com.cy/web-sms-api/en
#https://www.cyta.com.cy/id/c20?ReturnUrl=%2fweb-sms-api%2fen

#https://dashboard.nexmo.com/edit-profile
#ganimedesifestionas@outlook.com philea13
import os
import sys
if not (os.path.dirname(__file__) in sys.path): sys.path.append(os.path.dirname(__file__))

import re 
import requests
import phonenumbers
import xml.etree.ElementTree as ET

import nexmo
from sinchsms import SinchSMS 
import time

# import smtplib


# from email.mime.multipart import MIMEMultipart
# from email.mime.text import MIMEText
# from mailjet_rest import Client

import _appEnvironment as thisApp
from _utilities import string_translate
from _processServices import set_process_identity_dict, set_process_caller_area,build_process_signature, build_process_call_area
from _debugServices import get_debug_option_as_level,get_debug_files,get_debug_level
from _logProcessServices import log_process_start, log_process_finish, log_process_message, log_process_result,log_process_data, log_process_input, log_process_data,log_process_parameter
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 
module_ProgramName = os.path.splitext(os.path.basename(__file__))[0]
module_id = '{}'.format(module_ProgramName)
module_version = 0.1
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 
# using SendGrid's Python Library
# https://github.com/sendgrid/sendgrid-python
#import sendgrid
#from sendgrid.helpers.mail import *
#:::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
#:::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
#:::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
def get_template(template,application_name='',language='En'): #under construction
    subject = ''
    text = ''
    html = ''
    return (subject,text,html)
#:::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
#:::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
#:::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
def send_sms(From='', To='', Cc='', Bcc='', Message='', language='En', sms_template='', data_record={}, application_name='', caller_area={}):
    """
    send_sms (wrapper)
    """
    _process_name = 'send_sms'
    _process_entity = 'sms'
    _process_action = 'send_sms'
    _process_msgID = f'process:[{_process_name}]'
    _process_identity_kwargs = {'type': 'process', 'module': module_id, 'name': _process_name, 'action': _process_action, 'entity': _process_entity, 'msgID': _process_msgID,}
    _process_adapters_kwargs = {'dbsession': None}
    _process_log_kwargs = {'indent_method': 'AUTO', 'indent_level': None}
    _process_debug_level = get_debug_level(caller_area.get('debug_level'), **_process_identity_kwargs, **_process_adapters_kwargs)
    _process_debug_files = get_debug_files(_process_debug_level, **_process_identity_kwargs, **_process_adapters_kwargs)
    _process_debug_kwargs={'debug_level':_process_debug_level,'debug_files':_process_debug_files}

    _process_signature = build_process_signature(**_process_identity_kwargs, **_process_adapters_kwargs, **_process_debug_kwargs, **_process_log_kwargs)
    _process_call_area = build_process_call_area(_process_signature, caller_area)

    log_process_start(_process_msgID,**_process_call_area)

    log_process_input('', 'From', From,**_process_call_area)
    log_process_input('', 'To', To,**_process_call_area)
    log_process_input('', 'Cc', Cc,**_process_call_area)
    log_process_input('', 'Bcc', Bcc,**_process_call_area)
    log_process_input('', 'Message', Message, **_process_call_area)
    log_process_input('', 'language', language, **_process_call_area)
    log_process_input('', 'sms_template', sms_template, **_process_call_area)
    log_process_input('', 'application_name', application_name, **_process_call_area)
    log_process_input('', 'caller_area', caller_area, **_process_call_area)

    if not From:
        From = thisApp.application_configuration.get('sms_sender')
        log_process_data('', 'From', From,**_process_call_area)
    if not From:
        From = application_name
        log_process_data('', 'From', From,**_process_call_area)
    if not(From):
        msg = f'sms sender not defined'
        api_result = {'api_status': 'error', 'api_message': msg}
        log_process_finish(_process_msgID, api_result, **_process_call_area)    
        return api_result

    if not(To):
        msg = f'sms recipient not defined'
        api_result = {'api_status': 'error', 'api_message': msg}
        log_process_finish(_process_msgID, api_result, **_process_call_area)    
        return api_result
    
    phone_number = get_validated_phone_number(To)

    if not phone_number.get('api_status') == 'success':
        msg=phone_number.get('api_message','?')
        msg = f'invalid recipient number {To}. ({msg})'
        api_result = {'api_status': 'error', 'api_message': msg}
        log_process_finish(_process_msgID, api_result, **_process_call_area)    
        return api_result

    To=phone_number.get('international_number')
    if not(To):
        msg = f'system error'
        api_result = {'api_status': 'error', 'api_message': msg}
        log_process_finish(_process_msgID, api_result, **_process_call_area)    
        return api_result

    if not(Message):
        msg = f'Message not defined'
        api_result = {'api_status': 'error', 'api_message': msg}
        log_process_finish(_process_msgID, api_result, **_process_call_area)    
        return api_result

    if not(Message) and not(sms_template):
        msg = f'no message or template defined'
        api_result = {'api_status': 'error', 'api_message': msg}
        log_process_message('', 'warning', msg,**_process_call_area)
    else:
        if sms_template:
            (t1, t2, t3) = get_template(sms_template,application_name,language)
            if t1 or t2 or t3:
                Message = t1
            else:
                msg = f'sms template {sms_template} not found'
                api_result = {'api_status': 'error', 'api_message': msg}
                log_process_finish(_process_msgID, api_result, **_process_call_area)    
                return api_result

    if Message.find('#')>=0:
        Message = string_translate(Message, data_record)
        log_process_data('', 'translated Message', Message,**_process_call_area)

    SMS_SERVER_PROVIDER = thisApp.application_configuration.get('SMS_SERVER_PROVIDER')
    log_process_parameter('', 'config param', 'SMS_SERVER_PROVIDER', SMS_SERVER_PROVIDER, **_process_call_area)
    if not SMS_SERVER_PROVIDER:
        SMS_SERVER_PROVIDER = 'CYTA'
        log_process_parameter('', 'default config param', 'SMS_SERVER_PROVIDER', SMS_SERVER_PROVIDER, **_process_call_area)

    country_code = phone_number.get('country_code')
    if country_code == '357':
        SMS_SERVER_PROVIDER = 'CYTA'
        log_process_parameter('', 'set config param', 'SMS_SERVER_PROVIDER', SMS_SERVER_PROVIDER, **_process_call_area)
        To = phone_number.get('national_number')
        log_process_data('', 'To national number', To,**_process_call_area)
    else:
        SMS_SERVER_PROVIDER = 'NEXMO'
        log_process_parameter('', 'set config param', 'SMS_SERVER_PROVIDER', SMS_SERVER_PROVIDER, **_process_call_area)
        To = phone_number.get('international_number')
        log_process_data('', 'To international number', To,**_process_call_area)

    try:
        if SMS_SERVER_PROVIDER.upper() == 'SINCH':
                send_result = sendSMS_through_SINCH(From, To, Cc, Bcc, Message, language, caller_area=_process_call_area)
        else:
            if SMS_SERVER_PROVIDER == 'NEXMO':
                send_result = sendSMS_through_NEXMO(From, To, Cc, Bcc, Message, language, caller_area=_process_call_area)
            else:
                send_result = sendSMS_through_CYTA(From, To, Cc, Bcc, Message, language, caller_area=_process_call_area)
    except Exception as error_text:
        msg= f'sms send failed. system error:{error_text}'
        log_process_message('', 'error', msg,**_process_call_area)
        provider_reply={'provider_reply':f'exception occurred executing provider api','reply_code':'99'} 
        api_result = {'api_status': 'error', 'api_message': msg,'api_data':provider_reply}
        log_process_finish(_process_msgID, api_result, **_process_call_area)    
        return api_result

    if send_result.get('api_status')=='success':
        smstext=Message[0:5]+'***'
        msg = f'OK. sms sent To [{To}] from [{From}] with Text {smstext}'
        api_result = send_result        
        api_result.update({'api_message': msg})
    else:
        api_result = send_result
    # provider_reply = {'provider_reply': reply, 'reply_code': status_code,'reply_message':reply_message}
                
    log_process_finish(_process_msgID, api_result, **_process_call_area)    
    return api_result
#:::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
#:::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
#:::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
def sendSMS_through_CYTA(From, To, Cc, Bcc, Message, language='En', caller_area={}):
    """
    sendSMS_through_CYTA
    """
    _process_name = 'sendSMS_through_CYTA'
    _process_entity = 'sms'
    _process_action = 'send_sms'
    _process_msgID = f'process:[{_process_name}]'
    _process_identity_kwargs = {'type': 'process', 'module': module_id, 'name': _process_name, 'action': _process_action, 'entity': _process_entity, 'msgID': _process_msgID,}
    _process_adapters_kwargs = {'dbsession': None}
    _process_log_kwargs = {'indent_method': 'AUTO', 'indent_level': None}
    _process_debug_level = get_debug_level(caller_area.get('debug_level'), **_process_identity_kwargs, **_process_adapters_kwargs)
    _process_debug_files = get_debug_files(_process_debug_level, **_process_identity_kwargs, **_process_adapters_kwargs)
    _process_debug_kwargs={'debug_level':_process_debug_level,'debug_files':_process_debug_files}

    _process_signature = build_process_signature(**_process_identity_kwargs, **_process_adapters_kwargs, **_process_debug_kwargs, **_process_log_kwargs)
    _process_call_area = build_process_call_area(_process_signature, caller_area)

    log_process_start(_process_msgID,**_process_call_area)

    log_process_input('', 'From', From,**_process_call_area)
    log_process_input('', 'To', To,**_process_call_area)
    log_process_input('', 'Cc', Cc,**_process_call_area)
    log_process_input('', 'Bcc', Bcc,**_process_call_area)
    log_process_input('', 'language', language, **_process_call_area)
    log_process_input('', 'Message', Message, **_process_call_area)
    log_process_input('', 'caller_area', caller_area, **_process_call_area)

    SMS_SERVER_CYTA_USERNAME = thisApp.application_configuration.get('SMS_SERVER_CYTA_USERNAME')
    SMS_SERVER_CYTA_SECRETKEY = thisApp.application_configuration.get('SMS_SERVER_CYTA_SECRETKEY')
    SMS_SERVER_CYTA_SMS_SENDER = thisApp.application_configuration.get('SMS_SERVER_CYTA_SMS_SENDER')
    SMS_SERVER_CYTA_URL = thisApp.application_configuration.get('SMS_SERVER_CYTA_URL')


    # SMS_SERVER_CYTA_URL = 'https://www.cyta.com.cy/cytamobilevodafone/dev/websmsapi/sendsms.aspx'
    # SMS_SERVER_CYTA_USERNAME = 'Philippos'
    # SMS_SERVER_CYTA_SECRETKEY = 'f69f0d4702814d1fa1768f397ce9b485'
    # SMS_SERVER_CYTA_SMS_SENDER = 'GanimidesT'

    log_process_parameter('', 'config param', 'SMS_SERVER_CYTA_URL', SMS_SERVER_CYTA_URL, **_process_call_area)
    log_process_parameter('', 'config param', 'SMS_SERVER_CYTA_SMS_SENDER', SMS_SERVER_CYTA_SMS_SENDER, **_process_call_area)
    log_process_parameter('', 'config param', 'SMS_SERVER_CYTA_USERNAME', SMS_SERVER_CYTA_USERNAME, **_process_call_area)
    log_process_parameter('', 'config param', 'SMS_SERVER_CYTA_SECRETKEY', SMS_SERVER_CYTA_SECRETKEY, **_process_call_area)

    From = SMS_SERVER_CYTA_SMS_SENDER
    
    request_xml=f"""<?xml version="1.0" encoding="UTF-8" ?><websmsapi><version>1.0</version><username>{SMS_SERVER_CYTA_USERNAME}</username><secretkey>{SMS_SERVER_CYTA_SECRETKEY}</secretkey><recipients><count>1</count><mobiles><m>{To}</m></mobiles></recipients><message>{Message}</message><language>{language}</language></websmsapi>"""

    #print(request_xml)

    log_process_data('', 'From', From, **_process_call_area)
    log_process_data('', 'request_xml', request_xml, **_process_call_area)

    try:
        msg='start sending SMS using CYTA web api'
        log_process_message('', '', msg,**_process_call_area)

        # headers = {'Content-Type': 'application/xml; charset=utf-8', 'Content-length': len(request_xml), 'Connection': 'close',}
        headers = {'Content-Type': 'application/xml; charset=utf-8'}

        if caller_area.get('sms_simulation'):
            reply='sms_simulation:success'
            status_code = '0'
            reply_message = 'simulated sms send'
            sms_uid='simulated_sms:'
        else:
            r = requests.post(SMS_SERVER_CYTA_URL, headers=headers, data=request_xml)
            if r.status_code in (200, 201):
                if r.headers.get('Content-Type','')=='application/json':
                    log_process_data('', 'response', str(r.json()), **_process_call_area)
                    reply = r.json()
                    status_code = reply.get('status', 99)
                else:
                    reply = r.text
                    log_process_data('', 'response', reply, **_process_call_area)
                    r = ET.fromstring(reply) #xml parse from string
                    status_node = r.find('status')
                    try:
                        status_code = status_node.text
                    except:
                        status_code = '99'
                    lot_node = r.find('lot')
                    try:
                        sms_uid = lot_node.text
                    except:
                        sms_uid = 'failed_sms:'
            else:
                status_code = '99'
                sms_uid = 'failed_sms:'

        if not status_code=='0':
            error_text = get_cyta_error_message(status_code)
            reply_message=error_text
        else:
            reply_message = ""
            
        if not status_code=='0':
            msg= f'sending SMS provider error:{status_code}-{reply_message}'
            log_process_message('', 'error', msg,**_process_call_area)
        else:        
            msg='SMS sent using CYTA web api'
            log_process_message('', 'success', msg,**_process_call_area)
    except Exception as error_text:
        msg= f'sending SMS system error:{error_text}'
        log_process_message('', 'error', msg,**_process_call_area)
        reply='exception occurred executing CYTA web api'
        status_code = '99'
        reply_message = msg
        sms_uid=''
    
    provider_reply = {'provider_reply': reply, 'reply_code': status_code, 'reply_message': reply_message, 'provider': 'CYTA', 'provider_send_id': sms_uid}

    if not status_code=='0':
        api_result = {'api_status': 'error', 'api_message': msg,'api_data':provider_reply}
        log_process_finish(_process_msgID, api_result, **_process_call_area)    
        return api_result

    msg = f'SMS sent To [{To}] from [{From}] with Text [{Message}]'
    smstext=Message[0:5]+'***'
    msg= f'SMS sent To [{To}] from [{From}] with Text {smstext}'
    api_result = {'api_status': 'success', 'api_message': msg, 'api_data':provider_reply}
    log_process_finish(_process_msgID, api_result, **_process_call_area)    
    return api_result
#:::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
#:::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
#:::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
def sendSMS_through_NEXMO(From, To, Cc, Bcc, Message, language='En', caller_area={}):
    """
    sendSMS_through_NEXMO
    """
    _process_name = 'sendSMS_through_NEXMO'
    _process_entity = 'sms'
    _process_action = 'send_sms'
    _process_msgID = f'process:[{_process_name}]'
    _process_identity_kwargs = {'type': 'process', 'module': module_id, 'name': _process_name, 'action': _process_action, 'entity': _process_entity, 'msgID': _process_msgID,}
    _process_adapters_kwargs = {'dbsession': None}
    _process_log_kwargs = {'indent_method': 'AUTO', 'indent_level': None}
    _process_debug_level = get_debug_level(caller_area.get('debug_level'), **_process_identity_kwargs, **_process_adapters_kwargs)
    _process_debug_files = get_debug_files(_process_debug_level, **_process_identity_kwargs, **_process_adapters_kwargs)
    _process_debug_kwargs={'debug_level':_process_debug_level,'debug_files':_process_debug_files}

    _process_signature = build_process_signature(**_process_identity_kwargs, **_process_adapters_kwargs, **_process_debug_kwargs, **_process_log_kwargs)
    _process_call_area = build_process_call_area(_process_signature, caller_area)

    log_process_start(_process_msgID,**_process_call_area)

    log_process_input('', 'From', From,**_process_call_area)
    log_process_input('', 'To', To,**_process_call_area)
    log_process_input('', 'Cc', Cc,**_process_call_area)
    log_process_input('', 'Bcc', Bcc,**_process_call_area)
    log_process_input('', 'language', language, **_process_call_area)
    log_process_input('', 'Message', Message, **_process_call_area)
    log_process_input('', 'caller_area', caller_area, **_process_call_area)

    SMS_SERVER_NEXMO_API_KEY = thisApp.application_configuration.get('SMS_SERVER_NEXMO_API_KEY')
    SMS_SERVER_NEXMO_API_SECRET = thisApp.application_configuration.get('SMS_SERVER_NEXMO_API_SECRET')

    # SMS_SERVER_NEXMO_API_KEY = '3ee5cdd5'
    # SMS_SERVER_NEXMO_API_SECRET = 'lgzsdgI4cP9eZl7J'
    # # SMS_SERVER_NEXMO_FROM_NUMBER = '35799599819'

    log_process_parameter('', 'config param', 'SMS_SERVER_NEXMO_API_KEY', SMS_SERVER_NEXMO_API_KEY, **_process_call_area)
    log_process_parameter('', 'config param', 'SMS_SERVER_NEXMO_API_SECRET', SMS_SERVER_NEXMO_API_SECRET, **_process_call_area)
    # Within the Nexmo Voice API all numbers are in E.164 format. This means that numbers:
    # Omit both a leading + and the international access code such as 00 or 001.
    # Contain no special characters, such as a space, () or -    
    To = To.replace('+', '').replace('(', '').replace(')', '').replace('-', '')
    log_process_data('', 'To number in E.164 format', To, **_process_call_area)
    
    try:
        msg='start sending SMS using NEXMO'
        log_process_message('', '', msg,**_process_call_area)

        if caller_area.get('sms_simulation'):
            reply='sms_simulation:success'
            status_code = '0'
            reply_message = "simulated sms send"
            sms_uid = "simulated_sms:"
            log_process_message('','success',"SIMULATION:Message sent successfully.")
        else:
            # Create a new Nexmo Client object:
            nexmo_client = nexmo.Client(key=SMS_SERVER_NEXMO_API_KEY, secret=SMS_SERVER_NEXMO_API_SECRET)
            # Send the SMS message:
            nexmo_api_result = nexmo_client.send_message({
                'from': From,
                'to': To,
                'text': Message,
            })
            log_process_data('', 'nexmo_api_result', nexmo_api_result, **_process_call_area)
            #{'message-count': '1', 'messages': [{'to': 'YOUR-PHONE-NUMBER', 'message-id': '0D00000039FFD940', 'status': '0', 'remaining-balance': '14.62306950', 'message-price': '0.03330000', 'network': '12345'}]}
            #{'message-count': '1', 'messages': [{'to':'35799359864', 'message-id':'1C00000027D52523', 'status':'0', 'remaining-balance':'1.79360000', 'message-price':'0.06880000', 'network':'28001'}]}
            reply=nexmo_api_result
            status_code = nexmo_api_result["messages"][0].get("status","99")
            reply_message = nexmo_api_result["messages"][0].get("error-text","")
            sms_uid = nexmo_api_result["messages"][0].get("message-id","failed_sms")
            if not status_code=='0':
                msg= f'sending SMS provider error:{status_code}-{reply_message}'
                log_process_message('', 'error', msg,**_process_call_area)
            else:            
                msg='OK. SMS sent using NEXMO'
                log_process_message('', 'success', msg,**_process_call_area)
    except Exception as error_text:
        msg= f'sending SMS system error:{error_text}'
        log_process_message('', 'error', msg, **_process_call_area)
        reply='exception occurred executing NEXMO client api'
        status_code = '99'
        reply_message = msg
        sms_uid=''
    
    provider_reply = {'provider_reply': reply, 'reply_code': status_code, 'reply_message': reply_message, 'provider': 'NEXMO', 'provider_send_id': sms_uid}

    if not status_code=='0':
        api_result = {'api_status': 'error', 'api_message': msg,'api_data':provider_reply}
        log_process_finish(_process_msgID, api_result, **_process_call_area)    
        return api_result

    msg = f'SMS sent To [{To}] from [{From}] with Text [{Message}]'
    smstext=Message[0:5]+'***'
    msg= f'SMS sent To [{To}] from [{From}] with Text {smstext}'
    api_result = {'api_status': 'success', 'api_message': msg, 'api_data':provider_reply}
    log_process_finish(_process_msgID, api_result, **_process_call_area)    
    return api_result
#:::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
#:::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
#:::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
def sendSMS_through_SINCH(From, To, Cc, Bcc, Message, language='En', caller_area={}):
    """
    sendSMS_through_SINCH
    """
    _process_name = 'sendSMS_through_SINCH'
    _process_entity = 'sms'
    _process_action = 'send_sms'
    _process_msgID = f'process:[{_process_name}]'
    _process_identity_kwargs = {'type': 'process', 'module': module_id, 'name': _process_name, 'action': _process_action, 'entity': _process_entity, 'msgID': _process_msgID,}
    _process_adapters_kwargs = {'dbsession': None}
    _process_log_kwargs = {'indent_method': 'AUTO', 'indent_level': None}
    _process_debug_level = get_debug_level(caller_area.get('debug_level'), **_process_identity_kwargs, **_process_adapters_kwargs)
    _process_debug_files = get_debug_files(_process_debug_level, **_process_identity_kwargs, **_process_adapters_kwargs)
    _process_debug_kwargs={'debug_level':_process_debug_level,'debug_files':_process_debug_files}

    _process_signature = build_process_signature(**_process_identity_kwargs, **_process_adapters_kwargs, **_process_debug_kwargs, **_process_log_kwargs)
    _process_call_area = build_process_call_area(_process_signature, caller_area)

    log_process_start(_process_msgID,**_process_call_area)

    log_process_input('', 'From', From,**_process_call_area)
    log_process_input('', 'To', To,**_process_call_area)
    log_process_input('', 'Cc', Cc,**_process_call_area)
    log_process_input('', 'Bcc', Bcc,**_process_call_area)
    log_process_input('', 'language', language, **_process_call_area)
    log_process_input('', 'Message', Message, **_process_call_area)
    log_process_input('', 'caller_area', caller_area, **_process_call_area)

    SMS_SERVER_SINCH_API_KEY = thisApp.application_configuration.get('SMS_SERVER_SINCH_API_KEY')
    SMS_SERVER_SINCH_API_SECRET = thisApp.application_configuration.get('SMS_SERVER_SINCH_API_SECRET')
    SMS_SERVER_SINCH_FROM_NUMBER = thisApp.application_configuration.get('SMS_SERVER_SINCH_FROM_NUMBER')

    # SMS_SERVER_SINCH_API_KEY = 'be0c283385204338815a88ae81add209'
    # SMS_SERVER_SINCH_API_SECRET = '1d5c5cab2725437bbd6d68298f78f7b3'
    # SMS_SERVER_SINCH_FROM_NUMBER = '35799599819'

    log_process_parameter('', 'config param', 'SMS_SERVER_SINCH_FROM_NUMBER', SMS_SERVER_SINCH_FROM_NUMBER, **_process_call_area)
    log_process_parameter('', 'config param', 'SMS_SERVER_SINCH_API_KEY', SMS_SERVER_SINCH_API_KEY, **_process_call_area)
    log_process_parameter('', 'config param', 'SMS_SERVER_SINCH_API_SECRET', SMS_SERVER_SINCH_API_SECRET, **_process_call_area)

    try:
        msg='start sending SMS using SINCH'
        log_process_message('', '', msg,**_process_call_area)

        if caller_area.get('sms_simulation'):
            reply='sms_simulation:success'
            status_code = '0'
            reply_message = "simulated sms send"
            sms_uid = "simulated_sms:"
            log_process_message('','success',"SIMULATION:Message sent successfully.")
        else:
            # Create a new SinchSMS Client object:
            client = SinchSMS(SMS_SERVER_SINCH_API_KEY, SMS_SERVER_SINCH_API_SECRET)
            # Send the SMS message:
            response = client.send_message(To, Message)
            log_process_data('', 'response', response, **_process_call_area)
            message_id = response['messageId']
            sms_uid = message_id
            response = client.check_status(message_id)
            ix=0
            while response['status'] != 'Successful':
                ix = ix + 1
                log_process_data('', f'{ix}. status', response['status'], **_process_call_area)
                time.sleep(1)
                response = client.check_status(message_id)
                reply = response
                status_code = response['status']
                reply_message = response['status']

            provider_reply = {'provider_reply': reply, 'reply_code': status_code,'reply_message':reply_message}
           
            if not response['status'] == 'Successful':
                msg= f'sending SMS provider error:{status_code}-{reply_message}'
                log_process_message('', 'error', msg,**_process_call_area)
            else:            
                msg='OK. SMS sent using SINCH'
                log_process_message('', 'success', msg,**_process_call_area)
    except Exception as error_text:
        msg= f'sending SMS system error:{error_text}'
        log_process_message('', 'error', msg,**_process_call_area)
        reply='exception occurred executing NEXMO client api'
        status_code = '99'
        reply_message = msg
        sms_uid=''
    
    provider_reply = {'provider_reply': reply, 'reply_code': status_code, 'reply_message': reply_message, 'provider': 'SINCH', 'provider_send_id': sms_uid}

    if not status_code=='0':
        api_result = {'api_status': 'error', 'api_message': msg,'api_data':provider_reply}
        log_process_finish(_process_msgID, api_result, **_process_call_area)    
        return api_result

    msg = f'SMS sent To [{To}] from [{From}] with Text [{Message}]'
    smstext=Message[0:5]+'***'
    msg= f'SMS sent To [{To}] from [{From}] with Text {smstext}'
    api_result = {'api_status': 'success', 'api_message': msg, 'api_data':provider_reply}
    log_process_finish(_process_msgID, api_result, **_process_call_area)    
    return api_result
#:::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
# Python3 program to check if  
# given mobile number is valid 
def mobile_isValid(s): 
    # 1) Begins with 0 or 91 
    # 2) Then contains 7 or 8 or 9. 
    # 3) Then contains 9 digits 
    Pattern = re.compile("(0/91)?[7-9][0-9]{9}") 
    return Pattern.match(s) 
# This code is contributed by rishabh_jain  
#:::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
def get_phone_number_analysis_through_NEXMO(number):
    SMS_SERVER_NEXMO_API_KEY = '3ee5cdd5'
    SMS_SERVER_NEXMO_API_SECRET = 'lgzsdgI4cP9eZl7J'
    try:
        nexmo_client = nexmo.Client(key=SMS_SERVER_NEXMO_API_KEY, secret=SMS_SERVER_NEXMO_API_SECRET)
        result = nexmo_client.get_basic_number_insight(number=number)
        #{'status': 0, 'status_message': 'Success', 'request_id': '704f99f9-dbbc-47cd-aeed-dd0c1be7fa4b', 'international_format_number': '35799359864', 'national_format_number': '99 359864', 'country_code': 'CY', 'country_code_iso3': 'CYP', 'country_name': 'Cyprus', 'country_prefix': '357'}
        #print(result)
        return result
    except Exception as error_text:
        return {}
#:::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
def get_validated_phone_number(number):
    if not (number):
        return({'api_status':'error','message':'empty'})

    number = number.strip()
    while number[0] == '0' and len(number)>1:
        number = number[1:]
    while number[0] == '+' and len(number)>1:
        number = number[1:]    
    if len(number) < 11:
        return({'api_status':'error','message':'length error'})

    number = '+' + number

    try:
        phone_number = phonenumbers.parse(number)
    except:
        phone_number = None

    if not phone_number:
        return({'api_status':'error','message':'validation failed'})

    if 1 == 2:
        x='foo'

    inumber = '+' + str(phone_number.country_code) + str(phone_number.national_number)
    return {'api_status': 'success', 'api_message': 'OK', 'country_code': str(phone_number.country_code), 'national_number': str(phone_number.national_number), 'international_number': inumber}
#:::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
def get_cyta_error_message(code):
    reply_messages={
        '0': 'Send Sms success',
        '1': 'You are not allowed to use the service',
        '2': 'The service is suspended',
        '9': 'Generic send sms failure',
        '10': 'User not found or Suspended cybee account/Invalid Secret Key',
        '11': 'configuration settings not found for Username',
        '12': 'Web Sms Api Suspended or Terms not accepted',
        '13': 'Client IP does not match expected IP',
        '19': 'Registered mobile number for username not found',
        '20':'missing field values or case (lower/upper) of elements',
        '21':'invalid username',
        '22':'invalid characters in Recipients',
        '23':'invalid characters in recipient count',
        '24':'invalid language',
        '25':'cybee recipients count and user entered count does not match',
        '26':'Recipients list is bigger than allowed',
        '27':'Invalid mobile number found',
        '28': 'Message length is bigger than allowed',
        '29': ' Unsupported Content Type',
        '30': 'Missing HTTP Post request body',
        '31': 'Max allowed sms messages per day threshold reached',
        '39':' Invalid Version',
        '90': 'Exception',
        '91': 'Exception processing URL Encoded request',
        '92': 'Exception processing XML request',
        '93': 'Invalid XML request data',
        '99': 'GENERAL EXCEPTION',
    }
    msg = reply_messages.get(code, f'general exception, code={code}')
    return msg
#::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
def get_nexmo_error_message(code):
    reply_messages={
    '1':'Throttled	You have exceeded the submission capacity allowed on this account. Please wait and retry.',
    '2':'Missing params	Your request is incomplete and missing some mandatory parameters.',
    '3':'Invalid params	The value of one or more parameters is invalid.',
    '4':'Invalid credentials	The api_key / api_secret you supplied is either invalid or disabled.',
    '5':'Internal error	There was an error processing your request in the Platform.',
    '6':'Invalid message	The Platform was unable to process your request. For example, due to an unrecognised prefix for the phone number.',
    '7':'Number barred	The number you are trying to submit to is blacklisted and may not receive messages.',
    '8':'Partner account barred	The api_key you supplied is for an account that has been barred from submitting messages.',
    '9':'Partner quota exceeded	Your pre-paid account does not have sufficient credit to process this message.',
    '11':'Account not enabled for REST	This account is not provisioned for REST submission, you should use SMPP instead.',
    '12':'Message too long	The length of udh and body was greater than 140 octets for a binary type SMS request.',
    '13':'Communication Failed	Message was not submitted because there was a communication failure.',
    '14':'Invalid Signature	Message was not submitted due to a verification failure in the submitted signature.',
    '15':'Illegal Sender Address - rejected	Due to local regulations, the SenderID you set in from in the request was not accepted. Please check the Global messaging section.',
    '16':'Invalid TTL	The value of ttl in your request was invalid.',
    '19':'Facility not allowed	Your request makes use of a facility that is not enabled on your account.',
    '20':'Invalid Message class	The value of message-class in your request was out of range. See https://en.wikipedia.org/wiki/Data_Coding_Scheme.',
    '23':'Bad callback :: Missing Protocol	You did not include https in the URL you set in callback.',
    '29':'Non White-listed Destination	The phone number you set in to is not in your pre-approved destination list. To send messages to this phone number, add it using Dashboard.',
    '34': 'Invalid or Missing Msisdn Param	The phone number you supplied in the to parameter of your request was either missing or invalid.',
    '97': 'counter not len(messages)',
    '98': 'counter not 1',
    '99': 'GENERAL EXCEPTION',
    }
    msg = reply_messages.get(code, f'general exception, code={code}')
    return msg
#::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
#::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
# module initialization
#::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
#::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
#::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
# master_configuration = retrieve_module_configuration(module_identityDictionary, master_configuration, print_enabled=consolelog_enabled, filelog_enabled=filelog_enabled, handle_as_init=False)
master_configuration={}
#::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
#(print_enabled, filelog_enabled, log_file, errors_file,consolelog_enabled)=get_globals_from_configuration(master_configuration)
#::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
#master_configuration = add_methods_To_configuration('database_actions', master_configuration, leandroutechnologyforward_database_session_class, ['ALL'], ['_init_'])
#::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
# methods == collect_method_names_from_class(leandroutechnologyforward_database_session_class, methods_ids=['ALL'])
# print(methods)
# exit(0)

# master_configuration = add_apis_To_configuration('database_actions', master_configuration, thisModuleObj, functions_ids, exclude_functions_ids)

#save_module_configuration(module_identityDictionary, master_configuration, print_enabled=consolelog_enabled, filelog_enabled=filelog_enabled)
#thisApp.pair_module_configuration('database_actions',master_configuration)
#::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
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
    #tests/research
    # print(__file__)
    client = {'name': 'PHILIPPOS', 'mobile': '+35799359864'}
    # print(string_translate('hello #NAME#, Today is #TODAY#', client))
    message = 'hi. confirm http://127.0.0.1:5555/confirmation/ABCDEF1212121adasdada/mobile'
    message = 'hi. confirm http://127.0.0.1:5555/confirmation/2A2AC402AAA5/mobile'
    print(send_sms(From='noreply@leandrou.com', To='+35799359864', Message=message, data_record=client, caller_area={'debug_level': 99}))

