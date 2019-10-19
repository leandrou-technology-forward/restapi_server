import os
import sys
module_ProgramName = os.path.splitext(os.path.basename(__file__))[0]
module_id = '{}'.format(module_ProgramName)
module_version = 0.1
from _colorServices import apply_colors, colorized_string, Fore, Back, Style, default_colors_template, colors_template_result, colors_template_changes, xcolors,clean_colors
import textwrap
import pprint
#::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
#::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
#::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
#globals
#::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
#::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
#::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
global_max_print_line_width = 180
#::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
#::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
#::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
# print services
#::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
#::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
#::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
def print_data_dict(heading_string, data_dict, colors_template={}, printLevel=0):
    TABS=''
    if printLevel > 0:
        TABS = "\t" * printLevel
    c0 = Fore.LIGHTBLACK_EX
    c1 = Fore.BLUE
    c2 = Fore.GREEN
    cd = Fore.YELLOW
    c1 = default_colors_template.get('1stlevel',{}).get('key_color',Fore.BLUE)
    c2 = default_colors_template.get('1stlevel', {}).get('data_color', Fore.WHITE)
    is_success = False
    is_error = False
    is_warning=False
    previous_key = ""
   
    if not data_dict:
        msg = f"{Fore.YELLOW}" + "{"+'}' + Fore.RESET
    else:
        if len(data_dict) == 1:
            msg=f"{Fore.YELLOW}"+"{"
        else:
            msg=f"{Fore.YELLOW}"+"{"

        for k in data_dict:
            if not k=='api_data':
                ck = default_colors_template.get(k,{}).get('key_color',c1)
                cd = default_colors_template.get(k, {}).get('data_color', c2)
                if k == 'api_message':
                    if is_success:
                        cd = Fore.GREEN
                    elif is_error:
                        cd = Fore.RED
                    elif is_warning:
                        cd=Fore.MAGENTA
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
            
        k = 'api_data'
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
        #msg = msg + f"\n{Fore.YELLOW}" + "}" + c0 + Fore.RESET
        msg = msg + f"{Fore.YELLOW}" + "}" + c0 + Fore.RESET

    c0 = Fore.LIGHTBLACK_EX
    c1 = default_colors_template.get('prefix',{}).get('key_color',Fore.YELLOW)
    c2 = default_colors_template.get('prefix',{}).get('data_color',Fore.GREEN)
    suffix1 = default_colors_template.get('suffix',{}).get('key_color',Fore.WHITE)
    suffix2 = default_colors_template.get('suffix', {}).get('data_color', '\n')
    heading_string=apply_colors(heading_string,c0)
    msg=msg.replace('\n','\n'+TABS)
    heading_string=heading_string.replace('\n','\n'+TABS)
    msgP = f"{Style.NORMAL}{heading_string}{msg}{suffix1}{suffix2}{Fore.RESET}{Back.RESET}"   
    print(msgP)
    # print('zzzzzzzzzzzzz')
    # print(TABS.join(textwrap.wrap(msgP, 60)))
#::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
def get_colorized_data_dict(heading_string, data_dict, colors_template={}, printLevel=0):
    c0 = Fore.LIGHTBLACK_EX
    c1 = Fore.BLUE
    c2 = Fore.GREEN
    cd = Fore.YELLOW
    c1 = default_colors_template.get('1stlevel',{}).get('key_color',Fore.BLUE)
    c2 = default_colors_template.get('1stlevel', {}).get('data_color', Fore.WHITE)
    is_success = False
    is_error = False
    is_warning=False
    previous_key = ""
    
    if not data_dict:
        msg = f"{Fore.YELLOW}" + "{"+'}' + Fore.RESET
    else:
        if len(data_dict) == 1:
            msg=f"{Fore.YELLOW}"+"{"
        else:
            msg=f"{Fore.YELLOW}"+"{"

        for k in data_dict:
            if not k=='api_data':
                ck = default_colors_template.get(k,{}).get('key_color',c1)
                cd = default_colors_template.get(k, {}).get('data_color', c2)
                if k == 'api_message':
                    if is_success:
                        cd = Fore.GREEN
                    elif is_error:
                        cd = Fore.RED
                    elif is_warning:
                        cd=Fore.MAGENTA
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
            
        k = 'api_data'
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
        #msg = msg + f"\n{Fore.YELLOW}" + "}" + c0 + Fore.RESET
        msg = msg + f"{Fore.YELLOW}" + "}" + c0 + Fore.RESET

    c0 = Fore.LIGHTBLACK_EX
    c1 = default_colors_template.get('prefix',{}).get('key_color',Fore.YELLOW)
    c2 = default_colors_template.get('prefix',{}).get('data_color',Fore.GREEN)
    suffix1 = default_colors_template.get('suffix',{}).get('key_color',Fore.WHITE)
    suffix2 = default_colors_template.get('suffix', {}).get('data_color', '\n')
    heading_string=apply_colors(heading_string,c0)
    # msg=msg.replace('\n','\n'+TABS)
    msgP = f"{Style.NORMAL}{heading_string}{msg}{suffix1}{suffix2}{Fore.RESET}{Back.RESET}"   
    return msgP
