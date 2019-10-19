# -*- coding: utf-8 -*-
import os
import sys
if not (os.path.dirname(__file__) in sys.path): sys.path.append(os.path.dirname(__file__))

from _onlineApp import print_message, print_result, colorized_message
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
class leandroutechnologyforward_database_table_class:
    name = None
    model = None
    model_base = None
    engine = None
    session = None
    debug = False
    debug_set_externally = False
    model_name = None
    table_name = None
    def __init__(self, model, model_base, schema, engine, session, debug=None, table_name=''):
        if not model:
            msg = f'model not provided for [[leandroutechnologyforward_database_table_class]]. STOPPED'
            msgP = colorized_message(msg,"#ERROR#")
            if debug: print_message(msgP,printLevel=1)
            exit(0)
        if not model_base:
            msg = f'model Base not provided for [[leandroutechnologyforward_database_table_class]]. STOPPED'
            msgP = colorized_message(msg,"#ERROR#")
            if debug: print_message(msgP,printLevel=1)
            exit(0)

        if not engine and not session:
            msg = f'engine or session not provided for [[leandroutechnologyforward_database_table_class]]. STOPPED'
            msgP = colorized_message(msg,"#ERROR#")
            if debug: print_message(msgP,printLevel=1)
            exit(0)
        self.model_base = model_base
        self.model = model
        self.table_name = self.model.__tablename__
        self.model_name = self.model.__name__
        if not table_name:
            table_name= self.model.__tablename__.upper()+'_TABLE'
        self.name = table_name
        if not engine:
            self.engine = self.session.bind.engine
        else:
            self.engine = engine
        if not session:
            Session = sessionmaker(bind=self.engine)
            session = Session()
        self.session = session

        self.debug = None
        if hasattr(self.model, "_debug"):
            self.debug = self.model._debug
        if not debug == None:
            self.debug = debug
        if self.debug == None:
            debug=False
            try:
                xdebug = thisApp.application_configuration.database_engine_debug
                if xdebug:
                    debug=thisApp.application_configuration.database_engine_debug
            except:
                pass
            try:
                xdebug = thisApp.application_configuration.database_debug
                if xdebug:
                    debug=thisApp.application_configuration.database_debug
            except:
                pass
            try:
                xdebug = thisApp.application_configuration.database_tables_debug
                if xdebug:
                    debug=thisApp.application_configuration.database_tables_debug
            except:
                pass
            try:
                xdebug = thisApp.application_configuration.database_models_debug
                if xdebug:
                    debug=thisApp.application_configuration.database_models_debug
            except:
                pass
        # #create the table if not exists
        # self.model.__table__.create(self.engine,checkfirst=True)
        
        # #synchronize_physical_table
        # self.synchronize_physical_table()
        
        # #check_table
        # self.check_table()
        
        #store in schema dictionary
        schema.update({self.name:self})        
    #::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
    #::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
    #::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
    # table functions
    # DB <--session--> sqlalchemy workspace
    #::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
    #::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
    #::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
    def get(self, access_key, output_method='',*kwargs):
        if output_method.upper().find('DICT') >= 0 or output_method.upper().find('JSON') >= 0:
            return self.get_row_as_dict(access_key)
        elif output_method.upper().find('HTML') >= 0:
            return self.get_row_as_html(access_key)
        else:
            return self.get_row(access_key)
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 
    def get_list(self, access_key, output_method='',*kwargs):
        if output_method.upper().find('DICT') >= 0 or output_method.upper().find('JSON') >= 0:
            return self.get_rows_as_dict(access_key)
        elif output_method.upper().find('HTML') >= 0:
            return self.get_rows_as_html(access_key)
        else:
            return self.get_rows(access_key)
    #::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
    #::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
    #::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
    def get_row(self, access_key):
        debug = self.debug
        msg0=f"[{self.model.__tablename__}] [[get_row]] :"
        filter_dict = self.smart_locate_expression(access_key)
        msg1=f"search filter:#CYAN#{filter_dict}#RESET#"
        query = self.build_query(filter_dict)
        if not query:
            msgx = f"#ERROR#query failed#RESET#"
            msgP = msg0 + " " + msgx + " " + msg1
            if debug: print_message(msgP,printLevel=1)
            return None
        query_rows = query.count()
        if not query_rows >= 1:
            msgx = f"#ERROR#NOT FOUND#RESET# query result rows:#RED#{query_rows}#RESET#"
            msgP = msg0 + " " + msgx + " " + msg1
            if debug: print_message(msgP,printLevel=1)
            return None
        current_record_obj = query.first()
        color = '#GREEN#'
        if query_rows > 1:
            color = '#RED#'
        msgx = f"query result rows:{color}{query_rows}#RESET#"
        msgP = msg0 + " " + msgx + " " + msg1
        if debug: print_message(msgP,printLevel=1)
        return current_record_obj
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 
    def get_row_as_dict(self, access_key):
        rowObj = self.get_row(access_key)
        if not rowObj:
            return {}
        current_record_dict = self.model.to_dict(rowObj)
        return current_record_dict
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 
    def get_row_as_html(self, access_key):
        rowObj = self.get_row(access_key)
        if not rowObj:
            return {}
        current_record_dict = self.model.to_dict(rowObj)
        return current_record_dict
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 
    def get_rows(self, access_key):
        debug = self.debug
        msg0=f"[{self.model.__tablename__}] [[get_rows]] :"
        filter_dict = self.smart_locate_expression(access_key)
        msg1=f"search filter:#CYAN#{filter_dict}#RESET#"
        query = self.build_query(filter_dict)
        if not query:
            msgx = f"#ERROR#query failed#RESET#"
            msgP = msg0 + " " + msgx + " " + msg1
            if debug: print_message(msgP,printLevel=1)
            return None
        query_rows = query.count()
        if not query_rows >= 1:
            msgx = f"#ERROR#NOT FOUND#RESET# query result rows:#RED#{query_rows}#RESET#"
            msgP = msg0 + " " + msgx + " " + msg1
            if debug: print_message(msgP,printLevel=1)
            return None
        current_record_objects = query.all()
        msgx = f"query result rows:#GREEN#{query_rows}#RESET#"
        msgP = msg0 + " " + msgx + " " + msg1
        if debug: print_message(msgP,printLevel=1)
        return current_record_objects
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 
    def get_rows_as_dict(self, access_key):
        rowObjs = self.get_rows(access_key)
        if not rowObjs:
            return []
        rows_array = self.rows_to_dict(rowObjs)
        return rows_array
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 
    def get_rows_as_html(self, access_key):
        rowObjs = self.get_rows(access_key)
        if not rowObjs:
            return []
        rows_array = self.rows_to_dict(rowObjs)
        return rows_array
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 
    def rows_to_dict(self, rowObjs):
        if not rowObjs:
            return []
        rows_array=[]
        for rowObj in rowObjs:
            current_record_dict = self.model.to_dict(rowObj)
            rows_array.append(current_record_dict)
        return rows_array
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 
    def insert(self, input_dict, commit=False):
        debug = self.debug
        _api_name='insert'
        _api_action='INSERT'
        msg0 = f"[{self.model.__tablename__}] [[insert]] :"
        action_status='error'
        # rows_added = 0
        # rows_updated = 0
        # messages = []
        current_record_obj = self.get_row(input_dict)

        if current_record_obj:
            msg = f'[{self.model_name}] already exists'
            action_status='error'
            current_record_dict = current_record_obj.to_dict()
            #api_result = {'api_status': action_status, 'api_message': msg, 'api_data': current_record_dict, 'messages': messages, 'rows_added': rows_added, 'rows_updated': rows_updated, 'api_action': _api_action.upper(), 'api_name': _api_name}
            msgP = msg0+" "+colorized_message(msg,"#"+action_status.upper()+"#")
            if debug: print_message(msgP,printLevel=1)
            return current_record_obj
        else:
            current_record_obj=self.model()
            valid_fields_dictionary = current_record_obj.valid_model_fields_dictionary(input_dict)
            (ok,messages) = self.input_validation(valid_fields_dictionary)
            if not ok:
                msg = f'input validation errors for model [{self.model_name}]'
                action_status='error'
                #api_result = {'api_status': action_status, 'api_message': msg, 'api_data': valid_fields_dictionary, 'messages': messages, 'rows_added': rows_added, 'rows_updated': rows_updated, 'api_action': _api_action.upper(), 'api_name': _api_name}
                msgP = msg0+" "+colorized_message(msg,"#"+action_status.upper()+"#")
                if debug: print_message(msgP,printLevel=1)
                return None

            current_record_obj.update_from_dict(printLevel=1, debug=debug, **valid_fields_dictionary)
            self.session.add(current_record_obj)
            if commit:
                self.session.commit()
                msg = f'OK. [{self.model_name}] committed'
                rows_added=1
            else:
                msg = f'OK. [{self.model_name}] ready for insert (not committed)'
            current_record_dict = current_record_obj.to_dict()
            action_status='success'
            #api_result = {'api_status': action_status, 'api_message': msg, 'api_data': current_record_dict, 'messages': messages, 'rows_added': rows_added, 'rows_updated': rows_updated, 'api_action': _api_action.upper(), 'api_name': _api_name}
            msgP = msg0+" "+colorized_message(msg,"#"+action_status.upper()+"#")
            if debug: print_message(msgP,printLevel=1)
            return current_record_obj
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 
    def update(self, input_dict, commit=False):
        debug = self.debug
        _api_name='update'
        _api_action='UPDATE'
        msg0 = f"[{self.model.__tablename__}] [[update]] :"
        action_status='error'
        rows_added = 0
        rows_updated = 0
        messages = []

        current_record_obj = self.get_row(input_dict)

        if not current_record_obj:
            msg = f'[{self.model_name}] not found'
            action_status = 'error'
            current_record_obj=self.model()
            valid_fields_dictionary = current_record_obj.valid_model_fields_dictionary(input_dict)
            #api_result = {'api_status': action_status, 'api_message': msg, 'api_data': valid_fields_dictionary, 'messages': messages, 'rows_added': rows_added, 'rows_updated': rows_updated, 'api_action': _api_action.upper(), 'api_name': _api_name}
            msgP = msg0+" "+colorized_message(msg,"#"+action_status.upper()+"#")
            if debug: print_message(msgP,printLevel=1)
            return None
        else:
            valid_fields_dictionary = current_record_obj.valid_model_fields_dictionary(input_dict)
            current_record_obj.update_from_dict(printLevel=1, debug=debug, **valid_fields_dictionary)
            if not current_record_obj.has_model_changed():
                msg = f"OK. [{self.model_name}] is synchronized. no changes applied"
                action_status='success'
                #api_result = {'api_status': action_status, 'api_message': msg, 'api_data': valid_fields_dictionary, 'messages': messages, 'rows_added': rows_added, 'rows_updated': rows_updated, 'api_action': _api_action.upper(), 'api_name': _api_name}
                msgP = msg0+" "+colorized_message(msg,"#"+action_status.upper()+"#")
                if debug: print_message(msgP,printLevel=1)
                return current_record_obj
            (ok,messages) = self.update_validation(valid_fields_dictionary)
            if not ok:
                msg=f'update validation errors for model [{self.model_name}]'
                action_status='error'
                #api_result = {'api_status': action_status, 'api_message': msg, 'api_data': valid_fields_dictionary, 'messages': messages, 'rows_added': rows_added, 'rows_updated': rows_updated, 'api_action': _api_action.upper(), 'api_name': _api_name}
                msgP = msg0+" "+colorized_message(msg,"#"+action_status.upper()+"#")
                if debug: print_message(msgP,printLevel=1)
                return None
            self.session.add(current_record_obj)
            if commit:
                self.session.commit()
                msg = f'OK. [{self.model_name}] updated'
                rows_updated=1
            else:
                rows_updated=0
                msg = f'OK. [{self.model_name}] ready for update'
            current_record_dict = current_record_obj.to_dict()
            action_status='success'
            #api_result = {'api_status': action_status, 'api_message': msg, 'api_data': current_record_dict, 'messages': messages, 'rows_added': rows_added, 'rows_updated': rows_updated, 'api_action': _api_action.upper(), 'api_name': _api_name}
            msgP = msg0+" "+colorized_message(msg,"#"+action_status.upper()+"#")
            if debug: print_message(msgP,printLevel=1)
            return current_record_obj
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 
    def remove(self, input_dict, commit=False):
        debug = self.debug
        _api_name='remove'
        _api_action='REMOVE'
        msg0 = f"[{self.model.__tablename__}] [[remove]] :"
        action_status='error'
        rows_removed = 0
        messages = []

        current_record_obj = self.get_row(input_dict)

        if not current_record_obj:
            msg = f'[{self.model_name}] not found'
            action_status = 'error'
            current_record_obj=self.model()
            valid_fields_dictionary = current_record_obj.valid_model_fields_dictionary(input_dict)
            #api_result = {'api_status': action_status, 'api_message': msg, 'api_data': valid_fields_dictionary, 'rows_removed': rows_removed, 'api_action': _api_action.upper(), 'api_name': _api_name}
            msgP = msg0+" "+colorized_message(msg,"#"+action_status.upper()+"#")
            if debug: print_message(msgP,printLevel=1)
            return None
        else:
            self.session.delete(current_record_obj)
            if commit:
                self.session.commit()
                msg = f'OK. [{self.model_name}] removed'
                rows_removed=1
            else:
                rows_removed=0
                msg = f'OK. [{self.model_name}] ready for remove (not committed)'
            current_record_dict = current_record_obj.to_dict()
            action_status='success'
            #api_result = {'api_status': action_status, 'api_message': msg, 'api_data': current_record_dict, 'messages': messages, 'rows_removed': rows_removed, 'api_action': _api_action.upper(), 'api_name': _api_name}
            msgP = msg0+" "+colorized_message(msg,"#"+action_status.upper()+"#")
            if debug: print_message(msgP,printLevel=1)
            return current_record_obj
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 
    def insert_or_update(self, input_dict, commit=False):
        debug = self.debug
        _api_name='insert_or_update'
        _api_action=''
        msg0 = f"[{self.model.__tablename__}] [[insert_or_update]] :"
        action_status='error'
        rows_added = 0
        rows_updated = 0
        messages = []

        current_record_obj = self.get_row(input_dict)

        if not current_record_obj:
            _api_action='ADD'
            current_record_obj=self.model()
            valid_fields_dictionary = current_record_obj.valid_model_fields_dictionary(input_dict)
            (ok,messages) = self.input_validation(valid_fields_dictionary)
            if not ok:
                msg = f'input validation errors for model [{self.model_name}]'
                action_status='error'
                #api_result = {'api_status': action_status, 'api_message': msg, 'api_data': valid_fields_dictionary, 'messages': messages, 'rows_added': rows_added, 'rows_updated': rows_updated, 'api_action': _api_action.upper(), 'api_name': _api_name}
                msgP = msg0+" "+colorized_message(msg,"#"+action_status.upper()+"#")
                if debug: print_message(msgP,printLevel=1)
                return None

            current_record_obj.update_from_dict(printLevel=1, debug=debug, **valid_fields_dictionary)
            self.session.add(current_record_obj)
            if commit:
                self.session.commit()
                msg = f'OK. [{self.model_name}] committed'
                rows_added=1
            else:
                msg = f'OK. [{self.model_name}] ready for addition (not committed)'
            current_record_dict = current_record_obj.to_dict()
            action_status='success'
            #api_result = {'api_status': action_status, 'api_message': msg, 'api_data': current_record_dict, 'messages': messages, 'rows_added': rows_added, 'rows_updated': rows_updated, 'api_action': _api_action.upper(), 'api_name': _api_name}
            msgP = msg0+" "+colorized_message(msg,"#"+action_status.upper()+"#")
            if debug: print_message(msgP,printLevel=1)
            return current_record_obj
        else:
            _api_action='UPDATE'
            valid_fields_dictionary = current_record_obj.valid_model_fields_dictionary(input_dict)
            current_record_obj.update_from_dict(printLevel=1, debug=debug, **valid_fields_dictionary)
            if not current_record_obj.has_model_changed():
                msg = f"OK. [{self.model_name}] is synchronized. no changes applied"
                action_status='success'
                #api_result = {'api_status': action_status, 'api_message': msg, 'api_data': valid_fields_dictionary, 'messages': messages, 'rows_added': rows_added, 'rows_updated': rows_updated, 'api_action': _api_action.upper(), 'api_name': _api_name}
                msgP = msg0+" "+colorized_message(msg,"#"+action_status.upper()+"#")
                if debug: print_message(msgP,printLevel=1)
                return current_record_obj
            (ok,messages) = self.update_validation(valid_fields_dictionary)
            if not ok:
                msg=f'update validation errors for model [{self.model_name}]'
                action_status='error'
                #api_result = {'api_status': action_status, 'api_message': msg, 'api_data': valid_fields_dictionary, 'messages': messages, 'rows_added': rows_added, 'rows_updated': rows_updated, 'api_action': _api_action.upper(), 'api_name': _api_name}
                msgP = msg0+" "+colorized_message(msg,"#"+action_status.upper()+"#")
                if debug: print_message(msgP,printLevel=1)
                return None
            self.session.add(current_record_obj)
            if commit:
                self.session.commit()
                msg = f'OK. [{self.model_name}] updated'
                rows_updated=1
            else:
                rows_updated=0
                msg = f'OK. [{self.model_name}] ready for update'
            current_record_dict = current_record_obj.to_dict()
            action_status='success'
            #api_result = {'api_status': action_status, 'api_message': msg, 'api_data': valid_fields_dictionary, 'messages': messages, 'rows_added': rows_added, 'rows_updated': rows_updated, 'api_action': _api_action.upper(), 'api_name': _api_name}
            msgP = msg0+" "+colorized_message(msg,"#"+action_status.upper()+"#")
            if debug: print_message(msgP,printLevel=1)
            return current_record_obj
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 
    def refresh(self, input_dict, commit=False):
        return self.insert_or_update(input_dict, commit=commit)
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 
    def update_rows(self, input_dict, filter_dict, commit=False):
        debug = self.debug
        _api_name='update_rows'
        _api_action='UPDATE_ROWS'
        msg0 = f"[{self.model.__tablename__}] [[update_rows]] :"
        action_status='error'
        row_count = 0
        rows_updated = 0
        messages = []
        errors = 0
        
        locate_dict = {**filter_dict} 
        update_rows = self.session.get_rows(locate_dict)
        row_count = len(update_rows)
        msg = f"OK. {row_count} rows retrieved"
        if len(update_rows) <= 0:
            msg = f"zero records found. No Update"
            action_status='error'
            #api_result = {'api_status': action_status, 'api_message': msg, 'api_data': [], 'messages': messages, 'rows_retrieved': row_count, 'rows_updated': rows_updated, 'api_action': _api_action.upper(), 'api_name': _api_name}
            msgP = msg0+" "+colorized_message(msg,"#"+action_status.upper()+"#")
            if debug: print_message(msgP,printLevel=1)
            return None

        for rowObj in update_rows:
            valid_fields_dictionary = rowObj.valid_model_fields_dictionary(input_dict)
            rowObj.update_from_dict(printLevel=1, debug=debug, **valid_fields_dictionary)
            if not rowObj.has_model_changed():
                rows_synchronized = rows_synchronized + 1
                rowuid = self.model.get_unique_identifier()
                msg = f"[{rowuid}] is synchronized. no changes applied"
                messages.append(msg)
                msgP = msg0+" "+colorized_message(msg,"#"+action_status.upper()+"#")
                if debug: print_message(msgP,printLevel=1)
                continue
            else:
                (ok,messages) = self.update_validation(valid_fields_dictionary)
                if not ok:
                    errors = errors + 1
                    rowuid = self.model.get_unique_identifier()
                    msg = f"[{self.model_name}] [[{rowuid}]] with validation errors. update skipped"
                    messages.append(msg)
                    action_status='error'
                    msgP = msg0+" "+colorized_message(msg,"#"+action_status.upper()+"#")
                    if debug: print_message(msgP,printLevel=1)
                    continue
            rowObj.update_from_dict(printLevel=1, debug=debug, **valid_fields_dictionary)
            rows_updated = rows_updated + 1
        if errors > 0:
            action_status='error'
            msg = f'errors encountered during update. on {errors} row(s)'
            #api_result = {'api_status': action_status, 'api_message': msg, 'api_data': [], 'messages': messages, 'rows_retrieved': row_count, 'rows_updated': rows_updated, 'rows_with_errors': errors, 'api_action': _api_action.upper(), 'api_name': _api_name}
            msgP = msg0+" "+colorized_message(msg,"#"+action_status.upper()+"#")
            if debug: print_message(msgP,printLevel=1)
            return None

        action_status='success'
        if rows_updated > 0:
            if commit:
                self.session.commit()
                msg = f'OK. {rows_updated} [{self.model_name}] rows updated'
            else:
                msg = f'OK.  {rows_updated} [{self.model_name}] rows updated (not committed)'

        updated_rows_dict = self.rows_to_dict(update_rows)
        api_result = {'api_status': action_status, 'api_message': msg, 'api_data':updated_rows_dict, 'messages': messages, 'rows_retrieved': row_count, 'rows_updated': rows_updated, 'api_action': _api_action.upper(), 'api_name': _api_name}
        msgP = msg0+" "+colorized_message(msg,"#"+action_status.upper()+"#")
        if debug: print_message(msgP,printLevel=1)
        return api_result
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 
    def input_validation(self, input_dict):
        debug = self.debug
        msg0 = f"[{self.model.__tablename__}] [[input_validation]] :"
        current_record_obj=self.model()
        valid_fields_dictionary = current_record_obj.valid_model_fields_dictionary(input_dict)
        current_record_obj.update_from_dict(printLevel=1, debug=debug, **valid_fields_dictionary)
        (ok,messages) = current_record_obj.input_validation(valid_fields_dictionary)
        if not ok:
            msg = f'input validation errors for model [{self.model_name}]'
            msgC = colorized_message(msg,"#ERROR#")
        else:
            msg = f'OK. input validation passed for model [{self.model_name}]'
            msgC = colorized_message(msg,"#SUCCESS#")
        msgP = f"{msg0} {msgC}. OK=[{ok}] messages=[[{messages}]]"
        if debug: print_message(msgP,printLevel=1)
        return (ok, messages)
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 
    def update_validation(self, input_dict):
        debug = self.debug
        msg0 = f"[{self.model.__tablename__}] [[update_validation]] :"
        current_record_obj=self.model()
        valid_fields_dictionary = current_record_obj.valid_model_fields_dictionary(input_dict)
        current_record_obj.update_from_dict(printLevel=1, debug=debug, **valid_fields_dictionary)
        (ok,messages) = current_record_obj.update_validation(valid_fields_dictionary)
        if not ok:
            msg = f'update validation errors for model [{self.model_name}]'
            msgC = colorized_message(msg,"#ERROR#")
        else:
            msg = f'OK. update validation passed for model [{self.model_name}]'
            msgC = colorized_message(msg,"#SUCCESS#")
        msgP = f"{msg0} {msgC}. OK=[{ok}] messages=[[{messages}]]"
        if debug: print_message(msgP,printLevel=1)
        return (ok, messages)
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 
    def build_query(self, kwargs):
        if type(kwargs)==type({}):
            query = self.session.query(self.model)
            #query_rows = query.count()
            #print(query_rows)
            for key in kwargs.keys():
                if key in self.model.__table__.columns.keys():
                    val = kwargs.get(key)
                    query = query.filter(getattr(self.model.__table__.columns, key) == val)
                    #query_rows = query.count()
                    #print(query_rows)
        elif type(kwargs) == type(''):
            select_sql=f"select * from {self.model.__tablename__} where {kwargs}"
            query = self.session.query(self.model).from_statement(text(select_sql)).params().all()
        else:
            return None
        #print(str(query))
        return query
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 
    def smart_locate_expression(self,locate_dict):
        from_primary_key={}
        from_other_fields = {}
        partial_pk = False
        for column in self.model.__table__.columns:
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
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 
#::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
#::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
#::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
# admin functions
#::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
#::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
#::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
    def rowCount(self, filter_dict={}):
        # query = self.build_query(filter_dict)
        # self.table_rows = query.count()
        self.table_rows = self.engine.execute(f"select count(*) from {self.model.__tablename__}").scalar()
        # table_object = self.model.__table__ #database_metadata.tables.get("table_name")
        # query = table_object.count()
        # self.table_rows = self.engine.scalar(query)
        return self.table_rows
