import os
import sys
import datetime
module_ProgramName = os.path.splitext(os.path.basename(__file__))[0]
module_id = '{}'.format(module_ProgramName)
module_version = 0.1
import _appEnvironment as thisApp
from _appEnvironment import FILELOG_ON,CONSOLE_ON,log_file_name,log_errors_file_name
from _colorServices import colorized_text, apply_colors, colorized_string, Fore, Back, Style, default_colors_template, colors_template_result, colors_template_changes, xcolors,fix_colors,clean_colors
import textwrap
import pprint
#::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
#::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
#::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
#globals
#::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
#::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
#::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
global_max_print_line_width = 100
#::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
#::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
#::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
# print services
#::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
#::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
def factorial(n,d,s):
    print("n=",n,'d=',d,'s=',s)
    if not d or type(d) == type('') or not (type(d) == type([]) or type(d) == type({}) or type(d) == type(())):
        if type(d) == type(''):
            ds = f"'{d}'"
        else:
            ds=str(d)
        return(0,'',ds)
    else:
        if type(d) == type([]):
            if n < len(d):
                if n == 0:
                    s = s + '['
                w = d[n]
                print('wwwwww', w,'n=',n,'l=',len(d))
                
                if type(w) == type({}):
                    x = 1
                    
                (nn, nd, ns) = factorial(0, w, '')
                
                s = s + ns

                if n >= len(d)-1:
                    s = s + ']'
                else:
                    s = s + ', '

                return factorial(n + 1, d, s)
            else:
                return (0,'','')
        elif type(d) == type({}):
            if n < len(d):
                if n == 0:
                    s = s + '{'
                
                keys = list(d.keys())
                k = keys[n]
                w = d.get(k)
                s = s + f"'{k}':"
    
                (nn, nd, ns) = factorial(0, w, '')
                
                s = s + ns

                if n >= len(d)-1:
                    s = s + '}'
                else:
                    s = s + ', '

                return factorial(n + 1, d, s)
            else:
                return (0, '', s)
        else:
            return(0,'',s)
#::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
#print(factorial(0, ['aaaa', ['1111', 3.345, '3333', ['1', '2', '3']], 'cccc', {'xxxx':1111, 'zzzzz':3333}], ''))
#::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
def decorated_data_recursion_nocolors(n,d,s):
    # print("n=",n,'d=',d,'s=',s)
    if not d or type(d) == type('') or not (type(d) == type([]) or type(d) == type({}) or type(d) == type(())):
        if type(d) == type(''):
            ds = f"'{d}'"
        else:
            ds=str(d)
        return(0,'',ds)
    else:
        if type(d) == type([]):
            if n < len(d):
                if n == 0:
                    s = s + '['
                w = d[n]
                # print('next item:', w,'n=',n,'l=',len(d))
                
                (nn, nd, ns) = decorated_data_recursion_nocolors(0, w, '')
                
                s = s + ns

                if n >= len(d)-1:
                    s = s + ']'
                else:
                    s = s + ', '

                return decorated_data_recursion_nocolors(n + 1, d, s)
            else:
                return (0,'',s)
        elif type(d) == type({}):
            if n < len(d):
                if n == 0:
                    s = s + '{'
                
                keys = list(d.keys())
                k = keys[n]
                w = d.get(k)
                s = s + f"'{k}':"
    
                (nn, nd, ns) = decorated_data_recursion_nocolors(0, w, '')
                
                s = s + ns

                if n >= len(d)-1:
                    s = s + '}'
                else:
                    s = s + ', '

                return decorated_data_recursion_nocolors(n + 1, d, s)
            else:
                return (0, '', s)
        else:
            return(0,'',s)
#::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
def get_colors_template(template):
    if not template:
        return default_colors_template
    if template:
        if type(template) == type({}):
            colors_template = template
        elif type(template) == type(''):
            if template.strip().upper() == 'RESULT':
                colors_template = colors_template_result
            elif template.strip().upper() == 'CHANGES':
                colors_template = colors_template_changes
            elif template.strip().upper() == 'MONOCHROME':
                colors_template = colors_template_changes
            else:
                colors_template = colors_template
        elif type(template) == type([]):
            colors_template = colors_template
        else:
            colors_template = colors_template
        return colors_template
