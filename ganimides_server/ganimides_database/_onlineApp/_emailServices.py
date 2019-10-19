# -*- coding: utf-8 -*-
import os
import sys
if not (os.path.dirname(__file__) in sys.path): sys.path.append(os.path.dirname(__file__))

import smtplib

from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from mailjet_rest import Client

import _appEnvironment as thisApp
from _utilities import string_translate
from _processServices import set_process_identity_dict, set_process_caller_area,build_process_signature, build_process_call_area
from _debugServices import get_debug_option_as_level,get_debug_files,get_debug_level
from _logProcessServices import log_process_start, log_process_finish, log_process_message, log_process_result,log_process_data, log_process_input, log_process_output,log_process_parameter
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
def get_template(template,application_name=''): #under construction
    subject = ''
    text = ''
    html = ''
    return (subject,text,html)
#:::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
#:::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
#:::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
def send_email(From='', To='', Cc='', Bcc='', Subject='', text_body='', html_body='', email_template='', data_record={}, attachments=[], application_name='', language='En', caller_area={}):
    """
    send_email (wrapper)
    """
    _process_name = 'send_email'
    _process_entity = 'email'
    _process_action = 'send_email'
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
    log_process_input('', 'Subject', Subject, **_process_call_area)
    log_process_input('', 'text_body', text_body, **_process_call_area)
    log_process_input('', 'html_body', html_body, **_process_call_area)
    log_process_input('', 'email_template', email_template, **_process_call_area)
    log_process_input('', 'application_name', application_name, **_process_call_area)
    log_process_input('', 'attachments', attachments, **_process_call_area)
    log_process_input('', 'caller_area', caller_area, **_process_call_area)

    if not From:
        From = thisApp.application_configuration.get('mail_sender')
        log_process_data('', 'From', From,**_process_call_area)
    # if not From:
    #     From='ganimides@gmail.com'
    
    if not(From):
        msg = f'mail sender not defined'
        api_result = {'api_status': 'error', 'api_message': msg}
        log_process_finish(_process_msgID, api_result, **_process_call_area)    
        return api_result
    if not(To):
        msg = f'email recipient not defined'
        api_result = {'api_status': 'error', 'api_message': msg}
        log_process_finish(_process_msgID, api_result, **_process_call_area)    
        return api_result
    if not(Subject):
        msg = f'email Subject not defined'
        api_result = {'api_status': 'error', 'api_message': msg}
        log_process_finish(_process_msgID, api_result, **_process_call_area)    
        return api_result

    if not(text_body) and not(html_body) and not(email_template):
        msg = f'no body or template defined'
        api_result = {'api_status': 'error', 'api_message': msg}
        log_process_message('', 'warning', msg,**_process_call_area)
    else:
        if email_template:
            (t1, t2, t3) = get_template(email_template,application_name)
            if t1 or t2 or t3:
                Subject = t1
                text_body = t2
                html_body = t3
            else:
                msg = f'email template {email_template} not found'
                api_result = {'api_status': 'error', 'api_message': msg}
                log_process_finish(_process_msgID, api_result, **_process_call_area)    
                return api_result
            # # Create the body of the message (a plain-text and an HTML version).
            # template_Text = "Hi!\nHow are you?\nHere is the link you wanted:\nhttp://www.python.org"
            # template_Html = """\
            # <html>
            # <head></head>
            # <body>
            #     <p>Hi!<br>
            #     How are you?<br>
            #     Here is the <a href="http://www.python.org">link</a> you wanted.
            #     </p>
            # </body>
            # </html>
            # """

        if text_body.find('#')>=0:
            text_body = string_translate(text_body, data_record)
            log_process_data('', 'translated text_body', text_body,**_process_call_area)
        
        if html_body.find('#')>=0:
            html_body = string_translate(html_body, data_record)
            log_process_data('', 'translated html_body', html_body,**_process_call_area)

        if not(text_body) and not(html_body):
            msg = f'content build FAILED'
            api_result = {'api_status': 'error', 'api_message': msg}
            log_process_finish(_process_msgID, api_result, **_process_call_area)    
            return api_result

    if Subject.find('#')>=0:
        Subject = string_translate(Subject, data_record)
        log_process_data('', 'translated Subject', Subject,**_process_call_area)


    MAIL_SERVER_PROVIDER = thisApp.application_configuration.get('MAIL_SERVER_PROVIDER')
    MAIL_SERVER = thisApp.application_configuration.get('MAIL_SERVER')
    MAIL_PORT = thisApp.application_configuration.get('MAIL_PORT')
    MAIL_USE_TLS = thisApp.application_configuration.get('MAIL_USE_TLS')
    MAIL_USE_SSL = thisApp.application_configuration.get('MAIL_USE_SSL')
    MAIL_USERNAME = thisApp.application_configuration.get('MAIL_USERNAME')
    MAIL_PASSWORD = thisApp.application_configuration.get('MAIL_PASSWORD')
    MAIL_APIKEY_PUBLIC = thisApp.application_configuration.get('MAIL_APIKEY_PUBLIC')
    MAIL_APIKEY_PRIVATE = thisApp.application_configuration.get('MAIL_APIKEY_PRIVATE')
    MAIL_SEND_METHOD = thisApp.application_configuration.get('MAIL_SEND_METHOD')

    log_process_parameter('', 'config param', 'MAIL_SERVER', MAIL_SERVER, **_process_call_area)
    log_process_parameter('', 'config param', 'MAIL_SEND_METHOD', MAIL_SEND_METHOD, **_process_call_area)
    log_process_parameter('', 'config param', 'MAIL_PORT', MAIL_PORT, **_process_call_area)
    log_process_parameter('', 'config param', 'MAIL_USE_TLS', MAIL_USE_TLS, **_process_call_area)
    log_process_parameter('', 'config param', 'MAIL_USE_SSL', MAIL_USE_SSL, **_process_call_area)
    log_process_parameter('', 'config param', 'MAIL_USERNAME', MAIL_USERNAME, **_process_call_area)
    log_process_parameter('', 'config param', 'MAIL_PASSWORD', MAIL_PASSWORD, **_process_call_area)
    log_process_parameter('', 'config param', 'MAIL_APIKEY_PUBLIC', MAIL_APIKEY_PUBLIC, **_process_call_area)
    log_process_parameter('', 'config param', 'MAIL_APIKEY_PRIVATE', MAIL_APIKEY_PRIVATE, **_process_call_area)

    try:
        if MAIL_SERVER_PROVIDER.upper() == 'MAILJET':
            if MAIL_SEND_METHOD.upper() == 'SMTP':
                send_result=sendEmail_using_SMTP(From, To, Cc, Bcc, Subject, text_body, html_body, attachments, caller_area=_process_call_area)
            else:
                send_result=sendEmail_thru_mailjet(From, To, Cc, Bcc, Subject, text_body, html_body, attachments, caller_area=_process_call_area)
        else:
            if MAIL_SERVER_PROVIDER == 'YANDEX':
                if MAIL_SEND_METHOD =='SMTP':
                    send_result=sendEmail_using_SMTP(From, To, Cc, Bcc, Subject, text_body, html_body, attachments, caller_area=_process_call_area)
                else:
                    send_result=sendEmail_thru_sendgrid(From, To, Cc, Bcc, Subject, text_body, html_body, attachments, caller_area=_process_call_area)
            else:
                send_result=sendEmail_using_SMTP(From, To, Cc, Bcc, Subject, text_body, html_body, attachments, caller_area=_process_call_area)
                #send_result=sendEmail_thru_google(From, To, Cc, Bcc, Subject, text_body, html_body,parContentTemplate)
    except Exception as error_text:
        msg= f'email send failed. system error:{error_text}'
        log_process_message('', 'error', msg,**_process_call_area)
        api_result = {'api_status': 'error', 'api_message': msg}
        log_process_finish(_process_msgID, api_result, **_process_call_area)    
        return api_result

    if send_result.get('api_status')=='success':
        msg= f'OK. email send To [{To}] with Subject [[{Subject}]]'
        api_result = {'api_status': 'success', 'api_message': msg}
    else:
        api_result = send_result
                
    log_process_finish(_process_msgID, api_result, **_process_call_area)    
    return api_result
