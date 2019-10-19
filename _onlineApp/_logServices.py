import os
import sys
if not (os.path.dirname(__file__) in sys.path): sys.path.append(os.path.dirname(__file__))

import datetime
import shutil
import inspect
import configparser
import json
from glob import iglob
from dateutil.relativedelta import relativedelta
from dateutil.parser import parse
from _colorServices import apply_colors, colorized_string, Fore, Back, Style, default_colors_template, colors_template_result, colors_template_changes
from _colorServices import get_back_color_based_onForeground,get_fore_color_based_onBackground
# import colorama
# from colorama import Fore, Back, Style
# if sys.stdout.isatty():
#     colorama.init(autoreset=True)
# else:
#     # We're being piped, so skip colors
#     colorama.init(strip=True) 

import _appEnvironment as thisApp
import _debugServices
#::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
#::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
#::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
#module
#::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
#::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
#::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
module_Function = 'log services'
module_ProgramName = '_logServices'
module_BaseTimeStamp = datetime.datetime.now()
module_folder = os.getcwd()
module_color = Fore.LIGHTBLACK_EX
module_folder = os.path.dirname(__file__)
module_ProgramName = os.path.splitext(os.path.basename(__file__))[0]
module_id = f'{module_ProgramName}'
module_eyecatch = module_ProgramName
module_version = 0.1
module_log_file_name = module_ProgramName+'.log'
module_errors_file_name = os.path.splitext(os.path.basename(module_log_file_name))[0]+'_errors.log'
module_versionString = f'{module_id} version {module_version}'
module_file = __file__
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
}
master_configuration = {
}
#module config options
logServices_config_dictionary = {}
log_level = 0
log_indent_tab = '   '
log_eyecatch = module_ProgramName
log_current_prefix = ''
log_output_devices = 'FILE-PRINT-CONSOLE'
log_consolelog_enabled = thisApp.CONSOLE_ON
log_filelog_enabled = thisApp.FILELOG_ON
log_ignoreWarning = False
log_console_line_length = 99999
log_console_fix_line_length = 80
log_file_name = module_ProgramName+'.log'
log_errors_file_name = os.path.splitext(os.path.basename(log_file_name))[0]+'_errors.log'
log_force_log_warnings = True
log_force_print_warnings = False
log_force_log_errors = True
log_force_print_errors = False
log_force_log_system_errors = True
log_force_print_system_errors = False
log_indent_color = Fore.LIGHTYELLOW_EX
log_indent_bgcolor = ''
log_indent_char = 'o'
log_color_mode = 'COLOR'
config_version = 0
config_versionStr = ''
config_versionString = ''
logServicesConfigFile = thisApp.logServicesConfigFile
logServices_config_dictionary = {
    'log_file_name' : log_file_name,
    'log_errors_file_name' : log_errors_file_name,
    'log_output_devices' : log_output_devices,
    'log_consolelog_enabled' : log_consolelog_enabled,
    'log_filelog_enabled' : log_filelog_enabled,
    'log_ignoreWarning' : log_ignoreWarning,
    'log_console_fix_line_length':log_console_fix_line_length,
    'log_console_line_length' : log_console_line_length,
    'log_force_print_warnings' : log_force_print_warnings,
    'log_force_log_warnings' : log_force_log_warnings,
    'log_force_log_errors' : log_force_log_errors,
    'log_force_print_errors' : log_force_print_errors,
    'log_force_log_system_errors' : log_force_log_system_errors,
    'log_force_print_system_errors' : log_force_print_system_errors,
    'log_indent_color' : log_indent_color,
    'log_indent_bgcolor' : log_indent_bgcolor,
    'log_indent_char' : log_indent_char,
    'log_indent_tab' : log_indent_tab,
    'log_level': log_level,
    'logServicesConfigFile':logServicesConfigFile,
    'config_version': config_version,
    'config_versionStr': config_versionStr,
    'config_versionString': config_versionString,
    }
#::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
#::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
#::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
# globals
#::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
#::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
#::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
fore_colors = []
back_colors = []
color_names = []
fore_colors_dict = {}
back_colors_dict = {}
light_colors = []
dark_colors = []
fore_color_names_dict={}
back_color_names_dict={}
FgColor0 = Fore.LIGHTBLACK_EX
FgColor1 = Fore.YELLOW
FgColor2 = Fore.WHITE
FgColor3 = Fore.LIGHTBLUE_EX
FgColor4 = Fore.MAGENTA
FgColor5 = Fore.CYAN
FgColor6 = Fore.GREEN
FgColor7 = Fore.RED
FgColor8 = Fore.LIGHTWHITE_EX
FgColor9 = Fore.LIGHTBLUE_EX
# colors_array=[
#     ['#C0#',FgColor0],
#     ['#C1#',FgColor1],
#     ['#C2#',FgColor2],
#     ['#C3#',FgColor3],
#     ['#C4#',FgColor4],
#     ['#C5#',FgColor5],
#     ['#C6#',FgColor6],
#     ['#C7#',FgColor7],
#     ['#C8#',FgColor8],
#     ['#C9#',FgColor9],
#     ['#RED#',Fore.RED],
#     ['#GREEN#',Fore.GREEN],
#     ['#BLUE#',Fore.BLUE],
#     ['#WHITE#',Fore.WHITE],
#     ['#GRAY#',Fore.LIGHTBLACK_EX],
#     ['#MAGENTA#',Fore.MAGENTA],
#     ['#CYAN#',Fore.CYAN],
#     ['#ERROR#',Fore.RED],
#     ['#WARNING#',Fore.MAGENTA],
#     ['#OK#',Fore.GREEN],
#     ['#RESET#',Fore.RESET],
# ]
#::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
#::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
#::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
# services
#::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
#::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
#::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
def log_message(msg1='', msg2='', msg3='', msg4='', msg5='', msgType='INFO', msgOffset='AUTO', logFile='', logFileInit=False, msgColor='', msgBkgr='', output_devices='', print_enabled=None, filelog_enabled=None, ignoreWarning=None, msgCategory='', level=0):
    global log_file_name
    global log_current_prefix
    global log_output_devices
    global log_level
    global log_indent_tab
    global log_console_line_length
    global log_force_log_warnings
    global log_force_print_warnings
    global log_force_log_errors
    global log_force_print_errors
    global log_force_log_system_errors
    global log_force_print_system_errors
    global log_indent_color
    global log_indent_bgcolor
    global log_indent_char

    if msgCategory.upper().find('DEBUG') >= 0 and not thisApp.DEBUG_ON:
        return
    if print_enabled == None:
        print_enabled = thisApp.CONSOLE_ON
    if filelog_enabled == None:
        filelog_enabled = thisApp.FILELOG_ON
    if not filelog_enabled and not print_enabled:
        return

    if not (msgType.upper().find('START') >=0 or msgType.upper().find('FINISH') >= 0):
        if msgType.upper().find('WARN') >= 0:
            if log_force_log_warnings:
                filelog_enabled = True
            if log_force_print_warnings:
                print_enabled = True
        elif msgType.upper().find('ERROR') >= 0 and msgType.upper().find('SYS') >= 0:
            if log_force_log_errors:
                filelog_enabled = True
            if log_force_print_errors:
                print_enabled = True
        elif msgType.upper().find('ERROR') >= 0:
            if log_force_log_system_errors:
                filelog_enabled = True
            if log_force_print_system_errors:
                print_enabled = True

    if filelog_enabled:
        #do something only for log
        caller = sys._getframe(1)  # Obtain calling frame
        caller_module_name = caller.f_globals['__name__']
        #print(caller_module_name)
        caller_module_file = caller.f_globals['__file__']
        caller_module_ProgramName = os.path.splitext(os.path.basename(caller_module_file))[0]
        #print(caller_module_ProgramName)
        pass

    output_devices = get_logServices_OutputDevices(print_enabled=print_enabled, filelog_enabled=filelog_enabled, output_devices=output_devices, ignoreWarning=ignoreWarning)
   
    if msgType.upper().find('WARN') >= 0:
        ignoreWarningString = str(ignoreWarning)
        if ignoreWarningString.upper().find('INFO') >= 0:
            msgType = 'info'
        elif ignoreWarningString.upper().find('INFO-1') >= 0:
            msgType = 'info-1'
        elif ignoreWarningString.upper().find('INFO-1') >= 0:
            msgType = 'info-2'
        elif ignoreWarningString.upper().find('INFO-1') >= 0:
            msgType = 'info-3'

    
    if msgType.upper().find('START') >=0 or msgType.upper().find('FINISH') >= 0:
        msgOffset = 'AUTO'
    if not msgOffset:
        msgOffset = 'AUTO'

    if msgType.upper().find('FINISH') >= 0:
        ln = len(log_current_prefix) - 3
        if ln > 0:
            msgPrefix = log_current_prefix[:ln]
        else:
            msgPrefix = ''
        log_current_prefix = msgPrefix
        log_level = log_level - 1
        if log_level < 0:
            log_level = 0

    msg = '{} {} {} {} {}'.format(msg1, msg2, msg3, msg4, msg5)
    isEmpty = False
    if msg.strip() == '':
        isEmpty = True
    
    if msgType.upper().find('SPECIAL') >= 0:
        msg1 = msg
    else:
        if not (msgType.upper().find('START') >=0 or msgType.upper().find('FINISH') >= 0):
            if msgType.upper().find('WARN') >= 0:
                msg = 'warning: {} {} {} {} {}'.format(msg1, msg2, msg3, msg4, msg5)
            elif msgType.upper().find('ERROR') >= 0 and msgType.upper().find('SYS') >= 0:
                msg = 'system error: {} {} {} {} {}'.format(msg1, msg2, msg3, msg4, msg5)
            elif msgType.upper().find('ERROR') >= 0:
                msg = 'error: {} {} {} {} {}'.format(msg1, msg2, msg3, msg4, msg5)
        msg1 = msg.strip()

    msgPrefix = log_current_prefix
    if msgOffset.upper() == 'AUTO':
        msgPrefix = log_indent_tab*log_level
    elif msgOffset in ('+0', '0'):
        msgPrefix = log_current_prefix
    elif msgOffset == '+1':
        msgPrefix = f'{log_indent_tab}{log_current_prefix}'
    elif msgOffset == '-1':
        ln = len(log_current_prefix) - len(log_indent_tab)
        if ln > 0:
            msgPrefix = log_current_prefix[:ln]
        else:
            msgPrefix = ''

    if msgType.upper().find('SPECIAL') >= 0:
        msg = msg1
    else:
        msg = f'{msgPrefix}{msg1}'

    #for file log
    if filelog_enabled:
        msgF = f'{datetime.datetime.now()}|{caller_module_ProgramName}| {msg.strip()}\n'
        msgJson1 = f"dt:'{datetime.datetime.now()}'', module:'{caller_module_ProgramName}', msg='{msg.strip()}'"
        msgJson = '{'+msgJson1+'}\n'
    
    #for printing
    if not logFile:
        logFile = log_file_name
    if msgType.upper().find('SPECIAL') >= 0:
        msgP = msg
    else:
        msgP = msg1 #without prefix
        if len(msgP) > log_console_line_length:
            msgP = msgP[:log_console_line_length-3] + '...'
        
        #coloring
        if not msgColor:
            msgColor = get_logServices_MessageColor(msgType)
        msgP=apply_colors(msgP,msgColor)
        #background coloring
        if msgBkgr:
            msgP = '{}{}{}'.format(msgBkgr, msgP, Back.RESET)
        else:
            msgBkgr = get_logServices_MessageBgColor(msgType)
            if msgBkgr:
                msgP = '{}{}{}'.format(msgBkgr, msgP, Back.RESET)

        #for printing +1
        msgPrefix_print = msgPrefix
        if msgType.upper().find('INFO') >= 0 and not msgOffset:
           msgOffset == '+1'

        if msgOffset == '+1':
            msgPrefix_print = f'{log_indent_tab}{log_current_prefix}{log_indent_bgcolor}{log_indent_color}{log_indent_char}{Fore.RESET}{Back.RESET} '
        elif msgOffset == '+2':
            msgPrefix_print = f'{log_indent_tab}{log_indent_tab}{log_current_prefix}{log_indent_bgcolor}{log_indent_color}{log_indent_char}{Fore.RESET}{Back.RESET} '
        elif msgOffset == '+3':
            msgPrefix_print = f'{log_indent_tab}{log_indent_tab}{log_indent_tab}{log_current_prefix}{log_indent_bgcolor}{log_indent_color}{log_indent_char}{Fore.RESET}{Back.RESET} '
        elif msgOffset == '+0':
            msgPrefix_print = f'{log_current_prefix}{log_indent_bgcolor}{log_indent_color}{log_indent_char}{Fore.RESET}{Back.RESET} '

        #for debug
        #msgP = f'{xactive_moduleX}:{msgPrefix}{msgP}'
        #msgP = f'{xactive_moduleX}.{xcaller_prog}:{msgPrefix}{msgP}'

        msgP = f'{msgPrefix_print}{msgP}'
        #msgP = f'{logFile}:{msgP}'

    #log to logFile
    if option_enabled(output_devices, 'FILE'):
        if not logFile:
            logFile = log_file_name
        if logFileInit == True:
            try:
                os.remove(logFile)
            except:
                dummy = 1
        if not isEmpty:
            f = open(logFile, "a+")
            #f.write(msgF)
            f.write(msgJson)
            f.close

        if msgType.upper().find('ERROR') >= 0:
            errorsFile = log_errors_file_name
            if errorsFile:
                f = open(errorsFile, "a+")
                f.write(msgF)
                f.close

    #print or console write
    if not isEmpty:
        if option_enabled(output_devices, 'PRINT'):
            if not (msgType.upper().find('WARN') >= 0 and option_enabled(output_devices, 'IGNORE-WARNING')): #ignore warnings
                #print(msgP, log_level, msgOffset, msgType, logFile, xactive_moduleX)
                print(msgP + Fore.RESET + Back.RESET)
                if msgType.upper().find('FINISH') >= 0:
                    print('')

    #actions after print or log
    if msgType.upper().find('START') >=0:
        msgPrefix = log_current_prefix + log_indent_tab
        log_current_prefix = msgPrefix
        log_level = log_level + 1
    elif msgOffset not in ('+1'):
        log_current_prefix = msgPrefix

    #print(f'[{log_level}][{log_current_prefix}]')
    return log_level,log_current_prefix