#::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
def get_printformatted_data(data_dict,default_colors_template):
    c0 = Fore.LIGHTBLACK_EX
    if type(data_dict)==type([]):
        if not data_dict:
            api_data = f"{Fore.LIGHTWHITE_EX}" + "["+']' + Fore.RESET
        else:
            if len(data_dict) == 1:
                api_data = f"{Fore.LIGHTWHITE_EX}" + "["
            else:
                api_data = f"{Fore.LIGHTWHITE_EX}" + "[\n\t"
                api_data = f"{Fore.LIGHTWHITE_EX}" + "[\n"
            for ix in range(0, len(data_dict)):
                data = data_dict[ix]
                dataix = get_colorformatted_data(data,default_colors_template)
                api_data = api_data + dataix + ",\n"
            api_data = api_data.strip()
            if api_data[-1] == ",":
                api_data = api_data[0:-1]
            #api_data = api_data + f"{Fore.LIGHTWHITE_EX}" + "\n\t]" + c0 + Fore.RESET
            api_data = api_data + f"{Fore.LIGHTWHITE_EX}" + "]" + c0 + Fore.RESET
    else:
        api_data = get_colorformatted_data(data_dict,default_colors_template)
    return api_data
#::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
def get_colorformatted_data(data, default_colors_template):
    c0 = Fore.LIGHTBLACK_EX
    c1 = default_colors_template.get('2ndlevel',{}).get('key_color',Fore.BLUE)
    c2 = default_colors_template.get('2ndlevel',{}).get('data_color',Fore.WHITE)
    if type(data)==type({}):
        if not data:
            formatted_data = f"{Fore.RED}" + "{"+'}' + Fore.RESET
        else:
            formatted_data = f"{Fore.RED}" + "{"
            for k in data:
                ck = default_colors_template.get(k,{}).get('key_color',c1)
                cd = default_colors_template.get(k,{}).get('data_color',c2)
                v = data.get(k)
                formatted_data = formatted_data + f"{c0}'{ck}{k}{c0}':{cd}{v}{c0}, "
            formatted_data = formatted_data.strip()
            if formatted_data[-1] == ",":
                formatted_data = formatted_data[0:-1]
            formatted_data = formatted_data + f"{Fore.RED}" + "}" + c0 + Fore.RESET
    else:
        v=str(data)
        cd = default_colors_template.get(v, {}).get('data_color', '')
        formatted_data=f"{cd}{v}{c0}"
    return formatted_data
#::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
def text_wrap(msgText, printLevel=0,width=-1):
    indent = "\t" * printLevel
    if width < 20:
        width = global_max_print_line_width
    dedented_text = textwrap.dedent(msgText).strip()
    if printLevel <= 0:
        # new_text = textwrap.fill(dedented_text, initial_indent=indent, subsequent_indent=indent + '\t', break_long_words=True, width=width)
        return msgText
    else:        
        new_text=textwrap.fill(dedented_text, initial_indent=indent, subsequent_indent=indent+'\t',break_long_words=True,width=width)
        return new_text
