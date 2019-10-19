import os
import sys
if not (os.path.dirname(__file__) in sys.path): sys.path.append(os.path.dirname(__file__))

import fnmatch
import hashlib
import random
import re
import shutil
import pathlib
import time
import datetime
from datetime import timedelta
from datetime import date
from dateutil.relativedelta import relativedelta
from dateutil.parser import parse
from decimal import Decimal
from colorama import init as ColorsInit, Fore, Back, Style
from fpdf import FPDF
from _appEnvironment import CONSOLE_ON, FILELOG_ON,EXECUTION_MODE,Fore
from _logServices import log_message,log_module_initialization_message
# import tempfile
# from pdf2image import convert_from_path
# import PythonMagick
#::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
#::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
#::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
#module
#::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
#::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
#::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
module_Function = 'general utility services'
module_ProgramName = '_utilities'
module_BaseTimeStamp = datetime.datetime.now()
module_folder = os.getcwd()
module_color = Fore.GREEN
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
    'module_color':module_color,
    'module_folder':module_folder,
    'module_id':module_id,
    'module_eyecatch':module_eyecatch,
    'module_version':module_version,
    'module_versionString':module_versionString,
    'module_log_file_name':module_log_file_name,
    'module_errors_file_name':module_errors_file_name,
}
master_configuration = {
}
# log options
log_print_enabled=CONSOLE_ON
log_filelog_enabled=FILELOG_ON
log_file_name = module_log_file_name
log_errors_file_name = module_errors_file_name
#::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
#::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
#::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
# services
#::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
#::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
#::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
def random_string(type=''):
    this_string = ''
    if type.upper().find('HEX') >= 0:
        for ix1 in range(0, 4):
            if this_string:
                this_string = this_string + '-'
            for ix2 in range(0, 8):
                xc = '0123456789ABCDEF'
                r = random.randint(0, 15)
                c=xc[r]
                this_string = this_string + c
    else:
        for ix1 in range(0, 4):
            if this_string:
                this_string = this_string + '-'
            for ix2 in range(0, 8):
                a = random.randint(ord('A'), ord('Z'))
                c = str(chr(a))
                this_string = this_string + c
    return this_string
#############################################################################
def get_rand_string(length=12, allowed_chars='0123456789abcdef'):
    """
    Returns a securely generated random string. Taken from the Django project

    The default length of 12 with the a-z, A-Z, 0-9 character set returns
    a 71-bit value. log_2((26+26+10)^12) =~ 71 bits
    """
    if not using_sysrandom:
        # This is ugly, and a hack, but it makes things better than
        # the alternative of predictability. This re-seeds the PRNG
        # using a value that is hard for an attacker to predict, every
        # time a random string is required. This may change the
        # properties of the chosen random sequence slightly, but this
        # is better than absolute predictability.
        random.seed(
            hashlib.sha256(
                ("%s%s" % (
                    random.getstate(),
                    time.time())).encode('utf-8')
            ).digest())
    return ''.join([random.choice(allowed_chars) for i in range(length)])
#############################################################################
def make_msg_id():
    """
    Create a semi random message id, by using 12 char random hex string and
    a timestamp.
    @return: string consisting of timestamp, -, random value
    """
    random_string = get_rand_string(12)
    timestamp = time.strftime("%Y%m%d%I%M%S")
    msg_id = timestamp + "-" + random_string
    return msg_id
#############################################################################
def make_id(name):
    """
    Create a random id combined with the creditor name.
    @return string consisting of name (truncated at 22 chars), -,
    12 char rand hex string.
    """
    name = re.sub(r'[^a-zA-Z0-9]', '', name)
    r = get_rand_string(12)
    if len(name) > 22:
        name = name[:22]
    return name + "-" + r
#############################################################################
def int_to_decimal_str(integer):
    """
    Helper to convert integers (representing cents) into decimal currency
    string. WARNING: DO NOT TRY TO DO THIS BY DIVISION, FLOATING POINT
    ERRORS ARE NO FUN IN FINANCIAL SYSTEMS.
    @param integer The amount in cents
    @return string The amount in currency with full stop decimal separator
    """
    int_string = str(integer)
    if len(int_string) < 2:
        return "0." + int_string.zfill(2)
    else:
        return int_string[:-2] + "." + int_string[-2:]
#############################################################################
def decimal_str_to_int(decimal_string):
    """
    Helper to decimal currency string into integers (cents).
    WARNING: DO NOT TRY TO DO THIS BY CONVERSION AND MULTIPLICATION,
    FLOATING POINT ERRORS ARE NO FUN IN FINANCIAL SYSTEMS.
    @param string The amount in currency with full stop decimal separator
    @return integer The amount in cents
    """
    int_string = decimal_string.replace('.', '')
    int_string = int_string.lstrip('0')
    return int(int_string)
#############################################################################
def str_to_decimal(str):
    dec = Decimal(str.replace(',', '.'))
    return dec
#############################################################################
#############################################################################
def display_value(thisValue=''):
    thatValue = string_with_translated_colors(thisValue)
    if str(thatValue).strip() == '' and len(str(thatValue)) > 0:
        thatValue = '[{}]'.format(thatValue)
    return thatValue
#############################################################################
#############################################################################
def translate_configuration(config={}, thisdict={}, title='', print_enabled='', filelog_enabled=''):
    res = translate_dictionary(this_dict=config, translation_dict=thisdict, print_enabled=print_enabled, filelog_enabled=filelog_enabled, title=title)
    return res
