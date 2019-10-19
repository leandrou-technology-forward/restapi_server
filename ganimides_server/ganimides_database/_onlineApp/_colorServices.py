import os
import sys

module_ProgramName = os.path.splitext(os.path.basename(__file__))[0]
module_id = '{}'.format(module_ProgramName)
module_version = 0.1

import textwrap
import colorama
from colorama import Fore, Back, Style
if sys.stdout.isatty():
    colorama.init(autoreset=True)
else:
    # We're being piped, so skip colors
    colorama.init(strip=True)
try:
    import _appEnvironment as thisApp
    console_on = thisApp.CONSOLE_ON
except:
    console_on = True

FgColor0 = Fore.LIGHTBLACK_EX
FgColor1 = Fore.YELLOW
FgColor2 = Fore.CYAN
FgColor3 = Fore.GREEN
FgColor4 = Fore.MAGENTA
FgColor5 = Fore.LIGHTBLUE_EX
FgColor6 = Fore.RED
FgColor7 = Fore.BLUE
FgColor8 = Fore.LIGHTCYAN_EX
FgColor9 = Fore.LIGHTWHITE_EX
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
    ['#RED#',Fore.RED],
    ['#GREEN#',Fore.GREEN],
    ['#BLUE#',Fore.BLUE],
    ['#YELLOW#',Fore.YELLOW],
    ['#WHITE#',Fore.WHITE],
    ['#GRAY#',Fore.LIGHTBLACK_EX],
    ['#MAGENTA#',Fore.MAGENTA],
    ['#CYAN#',Fore.CYAN],
    ['#XRED#',Fore.LIGHTRED_EX],
    ['#XGREEN#',Fore.LIGHTGREEN_EX],
    ['#XBLUE#',Fore.LIGHTBLUE_EX],
    ['#XYELLOW#',Fore.LIGHTYELLOW_EX],
    ['#XWHITE#',Fore.LIGHTWHITE_EX],
    ['#XMAGENTA#',Fore.LIGHTMAGENTA_EX],
    ['#XCYAN#',Fore.LIGHTCYAN_EX],
    ['#ERROR#',Fore.RED],
    ['#WARNING#',Fore.MAGENTA],
    ['#OK#',Fore.GREEN],
    ['#SUCCESS#',Fore.GREEN],
    ['#RESET#',Fore.RESET],
    ['#BGRESET#',Back.RESET],
    ['#RESET_ALL#',Style.RESET_ALL],
    ['#BRIGHT#',Style.BRIGHT],
    ['#NORMAL#',Style.NORMAL],
    ['#DIM#',Style.DIM],
]
default_colors_template = {
    'level_0_dict_key': Fore.LIGHTBLUE_EX,
    'level_0_dict_data': Fore.CYAN,
    'level_1_dict_key': Fore.BLUE,
    'level_1_dict_data': Fore.YELLOW,
    'level_2_dict_key': Fore.CYAN,
    'level_2_dict_data': Fore.MAGENTA,
    'level_3_dict_key': Fore.LIGHTBLUE_EX,
    'level_3_dict_data': Fore.WHITE,
    'level_0_dict': {'key_color': Fore.BLUE, 'data_color': Fore.CYAN},
    'level_1_dict': {'key_color': Fore.BLUE, 'data_color': Fore.YELLOW},
    'level_2_dict': {'key_color': Fore.CYAN, 'data_color': Fore.MAGENTA},
    'level_3_dict': {'key_color': Fore.LIGHTBLUE_EX, 'data_color': Fore.WHITE},
    'api_data': {'key_color': Fore.WHITE, 'data_color': Fore.MAGENTA},
    'success': {'key_color': Fore.WHITE, 'data_color': Fore.GREEN},
    'error': {'key_color': Fore.WHITE, 'data_color': Fore.RED},
    'warning': {'key_color': Fore.WHITE, 'data_color': Fore.LIGHTRED_EX},
    'old_value': {'key_color': Fore.LIGHTBLACK_EX, 'data_color': Fore.MAGENTA},
    'new_value': {'key_color': Fore.LIGHTBLACK_EX, 'data_color': Fore.YELLOW},
    'alpha': {'key_color': Fore.WHITE, 'data_color': Fore.GREEN},
    'beta': {'key_color': Fore.WHITE, 'data_color': Fore.CYAN},
    }