#:::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
#:::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
#:::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
def send_outlook_email(To='', Cc='', Bcc='', Subject='', text_body='', html_body='', email_template='', data_record={}, attachments=[], application_name='', caller_area={}):
    _process_name = 'send_outlook_email'
    _process_entity = 'email'
    _process_action = 'send_email'
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

    log_process_input('', 'To', To,**_process_call_area)
    log_process_input('', 'Cc', Cc,**_process_call_area)
    log_process_input('', 'Bcc', Bcc,**_process_call_area)
    log_process_input('', 'Subject', Subject, **_process_call_area)
    log_process_input('', 'text_body', text_body, **_process_call_area)
    log_process_input('', 'html_body', html_body, **_process_call_area)
    log_process_input('', 'email_template', email_template, **_process_call_area)
    log_process_input('', 'application_name', application_name, **_process_call_area)
    log_process_input('', 'attachments', attachments, **_process_call_area)
    log_process_input('', 'caller_area', caller_area, **_process_call_area)


    # MAIL_APIKEY_PUBLIC = thisApp.application_configuration.get('MAIL_APIKEY_PUBLIC')
    # MAIL_APIKEY_PRIVATE = thisApp.application_configuration.get('MAIL_APIKEY_PRIVATE')

    # log_process_parameter('', 'config param', 'MAIL_APIKEY_PUBLIC', MAIL_APIKEY_PUBLIC, **_process_call_area)
    # log_process_parameter('', 'config param', 'MAIL_APIKEY_PRIVATE', MAIL_APIKEY_PRIVATE, **_process_call_area)

    msg='start sending email thru outlook'
    log_process_message('', '', msg,**_process_call_area)

    import win32com.client as win32

    # if not From:
    #     From = thisApp.application_configuration.get('mail_sender')
    #     log_process_data('', 'From', From,**_process_call_area)
    
    # if not(From):
    #     msg = f'mail sender not defined'
    #     api_result = {'api_status': 'error', 'api_message': msg}
    #     log_process_finish(_process_msgID, api_result, **_process_call_area)    
    #     return api_result

    if not(To):
        msg = f'email recipient not defined'
        api_result = {'api_status': 'error', 'api_message': msg}
        log_process_finish(_process_msgID, api_result, **_process_call_area)    
        return api_result
    if not(Subject):
        msg = f'email Subject not defined'
        api_result = {'api_status': 'error', 'api_message': msg}
        log_process_finish(_process_msgID, api_result, **_process_call_area)    
        return api_result

    if not(text_body) and not(html_body) and not(email_template):
        msg = f'no body or template defined'
        api_result = {'api_status': 'error', 'api_message': msg}
        log_process_message('', 'warning', msg,**_process_call_area)
    else:
        if email_template:
            (t1, t2, t3) = get_template(email_template,application_name)
            if t1 or t2 or t3:
                Subject = t1
                text_body = t2
                html_body = t3
            else:
                msg = f'email template {email_template} not found'
                api_result = {'api_status': 'error', 'api_message': msg}
                log_process_finish(_process_msgID, api_result, **_process_call_area)    
                return api_result

        if text_body.find('#')>=0:
            text_body = string_translate(text_body, data_record)
            log_process_data('', 'translated text_body', text_body,**_process_call_area)
        
        if html_body.find('#')>=0:
            html_body = string_translate(html_body, data_record)
            log_process_data('', 'translated html_body', html_body,**_process_call_area)

        if not(text_body) and not(html_body):
            msg = f'content build FAILED'
            api_result = {'api_status': 'error', 'api_message': msg}
            log_process_finish(_process_msgID, api_result, **_process_call_area)    
            return api_result

    if Subject.find('#')>=0:
        Subject = string_translate(Subject, data_record)
        log_process_data('', 'translated Subject', Subject,**_process_call_area)

    #########
    try:
        outlook = win32.Dispatch('outlook.application')
        mail = outlook.CreateItem(0)
        mail.To = To
        mail.Subject = Subject 
        if Cc:
            mail.Cc = Cc
        if text_body:     
            mail.Body = text_body
        if html_body:
            mail.HTMLBody = html_body

        # To attach a file To the email (optional):
        for ix in range(0, len(attachments)):
            attachment_file = attachments[ix]
            if attachment_file:
                mail.Attachments.Add(attachment_file)
        # if attachment1:
        #     mail.Attachments.Add(attachment1)
        # if attachment2:
        #     mail.Attachments.Add(attachment2)
        # if attachment3:
        #     mail.Attachments.Add(attachment3)
        # if attachment4:
        #     mail.Attachments.Add(attachment4)
        # if attachment5:
        #     mail.Attachments.Add(attachment5)

        #mail.Send() or mail.display()
        mail.display()
        #mail.Send()
        msg= f'OK. email send To [{To}] with Subject [[{Subject}]]'
        api_result = {'api_status': 'success', 'api_message': msg}
        log_process_finish(_process_msgID, api_result, **_process_call_area)    
        return api_result
    except Exception as error_text:
        msg= f'sending email thru outlook system error:{error_text}'
        log_process_message('', 'error', msg,**_process_call_area)
        api_result = {'api_status': 'error', 'api_message': msg}
        log_process_finish(_process_msgID, api_result, **_process_call_area)    
        return api_result