#############################################################################
def translate_dictionary(this_dict={}, translation_dict={}, title='', print_enabled='', filelog_enabled=True):
    # if title:
    #     _logServices.log_message(title, msgType='start', print_enabled=print_enabled, filelog_enabled=filelog_enabled)

    dt = module_BaseTimeStamp
    ix = 0
    it = 0
    for key in this_dict:
        ix += 1
        thisValue = this_dict[key]
        if thisValue and isinstance(thisValue, str):
            thatValue = string_datetime_translate(thisValue, base_datetime=dt).strip()
            thatValue = string_dictionary_translate(thatValue, dictionary=translation_dict).strip()
            if thisValue != thatValue:
                this_dict.update({key: thatValue})
                it = it + 1
                msg = '{}={} from {}'.format(key, thatValue, thisValue)
                #_logServices.log_message(msg, msgType='info', msgOffset='+1', print_enabled=print_enabled, filelog_enabled=filelog_enabled)

    resmsg = '{}/{} entries translated'.format(it, ix)
    # if title:
    #     _logServices.log_message(resmsg, msgType='finish', print_enabled=print_enabled, filelog_enabled=filelog_enabled)
    # else:
    #     _logServices.log_message(resmsg, msgType='RESULT', msgOffset='+1', print_enabled=print_enabled, filelog_enabled=filelog_enabled)
    return resmsg
#############################################################################
#############################################################################
def find_file(thisFileName='', thisDir='', search_Downwards=1, search_Upwards=0, search_SubFolders=False):
    found = False
    if not thisFileName:
        return None

    if not thisDir:
        thisDir = os.getcwd()

    thisFile = None

    #################search downwards####################
    if search_Downwards > 0 and search_Downwards <= search_Upwards:
        found = False
        fdir = os.path.dirname(thisFileName)
        fname = os.path.basename(thisFileName)
        if fdir:
            if os.path.isfile(thisFileName):
                found = True
                dirpath = fdir
                thisFileName = fname
        else:
            if not search_SubFolders:
                #print('dn-1',thisDir)
                basepath = thisDir
                dirpath = basepath
                for entry in os.listdir(basepath):
                    if os.path.isfile(os.path.join(basepath, thisFileName)):
                        found = True
                        break
                if found:
                    thisFile = os.path.join(dirpath, thisFileName)
                    if os.path.isfile(thisFile):
                        return thisFile
            else:
                for dirpath, dirnames, files in os.walk(thisDir, topdown=True):
                    #print('dn-2',dirpath)
                    #print(f'Found directory: {dirpath}')
                    for file_name in files:
                        #print(file_name)
                        if file_name.upper() == thisFileName.upper():
                            found = True
                            break
                    if found:
                        break
        if found:
            thisFile = os.path.join(dirpath, thisFileName)
            if os.path.isfile(thisFile):
                return thisFile
    #################search upwards ####################
    if search_Upwards > 0:
        prev_thisFolder = '*'
        thisFolder = thisDir
        #os.path.abspath(os.path.dirname(thisfile))
        xthisFile = os.path.join(thisFolder, thisFileName)
        ix = 0
        while not os.path.isfile(xthisFile) and ix <= 1000000 and thisFolder != prev_thisFolder:
            ix = ix + 1
            #print('up',ix,thisFolder,prev_thisFolder)
            prev_thisFolder = thisFolder
            thisFolder = os.path.abspath(os.path.dirname(thisFolder))
            xthisFile = os.path.join(thisFolder, thisFileName)
        if os.path.isfile(xthisFile):
            thisFile = xthisFile
            return thisFile    

    #################search downwards after upwards####################
    if search_Downwards > 0 and search_Downwards > search_Upwards:
        found = False
        fdir = os.path.dirname(thisFileName)
        fname = os.path.basename(thisFileName)
        if fdir:
            if os.path.isfile(thisFileName):
                found = True
                dirpath = fdir
                thisFileName = fname
        else:
            if search_SubFolders:
                basepath = thisDir
                dirpath = basepath
                for entry in os.listdir(basepath):
                    if os.path.isfile(os.path.join(basepath, thisFileName)):
                        found = True
                        break
            else:
                for dirpath, dirnames, files in os.walk(thisDir, topdown=True):
                    #print(f'Found directory: {dirpath}')
                    for file_name in files:
                        #print(file_name)
                        if file_name.upper() == thisFileName.upper():
                            found = True
                            break
                    if found:
                        break
        if found:
            thisFile = os.path.join(dirpath, thisFileName)
            if os.path.isfile(thisFile):
                return thisFile
        else:
            return None
#############################################################################
def file_delete(thisfile, print_enabled=None, filelog_enabled=None, ignoreWarning=None, msgOffset=None):
    if not msgOffset:
        msgOffset = '+1'
        
    if thisfile:
        if os.path.isfile(thisfile):
            try:
                os.remove(thisfile)
                msg = f'{thisfile} file deleted.'
                log_message(msg, msgType='info-1',msgOffset=msgOffset, print_enabled=print_enabled, filelog_enabled=filelog_enabled, ignoreWarning=ignoreWarning)
                return True
            except:
                msg = f'{thisfile} file delete failed.'
                log_message(msg, msgType='error',msgOffset=msgOffset, print_enabled=print_enabled, filelog_enabled=filelog_enabled, ignoreWarning=ignoreWarning)
                return False
        else:
            msg = f'{thisfile} file for deletion not exists.'
            log_message(msg, msgType='warning',msgOffset=msgOffset, print_enabled=print_enabled, filelog_enabled=filelog_enabled, ignoreWarning=ignoreWarning)
            return True
    else:
        msg = f'{thisfile} file for delete not provided.'
        log_message(msg, msgType='error', msgOffset=msgOffset, print_enabled=print_enabled, filelog_enabled=filelog_enabled, ignoreWarning=ignoreWarning)
        return False
