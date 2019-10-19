import os
import sys
import datetime
module_ProgramName = os.path.splitext(os.path.basename(__file__))[0]
module_id = '{}'.format(module_ProgramName)
module_version = 0.1
from _appEnvironment import application_configuration
# from _debugServices import master_configuration as debug_templates
from _colorServices import colorized_string,Fore
from _processServices import build_process_signature, build_process_call_area
from _logProcessServices import log_process_start, log_process_finish, log_process_message,log_process_parameter
from _debugServices import get_debug_level, get_debug_files
#::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
#::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
#::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
#globals
#::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
#::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
#::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
caller_area={'debug_level':99}
_process_name = module_id
_process_entity = ''
_process_action = 'confing'
_process_msgID = f'process:[{module_id}]'
_process_identity_kwargs = {'type': 'process', 'module': module_id, 'name': _process_name, 'action': _process_action, 'entity': _process_entity, 'msgID': _process_msgID,}
_process_adapters_kwargs = {'dbsession': None}
_process_log_kwargs = {'indent_method': 'AUTO', 'indent_level': None}
_process_debug_level = get_debug_level(caller_area.get('debug_level'), **_process_identity_kwargs, **_process_adapters_kwargs)
_process_debug_files = get_debug_files(_process_debug_level, **_process_identity_kwargs, **_process_adapters_kwargs)
_process_debug_kwargs={'debug_level':_process_debug_level,'debug_files':_process_debug_files}

_process_signature = build_process_signature(**_process_identity_kwargs, **_process_adapters_kwargs, **_process_debug_kwargs, **_process_log_kwargs)
_process_call_area = build_process_call_area(_process_signature, caller_area)
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 
log_process_start(_process_msgID,**_process_call_area)
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 
MAIL_SERVER_PROVIDER = os.environ.get('MAIL_SERVER_PROVIDER', 'GOOGLE')
log_process_parameter('', '', 'MAIL_SERVER_PROVIDER', MAIL_SERVER_PROVIDER, **_process_call_area)
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 
################################################################
### mail servers
################################################################
MAILJET_MAIL_SERVER = 'in-v3.mailjet.com'
MAILJET_MAIL_PORT = '587' # Port 25 or 587 (some providers block port 25). If TLS on port 587 doesn't work, try using port 465 and/or using SSL instead
MAILJET_MAIL_USE_TLS = 'True'
MAILJET_MAIL_USE_SSL = 'True'
MAILJET_MAIL_USERNAME = 'f8d33207c3c7a1ecaf2f74e809b57786'
MAILJET_MAIL_PASSWORD = '2d6a3c2de41ff45b5435382f3e267580'
MAILJET_MAIL_APIKEY_PUBLIC ='f8d33207c3c7a1ecaf2f74e809b57786'
MAILJET_MAIL_APIKEY_PRIVATE ='2d6a3c2de41ff45b5435382f3e267580'

YANDEX_MAIL_SERVER = "smtp.yandex.ru"
YANDEX_MAIL_PORT = '587'
YANDEX_MAIL_USE_TLS = 'True'
YANDEX_MAIL_USE_SSL = 'True'
YANDEX_MAIL_USERNAME = '...' #without the @yandex.ru
YANDEX_MAIL_PASSWORD = '***'
YANDEX_MAIL_APIKEY_PUBLIC = '...'
YANDEX_MAIL_APIKEY_PRIVATE = '...'

GOOGLE_MAIL_SERVER = "smtp.gmail.com"
GOOGLE_MAIL_PORT = '587'
GOOGLE_MAIL_USE_TLS = 'False'
GOOGLE_MAIL_USE_SSL = 'True'
GOOGLE_MAIL_USERNAME = 'akamas2020@gmail.com'
GOOGLE_MAIL_PASSWORD = 'philea13'
GOOGLE_MAIL_USERNAME = 'bstarr131@gmail.com'
GOOGLE_MAIL_PASSWORD = 'bstarr13'
GOOGLE_MAIL_USERNAME = 'spithas@leandrou.com'
GOOGLE_MAIL_PASSWORD = 'spithas3116'
GOOGLE_MAIL_APIKEY_PUBLIC = '...'
GOOGLE_MAIL_APIKEY_PRIVATE = '...'