#:::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
#:::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
#:::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
def sendEmail_using_SMTP(From, To, Cc, Bcc, Subject, text_body, html_body, attachments=[], caller_area={}):
    """
    sendEmail_using_SMTP
    """
    _process_name = 'sendEmail_using_SMTP'
    _process_entity = 'email'
    _process_action = 'send_email'
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
    log_process_input('', 'Subject', Subject, **_process_call_area)
    log_process_input('', 'text_body', text_body, **_process_call_area)
    log_process_input('', 'html_body', html_body, **_process_call_area)
    log_process_input('', 'attachments', attachments, **_process_call_area)
    log_process_input('', 'caller_area', caller_area, **_process_call_area)


    MAIL_SERVER = thisApp.application_configuration.get('MAIL_SERVER')
    MAIL_PORT = thisApp.application_configuration.get('MAIL_PORT')
    MAIL_USERNAME = thisApp.application_configuration.get('MAIL_USERNAME')
    MAIL_PASSWORD = thisApp.application_configuration.get('MAIL_PASSWORD')

    log_process_parameter('', 'config param', 'MAIL_SERVER', MAIL_SERVER, **_process_call_area)
    log_process_parameter('', 'config param', 'MAIL_PORT', MAIL_PORT, **_process_call_area)
    log_process_parameter('', 'config param', 'MAIL_USERNAME', MAIL_USERNAME, **_process_call_area)
    log_process_parameter('', 'config param', 'MAIL_PASSWORD', MAIL_PASSWORD, **_process_call_area)

    try:
        email_message = MIME_email_message(From,  To, Cc, Bcc, Subject, text_body, html_body, caller_area=_process_call_area)
        if not(email_message):
            msg= f'can not format email message'
            api_result = {'api_status': 'error', 'api_message': msg}
            log_process_finish(_process_msgID, api_result, **_process_call_area)    
            return api_result
    except Exception as error_text:
        msg= f'can not format email message. system error:{error_text}'
        log_process_message('', 'error', msg,**_process_call_area)
        api_result = {'api_status': 'error', 'api_message': msg}
        log_process_finish(_process_msgID, api_result, **_process_call_area)    
        return api_result

    try:
        msg='start sending email using SMTP method'
        log_process_message('', '', msg,**_process_call_area)
        mail = smtplib.SMTP(MAIL_SERVER, MAIL_PORT)
        mail.ehlo()
        mail.starttls()
        mail.login(MAIL_USERNAME, MAIL_PASSWORD)
        #mail.login('scantzochoiros@gmail.com','philea13')
        mail.sendmail(From, To, email_message.as_string())
        mail.quit()
        msg='email sent using SMTP method'
        log_process_message('', 'success', msg,**_process_call_area)
    except Exception as error_text:
        msg= f'sending email system error:{error_text}'
        log_process_message('', 'error', msg,**_process_call_area)
        api_result = {'api_status': 'error', 'api_message': msg}
        log_process_finish(_process_msgID, api_result, **_process_call_area)    
        return api_result

    msg= f'email send To [{To}] with Subject [[{Subject}]]'
    api_result = {'api_status': 'success', 'api_message': msg}
    log_process_finish(_process_msgID, api_result, **_process_call_area)    
    return api_result
