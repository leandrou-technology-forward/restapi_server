# -*- coding: utf-8 -*-
import os
import sys
if not (os.path.dirname(__file__) in sys.path): sys.path.append(os.path.dirname(__file__))

import datetime
import uuid
from sqlalchemy.orm import sessionmaker
from sqlalchemy.sql import text
#from sqlalchemy.engine import ddl
#from sqlalchemy import create_engine
#from sqlalchemy import MetaData
#from sqlalchemy import inspect
from _onlineApp import thisApp
from _onlineApp import get_debug_option_as_level,get_debug_files,get_debug_level,Fore
from _onlineApp import log_process_message, log_process_result, log_process_data, log_process_input, log_process_result_message, log_message
from _onlineApp import set_process_identity_dict, set_process_caller_area,get_globals_from_configuration
from _onlineApp import add_methods_to_configuration, get_module_debug_level
from _onlineApp import build_process_signature, build_process_call_area
#from sqlalchemy.ext.declarative import declarative_base
#from _onlineApp import thisApp
# from _database_class_session import leandroutechnologyforward_database_session_class as db_session_class
# from _database_class_table import leandroutechnologyforward_database_table_class as db_table_class
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 
#
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 
module_ProgramName = os.path.splitext(os.path.basename(__file__))[0]
module_id = '{}'.format(module_ProgramName)
module_version = 0.1
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 
#::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
#::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
#::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
#::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
# classes
#::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
#::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
#::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
class leandroutechnologyforward_database_session_class:
    engine = None
    session = None
    schema = None
    debug = False
    session_id=None
    def __init__(self, engine, session=None, schema_dictionary={},session_id=None,debug=None):
        self.engine = engine
        if not session:
            Session = sessionmaker(bind=self.engine)
            session = Session()
        self.session = session
        self.schema = schema_dictionary
        self.session_id = session_id
        self.debug = get_debug_option_as_level(debug)
    #::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
    #::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
    #::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
    # DB <--session--> sqlalchemy workspace
    #::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
    #::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
    #::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
    def get(self, table_model, get_specification, output_method='', caller_area={}, **kwargs):
        if not caller_area:
            print('')
            print(f'{Fore.RED}ooooooooo NO CALLER AREA', 'get')
            print('')

        if output_method.upper().find('DICT') >= 0 or output_method.upper().find('JSON') >= 0:
            return self.get_table_row_as_dict(table_model, get_specification, caller_area=caller_area, **kwargs)
        elif output_method.upper().find('HTML') >= 0:
            return self.get_table_row_as_dict(table_model, get_specification, caller_area=caller_area, **kwargs)
        else:
            return self.get_table_row(table_model, get_specification, caller_area=caller_area, **kwargs)
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 
    def get_rows(self, table_model, get_specification, output_method='', caller_area={}, **kwargs):
        if not caller_area:
            print('')
            print(f'{Fore.RED}ooooooooo NO CALLER AREA', 'get_rows')
            print('')

        if output_method.upper().find('DICT') >= 0 or output_method.upper().find('JSON') >= 0:
            return self.get_table_rows_as_dict(table_model,get_specification, caller_area=caller_area, **kwargs)
        elif output_method.upper().find('HTML') >= 0:
            return self.get_table_rows_as_dict(table_model,get_specification, caller_area=caller_area, **kwargs)
        else:
            return self.get_table_rows(table_model, get_specification, caller_area=caller_area, **kwargs)
    #::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
    def get_list(self, table_model, get_specification, output_method='', caller_area={}, **kwargs):
        if not caller_area:
            print('')
            print(f'{Fore.RED}ooooooooo NO CALLER AREA', 'list')
            print('')

        if output_method.upper().find('DICT') >= 0 or output_method.upper().find('JSON') >= 0:
            return self.get_table_rows_as_dict(table_model,get_specification, caller_area=caller_area, **kwargs)
        elif output_method.upper().find('HTML') >= 0:
            return self.get_table_rows_as_dict(table_model,get_specification, caller_area=caller_area, **kwargs)
        else:
            return self.get_table_rows(table_model, get_specification, caller_area=caller_area, **kwargs)
    #::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
    def refresh(self, table_model, data_record, auto_commit=False, caller_area={}, **kwargs):
        if not caller_area:
            print('')
            print(f'{Fore.RED}ooooooooo NO CALLER AREA', 'refresh')
            print('')
        return self.insert_or_update(table_model, data_record, auto_commit=auto_commit, caller_area=caller_area, **kwargs)
    #::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
    #::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
    #::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
    # session support functions
    #   form DB --> sqlalchemy workspace
    #::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
    #::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
    #::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
    def get_table_row(self, table_model, get_specification, caller_area={}, **kwargs):
        _method_name = 'get_table_row'
        _method_action = 'get'
        _method_entity = table_model.__name__
        _method_table=table_model.__tablename__
        _method_msgID = set_msgID(_method_name, _method_action, _method_table)

        if not caller_area:
            print('')
            print(f'{Fore.RED}ooooooooo NO CALLER AREA', _method_msgID)
            print('')

        _process_identity_kwargs = {'type': 'table', 'module': module_id, 'name': _method_name, 'action': _method_action, 'entity': _method_entity, 'msgID': _method_msgID,}
        _process_adapters_kwargs = {'dbsession': self, 'table_model': table_model, 'table_name': table_model.__tablename__}
        _process_log_kwargs = {'indent_method': 'CALL_LEVEL', 'indent_level':None}
        _process_debug_level = get_debug_level(caller_area.get('debug_level'), **_process_identity_kwargs, **_process_adapters_kwargs)

        _process_debug_files = get_debug_files(_process_debug_level, **_process_identity_kwargs, **_process_adapters_kwargs)
        _process_debug_kwargs={'debug_level':_process_debug_level,'debug_files':_process_debug_files}

        _process_signature = build_process_signature(**_process_identity_kwargs, **_process_adapters_kwargs, **_process_debug_kwargs, **_process_log_kwargs)
        _process_call_area = build_process_call_area(_process_signature, caller_area)

        log_process_input(_method_msgID, 'get_specification', get_specification, **_process_call_area)
        log_process_input(_method_msgID, 'caller_area', caller_area, **_process_call_area)

        filter_specification = self.smart_locate_expression(table_model, get_specification)
        msg1=f"search filter:[[{filter_specification}]]"
        query = self.build_query(table_model, filter_specification)
        if not query:
            msgx = f"query failed"
            msg = msgx + " #C0#" + msg1
            log_process_result_message(_method_msgID,'error',msg,**_process_call_area)
            return None
        
        query_rows = query.count()
        #str(query.count())
        if not query_rows >= 1:
            color = '' #'#RED#'
            msgx = f"NOT-FOUND" #, {color}zero rows retrieved"
            msg = msgx + " #C0#" + msg1
            log_process_result_message(_method_msgID,'warning',msg,**_process_call_area)
            return None
        current_record_obj = query.first()
        color = '' #color = '' #color = '#GREEN#'
        x=''
        if query_rows > 1:
            color = '' #'#RED#'
            x = 's'
        msgx = f"{color}OK, {query_rows} row{x} retrieved"
        msg = msgx + " #C0#" + msg1
        log_process_result_message(_method_msgID, 'success', msg, **_process_call_area)
        return current_record_obj
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 
    def get_table_rows(self, table_model, get_specification, caller_area={}, **kwargs):
        _method_name = 'get_table_rows'
        _method_action = 'get_table_rows'
        _method_entity = table_model.__name__
        _method_table = table_model.__tablename__
        _method_msgID = set_msgID(_method_name, _method_action, _method_table)

        if not caller_area:
            print('')
            print(f'{Fore.RED}ooooooooo NO CALLER AREA', _method_msgID)
            print('')

        _process_identity_kwargs = {'type': 'table', 'module': module_id, 'name': _method_name, 'action': _method_action, 'entity': _method_entity, 'msgID': _method_msgID,}
        _process_adapters_kwargs = {'dbsession': self, 'table_model': table_model, 'table_name': table_model.__tablename__}
        _process_log_kwargs = {'indent_method': 'CALL_LEVEL', 'indent_level':None}
        _process_debug_level = get_debug_level(caller_area.get('debug_level'), **_process_identity_kwargs, **_process_adapters_kwargs)
        _process_debug_files = get_debug_files(_process_debug_level, **_process_identity_kwargs, **_process_adapters_kwargs)
        _process_debug_kwargs={'debug_level':_process_debug_level,'debug_files':_process_debug_files}

        _process_signature = build_process_signature(**_process_identity_kwargs, **_process_adapters_kwargs, **_process_debug_kwargs, **_process_log_kwargs)
        _process_call_area = build_process_call_area(_process_signature, caller_area)

        log_process_input(_method_msgID, 'get_specification', get_specification, **_process_call_area)
        log_process_input(_method_msgID, 'caller_area', caller_area, **_process_call_area)

        filter_specification = self.smart_locate_expression(table_model, get_specification)
        msg1=f"search filter:[[{filter_specification}]]"
        query = self.build_query(table_model, filter_specification)
        if not query:
            msgx = f"query failed"
            msg = msgx + " #C0#" + msg1
            log_process_result_message(_method_msgID,'error',msg,**_process_call_area)
            return None
        query_rows = query.count()
        if not query_rows >= 1:
            color = '' #'#RED#'
            msgx = f"NOT-FOUND" #, {color}zero rows retrieved"
            msg = msgx + " #C0#" + msg1
            log_process_result_message(_method_msgID,'warning',msg,**_process_call_area)
            return None
        current_record_objects = query.all()
        color = '' #color = '#GREEN#'
        x=''
        if query_rows > 1:
            color = '' #'#RED#'
            x = 's'
        msgx = f"{color}OK, {query_rows} row{x} retrieved"
        msg = msgx + " #C0#" + msg1
        log_process_result_message(_method_msgID,'success',msg,**_process_call_area)
        return current_record_objects
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 
    def insert_or_update(self, table_model, data_record, auto_commit=False, caller_area={}, **kwargs):
        _method_name = 'insert_or_update'
        _method_action = 'insert_or_update'
        _method_entity = table_model.__name__
        _method_table = table_model.__tablename__
        _method_msgID = set_msgID(_method_name, _method_action, _method_table)

        _process_identity_kwargs = {'type': 'table', 'module': module_id, 'name': _method_name, 'action': _method_action, 'entity': _method_entity, 'msgID': _method_msgID,}
        _process_adapters_kwargs = {'dbsession': self, 'table_model': table_model, 'table_name': table_model.__tablename__}
        _process_log_kwargs = {'indent_method': 'CALL_LEVEL', 'indent_level':None}

        _process_debug_level = get_debug_level(caller_area.get('debug_level'), **_process_identity_kwargs, **_process_adapters_kwargs)
        _process_debug_files = get_debug_files(_process_debug_level, **_process_identity_kwargs, **_process_adapters_kwargs)
        _process_debug_kwargs={'debug_level':_process_debug_level,'debug_files':_process_debug_files}

        _process_signature = build_process_signature(**_process_identity_kwargs, **_process_adapters_kwargs, **_process_debug_kwargs, **_process_log_kwargs)
        _process_call_area = build_process_call_area(_process_signature, caller_area)

        log_process_input(_method_msgID, 'auto_commit', auto_commit, **_process_call_area)
        log_process_input(_method_msgID, 'data_record', data_record, **_process_call_area)
        log_process_input(_method_msgID, 'caller_area', caller_area, **_process_call_area)
        
        filter_specification = self.smart_locate_expression(table_model, data_record)
        msg1=f"search filter:[[{filter_specification}]]"
        query = self.build_query(table_model, filter_specification)
        if not query:
            msgx = f"query failed"
            msg = msgx + " #C0#" + msg1
            log_process_result_message(_method_msgID,'error',msg,**_process_call_area)
            return None        
        query_rows = query.count()
        #str(query.count())
        if not query_rows >= 1:
            color = '' #'#RED#'
            msgx = f"NOT-FOUND" #, {color}zero rows retrieved"
            msg = msgx + " #C0#" + msg1
            log_process_result_message(_method_msgID,'warning',msg,**_process_call_area)
            current_record_obj = None
        else:
            current_record_obj = query.first()
            color = '' #color = '#GREEN#'
            x=''
            if query_rows > 1:
                color = '' #'#RED#'
                x = 's'
            msgx = f"{color}OK, {query_rows} row{x} retrieved"
            msg = msgx + " #C0#" + msg1
            log_process_message(_method_msgID,'success',msg,**_process_call_area)

        if not current_record_obj:
            _method_action='ADD'
            current_record_obj=table_model()
            valid_fields_dictionary = current_record_obj.valid_model_fields_dictionary(data_record)
            changes = self.update_from_dict(current_record_obj, **valid_fields_dictionary)
            if changes:log_process_data(_method_msgID, 'record changes', changes, **_process_call_area)
            (ok,messages) = current_record_obj.input_validation(valid_fields_dictionary)
            if not ok:
                msg=f'{_method_entity.upper()} input validation errors'
                api_result = {'api_status': 'error', 'api_message': msg, 'api_data': valid_fields_dictionary, 'messages':messages, 'rows_added':0, 'api_action': _method_action.upper(), 'api_name':_method_name }
                log_process_result(_method_msgID,api_result,**_process_call_area)
                return None
            self.session.add(current_record_obj)
            if auto_commit:
                self.commit(**_process_call_area)
                msg = f'OK. {table_model.__name__.upper()} added'
                rows_added=1
            else:
                rows_added=0
                msg = f'OK. {table_model.__name__.upper()} ready for addition'
            current_record_dict = current_record_obj.to_dict()
            api_result = {'api_status': 'success', 'api_message': msg, 'api_data': current_record_dict, 'rows_added':rows_added,'rows_updated':0, 'api_action': _method_action.upper(), 'api_name': _method_name}
            log_process_result(_method_msgID,api_result,**_process_call_area)
            return current_record_obj
        else:
            _method_action='UPDATE'
            valid_fields_dictionary = current_record_obj.valid_model_fields_dictionary(data_record)
            changes = self.update_from_dict(current_record_obj, **valid_fields_dictionary)
            if changes:log_process_data(_method_msgID, 'record changes', changes, **_process_call_area)
            if not current_record_obj.has_model_changed():
                msg=f"OK. {table_model.__name__.upper()} is synchronized. no changes applied"
                api_result = {'api_status': 'success', 'api_message': msg, 'api_data': valid_fields_dictionary, 'rows_added':0,'rows_updated':0, 'api_action': _method_action.upper(), 'api_name':_method_name }
                log_process_result(_method_msgID,api_result,**_process_call_area)
                return current_record_obj
            (ok,messages) = current_record_obj.update_validation(valid_fields_dictionary)
            if not ok:
                msg=f'update validation errors'
                api_result = {'api_status': 'error', 'api_message': msg, 'api_data': current_record_dict, 'messages':messages, 'rows_updated':0, 'api_action': _method_action.upper(), 'api_name':_method_name }
                log_process_result(_method_msgID,api_result,**_process_call_area)
                return None
            self.session.add(current_record_obj)
            if auto_commit:
                try:
                    self.commit(**_process_call_area)
                    msg = f'OK. {table_model.__name__.upper()} updated'
                    rows_updated = 1
                except Exception as error_text:
                    msg = f'{table_model.__name__.upper()} update failed:{error_text}'
                    rows_updated = 0
                    print(error_text)
            else:
                rows_updated=0
                msg = f'OK. {table_model.__name__.upper()} ready for update'
            current_record_dict = current_record_obj.to_dict()
            api_result = {'api_status': 'success', 'api_message': msg, 'api_data': current_record_dict, 'rows_added':0,'rows_updated':rows_updated, 'api_action': _method_action.upper(), 'api_name': _method_name}
            log_process_result(_method_msgID,api_result,**_process_call_area)
            return current_record_obj
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 
    def insert(self, table_model, data_record, auto_commit=False, caller_area={}, **kwargs):
        _method_name='insert'
        _method_action='ADD'
        _method_entity = table_model.__name__
        _method_table = table_model.__tablename__ 
        _method_msgID = set_msgID(_method_name, _method_action, _method_table)

        _process_identity_kwargs = {'type': 'table', 'module': module_id, 'name': _method_name, 'action': _method_action, 'entity': _method_entity, 'msgID': _method_msgID,}
        _process_adapters_kwargs = {'dbsession': self, 'table_model': table_model, 'table_name': table_model.__tablename__}
        _process_log_kwargs = {'indent_method': 'CALL_LEVEL', 'indent_level':None}
        _process_debug_level = get_debug_level(caller_area.get('debug_level'), **_process_identity_kwargs, **_process_adapters_kwargs)
        _process_debug_files = get_debug_files(_process_debug_level, **_process_identity_kwargs, **_process_adapters_kwargs)
        _process_debug_kwargs={'debug_level':_process_debug_level,'debug_files':_process_debug_files}

        _process_signature = build_process_signature(**_process_identity_kwargs, **_process_adapters_kwargs, **_process_debug_kwargs, **_process_log_kwargs)
        _process_call_area = build_process_call_area(_process_signature, caller_area)

        log_process_input(_method_msgID, 'auto_commit', auto_commit, **_process_call_area)
        log_process_input(_method_msgID, 'data_record', data_record, **_process_call_area)
        log_process_input(_method_msgID, 'caller_area', caller_area, **_process_call_area)

        messages=[]

        filter_specification = self.smart_locate_expression2(table_model, data_record)
        msg1=f"search filter:[[{filter_specification}]]"
        query = self.build_query(table_model, filter_specification)
        if not query:
            msgx = f"query failed"
            msg = msgx + " #C0#" + msg1
            log_process_result_message(_method_msgID,'error',msg,**_process_call_area)
            return None        
        query_rows = query.count()
        #str(query.count())
        if not query_rows >= 1:
            color = '' #color = '#GREEN#'
            msgx = f"OK, not found"#, {color}zero rows retrieved"
            msg = msgx + " #C0#" + msg1
            log_process_message(_method_msgID,'success',msg,**_process_call_area)
            current_record_obj = None
        else:
            current_record_obj = query.first()
            color = '' #'#RED#'
            x=''
            if query_rows > 1:
                color = '' #'#RED#'
                x = 's'
            msgx = f"{color}{query_rows} row{x} retrieved"
            msg = msgx + " #C0#" + msg1
            log_process_message(_method_msgID,'warning',msg,**_process_call_area)

        if current_record_obj:
            current_record_dict = current_record_obj.to_dict()
            msg=f'[{table_model.__name__.upper()}] already exists. filter: [[{filter_specification}]]'
            api_result = {'api_status': 'error', 'api_message': msg, 'api_data': current_record_dict, 'messages':messages, 'rows_added':0, 'api_action': _method_action.upper(), 'api_name':_method_name }
            log_process_result(_method_msgID,api_result,**_process_call_area)
            return None

        _method_action='ADD'
        current_record_obj=table_model()
        valid_fields_dictionary = current_record_obj.valid_model_fields_dictionary(data_record)
        changes = self.update_from_dict(current_record_obj, **valid_fields_dictionary)
        if changes:log_process_data(_method_msgID, 'record changes', changes, **_process_call_area)
        (ok,messages) = current_record_obj.input_validation(valid_fields_dictionary)
        if not ok:
            msg=f'{_method_entity.upper()} input validation errors'
            api_result = {'api_status': 'error', 'api_message': msg, 'api_data': valid_fields_dictionary, 'messages':messages, 'rows_added':0, 'api_action': _method_action.upper(), 'api_name':_method_name }
            log_process_result(_method_msgID,api_result,**_process_call_area)
            return None
        self.session.add(current_record_obj)
        if auto_commit:
            self.commit(**_process_call_area)
            msg = f'OK. {table_model.__name__.upper()} added committed'
            rows_added=1
        else:
            rows_added=1
            msg = f'OK. {table_model.__name__.upper()} added not committed'
        current_record_dict = current_record_obj.to_dict()
        api_result = {'api_status': 'success', 'api_message': msg, 'api_data': current_record_dict, 'rows_added':rows_added,'rows_updated':0, 'api_action': _method_action.upper(), 'api_name': _method_name}
        log_process_result(_method_msgID,api_result,**_process_call_area)
        return current_record_obj
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 
    def update(self, table_model, data_record, update_filter={}, auto_commit=False, caller_area={}, **kwargs):
        _method_name='update'
        _method_action = 'UPDATE'
        _method_entity = table_model.__name__
        _method_table = table_model.__tablename__ 
        _method_msgID = set_msgID(_method_name, _method_action, _method_table)

        if not caller_area:
            print('')
            print(f'{Fore.RED}ooooooooo NO CALLER AREA', _method_msgID)
            print('')

        _process_identity_kwargs = {'type': 'table', 'module': module_id, 'name': _method_name, 'action': _method_action, 'entity': _method_entity, 'msgID': _method_msgID,}
        _process_adapters_kwargs = {'dbsession': self, 'table_model': table_model, 'table_name': table_model.__tablename__}
        _process_log_kwargs = {'indent_method': 'CALL_LEVEL', 'indent_level':None}
        _process_debug_level = get_debug_level(caller_area.get('debug_level'), **_process_identity_kwargs, **_process_adapters_kwargs)
        _process_debug_files = get_debug_files(_process_debug_level, **_process_identity_kwargs, **_process_adapters_kwargs)
        _process_debug_kwargs={'debug_level':_process_debug_level,'debug_files':_process_debug_files}

        _process_signature = build_process_signature(**_process_identity_kwargs, **_process_adapters_kwargs, **_process_debug_kwargs, **_process_log_kwargs)
        _process_call_area = build_process_call_area(_process_signature, caller_area)

        log_process_input(_method_msgID, 'auto_commit', auto_commit, **_process_call_area)
        log_process_input(_method_msgID, 'data_record', data_record, **_process_call_area)
        log_process_input(_method_msgID, 'caller_area', caller_area, **_process_call_area)

        messages=[]

        # record filter expression
        if update_filter:
            locate_dict = {**update_filter}
        else:
            locate_dict = {**data_record}

        # # locate record
        # locate_dict = {**update_filter, **data_record}

        filter_specification = self.smart_locate_expression(table_model, locate_dict)
        msg1=f"search filter:[[{filter_specification}]]"
        query = self.build_query(table_model, filter_specification)
        if not query:
            msgx = f"query failed"
            msg = msgx + " #C0#" + msg1
            log_process_result_message(_method_msgID,'error',msg,**_process_call_area)
            return None        
        query_rows = query.count()
        #str(query.count())
        if not query_rows >= 1:
            color = '' #'#RED#'
            msgx = f"NOT-FOUND" #, {color}zero rows retrieved"
            msg = msgx + " #C0#" + msg1
            log_process_message(_method_msgID,'warning',msg,**_process_call_area)
            current_record_obj = None
        else:
            current_record_obj = query.first()
            color = '' #color = '#GREEN#'
            msgType='success'
            x=''
            if query_rows > 1:
                msgType='warning'
                color = '' #'#RED#'
                x = 's'
            msgx = f"{color}OK, {query_rows} row{x} retrieved"
            msg = msgx + " #C0#" + msg1
            log_process_message(_method_msgID,msgType,msg,**_process_call_area)

        if not current_record_obj:
            current_record_dict = current_record_obj.to_dict()
            msg=f'[{table_model.__name__.upper()}] not exists. filter: [[{filter_specification}]]'
            api_result = {'api_status': 'error', 'api_message': msg, 'api_data': data_record, 'messages':messages, 'rows_added':0, 'api_action': _method_action.upper(), 'api_name':_method_name }
            log_process_result(_method_msgID,api_result,**_process_call_area)
            return None

        valid_fields_dictionary = current_record_obj.valid_model_fields_dictionary(data_record)
        changes = self.update_from_dict(current_record_obj, **valid_fields_dictionary)
        if changes:log_process_data(_method_msgID, 'record changes', changes, **_process_call_area)
        if not current_record_obj.has_model_changed():
            msg=f"OK. {table_model.__name__.upper()} is synchronized. no changes applied"
            api_result = {'api_status': 'success', 'api_message': msg, 'api_data': valid_fields_dictionary, 'rows_added':0,'rows_updated':0, 'api_action': _method_action.upper(), 'api_name':_method_name }
            log_process_result(_method_msgID,api_result,**_process_call_area)
            return current_record_obj
        (ok,messages) = current_record_obj.update_validation(valid_fields_dictionary)
        if not ok:
            msg=f'{_method_entity.upper()} update validation errors'
            api_result = {'api_status': 'error', 'api_message': msg, 'api_data': current_record_dict, 'messages':messages, 'rows_updated':0, 'api_action': _method_action.upper(), 'api_name':_method_name }
            log_process_result(_method_msgID,api_result,**_process_call_area)
            return None
        self.session.add(current_record_obj)
        if auto_commit:
            self.commit(**_process_call_area)
            msg = f'OK. {table_model.__name__.upper()} updated committed'
            rows_updated=1
        else:
            rows_updated=1
            msg = f'OK. {table_model.__name__.upper()} updated not committed'
        current_record_dict = current_record_obj.to_dict()
        api_result = {'api_status': 'success', 'api_message': msg, 'api_data': current_record_dict, 'rows_added':0,'rows_updated':rows_updated, 'api_action': _method_action.upper(), 'api_name': _method_name}
        log_process_result(_method_msgID,api_result,**_process_call_area)
        return current_record_obj
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 
    def table_action(self, table_model, action, data_record, action_filter={}, auto_commit=False, caller_area={}, **kwargs):
        _method_name = 'table_action' 
        _method_action = action
        _method_entity = table_model.__name__
        _method_table = table_model.__tablename__ 
        _method_msgID = set_msgID(_method_name, _method_action, _method_table)+' #XBLUE#'+_method_action.upper()+'#C0#'

        if not caller_area:
            print('')
            print(f'{Fore.RED}ooooooooo NO CALLER AREA', _method_msgID)
            print('')

        _process_identity_kwargs = {'type': 'table', 'module': module_id, 'name': _method_name, 'action': _method_action, 'entity': _method_entity, 'msgID': _method_msgID,}
        _process_adapters_kwargs = {'dbsession': self, 'table_model': table_model, 'table_name': table_model.__tablename__}
        _process_log_kwargs = {'indent_method': 'CALL_LEVEL', 'indent_level':None}
        _process_debug_level = get_debug_level(caller_area.get('debug_level'), **_process_identity_kwargs, **_process_adapters_kwargs)
        _process_debug_files = get_debug_files(_process_debug_level, **_process_identity_kwargs, **_process_adapters_kwargs)
        _process_debug_kwargs={'debug_level':_process_debug_level,'debug_files':_process_debug_files}

        _process_signature = build_process_signature(**_process_identity_kwargs, **_process_adapters_kwargs, **_process_debug_kwargs, **_process_log_kwargs)
        _process_call_area = build_process_call_area(_process_signature, caller_area)

        msg=f'#C0#action=#BLUE#{action.upper()}#C0#'
        log_process_message(_method_msgID, '', msg, **_process_call_area)

        log_process_input(_method_msgID, 'auto_commit', auto_commit, **_process_call_area)
        log_process_input(_method_msgID, 'data_record', data_record,**_process_call_area)
        log_process_input(_method_msgID, 'action_filter', action_filter,**_process_call_area)
        log_process_input(_method_msgID, 'caller_area', caller_area,**_process_call_area)

        row_count = 0
        rows_updated = 0
        action = action.replace('_', '-')
        actions_supported = ('ADD', 'UPDATE', 'UPDATE-ROWS', 'REFRESH', 'REGISTER', 'UNREGISTER', 'DELETE', 'REMOVE', 'ACTIVATE', 'DEACTIVATE', 'CONFIRM', 'INQUIRY', 'LIST', 'GET')
        if action.upper() not in actions_supported:
            msg = f"action '{action}' not supported. {actions_supported}"
            api_result = {'api_status': 'error', 'api_message': msg, 'api_data': actions_supported, 'row_count':row_count,'rows_updated':rows_updated, 'api_action': _method_action.upper(), 'api_name': _method_name}
            log_process_result(_method_msgID,api_result,**_process_call_area)
            return api_result

        now = datetime.datetime.utcnow()

        # record filter expression
        if action_filter:
            locate_dict = {**action_filter}
        else:
            locate_dict = {**data_record}

        if action.upper() in ('LIST'):
            # locate_dict = {**action_filter, **data_record} 
            records_dict = self.get_table_rows_as_dict(table_model, locate_dict, caller_area=_process_call_area, **kwargs)
            row_count = len(records_dict)
            msg = f"OK. {row_count} {_method_entity.upper()} rows retrieved"
            api_result = {'api_status': 'success', 'api_message': msg, 'api_data': records_dict, 'api_data_rows': row_count, 'api_action': _method_action.upper(), 'api_name': _method_name}
            log_process_result(_method_msgID,api_result,**_process_call_area)
            return api_result
        elif action.upper()=='UPDATE-ROWS':
            locate_dict = {**action_filter} 
            records = self.get_table_rows(table_model, action_filter, caller_area=_process_call_area, **kwargs)
            if not records:
                records={}
            row_count = len(records)
            msg = f"OK. {row_count} {_method_entity.upper()} rows retrieved"
            if len(records) <= 0:
                msg = f"zero {_method_entity.upper()} records found. No Update"
                api_result = {'api_status': 'success', 'api_message': msg, 'api_data': {},'row_count':row_count,'rows_updated':0, 'api_action': _method_action.upper(), 'api_name': _method_name}
                log_process_result(_method_msgID,api_result,**_process_call_area)
                return api_result
            rows_updated = 0
            for current_record_obj in records:
                record_dict = current_record_obj.to_dict()
                valid_fields_dictionary = current_record_obj.valid_model_fields_dictionary(data_record)
                changes = self.update_from_dict(current_record_obj, **valid_fields_dictionary)
                if changes:log_process_data(_method_msgID, 'record changes', changes, **_process_call_area)
                (ok,messages) = current_record_obj.update_validation(valid_fields_dictionary)
                if not ok:
                    msg=f'{_method_entity.upper()} update validation errors'
                    api_result = {'api_status': 'error', 'api_message': msg, 'api_data': record_dict, 'messages':messages, 'rows_updated':0, 'api_action': _method_action.upper(), 'api_name':_method_name }
                    log_process_result(_method_msgID,api_result,**_process_call_area)
                    self.rollback(**_process_call_area)
                    return api_result
                else:
                    if current_record_obj.has_model_changed():
                        rows_updated = rows_updated + 1
            if rows_updated>0 and auto_commit:
                self.commit(**_process_call_area)
            records_dict = self.rows_to_dict(table_model,records)
            msg = f'OK. {rows_updated} {_method_entity.upper()} rows updated'
            api_result = {'api_status': 'success', 'api_message': msg, 'api_data': records_dict, 'row_count':row_count,'rows_updated':rows_updated, 'api_action': _method_action.upper(), 'api_name':_method_name }
            log_process_result(_method_msgID,api_result,**_process_call_area)
            return api_result

        # # locate record
        # if action_filter:
        #     locate_dict = {**action_filter}
        # else:
        #     locate_dict = {**data_record}

        # get from database
        current_record_obj = self.get_table_row(table_model, locate_dict, caller_area=_process_call_area, **kwargs)
        #current_record_obj = APIS.get_one_row(locate_dict)

        #generic validations
        if current_record_obj:
            record_dict = current_record_obj.to_dict()
            if action.upper() in ('ADD'):
                msg=f'{_method_entity.upper()} already exist'
                api_result = {'api_status': 'error', 'api_message': msg, 'api_data': record_dict, 'api_action': _method_action.upper(), 'api_name':_method_name }
                log_process_result(_method_msgID,api_result,**_process_call_area)
                return api_result
        else:
            if action.upper() not in ('ADD', 'REFRESH','REGISTER'):
                current_record_obj=table_model()
                record_dict = current_record_obj.valid_model_fields_dictionary(data_record)
                msg = f'{_method_entity.upper()} not found'
                api_result = {'api_status': 'error', 'api_message': msg, 'api_data': record_dict, 'api_action': _method_action.upper(), 'api_name':_method_name }
                log_process_result(_method_msgID,api_result,**_process_call_area)
                return api_result

        if action.upper() in ('ADD'):   
            current_record_obj=table_model()
            valid_fields_dictionary = current_record_obj.valid_model_fields_dictionary(data_record)
            changes = self.update_from_dict(current_record_obj, **valid_fields_dictionary)
            if changes:log_process_data(_method_msgID, 'record changes', changes, **_process_call_area)
            (ok,messages) = current_record_obj.input_validation(valid_fields_dictionary)
            if not ok:
                msg=f'{_method_entity.upper()} input validation errors'
                api_result = {'api_status': 'error', 'api_message': msg, 'api_data': record_dict, 'messages':messages, 'rows_added':0, 'api_action': _method_action.upper(), 'api_name':_method_name }
                log_process_result(_method_msgID,api_result,**_process_call_area)
                return api_result

            self.session.add(current_record_obj)
            if auto_commit:
                self.commit(**_process_call_area)
            record_dict = current_record_obj.to_dict()
            msg=f'OK. {_method_entity.upper()} added'
            api_result = {'api_status': 'success', 'api_message': msg, 'api_data': record_dict, 'rows_added':1, 'api_action': _method_action.upper(), 'api_name':_method_name }
            log_process_result(_method_msgID,api_result,**_process_call_area)
            return api_result
        elif action.upper() in ('UPDATE'):   
            valid_fields_dictionary = current_record_obj.valid_model_fields_dictionary(data_record)
            changes = self.update_from_dict(current_record_obj, **valid_fields_dictionary)
            if changes:log_process_data(_method_msgID, 'record changes', changes, **_process_call_area)
            if not current_record_obj.has_model_changed():
                msg=f"OK. {_method_entity.upper()} is synchronized. no changes applied"
                api_result = {'api_status': 'success', 'api_message': msg, 'api_data': record_dict,'rows_updated':0, 'api_action': _method_action.upper(), 'api_name':_method_name }
                log_process_result(_method_msgID,api_result,**_process_call_area)
                return api_result
            (ok,messages) = current_record_obj.update_validation(valid_fields_dictionary)
            if not ok:
                msg=f'{_method_entity.upper()} update validation errors'
                api_result = {'api_status': 'error', 'api_message': msg, 'api_data': record_dict, 'messages':messages, 'rows_updated':0, 'api_action': _method_action.upper(), 'api_name':_method_name }
                log_process_result(_method_msgID,api_result,**_process_call_area)
                return api_result
            self.session.add(current_record_obj)
            if auto_commit:
                self.commit(**_process_call_area)
            record_dict = current_record_obj.to_dict()
            msg = f'OK. {_method_entity.upper()} updated'
            api_result = {'api_status': 'success', 'api_message': msg, 'api_data': record_dict, 'rows_updated':1, 'api_action': _method_action.upper(), 'api_name':_method_name }
            log_process_result(_method_msgID,api_result,**_process_call_area)
            return api_result
        elif action.upper() in ('REFRESH','REGISTER'):   
            if not current_record_obj:
                current_record_obj=table_model()
                valid_fields_dictionary = current_record_obj.valid_model_fields_dictionary(data_record)
                changes = self.update_from_dict(current_record_obj, **valid_fields_dictionary)
                if changes:log_process_data(_method_msgID, 'record changes', changes, **_process_call_area)
                (ok,messages) = current_record_obj.input_validation(valid_fields_dictionary)
                if not ok:
                    msg=f'{_method_entity.upper()} input validation errors'
                    api_result = {'api_status': 'error', 'api_message': msg, 'api_data': record_dict, 'messages':messages, 'rows_added':0, 'api_action': _method_action.upper(), 'api_name':_method_name }
                    log_process_result(_method_msgID,api_result,**_process_call_area)
                    return api_result
                self.session.add(current_record_obj)
                if auto_commit:
                    self.commit(**_process_call_area)
                record_dict = current_record_obj.to_dict()
                msg=f'OK. {_method_entity.upper()} added'
                api_result = {'api_status': 'success', 'api_message': msg, 'api_data': record_dict, 'rows_added':1,'rows_updated':0, 'api_action': _method_action.upper(), 'api_name': _method_name}
                log_process_result(_method_msgID,api_result,**_process_call_area)
                return api_result
            else:
                valid_fields_dictionary = current_record_obj.valid_model_fields_dictionary(data_record)
                changes = self.update_from_dict(current_record_obj, **valid_fields_dictionary)
                if changes:log_process_data(_method_msgID, 'record changes', changes, **_process_call_area)
                if not current_record_obj.has_model_changed():
                    msg=f"OK. {_method_entity.upper()} is synchronized. no changes applied"
                    api_result = {'api_status': 'success', 'api_message': msg, 'api_data': record_dict, 'rows_added':0,'rows_updated':0, 'api_action': _method_action.upper(), 'api_name':_method_name }
                    log_process_result(_method_msgID,api_result,**_process_call_area)
                    return api_result
                (ok,messages) = current_record_obj.update_validation(valid_fields_dictionary)
                if not ok:
                    msg=f'{_method_entity.upper()} update validation errors'
                    api_result = {'api_status': 'error', 'api_message': msg, 'api_data': record_dict, 'messages':messages, 'rows_updated':0, 'api_action': _method_action.upper(), 'api_name':_method_name }
                    log_process_result(_method_msgID,api_result,**_process_call_area)
                    return api_result
                self.session.add(current_record_obj)
                if auto_commit:
                    self.commit(**_process_call_area)
                record_dict = current_record_obj.to_dict()
                msg = f'OK. {_method_entity.upper()} refreshed'
                api_result = {'api_status': 'success', 'api_message': msg, 'api_data': record_dict, 'rows_added':0,'rows_updated':1, 'api_action': _method_action.upper(), 'api_name':_method_name }
                log_process_result(_method_msgID,api_result,**_process_call_area)
                return api_result
        elif action.upper() in ('DELETE'):   
            if str(current_record_obj.status).upper() in ('DELETED'):
                msg = f'OK. {_method_entity.upper()} already Deleted (status:{current_record_obj.status})'
                api_result = {'api_status': 'success', 'api_message': msg, 'api_data': record_dict, 'api_action': _method_action.upper(), 'api_name':_method_name }
                log_process_result(_method_msgID,api_result,**_process_call_area)
                return api_result
            current_record_obj.status='Deleted'
            if auto_commit:
                self.commit(**_process_call_area)
            record_dict = current_record_obj.to_dict()
            msg = f'OK. {_method_entity.upper()} deleted'
            api_result = {'api_status': 'success', 'api_message': msg, 'api_data': record_dict, 'api_action': _method_action.upper(), 'api_name':_method_name }
            log_process_result(_method_msgID,api_result,**_process_call_area)
            return api_result
        elif action.upper() in ('REMOVE'):   
            if str(current_record_obj.status).upper() not in ('DELETED'):
                msg = f'{_method_entity.upper()} must be DELETED before REMOVED (status:{current_record_obj.status})'
                api_result = {'api_status': 'error', 'api_message': msg, 'api_data': record_dict, 'api_action': _method_action.upper(), 'api_name':_method_name }
                log_process_result(_method_msgID,api_result,**_process_call_area)
                return api_result
            self.session.delete(current_record_obj)
            if auto_commit:
                self.commit(**_process_call_area)
            msg = f'OK. {_method_entity.upper()} removed'
            api_result = {'api_status': 'success', 'api_message': msg, 'api_data': record_dict, 'api_action': _method_action.upper(), 'api_name':_method_name }
            log_process_result(_method_msgID,api_result,**_process_call_area)
            return api_result
        elif action.upper() in ('ACTIVATE'):
            if str(current_record_obj.status).upper() in ('ACTIVE'):
                msg = f'OK. {_method_entity.upper()} already Active (status:{current_record_obj.status})'
                api_result = {'api_status': 'success', 'api_message': msg, 'api_data': record_dict, 'api_action': _method_action.upper(), 'api_name':_method_name }
                log_process_result(_method_msgID,api_result,**_process_call_area)
                return api_result
            current_record_obj.status='Active'
            if auto_commit:
                self.commit(**_process_call_area)
            record_dict = current_record_obj.to_dict()
            msg = f'OK. {_method_entity.upper()} activated'
            api_result = {'api_status': 'success', 'api_message': msg, 'api_data': record_dict, 'api_action': _method_action.upper(), 'api_name':_method_name }
            log_process_result(_method_msgID,api_result,**_process_call_area)
            return api_result
        elif action.upper() in ('DEACTIVATE'):   
            if str(current_record_obj.status).upper() not in ('ACTIVE'):
                msg = f'OK. {_method_entity.upper()} already inActive (status:{current_record_obj.status})'
                api_result = {'api_status': 'success', 'api_message': msg, 'api_data': record_dict, 'api_action': _method_action.upper(), 'api_name':_method_name }
                log_process_result(_method_msgID,api_result,**_process_call_area)
                return api_result
            current_record_obj.status='InActive'
            if auto_commit:
                self.commit(**_process_call_area)
            record_dict = current_record_obj.to_dict()
            msg = f'OK. {_method_entity.upper()} deactivated'
            api_result = {'api_status': 'success', 'api_message': msg, 'api_data': record_dict, 'api_action': _method_action.upper(), 'api_name':_method_name }
            log_process_result(_method_msgID,api_result,**_process_call_area)
            return api_result
        elif action.upper() in ('UNREGISTER'):   
            if str(current_record_obj.status).upper() not in ('ACTIVE'):
                msg = f'OK. {_method_entity.upper()} already inActive (status:{current_record_obj.status})'
                api_result = {'api_status': 'success', 'api_message': msg, 'api_data': record_dict, 'api_action': _method_action.upper(), 'api_name':_method_name }
                log_process_result(_method_msgID,api_result,**_process_call_area)
                return api_result
            current_record_obj.status='UnRegistered'
            if auto_commit:
                self.commit(**_process_call_area)
            record_dict = current_record_obj.to_dict()
            msg = f'OK. {_method_entity.upper()} UnRegistered'
            api_result = {'api_status': 'success', 'api_message': msg, 'api_data': record_dict, 'api_action': _method_action.upper(), 'api_name':_method_name }
            log_process_result(_method_msgID,api_result,**_process_call_area)
            return api_result
        elif action.upper() in ('CONFIRM'):
            try:
                confirmed = current_record_obj.confirmed
                confirmed_in_record = True
            except:
                confirmed = 0
                confirmed_in_record = False

            if confirmed_in_record:
                if confirmed:
                    if str(current_record_obj.status).upper() in ('ACTIVE'):
                        msg = f'OK. {_method_entity.upper()} already Confirmed (status:{current_record_obj.status})'
                        api_result = {'api_status': 'success', 'api_message': msg, 'api_data': record_dict, 'api_action': _method_action.upper(), 'api_name':_method_name }
                        log_process_result(_method_msgID, api_result, **_process_call_area)
                        return api_result
                    else:
                        msg = f'OK. {_method_entity.upper()} Confirmed but status not active. (status:{current_record_obj.status})'
                        api_result = {'api_status': 'success', 'api_message': msg, 'api_data': record_dict, 'api_action': _method_action.upper(), 'api_name':_method_name }
                        log_process_message(_method_msgID, 'warning', msg, **_process_call_area)
            else:
                if str(current_record_obj.status).upper() in ('ACTIVE'):
                    msg = f'OK. {_method_entity.upper()} already Confirmed (status:{current_record_obj.status})'
                    api_result = {'api_status': 'success', 'api_message': msg, 'api_data': record_dict, 'api_action': _method_action.upper(), 'api_name':_method_name }
                    log_process_result(_method_msgID, api_result, **_process_call_area)
                    return api_result

            if not confirmed:
                current_record_obj.status='Confirmed'
                try:
                    current_record_obj.confirmed_timestamp = now
                except:
                    pass
                try:
                    current_record_obj.confirmed=1
                except:
                    pass
                if auto_commit:
                    self.commit(**_process_call_area)
                record_dict = current_record_obj.to_dict()
                msg = f'OK. {_method_entity.upper()} Confirmed'
                api_result = {'api_status': 'success', 'api_message': msg, 'api_data': record_dict, 'api_action': _method_action.upper(), 'api_name':_method_name }
                log_process_result(_method_msgID, api_result, **_process_call_area)

            current_record_obj.status='Active'
            if auto_commit:
                self.commit(**_process_call_area)
            record_dict = current_record_obj.to_dict()
            msg = f'OK. {_method_entity.upper()} confirmed and activated'
            api_result = {'api_status': 'success', 'api_message': msg, 'api_data': record_dict, 'api_action': _method_action.upper(), 'api_name':_method_name }
            log_process_result(_method_msgID,api_result,**_process_call_area)
            return api_result
        else:#inquiry
            msg = f'OK. {_method_entity.upper()} retrieved'
            api_result = {'api_status': 'success', 'api_message': msg, 'api_data': record_dict, 'api_action': _method_action.upper(), 'api_name':_method_name }
            log_process_result(_method_msgID,api_result,**_process_call_area)
            return api_result
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    def build_query(self, table_model, kwargs):
        if type(kwargs)==type({}):
            query = self.session.query(table_model)
            #query_rows = query.count()
            #print(query_rows)
            for key in kwargs.keys():
                if key in table_model.__table__.columns.keys():
                    val = kwargs.get(key)
                    query = query.filter(getattr(table_model.__table__.columns, key) == val)
                    #query_rows = query.count()
                    #print(query_rows)
        elif type(kwargs) == type(''):
            select_sql=f"select * from {table_model.__tablename__} where {kwargs}"
            query = self.session.query(table_model).from_statement(text(select_sql)).params().all()
        else:
            return None
        #print(str(query))
        return query
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 
    def smart_locate_expression(self,table_model, locate_dict):
        from_primary_key={}
        from_unique_key={}
        from_other_fields = {}
        partial_pk = False
        for column in table_model.__table__.columns:
            if column.unique:
                if column.key in locate_dict:
                    val = locate_dict[column.key]
                    if not val == None:
                        from_unique_key = {column.key: val}
                        #return from_unique_key
            if column.primary_key:
                if column.key in locate_dict:
                    val = locate_dict[column.key]
                    if not val == None:
                        from_primary_key.update({column.key: val})
                else:
                    partial_pk = True
            if not column.unique:
                if column.key in locate_dict:
                    val = locate_dict[column.key]
                    if not val == None:
                        from_other_fields.update({column.key: val})
        if from_primary_key and not partial_pk:
            return from_primary_key
        elif from_unique_key:
            return from_unique_key
        elif from_other_fields:
            return from_other_fields
        return {}
        ########################################################################################
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 
    def smart_locate_expression2(self,table_model, locate_dict):
        from_primary_key={}
        from_unique_key={}
        from_other_fields = {}
        partial_pk = False
        for column in table_model.__table__.columns:
            if column.unique:
                if column.key in locate_dict:
                    val = locate_dict[column.key]
                    if not val == None:
                        from_unique_key = {column.key: val}
                        #return from_unique_key
            if column.primary_key:
                val = locate_dict.get(column.key)
                from_primary_key.update({column.key: val})
            if not column.unique:
                if column.key in locate_dict:
                    val = locate_dict[column.key]
                    if not val == None:
                        from_other_fields.update({column.key: val})
        if from_primary_key and not partial_pk:
            return from_primary_key
        elif from_unique_key:
            return from_unique_key
        elif from_other_fields:
            return from_other_fields
        return {}
        ########################################################################################
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 
    def get_table_row_as_dict(self, table_model, get_specification, caller_area={}, **kwargs):
        rowObj = self.get_table_row(table_model, get_specification, caller_area=caller_area, **kwargs)
        if not rowObj:
            return {}
        current_record_dict = table_model.to_dict(rowObj)
        return current_record_dict
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 
    def get_table_rows_as_dict(self, table_model, get_specification, caller_area={}, **kwargs):
        rowObjs = self.get_table_rows(table_model, get_specification, caller_area=caller_area, **kwargs)
        if not rowObjs:
            return []
        rows_array = self.rows_to_dict(table_model, rowObjs)
        return rows_array
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 
    def rows_to_dict(self, table_model, rowObjs, caller_area={}, **kwargs):
        if not rowObjs:
            return []
        rows_array=[]
        for rowObj in rowObjs:
            current_record_dict = table_model.to_dict(rowObj)
            rows_array.append(current_record_dict)
        return rows_array
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 
    def update_from_dict(self, model_record, **kwargs):
        """Update this model with a dictionary."""
        changes = {}
        readonly_columns = []
        autoset_columns=[]
        if hasattr(model_record, "_readonly_fields"):
            readonly_columns += model_record._readonly_fields
        if hasattr(model_record, "_hidden_fields"):
            readonly_columns += model_record._hidden_fields
        
        for c in model_record.__table__.columns:
            if c.key not in readonly_columns:
                if c.info:
                    if type(c.info) == type({}):
                        if c.info.get('is_readOnly'):
                            readonly_columns.append(c.key)
                        elif c.info.get('is_rowUID'):
                            val_old = getattr(model_record, c.key)
                            if val_old == None:
                                val_new = get_uuid(model_record.__table__,c.key)
                                setattr(model_record, c.key, val_new)
                                autoset_columns.append(c.key)
                                changes[c.key] = {"old_value": val_old, "new_value": val_new}
                        elif c.info.get('is_autoSetTimestamp'):
                            val_old = getattr(model_record, c.key)
                            if str(val_old).isnumeric():
                                val_new = datetime.datetime.utcnow()
                                setattr(model_record, c.key, val_new)
                                autoset_columns.append(c.key)
                                changes[c.key] = {"old_value": val_old, "new_value": val_new}
                        elif c.info.get('is_autoIncrementCounter'):
                            val_old = getattr(model_record, c.key)
                            if str(val_old).isnumeric():
                                val_new = int(val_old) + 1
                                setattr(model_record, c.key, val_new)
                                autoset_columns.append(c.key)
                                changes[c.key] = {"old_value": val_old, "new_value": val_new}
                        
        for key in kwargs:
            if key in model_record.__table__.columns.keys():
                if not key.startswith("_"):
                    if key not in readonly_columns and key not in autoset_columns:
                        val_old = getattr(model_record, key)
                        val_new = kwargs[key]
                        if str(val_old) != str(val_new):
                            changes[key] = {"old_value": val_old, "new_value": val_new}
                            setattr(model_record, key, val_new)
        # heading = f"[{model_record.__tablename__}] [[changes]]:"
        # print_changes(_method_msgID, changes,printLevel=_api_level)        
        return changes
    #::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
    #::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
    #::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
    def commit(self, **kwargs):
        session_debug_level = get_debug_option_as_level(self.debug)
        process_id = kwargs.get('msgID', '')
        caller_debug_level = get_debug_option_as_level(kwargs.get('debug_level'))
        kwargs.update({'debug_level':max(session_debug_level,caller_debug_level)})
        if not kwargs.get('indent_method'):
            kwargs.update({'indent_method':'CALL_LEVEL'})

        msg=f"[session] [[{self.session_id}]] [COMMIT]"
        if process_id:
            msg=msg+'#C0# in #C0#'+process_id

        self.session.commit()

        log_process_result_message('','session',msg,**kwargs)
    #::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
    def rollback(self, **kwargs):
        session_debug_level = get_debug_option_as_level(self.debug)
        process_id = kwargs.get('msgID', '')
        caller_debug_level = get_debug_option_as_level(kwargs.get('debug_level'))
        kwargs.update({'debug_level':max(session_debug_level,caller_debug_level)})
        if not kwargs.get('indent_method'):
            kwargs.update({'indent_method':'CALL_LEVEL'})

        msg=f"[session] [[{self.session_id}]] [ROLLBACK]"
        if process_id:
            msg=msg+'#C0# in #C0#'+process_id

        self.session.rollback()

        log_process_result_message('','session',msg,**kwargs)
    #::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
    def close(self, **kwargs):
        session_debug_level = get_debug_option_as_level(self.debug)
        process_id = kwargs.get('msgID', '')
        caller_debug_level = get_debug_option_as_level(kwargs.get('debug_level'))
        kwargs.update({'debug_level': max(session_debug_level, caller_debug_level)})
        if not kwargs.get('indent_method'):
            kwargs.update({'indent_method':'CALL_LEVEL'})
        
        msg=f"[session] [[{self.session_id}]] [CLOSE]"
        if process_id:
            msg=msg+'#C0# in #C0#'+process_id

        self.session.close()

        log_process_result_message('','session',msg,**kwargs)
    #::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
    def flush(self, **kwargs):
        session_debug_level = get_debug_option_as_level(self.debug)
        process_id = kwargs.get('msgID', '')
        caller_debug_level = get_debug_option_as_level(kwargs.get('debug_level'))
        kwargs.update({'debug_level':max(session_debug_level,caller_debug_level)})
        if not kwargs.get('indent_method'):
            kwargs.update({'indent_method':'CALL_LEVEL'})

        msg=f"[session] [[{self.session_id}]] [FLUSH]"
        if process_id:
            msg=msg+'#C0# in #C0#'+process_id

        self.session.flush()

        log_process_result_message('','session',msg,**kwargs)
    #::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