#################################################################################################
def log_message_special(msg1='', msg2='', msg3='', msg4='', msg5='', msgType='', msgOffset='AUTO', logFile='', logFileInit=False, msgColor='', msgBkgr='', output_devices='', print_enabled='', filelog_enabled='', ignoreWarning='', caller_module='', caller_function='', colorB1=Back.WHITE, colorB2=Back.WHITE, colorF1=Fore.MAGENTA, colorF2=Fore.BLACK):
    global log_console_fix_line_length
    if log_console_fix_line_length < 120:
        log_console_fix_line_length=120
    #log_console_fix_line_length = _logServices.log_console_fix_line_length+40
    processid=f'{caller_module}.{caller_function}'
    msgLen = log_console_fix_line_length - len(processid)
    processString = f'{colorF1}{colorB1}{processid} {Back.RESET}{Fore.RESET}'
    if msgType.upper().find('ERROR') >= 0:
        colorF2 = Fore.RED
    elif msgType.upper().find('SUCCESS') >= 0:
        colorF2 = Fore.GREEN
    elif msgType.upper().find('OK') >= 0:
        colorF2 = Fore.GREEN
    msgLog=f'{msg1} {msg2} {msg3} {msg4} {msg5}'
    msgX=f'{msg1} {msg2} {msg3} {msg4} {msg5}'+' '*640
    msgF=msgX[:msgLen]
    msg = f'{processString}{colorF2}{colorB2}{msgF}{Back.RESET}{Fore.RESET}'
    log_message(msg,msgType='Special',filelog_enabled=False,print_enabled=True)
    log_message(msgLog,msgType='',filelog_enabled=True,print_enabled=False)
#################################################################################################
def log_message_wait(msg1='', msg2='', msg3='', msg4='', msg5='', msgType='', msgOffset='AUTO', logFile='', logFileInit=False, msgColor='', msgBkgr='', output_devices='', print_enabled='', filelog_enabled='', ignoreWarning='',caller_module='',caller_function=''):
    colorB1 = Back.LIGHTWHITE_EX
    colorB2 = Back.WHITE
    colorF1 = Fore.BLUE
    colorF2 = Fore.MAGENTA
    log_message_special(msg1=msg1, msg2=msg2, msg3=msg3, msg4=msg4, msg5=msg5, msgType=msgType, msgOffset=msgOffset, logFile=logFile, logFileInit=logFileInit, msgColor=msgColor, msgBkgr=msgBkgr, output_devices=output_devices, print_enabled=print_enabled, filelog_enabled=filelog_enabled, ignoreWarning=ignoreWarning, caller_module=caller_module, caller_function=caller_function,colorB1 = colorB1,colorB2 = colorB2,colorF1 = colorF1,colorF2 = colorF2)
#################################################################################################
def log_message_wait_success(msg1='', msg2='', msg3='', msg4='', msg5='', msgType='', msgOffset='AUTO', logFile='', logFileInit=False, msgColor='', msgBkgr='', output_devices='', print_enabled='', filelog_enabled='', ignoreWarning='',caller_module='',caller_function=''):
    colorB1 = Back.LIGHTWHITE_EX
    colorB2 = Back.WHITE
    colorF1 = Fore.BLUE
    colorF2 = Fore.GREEN
    log_message_special(msg1=msg1, msg2=msg2, msg3=msg3, msg4=msg4, msg5=msg5, msgType=msgType, msgOffset=msgOffset, logFile=logFile, logFileInit=logFileInit, msgColor=msgColor, msgBkgr=msgBkgr, output_devices=output_devices, print_enabled=print_enabled, filelog_enabled=filelog_enabled, ignoreWarning=ignoreWarning, caller_module=caller_module, caller_function=caller_function,colorB1 = colorB1,colorB2 = colorB2,colorF1 = colorF1,colorF2 = colorF2)
#################################################################################################
def log_message_start_subprocess(msg1='', msg2='', msg3='', msg4='', msg5='', msgType='', msgOffset='AUTO', logFile='', logFileInit=False, msgColor='', msgBkgr='', output_devices='', print_enabled='', filelog_enabled='', ignoreWarning='',caller_module='',caller_function=''):
    colorB1 = Back.WHITE
    colorB2 = Back.LIGHTWHITE_EX
    colorF1 = Fore.MAGENTA
    colorF2 = Fore.BLUE
    log_message_special(msg1=msg1, msg2=msg2, msg3=msg3, msg4=msg4, msg5=msg5, msgType=msgType, msgOffset=msgOffset, logFile=logFile, logFileInit=logFileInit, msgColor=msgColor, msgBkgr=msgBkgr, output_devices=output_devices, print_enabled=print_enabled, filelog_enabled=filelog_enabled, ignoreWarning=ignoreWarning, caller_module=caller_module, caller_function=caller_function,colorB1 = colorB1,colorB2 = colorB2,colorF1 = colorF1,colorF2 = colorF2)
#################################################################################################
def log_message_starting(msg1='', msg2='', msg3='', msg4='', msg5='', msgType='', msgOffset='AUTO', logFile='', logFileInit=False, msgColor='', msgBkgr='', output_devices='', print_enabled='', filelog_enabled='', ignoreWarning='',caller_module='',caller_function=''):
    colorB1 = Back.WHITE
    colorB2 = Back.LIGHTWHITE_EX
    colorF1 = Fore.BLUE
    colorF2 = Fore.BLACK
    log_message_special(msg1=msg1, msg2=msg2, msg3=msg3, msg4=msg4, msg5=msg5, msgType=msgType, msgOffset=msgOffset, logFile=logFile, logFileInit=logFileInit, msgColor=msgColor, msgBkgr=msgBkgr, output_devices=output_devices, print_enabled=print_enabled, filelog_enabled=filelog_enabled, ignoreWarning=ignoreWarning, caller_module=caller_module, caller_function=caller_function,colorB1 = colorB1,colorB2 = colorB2,colorF1 = colorF1,colorF2 = colorF2)
#################################################################################################
def log_message_subprocess_running(msg1='', msg2='', msg3='', msg4='', msg5='', msgType='', msgOffset='AUTO', logFile='', logFileInit=False, msgColor='', msgBkgr='', output_devices='', print_enabled='', filelog_enabled='', ignoreWarning='',caller_module='',caller_function=''):
    colorB1 = Back.MAGENTA
    colorB2 = Back.MAGENTA
    colorF1 = Fore.WHITE
    colorF2 = Fore.YELLOW
    log_message_special(msg1=msg1, msg2=msg2, msg3=msg3, msg4=msg4, msg5=msg5, msgType=msgType, msgOffset=msgOffset, logFile=logFile, logFileInit=logFileInit, msgColor=msgColor, msgBkgr=msgBkgr, output_devices=output_devices, print_enabled=print_enabled, filelog_enabled=filelog_enabled, ignoreWarning=ignoreWarning, caller_module=caller_module, caller_function=caller_function,colorB1 = colorB1,colorB2 = colorB2,colorF1 = colorF1,colorF2 = colorF2)
#############################################################################
def log_message_special_error(msg1='', msg2='', msg3='', msg4='', msg5='', msgType='', msgOffset='AUTO', logFile='', logFileInit=False, msgColor='', msgBkgr='', output_devices='', print_enabled='', filelog_enabled='', ignoreWarning='',caller_module='',caller_function=''):
    colorB1 = Back.RED
    colorB2 = Back.RED
    colorF1 = Fore.YELLOW
    colorF2 = Fore.WHITE
    log_message_special(msg1=msg1, msg2=msg2, msg3=msg3, msg4=msg4, msg5=msg5, msgType=msgType, msgOffset=msgOffset, logFile=logFile, logFileInit=logFileInit, msgColor=msgColor, msgBkgr=msgBkgr, output_devices=output_devices, print_enabled=print_enabled, filelog_enabled=filelog_enabled, ignoreWarning=ignoreWarning, caller_module=caller_module, caller_function=caller_function,colorB1 = colorB1,colorB2 = colorB2,colorF1 = colorF1,colorF2 = colorF2)
#################################################################################################
def log_message_special_success(msg1='', msg2='', msg3='', msg4='', msg5='', msgType='', msgOffset='AUTO', logFile='', logFileInit=False, msgColor='', msgBkgr='', output_devices='', print_enabled='', filelog_enabled='', ignoreWarning='',caller_module='',caller_function=''):
    colorB1 = Back.LIGHTGREEN_EX
    colorB2 = Back.LIGHTGREEN_EX
    colorF1 = Fore.LIGHTBLUE_EX
    colorF2 = Fore.BLACK
    log_message_special(msg1=msg1, msg2=msg2, msg3=msg3, msg4=msg4, msg5=msg5, msgType=msgType, msgOffset=msgOffset, logFile=logFile, logFileInit=logFileInit, msgColor=msgColor, msgBkgr=msgBkgr, output_devices=output_devices, print_enabled=print_enabled, filelog_enabled=filelog_enabled, ignoreWarning=ignoreWarning, caller_module=caller_module, caller_function=caller_function,colorB1 = colorB1,colorB2 = colorB2,colorF1 = colorF1,colorF2 = colorF2)
#################################################################################################
def log_dictionary(dict={}, title='', sortedbyKey=True, sortedbyValue=False, print_enabled='', filelog_enabled=''):
    global utils_logOutput_Devices
    global utils_consolelog_enabled
    global utils_filelog_enabled

    if title:
        log_message(title, msgType='start', print_enabled=print_enabled, filelog_enabled=filelog_enabled)

    ix = 0
    if sortedbyKey:
        for key in sorted(dict):
            ix += 1
            thisValue = dict[key]
            thatValue = display_value(thisValue)
            msg = '{}={}'.format(key, thatValue)
            log_message(msg, msgType='info', msgOffset='+1', print_enabled=print_enabled, filelog_enabled=filelog_enabled)
    elif sortedbyValue:
        sorted_keys = sorted(dict, key=dict.get, reverse=False)
        for key in sorted_keys:
            ix += 1
            thisValue = dict[key]
            thatValue = display_value(thisValue)
            msg = '{}={}'.format(key, thatValue)
            log_message(msg, msgType='info', msgOffset='+1', print_enabled=print_enabled, filelog_enabled=filelog_enabled)
    else:
        for key in dict:
            ix += 1
            thatValue = display_value(thisValue)
            msg = '{}={}'.format(key, thatValue)
            log_message(msg, msgType='info', msgOffset='+1', print_enabled=print_enabled, filelog_enabled=filelog_enabled)

    resmsg = '{} entries'.format(ix)
    if title:
        log_message(resmsg, msgType='finish', print_enabled=print_enabled, filelog_enabled=filelog_enabled)
    else:
        log_message(resmsg, msgType='RESULT', msgOffset='+1', print_enabled=print_enabled, filelog_enabled=filelog_enabled)
#############################################################################
def arrange_components_length(components=[], target_length=40, method='',required_lens=[]):
    if len(components) <= 0:
        return components
    if target_length < 20:
        for ix in range(0, len(components)):
            if ix == 0:
                compo=components[0][:target_length]
                components[0]=compo
            else:
                new_components.uppend('')
    else:
        # if method.upper() in ('EQUAL', ''):
        #     min_len = 5
        # if method.upper() in ('EQUAL', ''):
        #     min_len = 5
        
        ix=0
        totlen = 0
        for ix in range(0, len(components)):
            totlen = totlen + len(str(components[ix]))
        origtotlen=totlen
        while totlen > target_length and ix < 999:
            ix = ix + 1
            for cx1 in range(0, len(components)):
                cx = len(components) - cx1 - 1
                compo = str(components[cx])
                origlen = len(compo)
                xtotlen=totlen
                while len(compo) > 5 and xtotlen > target_length:
                    compo = compo[:len(compo) - 1]
                    xtotlen = totlen -origlen + len(compo)
                components[cx]=compo
            
                totlen = 0
                for ix in range(0, len(components)):
                    totlen = totlen + len(str(components[ix]))

    return(components)