#::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
def get_template_compo(compo,what='',default='',colors_template={}):
    if what:
        color = colors_template.get(compo, {}).get(what)
        if color:
            return color

    color = colors_template.get(compo)
    if type(color)==type({}):
        if compo.lower().find('key')>=0:
            color = colors_template.get(compo, {}).get('key_color')
            if not color:
                color = colors_template.get(compo, {}).get('data_color')
        elif compo.lower().find('data')>=0:
            color = colors_template.get(compo, {}).get('data_color')
            if not color:
                color = colors_template.get(compo, {}).get('key_color')
    if not color:
        color=default
    return color
#::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
def get_template_dict_compos(colors_template,level=0):
    c0=None
    for k in ('[', ']', '{', '}'):
        c0 = get_template_compo(k, '', '', colors_template)
        if c0:
            break
    if not c0:
        c0 = '#YELLOW#'

    k='level_'+str(level)+'_dict_key'
    c1 = get_template_compo(k, '', '', colors_template)
    if not c1:
        c1 = get_template_compo('dict_key', '', '#BLUE#', colors_template)
    k='level_'+str(level)+'_dict_data'
    c2 = get_template_compo(k, '', '', colors_template)
    if not c2:
        c2 = get_template_compo('dict_key', '', '#WHITE#', colors_template)
    # if 1==2:
    #     k='level_'+str(level)+'_dict_keys'
    #     c1 = get_template_compo(k, '', '', colors_template)
    #     if not c1:
    #         c1 = get_template_compo('dict_keys', '', '#BLUE#', colors_template)

    #     k='level_'+str(level)+'_dict_data'
    #     c2 = get_template_compo(k, '', '', colors_template)
    #     if not c2:
    #         c2=get_template_compo('dict_data','','#WHITE#',colors_template)
    return (c0, c1, c2)
#::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
def decorated_data_recursion(n,d,s,colors_template={},level=0):
    # print("n=",n,'d=',d,'s=',s)
    (c0, c1, c2) = get_template_dict_compos(colors_template,level)
    if not d or type(d) == type('') or not (type(d) == type([]) or type(d) == type({}) or type(d) == type(())):
        if d == None:
            ds = str(d)
        else:
            ds=d
        return(0,'',ds)
    else:
        if type(d) == type([]):
            k = 'array_item_' + str(n + 1)
            ck=get_template_compo(k,'key_color',c1,colors_template)
            cd=get_template_compo(k,'data_color',c2,colors_template)
            if n < len(d):
                if n == 0:
                    s = s + '['
                w = d[n]
                # print('next item:', w,'n=',n,'l=',len(d))
                
                (nn, nd, ns) = decorated_data_recursion(0, w, '', colors_template, level)
                
                if type(ns) == type(''):
                    ds = f"#C0#'{cd}{ns}#C0#'"
                else:
                    ds=f"{cd}{d}#C0#"
                s = s + ds

                if n >= len(d)-1:
                    s = s + ']'
                else:
                    s = s + ', '

                return decorated_data_recursion(n + 1, d, s, colors_template, level)
            else:
                return (0,'',s)
        elif type(d) == type({}):
            if n < len(d):
                if n == 0:
                    level = level + 1
                    (c0, c1, c2) = get_template_dict_compos(colors_template,level)
                    s = s + c0+'{'
            
                keys = list(d.keys())
                k = keys[n]
                w = d.get(k)
                ck=get_template_compo(k,'key_color',c1,colors_template)
                cd=get_template_compo(k,'data_color',c2,colors_template)

                s = s + f"#C0#'{ck}{k}#C0#':"
    
                (nn, nd, ns) = decorated_data_recursion(0, w, '', colors_template, level)

                cd = colors_template.get(k,{}).get('key_color',cd)
                cd = colors_template.get(str(ns), {}).get('data_color', cd)

                if k.lower().find('status') >= 0:
                    if str(ns).lower() == 'success':
                        cd='#GREEN#'
                        colors_template.update({'status_color': cd})
                    elif str(ns).lower().find('error') >= 0:
                        cd='#RED#'
                        colors_template.update({'status_color': cd})
                    elif str(ns).lower().find('warning') >= 0:
                        cd='#YELLOW#'
                        colors_template.update({'status_color': cd})

                if k.lower().find('message') >= 0:
                    cd=colors_template.get('status_color','#WHITE#')
                    
                if type(ns) == type(''):
                    ds = f"#C0#'{cd}{ns}#C0#'"
                else:
                    ds=f"{cd}{ns}#C0#"
                s = s + ds

                if n >= len(d) - 1:
                    s = s + c0+'}'
                    level = level - 1
                    (c0, c1, c2) = get_template_dict_compos(colors_template,level)
                else:
                    s = s + ', '

                return decorated_data_recursion(n + 1, d, s, colors_template, level)
    
            else:
                return (0, '', s)
        else:
            return (0, '', s)