#############################################################################
def string_datetime_translate(thisString, base_datetime=''):
    global module_BaseTimeStamp
    if not base_datetime:
        dt = module_BaseTimeStamp
    else:
        dt = base_datetime

    now = datetime.datetime.now()
    
    lastmonthdt = date.today() + relativedelta(months=-1)

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

    thatString = thatString.replace('#TODAY#', now.strftime('%A, %b %d %H:%M:%S %Y'))

    #A, %b %d %H:%M:%S %YYYY
    # %c	Locale’s appropriate date and time representation.	Mon Sep 30 07:06:05 2013
    
    return thatString
    # Directive	Meaning	Example
    # %a	Abbreviated weekday name.	Sun, Mon, ...
    # %A	Full weekday name.	Sunday, Monday, ...
    # %w	Weekday as a decimal number.	0, 1, ..., 6
    # %d	Day of the month as a zero-padded decimal.	01, 02, ..., 31
    # %-d	Day of the month as a decimal number.	1, 2, ..., 30
    # %b	Abbreviated month name.	Jan, Feb, ..., Dec
    # %B	Full month name.	January, February, ...
    # %m	Month as a zero-padded decimal number.	01, 02, ..., 12
    # %-m	Month as a decimal number.	1, 2, ..., 12
    # %y	Year without century as a zero-padded decimal number.	00, 01, ..., 99
    # %-y	Year without century as a decimal number.	0, 1, ..., 99
    # %Y	Year with century as a decimal number.	2013, 2019 etc.
    # %H	Hour (24-hour clock) as a zero-padded decimal number.	00, 01, ..., 23
    # %-H	Hour (24-hour clock) as a decimal number.	0, 1, ..., 23
    # %I	Hour (12-hour clock) as a zero-padded decimal number.	01, 02, ..., 12
    # %-I	Hour (12-hour clock) as a decimal number.	1, 2, ... 12
    # %p	Locale’s AM or PM.	AM, PM
    # %M	Minute as a zero-padded decimal number.	00, 01, ..., 59
    # %-M	Minute as a decimal number.	0, 1, ..., 59
    # %S	Second as a zero-padded decimal number.	00, 01, ..., 59
    # %-S	Second as a decimal number.	0, 1, ..., 59
    # %f	Microsecond as a decimal number, zero-padded on the left.	000000 - 999999
    # %z	UTC offset in the form +HHMM or -HHMM.	 
    # %Z	Time zone name.	 
    # %j	Day of the year as a zero-padded decimal number.	001, 002, ..., 366
    # %-j	Day of the year as a decimal number.	1, 2, ..., 366
    # %U	Week number of the year (Sunday as the first day of the week). All days in a new year preceding the first Sunday are considered to be in week 0.	00, 01, ..., 53
    # %W	Week number of the year (Monday as the first day of the week). All days in a new year preceding the first Monday are considered to be in week 0.	00, 01, ..., 53
    # %c	Locale’s appropriate date and time representation.	Mon Sep 30 07:06:05 2013
    # %x	Locale’s appropriate date representation.	09/30/13
    # %X	Locale’s appropriate time representation.	07:06:05
    # %%	A literal '%' character.	%
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
def send_outlook_email(to='foo@gmail.com', cc='', subject='subject', Body='', HTMLBody='', attachment='', attachment1='', attachment2='', attachment3='', attachment4='', attachment5=''):
    import win32com.client as win32

    if not subject:
        subject = 'hi...'

    outlook = win32.Dispatch('outlook.application')
    mail = outlook.CreateItem(0)
    mail.To = to
    mail.Subject = subject 
    if cc:
        mail.Cc = cc
    if Body:     
        mail.Body = Body
    if HTMLBody:
        mail.HTMLBody = HTMLBody

    # To attach a file to the email (optional):
    if attachment:
        mail.Attachments.Add(attachment)
    if attachment1:
        mail.Attachments.Add(attachment1)
    if attachment2:
        mail.Attachments.Add(attachment2)
    if attachment3:
        mail.Attachments.Add(attachment3)
    if attachment4:
        mail.Attachments.Add(attachment4)
    if attachment5:
        mail.Attachments.Add(attachment5)

    #mail.Send() or mail.display()
    mail.display()
#############################################################################
def display_errors_file(errors_file):
    try:
        f = open(errors_file, "r")
        text = f.readlines()
        f.close()
        #_dialogServices.textshowbox("errors:" + errors_file, "", text)        
    except:
        return
#############################################################################
def display_results_file(logFile):
    try:
        f = open(logFile, "r")
        text = f.readlines()
        f.close()
        #_dialogServices.textshowbox("results:" + logFile, "", text)        
    except:
        return
#############################################################################
def display_file(logFile, title=''):
    if not title:
        title = "Show File Contents"
    try:
        f = open(logFile, "r")
        text = f.readlines()
        f.close()
        #_dialogServices.textshowbox(logFile, title, text)        
    except:
        return