#::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
    def delete_rows(self, filter_dict={}, commit=True):
        debug = self.debug
        _api_name = 'delete_rows'
        _api_action = 'DELETE'
        msg0 = f"[{self.model.__tablename__}] [[delete_rows]] :"
        action_status='error'
        rows_deleted = 0        
        #messages = []

        filter_dict = self.smart_locate_expression(filter_dict)
        msg1=f"filter:#CYAN#{filter_dict}#RESET#"
        query = self.build_query(filter_dict)
        if not query:
            msgx = f"#ERROR#query failed#RESET#"
            msgP = msg0 + " " + msgx + " " + msg1
            if debug: print_message(msgP,printLevel=1)
            return None
        query_rows = query.count()
        # current_record_objects = query.all()
        msgx = f"query result rows:#GREEN#{query_rows}#RESET#"
        if query_rows <= 0:
            msg = f'zero rows to delete'
        else:
            query.delete()
            if commit:
                self.session.commit()
                msg = f'OK. [{query_rows}] deleted'
                rows_deleted=query_rows
            else:
                msg = f'OK. [{query_rows}] deleted (not committed)'

            action_status='success'
            api_result = {'api_status': action_status, 'api_message': msg, 'api_data': {},  'rows_deleted': rows_deleted, 'api_action':_api_action.upper(), 'api_name': _api_name}
            msgP = msg0+" "+colorized_message(msg,"#"+action_status.upper()+"#")
            if debug: print_message(msgP,printLevel=1)
            return api_result
#::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
    def set_debug(self, debug=True):
        self.debug = debug
        self.debug_set_externally=True
#::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::        
    def set_debug_on(self):
        self.debug = True
        self.debug_set_externally=True
#::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::        
    def set_debug_off(self):
        self.debug = False
        self.debug_set_externally=True
#::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::        
    def set_debug_default(self):
        self.debug_set_externally=False
#::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::        
    def debug_is_on(self):
        if self.debug_set_externally:
            return self.debug
        debug=self.debug
        return debug
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