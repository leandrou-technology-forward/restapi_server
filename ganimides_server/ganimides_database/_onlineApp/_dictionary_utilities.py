import os
import sys
import colorama
from colorama import Fore as colors,Back as bgcolors
if sys.stdout.isatty():
    colorama.init(autoreset=True)
else:
    # We're being piped, so skip colors
    colorama.init(strip=True) 

FgColor0 = colors.LIGHTBLACK_EX
FgColor1 = colors.YELLOW
FgColor2 = colors.WHITE
FgColor3 = colors.LIGHTBLUE_EX
FgColor4 = colors.MAGENTA
FgColor5 = colors.CYAN
FgColor6 = colors.GREEN
FgColor7 = colors.RED
FgColor8 = colors.LIGHTWHITE_EX
FgColor9 = colors.LIGHTBLUE_EX
colors_array=[
    ['#C0#',FgColor0],
    ['#C1#',FgColor1],
    ['#C2#',FgColor2],
    ['#C3#',FgColor3],
    ['#C4#',FgColor4],
    ['#C5#',FgColor5],
    ['#C6#',FgColor6],
    ['#C7#',FgColor7],
    ['#C8#',FgColor8],
    ['#C9#',FgColor9],
    ['#RED#',colors.RED],
    ['#GREEN#',colors.GREEN],
    ['#BLUE#',colors.BLUE],
    ['#WHITE#',colors.WHITE],
    ['#GRAY#',colors.LIGHTBLACK_EX],
    ['#MAGENTA#',colors.MAGENTA],
    ['#CYAN#',colors.CYAN],
    ['#ERROR#',colors.RED],
    ['#WARNING#',colors.MAGENTA],
    ['#OK#',colors.GREEN],
    ['#RESET#',colors.RESET],
]
default_colors_template = {
    'prefix': {'key_color': colors.YELLOW, 'data_color': colors.LIGHTRED_EX},
    '1stlevel': {'key_color': colors.BLUE, 'data_color': colors.YELLOW},
    '2ndlevel': {'key_color': colors.CYAN, 'data_color': colors.MAGENTA},
    'suffix': {'key_color': colors.WHITE, 'data_color': '\n'},
    'old_value': {'key_color': colors.LIGHTBLACK_EX, 'data_color': colors.MAGENTA},
    'new_value': {'key_color': colors.LIGHTBLACK_EX, 'data_color': colors.YELLOW},
    'alpha': {'key_color': colors.WHITE, 'data_color': colors.GREEN},
    'beta': {'key_color': colors.WHITE, 'data_color': colors.CYAN},
    'success': {'key_color': colors.WHITE, 'data_color': colors.GREEN},
    'error': {'key_color': colors.WHITE, 'data_color': colors.RED},
    }
colors_template_result = {
    'prefix': {'key_color': colors.YELLOW, 'data_color': colors.GREEN},
    '1stlevel': {'key_color': colors.BLUE, 'data_color': colors.YELLOW},
    '2ndlevel': {'key_color': colors.CYAN, 'data_color': colors.MAGENTA},
    'suffix': {'key_color': colors.WHITE, 'data_color': colors.WHITE},
    'api_data': {'key_color': colors.LIGHTBLUE_EX, 'data_color': colors.MAGENTA},
    'success': {'key_color': colors.WHITE, 'data_color': colors.GREEN},
    'error': {'key_color': colors.WHITE, 'data_color': colors.RED},
    'warning': {'key_color': colors.WHITE, 'data_color': colors.LIGHTRED_EX},
    }
colors_template_changes = {
    'prefix': {'key_color': colors.YELLOW, 'data_color': colors.LIGHTRED_EX},
    '1stlevel': {'key_color': colors.BLUE, 'data_color': colors.YELLOW},
    '2ndlevel': {'key_color': colors.CYAN, 'data_color': colors.MAGENTA},
    'suffix': {'key_color': colors.WHITE, 'data_color': ''},
    'old_value': {'key_color': colors.LIGHTBLACK_EX, 'data_color': colors.MAGENTA},
    'new_value': {'key_color': colors.LIGHTBLACK_EX, 'data_color': colors.YELLOW},
    }
