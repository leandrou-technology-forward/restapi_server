import os
import sys

if not (os.path.dirname(os.path.dirname(__file__)) in sys.path): sys.path.append(os.path.dirname(os.path.dirname(__file__)))
if not (os.path.dirname(__file__) in sys.path): sys.path.append(os.path.dirname(__file__))
try:
    import config
except:
    pass

import datetime
import configparser
import subprocess
import inspect
import colorama
from colorama import Fore, Back, Style
from pprint import pprint
from types import FunctionType
#::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
#::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
#::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
#module
#::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
#::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
#::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
colorama.init()
colorama.init(autoreset=True)
module_Function = 'general application services'
module_ProgramName = '_appEnvironment'
module_BaseTimeStamp = datetime.datetime.now()
module_folder = os.getcwd()
module_color = Fore.YELLOW
module_folder = os.path.dirname(__file__)
module_ProgramName = os.path.splitext(os.path.basename(__file__))[0]
module_id = f'{module_ProgramName}'
module_eyecatch = module_ProgramName
module_version = 0.1
module_log_file_name = module_ProgramName+'.log'
module_errors_file_name = os.path.splitext(os.path.basename(module_log_file_name))[0]+'_errors.log'
module_versionString = f'{module_id} version {module_version}'
module_file = __file__
module_configFile = module_ProgramName + '.cfg'
module_is_externally_configurable = True
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
    'module_errors_file_name':module_errors_file_name,
    'module_is_externally_configurable':module_is_externally_configurable,
}
master_configuration = {
}
#::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
#::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
#::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
#::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
# globals
#::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
#::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
#::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
# constants_dictionary = {}
ON = True
OFF = False
DEFAULT = None
fileLogON = True
fileLogOFF = False
fileLogDEFAULT = None
consoleOutputON = True
consoleOutputOFF = False
consoleOutputDEFAULT = None
ignoreWarningsON = True
ignoreWarningsOFF = False
ignoreWarningsDEFAULT = None
logServicesConfigFile=''

global_log_current_prefix=''

CONSOLE_ON = True
FILELOG_ON = False

EXECUTION_MODE = 'DEV'
ENVIRONMENT = 'DEV'
MAIL_SERVER_PROVIDER=''
MAIL_SENDER =''
# this_ini_file_name = 'server.ini'
# ini_file = find_file(this_ini_file_name, search_Downwards=1, search_Upwards=2, search_SubFolders=False)
config_parser = configparser.ConfigParser()
#DeviceIniFile = find_file('device.ini', search_Downwards=1, search_Upwards=0, search_SubFolders=False)
DeviceIniFile = 'device.ini'
if not os.path.isfile(DeviceIniFile):
    #DeviceIniFile = find_file('server.ini', search_Downwards=1, search_Upwards=0, search_SubFolders=False)
    DeviceIniFile = 'server.ini'
if not os.path.isfile(DeviceIniFile):
    #DeviceIniFile = find_file('environment.ini', search_Downwards=1, search_Upwards=0, search_SubFolders=False)
    DeviceIniFile = 'environment.ini'

if os.path.isfile(DeviceIniFile):
    config_parser.read(DeviceIniFile)
    if config_parser.has_section('APPLICATION') :
        DEBUG_ON = config_parser.getboolean('APPLICATION', 'DEBUG')
        CONSOLE_ON = config_parser.getboolean('APPLICATION', 'CONSOLE')
        FILELOG_ON = config_parser.getboolean('APPLICATION', 'FILELOG')
        MAIL_SERVER_PROVIDER = config_parser.get('APPLICATION', 'MAIL_SERVER_PROVIDER')
    elif config_parser.has_section('DEFAULT') :
        if not config_parser.has_section('APPLICATION'):
            DEBUG_ON = config_parser.getboolean('DEFAULT', 'DEBUG')
            CONSOLE_ON = config_parser.getboolean('DEFAULT', 'CONSOLE')
            FILELOG_ON = config_parser.getboolean('DEFAULT', 'FILELOG')
            MAIL_SERVER_PROVIDER = config_parser.get('DEFAULT', 'MAIL_SERVER_PROVIDER')
        environment = config_parser.get('DEFAULT', 'ENVIRONEMNT').lower()
        if not environment:
            environment = 'production'
        EXECUTION_MODE = environment
        msg0 = f'{Fore.RED}o{Fore.RESET} {Fore.LIGHTBLACK_EX}{module_id}:{Fore.YELLOW}EXECUTION_MODE{Fore.LIGHTBLACK_EX} set to {Fore.LIGHTWHITE_EX}{EXECUTION_MODE}{Fore.RESET}.'