#::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
def decorated_data(data, colors_template={}):
    colors_template = get_colors_template(colors_template)
    (dummy1, dummy2, thisText) = decorated_data_recursion(0, data, '',colors_template,0)
    return str(thisText)
#::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
def bobbi_starr(msgtext,initial_indent="", subsequent_indent="", break_long_words=True, width=0):
    if width < 20:
        width = global_max_print_line_width
    text = fix_colors(msgtext)
    #print(text)

    lines = []
    ix=-1
    x = False
    line = ''
    lw=0
    for ix in range(0,len(text)):
        c = text[ix]
        line = line + c
        if c == '#':
            x = not (x)
            continue
        if not x:
            lw=lw+1
        if lw == width:
            lines.append(line.strip())
            line = ''
            lw=0            
    lines.append(line.strip())            
        # line = text[0:width]
        # #print(ix,line+'|', len(line))
        # text = text[width:]
        # #print(ix,text, len(text))
        
        # lines.append(line)
        # if not text:
        #     break
    newText=""
    for ix in range(0, len(lines)):
        line = initial_indent+ lines[ix]
        if ix <len(lines)-1:
            line=line+"\n"
        newText = newText + line
    return newText
    # new_text = textwrap.fill(dedented_text, initial_indent=indent, subsequent_indent=indent + '\t', break_long_words=True, break_on_hyphens=True, width=width)
#::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
def text_wrap(msgText, printLevel=0,width=-1):
    indent = "\t" * printLevel
    if width < 20:
        width = global_max_print_line_width
    dedented_text = textwrap.dedent(msgText).strip()
    
    return bobbi_starr(dedented_text,initial_indent=indent, subsequent_indent=indent + '\t', break_long_words=True, width=width)

    # if printLevel <= 0:
    #     # new_text = textwrap.fill(dedented_text, initial_indent=indent, subsequent_indent=indent + '\t', break_long_words=True, width=width)
    #     return msgText
    # else:        
    #     new_text = textwrap.fill(dedented_text, initial_indent=indent, subsequent_indent=indent + '\t', break_long_words=True, break_on_hyphens=True, width=width)
    #     return new_text
#::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
#::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
#::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
def log_msg(msg_text, **kwargs):
    if CONSOLE_ON:
        msgText = text_wrap(msg_text, kwargs.get('indent_level', 0), kwargs.get('width',0))
        msgText = colorized_text(msgText, kwargs.get('color_template',''))
        print(msgText)

    if FILELOG_ON or kwargs.get('msg_type', '').upper().find('ERROR') >= 0 or msg_text.upper().find('ERROR') >= 0:
        msgText = clean_colors(msg_text)
        msgJson1 = f"dt:'{str(datetime.datetime.utcnow())}', module:'{kwargs.get('process_name','')}', msg='{msgText.strip()}'"
        msgJson = '{'+msgJson1+'}\n'

    if kwargs.get('msg_type', '').upper().find('ERROR') >= 0 or msg_text.upper().find('ERROR') >= 0:
        errorsFile = kwargs.get('errors_file', '')
        if not errorsFile:
            errorsFile = thisApp.log_errors_file_name
        if errorsFile:
            f = open(errorsFile, "a+")
            f.write(msgText)
            f.close
                    
    if FILELOG_ON:
        log_files=[]
        # log_file = kwargs.get('log_file','')
        # if not log_file:
        #     log_file = thisApp.log_file_name
        # if log_file:
        #     log_files.append(log_file)

        xdebug_files = kwargs.get('debug_files', [])
        if xdebug_files:
            if type(xdebug_files) == type(''):
                f_array = xdebug_files.split(';')
                for ix in range(0, len(f_array)):
                    if f_array[ix]:
                        log_files.append(f_array[ix])
            elif type(xdebug_files) == type([]):
                for ix in range(0, len(xdebug_files)):
                    if xdebug_files[ix]:
                        log_files.append(xdebug_files[ix])

        for logFile in log_files:
            if logFile:
                f = open(logFile, "a+")
                f.write(msgJson)
                f.close