#############################################################################
def display_configuration_options(module_id='[module_id]', config_dictionary={}, config_dictionary_prev={}, msgOffset='', msgColor='', outputOption='changes', print_enabled=True, filelog_enabled=False):
    if not outputOption:
        outputOption = 'FULL'

    if not filelog_enabled:
        filelog_enabled = False
    if str(filelog_enabled).upper() in ('NONE', 'OFF', 'FALSE'):
        filelog_enabled = False
    else:
        filelog_enabled = True
    if not print_enabled:
        print_enabled = False
    if str(print_enabled).upper() in ('NONE', 'OFF', 'FALSE'):
        print_enabled = False
    else:
        print_enabled = True

    for key in sorted(config_dictionary):
        if outputOption.upper() in ('CHANGES', 'DIFFERENTIAL'):
            if str(config_dictionary.get(key)).upper() != str(config_dictionary_prev.get(key)).upper():
                msg = '{} = {}'.format(key, config_dictionary.get(key))
                msg = '{} = {} (from:{})'.format(key, config_dictionary.get(key), config_dictionary_prev.get(key))
                msgP = f'{msgColor}{msgOffset} {module_id} {msg}{Fore.RESET}'
                log_message(msg, msgType='info',msgOffset='+1')
                # if print_enabled:
                #     print(msg)
        else:
            if outputOption.upper() not in ('NONE', 'OFF', 'FALSE'):
                msg = '{} = {}'.format(key, config_dictionary.get(key))
                #log_message(module_id, msg, msgType='configuration', filelog_enabled=filelog_enabled, print_enabled=True)
                msgP = f'{msgColor}{msgOffset} {module_id} {msg}{Fore.RESET}'
                #if print_enabled:
                #    print(msg)
            else:
                msg = '{} = {}'.format(key, config_dictionary.get(key))
                msgP = f'{msgColor}{msgOffset} {module_id} {msg}{Fore.RESET}'
                if print_enabled:
                    print(msg)
#############################################################################
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
def display_pdf(pdf_file=None):
    if not pdf_file:
        return False

    # base_filename  =  os.path.splitext(os.path.basename(pdf_file))[0] + '.tif'     
    # outfile = os.path.join(save_dir, base_filename)

    import webbrowser
    
    new = 2 # open in a new tab, if possible
    pdf_file_fullpath = find_file(pdf_file)
    url='file://'+pdf_file_fullpath #/C:/Users/User/Documents/my%20Projects/Development/python-sepaxml/SepaPaymentsXML_journal.pdf
    # open a public URL, in this case, the webbrowser docs
    #url = "http://docs.python.org/library/webbrowser.html"
    webbrowser.open(url,new=new)
    return True
    # open an HTML file on my own (Windows) computer
    #url = "file://X:/MiscDev/language_links.html"
    #webbrowser.open(url,new=new)
#############################################################################
def value_is_valid(val='', validationRules={}, tryoption=False):
    if not isinstance(validationRules, dict):
        return True
    values = validationRules.get('values')
    if values:
        xvalues = values.upper().split(',')
        values_list = map(str.strip, xvalues)
        if val.upper() in values_list:
            ok1 = True
        else:
            msg = 'must be in range {}'.format(values_list)
            ok1 = False
    else:
        ok1 = True

    value_range = validationRules.get('range')
    if value_range:
        value_range_list = value_range.split(',')
        v1 = value_range_list[0].strip()
        v2 = value_range_list[1].strip()
        if val >= v1 and val<= v2:
            ok2 = True
        else:
            msg = 'must be in range {}'.format(value_range_list)
            ok2 = False
    else:
        ok2 = True

    excludevalues = validationRules.get('exclude')
    if excludevalues:
        xvalues = excludevalues.upper().split(',')
        excludevalues_list = map(str.strip, xvalues)
        if val in excludevalues_list:
            msg = 'must not be in {}'.format(excludevalues_list)
            ok3 = False
        else:
            ok3 = True
    else:
        ok3 = True

    specialOptions = validationRules.get('options')
    if specialOptions:
        xvalues = specialOptions.upper().split(',')
        specialOptions_list = map(str.strip, xvalues)
        ok4 = True
        for option in specialOptions_list:
            if option == 'NOTEMPTY' and not val:
                ok4 = False
                msg = 'must not be empty'
                break
            elif option == 'EMPTY' and val:
                ok4 = False
                msg = 'must be empty'
                break
            elif option in ('ON-OFF', 'ONOFF') and val.upper() not in ('ON', 'OFF'):
                msg = 'must be ON or OFF'
                ok4 = False
                break
            elif option == 'NUMERIC' and not val.isnumeric():
                msg = 'must be numeric'
                ok4 = False
                break
            elif option == 'DATE' and not val.isnumeric():
                try:
                    parse(val)
                    ok4 = True
                except ValueError as error:
                    msg = error
                    ok4 = False
                    break
            elif option == 'ALPHA' and not val.isalpha():
                msg = 'must be alphabetic'
                ok4 = False
                break
            elif option == 'ALPHANUMERIC' and not val.isalnum():
                msg = 'must be alphanumeric'
                ok4 = False
                break
            elif option in ('DIGIT', 'INTEGER') and not val.isdigit():
                msg = 'must be integer'
                ok4 = False
                break
            elif option == 'BOOLEAN' and not val.isinstance(val, bool):
                msg = 'must be True or False'
                ok4 = False
                break
    else:
        ok4 = True
    ok = ok1 and ok2 and ok3 and ok4
    if tryoption:
        if ok:
            return 'OK'
        else:
            return msg
    else:
        return ok
#############################################################################
def boolean_to_ONOFF(val=''):
    if str(val).upper() in ('TRUE', 'FALSE'):
        if str(val).upper() == 'TRUE':
            thatValue = 'ON'
        else:
            thatValue = 'OFF'
        return thatValue
    else:
        return val