else:
    environment = 'development'
    EXECUTION_MODE = environment
    msg0 = f'{Fore.RED}o{Fore.RESET} {Fore.LIGHTBLACK_EX}{module_id}:{Fore.YELLOW}EXECUTION_MODE{Fore.LIGHTBLACK_EX} set to {Fore.LIGHTWHITE_EX}{EXECUTION_MODE}{Fore.LIGHTBLACK_EX}.(device.ini or server.ini or environment.ini not located){Fore.RESET}'

appIniFile = 'application.ini'
if os.path.isfile(appIniFile):
    with open(appIniFile, 'r') as f:
        config_string = '[dummy_section]\n' + f.read()
    config_parser = configparser.ConfigParser()
    config_parser.read_string(config_string)    
    DEBUG_ON = config_parser.getboolean('dummy_section', 'DEBUG')
    CONSOLE_ON = config_parser.getboolean('dummy_section', 'CONSOLE')
    FILELOG_ON = config_parser.getboolean('dummy_section', 'FILELOG')
    MAIL_SERVER_PROVIDER = config_parser.get('dummy_section', 'MAIL_SERVER_PROVIDER',fallback=None)
    msg0x = '(from application.ini)'
else:
    msg0x = '(application.ini not located)'
    if EXECUTION_MODE.upper().find('DEV') >= 0 or EXECUTION_MODE.upper().find('SAND') >= 0:
        CONSOLE_ON = True
        FILELOG_ON = True
        DEBUG_ON = True

if EXECUTION_MODE.upper().find('PROD') >= 0:
        CONSOLE_ON = False
        DEBUG_ON = False
        FILELOG_ON = False

if CONSOLE_ON:
    msg1 = f'{Fore.RED}o{Fore.RESET} {Fore.LIGHTBLACK_EX}{module_id}:{Fore.YELLOW}DEBUG{Fore.LIGHTBLACK_EX} set to {Fore.LIGHTWHITE_EX}{DEBUG_ON}{Fore.RESET}. {msg0x}'
    msg2 = f'{Fore.RED}o{Fore.RESET} {Fore.LIGHTBLACK_EX}{module_id}:{Fore.YELLOW}CONSOLE{Fore.LIGHTBLACK_EX} set to {Fore.LIGHTWHITE_EX}{CONSOLE_ON}{Fore.RESET}. {msg0x}'
    msg3 = f'{Fore.RED}o{Fore.RESET} {Fore.LIGHTBLACK_EX}{module_id}:{Fore.YELLOW}FILELOG{Fore.LIGHTBLACK_EX} set to {Fore.LIGHTWHITE_EX}{FILELOG_ON}{Fore.RESET}. {msg0x}'
    if DEBUG_ON:
        print(msg0)
        print(msg1)
        print(msg2)
        print(msg3)

applicationID = None
application_title = None
application_name = None
application_configuration={}
client_configuration={}
client_config_file='app_client_config.cfg'
client_id = ''
client_secretKey = ''
machine_id = subprocess.check_output('wmic csproduct get uuid').decode().split('\n')[1].strip()
device_uid = machine_id
geolocation_lon = '12.123456'
geolocation_lat = '34.789012'
applicationID='dummy'
application_name=__package__
application_title=__name__
user_id = ''
user_is_loggedin = False
log_file_name = module_ProgramName+'.log'
log_errors_file_name = os.path.splitext(os.path.basename(log_file_name))[0]+'_errors.log'