#::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
#::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
#::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
#::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
#::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
#::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
#::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
def log_process_message(process_id='', msgType='', msg_data='', **kwargs):
    # print(kwargs)
    debug_level = kwargs.get('debug_level', -1)
    filelog_enabled = kwargs.get('filelog_enabled',None)
    print_enabled = kwargs.get('print_enabled',None)
    if debug_level >0 and (FILELOG_ON or CONSOLE_ON or filelog_enabled or print_enabled):
        pass
    else:
        return

    msg_type='message'
    msg_type_debug = kwargs.get(msg_type + '_debug', True)
    if not msg_type_debug:
        msgtype_debug = kwargs.get(msgType + '_' + msg_type + '_debug', False)
        if not msgtype_debug:
            return
    else:
        msgtype_debug = kwargs.get(msgType + '_' + msg_type + '_debug', True)
        if not msgtype_debug:
            return

    msg_type = msgType

    indent_method = kwargs.get('indent_method', 'NEXT_LEVEL')
    indent_level = kwargs.get('indent_level',0)
    if not (indent_method.upper().replace('_', '').replace('-', '').strip() in ('CALLLEVEL', 'SAMELEVEL', 'NOINDENT')):
        indent_level = indent_level + 1

    if msg_type.lower().find('error') >= 0:
        c1 = '#RED#'
        c2 = '#YELLOW#'
    elif msg_type.lower().find('success') >= 0 or msg_type.lower().find('ok') >= 0:
        c1 = '#GREEN#'
        c2 = '#YELLOW#'
    elif msg_type.lower().find('warning') >= 0:
        c1 = '#YELLOW#'
        c2 = '#WHITE#'
    else:
        c1 = '#WHITE#'
        c2 = '#YELLOW#'

    msg_prefix = f"#C9#{process_id}#C0#"
    if kwargs.get('msg_formatting', '').upper() == 'AUTO':
        msg_prefix = f"#C9#{process_id}#C0# #C1#{kwargs.get('process_entity','')}#C0# action #C2#{kwargs.get('process_action','').upper()}#C0#"

    if msg_type:
        msg_id = f"{c1}{msg_type.lower()} message#C0#: "
    else:
        msg_id = '#C0#: '
        if not process_id:
            msg_id = ''

    if process_id:
        msg_id = ' ' + msg_id
        
    msg_data_prefix =''
    msg_data = c2+decorated_data(msg_data, kwargs.get('colors_template',''))+'#C0#'
    msg_text = '#C0#' + msg_prefix + '#C0#' + msg_id + '#C0#' + msg_data_prefix + '#C0#' + msg_data + '#C0#'

    kwargs.update({'indent_level':indent_level,'msg_type':msg_type})

    log_msg(msg_text, **kwargs)
#::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
def log_process_result_message(process_id='', msgType='', msg_data='', **kwargs):
    # print(kwargs)
    debug_level = kwargs.get('debug_level', -1)
    filelog_enabled = kwargs.get('filelog_enabled',None)
    print_enabled = kwargs.get('print_enabled',None)
    if debug_level >0 and (FILELOG_ON or CONSOLE_ON or filelog_enabled or print_enabled):
        pass
    else:
        return

    msg_type='result_message'
    data_name = kwargs.get('data_name', '')

    msg_type_debug = kwargs.get(msg_type + '_debug', True)
    if not msg_type_debug:
        msgtype_debug = kwargs.get(msgType + '_' + msg_type + '_debug', False)
        if not msgtype_debug:
            data_debug = kwargs.get(data_name + '_' + msg_type + '_debug', False)
            if not data_debug:
                return
        else:
            data_debug = kwargs.get(data_name + '_' + msg_type + '_debug', True)
            if not data_debug:
                return
    else:
        msgtype_debug = kwargs.get(msgType + '_' + msg_type + '_debug', True)
        if not msgtype_debug:
            data_debug = kwargs.get(data_name + '_' + msg_type + '_debug', False)
            if not data_debug:
                return
        else:
            data_debug = kwargs.get(data_name + '_' + msg_type + '_debug', True)
            if not data_debug:
                return

    msg_type = msgType

    indent_method = kwargs.get('indent_method', 'SAME_LEVEL')
    indent_level = kwargs.get('indent_level',0)
    # if not (indent_method.upper().replace('_', '').replace('-', '').strip() in ('CALLLEVEL', 'SAMELEVEL', 'NOINDENT')):
    #     indent_level = indent_level + 1

    if msg_type.lower().find('error') >= 0:
        c1 = '#RED#'
        c2 = '#YELLOW#'
    elif msg_type.lower().find('success') >= 0 or msg_type.lower().find('ok') >= 0:
        c1 = '#GREEN#'
        c2 = '#YELLOW#'
    elif msg_type.lower().find('warning') >= 0:
        c1 = '#YELLOW#'
        c2 = '#MAGENTA#'
    else:
        c1 = '#WHITE#'
        c2 = '#YELLOW#'
        msg_type=''
        
    msg_prefix = f"#C9#{process_id}#C0#"
    if kwargs.get('msg_formatting', '').upper() == 'AUTO':
        msg_prefix = f"#C9#{process_id}#C0# #C1#{kwargs.get('process_entity','')}#C0# action #C2#{kwargs.get('process_action','').upper()}#C0#"

    if msg_type:
        msg_id = f"{c1}{msg_type.lower()} result message#C0#: "
    else:
        msg_id = '#C0#: '
        if not process_id:
            msg_id = ''

    if process_id:
        msg_id = ' ' + msg_id
        
    msg_data_prefix =''
    msg_data = c2+decorated_data(msg_data, kwargs.get('colors_template',''))+'#C0#'
    msg_text = '#C0#' + msg_prefix + '#C0#' + msg_id + '#C0#' + msg_data_prefix + '#C0#' + msg_data + '#C0#'

    kwargs.update({'indent_level':indent_level,'msg_type':msg_type})

    log_msg(msg_text, **kwargs)