#############################################################################
def read_input_fields(title='', msg='', inputFields=[]):
    #2. setup screen for exasygui
    
    fieldNames = []
    fieldValues = []
    fieldTypes = []
    fieldDefaultValues = []
    fieldisMandatory = []
    fieldvalueValidation = []
    
    for i in range(0, len(inputFields), +1):
        if str(inputFields[i][1]).upper() in ('ONOFF','ON-OFF'):
            inputFields[i][1]=boolean_to_ONOFF(inputFields[i][2])
        field = inputFields[i]
        fieldNames.append(inputFields[i][0])
        fieldValues.append(inputFields[i][1])
        fieldTypes.append(inputFields[i][2].upper().strip())
        fieldisMandatory.append(inputFields[i][3].upper().strip())
        fieldDefaultValues.append(inputFields[i][4])
        fieldvalueValidation.append(inputFields[i][5])
        
    #3. read user input with exasygui
    #fieldValues = _dialogServices.multipleinputbox(msg, title, fieldNames, fieldValues)

    #4.validate fields
    errmsg = ""
    while True:
        errmsg = ""
        #fieldValues = _dialogServices.multipleinputbox(msg, title, fieldNames, fieldValues)
        if not fieldValues: #cancel requested
            break
        for i in range(0, len(fieldNames), +1):
            #default values:
            if not fieldValues[i] and fieldDefaultValues[i]:
                fieldValues[i] = fieldDefaultValues[i]
            #data type: ONOFF
            if fieldTypes[i]in ('ONOFF','ON-OFF'):
                if fieldValues[i].upper() not in ('ON', 'OFF'):
                    fieldValues[i] = 'OFF'
            #mandatory fields
            if str(fieldisMandatory[i]).strip().upper() in ('TRUE', 'MANDATORY', 'M', '*'):
                if not fieldValues[i]:
                    errmsg = errmsg + '"{}" is a required field.\n'.format(fieldNames[i])
            #validation
            if fieldvalueValidation[i]:
                if not value_is_valid(val=fieldValues[i], validationRules=fieldvalueValidation[i], tryoption=False):
                    msg = value_is_valid(val=fieldValues[i], validationRules=fieldvalueValidation[i], tryoption=True)
                    errmsg = errmsg + '"{}" values {}.\n'.format(fieldNames[i], msg)
        if errmsg == "":
            break
    #end of while loop

    if not fieldValues: #cancel requested
        return None
    outFields=[]
    for i in range(0, len(inputFields), +1):
        outFields.append({'fieldName':fieldNames[i], 'fieldValue':fieldValues[i]})
    return outFields
#############################################################################
def get_folder(title='select folder', path='', name='', basefolder=''):
    if not basefolder:
        basefolder = os.getcwd()
    if not path:
        path = basefolder
    thisFolder = os.path.join(path, name)
    #path = _dialogServices.diropenbox(title=title, default=thisFolder)
    if path:
        if not name:
            thisFolderPath = os.path.dirname(path)
            thisFolderName = os.path.basename(path)
        else:
            thisFolderPath = path
            thisFolderName = name
            if thisFolderName.upper() == os.path.basename(path).upper():
                thisFolderPath = os.path.dirname(path)
        thisFolder= os.path.join(thisFolderPath, thisFolderName)
        thisRelativeFolderPath = thisFolderPath.replace(basefolder,'')
        # msg = 'path={} name={} rel={} full={}'.format(thisFolderPath, thisFolderName, thisRelativeFolderPath, thisFolder)
        # _dialogServices.msgbox(msg=msg, title=title, ok_button='OK', image=None, root=None)
        return {'folder_path': thisFolderPath, 'folder_name': thisFolderName, 'folder': thisFolder, 'relative_folder': thisRelativeFolderPath}
    else:
        return None
#############################################################################
def utility_json_to_FieldsAndValues(jsonExpr, top_fieldNames=[], top_fieldValues=[], bottom_fieldNames=[], bottom_fieldValues=[]):
    fieldNames = []
    fieldValues = []

    for ix in range(0, len(top_fieldNames)):
        fieldNames.append(top_fieldNames[ix])
        fieldValues.append(top_fieldValues[ix])

    for key in jsonExpr:
        val = jsonExpr.get(key)
        if str(val).strip().lower() not in('','string','none'):
            if not isinstance(val,(list, dict, tuple)):
                fieldNames.append(key)
                fieldValues.append(jsonExpr.get(key))
            else:
                nkey = f'{key} '
                values = jsonExpr.get(key)
                for subkey in values:
                    if isinstance(subkey,str):
                        subval = values.get(subkey)
                        if str(subval).strip().lower() not in('','string','none'):
                            nkey =f"{key} {subkey}"
                            fieldNames.append(nkey)
                            fieldValues.append(subval)
                    else:
                        subval = subkey
                        nkey =f"{key}"
                        fieldNames.append(nkey)
                        fieldValues.append(subval)

    for ix in range(0, len(bottom_fieldNames)):
        fieldNames.append(bottom_fieldNames[ix])
        fieldValues.append(bottom_fieldValues[ix])

    return({'fieldNames':fieldNames,'fieldValues':fieldValues})
##########################################################
def utility_json_to_FieldsAndValues_fieldsOnly(jsonExpr, top_fieldNames=[], top_fieldValues=[], bottom_fieldNames=[], bottom_fieldValues=[]):
    fieldNames = []
    fieldValues = []

    for ix in range(0, len(top_fieldNames)):
        fieldNames.append(top_fieldNames[ix])
        fieldValues.append(top_fieldValues[ix])

    for key in jsonExpr:
        val = jsonExpr.get(key)
        if str(val).strip().lower() not in('','string','none'):
            if not isinstance(val,(list, dict, tuple)):
                fieldNames.append(key)
                fieldValues.append(jsonExpr.get(key))
            elif type(val) == type([]): #arrays of strings included
                if len(val) > 0:
                    val2 = val[0]
                    if not isinstance(val2, (list, dict, tuple)):
                        fieldNames.append(key)
                        fieldValues.append(jsonExpr.get(key))

    for ix in range(0, len(bottom_fieldNames)):
        fieldNames.append(bottom_fieldNames[ix])
        fieldValues.append(bottom_fieldValues[ix])

    return({'fieldNames':fieldNames,'fieldValues':fieldValues})