#############################################################################
def xlog_result_message(action_level=1,action='', msg1='', msg2='', msg3='', msgType='', msgOffset='AUTO', logFile='', logFileInit=False, msgColor='', msgBkgr='', output_devices='', print_enabled='', filelog_enabled='', ignoreWarning='',caller_module='',caller_function=''):
    global fore_colors
    global back_colors
    global color_names
    global fore_colors_dict
    global back_colors_dict
    global fore_color_names_dict
    global back_color_names_dict

    process_name = whosdaddy()

    compos = arrange_components_length(components=[process_name, action], target_length=40, method='', required_lens=[30, 20])
    process_name=compos[0]
    action=compos[1]

    compos = arrange_components_length(components=[msg1, msg2,msg3], target_length=80, method='', required_lens=[])
    msg1=compos[0]
    msg2=compos[1]
    msg3=compos[2]

    bgcolor = Back.Black
    fgcolor = get_fore_color_based_onBackground(bgcolor, action_level)
    msgP1 = f"{bgcolor}{fgcolor}{process_name}{Fore.RESET}{Back.RESET}"

    # bgcolor = Back.LIGHTBLACK_EX
    # fgcolor = get_fore_color_based_onBackground(bgcolor, action_level)
    # msgP2 = f"{bgcolor}{fgcolor}{action}{Fore.RESET}{Back.RESET}"

    if msgType.upper().find('ERROR') >= 0:
        msg1=f"{Fore.RED}{msg1}{Fore.RESET}"
    elif msgType.upper().find('WARN') >= 0:
        msg1=f"{Fore.YELLOW}{msg1}{Fore.RESET}"
    elif msgType.upper().find('OK') >= 0 or msgType.upper().find('SUCCESS') >= 0:
        msg1=f"{Fore.GREEN}{msg1}{Fore.RESET}"
    msg3 = f"{msg3}{Fore.RESET}{Back.RESET}"
    msgOffset=''
    log_message(msg1=msgP1, msg2=msg1, msg3=msg2, msg4=msg3, msg5=msg4, msgType='info', msgOffset=msgOffset, msgCategory='DEBUG', logFile=logFile, logFileInit=logFileInit, msgColor=Fore.WHITE)
#################################################################################################
def log_result_message(msg1='', msg2='', msg3='', msg4='', msgType='', msgOffset='AUTO', level=0, logFile='', logFileInit=False, msgColor='', msgBkgr='', output_devices='', print_enabled='', filelog_enabled='', ignoreWarning='', caller_module='', caller_function=''):
    global fore_colors
    global back_colors
    global color_names
    global fore_colors_dict
    global back_colors_dict
    global fore_color_names_dict
    global back_color_names_dict

    process_name = whosdaddy()

    debug_level = _debugServices.global_debug_levels.get(process_name.upper(), -1)
    if debug_level < 0:
        debug_level = _debugServices.global_debug_level

    if not debug_level >= level:
        return
    
    action_level = 1
    action = ''
    
    compos = arrange_components_length(components=[process_name, action], target_length=30, method='', required_lens=[30, 20])
    process_name=compos[0]
    action=compos[1]

    compos = arrange_components_length(components=[msg1, msg2,msg3], target_length=100, method='', required_lens=[])
    msg1=compos[0]
    msg2=compos[1]
    msg3=compos[2]

    # level :0 1 2 3 4 5 6 7 8 9
    # offset:0 8 7 6 5 4 3 2 1 0
    offset = 9 - level
    if offset < 0:
        offset = 0
    bgcolor = Back.BLACK
    fgcolor = get_fore_color_based_onBackground(bgcolor, level)
    #msgP1 = f"{bgcolor}{fgcolor}{level}-{'o'*level}{Fore.RED}o{fgcolor}{process_name}{Fore.RESET}{Back.RESET}:"
    #msgP1 = f"{bgcolor}{fgcolor}{' '*level}{Fore.RED}o{fgcolor}{process_name}{Fore.RESET}{Back.RESET}:"
    #msgP1 = f"{bgcolor}{fgcolor}{' '*offset}{process_name}{Fore.RESET}{Back.RESET}:"
    msgP1 = f"{' '*offset}#C9#{process_name}#C0#:"

    # bgcolor = Back.LIGHTBLACK_EX
    # fgcolor = get_fore_color_based_onBackground(bgcolor, action_level)
    # msgP2 = f"{bgcolor}{fgcolor}{action}{Fore.RESET}{Back.RESET}"
    msg = f"{str(msg1)} {str(msg2)} {str(msg3)} {str(msg4)}".replace('  ', ' ').strip()
        
    if msgType.upper().find('ERROR') >= 0:
        msg=f"[[[[{msg}]]]]"
    elif msgType.upper().find('WARN') >= 0:
        msg=f"[{msg}]"
    elif msgType.upper().find('OK') >= 0 or msgType.upper().find('SUCCESS') >= 0:
        msg = f"[[[[[{msg}]]]]]"
    else:
        msg = f"[[{msg}]]"

    msgOffset=''
    log_message(msg1=msgP1, msg2=msg, msg3='', msg4='', msg5='', msgType='info', msgOffset=msgOffset, msgCategory='DEBUG', logFile=logFile, logFileInit=logFileInit, msgColor=Fore.WHITE)
#################################################################################################
def log_module_initialization_message(module_identityDictionary):
    module_id = module_identityDictionary.get('module_id', '?')
    module_version = module_identityDictionary.get('module_version', '?')
    module_color = module_identityDictionary.get('module_color', Fore.RED)
    print_enabled=module_identityDictionary.get('consolelog_enabled', None)
    filelog_enabled=module_identityDictionary.get('filelog_enabled', None)
    msg = f'module [{module_id}] [[version {module_version}]] loaded.'
    log_message(msg,print_enabled=print_enabled, filelog_enabled=filelog_enabled)
    if thisApp.CONSOLE_ON:
        pass
        #print('')
#################################################################################################
def log_debug_message(action_level=1,action='', msg1='', msg2='', msg3='', msgType='', msgOffset='AUTO', logFile='', logFileInit=False, msgColor='', msgBkgr='', output_devices='', print_enabled='', filelog_enabled='', ignoreWarning='',caller_module='',caller_function=''):
    global fore_colors
    global back_colors
    global color_names
    global fore_colors_dict
    global back_colors_dict
    global fore_color_names_dict
    global back_color_names_dict

    process_name = whosdaddy()

    compos = arrange_components_length(components=[process_name, action], target_length=40, method='', required_lens=[20, 20])
    process_name=compos[0]
    action=compos[1]

    compos = arrange_components_length(components=[msg1, msg2,msg3], target_length=60, method='', required_lens=[])
    msg1=compos[0]
    msg2=compos[1]
    msg3=compos[2]

    bgcolor = Back.WHITE
    fgcolor = get_fore_color_based_onBackground(bgcolor, action_level)
    msgP1 = f"{bgcolor}{fgcolor}{process_name}{Fore.RESET}{Back.RESET}"

    bgcolor = Back.LIGHTBLACK_EX
    fgcolor = get_fore_color_based_onBackground(bgcolor, action_level)
    msgP2 = f"{bgcolor}{fgcolor}{action}{Fore.RESET}{Back.RESET}"

    if msgType.upper().find('ERROR') >= 0:
        msg1=f"{Fore.RED}{msg1}{Fore.RESET}"
    elif msgType.upper().find('WARN') >= 0:
        msg1=f"{Fore.YELLOW}{msg1}{Fore.RESET}"
    elif msgType.upper().find('OK') >= 0 or msgType.upper().find('SUCCESS') >= 0:
        msg1=f"{Fore.GREEN}{msg1}{Fore.RESET}"
    msg3 = f"{msg3}{Fore.RESET}{Back.RESET}"
    msgOffset=''
    log_message(msg1=msgP1, msg2=msgP2, msg3=msg1, msg4=msg2, msg5=msg3, msgType='info', msgOffset=msgOffset, msgCategory='DEBUG', logFile=logFile, logFileInit=logFileInit, msgColor=Fore.WHITE)
#################################################################################################
def log_module_process_start(process_name='',msgColor=''):
    if not process_name:
        process_name = whosdaddy()
    log_message(process_name, msgType='START',msgColor=msgColor)
#############################################################################
def log_module_process_finish(process_name='',msgColor=''):
    if not process_name:
        process_name = whosdaddy()
    if process_name:
        msg = f'{process_name} finished'
    log_message(msg, msgType='FINISH',msgColor=msgColor)
#############################################################################
def log_process_start(process_name=''):
    if not process_name:
        process_name = whosdaddy()
    log_message(process_name, msgType='START')
#############################################################################
def log_process_finish(process_name=''):
    if process_name:
        msg = f'{process_name} finished'
    else:
        msg = ''
    log_message(msg, msgType='FINISH')
#############################################################################
def log_process_section_start(process_name):
    log_message(process_name, msgType='START')
#############################################################################
def log_process_section_finish(process_name=''):
    if process_name:
        msg = f'section:{process_name} finished'
    else:
        msg = 'section finished'
    log_message(msg, msgType='FINISH')
#############################################################################
def log_process_input_param(what,value):
    msg=f'input: {what}={value}'
    log_message(msg, msgType='INFO-3', msgOffset='+1')
#############################################################################
def log_process_result(what,value):
    msg=f'output: {what}={value}'
    log_message(msg, msgType='INFO-2', msgOffset='+1')
#############################################################################
def log_process_output(what,value):
    msg=f'output: {what}={value}'
    log_message(msg, msgType='INFO-4', msgOffset='+1')
#############################################################################
def log_process_value(what='', value=''):
    msg=f'{what}={value}'
    log_message(msg, msgType='INFO', msgOffset='+1')
#############################################################################
def log_process_error(what=''):
    log_message(what, msgType='ERROR', msgOffset='+1')
#############################################################################
# def apply_colors(msgP,msgColor=Fore.LIGHTBLACK_EX):
#     if not msgColor:
#         msgColor=FgColor0
#     #msgP=msgP.replace('[o','#C8#').replace('o]','#C0#')
#     msgP=msgP.replace('[[[[[[[[','#C8#').replace(']]]]]]]]','#C0#')
#     msgP=msgP.replace('[[[[[[[','#C7#').replace(']]]]]]]','#C0#')
#     msgP=msgP.replace('[[[[[[','#C6#').replace(']]]]]]','#C0#')
#     msgP=msgP.replace('[[[[[','#C5#').replace(']]]]]','#C0#')
#     msgP=msgP.replace('[[[[','#C4#').replace(']]]]','#C0#')
#     msgP=msgP.replace('[[[','#C3#').replace(']]]','#C0#')
#     msgP=msgP.replace('[[','#C2#').replace(']]','#C0#')
#     msgP=msgP.replace('[','#C1#').replace(']','#C0#')
#     msgP = f"{FgColor0}{msgP}{Fore.RESET}{Back.RESET}"

#     msgP=msgP.replace('#RESET#',msgColor)
#     for ix in range(0, len(colors_array)):
#         if not msgP.find('#') >= 0:
#             break
#         msgP=msgP.replace(colors_array[ix][0],colors_array[ix][1])
#     return msgP
#############################################################################
def display_logServices_options(outputOption='changes', filelog_enabled=''):
    global logServices_config_dictionary
    global logServices_config_dictionary_prev
    global module_id
    for key in sorted(logServices_config_dictionary):
        if outputOption.upper() in ('CHANGES', 'DIFFERENTIAL'):
            if str(logServices_config_dictionary.get(key)).upper() != str(logServices_config_dictionary_prev.get(key)).upper():
                msg = '{} = {}'.format(key, logServices_config_dictionary.get(key))
                msg = '{} = {} (from:{})'.format(key, logServices_config_dictionary.get(key), logServices_config_dictionary_prev.get(key))
                log_message(module_id, msg, msgType='configuration', filelog_enabled=filelog_enabled, print_enabled=True)
        else:
            if outputOption.upper() not in ('NONE', 'OFF', 'FALSE'):
                msg = '{} = {}'.format(key, logServices_config_dictionary.get(key))
                log_message(module_id, msg, msgType='configuration', filelog_enabled=filelog_enabled, print_enabled=True)
            else:
                msg = '{} = {}'.format(key, logServices_config_dictionary.get(key))
                log_message(module_id, msg, msgType='configuration', filelog_enabled=filelog_enabled, print_enabled=False)
#############################################################################
def display_logServices_Configuration():
    global logServices_config_dictionary
    title = '_logServices configuration options:{}'.format('')
    log_dictionary(dict=logServices_config_dictionary, title=title, sortedbyKey=True, print_enabled=True, filelog_enabled=False)