#::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
def log_process_result(process_id='',result_data='', **kwargs):
    # print(kwargs)
    debug_level = kwargs.get('debug_level', -1)
    filelog_enabled = kwargs.get('filelog_enabled',None)
    print_enabled = kwargs.get('print_enabled',None)
    if debug_level >0 and (FILELOG_ON or CONSOLE_ON or filelog_enabled or print_enabled):
        pass
    else:
        return

    msg_type = 'result'
    data_name = kwargs.get('data_name', '')

    msg_type_debug = kwargs.get(msg_type + '_debug', True)
    if not msg_type_debug:
        data_debug = kwargs.get(data_name + '_' + msg_type + '_debug', False)
        if not data_debug:
            return
    else:
        data_debug = kwargs.get(data_name + '_' + msg_type + '_debug', True)
        if not data_debug:
            return

    indent_method = kwargs.get('indent_method', 'CALL_LEVEL')
    indent_level = kwargs.get('indent_level',0)
    # if not (indent_method.upper().replace('_', '').replace('-', '').strip() in ('CALLLEVEL', 'SAMELEVEL', 'NOINDENT')):
    #     indent_level = indent_level + 1

    msg_prefix = f"#C9#{process_id}#C0#"
    if kwargs.get('msg_formatting', '').upper() == 'AUTO':
        msg_prefix = f"#C9#{process_id}#C0# #C1#{kwargs.get('process_entity','')}#C0# action #C2#{kwargs.get('process_action','').upper()}#C0#"

    msg_id = 'result: '

    msg_data_prefix =''
    if kwargs.get('data_name',''):
        msg_data_prefix = f"{kwargs.get('data_name','')}="
    else:
        msg_data_prefix = f""
    msg_data = decorated_data(result_data, kwargs.get('colors_template',''))+'#C0#'
    if not result_data:
        msg_data='#RED#'+msg_data
        msg_data_prefix='#RED#'+msg_data_prefix

    if process_id:
        msg_id = ' ' + msg_id

    msg_text = '#C0#' + msg_prefix + '#C0#' + msg_id + '#C0#' + msg_data_prefix + '#C0#' + msg_data + '#C0#'
    kwargs.update({'indent_level':indent_level,'msg_type':msg_type})

    log_msg(msg_text, **kwargs)