########################################################
def print_data_dict(heading_string, data_dict, colors_template={}):
    c0 = colors.LIGHTBLACK_EX
    c1 = colors.BLUE
    c2 = colors.GREEN
    c3 = colors.RED
    cd=colors.YELLOW
    c1 = default_colors_template.get('1stlevel',{}).get('key_color',colors.BLUE)
    c2 = default_colors_template.get('1stlevel', {}).get('data_color', colors.WHITE)
    is_success = False
    is_error = False
    is_warning=False
    previous_key = ""

    if not data_dict:
        msg = f"{colors.YELLOW}" + "{"+'}' + colors.RESET
    else:
        msg=f"{colors.YELLOW}"+"{\n"

        for k in data_dict:
            if not k=='api_data':
                ck = default_colors_template.get(k,{}).get('key_color',c1)
                cd = default_colors_template.get(k, {}).get('data_color', c2)
                if k == 'api_message':
                    if is_success:
                        cd = colors.GREEN
                    elif is_error:
                        cd = colors.RED
                    elif is_warning:
                        cd=colors.MAGENTA
                vv = data_dict.get(k)
                v = get_printformatted_data(vv, default_colors_template)
                if k == 'api_status':
                    if v.find('success') >= 0:
                        is_success=True
                    elif v.find('error') >= 0:
                        is_error=True
                    elif v.find('warning') >= 0:
                        is_warning=True
                
                msg1 = f"{c0}'{ck}{k}{c0}':{cd}{v}{c0},"
                if not previous_key:
                    separator=""
                elif (previous_key == 'api_status' and k == 'api_message') or (previous_key == 'api_message' and k == 'api_status'):
                    separator = " "
                elif (previous_key == 'api_action' and k == 'api_name') or (previous_key == 'api_name' and k == 'api_action'):
                    separator = " "
                elif (previous_key.find('rows')>=0 and k.find('rows')>=0):
                    separator = " "
                elif k == 'api_data':
                    separator="\n"
                else:
                    separator="\n"
                msg = msg + separator + msg1
                previous_key = k
            
        k='api_data'
        if k in data_dict.keys():
            ck = default_colors_template.get(k,{}).get('key_color',c1)
            cd = default_colors_template.get(k,{}).get('data_color',c2)
            vv = data_dict.get(k)
            v=get_printformatted_data(vv,default_colors_template)
            msg1 = f"{c0}'{ck}{k}{c0}':{cd}{v}{c0}, \n"
            msg = msg + "\n" +msg1

        msg = msg.strip()
        if msg[-1] == ",":
            msg = msg[0:-1]
        #msg = msg + f"\n{colors.YELLOW}" + "}" + c0 + colors.RESET
        msg = msg + f"{colors.YELLOW}" + "}" + c0 + colors.RESET

    c0 = colors.LIGHTBLACK_EX
    cx = colors.LIGHTBLACK_EX
    c1 = default_colors_template.get('prefix',{}).get('key_color',colors.YELLOW)
    c2 = default_colors_template.get('prefix',{}).get('data_color',colors.GREEN)
    suffix1 = default_colors_template.get('suffix',{}).get('key_color',colors.WHITE)
    suffix2 = default_colors_template.get('suffix', {}).get('data_color', '\n')
    heading_string=apply_colors(heading_string,c0)
    # prefix=f"{c0}{heading_string}{c0}:{colors.RESET}"
    msgP=f"{heading_string}{msg}{suffix1}{suffix2}{colors.RESET}{bgcolors.RESET}"
    print(msgP)
#::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
def get_printformatted_data(data_dict,default_colors_template):
    c0 = colors.LIGHTBLACK_EX
    if type(data_dict)==type([]):
        if not data_dict:
            api_data = f"{colors.LIGHTWHITE_EX}" + "["+']' + colors.RESET
        else:
            api_data = f"{colors.LIGHTWHITE_EX}" + "[\n\t"
            for ix in range(0, len(data_dict)):
                data = data_dict[ix]
                dataix = get_colorformatted_data(data,default_colors_template)
                api_data = api_data + dataix + ",\n\t"
            api_data = api_data.strip()
            if api_data[-1] == ",":
                api_data = api_data[0:-1]
            #api_data = api_data + f"{colors.LIGHTWHITE_EX}" + "\n\t]" + c0 + colors.RESET
            api_data = api_data + f"{colors.LIGHTWHITE_EX}" + "]" + c0 + colors.RESET
    else:
        api_data = get_colorformatted_data(data_dict,default_colors_template)
    return api_data