#############################################################################
def xinitialize_application_configuration(outputOption='FULL', filelog_enabled=''):
    global logServices_config_dictionary
    global logServices_config_dictionary_prev

    global log_file_name
    global log_errors_file_name
    global log_output_devices
    global log_consolelog_enabled
    global log_filelog_enabled
    global log_ignoreWarning
    global log_console_line_length
    global log_force_log_warnings
    global log_force_print_warnings
    global log_force_log_errors
    global log_force_print_errors
    global log_force_log_system_errors
    global log_force_print_system_errors
    global log_indent_color
    global log_indent_bgcolor
    global log_indent_char
    global log_indent_tab
    global log_level
    global config_version
    global config_versionStr
    global config_versionString
    global log_eyecatch
    global log_color_mode

    if not outputOption:
        outputOption = 'NONE'
    if outputOption == True:
        outputOption = 'FULL'
        
    config_versionString = config_version_string(config_version, config_versionStr, module_BaseTimeStamp='')

    logServices_config_dictionary.update({'log_file_name' : string_datetime_translate(log_file_name)})
    logServices_config_dictionary.update({'log_errors_file_name' : string_datetime_translate(log_errors_file_name)})
    logServices_config_dictionary.update({'log_output_devices' : log_output_devices})
    logServices_config_dictionary.update({'log_consolelog_enabled' : log_consolelog_enabled})
    logServices_config_dictionary.update({'log_filelog_enabled' : log_filelog_enabled})
    logServices_config_dictionary.update({'log_ignoreWarning' : log_ignoreWarning})
    logServices_config_dictionary.update({'log_console_line_length' : log_console_line_length})
    logServices_config_dictionary.update({'log_force_print_warnings' : log_force_print_warnings})
    logServices_config_dictionary.update({'log_force_log_warnings' : log_force_log_warnings})
    logServices_config_dictionary.update({'log_force_log_errors' : log_force_log_errors})
    logServices_config_dictionary.update({'log_force_print_errors' : log_force_print_errors})
    logServices_config_dictionary.update({'log_force_log_system_errors' : log_force_log_system_errors})
    logServices_config_dictionary.update({'log_force_print_system_errors' : log_force_print_system_errors})
    logServices_config_dictionary.update({'log_indent_color' : log_indent_color})
    logServices_config_dictionary.update({'log_indent_bgcolor' : log_indent_bgcolor})
    logServices_config_dictionary.update({'log_indent_char' : log_indent_char})
    logServices_config_dictionary.update({'log_indent_tab' : log_indent_tab})
    logServices_config_dictionary.update({'config_version' : config_version})
    logServices_config_dictionary.update({'config_versionString' : config_versionString})
    logServices_config_dictionary.update({'config_versionStr' : config_versionStr})
    logServices_config_dictionary.update({'log_level' : log_level})
    logServices_config_dictionary.update({'eyecatch': module_ProgramName})

    changes = 0
    for key in sorted(logServices_config_dictionary):
            if str(logServices_config_dictionary.get(key)).upper() != str(logServices_config_dictionary_prev.get(key)).upper():
                changes = changes + 1

    display_logServices_options(outputOption=outputOption, filelog_enabled='') #display
    logServices_config_dictionary_prev = logServices_config_dictionary.copy() #save a copy
    return changes
#############################################################################
def set_log_options(
    print_enabled='',
    filelog_enabled='',
    logfile_name='',
    ignoreWarning='',
    output_devices='',
    console_line_length='',
    console_line_fixlength='',
    force_log_warnings='',
    force_print_warnings='',
    force_log_errors='',
    force_print_errors='',
    force_log_system_errors='',
    force_print_system_errors='',
    indent_color='',
    indent_bgcolor='',
    indent_char='',
    indent_tab=None,
    color_mode=None,
    caller_module_file='',
    caller_module_ProgramName='',
    caller_module_identityDictionary={},
    set_as_appl_log=False,
    ):
    global module_identityDictionary
    global module_id
    global module_color
    global logServices_config_dictionary
    global log_file_name
    global log_errors_file_name
    global log_output_devices
    global log_consolelog_enabled
    global log_filelog_enabled
    global log_ignoreWarning
    global log_console_line_length
    global log_console_fix_line_length
    global log_force_log_warnings
    global log_force_print_warnings
    global log_force_log_errors
    global log_force_print_errors
    global log_force_log_system_errors
    global log_force_print_system_errors
    global log_indent_color
    global log_indent_bgcolor
    global log_indent_char
    global log_indent_tab
    global log_color_mode
    global logServicesConfigFile
    global config_version
    global config_versionStr
    global config_versionString

    caller_module_Color=module_color
    caller_module_folder = ''
    if caller_module_identityDictionary:
        caller_module_Color = caller_module_identityDictionary.get('module_color', '')
        caller_module_ProgramName = caller_module_identityDictionary.get('module_ProgramName', '')
    if caller_module_file:
            caller_module_folder = os.path.dirname(caller_module_file)
            if not caller_module_ProgramName:
                caller_module_ProgramName = os.path.splitext(os.path.basename(caller_module_file))[0]
    if not caller_module_folder:
        caller = sys._getframe(1)  # Obtain calling frame
        caller_module_file = caller.f_globals['__file__']
        caller_module_folder = os.path.dirname(caller_module_file)
        if not caller_module_ProgramName:
            caller_module_ProgramName = os.path.splitext(os.path.basename(caller_module_file))[0]

    logServicesConfigFile=f'{caller_module_ProgramName}_{module_id}.cfg'
    if set_as_appl_log:
        thisApp.logServicesConfigFile=logServicesConfigFile

    #retrieve existing config from this config file (app config) logServicesConfigFile
    logServices_config_dictionary = retrieve_configuration_from_file(logServicesConfigFile, this_configuration=logServices_config_dictionary, module_identityDictionary=module_identityDictionary, print_enabled=None, filelog_enabled=None)
    set_global_vars_from_dictionary(logServices_config_dictionary,logServicesConfigFile)


    msg=f'{module_id}: log_file: {log_file_name}'
    log_message(msg,msgType='info',msgOffset='+1',msgColor=caller_module_Color)
    msg=f'{module_id}: consolelog_enabled: {log_consolelog_enabled}, filelog_enabled: {log_filelog_enabled}, ignoreWarning: {log_ignoreWarning}'
    log_message(msg,msgType='info',msgOffset='+1',msgColor=caller_module_Color)

    prev_logServices_config_dictionary = logServices_config_dictionary.copy()

    if output_devices:
        output_devices = output_devices.upper()
    else:
        output_devices = log_output_devices
    if print_enabled == True:
        if not output_devices.find('PRINT') >= 0:
            output_devices = output_devices + ' PRINT'
    if filelog_enabled == True:
        if not output_devices.find('FILE') >= 0:
            output_devices = output_devices + ' FILE'
    if print_enabled == False:
        output_devices = output_devices.replace('PRINT','')
        output_devices = output_devices.replace('CONSOLE','')
    if filelog_enabled == False:
        output_devices = output_devices.replace('FILE','')
    if ignoreWarning == True:
        if not output_devices.find('IGNORE-WARNING') >= 0:
            output_devices = output_devices + ' IGNORE-WARNING'
    if ignoreWarning == False:
        output_devices = output_devices.replace('IGNORE-WARNING','')

    output_devices = output_devices.upper().strip()

    xlog_output_devices = output_devices
    log_ignoreWarning = option_enabled(output_devices, 'IGNORE-WARNING')
    xlog_consolelog_enabled = option_enabled(output_devices, 'PRINT')
    xlog_filelog_enabled = option_enabled(output_devices, 'FILE')

    if console_line_length:
        log_console_line_length = console_line_length
    if log_console_line_length <= 0:
        log_console_line_length = 999999        
    if console_line_fixlength:
        log_console_line_length = console_line_fixlength
    if log_console_line_length <= 0:
        log_console_line_length = 80        

    if logfile_name:
        logfile_name = string_datetime_translate(logfile_name)
    if logfile_name:
        ok = False
        try:
            f = open(logfile_name, "a+")
            #f.write('test...')
            f.close
            ok = True
        except:
            ok = False
        # try:
        #     os.remove(logfile_name)
        #     ok = True
        # except OSError as error:
        #     msg = error
        #     print(msg)
        #     ok = False
        if ok:
            xlog_file_name = logfile_name
            msg = f'{module_id}: log file set to [{xlog_file_name}] by {caller_module_ProgramName}'
            log_message(msg, msgType='info-1', msgOffset='+1',msgColor=caller_module_Color)
        else:
            msg = f'log file [{logfile_name}] can not be set. current log file is [{log_file_name}]'
            log_message(msg, msgType='warning', msgOffset='+1',msgColor=caller_module_Color)

    if force_log_warnings == True:
        log_force_log_warnings = True
    elif force_log_warnings == False:
        log_force_log_warnings = False

    if force_log_errors == True:
        log_force_log_errors = True
    elif force_log_errors == False:
        log_force_log_errors = False

    if force_log_system_errors == True:
        log_force_log_system_errors = True
    elif force_log_system_errors == False:
        log_force_log_system_errors = False

    if indent_color:
        log_indent_color = log_indent_color
    if indent_bgcolor:
        log_indent_bgcolor = log_indent_bgcolor
    if indent_char:
        log_indent_char = log_indent_char
    if indent_tab:
        log_indent_tab = log_indent_tab
    if color_mode:
        if color_mode.upper() in ('COLOR'):
            log_color_mode = 'COLOR'
        elif color_mode.upper() in ('MONO', 'BW'):
            log_color_mode = 'MONO'
        else:
            col = string_translate_colors(color_mode)
            if col != log_color_mode:
                log_color_mode = color_mode

    xlog_errors_file_name = os.path.splitext(os.path.basename(xlog_file_name))[0]+'_errors.log'

    if logServices_config_dictionary.get('log_file_name','') != xlog_file_name:
        #prev_log_file_name =logServices_config_dictionary.get('log_file_name','')
        msg=f"\n{module_id}: log file changed to [{xlog_file_name}] from [{logServices_config_dictionary.get('log_file_name','')}]\n"
        log_message(msg, msgType='configuration', msgOffset='+1', msgColor=Fore.RED)
        new_log_file_name = xlog_file_name        
        merge_log_files(caller_module_folder, new_log_file_name, remove_old_file=True)

    if logServices_config_dictionary.get('log_errors_file_name','') != xlog_errors_file_name:
        #prev_log_file_name =logServices_config_dictionary.get('log_errors_file_name','')
        msg=f"\n{module_id}: errors file changed to [{xlog_errors_file_name}] from [{logServices_config_dictionary.get('log_errors_file_name','')}]\n"
        log_message(msg, msgType='configuration',msgOffset='+1',msgColor=caller_module_Color)
        new_log_file_name = xlog_errors_file_name        
        merge_log_files(caller_module_folder, new_log_file_name, remove_old_file=True)
    
    if logServices_config_dictionary.get('log_consolelog_enabled',None) != xlog_consolelog_enabled:
        msg=f'{module_id}: log_print_enabled set to [{xlog_consolelog_enabled}]'
        log_message(msg, msgType='configuration',msgOffset='+1',msgColor=caller_module_Color)

    if logServices_config_dictionary.get('log_filelog_enabled',None) != xlog_filelog_enabled:
        msg=f'{module_id}: log_filelog_enabled set to [{log_filelog_enabled}]'
        log_message(msg, msgType='configuration',msgOffset='+1',msgColor=caller_module_Color)

    logServices_config_dictionary.update({'log_file_name':xlog_file_name})
    logServices_config_dictionary.update({'log_errors_file_name':xlog_errors_file_name})
    logServices_config_dictionary.update({'log_output_devices':xlog_output_devices})
    logServices_config_dictionary.update({'log_consolelog_enabled':xlog_consolelog_enabled})
    logServices_config_dictionary.update({'log_filelog_enabled':xlog_filelog_enabled})
    logServices_config_dictionary.update({'log_ignoreWarning':log_ignoreWarning})
    logServices_config_dictionary.update({'log_console_line_length': log_console_line_length})
    logServices_config_dictionary.update({'log_console_fix_line_length': log_console_fix_line_length})
    logServices_config_dictionary.update({'log_level':log_level})
    logServices_config_dictionary.update({'log_current_prefix':log_current_prefix})
    logServices_config_dictionary.update({'log_force_log_warnings':log_force_log_warnings})
    logServices_config_dictionary.update({'log_force_print_warnings':log_force_print_warnings})
    logServices_config_dictionary.update({'log_force_log_errors':log_force_log_errors})
    logServices_config_dictionary.update({'log_force_print_errors':log_force_print_errors})
    logServices_config_dictionary.update({'log_force_log_system_errors':log_force_log_system_errors})
    logServices_config_dictionary.update({'log_force_print_system_errors':log_force_print_system_errors})
    logServices_config_dictionary.update({'log_indent_char':log_indent_char})
    logServices_config_dictionary.update({'log_indent_tab':log_indent_tab})
    logServices_config_dictionary.update({'log_indent_color':log_indent_color})
    logServices_config_dictionary.update({'log_indent_bgcolor': log_indent_bgcolor})
    logServices_config_dictionary.update({'log_color_mode': log_color_mode})

    log_file_name=xlog_file_name
    log_errors_file_name=xlog_errors_file_name
    log_output_devices=xlog_output_devices
    log_consolelog_enabled=xlog_consolelog_enabled
    log_filelog_enabled=xlog_filelog_enabled

    if prev_logServices_config_dictionary != logServices_config_dictionary:
        new_config_version(caller_module_ProgramName)
        save_config_to_file(logServicesConfigFile, config_dictionary=logServices_config_dictionary)
        if set_as_appl_log:
            appl_logServicesConfigFile='applogServices.cfg'
            save_config_to_file(appl_logServicesConfigFile, config_dictionary=logServices_config_dictionary)

        msg=f'{module_id}: log_file: {log_file_name}'
        log_message(msg,msgType='info',msgOffset='+1',msgColor=caller_module_Color)
        msg=f'{module_id}: consolelog_enabled: {log_consolelog_enabled}, filelog_enabled: {log_filelog_enabled}, ignoreWarning: {log_ignoreWarning}'
        log_message(msg,msgType='info',msgOffset='+1',msgColor=caller_module_Color)

    if set_as_appl_log:
        appl_logServicesConfigFile = 'applogServices.cfg'
        if not os.path.isfile(appl_logServicesConfigFile):
            save_config_to_file(appl_logServicesConfigFile, config_dictionary=logServices_config_dictionary)

    msg=f'{module_id} configured as {config_versionString}.'
    log_message(msg, msgType='config',msgOffset='+1',msgColor=caller_module_Color)