#::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
def log_process_output(process_id='',result_data='', **kwargs):
    # print(kwargs)
    debug_level = kwargs.get('debug_level', -1)
    filelog_enabled = kwargs.get('filelog_enabled',None)
    print_enabled = kwargs.get('print_enabled',None)
    if debug_level >0 and (FILELOG_ON or CONSOLE_ON or filelog_enabled or print_enabled):
        pass
    else:
        return

    msg_type = 'output'
    data_name = kwargs.get('data_name', '')

    msg_type_debug = kwargs.get(msg_type + '_debug', True)
    if not msg_type_debug:
        data_debug = kwargs.get(data_name + '_' + msg_type + '_debug', False)
        if not data_debug:
            return
    else:
        data_debug = kwargs.get(data_name + '_' + msg_type + '_debug', True)
        if not data_debug:
            return

    indent_method = kwargs.get('indent_method', 'NEXT_LEVEL')
    indent_level = kwargs.get('indent_level',0)
    if not (indent_method.upper().replace('_', '').replace('-', '').strip() in ('CALLLEVEL', 'SAMELEVEL', 'NOINDENT')):
        indent_level = indent_level + 1

    msg_prefix = f"#C9#{process_id}#C0#"
    if kwargs.get('msg_formatting', '').upper() == 'AUTO':
        msg_prefix = f"#C9#{process_id}#C0# #C1#{kwargs.get('process_entity','')}#C0# action #C2#{kwargs.get('process_action','').upper()}#C0#"

    msg_id = 'result: '

    msg_data_prefix =''
    if kwargs.get('data_name',''):
        msg_data_prefix = f"{kwargs.get('data_name','')}="
    else:
        msg_data_prefix = f""
    msg_data = decorated_data(result_data, kwargs.get('colors_template',''))+'#C0#'
    if not result_data:
        msg_data='#RED#'+msg_data
        msg_data_prefix='#RED#'+msg_data_prefix

    if process_id:
        msg_id = ' ' + msg_id

    msg_text = '#C0#' + msg_prefix + '#C0#' + msg_id + '#C0#' + msg_data_prefix + '#C0#' + msg_data + '#C0#'
    kwargs.update({'indent_level':indent_level,'msg_type':msg_type})

    log_msg(msg_text, **kwargs)
#::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
def log_process_input(process_id='',data_name='',data='', **kwargs):
    # print(kwargs)
    debug_level = kwargs.get('debug_level', -1)
    filelog_enabled = kwargs.get('filelog_enabled',None)
    print_enabled = kwargs.get('print_enabled', None)
    if debug_level >0 and (FILELOG_ON or CONSOLE_ON or filelog_enabled or print_enabled):
        pass
    else:
        return

    msg_type = 'input'

    msg_type_debug = kwargs.get(msg_type + '_debug', True)
    if not msg_type_debug:
        data_debug = kwargs.get(data_name + '_' + msg_type + '_debug', False)
        if not data_debug:
            return
    else:
        data_debug = kwargs.get(data_name + '_' + msg_type + '_debug', True)
        if data_name=='caller_area':
            data_debug = kwargs.get(data_name + '_' + msg_type + '_debug', False)
        if not data_debug:
            return

    indent_method = kwargs.get('indent_method', 'NEXT_LEVEL')
    indent_level = kwargs.get('indent_level',0)
    if not (indent_method.upper().replace('_', '').replace('-', '').strip() in ('CALLLEVEL', 'SAMELEVEL', 'NOINDENT')):
        indent_level = indent_level + 1

    msg_prefix = f"#C9#{process_id}#C0#"
    if kwargs.get('msg_formatting', '').upper() == 'AUTO':
        msg_prefix = f"#C9#{process_id}#C0# #C1#{kwargs.get('process_entity','')}#C0# action #C2#{kwargs.get('process_action','').upper()}#C0#"

    msg_id = 'input: '
        
    msg_data_prefix =''

    if data_name:
        msg_data_prefix = f"{data_name}="
    else:
        msg_data_prefix = f""
    msg_data = decorated_data(data, kwargs.get('colors_template',''))+'#C0#'
    if data == None:
        msg_data_prefix='#WHITE#'+msg_data_prefix
        msg_data='#RED#'+msg_data
    else:
        msg_data_prefix='#WHITE#'+msg_data_prefix
        msg_data='#XBLUE#'+msg_data

    if process_id:
        msg_id = ' ' + msg_id

    msg_text = '#C0#' + msg_prefix + '#C0#' + msg_id + '#C0#' + msg_data_prefix + '#C0#' + msg_data + '#C0#'
    kwargs.update({'indent_level':indent_level,'msg_type':msg_type,'data_name':data_name})

    log_msg(msg_text, **kwargs)