#:::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
#:::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
#:::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
def sendEmail_thru_google(From, To, Cc, Bcc, Subject, text_body, html_body, attachments=[], caller_area={}):
    """
    sendEmail_thru_google
    """
    _process_name = 'sendEmail_thru_google'
    _process_entity = 'email'
    _process_action = 'send_email'
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
    log_process_input('', 'Subject', Subject, **_process_call_area)
    log_process_input('', 'text_body', text_body, **_process_call_area)
    log_process_input('', 'html_body', html_body, **_process_call_area)
    log_process_input('', 'attachments', attachments, **_process_call_area)
    log_process_input('', 'caller_area', caller_area, **_process_call_area)


    MAIL_SERVER = thisApp.application_configuration.get('MAIL_SERVER')
    MAIL_PORT = thisApp.application_configuration.get('MAIL_PORT')
    MAIL_USERNAME = thisApp.application_configuration.get('MAIL_USERNAME')
    MAIL_PASSWORD = thisApp.application_configuration.get('MAIL_PASSWORD')

    log_process_parameter('', 'config param', 'MAIL_SERVER', MAIL_SERVER, **_process_call_area)
    log_process_parameter('', 'config param', 'MAIL_PORT', MAIL_PORT, **_process_call_area)
    log_process_parameter('', 'config param', 'MAIL_USERNAME', MAIL_USERNAME, **_process_call_area)
    log_process_parameter('', 'config param', 'MAIL_PASSWORD', MAIL_PASSWORD, **_process_call_area)

    try:
        email_message = MIME_email_message(From,  To, Cc, Bcc, Subject, text_body, html_body, caller_area=_process_call_area)
        if not(email_message):
            msg= f'can not format email message'
            api_result = {'api_status': 'error', 'api_message': msg}
            log_process_finish(_process_msgID, api_result, **_process_call_area)    
            return api_result
    except Exception as error_text:
        msg= f'can not format email message. system error:{error_text}'
        log_process_message('', 'error', msg,**_process_call_area)
        api_result = {'api_status': 'error', 'api_message': msg}
        log_process_finish(_process_msgID, api_result, **_process_call_area)    
        return api_result

    try:
        msg='start sending email thru google'
        log_process_message('', '', msg,**_process_call_area)
        mail = smtplib.SMTP(MAIL_SERVER, MAIL_PORT)
        mail.ehlo()
        mail.starttls()
        mail.login(MAIL_USERNAME, MAIL_PASSWORD)
        #mail.login('bstarr131@gmail.com', 'bstarr13')
        #mail.login('scantzochoiros@gmail.com', 'philea13')
        mail.sendmail(From, To, email_message.as_string())
        mail.quit()
        msg='email sent thru google'
        log_process_message('', 'success', msg,**_process_call_area)
    except Exception as error_text:
        msg= f'sending email system error:{error_text}'
        log_process_message('', 'error', msg,**_process_call_area)
        api_result = {'api_status': 'error', 'api_message': msg}
        log_process_finish(_process_msgID, api_result, **_process_call_area)    
        return api_result

    msg= f'email send To [{To}] with Subject [[{Subject}]]'
    api_result = {'api_status': 'success', 'api_message': msg}
    log_process_finish(_process_msgID, api_result, **_process_call_area)    
    return api_result