#############################################################################
def pair_logServices_configuration_with_application_config(appl_logServicesConfigFile='',caller_module_identityDictionary={}):
    global logServices_config_dictionary
    global logServicesConfigFile
    global module_identityDictionary
    global log_file_name
    caller_module_id=caller_module_identityDictionary.get('module_id','?')
    caller_module_Color = caller_module_identityDictionary.get('module_color', '')
    if not appl_logServicesConfigFile:
        appl_logServicesConfigFile=thisApp.logServicesConfigFile
    # if not appl_logServicesConfigFile:
    #     appl_logServicesConfigFile=logServicesConfigFile
    if appl_logServicesConfigFile:
        logServices_config_dictionary = retrieve_configuration_from_file(appl_logServicesConfigFile,this_configuration=logServices_config_dictionary, module_identityDictionary=caller_module_identityDictionary, print_enabled=None, filelog_enabled=None)
        set_global_vars_from_dictionary(logServices_config_dictionary,appl_logServicesConfigFile)
        logServicesConfigFile=appl_logServicesConfigFile
        msg=f'{caller_module_id}: paired logServices_configuration with {appl_logServicesConfigFile}'
        log_message(msg, msgType='info', msgOffset='+1', msgColor=caller_module_Color)
    else:
        msg=f'{caller_module_id}: paired logServices_configuration withoout appl_logServicesConfigFile in _appEnvironment'
        log_message(msg, msgType='warning', msgOffset='+1', msgColor=caller_module_Color)
#############################################################################
#::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
#::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
#::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
#config support services
#::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
#::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
#::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
#############################################################################
def retrieve_module_configuration(module_identityDictionary, module_configuration={}, print_enabled=None, filelog_enabled=None):
    module_file = module_identityDictionary.get('module_file', '')
    module_log_file_name = module_identityDictionary.get('module_log_file_name', '')
    module_errors_file_name = module_identityDictionary.get('module_errors_file_name', '')
    module_id = module_identityDictionary.get('module_id', '')
    module_version = module_identityDictionary.get('module_version', '')
    module_color = module_identityDictionary.get('module_color', '')
    if module_identityDictionary.get('consolelog_enabled', None) == None:
        module_consolelog_enabled = print_enabled
    else:
        module_consolelog_enabled = module_identityDictionary.get('consolelog_enabled')

    if module_identityDictionary.get('filelog_enabled', None) == None:
        module_filelog_enabled = filelog_enabled
    else:
        module_filelog_enabled = module_identityDictionary.get('filelog_enabled')
    
    file_delete(module_log_file_name,msgOffset='+1',print_enabled=print_enabled,filelog_enabled=filelog_enabled, ignoreWarning=True ,msgColor=module_color)
    file_delete(module_errors_file_name,msgOffset='+1',print_enabled=print_enabled,filelog_enabled=filelog_enabled, ignoreWarning=True,msgColor=module_color)

    new_module_configuration = retrieve_module_configuration_from_file(module_file, module_configuration, module_identityDictionary, print_enabled, filelog_enabled)
    if not new_module_configuration.get('initialized', None):
        msg=f'{module_id}: FAILED TO INITIALIZED'
        log_message(msg, msgType='error', msgOffset='+1', msgColor=Fore.RED,print_enabled=print_enabled,filelog_enabled=filelog_enabled)
    else:
        msg = f'{module_id}: version {module_version} loaded.'
        if thisApp.DEBUG_ON:
            log_message(msg, msgType='config', msgOffset='+1', msgColor=module_color, print_enabled=print_enabled, filelog_enabled=filelog_enabled)

    #logging options
    new_module_configuration.update({'consolelog_enabled':module_consolelog_enabled})
    new_module_configuration.update({'print_enabled':module_consolelog_enabled})
    new_module_configuration.update({'filelog_enabled':module_filelog_enabled})
    #new_module_configuration.update({'module_log_file_name':module_log_file_name})
    #new_module_configuration.update({'module_errors_file_name':module_errors_file_name})

    return new_module_configuration
#############################################################################
def retrieve_module_configuration_from_file(this_file, this_configuration={}, module_identityDictionary={}, print_enabled=None, filelog_enabled=None):
    # global thisApp.EXECUTION_MODE

    module_color = module_identityDictionary.get('module_color', '')
    module_id=module_identityDictionary.get('module_id','')
    if not this_file:
        errorMsg = f'{module_ProgramName}: retrieve_module_configuration_from_file: config file not provided'
        log_message(errorMsg, msgType='WARNING', msgOffset='+1', msgColor=module_color)
        return this_configuration
        #raise Exception(errorMsg)

    moduleProgramName = os.path.splitext(os.path.basename(this_file))[0]
    if thisApp.EXECUTION_MODE.upper().find('PROD') >= 0:
        configFile = f'{moduleProgramName}.cfg'
    else:
        configFile = f'{moduleProgramName}_{thisApp.EXECUTION_MODE.lower()}.cfg'    
    config_folder = os.path.dirname(this_file)

    if not os.path.isfile(configFile):
        configString = json.dumps(this_configuration, sort_keys=True, indent=4)
        with open(configFile, 'w') as cfgFile:
            cfgFile.write(configString)
        msg = f'{module_id}: config file {configFile} created'
        if thisApp.DEBUG_ON:
            log_message(msg, msgType='WARNING', msgOffset='+1',msgColor=module_color)
    else:
        try:
            with open(configFile, 'r') as cfgFile:
                configString=cfgFile.read()
            if thisApp.DEBUG_ON:
                log_message(f'{module_id}: config file {configFile} retrieved',msgType='OK',msgOffset='+1',msgColor=module_color)
        except:
            configString = None
            errorMsg = f'{module_id}: config file {configFile} not found'
            log_message(errorMsg, msgType='ERROR', msgOffset='+1',msgColor=module_color)
            raise Exception(errorMsg)
        if configString:
            this_configuration = json.loads(configString)

    msg=f'{module_id}: config folder is [ {config_folder} ]'
    log_message(msg, msgCategory='DEBUG', msgType='info', msgOffset='+1', msgColor=module_color)
    
    configFilePath='?'
    #configFilePath = find_file(configFile, search_Downwards=1, search_Upwards=0, search_SubFolders=False)
    msg=f'{module_id}: config file path is [ {configFilePath} ]'
    log_message(msg, msgCategory='DEBUG', msgType='info', msgOffset='+1', msgColor=module_color)

    if not configFilePath:
        errorMsg = f'{module_id}: config file [{configFile}] not found in config folder [ {config_folder} ]'
        log_message(errorMsg, msgType='SYSTEM ERROR', msgOffset='+1',msgColor=module_color)
        raise Exception(errorMsg)
    
    relativePath = configFilePath.lower().replace(config_folder.lower(),'').replace(configFile.lower(),'')
    msg = f'{module_id}: relative configuration path is [{relativePath}]'
    log_message(msg, msgCategory='DEBUG', msgType='info', msgOffset='+1', msgColor=module_color)

    this_configuration.update({'configFile': configFile})
    this_configuration.update({'configFilePath': configFilePath})

    msg = f'{module_id}: configuration imported from [{configFile}]'
    log_message(msg, msgCategory='DEBUG', msgType='OK', msgOffset='+1', msgColor=module_color)
    
    initTimeStamp = str(datetime.datetime.now())
    this_configuration.update({'initialized':initTimeStamp})

    return this_configuration
################################################################
def notused_read_client_configuration_dictionary_from_file(configFile, module_identityDictionary = {}, print_enabled = None, filelog_enabled = None):
    module_color = module_identityDictionary.get('module_color', '')
    module_id=module_identityDictionary.get('module_id','')
    if not os.path.isfile(configFile):
        msg = f'client config file {configFile} not found...'
        log_message(msg, msgType='WARNING', msgOffset='+1',msgColor=module_color)
        return {}
    else:
        try:
            with open(configFile, 'r') as cfgFile:
                configString=cfgFile.read()
            msg=(f'{module_id}: client config file {configFile} retrieved...')
            log_message(msg, msgType='OK', msgOffset='+1',msgColor=module_color)
            configDict=json.loads(configString)
            return configDict
        except:
            configString = None
            msg = f'{module_id}: client config file {configFile} can not be read'
            log_message(msg, msgType='SYSTEM ERROR', msgOffset='+1',msgColor=module_color)
            return {}
            #raise Exception(errorMsg)
################################################################
def retrieve_configuration_from_file(this_file, this_configuration={}, module_identityDictionary={}, print_enabled=None, filelog_enabled=None, ignoreWarning=None):
    # global thisApp.EXECUTION_MODE

    module_color = module_identityDictionary.get('module_color', '')
    module_id=module_identityDictionary.get('module_id','')
    if not this_file:
        errorMsg = f'{module_ProgramName}.retrieve_module_configuration_from_file: config file not provided'
        if not ignoreWarning:
            log_message(errorMsg, msgType='WARNING', msgOffset='+1', msgColor=module_color)
        return this_configuration
        #raise Exception(errorMsg)

    configFile = this_file
    config_folder = os.path.dirname(this_file)

    if not os.path.isfile(configFile):
        configString = json.dumps(this_configuration, sort_keys=True, indent=4)
        with open(configFile, 'w') as cfgFile:
            cfgFile.write(configString)
        msg = f'{module_id}: config file {configFile} created'
        log_message(msg, msgType='WARNING', msgOffset='+1',msgColor=module_color)
    else:
        try:
            with open(configFile, 'r') as cfgFile:
                configString=cfgFile.read()
            if thisApp.DEBUG_ON:
                log_message(f'{module_id}: config file {configFile} retrieved',msgType='OK',msgOffset='+1',msgColor=module_color)
        except:
            configString = None
            errorMsg = f'{module_id}: config file {configFile} not found'
            log_message(errorMsg, msgType='ERROR', msgOffset='+1',msgColor=module_color)
            raise Exception(errorMsg)
        if configString:
            this_configuration = json.loads(configString)

    msg=f'{module_id}: config folder is [ {config_folder} ]'
    log_message(msg, msgCategory='DEBUG', msgType='info', msgOffset='+1', msgColor=module_color)
    
    configFilePath='?'
    #configFilePath = find_file(configFile, search_Downwards=1, search_Upwards=0, search_SubFolders=False)
    msg=f'{module_id}: config file path is [ {configFilePath} ]'
    log_message(msg, msgCategory='DEBUG', msgType='info', msgOffset='+1', msgColor=module_color)

    if not configFilePath:
        errorMsg = f'{module_id}: config file [{configFile}] not found in config folder [ {config_folder} ]'
        log_message(errorMsg, msgType='SYSTEM ERROR', msgOffset='+1',msgColor=module_color)
        raise Exception(errorMsg)
    
    relativePath = configFilePath.lower().replace(config_folder.lower(),'').replace(configFile.lower(),'')
    msg = f'{module_id}: relative configuration path is [{relativePath}]'
    log_message(msg, msgCategory='DEBUG', msgType='info', msgOffset='+1', msgColor=module_color)

    this_configuration.update({'configFile': configFile})
    this_configuration.update({'configFilePath': configFilePath})

    if thisApp.DEBUG_ON:
        msg = f'{module_id}: configuration imported from [{configFile}]'
        log_message(msg,msgType='OK',msgOffset='+1',msgColor=module_color)

    initTimeStamp = str(datetime.datetime.now())
    this_configuration.update({'initialized':initTimeStamp})

    return this_configuration
#############################################################################
def save_config_to_file(configFile, config_dictionary={}):
    if not configFile:
        return
    if not configFile:
        return
    if not config_dictionary:
        return
    configString = json.dumps(config_dictionary, sort_keys=True, indent=4)
    with open(configFile, 'w') as cfgFile:
        cfgFile.write(configString)
    msg = f'{module_id}: config file {configFile} created'
    log_message(msg, msgType='config', msgOffset='+1',msgColor=Fore.RED)
#############################################################################
def new_config_version(VersionString='', print_enabled=None, filelog_enabled=None, ignoreWarning=None):
    global logServices_config_dictionary
    global config_version
    global config_versionStr
    global config_versionString
    global module_ProgramName
    global module_BaseTimeStamp
    global master_configuration
    global module_id
    if master_configuration.get('initialized'):
        config_version = config_version + 1
        config_versionStr = VersionString 
        config_versionString = config_version_string(config_version=config_version, config_versrionString=config_versionStr, module_BaseTimeStamp='')
        log_message(f'{module_id} new config version', config_versionString, msgType='config', msgOffset='+1', print_enabled=print_enabled, filelog_enabled=filelog_enabled, ignoreWarning=ignoreWarning,msgColor=module_color)

    logServices_config_dictionary.update({'config_version':config_version})
    logServices_config_dictionary.update({'config_versionString':config_versionString})
    logServices_config_dictionary.update({'config_versionStr':config_versionStr})

    return config_versionString