#::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
def get_colorformatted_data(data, default_colors_template):
    c0 = colors.LIGHTBLACK_EX
    c1 = default_colors_template.get('2ndlevel',{}).get('key_color',colors.BLUE)
    c2 = default_colors_template.get('2ndlevel',{}).get('data_color',colors.WHITE)
    if type(data)==type({}):
        if not data:
            formatted_data = f"{colors.RED}" + "{"+'}' + colors.RESET
        else:
            formatted_data = f"{colors.RED}" + "{"
            for k in data:
                ck = default_colors_template.get(k,{}).get('key_color',c1)
                cd = default_colors_template.get(k,{}).get('data_color',c2)
                v = data.get(k)
                formatted_data = formatted_data + f"{c0}'{ck}{k}{c0}':{cd}{v}{c0}, "
            formatted_data = formatted_data.strip()
            if formatted_data[-1] == ",":
                formatted_data = formatted_data[0:-1]
            formatted_data = formatted_data + f"{colors.RED}" + "}" + c0 + colors.RESET
    else:
        v=str(data)
        cd = default_colors_template.get(v, {}).get('data_color', '')
        formatted_data=f"{cd}{v}{c0}"
    return formatted_data
#::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
def apply_colors(msgP,msgColor=''):
    if not msgColor:
        msgColor=FgColor0
    #msgP=msgP.replace('[o','#C8#').replace('o]','#C0#')
    msgP=msgP.replace('[[[[[[[[','#C8#').replace(']]]]]]]]','#C0#')
    msgP=msgP.replace('[[[[[[[','#C7#').replace(']]]]]]]','#C0#')
    msgP=msgP.replace('[[[[[[','#C6#').replace(']]]]]]','#C0#')
    msgP=msgP.replace('[[[[[','#C5#').replace(']]]]]','#C0#')
    msgP=msgP.replace('[[[[','#C4#').replace(']]]]','#C0#')
    msgP=msgP.replace('[[[','#C3#').replace(']]]','#C0#')
    msgP=msgP.replace('[[','#C2#').replace(']]','#C0#')
    msgP=msgP.replace('[','#C1#').replace(']','#C0#')
    msgP = f"{FgColor0}{msgP}{colors.RESET}{bgcolors.RESET}"

    msgP=msgP.replace('#RESET#',msgColor)
    for ix in range(0, len(colors_array)):
        if not msgP.find('#') >= 0:
            break
        msgP=msgP.replace(colors_array[ix][0],colors_array[ix][1])
    return msgP
#::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
def print_changes(heading, changes_dict):
    print_data_dict(heading,changes_dict,colors_template_changes)
#::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
def print_result(heading, result_dict):
    print_data_dict(heading, result_dict, colors_template_result)
    # print('--------------------------------------------------------')    
#::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
def print_api_result(heading, result_dict):
    print_data_dict(heading, result_dict, colors_template_result)
    print('--------------------------------------------------------')    
#::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
#::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
#::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
def print_message(msgP, msgColor=colors.LIGHTBLACK_EX):
    msgP=apply_colors(msgP,msgColor)
    print(msgP)
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
    xdict = {'gama': {'old_value': 'bbbbbbb', 'new_value': 'sssssssss'},
    'alpha': {'old_value': 'bbbbbbb', 'new_value': 'sssssssss'},
    'beta': {'old_value': 'bbbbbbb', 'new_value': 'sssssssss'},
    'deta': {'old_value': 'bbbbbbb', 'new_value': 'sssssssss'},
    'epsilon':'success',
    'aaaaa':'error',
    }
    default_colors_template = {
        'prefix': {'key_color': colors.YELLOW, 'data_color': colors.LIGHTRED_EX},
        '1stlevel': {'key_color': colors.BLUE, 'data_color': colors.YELLOW},
        '2ndlevel': {'key_color': colors.CYAN, 'data_color': colors.MAGENTA},
        'suffix': {'key_color': colors.WHITE, 'data_color': '\n'},
        'old_value': {'key_color': colors.LIGHTBLACK_EX, 'data_color': colors.MAGENTA},
        'new_value': {'key_color': colors.LIGHTBLACK_EX, 'data_color': colors.YELLOW},
        'alpha': {'key_color': colors.WHITE, 'data_color': colors.GREEN},
        'beta': {'key_color': colors.WHITE, 'data_color': colors.CYAN},
        'success': {'key_color': colors.WHITE, 'data_color': colors.GREEN},
        'error': {'key_color': colors.WHITE, 'data_color': colors.RED},
        }
    print_data_dict('changes',xdict,default_colors_template)