#:::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
#:::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
#:::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
def sendEmail_thru_mailjet(From, To, Cc, Bcc, Subject, text_body, html_body, attachments=[], caller_area={}):
    """
    sendEmail_thru_mailjet
    """
    _process_name = 'sendEmail_thru_mailjet'
    _process_entity = 'email'
    _process_action = 'send_email'
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
    log_process_input('', 'Subject', Subject, **_process_call_area)
    log_process_input('', 'text_body', text_body, **_process_call_area)
    log_process_input('', 'html_body', html_body, **_process_call_area)
    log_process_input('', 'attachments', attachments, **_process_call_area)
    log_process_input('', 'caller_area', caller_area, **_process_call_area)


    MAIL_SERVER = thisApp.application_configuration.get('MAIL_SERVER')
    MAIL_PORT = thisApp.application_configuration.get('MAIL_PORT')
    MAIL_USERNAME = thisApp.application_configuration.get('MAIL_USERNAME')
    MAIL_PASSWORD = thisApp.application_configuration.get('MAIL_PASSWORD')

    log_process_parameter('', 'config param', 'MAIL_SERVER', MAIL_SERVER, **_process_call_area)
    log_process_parameter('', 'config param', 'MAIL_PORT', MAIL_PORT, **_process_call_area)
    log_process_parameter('', 'config param', 'MAIL_USERNAME', MAIL_USERNAME, **_process_call_area)
    log_process_parameter('', 'config param', 'MAIL_PASSWORD', MAIL_PASSWORD, **_process_call_area)

    try:
        email_message = MIME_email_message(From,  To, Cc, Bcc, Subject, text_body, html_body, caller_area=_process_call_area)
        if not(email_message):
            msg= f'can not format email message'
            api_result = {'api_status': 'error', 'api_message': msg}
            log_process_finish(_process_msgID, api_result, **_process_call_area)    
            return api_result
    except Exception as error_text:
        msg= f'can not format email message. system error:{error_text}'
        log_process_message('', 'error', msg,**_process_call_area)
        api_result = {'api_status': 'error', 'api_message': msg}
        log_process_finish(_process_msgID, api_result, **_process_call_area)    
        return api_result

    try:
        msg='start sending email thru mailjet'
        log_process_message('', '', msg,**_process_call_area)
        mail = smtplib.SMTP(MAIL_SERVER, MAIL_PORT)
        mail.ehlo()
        mail.starttls()
        mail.login(MAIL_USERNAME, MAIL_PASSWORD)
        mail.sendmail(From, To, email_message.as_string())
        mail.quit()
        msg='email sent thru mailjet'
        log_process_message('', 'success', msg,**_process_call_area)
    except Exception as error_text:
        msg= f'sending email system error:{error_text}'
        log_process_message('', 'error', msg,**_process_call_area)
        api_result = {'api_status': 'error', 'api_message': msg}
        log_process_finish(_process_msgID, api_result, **_process_call_area)    
        return api_result

    msg= f'email send To [{To}] with Subject [[{Subject}]]'
    api_result = {'api_status': 'success', 'api_message': msg}
    log_process_finish(_process_msgID, api_result, **_process_call_area)    
    return api_result