#############################################################################
def set_global_vars_from_dictionary(this_dictionary={},this_name=''):
    global module_id
    global module_color
    global logServices_config_dictionary
    global config_version
    global config_versionStr
    global config_versionString
    global log_current_prefix
    global log_file_name
    global log_errors_file_name
    global log_output_devices
    global log_consolelog_enabled
    global log_filelog_enabled
    global log_ignoreWarning
    global log_console_fix_line_length
    global log_console_line_length
    global log_force_log_warnings
    global log_force_print_warnings
    global log_force_log_errors
    global log_force_print_errors
    global log_force_log_system_errors
    global log_force_print_system_errors
    global log_indent_color
    global log_indent_bgcolor
    global log_indent_char
    global log_indent_tab
    global log_level
    global log_eyecatch
    global log_color_mode
    global logServicesConfigFile
    ix=0
    for k, v in this_dictionary.items():
        ix = ix + 1
        kk = k.replace(' ', '')
        #print (ix,kk,k)
        if type(v) == type(''):
            v = v.replace("\\",'/')
            assign_command = f"{kk} = '{v}'"
        elif type(v) == type(None):
            assign_command = f"{kk} = None"
        else:
            assign_command = f"{kk} = {v}"
        log_message(ix, 'global', assign_command, msgCategory='DEBUG', msgType='config', msgOffset='+1', msgColor=module_color)
        exec(assign_command,globals())

    log_output_devices = get_logServices_OutputDevices(print_enabled=log_consolelog_enabled, filelog_enabled=log_filelog_enabled, output_devices=log_output_devices, ignoreWarning=log_ignoreWarning)
    msg=f'{module_id}: [[{ix} global variables]] imported from dictionary [{this_name}]'
    if thisApp.DEBUG_ON:
        log_message(msg, msgType='info', msgOffset='+1', msgColor=module_color)
#::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
#::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
#::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
# utilities
#::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
#::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
#::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
def option_enabled(options='', what='PRINT'):
    if not what:
        return True
    if what.upper().find('PRINT') >= 0 or what.upper().find('CONS') >= 0:
        if options.upper().find('PRINT') >= 0 or options.upper().find('CONS') >= 0:
            return True
    else:
        if options.upper().find(what.upper().strip()) >= 0:
            return True
    return False
#############################################################################
def get_logServices_OutputDevices(print_enabled='', filelog_enabled='', output_devices='', title='', ignoreWarning=''):
    global log_output_devices

    if output_devices:
        output_devices = output_devices.upper()
    else:
        output_devices = log_output_devices
    if print_enabled == True:
        if not output_devices.find('PRINT') >= 0:
            output_devices = output_devices + ' PRINT'
    if filelog_enabled == True:
        if not output_devices.find('FILE') >= 0:
            output_devices = output_devices + ' FILE'
    if print_enabled == False:
        output_devices = output_devices.replace('PRINT','')
        output_devices = output_devices.replace('CONSOLE','')
    if filelog_enabled == False:
        output_devices = output_devices.replace('FILE','')
    if ignoreWarning == True:
        if not output_devices.find('IGNORE-WARNING') >= 0:
            output_devices = output_devices + ' IGNORE-WARNING'
    if ignoreWarning == False:
        output_devices = output_devices.replace('IGNORE-WARNING','')

    output_devices = output_devices.upper().strip()
    return output_devices
#############################################################################
def get_logServices_MessageColor(msgType=''):
    global log_color_mode
    
    ForeColor = Fore.WHITE
    if log_color_mode in ('COLOR', ''):
        if msgType.upper().find('START') >= 0 or msgType.upper().find('FINISH') >= 0:
            ForeColor = Fore.LIGHTWHITE_EX
        else:
            ForeColor = Fore.WHITE

        if msgType.upper().find('FINISH') >= 0 and msgType.upper().find('OK') >= 0:
            ForeColor = Fore.LIGHTGREEN_EX
        elif msgType.upper().find('ERROR') >= 0 and msgType.upper().find('SYS') >= 0:
            ForeColor = Fore.LIGHTRED_EX
        elif msgType.upper().find('ERROR') >= 0:
            ForeColor = Fore.RED
        elif msgType.upper().find('WARN') >= 0:
            ForeColor = Fore.YELLOW
        elif msgType.upper().find('SUCCESS') >= 0:
            ForeColor = Fore.LIGHTGREEN_EX
        elif msgType.upper().find('RESULT') >= 0:
            ForeColor = Fore.WHITE
        elif msgType.upper().find('OK') >= 0:
            ForeColor = Fore.GREEN
        elif msgType.upper().find('INFO-1X') >= 0:
            ForeColor = Back.MAGENTA
        elif msgType.upper().find('INFO-2X') >= 0:
            ForeColor = Back.BLUE
        elif msgType.upper().find('INFO-3X') >= 0:
            ForeColor = Back.LIGHTBLACK_EX
        elif msgType.upper().find('INFO-1') >= 0:
            ForeColor = Fore.WHITE
        elif msgType.upper().find('INFO-2') >= 0:
            ForeColor = Fore.LIGHTBLUE_EX
        elif msgType.upper().find('INFO-3') >= 0:
            ForeColor = Fore.LIGHTRED_EX
        elif msgType.upper().find('INFO') >= 0:
            ForeColor = Fore.LIGHTBLACK_EX
        elif msgType.upper().find('CONFIG') >= 0:
            ForeColor = Fore.LIGHTYELLOW_EX
        elif msgType.upper().find('DETAIL') >= 0:
            ForeColor = Fore.LIGHTCYAN_EX
        elif msgType.upper().find('MESSAGE') >= 0 or msgType.upper().find('MSG') >= 0:
            ForeColor = Fore.WHITE
        elif msgType.upper().find('EX') >= 0 or msgType.upper().find('LIGHT') >= 0:
            ForeColor = Fore.LIGHTMAGENTA_EX
            if msgType.upper().find('MAGEN') >= 0:
                ForeColor = Fore.LIGHTMAGENTA_EX
            elif msgType.upper().find('BLACK') >= 0:
                ForeColor = Fore.LIGHTBLACK_EX
            elif msgType.upper().find('BLUE') >= 0:
                ForeColor = Fore.LIGHTBLUE_EX
            elif msgType.upper().find('CYAN') >= 0:
                ForeColor = Fore.LIGHTCYAN_EX
            elif msgType.upper().find('GREEN') >= 0:
                ForeColor = Fore.LIGHTGREEN_EX
            elif msgType.upper().find('RED') >= 0:
                ForeColor = Fore.LIGHTRED_EX
            elif msgType.upper().find('WHITE') >= 0:
                ForeColor = Fore.LIGHTWHITE_EX
            elif msgType.upper().find('YELLOW') >= 0:
                ForeColor = Fore.LIGHTYELLOW_EX
        elif msgType.upper().find('BACK') >= 0  or msgType.upper().find('BG') >= 0 or msgType.upper().find('BKG') >= 0:
            ForeColor = Back.MAGENTA
            if msgType.upper().find('MAGEN') >= 0:
                ForeColor = Back.MAGENTA
            elif msgType.upper().find('BLACK') >= 0:
                ForeColor = Back.BLACK
            elif msgType.upper().find('BLUE') >= 0:
                ForeColor = Back.BLUE
            elif msgType.upper().find('CYAN') >= 0:
                ForeColor = Back.CYAN
            elif msgType.upper().find('GREEN') >= 0:
                ForeColor = Back.GREEN
            elif msgType.upper().find('RED') >= 0:
                ForeColor = Back.RED
            elif msgType.upper().find('WHITE') >= 0:
                ForeColor = Back.WHITE
            elif msgType.upper().find('YELLOW') >= 0:
                ForeColor = Back.YELLOW
        elif msgType.upper().find('MAGEN') >= 0:
            ForeColor = Fore.MAGENTA
        elif msgType.upper().find('BLACK') >= 0:
            ForeColor = Fore.BLACK
        elif msgType.upper().find('BLUE') >= 0:
            ForeColor = Fore.BLUE
        elif msgType.upper().find('CYAN') >= 0:
            ForeColor = Fore.CYAN
        elif msgType.upper().find('GREEN') >= 0:
            ForeColor = Fore.GREEN
        elif msgType.upper().find('RED') >= 0:
            ForeColor = Fore.RED
        elif msgType.upper().find('WHITE') >= 0:
            ForeColor = Fore.WHITE
        elif msgType.upper().find('YELLOW') >= 0:
            ForeColor = Fore.YELLOW

    elif log_color_mode.upper() in ('MONO', 'BW'):
        ForeColor = Fore.WHITE
    else:
        ForeColor = log_color_mode
        
    return ForeColor
#############################################################################
def get_logServices_MessageBgColor(msgType=''):
    BackColor = ''
    return BackColor
#############################################################################
def copy_log_file_to_errors_file():
    global log_file_name
    global log_errors_file_name
    shutil.copy2(log_file_name, log_errors_file_name)
    return log_errors_file_name
#############################################################################
def file_delete(thisfile, print_enabled=None, filelog_enabled=None, ignoreWarning=None, msgOffset=None,msgColor=''):
    if not msgOffset:
        msgOffset = '+1'
        
    if thisfile:
        if os.path.isfile(thisfile):
            try:
                os.remove(thisfile)
                msg = f'{thisfile} file deleted.'
                if thisApp.DEBUG_ON:
                    log_message(msg, msgType='info-1',msgOffset=msgOffset, msgColor=msgColor, print_enabled=print_enabled, filelog_enabled=filelog_enabled, ignoreWarning=ignoreWarning)
                return True
            except:
                msg = f'{thisfile} file delete failed.'
                log_message(msg, msgType='error',msgOffset=msgOffset, msgColor=msgColor, print_enabled=print_enabled, filelog_enabled=filelog_enabled, ignoreWarning=ignoreWarning)
                return False
        else:
            msg = f'{thisfile} file for deletion not exists.'
            if thisApp.DEBUG_ON:
                log_message(msg, msgType='warning',msgOffset=msgOffset, msgColor=msgColor, print_enabled=print_enabled, filelog_enabled=filelog_enabled, ignoreWarning=ignoreWarning)
            return True
    else:
        msg = f'{thisfile} file for delete not provided.'
        log_message(msg, msgType='error', msgOffset=msgOffset, msgColor=msgColor, print_enabled=print_enabled, filelog_enabled=filelog_enabled, ignoreWarning=ignoreWarning)
        return False
#############################################################################
def merge_log_files(app_folder_path, new_log_file_name, remove_old_file=True):
    global module_color

    if not app_folder_path:
        app_folder_path = os.path.dirname(__file__)
    if not new_log_file_name:
        return

    # with open(new_log_file_name, 'a+') as newlogFile:
    #     newlogFile.write(f'log for {app_folder_path} {datetime.datetime.now()}\n')
    destination = open(new_log_file_name, 'a+b')
    for logfile in iglob(os.path.join(app_folder_path, '*.log')):
        logfilename = os.path.basename(logfile)
        ok = False
        if logfilename != new_log_file_name:
            if new_log_file_name.lower().find('errors.log') >= 0 or new_log_file_name.lower().find('error.log') >= 0:
                if logfilename.lower().find('errors.log') >= 0 or logfilename.lower().find('error.log') >= 0:
                    ok = True
            else:
                if not (logfilename.lower().find('errors.log') >= 0 or logfilename.lower().find('error.log') >= 0):
                    ok = True
        if ok:
            #destination = open(new_log_file_name, 'a+')
            #shutil.copyfileobj(open(logfilename, 'rb'), open(new_log_file_name, 'a+b'))
            shutil.copyfileobj(open(logfilename, 'rb'), destination)

            old_lines = 0
            if os.path.isfile(logfilename):
                try:
                    with open(logfilename) as logFile:
                        for line in logFile:
                            old_lines = old_lines + 1
                except:
                    pass
            msg=f'{module_id}: {old_lines} lines copied from [{logfilename}] to [{new_log_file_name}]'
            log_message(msg, msgType='configuration',msgOffset='+1',msgColor=module_color)
            if remove_old_file and os.path.isfile(logfilename) and logfilename!=new_log_file_name:
                file_delete(logfilename,msgColor=module_color,msgOffset='+1')
                msg=f'{module_id}: [{logfilename}] deleted after merged to [{new_log_file_name}]'
                log_message(msg, msgType='configuration',msgOffset='+1',msgColor=module_color)

    destination.close()
    new_lines = 0
    if os.path.isfile(new_log_file_name):
        try:
            with open(new_log_file_name) as logFile:
                for line in logFile:
                    new_lines = new_lines + 1
        except:
            pass
    msg=f'{module_id}: {new_lines} lines in [{new_log_file_name}]'
    log_message(msg, msgType='configuration',msgOffset='+1',msgColor=module_color)
#############################################################################
#############################################################################
#############################################################################
#############################################################################
def whoami():
    return inspect.stack()[1][3]
#############################################################################
def whosdaddy():
    return inspect.stack()[2][3]
#############################################################################
def whosdaddy2():
    return inspect.stack()[3][3]
