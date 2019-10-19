# -*- coding: utf-8 -*-
import os
import sys
if not (os.path.dirname(__file__) in sys.path): sys.path.append(os.path.dirname(__file__))

from _onlineApp import print_message, print_result
from _onlineApp import log_process_start, log_process_finish, log_process_input, log_process_output, log_process_message
from colorama import Fore as colors
from sqlalchemy.orm import sessionmaker
from sqlalchemy.sql import text
from sqlalchemy.engine import ddl
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
    def __init__(self, engine, session=None, schema_dictionary={},debug=True):
        self.engine = engine
        if not session:
            Session = sessionmaker(bind=self.engine)
            session = Session()
        self.session = session
        self.schema = schema_dictionary
        thisApp.application_configuration.database_engine_debug = debug
    #::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
    #::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
    #::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
    # session support functions
    #   form DB --> sqlalchemy workspace
    #::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
    #::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
    #::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
    def get_table_row(self, table_model, access_key):
        msg0=f"[{table_model.__tablename__}] [[get_table_row]] :"
        filter_dict = self.smart_locate_expression(table_model, access_key)
        msg1=f"search filter:#CYAN#{filter_dict}#RESET#"
        query = self.build_query(table_model, filter_dict)
        if not query:
            msgx = f"#ERROR#query failed#RESET#"
            msg = msg0 + " " + msgx + " " + msg1
            if thisApp.application_configuration.database_engine_debug: print_message(msg,printLevel=1)
            return None
        
        query_rows = query.count()
        str(query.count())
        if not query_rows >= 1:
            msgx = f"#ERROR#NOT FOUND#RESET# query result rows:#RED#{query_rows}#RESET#"
            msg = msg0 + " " + msgx + " " + msg1
            if thisApp.application_configuration.database_engine_debug: print_message(msg,printLevel=1)
            return None
        current_record_obj = query.first()
        color = '#GREEN#'
        if query_rows > 1:
            color = '#RED#'
        msgx = f"query result rows:{color}{query_rows}#RESET#"
        msg = msg0 + " " + msgx + " " + msg1
        if current_record_obj.debug_is_on() or thisApp.application_configuration.database_engine_debug: print_message(msg,printLevel=1)
        return current_record_obj
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 
    def get_table_rows(self, table_model, access_key):
        msg0=f"[{table_model.__tablename__}] [[get_table_rows]] :"
        filter_dict = self.smart_locate_expression(table_model, access_key)
        msg1=f"search filter:#CYAN#{filter_dict}#RESET#"
        query = self.build_query(table_model, filter_dict)
        if not query:
            msgx = f"#ERROR#query failed#RESET#"
            msg = msg0 + " " + msgx + " " + msg1
            if thisApp.application_configuration.database_engine_debug: print_message(msg,printLevel=1)
            return None
        query_rows = query.count()
        if not query_rows >= 1:
            msgx = f"#ERROR#NOT FOUND#RESET# query result rows:#RED#{query_rows}#RESET#"
            msg = msg0 + " " + msgx + " " + msg1
            if thisApp.application_configuration.database_engine_debug: print_message(msg,printLevel=1)
            return None
        current_record_objects = query.all()
        msgx = f"query result rows:#GREEN#{query_rows}#RESET#"
        msg = msg0 + " " + msgx + " " + msg1
        if thisApp.application_configuration.database_engine_debug: print_message(msg,printLevel=1)
        return current_record_objects
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 
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
        from_other_fields = {}
        partial_pk = False
        for column in table_model.__table__.columns:
            if column.unique:
                if column.key in locate_dict:
                    val = locate_dict[column.key]
                    if val:
                        from_unique_key = {column.key: val}
                        return from_unique_key
            elif column.primary_key:
                if column.key in locate_dict:
                    val = locate_dict[column.key]
                    if val:
                        from_primary_key.update({column.key: val})
                else:
                    partial_pk = True
            if 1==1 and not column.unique:
                if column.key in locate_dict:
                    val = locate_dict[column.key]
                    if val:
                        from_other_fields.update({column.key: val})
        if from_primary_key and not partial_pk:
            return from_primary_key
        if from_other_fields:
            return from_other_fields
        return {}
        ########################################################################################
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 
    def get_table_row_as_dict(self, table_model, access_key):
        rowObj = self.get_table_row(table_model, access_key)
        if not rowObj:
            return {}
        current_record_dict = table_model.to_dict(rowObj)
        return current_record_dict
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 
    def get_table_rows_as_dict(self, table_model, access_key):
        rowObjs = self.get_table_rows(table_model, access_key)
        if not rowObjs:
            return []
        rows_array = self.rows_to_dict(table_model, rowObjs)
        return rows_array
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 
    def rows_to_dict(self, table_model, rowObjs):
        if not rowObjs:
            return []
        rows_array=[]
        for rowObj in rowObjs:
            current_record_dict = table_model.to_dict(rowObj)
            rows_array.append(current_record_dict)
        return rows_array
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 
    def insert_or_update(self, table_model, input_dict,commit=False):
        _api_name='insert_or_update'
        msg0=f"[{table_model.__tablename__}] [[insert_or_update]] :"
        filter_dict = self.smart_locate_expression(table_model, input_dict)
        msg1=f"search filter:#CYAN#{filter_dict}#RESET#"
        query = self.build_query(table_model, filter_dict)
        if not query:
            msgx = f"#ERROR#query failed#RESET#"
            msg = msg0 + " " + msgx + " " + msg1
            if thisApp.application_configuration.database_engine_debug: print_message(msg,printLevel=1)
            return None
        query_rows = query.count()
        if not query_rows >= 1:
            msgx = f"#ERROR#NOT FOUND#RESET# query result rows:#RED#{query_rows}#RESET#"
            msg = msg0 + " " + msgx + " " + msg1
            if thisApp.application_configuration.database_engine_debug: print_message(msg,printLevel=1)
            current_record_obj = None
        else:
            current_record_obj = query.first()
            color = '#GREEN#'
            if query_rows > 1:
                color = '#RED#'
            msgx = f"query result rows:{color}{query_rows}#RESET#"
            msg = msg0 + " " + msgx + " " + msg1
            if current_record_obj.debug_is_on() or thisApp.application_configuration.database_engine_debug: print_message(msg,printLevel=1)

        if not current_record_obj:
            _api_action='ADD'
            current_record_obj=table_model()
            valid_fields_dictionary = current_record_obj.valid_model_fields_dictionary(input_dict)
            current_record_obj.update_from_dict(**valid_fields_dictionary)
            (ok,messages) = current_record_obj.input_validation(valid_fields_dictionary)
            if not ok:
                msg=f'input validation errors'
                api_result = {'api_status': 'error', 'api_message': msg, 'api_data': valid_fields_dictionary, 'messages':messages, 'rows_added':0, 'api_action': _api_action.upper(), 'api_name':_api_name }
                if thisApp.application_configuration.database_engine_debug: print_result(f"{msg0} result:", api_result, printLevel=1)
                return None
            self.session.add(current_record_obj)
            if commit:
                self.session.commit()
                msg = f'OK. {table_model.__name__.upper()} added'
                rows_added=1
            else:
                rows_added=0
                msg = f'OK. {table_model.__name__.upper()} ready for addition'
            current_record_dict = current_record_obj.to_dict()
            api_result = {'api_status': 'success', 'api_message': msg, 'api_data': current_record_dict, 'rows_added':rows_added,'rows_updated':0, 'api_action': _api_action.upper(), 'api_name': _api_name}
            if thisApp.application_configuration.database_engine_debug: print_result(f"{msg0} result:", api_result, printLevel=1)
            return current_record_obj
        else:
            _api_action='UPDATE'
            valid_fields_dictionary = current_record_obj.valid_model_fields_dictionary(input_dict)
            current_record_obj.update_from_dict(**valid_fields_dictionary)
            if not current_record_obj.has_model_changed():
                msg=f"OK. {table_model.__name__.upper()} is synchronized. no changes applied"
                api_result = {'api_status': 'success', 'api_message': msg, 'api_data': valid_fields_dictionary, 'rows_added':0,'rows_updated':0, 'api_action': _api_action.upper(), 'api_name':_api_name }
                if thisApp.application_configuration.database_engine_debug: print_result(f"{msg0} result:", api_result, printLevel=1)
                return current_record_obj
            (ok,messages) = current_record_obj.update_validation(valid_fields_dictionary)
            if not ok:
                msg=f'update validation errors'
                api_result = {'api_status': 'error', 'api_message': msg, 'api_data': api_record, 'messages':messages, 'rows_updated':0, 'api_action': _api_action.upper(), 'api_name':_api_name }
                if thisApp.application_configuration.database_engine_debug: print_result(f"{msg0} result:", api_result, printLevel=1)
                return None
            self.session.add(current_record_obj)
            if commit:
                self.session.commit()
                msg = f'OK. {table_model.__name__.upper()} updated'
                rows_updated=1
            else:
                rows_updated=0
                msg = f'OK. {table_model.__name__.upper()} ready for update'
            current_record_dict = current_record_obj.to_dict()
            api_result = {'api_status': 'success', 'api_message': msg, 'api_data': current_record_dict, 'rows_added':0,'rows_updated':rows_updated, 'api_action': _api_action.upper(), 'api_name': _api_name}
            if thisApp.application_configuration.database_engine_debug: print_result(f"{msg0} result:", api_result, printLevel=1)
            return current_record_obj
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 
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