#:::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
#:::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
#:::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
def sendEmail_thru_sendgrid(From, To, Cc, Bcc, Subject, text_body, html_body, attachments=[], caller_area={}):
    """
    sendEmail_thru_sendgrid
    """
    _process_name = 'sendEmail_thru_sendgrid'
    _process_entity = 'email'
    _process_action = 'send_email'
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
    log_process_input('', 'Subject', Subject, **_process_call_area)
    log_process_input('', 'text_body', text_body, **_process_call_area)
    log_process_input('', 'html_body', html_body, **_process_call_area)
    log_process_input('', 'attachments', attachments, **_process_call_area)
    log_process_input('', 'caller_area', caller_area, **_process_call_area)


    MAIL_APIKEY_PUBLIC = thisApp.application_configuration.get('MAIL_APIKEY_PUBLIC')
    MAIL_APIKEY_PRIVATE = thisApp.application_configuration.get('MAIL_APIKEY_PRIVATE')

    log_process_parameter('', 'config param', 'MAIL_APIKEY_PUBLIC', MAIL_APIKEY_PUBLIC, **_process_call_area)
    log_process_parameter('', 'config param', 'MAIL_APIKEY_PRIVATE', MAIL_APIKEY_PRIVATE, **_process_call_area)

    try:
        msg='start sending email thru sendgrid'
        log_process_message('', '', msg,**_process_call_area)

        # mail = smtplib.SMTP(MAIL_SERVER, MAIL_PORT)
        # mail.ehlo()
        # mail.starttls()
        # mail.login(MAIL_USERNAME, MAIL_PASSWORD)
        # mail.sendmail(From, To, msg.as_string())
        # mail.quit()

        #echo "export SENDGRID_API_KEY='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'" > sendgrid.env
        #echo "sendgrid.env" >> .gitignore
        #source ./sendgrid.env
        SENDGRID_API_KEY='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'
        sg = sendgrid.SendGridAPIClient(apikey=SENDGRID_API_KEY)
        From="noreply@ganimides.com"
        from_email = Email(From)
        To_email = Email(To)
        Subject = Subject
        content = Content("text/plain", "and easy To do anywhere, even with Python")
        mail = Mail(from_email, Subject, To_email, content)
        response = sg.client.mail.send.post(request_body=mail.get())
        
        log_process_data('', 'response.status_code', response.status_code,**_process_call_area)
        log_process_data('', 'response.body', response.body,**_process_call_area)
        log_process_data('', 'response.headers', response.headers,**_process_call_area)

        msg='email sent thru sendgrid'
        log_process_message('', 'success', msg,**_process_call_area)
    except Exception as error_text:
        msg= f'sending email system error:{error_text}'
        log_process_message('', 'error', msg,**_process_call_area)
        api_result = {'api_status': 'error', 'api_message': msg}
        log_process_finish(_process_msgID, api_result, **_process_call_area)    
        return api_result

    msg= f'email send To [{To}] with Subject [[{Subject}]]'
    api_result = {'api_status': 'success', 'api_message': msg}
    log_process_finish(_process_msgID, api_result, **_process_call_area)    
    return api_result