#############################################################################
def call_chain():
    xcaller = sys._getframe(1)  # Obtain calling frame
    xactive_moduleX = xcaller.f_globals['__name__']
    xcaller = sys._getframe(2)  # Obtain calling frame
    xactive_moduleX2 = xcaller.f_globals['__name__']
    # xcaller_prog1 = whosdaddy()
    # xcaller_prog2 = whosdaddy2()
    # xcaller_prog = f'{xcaller_prog2}{xcaller_prog1}'
    i=-1
    p = ''
    #xx[0].f_locals.self.name
    for i in range(1,len(inspect.stack())):
        xx = inspect.stack()[i]
        name = inspect.stack()[i][3]
        function = xx.function
        print('-----',i,function,name)

        z = xx[0]

        z1 = z.f_locals
        try:
            n1 = z.get('name')
            if n1:
                print('#####z####name=',n1)
        except:
            pass
        try:
            n1 = z1.get('name')
            if n1:
                print('#####z1####name=',n1)
        except:
            pass
        #.self.name
        #print(z)
        if function in ('<module>'):
           name= xactive_moduleX
        if function not in ('call_chain','_call_with_frames_removed','exec_module','_load_unlocked','_find_and_load_unlocked','_find_and_load'):
            name = inspect.stack()[i][3]
        else:
            name=None
        if name:
            if p:
                p = p + '|' + name
            else:
                p = name
        # if not name:
        #     break
        
    print('chain:',p)
#############################################################################
def string_datetime_translate(thisString, base_datetime=''):
    global module_BaseTimeStamp
    if not base_datetime:
        dt = module_BaseTimeStamp
    else:
        dt = base_datetime

    lastmonthdt = datetime.date.today() + relativedelta(months=-1)

    thatString = string_macro_enabled(thisString)

    thatString = thatString.replace('#YYYY#', dt.strftime('%Y'))
    thatString = thatString.replace('#MM#', dt.strftime('%m'))
    thatString = thatString.replace('#M#', dt.strftime('%m'))
    thatString = thatString.replace('#CCYY#', dt.strftime('%Y'))
    thatString = thatString.replace('#YY#', str(dt.year)[2:4])
    thatString = thatString.replace('#CC#', str(dt.year)[:2])
    thatString = thatString.replace('#DD#', dt.strftime('%d'))
    thatString = thatString.replace('#D#', dt.strftime('%d'))
    thatString = thatString.replace('#YYYYMMDD#',dt.strftime('%Y')+dt.strftime('%m')+dt.strftime('%d'))
    thatString = thatString.replace('#HHMMSS#',dt.strftime('%H')+dt.strftime('%M')+dt.strftime('%S'))
    thatString = thatString.replace('#MON#', dt.strftime('%b'))
    thatString = thatString.replace('#MONTH#', dt.strftime('%B'))
    thatString = thatString.replace('#WEEKDAY#', dt.strftime('%A'))
    thatString = thatString.replace('#WEEKDAY3#', dt.strftime('%a'))
    thatString = thatString.replace('#DAY#', dt.strftime('%A'))
    thatString = thatString.replace('#DAY3#', dt.strftime('%a'))

    thatString = thatString.replace('#LASTMONTH#', lastmonthdt.strftime('%B'))
    thatString = thatString.replace('#LASTMONTHYEAR#', lastmonthdt.strftime('%Y'))
    thatString = thatString.replace('#LASTMM#', lastmonthdt.strftime('%m'))

    return thatString
#############################################################################
def string_translate_colors(thisString):
    if not isinstance(thisString, str):
        return thisString
    thatString = thisString
    thatString = thatString.replace('Fore.BLACK', Fore.BLACK)
    thatString = thatString.replace('Fore.WHITE', Fore.WHITE)
    thatString = thatString.replace('Fore.YELLOW', Fore.YELLOW)
    thatString = thatString.replace('Fore.BLUE', Fore.BLUE)
    thatString = thatString.replace('Fore.MAGENTA', Fore.MAGENTA)
    thatString = thatString.replace('Fore.GREEN', Fore.GREEN)
    thatString = thatString.replace('Fore.CYAN', Fore.CYAN)
    thatString = thatString.replace('Fore.LIGHTBLACK_EX', Fore.LIGHTBLACK_EX)
    thatString = thatString.replace('Fore.LIGHTWHITE_EX', Fore.LIGHTWHITE_EX)
    thatString = thatString.replace('Fore.LIGHTYELLOW_EX', Fore.LIGHTYELLOW_EX)
    thatString = thatString.replace('Fore.LIGHTBLUE_EX', Fore.LIGHTBLUE_EX)
    thatString = thatString.replace('Fore.LIGHTMAGENTA_EX', Fore.LIGHTMAGENTA_EX)
    thatString = thatString.replace('Fore.LIGHTGREEN_EX', Fore.LIGHTGREEN_EX)
    thatString = thatString.replace('Fore.LIGHTCYAN_EX', Fore.LIGHTCYAN_EX)

    thatString = thatString.replace('Back.BLACK', Back.BLACK)
    thatString = thatString.replace('Back.WHITE', Back.WHITE)
    thatString = thatString.replace('Back.YELLOW', Back.YELLOW)
    thatString = thatString.replace('Back.BLUE', Back.BLUE)
    thatString = thatString.replace('Back.MAGENTA', Back.MAGENTA)
    thatString = thatString.replace('Back.GREEN', Back.GREEN)
    thatString = thatString.replace('Back.CYAN', Back.CYAN)
    thatString = thatString.replace('Back.LIGHTBLACK_EX', Back.LIGHTBLACK_EX)
    thatString = thatString.replace('Back.LIGHTWHITE_EX', Back.LIGHTWHITE_EX)
    thatString = thatString.replace('Back.LIGHTYELLOW_EX', Back.LIGHTYELLOW_EX)
    thatString = thatString.replace('Back.LIGHTBLUE_EX', Back.LIGHTBLUE_EX)
    thatString = thatString.replace('Back.LIGHTMAGENTA_EX', Back.LIGHTMAGENTA_EX)
    thatString = thatString.replace('Back.LIGHTGREEN_EX', Back.LIGHTGREEN_EX)
    thatString = thatString.replace('Back.LIGHTCYAN_EX', Back.LIGHTCYAN_EX)

    thatString = thatString.replace('BLACK', Fore.BLACK)
    thatString = thatString.replace('WHITE', Fore.WHITE)
    thatString = thatString.replace('YELLOW', Fore.YELLOW)
    thatString = thatString.replace('BLUE', Fore.BLUE)
    thatString = thatString.replace('MAGENTA', Fore.MAGENTA)
    thatString = thatString.replace('GREEN', Fore.GREEN)
    thatString = thatString.replace('CYAN', Fore.CYAN)
    thatString = thatString.replace('LIGHTBLACK_EX', Fore.LIGHTBLACK_EX)
    thatString = thatString.replace('LIGHTWHITE_EX', Fore.LIGHTWHITE_EX)
    thatString = thatString.replace('LIGHTYELLOW_EX', Fore.LIGHTYELLOW_EX)
    thatString = thatString.replace('LIGHTBLUE_EX', Fore.LIGHTBLUE_EX)
    thatString = thatString.replace('LIGHTMAGENTA_EX', Fore.LIGHTMAGENTA_EX)
    thatString = thatString.replace('LIGHTGREEN_EX', Fore.LIGHTGREEN_EX)
    thatString = thatString.replace('LIGHTCYAN_EX', Fore.LIGHTCYAN_EX)

    thatString = thatString.replace('Back.RESET', Back.RESET)
    thatString = thatString.replace('Fore.RESET', Fore.RESET)

    return thatString
#############################################################################
def display_value(thisValue=''):
    thatValue = string_with_translated_colors(thisValue)
    if str(thatValue).strip() == '' and len(str(thatValue)) > 0:
        thatValue = '[{}]'.format(thatValue)
    return thatValue
#############################################################################
def string_with_translated_colors(thisString):
    if not isinstance(thisString, str):
        return thisString

    thatString = thisString
    thatString = thatString.replace(Fore.BLACK, 'Fore.BLACK')
    thatString = thatString.replace(Fore.WHITE, 'Fore.WHITE')
    thatString = thatString.replace(Fore.YELLOW, 'Fore.YELLOW')
    thatString = thatString.replace(Fore.BLUE, 'Fore.BLUE')
    thatString = thatString.replace(Fore.MAGENTA, 'Fore.MAGENTA')
    thatString = thatString.replace(Fore.GREEN, 'Fore.GREEN')
    thatString = thatString.replace(Fore.CYAN, 'Fore.CYAN')
    thatString = thatString.replace(Fore.LIGHTBLACK_EX, 'Fore.LIGHTBLACK_EX')
    thatString = thatString.replace(Fore.LIGHTWHITE_EX, 'Fore.LIGHTWHITE_EX')
    thatString = thatString.replace(Fore.LIGHTYELLOW_EX, 'Fore.LIGHTYELLOW_EX')
    thatString = thatString.replace(Fore.LIGHTBLUE_EX, 'Fore.LIGHTBLUE_EX')
    thatString = thatString.replace(Fore.LIGHTMAGENTA_EX, 'Fore.LIGHTMAGENTA_EX')
    thatString = thatString.replace(Fore.LIGHTGREEN_EX, 'Fore.LIGHTGREEN_EX')
    thatString = thatString.replace(Fore.LIGHTCYAN_EX, 'Fore.LIGHTCYAN_EX')

    thatString = thatString.replace(Back.BLACK, 'Back.BLACK')
    thatString = thatString.replace(Back.WHITE, 'Back.WHITE')
    thatString = thatString.replace(Back.YELLOW, 'Back.YELLOW')
    thatString = thatString.replace(Back.BLUE, 'Back.BLUE')
    thatString = thatString.replace(Back.MAGENTA, 'Back.MAGENTA')
    thatString = thatString.replace(Back.GREEN, 'Back.GREEN')
    thatString = thatString.replace(Back.CYAN, 'Back.CYAN')
    thatString = thatString.replace(Back.LIGHTBLACK_EX, 'Back.LIGHTBLACK_EX')
    thatString = thatString.replace(Back.LIGHTWHITE_EX, 'Back.LIGHTWHITE_EX')
    thatString = thatString.replace(Back.LIGHTYELLOW_EX, 'Back.LIGHTYELLOW_EX')
    thatString = thatString.replace(Back.LIGHTBLUE_EX, 'Back.LIGHTBLUE_EX')
    thatString = thatString.replace(Back.LIGHTMAGENTA_EX, 'Back.LIGHTMAGENTA_EX')
    thatString = thatString.replace(Back.LIGHTGREEN_EX, 'Back.LIGHTGREEN_EX')
    thatString = thatString.replace(Back.LIGHTCYAN_EX, 'Back.LIGHTCYAN_EX')

    thatString = thatString.replace(Fore.RESET, 'Fore.RESET')
    thatString = thatString.replace(Back.RESET, 'Back.RESET')

    return thatString
#############################################################################
def string_macro_enabled(String, dictionary={}):
    thisString = str(String)
    slen = len(thisString)
    if slen <= 0:
        return thisString
    inmacro = False
    thatString=''
    for i in range(0, slen, +1):
        if thisString[i] == '#':
            inmacro = not inmacro
            thatString = thatString+thisString[i]
        else:
            if inmacro:
                #thisString[i] = thisString[i].upper()
                thatString = thatString+thisString[i].upper()
            else:
                thatString = thatString + thisString[i]
    return thatString
#############################################################################
def string_dictionary_translate(thisString, dictionary={}):
    thatString = string_macro_enabled(thisString)
    for key in dictionary:
        val = str(dictionary[key])
        word = '#{}#'.format(key.upper())
        thatString = thatString.replace(word,val)
    return thatString
#############################################################################
def string_translate(thisString, dictionary={}):
    dt = datetime.datetime.now()
    thatString1 = string_datetime_translate(thisString, dt)
    thatString2 = string_dictionary_translate(thatString1, dictionary)
    return thatString2
#############################################################################
def dictionary_translated_value(thisKey='', dictionary={}):
    thisString = dictionary.get(thisKey)
    if thisString:
        thatString1 = string_datetime_translate(thisString)
        thatString2 = string_dictionary_translate(thatString1, dictionary)
        return thatString2
    else:
        return thisString
#############################################################################
def config_version_string(config_version=None, config_versrionString='', module_BaseTimeStamp=''):
    msg1 = ''
    msg2 = ''
    msg3 = ''
    if config_version:
        msg2 = 'config version {}'.format(config_version)
        if config_versrionString:
            msg2 = 'config version {} ({})'.format(config_version, config_versrionString)
    else:
        if config_versrionString:
            msg2 = 'config version 0 ({})'.format(config_versrionString)
    if module_BaseTimeStamp:
        msg3 = 'baseTimeStamp:{}'.format(module_BaseTimeStamp)
    versionStr = '{} {} {}'.format(msg1, msg2, msg3).strip()
    return versionStr