application_configuration.update({'applicationID': applicationID})
application_configuration.update({'application_title': application_title})
application_configuration.update({'application_name': application_name})
application_configuration.update({'client_configuration': client_configuration})
application_configuration.update({'client_config_file': client_config_file})
application_configuration.update({'client_id': client_id})
application_configuration.update({'client_secretKey': client_secretKey})
application_configuration.update({'machine_id': machine_id})
application_configuration.update({'device_uid': device_uid})
application_configuration.update({'geolocation_lon': geolocation_lon})
application_configuration.update({'geolocation_lat': geolocation_lat})
application_configuration.update({'log_file_name': log_file_name})
application_configuration.update({'log_errors_file_name': log_errors_file_name})
application_configuration.update({'logServicesConfigFile': logServicesConfigFile})

application_configuration.update({'EXECUTION_MODE': EXECUTION_MODE})
application_configuration.update({'CONSOLE_ON': CONSOLE_ON})
application_configuration.update({'FILELOG_ON': FILELOG_ON})
application_configuration.update({'environment': environment})
try:
    application_configuration.update({'database_session_debug': config.database_session_debug})
    application_configuration.update({'database_engine_debug': config.database_engine_debug})
    application_configuration.update({'database_debug': config.database_debug})
    application_configuration.update({'database_models_debug': config.database_models_debug})
    application_configuration.update({'database_tables_debug': config.database_tables_debug})
    application_configuration.update({'database_admin_debug': config.database_admin_debug})
    application_configuration.update({'database_commands_echo': config.database_commands_echo})
    application_configuration.update({'database_api_debug': config.database_api_debug})
    application_configuration.update({'openbanking_api_debug': config.openbanking_api_debug})
except:
    pass
#::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
#::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
#::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
# mail servers
#::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
#::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
#::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
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
#::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
if not MAIL_SERVER_PROVIDER:
    MAIL_SERVER_PROVIDER = os.environ.get('MAIL_SERVER_PROVIDER', 'GOOGLE')
#::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
if os.path.isfile(DeviceIniFile):
    config_parser.read(DeviceIniFile)
    if not config_parser.has_section(MAIL_SERVER_PROVIDER):
        MAIL_SERVER_PROVIDER = 'GOOGLE'
    if config_parser.has_section(MAIL_SERVER_PROVIDER) :
        MAIL_SERVER = config_parser.get(MAIL_SERVER_PROVIDER, 'MAIL_SERVER')
        MAIL_PORT = config_parser.get(MAIL_SERVER_PROVIDER, 'MAIL_PORT')
        MAIL_USE_TLS = config_parser.get(MAIL_SERVER_PROVIDER, 'MAIL_USE_TLS')
        MAIL_USE_SSL = config_parser.get(MAIL_SERVER_PROVIDER, 'MAIL_USE_SSL')
        MAIL_USERNAME = config_parser.get(MAIL_SERVER_PROVIDER, 'MAIL_USERNAME')
        MAIL_PASSWORD = config_parser.get(MAIL_SERVER_PROVIDER, 'MAIL_PASSWORD')
        MAIL_APIKEY_PUBLIC = config_parser.get(MAIL_SERVER_PROVIDER, 'MAIL_APIKEY_PUBLIC')
        MAIL_APIKEY_PRIVATE = config_parser.get(MAIL_SERVER_PROVIDER, 'MAIL_APIKEY_PRIVATE')
    else:
        MAIL_SERVER_PROVIDER = None
else:
    MAIL_SERVER_PROVIDER=None
#::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
if not MAIL_SERVER_PROVIDER:
    MAIL_SERVER_PROVIDER = os.environ.get('MAIL_SERVER_PROVIDER', 'GOOGLE')
#::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
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
if not MAIL_SERVER_PROVIDER:
    MAIL_SERVER_PROVIDER = 'GOOGLE'
    MAIL_SERVER = GOOGLE_MAIL_SERVER
    MAIL_PORT = GOOGLE_MAIL_PORT
    MAIL_USE_TLS = GOOGLE_MAIL_USE_TLS
    MAIL_USE_SSL = GOOGLE_MAIL_USE_SSL
    MAIL_USERNAME = GOOGLE_MAIL_USERNAME
    MAIL_PASSWORD = GOOGLE_MAIL_PASSWORD
    MAIL_APIKEY_PUBLIC = GOOGLE_MAIL_APIKEY_PUBLIC
    MAIL_APIKEY_PRIVATE = GOOGLE_MAIL_APIKEY_PRIVATE