#:::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
#:::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
#:::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
def sendEmail_thru_mailjet_api(From, To, Cc, Bcc, Subject, text_body, html_body, attachments=[], caller_area={}):
    """
    sendEmail_thru_mailjet_api
    """
    _process_name = 'sendEmail_thru_mailjet_api'
    _process_entity = 'email'
    _process_action = 'send_email'
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
    log_process_input('', 'Subject', Subject, **_process_call_area)
    log_process_input('', 'text_body', text_body, **_process_call_area)
    log_process_input('', 'html_body', html_body, **_process_call_area)
    log_process_input('', 'attachments', attachments, **_process_call_area)
    log_process_input('', 'caller_area', caller_area, **_process_call_area)


    MAIL_APIKEY_PUBLIC = thisApp.application_configuration.get('MAIL_APIKEY_PUBLIC')
    MAIL_APIKEY_PRIVATE = thisApp.application_configuration.get('MAIL_APIKEY_PRIVATE')

    log_process_parameter('', 'config param', 'MAIL_APIKEY_PUBLIC', MAIL_APIKEY_PUBLIC, **_process_call_area)
    log_process_parameter('', 'config param', 'MAIL_APIKEY_PRIVATE', MAIL_APIKEY_PRIVATE, **_process_call_area)

    msg='start sending email thru mailjet_api'
    log_process_message('', '', msg,**_process_call_area)
    try:
        #mailjet = Client(auth=(api_key, api_secret), version='v1.3.0')
        mailjet = Client(auth=(MAIL_APIKEY_PUBLIC, MAIL_APIKEY_PRIVATE))
        msg=f'mailjet_api CONNECT OK'
        log_process_message('', 'success', msg,**_process_call_area)
    except Exception as error_text:
        msg = f'mailjet_api ERROR api authorization failed: {error_text}'
        log_process_message('', 'error', msg,**_process_call_area)
        api_result = {'api_status': 'error', 'api_message': msg}
        log_process_finish(_process_msgID, api_result, **_process_call_area)    
        return api_result

    data1 = {
        'FromEmail': 'your sender email'
        ,'Subject': 'Hello Mailjet!'
        ,'Text-Part': 'Welcome Onboard'
        ,'Recipients': [{'Email': 'recipient email'}]
    }

    data = {
          'Messages': [
        	{
        		"From": {
        			"Email": From,
        			"Name": "Mailjet Pilot"
        		},
        		"To": [
        			{
        			"Email": To,
        			"Name": "passenger"
        			}
        		],
        		"Subject": Subject,
        		"TemplateLanguage": True,
        		"TextPart": "Dear {{data:firstname:\"passenger\"}}, welcome To Mailjet! ",
        		"HTMLPart": "Dear {{data:firstname:\"passenger\"}}, welcome To Mailjet!"
        	}
        ]
    }

    # print('   sendEmail_thru_mailjet_api DATA=',data)
        # msg='start sending email thru sendgrid'
    log_process_data('', 'email_data', data,**_process_call_area)

    try:
        result = mailjet.send.create(data=data)
        log_process_data('', 'result.status_code', result.status_code,**_process_call_area)
        log_process_data('', 'result.json', str(result.json()),**_process_call_area)

        msg='email sent thru mailjet_api'
        log_process_message('', 'success', msg, **_process_call_area)
    except Exception as error_text:
        msg = f'send email thru mailjet_api system error: {error_text}'
        log_process_message('', 'error', msg,**_process_call_area)
        api_result = {'api_status': 'error', 'api_message': msg}
        log_process_finish(_process_msgID, api_result, **_process_call_area)    
        return api_result

    msg= f'email send To [{To}] with Subject [[{Subject}]]'
    api_result = {'api_status': 'success', 'api_message': msg}
    log_process_finish(_process_msgID, api_result, **_process_call_area)    
    return api_result