#############################################################################
#############################################################################
#############################################################################
# def get_fore_color_based_onBackground(bgcolor,colorindex):
#     global back_colors_dict
#     global fore_colors_dict
#     global color_names
#     global light_colors
#     global dark_colors
#     global fore_color_names_dict
#     global back_color_names_dict
#     bgcolor_index = back_colors_dict.get(bgcolor,{}).get('index',0)
#     bgcolor_name = color_names[bgcolor_index]
#     if bgcolor_name in light_colors:
#         ix = colorindex % len(dark_colors)
#         fgcolor_name = dark_colors[ix]
#         fgcolor = fore_color_names_dict.get(fgcolor_name,{}).get('color','')
#     else:
#         ix = colorindex % len(light_colors)
#         fgcolor_name = light_colors[ix]
#         fgcolor = fore_color_names_dict.get(fgcolor_name,{}).get('color','')
#     return fgcolor
#############################################################################
# def get_back_color_based_onForeground(fgcolor,colorindex):
#     global back_colors_dict
#     global fore_colors_dict
#     global color_names
#     global light_colors
#     global dark_colors
#     global fore_color_names_dict
#     global back_color_names_dict
#     fgcolor_index = fore_colors_dict.get(fgcolor,{}).get('index',0)
#     fgcolor_name = color_names[fgcolor_index]
#     if fgcolor_name in light_colors:
#         ix = colorindex % len(dark_colors)
#         bgcolor_name = dark_colors[ix]
#         bgcolor = back_color_names_dict.get(bgcolor_name,{}).get('color','')
#     else:
#         ix = colorindex % len(light_colors)
#         bgcolor_name = light_colors[ix]
#         bgcolor = back_color_names_dict.get(bgcolor_name,{}).get('color','')
#     return bgcolor
#############################################################################
# def make_colors_array():
#     global fore_colors
#     global back_colors
#     global color_names
#     global fore_colors_dict
#     global back_colors_dict
#     global light_colors
#     global dark_colors
#     global fore_color_names_dict
#     global back_color_names_dict

#     fore_colors
#     fore_colors = []
#     fore_colors.append(Fore.WHITE)
#     fore_colors.append(Fore.YELLOW)
#     fore_colors.append(Fore.BLUE)
#     fore_colors.append(Fore.MAGENTA)
#     fore_colors.append(Fore.GREEN)
#     fore_colors.append(Fore.CYAN)
#     fore_colors.append(Fore.LIGHTWHITE_EX)
#     fore_colors.append(Fore.LIGHTYELLOW_EX)
#     fore_colors.append(Fore.LIGHTBLUE_EX)
#     fore_colors.append(Fore.LIGHTMAGENTA_EX)
#     fore_colors.append(Fore.LIGHTGREEN_EX)
#     fore_colors.append(Fore.LIGHTCYAN_EX)
#     fore_colors.append(Fore.BLACK)
#     fore_colors.append(Fore.LIGHTBLACK_EX)
#     fore_colors_dict = {}
#     fore_colors_dict.update({Fore.WHITE:{'index':0,'darkness':0,'lightness':0,'name':'WHITE'}})
#     fore_colors_dict.update({Fore.YELLOW:{'index':1,'darkness':0,'lightness':0,'name':'YELLOW'}})
#     fore_colors_dict.update({Fore.BLUE:{'index':2,'darkness':0,'lightness':0,'name':'BLUE'}})
#     fore_colors_dict.update({Fore.MAGENTA:{'index':3,'darkness':0,'lightness':0,'name':'MAGENTA'}})
#     fore_colors_dict.update({Fore.GREEN:{'index':4,'darkness':0,'lightness':0,'name':'GREEN'}})
#     fore_colors_dict.update({Fore.CYAN:{'index':5,'darkness':0,'lightness':0,'name':'CYAN'}})
#     fore_colors_dict.update({Fore.LIGHTWHITE_EX:{'index':6,'darkness':0,'lightness':0,'name':'LIGHTWHITE_EX'}})
#     fore_colors_dict.update({Fore.LIGHTYELLOW_EX:{'index':7,'darkness':0,'lightness':0,'name':'LIGHTYELLOW_EX'}})
#     fore_colors_dict.update({Fore.LIGHTBLUE_EX:{'index':8,'darkness':0,'lightness':0,'name':'LIGHTBLUE_EX'}})
#     fore_colors_dict.update({Fore.LIGHTMAGENTA_EX:{'index':9,'darkness':0,'lightness':0,'name':'LIGHTMAGENTA_EX'}})
#     fore_colors_dict.update({Fore.LIGHTGREEN_EX:{'index':10,'darkness':0,'lightness':0,'name':'LIGHTGREEN_EX'}})
#     fore_colors_dict.update({Fore.LIGHTCYAN_EX:{'index':11,'darkness':0,'lightness':0,'name':'LIGHTCYAN_EX'}})
#     fore_colors_dict.update({Fore.BLACK:{'index':12,'darkness':12,'lightness':0,'name':'BLACK'}})
#     fore_colors_dict.update({Fore.LIGHTBLACK_EX:{'index':13,'darkness':0,'lightness':0,'name':'LIGHTBLACK_EX'}})

#     fore_color_names_dict = {}
#     fore_color_names_dict.update({'WHITE': {'index': 0, 'color': Fore.WHITE}})
#     fore_color_names_dict.update({'YELLOW': {'index': 1, 'color': Fore.YELLOW}})
#     fore_color_names_dict.update({'BLUE': {'index': 2, 'color': Fore.BLUE}})
#     fore_color_names_dict.update({'MAGENTA': {'index': 3, 'color': Fore.MAGENTA}})
#     fore_color_names_dict.update({'GREEN': {'index': 4, 'color': Fore.GREEN}})
#     fore_color_names_dict.update({'CYAN': {'index': 5, 'color': Fore.CYAN}})
#     fore_color_names_dict.update({'LIGHTWHITE_EX': {'index': 6, 'color': Fore.LIGHTWHITE_EX}})
#     fore_color_names_dict.update({'LIGHTYELLOW_EX': {'index': 7, 'color': Fore.LIGHTYELLOW_EX}})
#     fore_color_names_dict.update({'LIGHTBLUE_EX': {'index': 8, 'color': Fore.LIGHTBLUE_EX}})
#     fore_color_names_dict.update({'LIGHTMAGENTA_EX': {'index': 9, 'color': Fore.LIGHTMAGENTA_EX}})
#     fore_color_names_dict.update({'LIGHTGREEN_EX': {'index': 10, 'color': Fore.LIGHTGREEN_EX}})
#     fore_color_names_dict.update({'LIGHTCYAN_EX': {'index': 11, 'color': Fore.LIGHTCYAN_EX}})
#     fore_color_names_dict.update({'BLACK': {'index': 12, 'color': Fore.BLACK}})
#     fore_color_names_dict.update({'LIGHTBLACK_EX': {'index': 13, 'color': Fore.LIGHTBLACK_EX}})

#     back_colors = []
#     back_colors.append(Back.WHITE)
#     back_colors.append(Back.YELLOW)
#     back_colors.append(Back.BLUE)
#     back_colors.append(Back.MAGENTA)
#     back_colors.append(Back.GREEN)
#     back_colors.append(Back.CYAN)
#     back_colors.append(Back.LIGHTWHITE_EX)
#     back_colors.append(Back.LIGHTYELLOW_EX)
#     back_colors.append(Back.LIGHTBLUE_EX)
#     back_colors.append(Back.LIGHTMAGENTA_EX)
#     back_colors.append(Back.LIGHTGREEN_EX)
#     back_colors.append(Back.LIGHTCYAN_EX)
#     back_colors.append(Back.BLACK)
#     back_colors.append(Back.LIGHTBLACK_EX)
#     back_colors_dict = {}
#     back_colors_dict.update({Back.WHITE:{'index':0,'darkness':0,'lightness':0,'name':'WHITE'}})
#     back_colors_dict.update({Back.YELLOW:{'index':1,'darkness':0,'lightness':0,'name':'YELLOW'}})
#     back_colors_dict.update({Back.BLUE:{'index':2,'darkness':1,'lightness':0,'name':'BLUE'}})
#     back_colors_dict.update({Back.MAGENTA:{'index':3,'darkness':1,'lightness':0,'name':'MAGENTA'}})
#     back_colors_dict.update({Back.GREEN:{'index':4,'darkness':1,'lightness':0,'name':'GREEN'}})
#     back_colors_dict.update({Back.CYAN:{'index':5,'darkness':1,'lightness':0,'name':'CYAN'}})
#     back_colors_dict.update({Back.LIGHTWHITE_EX:{'index':6,'darkness':0,'lightness':0,'name':'LIGHTWHITE_EX'}})
#     back_colors_dict.update({Back.LIGHTYELLOW_EX:{'index':7,'darkness':0,'lightness':0,'name':'LIGHTYELLOW_EX'}})
#     back_colors_dict.update({Back.LIGHTBLUE_EX:{'index':8,'darkness':0,'lightness':0,'name':'LIGHTBLUE_EX'}})
#     back_colors_dict.update({Back.LIGHTMAGENTA_EX:{'index':9,'darkness':0,'lightness':0,'name':'LIGHTMAGENTA_EX'}})
#     back_colors_dict.update({Back.LIGHTGREEN_EX:{'index':10,'darkness':0,'lightness':0,'name':'LIGHTGREEN_EX'}})
#     back_colors_dict.update({Back.LIGHTCYAN_EX:{'index':11,'darkness':0,'lightness':0,'name':'LIGHTCYAN_EX'}})
#     back_colors_dict.update({Back.BLACK:{'index':12,'darkness':12,'lightness':0,'name':'BLACK'}})
#     back_colors_dict.update({Back.LIGHTBLACK_EX:{'index':13,'darkness':0,'lightness':0,'name':'LIGHTBLACK_EX'}})

#     back_color_names_dict = {}
#     back_color_names_dict.update({'WHITE': {'index': 0, 'color': Back.WHITE}})
#     back_color_names_dict.update({'YELLOW': {'index': 1, 'color': Back.YELLOW}})
#     back_color_names_dict.update({'BLUE': {'index': 2, 'color': Back.BLUE}})
#     back_color_names_dict.update({'MAGENTA': {'index': 3, 'color': Back.MAGENTA}})
#     back_color_names_dict.update({'GREEN': {'index': 4, 'color': Back.GREEN}})
#     back_color_names_dict.update({'CYAN': {'index': 5, 'color': Back.CYAN}})
#     back_color_names_dict.update({'LIGHTWHITE_EX': {'index': 6, 'color': Back.LIGHTWHITE_EX}})
#     back_color_names_dict.update({'LIGHTYELLOW_EX': {'index': 7, 'color': Back.LIGHTYELLOW_EX}})
#     back_color_names_dict.update({'LIGHTBLUE_EX': {'index': 8, 'color': Back.LIGHTBLUE_EX}})
#     back_color_names_dict.update({'LIGHTMAGENTA_EX': {'index': 9, 'color': Back.LIGHTMAGENTA_EX}})
#     back_color_names_dict.update({'LIGHTGREEN_EX': {'index': 10, 'color': Back.LIGHTGREEN_EX}})
#     back_color_names_dict.update({'LIGHTCYAN_EX': {'index': 11, 'color': Back.LIGHTCYAN_EX}})
#     back_color_names_dict.update({'BLACK': {'index': 12, 'color': Back.BLACK}})
#     back_color_names_dict.update({'LIGHTBLACK_EX': {'index': 13, 'color': Back.LIGHTBLACK_EX}})
    
#     color_names = []
#     color_names.append('WHITE')
#     color_names.append('YELLOW')
#     color_names.append('BLUE')
#     color_names.append('MAGENTA')
#     color_names.append('GREEN')
#     color_names.append('CYAN')
#     color_names.append('LIGHTWHITE_EX')
#     color_names.append('LIGHTYELLOW_EX')
#     color_names.append('LIGHTBLUE_EX')
#     color_names.append('LIGHTMAGENTA_EX')
#     color_names.append('LIGHTGREEN_EX')
#     color_names.append('LIGHTCYAN_EX')
#     color_names.append('BLACK')
#     color_names.append('LIGHTBLACK_EX')

#     dark_colors=['BLUE','MAGENTA','GREEN','CYAN','BLACK','LIGHTBLUE_EX','LIGHTMAGENTA_EX','LIGHTGREEN_EX','LIGHTCYAN_EX','LIGHTBLACK_EX']
#     light_colors=[]
#     for c in color_names:
#         if c not in dark_colors:
#             light_colors.append(c)
#::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
#::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
#::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
# module inititialization
#::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
#::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
#::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
master_configuration = retrieve_module_configuration(module_identityDictionary, module_configuration=master_configuration, print_enabled=None, filelog_enabled=None)
cfgfile=module_ProgramName+'.cfg'
set_global_vars_from_dictionary(logServices_config_dictionary,cfgfile)
logServices_config_dictionary = retrieve_configuration_from_file(logServicesConfigFile, this_configuration=master_configuration, module_identityDictionary=module_identityDictionary, print_enabled=None, filelog_enabled=None,ignoreWarning=True)
#make_colors_array()
if logServices_config_dictionary != master_configuration:
    set_global_vars_from_dictionary(logServices_config_dictionary,logServicesConfigFile)
    master_configuration = logServices_config_dictionary.copy()
if thisApp.DEBUG_ON:
    msg=f'{module_id}: log_file set to [ {log_file_name}]'
    log_message(msg,msgType='info',msgOffset='+1',msgColor=module_color)
    msg=f'{module_id}: [consolelog_enabled]: [[{log_consolelog_enabled}]], [filelog_enabled]: [[{log_filelog_enabled}]], [ignoreWarning]: [[{log_ignoreWarning}]]'
    log_message(msg,msgType='info',msgOffset='+1',msgColor=module_color)

log_module_initialization_message(module_identityDictionary)
#::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
#::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
#::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
# main (for testing)
#::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
#::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
#::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
# if __name__ == '__main__':
#     print(__file__)
#     print(Fore)
#     #print(Fore[0])

#     print('x')