colors_template_result = {
    'prefix': {'key_color': Fore.YELLOW, 'data_color': Fore.GREEN},
    'level_0_dict_key': Fore.BLUE,
    'level_0_dict_data': Fore.MAGENTA,
    'level_1_dict_key': Fore.BLUE,
    'level_1_dict_data': Fore.WHITE,
    'level_2_dict_key': Fore.WHITE,
    'level_2_dict_data': Fore.MAGENTA,
    'level_0_dict_keys': {'key_color': Fore.BLUE, 'data_color': Fore.BLUE},
    'level_0_dict_data': {'key_color': Fore.BLUE, 'data_color': Fore.YELLOW},
    'level_1_dict_keys': {'key_color': Fore.BLUE, 'data_color': Fore.BLUE},
    'level_1_dict_data': {'key_color': Fore.BLUE, 'data_color': Fore.WHITE},
    'level_2_dict_keys': {'key_color': Fore.BLUE, 'data_color': Fore.MAGENTA},
    'level_2_dict_data': {'key_color': Fore.BLUE, 'data_color': Fore.YELLOW},
    'level_3_dict_keys': {'key_color': Fore.BLUE, 'data_color': Fore.LIGHTBLUE_EX},
    'level_3_dict_data': {'key_color': Fore.BLUE, 'data_color': Fore.CYAN},
    'level_4_dict_keys': {'key_color': Fore.BLUE, 'data_color': Fore.BLUE},
    'level_4_dict_data': {'key_color': Fore.BLUE, 'data_color': Fore.MAGENTA},
    'suffix': {'key_color': Fore.WHITE, 'data_color': Fore.WHITE},
    'api_data': {'key_color': Fore.RED, 'data_color': Fore.MAGENTA},
    'success': {'key_color': Fore.WHITE, 'data_color': Fore.GREEN},
    'error': {'key_color': Fore.WHITE, 'data_color': Fore.RED},
    'warning': {'key_color': Fore.WHITE, 'data_color': Fore.LIGHTRED_EX},
    'old_value': {'key_color': Fore.LIGHTBLACK_EX, 'data_color': Fore.MAGENTA},
    'new_value': {'key_color': Fore.LIGHTBLACK_EX, 'data_color': Fore.YELLOW},
    'alpha': {'key_color': Fore.WHITE, 'data_color': Fore.GREEN},
    'beta': {'key_color': Fore.WHITE, 'data_color': Fore.CYAN},
    }
colors_template_changes = {
    'prefix': {'key_color': Fore.YELLOW, 'data_color': Fore.GREEN},
    'level_0_dict_keys': {'key_color': Fore.BLUE, 'data_color': Fore.BLUE},
    'level_0_dict_data': {'key_color': Fore.BLUE, 'data_color': Fore.YELLOW},
    'level_1_dict_keys': {'key_color': Fore.BLUE, 'data_color': Fore.BLUE},
    'level_1_dict_data': {'key_color': Fore.BLUE, 'data_color': Fore.WHITE},
    'level_2_dict_keys': {'key_color': Fore.BLUE, 'data_color': Fore.MAGENTA},
    'level_2_dict_data': {'key_color': Fore.BLUE, 'data_color': Fore.YELLOW},
    'level_3_dict_keys': {'key_color': Fore.BLUE, 'data_color': Fore.LIGHTBLUE_EX},
    'level_3_dict_data': {'key_color': Fore.BLUE, 'data_color': Fore.CYAN},
    'level_4_dict_keys': {'key_color': Fore.BLUE, 'data_color': Fore.BLUE},
    'level_4_dict_data': {'key_color': Fore.BLUE, 'data_color': Fore.MAGENTA},
    'suffix': {'key_color': Fore.WHITE, 'data_color': Fore.WHITE},
    'api_data': {'key_color': Fore.RED, 'data_color': Fore.MAGENTA},
    'success': {'key_color': Fore.WHITE, 'data_color': Fore.GREEN},
    'error': {'key_color': Fore.WHITE, 'data_color': Fore.RED},
    'warning': {'key_color': Fore.WHITE, 'data_color': Fore.LIGHTRED_EX},
    'old_value': {'key_color': Fore.LIGHTBLACK_EX, 'data_color': Fore.MAGENTA},
    'new_value': {'key_color': Fore.LIGHTBLACK_EX, 'data_color': Fore.YELLOW},
    'alpha': {'key_color': Fore.WHITE, 'data_color': Fore.GREEN},
    'beta': {'key_color': Fore.WHITE, 'data_color': Fore.CYAN},
    }