#::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
#::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
#::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
#::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
def set_msgID(api_name, api_action, api_table):
    msgid=f"table [{api_table.upper()}] #MAGENTA#{api_name}#C0#"
    return msgid
#::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
# def uniqueid():
#     seed = random.getrandbits(32)
#     seed=0
#     while True:
#        yield seed
#        seed += 1
def get_uuid(what='?',col='?'):
    #print('====',what)
    #x=str(next(unique_sequence))
    #x=what+' '+col+' '+str(mydefault())
    #x='|'+what+'|'+col+'|'+xguid(what,col)+'|'
    x=str(uuid.uuid1(uuid._random_getnode()))
    #return get_uuid()
    #print_message(f"[UUID-SET] [[[{x}]]] [{col}] [[{what}]]")
    return x

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
(print_enabled, filelog_enabled, log_file, errors_file,consolelog_enabled)=get_globals_from_configuration(master_configuration)
#::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
master_configuration = add_methods_to_configuration('database_actions', master_configuration, leandroutechnologyforward_database_session_class, ['ALL'], ['_init_'])
#::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
# methods == collect_method_names_from_class(leandroutechnologyforward_database_session_class, methods_ids=['ALL'])
# print(methods)
# exit(0)

# master_configuration = add_apis_to_configuration('database_actions', master_configuration, thisModuleObj, functions_ids, exclude_functions_ids)

#save_module_configuration(module_identityDictionary, master_configuration, print_enabled=consolelog_enabled, filelog_enabled=filelog_enabled)
thisApp.pair_module_configuration('database_actions',master_configuration)
#::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
if get_module_debug_level(module_id) > 0:
    actions = thisApp.application_configuration.get('database_actions', {})
    for action_name in actions.keys():
        action_entry = actions.get(action_name)
        msg=f'module [[{module_id}]] database action [{action_name} [[[{action_entry}]]]'
        log_message(msg)
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