#::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
msg = f'{Fore.RED}o{Fore.RESET} {Fore.LIGHTBLACK_EX}{module_id}:{Fore.YELLOW}MAIL_SERVER_PROVIDER{Fore.LIGHTBLACK_EX} set to {Fore.LIGHTWHITE_EX}{MAIL_SERVER_PROVIDER}{Fore.LIGHTBLACK_EX}'
if DEBUG_ON:
    print(msg)
#::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
application_configuration.update({'MAIL_SERVER_PROVIDER': MAIL_SERVER_PROVIDER})
application_configuration.update({'MAIL_SERVER': MAIL_SERVER})
application_configuration.update({'MAIL_PORT': MAIL_PORT})
application_configuration.update({'MAIL_USE_TLS': MAIL_USE_TLS})
application_configuration.update({'MAIL_USE_SSL': MAIL_USE_SSL})
application_configuration.update({'MAIL_USERNAME': MAIL_USERNAME})
application_configuration.update({'MAIL_PASSWORD': MAIL_PASSWORD})
application_configuration.update({'MAIL_APIKEY_PUBLIC': MAIL_APIKEY_PUBLIC})
application_configuration.update({'MAIL_APIKEY_PRIVATE': MAIL_APIKEY_PRIVATE})
#::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
#::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
#::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
# sms service providers
#::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
#::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
#::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
SMS_SERVER_PROVIDER = 'NEXMO'
application_configuration.update({'SMS_SERVER_PROVIDER': SMS_SERVER_PROVIDER})

SMS_SERVER_CYTA_URL = 'https://www.cyta.com.cy/cytamobilevodafone/dev/websmsapi/sendsms.aspx'
SMS_SERVER_CYTA_USERNAME = 'Philippos'
SMS_SERVER_CYTA_SECRETKEY = 'f69f0d4702814d1fa1768f397ce9b485'
SMS_SERVER_CYTA_SMS_SENDER = 'GanimidesT'
application_configuration.update({'SMS_SERVER_CYTA_URL': SMS_SERVER_CYTA_URL})
application_configuration.update({'SMS_SERVER_CYTA_USERNAME': SMS_SERVER_CYTA_USERNAME})
application_configuration.update({'SMS_SERVER_CYTA_SECRETKEY': SMS_SERVER_CYTA_SECRETKEY})
application_configuration.update({'SMS_SERVER_CYTA_SMS_SENDER': SMS_SERVER_CYTA_SMS_SENDER})

SMS_SERVER_NEXMO_API_KEY = '3ee5cdd5'
SMS_SERVER_NEXMO_API_SECRET = 'lgzsdgI4cP9eZl7J'
application_configuration.update({'SMS_SERVER_NEXMO_API_KEY': SMS_SERVER_NEXMO_API_KEY})
application_configuration.update({'SMS_SERVER_NEXMO_API_SECRET': SMS_SERVER_NEXMO_API_SECRET})

SMS_SERVER_SINCH_API_KEY = 'be0c283385204338815a88ae81add209'
SMS_SERVER_SINCH_API_SECRET = '1d5c5cab2725437bbd6d68298f78f7b3'
SMS_SERVER_SINCH_FROM_NUMBER = '35799599819'
application_configuration.update({'SMS_SERVER_SINCH_API_KEY': SMS_SERVER_SINCH_API_KEY})
application_configuration.update({'SMS_SERVER_SINCH_API_SECRET': SMS_SERVER_SINCH_API_SECRET})
application_configuration.update({'SMS_SERVER_SINCH_FROM_NUMBER': SMS_SERVER_SINCH_FROM_NUMBER})




#::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
#::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
#::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
#google recapcha