########################################################
fore_colors=[]
back_colors=[]
color_names=[]
fore_colors_dict={}
back_colors_dict={}
light_colors=[]
dark_colors=[]
fore_color_names_dict={}
back_color_names_dict={}
#::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
#::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
#::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
def apply_colors(msgP,msgColor='',color_palette={}):
    if not msgColor:
        msgColor=FgColor0
    # #msgP=msgP.replace('[o','#C8#').replace('o]','#C0#')
    for ix in range(0, len(colors_array)):
        if not msgP.find('[') >= 0:
            break
        msgP=msgP.replace(colors_array[ix][1],colors_array[ix][0])

    msgP=msgP.replace('[[[[[[[[','#C8#').replace(']]]]]]]]','#C0#')
    msgP=msgP.replace('[[[[[[[','#C7#').replace(']]]]]]]','#C0#')
    msgP=msgP.replace('[[[[[[','#C6#').replace(']]]]]]','#C0#')
    msgP=msgP.replace('[[[[[','#C5#').replace(']]]]]','#C0#')
    msgP=msgP.replace('[[[[','#C4#').replace(']]]]','#C0#')
    msgP=msgP.replace('[[[','#C3#').replace(']]]','#C0#')
    msgP=msgP.replace('[[','#C2#').replace(']]','#C0#')
    msgP=msgP.replace('[','#C1#').replace(']','#C0#')
    msgP = f"{FgColor0}{msgP}{Fore.RESET}{Back.RESET}"
    msgP=msgP.replace('#RESET#',msgColor)
    msgP=msgP.replace('#C0#',msgColor)
    msgP=msgP.replace('#>#','\t')
    for ix in range(0, len(colors_array)):
        if not msgP.find('#') >= 0:
            break
        msgP=msgP.replace(colors_array[ix][0],colors_array[ix][1])
    return msgP
#::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
def colorized_message(msgP, msgColor=Fore.LIGHTBLACK_EX,color_palette=None):
    msgC=apply_colors(msgP,msgColor)
    return msgC
#::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
def colorized_string(msgP, msgColor=Fore.LIGHTBLACK_EX,color_palette=None):
    msgC=apply_colors(msgP,msgColor)
    return msgC
#::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
def colorized_text(text, color_palette={}):
    for ix in range(0, len(colors_array)):
        # if not text.find('[') >= 0:
        #     break
        text=text.replace(colors_array[ix][1],colors_array[ix][0])

    text=text.replace('[[[[[[[[','#C8#').replace(']]]]]]]]','#C0#')
    text=text.replace('[[[[[[[','#C7#').replace(']]]]]]]','#C0#')
    text=text.replace('[[[[[[','#C6#').replace(']]]]]]','#C0#')
    text=text.replace('[[[[[','#C5#').replace(']]]]]','#C0#')
    text=text.replace('[[[[','#C4#').replace(']]]]','#C0#')
    text=text.replace('[[[','#C3#').replace(']]]','#C0#')
    text=text.replace('[[','#C2#').replace(']]','#C0#')
    text=text.replace('[','#C1#').replace(']','#C0#')
    # text = f"{FgColor0}{text}{Fore.RESET}{Back.RESET}"
    # text=text.replace('#RESET#',msgColor)
    # text=text.replace('#C0#',msgColor)
    text=text.replace('#>#','\t')
    for ix in range(0, len(colors_array)):
        if not text.find('#') >= 0:
            break
        text=text.replace(colors_array[ix][0],colors_array[ix][1])
    return text
#::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
#::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
#::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
def clean_colors(msgP):
    msgP=fix_colors(msgP)
    for ix in range(0, len(colors_array)):
        msgP=msgP.replace(colors_array[ix][0],'')
    return msgP
def xcolors(msgP):
    msgP=fix_colors(msgP)
    for ix in range(0, len(colors_array)):
        msgP=msgP.replace(colors_array[ix][0],'')
    return msgP