#::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
def pprint_text_clear(pText):
    if pText[0] == "'" or pText[0] == '"' or pText[0] == '(':
        pText = pText[1:]
    if pText[-1] == "'" or pText[-1] == '"' or pText[-1] == ')':
        pText = pText[0:-1]
    if pText[0] == "'" or pText[0] == '"' or pText[0] == '(':
        pText = pText[1:]
    if pText[-1] == "'" or pText[-1] == '"' or pText[-1] == ')':
        pText = pText[0:-1]
    pText=pText.replace('"',"")
    pText=pText.replace('\n',"")
    return pText
#::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
def print_changes(heading, changes_dict, printLevel=0):
    msgText = get_colorized_data_dict(heading + '#GREEN# changes:#RESET#', changes_dict, colors_template_changes, printLevel)
    # msgText = xcolors(msgText)
    wrapped_text = text_wrap(msgText, printLevel)
    print(wrapped_text)
    #pp = pprint.PrettyPrinter(indent=printLevel*3, compact=True,width=80)
    # pp.pprint(msgText)
    # pText = pprint.pformat(msgText, indent=printLevel * 3, compact=True, width=240)
    # pText = pprint_text_clear(pText)
    # msgText = colorized_message(pText)
    # print(msgText)
#::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
def print_result(heading, result_dict, printLevel=0):
    msgText = get_colorized_data_dict(heading+'#RED# result:#RESET#', result_dict, colors_template_result, printLevel)
    # msgText = xcolors(msgText)
    wrapped_text = text_wrap(msgText, printLevel)
    print(wrapped_text)
    # pp = pprint.PrettyPrinter(indent=printLevel*3, compact=True,width=80)
    # # pp.pprint(msgText)
    # pText = pp.pformat(msgText)
    # pText = pprint.pformat(msgText, indent=printLevel * 3, compact=True, width=240)
    # pText = pprint_text_clear(pText)
    # msgText = colorized_message(pText)
    # print(msgText)
#::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
def print_api_result(heading, result_dict, printLevel=0):
    txt=heading+'#RED# api result:#RESET#'
    msgText = get_colorized_data_dict(txt, result_dict, colors_template_result, printLevel)
    # msgText = xcolors(msgText)
    wrapped_text = text_wrap(msgText, printLevel)
    print(wrapped_text)
    # pText = pprint.pformat(msgText, indent=printLevel * 3, compact=True, width=240)
    # pText = pprint_text_clear(pText)
    # msgText = colorized_message(pText)
    # print(msgText)
    indent="\t" * printLevel
    print(indent + f'{Style.BRIGHT}--------------------------------------------------------{Style.RESET_ALL}')
#::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
def print_message(msg, msgColor=Fore.LIGHTBLACK_EX,printLevel=0):
    msgText = colorized_message(msg, msgColor)
    # msgText = xcolors(msg, msgColor)
    wrapped_text=text_wrap(msgText,printLevel)
    print(wrapped_text)
    # pText = pprint.pformat(msgText, indent=printLevel * 3, compact=True, width=240)
    # pText = pprint_text_clear(pText)
    # msgText = colorized_message(pText, msgColor)
    # print(msgText)
#::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
def colorized_message(msgP, msgColor=Fore.LIGHTBLACK_EX):
    msgC=apply_colors(msgP,msgColor)
    return msgC
#::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
def get_colors_template(template):
    if not template:
        return default_colors_template
    if template:
        if type(template) == type({}):
            default_colors_template = template
        elif type(template) == type(''):
            if template.strip().upper() == 'RESULT':
                default_colors_template = colors_template_result
            elif template.strip().upper() == 'CHANGES':
                default_colors_template = colors_template_changes
            elif template.strip().upper() == 'MONOCHROME':
                default_colors_template = colors_template_changes
            else:
                default_colors_template = default_colors_template
        elif type(template) == type([]):
            default_colors_template = default_colors_template
        else:
            default_colors_template = default_colors_template
        return default_colors_template
#::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
#::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
msg = f'module [{module_id}] [[version {module_version}]] loaded.'
# if thisApp.CONSOLE_ON:
#     print_message(msg)
# else:
print_message(msg)
#::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
#::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
#::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
# main
#::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
#::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
#::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
if __name__ == '__main__':
    print(__file__)