#::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
#::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
#::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
GOOGLE_RECAPTCHA_SITE_KEY = "6LcD3XkUAAAAABAoO2p4WOoBGg6uRyCoVCcGNCFV"
GOOGLE_RECAPTCHA_SECRET_KEY = "6LcD3XkUAAAAAHTNpV8RsDN8CybCNEJ0htRddCMq"
GOOGLE_RECAPTCHA_INVISIBLE_SITE_KEY = "6LfL2HkUAAAAAF8ot-2aPAHYzHPAAxvLtKI-PyXi"
GOOGLE_RECAPTCHA_INVISIBLE_SECRET_KEY = "6LfL2HkUAAAAAIdjgyCwgSaV2hvOS6APpoXot1yw"
#application_configuration.update({'GOOGLE_RECAPTCHA_SITE_KEY': GOOGLE_RECAPTCHA_SITE_KEY})
application_configuration.update({'RECAPTCHA_SITE_KEY': GOOGLE_RECAPTCHA_SITE_KEY})
application_configuration.update({'RECAPTCHA_PRIVATE_KEY': GOOGLE_RECAPTCHA_SECRET_KEY})
#application_configuration.update({'GOOGLE_RECAPTCHA_INVISIBLE_SITE_KEY': GOOGLE_RECAPTCHA_INVISIBLE_SITE_KEY})
#application_configuration.update({'GOOGLE_RECAPTCHA_INVISIBLE_SECRET_KEY': GOOGLE_RECAPTCHA_INVISIBLE_SECRET_KEY})
#::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
#::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
#::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
#services
#::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
#::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
#::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
def pair_application_configuration(paired_appl_configuration,paired_appl_identityDictionary):
    global applicationID
    global application_title
    global application_name
    global application_configuration
    global client_config_file
    global module_identityDictionary
    global client_id
    global client_secretKey
    global device_uid
    global machine_id
    
    thisApplication_name = application_name
    if not thisApplication_name:
        thisApplication_name='thisApp'
    
    #module_ProgramName = module_identityDictionary.get('module_ProgramName')
    module_color = module_identityDictionary.get('module_color')

    applicationID = None
    application_title = None
    application_name = None
    application_configuration_paired = None
    changed=False

    if paired_appl_configuration:
        for key in paired_appl_configuration:
            valnew = paired_appl_configuration.get('key','')
            valold = application_configuration.get('key', '')
            if valnew != valold:
                changed=True        
            application_configuration.update({key: paired_appl_configuration.get(key)})

    #copy this config from paired_appl_identityDictionary
    for key in paired_appl_identityDictionary:
        if key not in ('application_name','application_title','application_id','application_ProgramName'):
            valnew = paired_appl_identityDictionary.get('key','')
            valold = application_configuration.get('key', '')
            if valnew != valold:
                changed=True        
            application_configuration.update({key: paired_appl_identityDictionary.get(key)})

    paired_module_name = application_configuration.get('application_ProgramName', '?')
    if paired_module_name == '__init__':
        paired_module_name = paired_appl_identityDictionary.get('module_id', '?')
        
    application_Color = paired_appl_identityDictionary.get('module_color')

    if application_configuration.get('application_name'):
        application_name = application_configuration.get('application_name')
    if application_configuration.get('application_title'):
        application_title = application_configuration.get('application_title')
    if application_configuration.get('application_id'):
        applicationID = application_configuration.get('application_id')
    if application_configuration.get('ganimides_registered_application'):
        application_name = application_configuration.get('ganimides_registered_application')

    if application_name and paired_module_name: #and applicationID and application_title and
        application_configuration_paired = True
        msg = f'   {Fore.RED}o{Fore.RESET} {module_color}{thisApplication_name} {Fore.LIGHTBLACK_EX}application paired with {application_Color}{paired_module_name}{Fore.RESET}{Back.RESET}'
        if CONSOLE_ON:
            print(msg)
    else:
        msg = f'   {Fore.RED}o{Fore.RESET} {module_color}{thisApplication_name} {Fore.LIGHTBLACK_EX}application {Fore.RED}FAILED to paired{Fore.LIGHTBLACK_EX} with {application_Color}{paired_module_name}{Fore.RESET}{Back.RESET}'
        if CONSOLE_ON:
            print(msg)

    application_configuration.update({'machine_id': machine_id})
    application_configuration.update({'device_uid': device_uid})

    client_id = application_configuration.get('client_id','')
    client_secretKey = application_configuration.get('client_secretKey','')
    if CONSOLE_ON:
        msg=f'   {Fore.RED}o{Fore.LIGHTBLACK_EX} {Fore.YELLOW}{thisApplication_name}{Fore.LIGHTBLACK_EX}: client_id set to {Fore.CYAN}{client_id}{Fore.RESET}'
        print(msg)
        secretKeyStr=client_secretKey[0:20]+'...'
        msg=f'   {Fore.RED}o{Fore.LIGHTBLACK_EX} {Fore.YELLOW}{thisApplication_name}{Fore.LIGHTBLACK_EX}: client_secretKey set to {Fore.CYAN}{secretKeyStr}{Fore.RESET}'
        print(msg)
        msg=f'   {Fore.RED}o{Fore.LIGHTBLACK_EX} {Fore.YELLOW}{thisApplication_name}{Fore.LIGHTBLACK_EX}: device_uid set to {Fore.CYAN}{device_uid}{Fore.RESET}'
        print(msg)

    application_configuration.update({'application_configuration_paired': application_configuration_paired})
    application_configuration.update({'application_configuration_changed': changed})

    client_config_file = f'{applicationID}_client.cfg'
    application_configuration.update({'client_config_file': client_config_file})
    return application_configuration