#############################################################################
def fix_colors(msgP):
    for ix in range(0, len(colors_array)):
        # if not msgP.find('[') >= 0:
        #     break
        msgP=msgP.replace(colors_array[ix][1],colors_array[ix][0])

    msgP=msgP.replace('[[[[[[[[','#C8#').replace(']]]]]]]]','#C0#')
    msgP=msgP.replace('[[[[[[[','#C7#').replace(']]]]]]]','#C0#')
    msgP=msgP.replace('[[[[[[','#C6#').replace(']]]]]]','#C0#')
    msgP=msgP.replace('[[[[[','#C5#').replace(']]]]]','#C0#')
    msgP=msgP.replace('[[[[','#C4#').replace(']]]]','#C0#')
    msgP=msgP.replace('[[[','#C3#').replace(']]]','#C0#')
    msgP=msgP.replace('[[','#C2#').replace(']]','#C0#')
    msgP=msgP.replace('[','#C1#').replace(']','#C0#')
    # msgP = f"{FgColor0}{msgP}{Fore.RESET}{Back.RESET}"
    # msgP=msgP.replace('#RESET#',msgColor)
    # msgP=msgP.replace('#C0#',msgColor)
    # msgP=msgP.replace('#>#','\t')
    # for ix in range(0, len(colors_array)):
    #     if not msgP.find('#') >= 0:
    #         break
    #     msgP=msgP.replace(colors_array[ix][0],colors_array[ix][1])
    return msgP
#############################################################################
#############################################################################
def get_fore_color_based_onBackground(bgcolor,colorindex):
    bgcolor_index = back_colors_dict.get(bgcolor,{}).get('index',0)
    bgcolor_name = color_names[bgcolor_index]
    if bgcolor_name in light_colors:
        ix = colorindex % len(dark_colors)
        fgcolor_name = dark_colors[ix]
        fgcolor = fore_color_names_dict.get(fgcolor_name,{}).get('color','')
    else:
        ix = colorindex % len(light_colors)
        fgcolor_name = light_colors[ix]
        fgcolor = fore_color_names_dict.get(fgcolor_name,{}).get('color','')
    return fgcolor
#############################################################################
def get_back_color_based_onForeground(fgcolor,colorindex):
    fgcolor_index = fore_colors_dict.get(fgcolor,{}).get('index',0)
    fgcolor_name = color_names[fgcolor_index]
    if fgcolor_name in light_colors:
        ix = colorindex % len(dark_colors)
        bgcolor_name = dark_colors[ix]
        bgcolor = back_color_names_dict.get(bgcolor_name,{}).get('color','')
    else:
        ix = colorindex % len(light_colors)
        bgcolor_name = light_colors[ix]
        bgcolor = back_color_names_dict.get(bgcolor_name,{}).get('color','')
    return bgcolor