if MAIL_SERVER_PROVIDER == 'MAILJET':
    MAIL_SERVER = MAILJET_MAIL_SERVER
    MAIL_PORT = MAILJET_MAIL_PORT
    MAIL_USE_TLS = MAILJET_MAIL_USE_TLS
    MAIL_USE_SSL = MAILJET_MAIL_USE_SSL
    MAIL_USERNAME = MAILJET_MAIL_USERNAME
    MAIL_PASSWORD = MAILJET_MAIL_PASSWORD
    MAIL_APIKEY_PUBLIC = MAILJET_MAIL_APIKEY_PUBLIC
    MAIL_APIKEY_PRIVATE = MAILJET_MAIL_APIKEY_PRIVATE
else:
    if MAIL_SERVER_PROVIDER == 'YANDEX':
        MAIL_SERVER = YANDEX_MAIL_SERVER
        MAIL_PORT = YANDEX_MAIL_PORT
        MAIL_USE_TLS = YANDEX_MAIL_USE_TLS
        MAIL_USE_SSL = YANDEX_MAIL_USE_SSL
        MAIL_USERNAME = YANDEX_MAIL_USERNAME
        MAIL_PASSWORD = YANDEX_MAIL_PASSWORD
        MAIL_APIKEY_PUBLIC = YANDEX_MAIL_APIKEY_PUBLIC
        MAIL_APIKEY_PRIVATE = YANDEX_MAIL_APIKEY_PRIVATE
    else:
        MAIL_SERVER = GOOGLE_MAIL_SERVER
        MAIL_PORT = GOOGLE_MAIL_PORT
        MAIL_USE_TLS = GOOGLE_MAIL_USE_TLS
        MAIL_USE_SSL = GOOGLE_MAIL_USE_SSL
        MAIL_USERNAME = GOOGLE_MAIL_USERNAME
        MAIL_PASSWORD = GOOGLE_MAIL_PASSWORD
        MAIL_APIKEY_PUBLIC = GOOGLE_MAIL_APIKEY_PUBLIC
        MAIL_APIKEY_PRIVATE = GOOGLE_MAIL_APIKEY_PRIVATE
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 
application_configuration.update({'MAIL_SERVER': MAIL_SERVER})
application_configuration.update({'MAIL_PORT': MAIL_PORT})
application_configuration.update({'MAIL_USE_TLS': MAIL_USE_TLS})
application_configuration.update({'MAIL_USE_SSL': MAIL_USE_SSL})
application_configuration.update({'MAIL_USERNAME': MAIL_USERNAME})
application_configuration.update({'MAIL_PASSWORD': MAIL_PASSWORD})
application_configuration.update({'MAIL_APIKEY_PUBLIC': MAIL_APIKEY_PUBLIC})
application_configuration.update({'MAIL_APIKEY_PRIVATE': MAIL_APIKEY_PRIVATE})
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 
log_process_parameter('', '', 'MAIL_SERVER', MAIL_SERVER, **_process_call_area)
log_process_parameter('', '', 'MAIL_PORT', MAIL_PORT, **_process_call_area)
log_process_parameter('', '', 'MAIL_USE_TLS', MAIL_USE_TLS, **_process_call_area)
log_process_parameter('', '', 'MAIL_USE_SSL', MAIL_USE_SSL, **_process_call_area)
log_process_parameter('', '', 'MAIL_USERNAME', MAIL_USERNAME, **_process_call_area)
log_process_parameter('', '', 'MAIL_PASSWORD', MAIL_PASSWORD, **_process_call_area)
log_process_parameter('', '', 'MAIL_APIKEY_PUBLIC', MAIL_APIKEY_PUBLIC, **_process_call_area)
log_process_parameter('', '', 'MAIL_APIKEY_PRIVATE', MAIL_APIKEY_PRIVATE, **_process_call_area)
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 
log_process_finish(_process_msgID,{},**_process_call_area)
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 