#::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
def log_process_data(process_id='',data_name='',data='', **kwargs):
    # print(kwargs)
    debug_level = kwargs.get('debug_level', -1)
    filelog_enabled = kwargs.get('filelog_enabled',None)
    print_enabled = kwargs.get('print_enabled',None)
    if debug_level >0 and (FILELOG_ON or CONSOLE_ON or filelog_enabled or print_enabled):
        pass
    else:
        return

    msg_type = 'data'

    msg_type_debug = kwargs.get(msg_type + '_debug', True)
    if not msg_type_debug:
        data_debug = kwargs.get(data_name + '_' + msg_type + '_debug', False)
        if not data_debug:
            return
    else:
        data_debug = kwargs.get(data_name + '_' + msg_type + '_debug', True)
        if not data_debug:
            return

    indent_method = kwargs.get('indent_method', 'NEXT_LEVEL')
    indent_level = kwargs.get('indent_level',0)
    if not (indent_method.upper().replace('_', '').replace('-', '').strip() in ('CALLLEVEL', 'SAMELEVEL', 'NOINDENT')):
        indent_level = indent_level + 1

    msg_prefix = f"#C9#{process_id}#C0#"
    if kwargs.get('msg_formatting', '').upper() == 'AUTO':
        msg_prefix = f"#C9#{process_id}#C0# #C1#{kwargs.get('process_entity','')}#C0# action #C2#{kwargs.get('process_action','').upper()}#C0#"

    msg_id = 'data: '

    msg_data_prefix =''

    if data_name:
        msg_data_prefix = f"{data_name}="
    else:
        msg_data_prefix = f""
    msg_data = decorated_data(data, kwargs.get('colors_template',''))+'#C0#'
    if not data:
        msg_data='#RED#'+msg_data
        msg_data_prefix='#RED#'+msg_data_prefix
    else:
        msg_data_prefix='#WHITE#'+msg_data_prefix

    if process_id:
        msg_id = ' ' + msg_id

    msg_text = '#C0#' + msg_prefix + '#C0#' + msg_id + '#C0#' + msg_data_prefix + '#C0#' + msg_data + '#C0#'
    kwargs.update({'indent_level':indent_level,'msg_type':msg_type,'data_name':data_name})

    log_msg(msg_text, **kwargs)
#::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
def log_process_parameter(process_id='', param_prefix='', data_name='', data='', **kwargs):
    # print(kwargs)
    debug_level = kwargs.get('debug_level', -1)
    filelog_enabled = kwargs.get('filelog_enabled',None)
    print_enabled = kwargs.get('print_enabled',None)
    if debug_level >0 and (FILELOG_ON or CONSOLE_ON or filelog_enabled or print_enabled):
        pass
    else:
        return

    msg_type = 'parameter'

    msg_type_debug = kwargs.get(msg_type + '_debug', True)
    if not msg_type_debug:
        data_debug = kwargs.get(data_name + '_' + msg_type + '_debug', False)
        if not data_debug:
            return
    else:
        data_debug = kwargs.get(data_name + '_' + msg_type + '_debug', True)
        if not data_debug:
            return

    indent_method = kwargs.get('indent_method', 'NEXT_LEVEL')
    indent_level = kwargs.get('indent_level',0)
    if not (indent_method.upper().replace('_', '').replace('-', '').strip() in ('CALLLEVEL', 'SAMELEVEL', 'NOINDENT')):
        indent_level = indent_level + 1

    msg_prefix = f"#C9#{process_id}#C0#"
    if kwargs.get('msg_formatting', '').upper() == 'AUTO':
        msg_prefix = f"#C9#{process_id}#C0# #C1#{kwargs.get('process_entity','')}#C0# action #C2#{kwargs.get('process_action','').upper()}#C0#"
    
    if param_prefix:
        param_prefix = param_prefix+':'

    msg_data_prefix =''

    if data_name:
        msg_data_prefix = f"{data_name}#C0#="
    else:
        msg_data_prefix = f""
    msg_data = decorated_data(data, kwargs.get('colors_template',''))+'#C0#'
    if not data:
        msg_data='#RED#'+msg_data
        msg_data_prefix='#RED#'+msg_data_prefix
    else:
        msg_data='#YELLOW#'+msg_data
        msg_data_prefix='#XBLUE#'+msg_data_prefix

    if process_id:
        msg_id = ' ' + msg_id

    msg_text = '#C0#' + msg_prefix + '#C0#' + param_prefix + '#C0#' + msg_data_prefix + '#C0#' + msg_data + '#C0#'
    kwargs.update({'indent_level':indent_level,'msg_type':msg_type,'data_name':data_name})

    log_msg(msg_text, **kwargs)