#############################################################################
def make_colors_array():
    fore_colors = []
    fore_colors.append(Fore.WHITE)
    fore_colors.append(Fore.YELLOW)
    fore_colors.append(Fore.BLUE)
    fore_colors.append(Fore.MAGENTA)
    fore_colors.append(Fore.GREEN)
    fore_colors.append(Fore.CYAN)
    fore_colors.append(Fore.LIGHTWHITE_EX)
    fore_colors.append(Fore.LIGHTYELLOW_EX)
    fore_colors.append(Fore.LIGHTBLUE_EX)
    fore_colors.append(Fore.LIGHTMAGENTA_EX)
    fore_colors.append(Fore.LIGHTGREEN_EX)
    fore_colors.append(Fore.LIGHTCYAN_EX)
    fore_colors.append(Fore.BLACK)
    fore_colors.append(Fore.LIGHTBLACK_EX)
    fore_colors_dict = {}
    fore_colors_dict.update({Fore.WHITE:{'index':0,'darkness':0,'lightness':0,'name':'WHITE'}})
    fore_colors_dict.update({Fore.YELLOW:{'index':1,'darkness':0,'lightness':0,'name':'YELLOW'}})
    fore_colors_dict.update({Fore.BLUE:{'index':2,'darkness':0,'lightness':0,'name':'BLUE'}})
    fore_colors_dict.update({Fore.MAGENTA:{'index':3,'darkness':0,'lightness':0,'name':'MAGENTA'}})
    fore_colors_dict.update({Fore.GREEN:{'index':4,'darkness':0,'lightness':0,'name':'GREEN'}})
    fore_colors_dict.update({Fore.CYAN:{'index':5,'darkness':0,'lightness':0,'name':'CYAN'}})
    fore_colors_dict.update({Fore.LIGHTWHITE_EX:{'index':6,'darkness':0,'lightness':0,'name':'LIGHTWHITE_EX'}})
    fore_colors_dict.update({Fore.LIGHTYELLOW_EX:{'index':7,'darkness':0,'lightness':0,'name':'LIGHTYELLOW_EX'}})
    fore_colors_dict.update({Fore.LIGHTBLUE_EX:{'index':8,'darkness':0,'lightness':0,'name':'LIGHTBLUE_EX'}})
    fore_colors_dict.update({Fore.LIGHTMAGENTA_EX:{'index':9,'darkness':0,'lightness':0,'name':'LIGHTMAGENTA_EX'}})
    fore_colors_dict.update({Fore.LIGHTGREEN_EX:{'index':10,'darkness':0,'lightness':0,'name':'LIGHTGREEN_EX'}})
    fore_colors_dict.update({Fore.LIGHTCYAN_EX:{'index':11,'darkness':0,'lightness':0,'name':'LIGHTCYAN_EX'}})
    fore_colors_dict.update({Fore.BLACK:{'index':12,'darkness':12,'lightness':0,'name':'BLACK'}})
    fore_colors_dict.update({Fore.LIGHTBLACK_EX:{'index':13,'darkness':0,'lightness':0,'name':'LIGHTBLACK_EX'}})

    fore_color_names_dict = {}
    fore_color_names_dict.update({'WHITE': {'index': 0, 'color': Fore.WHITE}})
    fore_color_names_dict.update({'YELLOW': {'index': 1, 'color': Fore.YELLOW}})
    fore_color_names_dict.update({'BLUE': {'index': 2, 'color': Fore.BLUE}})
    fore_color_names_dict.update({'MAGENTA': {'index': 3, 'color': Fore.MAGENTA}})
    fore_color_names_dict.update({'GREEN': {'index': 4, 'color': Fore.GREEN}})
    fore_color_names_dict.update({'CYAN': {'index': 5, 'color': Fore.CYAN}})
    fore_color_names_dict.update({'LIGHTWHITE_EX': {'index': 6, 'color': Fore.LIGHTWHITE_EX}})
    fore_color_names_dict.update({'LIGHTYELLOW_EX': {'index': 7, 'color': Fore.LIGHTYELLOW_EX}})
    fore_color_names_dict.update({'LIGHTBLUE_EX': {'index': 8, 'color': Fore.LIGHTBLUE_EX}})
    fore_color_names_dict.update({'LIGHTMAGENTA_EX': {'index': 9, 'color': Fore.LIGHTMAGENTA_EX}})
    fore_color_names_dict.update({'LIGHTGREEN_EX': {'index': 10, 'color': Fore.LIGHTGREEN_EX}})
    fore_color_names_dict.update({'LIGHTCYAN_EX': {'index': 11, 'color': Fore.LIGHTCYAN_EX}})
    fore_color_names_dict.update({'BLACK': {'index': 12, 'color': Fore.BLACK}})
    fore_color_names_dict.update({'LIGHTBLACK_EX': {'index': 13, 'color': Fore.LIGHTBLACK_EX}})

    back_colors = []
    back_colors.append(Back.WHITE)
    back_colors.append(Back.YELLOW)
    back_colors.append(Back.BLUE)
    back_colors.append(Back.MAGENTA)
    back_colors.append(Back.GREEN)
    back_colors.append(Back.CYAN)
    back_colors.append(Back.LIGHTWHITE_EX)
    back_colors.append(Back.LIGHTYELLOW_EX)
    back_colors.append(Back.LIGHTBLUE_EX)
    back_colors.append(Back.LIGHTMAGENTA_EX)
    back_colors.append(Back.LIGHTGREEN_EX)
    back_colors.append(Back.LIGHTCYAN_EX)
    back_colors.append(Back.BLACK)
    back_colors.append(Back.LIGHTBLACK_EX)
    back_colors_dict = {}
    back_colors_dict.update({Back.WHITE:{'index':0,'darkness':0,'lightness':0,'name':'WHITE'}})
    back_colors_dict.update({Back.YELLOW:{'index':1,'darkness':0,'lightness':0,'name':'YELLOW'}})
    back_colors_dict.update({Back.BLUE:{'index':2,'darkness':1,'lightness':0,'name':'BLUE'}})
    back_colors_dict.update({Back.MAGENTA:{'index':3,'darkness':1,'lightness':0,'name':'MAGENTA'}})
    back_colors_dict.update({Back.GREEN:{'index':4,'darkness':1,'lightness':0,'name':'GREEN'}})
    back_colors_dict.update({Back.CYAN:{'index':5,'darkness':1,'lightness':0,'name':'CYAN'}})
    back_colors_dict.update({Back.LIGHTWHITE_EX:{'index':6,'darkness':0,'lightness':0,'name':'LIGHTWHITE_EX'}})
    back_colors_dict.update({Back.LIGHTYELLOW_EX:{'index':7,'darkness':0,'lightness':0,'name':'LIGHTYELLOW_EX'}})
    back_colors_dict.update({Back.LIGHTBLUE_EX:{'index':8,'darkness':0,'lightness':0,'name':'LIGHTBLUE_EX'}})
    back_colors_dict.update({Back.LIGHTMAGENTA_EX:{'index':9,'darkness':0,'lightness':0,'name':'LIGHTMAGENTA_EX'}})
    back_colors_dict.update({Back.LIGHTGREEN_EX:{'index':10,'darkness':0,'lightness':0,'name':'LIGHTGREEN_EX'}})
    back_colors_dict.update({Back.LIGHTCYAN_EX:{'index':11,'darkness':0,'lightness':0,'name':'LIGHTCYAN_EX'}})
    back_colors_dict.update({Back.BLACK:{'index':12,'darkness':12,'lightness':0,'name':'BLACK'}})
    back_colors_dict.update({Back.LIGHTBLACK_EX:{'index':13,'darkness':0,'lightness':0,'name':'LIGHTBLACK_EX'}})

    back_color_names_dict = {}
    back_color_names_dict.update({'WHITE': {'index': 0, 'color': Back.WHITE}})
    back_color_names_dict.update({'YELLOW': {'index': 1, 'color': Back.YELLOW}})
    back_color_names_dict.update({'BLUE': {'index': 2, 'color': Back.BLUE}})
    back_color_names_dict.update({'MAGENTA': {'index': 3, 'color': Back.MAGENTA}})
    back_color_names_dict.update({'GREEN': {'index': 4, 'color': Back.GREEN}})
    back_color_names_dict.update({'CYAN': {'index': 5, 'color': Back.CYAN}})
    back_color_names_dict.update({'LIGHTWHITE_EX': {'index': 6, 'color': Back.LIGHTWHITE_EX}})
    back_color_names_dict.update({'LIGHTYELLOW_EX': {'index': 7, 'color': Back.LIGHTYELLOW_EX}})
    back_color_names_dict.update({'LIGHTBLUE_EX': {'index': 8, 'color': Back.LIGHTBLUE_EX}})
    back_color_names_dict.update({'LIGHTMAGENTA_EX': {'index': 9, 'color': Back.LIGHTMAGENTA_EX}})
    back_color_names_dict.update({'LIGHTGREEN_EX': {'index': 10, 'color': Back.LIGHTGREEN_EX}})
    back_color_names_dict.update({'LIGHTCYAN_EX': {'index': 11, 'color': Back.LIGHTCYAN_EX}})
    back_color_names_dict.update({'BLACK': {'index': 12, 'color': Back.BLACK}})
    back_color_names_dict.update({'LIGHTBLACK_EX': {'index': 13, 'color': Back.LIGHTBLACK_EX}})
    
    color_names = []
    color_names.append('WHITE')
    color_names.append('YELLOW')
    color_names.append('BLUE')
    color_names.append('MAGENTA')
    color_names.append('GREEN')
    color_names.append('CYAN')
    color_names.append('LIGHTWHITE_EX')
    color_names.append('LIGHTYELLOW_EX')
    color_names.append('LIGHTBLUE_EX')
    color_names.append('LIGHTMAGENTA_EX')
    color_names.append('LIGHTGREEN_EX')
    color_names.append('LIGHTCYAN_EX')
    color_names.append('BLACK')
    color_names.append('LIGHTBLACK_EX')

    dark_colors=['BLUE','MAGENTA','GREEN','CYAN','BLACK','LIGHTBLUE_EX','LIGHTMAGENTA_EX','LIGHTGREEN_EX','LIGHTCYAN_EX','LIGHTBLACK_EX']
    light_colors=[]
    for c in color_names:
        if c not in dark_colors:
            light_colors.append(c)
#::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
#::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
#::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
make_colors_array()
msg = f'module [{module_id}] [[version {module_version}]] loaded.'
if console_on:
    print(colorized_message(msg))
#::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
#::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
#::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
# main
#::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
#::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
#::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
if __name__ == '__main__':
    print(__file__)