#::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
#::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
def pair_module_configuration(config_key,paired_module_configuration):
    global application_configuration
    ix = 0
    if not config_key:
        config = {}
    elif config_key.upper() in ('ALL','*'):
        config = paired_module_configuration.copy()
    else:
        config = paired_module_configuration.get(config_key)
        if not type(config)==type({}):
            config = {}
    if config_key:
        if config_key.upper() not in ('ALL','*'):
            config = paired_module_configuration.get(config_key)
            if type(config)==type({}):
                if config_key not in application_configuration.keys():
                    application_configuration.update({config_key:{}})
                    for key in config:
                        if key:
                            v = application_configuration.get(key)
                            ix = ix + 1
                            application_configuration[config_key].update({key: v})
        else:
            config = paired_module_configuration.copy()
            if type(config)==type({}):
                for key in config:
                    if key:
                        v = application_configuration.get(key)
                        ix = ix + 1
                        application_configuration.update({key: v})
    if CONSOLE_ON:
        msg=f'   {Fore.RED}o{Fore.LIGHTBLACK_EX} {Fore.YELLOW}{config_key}{Fore.LIGHTBLACK_EX}: {Fore.BLUE}{ix} keys added to {Fore.CYAN}application configuration{Fore.RESET}'
        print(msg)
    return application_configuration
#::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
def collect_functions_from_module_globals(module_globals,functions_prefix=''):
    functions=[]
    current_globals = module_globals
    #pprint(current_globals)
    for k in list(current_globals):
        if k.upper().find(functions_prefix.upper()) >= 0:
            # print(k)
            v = current_globals.get(k)
            # print(v)
            # print(type(v))
            if inspect.isfunction(v):
                prog = k
                functions.append(prog)
    return functions
#############################################################################
def is_mod_function(mod, func):
    return inspect.isfunction(func) and inspect.getmodule(func) == mod
#############################################################################
def collect_function_names_from_module(moduleObj, functions_ids=[],exclude_functions_ids=[]):
    functions=[]
    #current_globals = moduleObj.globals()
    #pprint(current_globals)
    for k in list(moduleObj.__dict__):
        for id in map(str.upper, functions_ids):
            if k.upper().find(id) >= 0 or id in ('*', 'ALL'):
                ignore=False
                for exclude_id in map(str.upper, exclude_functions_ids):
                    if k.upper().find(exclude_id) >= 0:
                        ignore = True
                        break
                if not ignore:
                    obj = moduleObj.__dict__.get(k)
                    if inspect.isfunction(obj):
                        if is_mod_function(moduleObj, obj):
                            prog = k
                            functions.append(prog)
    return functions
#############################################################################
def collect_function_objects_from_module(moduleObj, functions_ids=[]):
    function_objects={}
    for k in list(moduleObj.__dict__):
        for id in map(str.upper, functions_ids):
            if k.upper().find(id)>=0 or id in ('*','ALL'):
                # print(k)
                obj = moduleObj.__dict__.get(k)
                if inspect.isfunction(obj):
                    if is_mod_function(moduleObj, obj):
                        function = k
                        function_objects.update({function:obj})
    return function_objects