##########################################################
def xutility_json_to_FieldsAndValues(jsonExpr={}):
    fieldNames = []
    fieldValues=[]
    for key in jsonExpr:
        val = jsonExpr.get(key)
        if str(val).strip().lower() not in('','string','none'):
            if not isinstance(val,(list, dict, tuple)):
                fieldNames.append(key)
                fieldValues.append(jsonExpr.get(key))
            else:
                nkey = f'{key} '
                values = jsonExpr.get(key)
                for subkey in values:
                    if isinstance(subkey,str):
                        subval = values.get(subkey)
                        if str(subval).strip().lower() not in('','string','none'):
                            nkey =f"{key} {subkey}"
                            fieldNames.append(nkey)
                            fieldValues.append(subval)
                    else:
                        subval = subkey
                        nkey =f"{key}"
                        fieldNames.append(nkey)
                        fieldValues.append(subval)

    return({'fieldNames':fieldNames,'fieldValues':fieldValues})
################################################################
# def retrieve_module_configuration(module_identityDictionary, module_configuration={}, print_enabled=DEFAULT, filelog_enabled=DEFAULT):
#     module_file = module_identityDictionary.get('module_file', '')
#     module_log_file_name = module_identityDictionary.get('module_log_file_name', '')
#     module_errors_file_name = module_identityDictionary.get('module_errors_file_name', '')
#     module_id = module_identityDictionary.get('module_id', '')
#     module_version = module_identityDictionary.get('module_version', '')
#     log_message('', msgType='start',print_enabled=print_enabled)
#     set_log_options(print_enabled=CONSOLE_ON, filelog_enabled=ON, logfile_name=module_log_file_name, ignoreWarning=OFF, makeNewVersion=OFF)
#     file_delete(module_log_file_name, print_enabled=DEFAULT, ignoreWarning=DEFAULT)
#     file_delete(module_errors_file_name, print_enabled=DEFAULT, ignoreWarning=DEFAULT)
#     module_configuration.update({'initialized':None})
#     new_module_configuration = retrieve_module_configuration_from_file(module_file, module_configuration)
#     if not new_module_configuration.get('initialized', None):
#         msg=f'{module_id} FAILED TO INITIALIZED'
#         log_message(msg, msgType='finish', msgColor=Fore.RED, print_enabled=CONSOLE_ON, filelog_enabled=ON)
#     else:
#         msg = f'module [{module_id}] version {module_version} loaded.'
#         log_message(msg, msgType='finish', msgColor=module_color, print_enabled=CONSOLE_ON, filelog_enabled=ON)
#     return new_module_configuration
# ###############################################################################################################
# def retrieve_module_configuration_from_file(this_file, this_configuration={}):
#     global module_ProgramName
#     if not this_file:
#         this_file = __file__
#         errorMsg = f'{module_ProgramName}.retrieve_module_configuration_from_file(): module file not provided'
#         log_message(errorMsg, msgType='SYSTEM ERROR', msgOffset='+1')
#         raise Exception(errorMsg)
#     config = configparser.ConfigParser()
#     DeviceIniFile = find_file('device.ini', search_Downwards=1, search_Upwards=0, search_SubFolders=False)
#     if not DeviceIniFile:
#         DeviceIniFile = find_file('server.ini', search_Downwards=1, search_Upwards=0, search_SubFolders=False)
#     if DeviceIniFile:
#         config.read(DeviceIniFile)
#         environment = config.get('DEFAULT', 'ENVIRONEMNT').lower()
#         if not environment:
#             environment = 'production'
#         msg=f'environment set to {environment}'
#         log_message(msg,msgType='info-1',msgOffset='+1')
#     else:
#         environment = 'sandbox'
#         msg=f'device.ini or server.ini not found. environment set to sandbox'
#         log_message(msg,msgType='WARNING',msgOffset='+1')

#     moduleProgramName = os.path.splitext(os.path.basename(this_file))[0]
#     configFile = f'{moduleProgramName}_{environment}.cfg'
#     config_folder = os.path.dirname(this_file)

#     if not os.path.isfile(configFile):
#         configString=json.dumps(this_configuration)
#         with open(configFile, 'w') as cfgFile:
#             cfgFile.write(configString)
#         msg = f'config file {configFile} created'
#         log_message(msg, msgType='WARNING', msgOffset='+1')
#     else:
#         try:
#             with open(configFile, 'r') as cfgFile:
#                 configString=cfgFile.read()
#             log_message(f'config file {configFile} retrieved',msgType='OK',msgOffset='+1')
#         except:
#             configString = None
#             errorMsg = f'config file {configFile} not found'
#             log_message(errorMsg, msgType='ERROR', msgOffset='+1')
#             raise Exception(errorMsg)
#         if configString:
#             this_configuration = json.loads(configString)
#             # msg = f'{moduleProgramName} configuration in {configFile}={this_configuration}'
#             # log_message(msg,this_configuration)

#     msg=f'config folder is [ {config_folder} ]'
#     log_message(msg,msgType='info',msgOffset='+1')

#     configFilePath = find_file(configFile, search_Downwards=1, search_Upwards=0, search_SubFolders=False)
#     this_configuration.update({'configFilePath': configFilePath})
#     msg=f'config file path is [ {configFilePath} ]'
#     log_message(msg,msgType='info',msgOffset='+1')

#     if not configFilePath:
#         errorMsg = f'config file [{configFile}] not found in config folder [ {config_folder} ]'
#         log_message(errorMsg, msgType='SYSTEM ERROR', msgOffset='+1')
#         raise Exception(errorMsg)
#     relativePath = configFilePath.lower().replace(config_folder.lower(),'').replace(configFile.lower(),'')
#     msg = f'relative configuration path is [{relativePath}]'
#     log_message(msg, msgType='info', msgOffset='+1')
    