#:::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
#:::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
#:::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
def MIME_email_message(From, To, Cc, Bcc, Subject, text_body, html_body, caller_area={}):
    # Create message container - the correct MIME type is multipart/alternative.
    _process_name = 'MIME_email_message'
    _process_entity = 'email'
    _process_action = 'format_email'
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
    log_process_input('', 'Subject', Subject, **_process_call_area)
    log_process_input('', 'text_body', text_body, **_process_call_area)
    log_process_input('', 'html_body', html_body, **_process_call_area)
    log_process_input('', 'caller_area', caller_area, **_process_call_area)

    MIME_msg = MIMEMultipart('alternative')
    MIME_msg['Subject'] = Subject
    MIME_msg['From'] = From
    MIME_msg['To'] = To
    MIME_msg['Cc'] = Cc
    MIME_msg['Bcc'] = Bcc

    # Attach parts inTo message container.
    # According To RFC 2046, the last part of a multipart message, in this case
    # the HTML message, is best and preferred.

    # Record the MIME types of both parts - text/plain and text/html.
    if text_body:
        part1 = MIMEText(text_body, 'plain')
        MIME_msg.attach(part1)

    if html_body:
        part2 = MIMEText(html_body, 'html','utf8')
        MIME_msg.attach(part2)

    msg= f'OK. email formatted according To MIME'
    log_process_message('', 'success', msg,**_process_call_area)
    api_result = {'api_status': 'success', 'api_message': msg,'api_data':MIME_msg}
    api_result = {'api_status': 'success', 'api_message': msg}
    log_process_finish(_process_msgID, api_result, **_process_call_area)
    
    return MIME_msg
#:::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
#:::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
#:::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
#::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
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
    print(__file__)
    client = {'name': 'PHILIPPOS', 'mobile': '+35799359864'}
    print(string_translate('hello #NAME#, Today is #TODAY#', client))
    print(send_email(From='noreply@leandrou.com', To='philippos.leandrou@gmail.com', Subject='#NAME# test from gani', text_body='hello #NAME#, Today is #TODAY#', data_record=client, caller_area={'debug_level': 99}))
    print(send_email(From='noreply@leandrou.com',To='philippos.leandrou@gmail.com', Subject='hi #MOBILE#, this is a test from gani', text_body='hello #NAME#, Today is #TODAY#', data_record=client, caller_area={'debug_level': 0}))
    print(send_outlook_email(To='philippos.leandrou@gmail.com', Subject='#NAME# test from gani', text_body='hello #NAME#, Today is #TODAY#', data_record=client, caller_area={'debug_level': 99}))
