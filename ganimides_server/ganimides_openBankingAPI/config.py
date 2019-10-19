import os
import sys
if not (os.path.dirname(__file__) in sys.path): sys.path.append(os.path.dirname(__file__))
import configparser

module_id = os.path.splitext(os.path.basename(__file__))[0]
module_version = 1
module_folder = os.path.dirname(__file__)

from colorama import Fore as colors,init as ColorsInit,Back as bgcolors
ColorsInit(convert=True)
########################################################################
########################################################################
########################################################################
database_debug = False
database_engine_debug = False
database_models_debug = False
database_session_debug = False
database_tables_debug = False
database_admin_debug = False
database_commands_echo = False
database_api_debug = 99
database_schema_silent_loading = True
openbanking_api_debug = True
########################################################################
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
    elif config_parser.has_section('DEFAULT') :
        if not config_parser.has_section('APPLICATION'):
            DEBUG_ON = config_parser.getboolean('APPLICATION', 'DEBUG')
            CONSOLE_ON = config_parser.getboolean('APPLICATION', 'CONSOLE')
            FILELOG_ON = config_parser.getboolean('APPLICATION', 'FILELOG')
        environment = config_parser.get('DEFAULT', 'ENVIRONEMNT').lower()
        if not environment:
            environment = 'production'
        EXECUTION_MODE = environment
        msg0 = f'{colors.RED}o{colors.RESET} {colors.LIGHTBLACK_EX}{module_id}:{colors.YELLOW}EXECUTION_MODE{colors.LIGHTBLACK_EX} set to {colors.LIGHTWHITE_EX}{EXECUTION_MODE}{colors.RESET}.'
else:
    environment = 'development'
    EXECUTION_MODE = environment
    msg0 = f'{colors.RED}o{colors.RESET} {colors.LIGHTBLACK_EX}{module_id}:{colors.YELLOW}EXECUTION_MODE{colors.LIGHTBLACK_EX} set to {colors.LIGHTWHITE_EX}{EXECUTION_MODE}{colors.LIGHTBLACK_EX}.(device.ini or server.ini or environment.ini not located){colors.RESET}'

appIniFile = 'application.ini'
if os.path.isfile(appIniFile):
    with open(appIniFile, 'r') as f:
        config_string = '[dummy_section]\n' + f.read()
    config = configparser.ConfigParser()
    config_parser.read_string(config_string)    
    DEBUG_ON = config_parser.getboolean('dummy_section', 'DEBUG')
    CONSOLE_ON = config_parser.getboolean('dummy_section', 'CONSOLE')
    FILELOG_ON = config_parser.getboolean('dummy_section', 'FILELOG')
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
########################################################################
def print_config_param(what, value):
    if type(value) == type(True):
        if value:
            vcolor = colors.LIGHTGREEN_EX
        else:
            vcolor = colors.LIGHTBLACK_EX
    else:
        vcolor = colors.MAGENTA            
    print(f"{colors.RED}{module_id}{colors.LIGHTBLACK_EX} {colors.YELLOW}{what}{colors.RESET} = {vcolor}{value}{colors.RESET}")
########################################################################
module_folder_short=module_folder
if len(module_folder_short) > 50:
    module_folder_short='...'+module_folder[-47:]
msg = f'{colors.RED}{module_id}{colors.LIGHTBLACK_EX} {colors.GREEN}V{module_version}{colors.LIGHTBLACK_EX} loaded from {colors.CYAN}{module_folder_short}{colors.RESET}{bgcolors.RESET}'
if CONSOLE_ON:
    print(msg)
    print_config_param('database_session_debug', database_session_debug)
    print_config_param('database_engine_debug', database_engine_debug)
    print_config_param('database_debug', database_debug)
    print_config_param('database_models_debug', database_models_debug)
    print_config_param('database_tables_debug', database_tables_debug)
    print_config_param('database_admin_debug', database_admin_debug)
    print_config_param('database_commands_echo', database_commands_echo)
    print_config_param('openbanking_api_debug', openbanking_api_debug)
    print_config_param('database_api_debug', database_api_debug)
    print_config_param('environment', environment)
    print_config_param('EXECUTION_MODE', EXECUTION_MODE)
    print_config_param('CONSOLE_ON', CONSOLE_ON)
    print_config_param('FILELOG_ON', FILELOG_ON)
    print_config_param('DEBUG_ON', DEBUG_ON)