#     msg = f'configuration imported from [{configFile}]'
#     log_message(msg,msgType='OK',msgOffset='+1')

#     initTimeStamp = str(datetime.datetime.datetime.now())
#     this_configuration.update({'initialized':initTimeStamp})

#     return this_configuration
# ################################################################
# def read_client_configuration_dictionary_from_file(configFile):
#     if not os.path.isfile(configFile):
#         msg = f'client config file {configFile} not found...'
#         log_message(msg, msgType='WARNING', msgOffset='+1')
#         return {}
#     else:
#         try:
#             with open(configFile, 'r') as cfgFile:
#                 configString=cfgFile.read()
#             msg=(f'client config file {configFile} retrieved...')
#             log_message(msg, msgType='OK', msgOffset='+1')
#             configDict=json.loads(configString)
#             return configDict
#         except:
#             configString = None
#             msg = f'client config file {configFile} can not be read'
#             log_message(msg, msgType='SYSTEM ERROR', msgOffset='+1')
#             return {}
#             #raise Exception(errorMsg)
###############################################################################################################
def module_version_string(module_id='', module_version=1.1, module_BaseTimeStamp='', config_version=None, config_versrionString=''):
    msg1 = ''
    msg2 = ''
    msg3 = ''
    if module_id:
        msg1 = '{} version {}'.format(module_id, module_version)
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
###############################################################################################################
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
def ulog_message(msg1='', msg2='', msg3='', msg4='', msg5='', msgType='', msgOffset='AUTO', logFile='', logFileInit=False, msgColor='', msgBkgr='', output_devices='', print_enabled=None, filelog_enabled=None, ignoreWarning=''):
    global module_color
    global module_ProgramName
    global log_file_name
    global log_errors_file_name
    global log_print_enabled
    global log_filelog_enabled
    log_indent_bgcolor=Back.BLACK
    log_indent_color = msgColor
    log_indent_char = 'o'
    log_level = 0
    log_indent_tab = '   '
    log_current_prefix = '   '
    log_console_line_length = 99999
    ignoreWarning = OFF
    if not print_enabled:
        print_enabled = log_print_enabled
    if not filelog_enabled:
        filelog_enabled = log_filelog_enabled
    if print_enabled:
        output_devices = 'CONSOLE PRINT'
    if filelog_enabled:
        output_devices = f'{output_devices} FILE'
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

    if not (msgType.upper().find('START') >=0 or msgType.upper().find('FINISH') >= 0):
        if msgType.upper().find('WARN') >= 0:
            msg = 'warning: {} {} {} {} {}'.format(msg1, msg2, msg3, msg4, msg5)
        elif msgType.upper().find('ERROR') >= 0 and msgType.upper().find('SYS') >= 0:
            msg = 'system error: {} {} {} {} {}'.format(msg1, msg2, msg3, msg4, msg5)
            output_devices = f'{output_devices} FILE PRINT CONSOLE'
            msgColor=Fore.LIGHTRED_EX
        elif msgType.upper().find('ERROR') >= 0:
            msg = 'error: {} {} {} {} {}'.format(msg1, msg2, msg3, msg4, msg5)
            output_devices = f'{output_devices} FILE {CONSOLE_ON}'
            msgColor=Fore.LIGHTRED_EX
    msg1 = msg.strip()

    msgPrefix = log_current_prefix
    if msgOffset.upper() == 'AUTO':
        msgPrefix = '   '*log_level
    elif msgOffset in ('+0', '0'):
        msgPrefix = log_current_prefix
    elif msgOffset == '+1':
        msgPrefix = log_current_prefix + '   ' #' {} '.format(log_indent_char)
    elif msgOffset == '-1':
        ln = len(log_current_prefix) - len(log_indent_tab)
        if ln > 0:
            msgPrefix = log_current_prefix[:ln]
        else:
            msgPrefix = ''

    msg = '{}{}'.format(msgPrefix, msg1)

    #for file log
    msgF = '{}\n'.format(msg)
    
    #for printing
    msgP = msg1 #without prefix
    if len(msgP) > log_console_line_length:
        msgP = msgP[:log_console_line_length-3] + '...'
    
    #coloring
    if msgColor:
        msgP = '{}{}{}{}'.format(msgColor, msgP, Back.RESET, Fore.RESET)
    else:
        msgColor = module_color #get_logServices_MessageColor(msgType)
        msgP = '{}{}{}{}'.format(msgColor, msgP, Back.RESET, Fore.RESET)

    #background coloring
    if msgBkgr:
        msgP = '{}{}{}'.format(msgBkgr, msgP, Back.RESET)
    else:
        msgBkgr = Fore.BLACK #get_logServices_MessageBgColor(msgType)
        if msgBkgr:
            msgP = '{}{}{}'.format(msgBkgr, msgP, Back.RESET)

    #for printing +1
    if msgOffset == '+1':
        msgPrefix = log_current_prefix + '{}{}{}{}{} '.format(log_indent_bgcolor, log_indent_color, log_indent_char, Fore.RESET, Back.RESET)
        #msgPrefix = log_current_prefix + ' {} '.format(log_indent_char)

    msgP = '{}{}'.format(msgPrefix, msgP)

    #log to logFile
    if output_devices.upper().find('FILE') >= 0:
        if not logFile:
            logFile = log_file_name
        if logFileInit == True:
            try:
                os.remove(logFile)
            except:
                dummy = 1
        if not isEmpty:
            f = open(logFile, "a+")
            f.write(msgF)
            f.close

        if msgType.upper().find('ERROR') >= 0:
            errorsFile = log_errors_file_name
            if errorsFile:
                f = open(errorsFile, "a+")
                f.write(msgF)
                f.close

    #print or concole write
    if not isEmpty:
        if output_devices.upper().find('PRINT') >= 0 or output_devices.upper().find('CONSOLE') >= 0:
            if not msgType.upper().find('WARN') >= 0 and not output_devices.upper().find('IGNORE-WARNING') >= 0: #ignore warnings
                #print(msgP, log_level, msgOffset, msgType, logFile, xactive_moduleX)
                print(msgP)

    #actions after print or log
    if msgType.upper().find('START') >=0:
        msgPrefix = log_current_prefix + log_indent_tab
        log_current_prefix = msgPrefix
        log_level = log_level + 1

    if msgOffset not in ('+1'):
        log_current_prefix = msgPrefix