#############################################################################
def collect_method_names_from_class(classObj, methods_ids=[],exclude_methods_ids=[]):
    methods = []
    xmethods= [x for x, y in classObj.__dict__.items() if type(y) == FunctionType]
    for m in xmethods:
        for id in map(str.upper, methods_ids):
            if m.upper().find(id) >= 0 or id in ('*', 'ALL'):
                if not m == '__init__':
                    ignore=False
                    for exclude_id in map(str.upper, exclude_methods_ids):
                        if m.upper().find(exclude_id) >= 0:
                            ignore = True
                            break
                    if not ignore:
                        methods.append(m)
    # #methods(Foo)  # ['bar', 'baz']    
    # current_globals = inspect.getmembers(classObj)
    # #pprint(current_globals)
    # for t in current_globals:
    #     k = t[0]
    #     v = t[1]
    #     for id in map(str.upper, methods_ids):
    #         if k.upper().find(id)>=0 or id in ('*','ALL'):
    #             print(k)
    #             # print(v)
    #             # print(type(v))
    #             if inspect.ismethod(v):
    #                 prog = k
    #                 methods.append(prog)
    return methods
#############################################################################
def collect_method_objects_from_class(classObj, methods_ids=[]):
    method_objects={}
    current_globals = inspect.getmembers(classObj)
    for t in current_globals:
        k = t[0]
        obj = t[1]
        for id in map(str.upper, methods_ids):
            if k.upper().find(id)>=0 or id in ('*','ALL'):
                # print(k)
                if inspect.ismethod(obj):
                    method = k
                    method_objects.update({method:obj})
    return method_objects
#############################################################################
def whoami1():
    return inspect.stack()[1][3]
#############################################################################
def whoami():
    return inspect.stack()[2][3]
#############################################################################
def whosdaddy():
    return inspect.stack()[3][3]
#############################################################################
def execute_external_program(current_globals, what):
    external_module_file=current_globals.get('__file__')
    external_module = os.path.splitext(os.path.basename(external_module_file))[0]
    for k in list(current_globals):
        if k.upper()==what.upper():
            v = current_globals.get(k)
            if inspect.isfunction(v):
                prog = k
                msg=f'   {Fore.RED}o{Fore.RESET} {Fore.WHITE}executing function [{Fore.CYAN}{prog}{Fore.RESET}] from module [{module_color}{external_module}{Fore.RESET}]{Fore.RESET}'
                if CONSOLE_ON:
                    print(msg)
                try:
                    current_globals[prog]()
                except Exception as e:
                    msg=f'   {Fore.RED}o{Fore.RESET} {Fore.WHITE}execution of [{Fore.CYAN}{prog}{Fore.RESET}] from module [{module_color}{external_module}{Fore.RESET}] failed with error: {Fore.RED}{e}{Fore.RESET}'
                    if CONSOLE_ON:
                        print(msg)
                    pass
#############################################################################
def set_debug_on():
    global DEBUG_ON
    DEBUG_ON=True
def set_debug_off():
    global DEBUG_ON
    DEBUG_ON = False
def set_console_on():
    global CONSOLE_ON
    CONSOLE_ON=True
def set_console_off():
    global CONSOLE_ON
    CONSOLE_ON = False
def set_filelog_on():
    global FILELOG_ON
    FILELOG_ON=True
def set_filelog_off():
    global FILELOG_ON
    FILELOG_ON = False
#::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
#::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
#::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
#::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
# module inititialization
#::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
#::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
#::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
module_Config_Initialized = True
msg = f'{Style.RESET_ALL}{Fore.LIGHTBLACK_EX}module {Fore.YELLOW}{module_id}{Fore.RESET} {Fore.CYAN}version {module_version}{Fore.LIGHTBLACK_EX} loaded.{Fore.RESET}'
if CONSOLE_ON:
    print(msg)
    #print('')
else:
    print(msg)
    #print('')
#::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
#::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
#::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
# main (for testing)
#::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
#::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
#::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
if __name__ == '__main__':
    print(__file__)
    print(application_configuration)