#::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
def log_process_start(process_id='', **kwargs):
    # print(kwargs)
    debug_level = kwargs.get('debug_level', -1)
    filelog_enabled = kwargs.get('filelog_enabled',None)
    print_enabled = kwargs.get('print_enabled',None)
    if debug_level >0 and (FILELOG_ON or CONSOLE_ON or filelog_enabled or print_enabled):
        pass
    else:
        return

    msg_type = 'start'

    msg_type_debug = kwargs.get(msg_type + '_debug', True)
    if not msg_type_debug:
        return

    indent_method = kwargs.get('indent_method', 'CALL_LEVEL')
    indent_level = kwargs.get('indent_level',0)
    # if not (indent_method.upper().replace('_', '').replace('-', '').strip() in ('CALLLEVEL', 'SAMELEVEL', 'NOINDENT')):
    #     indent_level = indent_level + 1

    msg_prefix = f"#C9#{process_id}#C0#"
    if kwargs.get('msg_formatting', '').upper() == 'AUTO':
        msg_prefix = f"#C9#{process_id}#C0# #C1#{kwargs.get('process_entity','')}#C0# action #C2#{kwargs.get('process_action','').upper()}#C0#"

    msg_id = 'start: '

    msg_data_prefix =''
    if kwargs.get('data_name',''):
        msg_data_prefix = f"{kwargs.get('data_name','')}="
    else:
        msg_data_prefix = f""

    msg_data =''
    if kwargs.get('start_data',''):
        msg_data = decorated_data(kwargs.get('start_data', ''), kwargs.get('colors_template', '')) + '#C0#'

    if process_id:
        msg_id = ' ' + msg_id

    msg_text = '#C0#' + msg_prefix + '#C0#' + msg_id + '#C0#' + msg_data_prefix + '#C0#' + msg_data + '#C0#'
    kwargs.update({'indent_level':indent_level,'msg_type':msg_type})

    log_msg(msg_text, **kwargs)
#::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
def log_process_finish(process_id='',result_data='', **kwargs):
    # print(kwargs)
    debug_level = kwargs.get('debug_level', -1)
    filelog_enabled = kwargs.get('filelog_enabled',None)
    print_enabled = kwargs.get('print_enabled',None)
    if debug_level >0 and (FILELOG_ON or CONSOLE_ON or filelog_enabled or print_enabled):
        pass
    else:
        return


    msg_type = 'finish'

    msg_type_debug = kwargs.get(msg_type + '_debug', True)
    if not msg_type_debug:
        return

    indent_method = kwargs.get('indent_method', 'CALL_LEVEL')
    indent_level = kwargs.get('indent_level',0)
    # if not (indent_method.upper().replace('_', '').replace('-', '').strip() in ('CALLLEVEL', 'SAMELEVEL', 'NOINDENT')):
    #     indent_level = indent_level + 1

    msg_prefix = f"#C9#{process_id}#C0#"
    if kwargs.get('msg_formatting', '').upper() == 'AUTO':
        msg_prefix = f"#C9#{process_id}#C0# #C1#{kwargs.get('process_entity','')}#C0# action #C2#{kwargs.get('process_action','').upper()}#C0#"

    msg_id = 'finish: '

    msg_data_prefix =''
    if kwargs.get('data_name',''):
        msg_data_prefix = f"{kwargs.get('data_name','')}="
    else:
        msg_data_prefix = f""
    msg_data = decorated_data(result_data, kwargs.get('colors_template',''))+'#C0#'
    if not result_data:
        msg_data='#RED#'+msg_data
        msg_data_prefix='#RED#'+msg_data_prefix

    if process_id:
        msg_id = ' ' + msg_id

    msg_text = '#C0#' + msg_prefix + '#C0#' + msg_id + '#C0#' + msg_data_prefix + '#C0#' + msg_data + '#C0#'
    kwargs.update({'indent_level':indent_level,'msg_type':msg_type})

    log_msg(msg_text, **kwargs)
#::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
def x(p1='', **kwrgs):
    print('p1 =',p1)
    p2 = kwrgs.get('p2')
    print('p2 =', p2)
    p3 = kwrgs.get('p3')
    print('p3 =', p3)
#::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
#::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
#::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
msg = f'module [{module_id}] [[version {module_version}]] loaded.'
if CONSOLE_ON:
    print(colorized_string(msg))
#::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
#x('xxxx',p2='222222',p4='4444444')
#::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
#::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
# main
#::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
#::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
#::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
if __name__ == '__main__':
    print(__file__)
    msgText="""This function wraps the #C0# input paragraph #C0#such that each line in th#C0#e paragraph is at most width characters long. The wrap method returns a list of output lines. The returned list is empty if the wrapped output has no content. """
    print(msgText)
    print('')
    x = bobbi_starr(msgText, initial_indent="", subsequent_indent="", break_long_words=True, width=0)
    print(x)