# def display_configuration_dictionary(this_dictionary={},this_title='dictionary display',this_message='this dictionary...'):
#     while True:
#         config_keys = []
#         val_entries = []
#         val_type = ''
#         keys_chain = []
#         for key in sorted(this_dictionary):
#             val = this_dictionary.get(key)
#             cfgEntry = f'{key} : {val}'
#             config_keys.append(cfgEntry)
#         selectedKey = _dialogServices.choicebox(this_message, this_title, choices=config_keys)
#         if not selectedKey:
#             break
#         configkey = selectedKey.split(':')[0].strip()
#         configval = this_dictionary.get(configkey)

#         if isinstance(configval, (list,tuple)):
#             val_type='list'
#             for entry in configval:
#                 ix = configval.index(entry)
#                 estr=f'{ix}: {entry}'
#                 val_entries.append(estr)
#         elif isinstance(configval,(dict)):
#             val_type='dict'
#             for key in sorted(configval):
#                 val = configval.get(key)
#                 ventry = f'{key}:{val}'
#                 val_entries.append(ventry)
#         if not val_entries:
#             continue

#         keys_chain.append({'key':configkey,'type':val_type})
#         prev_val_entries = val_entries
#         prev_val_type = val_type
#         prev_keys_chain=keys_chain
#         while val_entries and val_type in ('dict','list'):
#             #keys_chain.append({'key':configkey,'type':val_type})
#             xkey = ''
#             ix=0
#             for kk in keys_chain:
#                 key = kk.get('key')
#                 valtype = kk.get('type')
#                 if not xkey:
#                     xkey = f'{key}({valtype})'
#                 else:
#                     offset='...'*ix
#                     xkey = f'{xkey}\n{offset}{key}({valtype})'
#                 ix = ix + 1
                
#             msg = f'{this_message}:\n{xkey}'

#             selectedKey = _dialogServices.choicebox(msg, this_title, choices=val_entries)
#             if not selectedKey:
#                 break
#             if val_type == 'dict':
#                 configkey = selectedKey.split(':')[0].strip()
#                 #configval = selectedKey.split(':')[1]
#                 val = this_dictionary
#                 valtype = ''
#                 for kk in keys_chain:
#                     key = kk.get('key')
#                     valtype = kk.get('type') 
#                     val = val.get(key)
#                 configval = val
#                 #valtype = valtype
#             if val_type == 'list':
#                 ix  = int(selectedKey.split(':')[0].strip())
#                 # configval = selectedKey.split(':')[1]
#                 val = this_dictionary
#                 valtype = ''
#                 for kk in keys_chain:
#                     key = kk.get('key')
#                     valtype = kk.get('type') 
#                     val = val.get(key)
#                 configval = val[ix]

#             valtype = '?'
#             if isinstance(configval, (list,tuple)):
#                 valtype='list'
#             elif isinstance(configval,(dict)):
#                 valtype='dict'

#             if valtype in ('dict','list'):
#                 new_val_entries = []
#                 new_val_type = ''
#                 if isinstance(configval, (list)):
#                     new_val_type='list'
#                     for entry in configval:
#                         ix = configval.index(entry)
#                         estr=f'{ix}: {entry}'
#                         new_val_entries.append(estr)
#                 elif isinstance(configval,(dict)):
#                     new_val_type='dict'
#                     for key in sorted(configval):
#                         val = configval.get(key)
#                         ventry = f'{key}:{val}'
#                         new_val_entries.append(ventry)
                
#                 if len(new_val_entries) > 0:
#                     prev_val_entries = val_entries
#                     prev_val_type = val_type
#                     prev_keys_chain=keys_chain
#                     val_entries = new_val_entries
#                     val_type = new_val_type
#                     keys_chain.append({'key':configkey,'type':val_type})

#::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
#::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
#::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
# module inititialization
#::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
#::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
#::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
ColorsInit(convert=True)
try:
    random = random.SystemRandom()
    using_sysrandom = True
except NotImplementedError:
    import warnings
    warnings.warn('A secure pseudo-random number generator is not available '
                  'on your system. Falling back to Mersenne Twister.')
    using_sysrandom = False
file_delete(module_log_file_name,print_enabled=CONSOLE_ON,filelog_enabled=FILELOG_ON, ignoreWarning=True)
file_delete(module_errors_file_name,print_enabled=CONSOLE_ON,filelog_enabled=FILELOG_ON, ignoreWarning=True)
module_Config_Initialized = True
msgLog = f'module [{module_id}] version {module_version} loaded.'
msg = f'{module_color}module [{module_id}] version {module_version} loaded.{Fore.RESET}'
if CONSOLE_ON:
    log_module_initialization_message(module_identityDictionary)
#::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
#::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
#::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
# main (for testing)
#::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
#::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
#::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
#::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
if __name__ == '__main__':
    print(__file__)
