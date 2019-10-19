# -*- coding: utf-8 -*-
import os
import sys
import datetime
from datetime import timedelta
import time
import configparser
import json
import decimal
# import inspect
import copy
import subprocess
from inspect import getmembers, isfunction
from colorama import Fore as colors
import uuid
from pprint import pprint

from sqlalchemy import Column, inspect
from sqlalchemy.sql import text
from sqlalchemy.engine import ddl
from _onlineApp import _appEnvironment as thisApp
from _onlineApp._logServices import log_message
# from ._moduleConfigServices import retrieve_module_configuration
# from ._tokenServices import generate_token
# from ._secretServices import token_urlsafe,token_hex
# from ._encodingServices import ascii_char
# from ._database_modeling_services import generate_table_model, compare_table_model_with_table_structure,select_expression_from_values,bobbi_starr
# from ._database_classes_utilities import import_reorganization_functions, table_reorganization
# from ._database_layer1_services import get_table_structure, make_a_table_copy, create_table, recreate_table
# from ._database_layer1_services import copy_table_records, drop_table, get_table_rowsCount, data_type_is_numeric
# from ._database_layer1_services import table_exists as table_exists_in_database
#::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
# import sqlalchemy as db

# from sqlalchemy import String, Integer, Float, BigInteger, DateTime

# from sqlalchemy.schema import DropTable, CreateTable
# from sqlalchemy.orm import scoped_session, sessionmaker
# #from sqlalchemy import create_engine
# from sqlalchemy.pool import SingletonThreadPool
# from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy import (create_engine, MetaData, Table, Column,
                        Integer, Numeric, String, Date, DateTime, text)
from sqlalchemy.ext.compiler import compiles
from sqlalchemy.schema import (CreateTable, AddConstraint, CreateIndex,
                               DropTable, DropConstraint, DropIndex,
                               ForeignKeyConstraint, CheckConstraint,
                               UniqueConstraint, PrimaryKeyConstraint)
# from sqlalchemy import Column, Table,CreateTable
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import MetaData
# meta = MetaData()
#::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
#::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
#::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
# globals
#::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
#::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
#::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
debug = False
#::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
#::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
#::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
#::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
# services 
#::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
#::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
#::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
class leandroutechnologyforward_database_table_class:
    objclass='table'
    name = ''
    db_engine = None
    db_connection = None
    dbConnectionObj = None
    dbms=None
    schema = None
    
    table = None
    #-----------------
    model = None
    query = None
    query_rows = 0
    current_record_obj = None
    current_record_dict = {}
    records_obj = None
    records_dict = []
    last_changes={}
    unmapped_columns = 0
    new_columns = 0
    changed_columns = 0
    #-----------------
    dialect=''
    database_schema = {}
    schema_id = ''
    schema_name = ''
    version = ''
    table_name = ''
    table_alias = ''
    table_entity = ''
    table_reference = f"{schema_name}.{table_name.upper()}"
    reference =""
    table_model = {}
    reorganization_minutes=1
    reorganization_functions = []
    last_reorganizationDT = datetime.datetime.utcnow()
    next_reorganizationDT = last_reorganizationDT
 #   color = thisApp.Fore.LIGHTBLUE_EX
    parent_module=None
    parent_module_name = ''
    user = ''
    password = ''
    time_start = None
    time_end = None
    duration = None
    debug_level = 0
    #------------------------------------#
    after_update_commands = []
    rowid_column = ''
    columns = {}
    primary_key_columns = []
    unique_value_columns = []
    mandatory_columns = []
    after_insert_sqlCommands = []
    unique_key_validations = []
    create_table_commands = []
    record_locate_expression = ''
    record_locate_expression_from_rowid = ''
    row_descriptor_expression = ''
    row_descriptor_expression2 = ''
    ordered_columns_list = []
    table_structure_changed = True
    table_structure_is_synchronized = False
    table_structure_dictionary = {}
    #-----------------------------------#
    def __init__(self, db_schema, db_session, table_model, table_alias, table_entity):
        self.db_session = db_session
        self.session = db_session.session
        self.model = table_model
        if table_alias:
            self.table_alias=table_alias
        else:
            self.table_alias = self.model.__tablename__
        if table_entity:
            self.table_alias=table_entity
        else:
            table_entity = self.table_alias
            if table_entity[-1].upper() == 'S':
                table_entity=table_entity[0:-1]
            self.table_entity = table_entity
        #create the table if not exists
        self.model.__table__.create(self.session.bind.engine,checkfirst=True)
        #synchronize_physical_table
        self.synchronize_physical_table()
        #check_table
        self.check_table()
        #store in schema dictionary
        db_schema.update({table_alias:self})
    #::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
    #::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
    #::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
    # dict support functions
    #::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
    #::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
    #::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
    def valid_fields_dictionary(self, kwargs):
        valid_model_record={}
        columns = self.model.__table__.columns.keys()
        for key in kwargs:
            if key in columns:
                if not key.startswith("_"):
                    val = kwargs[key]
                    #shalimar
                    # if str(self.model.__table__.columns[key].type.python_type).upper().find('UUID')>0:
                    #     val=str(val)
                    valid_model_record.update({key:kwargs[key]})
        return valid_model_record
    ##############################################
    def xto_dict(self, show=None, _hide=[], _path=None):
        """Return a dictionary representation of this model."""
        show = show or []

        hidden = self._hidden_fields if hasattr(self, "_hidden_fields") else []
        default = self._default_fields if hasattr(self, "_default_fields") else self.__table__.columns.keys()
        # default.extend(['id', 'modified_at', 'created_at'])

        if not _path:
            _path = self.__tablename__.lower()

            def prepend_path(item):
                item = item.lower()
                if item.split(".", 1)[0] == _path:
                    return item
                if len(item) == 0:
                    return item
                if item[0] != ".":
                    item = ".%s" % item
                item = "%s%s" % (_path, item)
                return item

            _hide[:] = [prepend_path(x) for x in _hide]
            show[:] = [prepend_path(x) for x in show]

        columns = self.__table__.columns.keys()
        relationships = self.__mapper__.relationships.keys()
        properties = dir(self)

        ret_data = {}

        for key in columns:
            if key.startswith("_"):
                continue
            check = "%s.%s" % (_path, key)
            if check in _hide or key in hidden:
                continue
            if check in show or key in default:
                ret_data[key] = getattr(self, key)

        for key in relationships:
            if key.startswith("_"):
                continue
            check = "%s.%s" % (_path, key)
            if check in _hide or key in hidden:
                continue
            if check in show or key in default:
                _hide.append(check)
                is_list = self.__mapper__.relationships[key].uselist
                if is_list:
                    items = getattr(self, key)
                    if self.__mapper__.relationships[key].query_class is not None:
                        if hasattr(items, "all"):
                            items = items.all()
                    ret_data[key] = []
                    for item in items:
                        ret_data[key].append(
                            item.to_dict(
                                show=list(show),
                                _hide=list(_hide),
                                _path=("%s.%s" % (_path, key.lower())),
                            )
                        )
                else:
                    if (
                        self.__mapper__.relationships[key].query_class is not None
                        or self.__mapper__.relationships[key].instrument_class
                        is not None
                    ):
                        item = getattr(self, key)
                        if item is not None:
                            ret_data[key] = item.to_dict(
                                show=list(show),
                                _hide=list(_hide),
                                _path=("%s.%s" % (_path, key.lower())),
                            )
                        else:
                            ret_data[key] = None
                    else:
                        ret_data[key] = getattr(self, key)

        for key in list(set(properties) - set(columns) - set(relationships)):
            if key.startswith("_"):
                continue
            if not hasattr(self.__class__, key):
                continue
            attr = getattr(self.__class__, key)
            if not (isinstance(attr, property) or isinstance(attr, QueryableAttribute)):
                continue
            check = "%s.%s" % (_path, key)
            if check in _hide or key in hidden:
                continue
            if check in show or key in default:
                val = getattr(self, key)
                if hasattr(val, "to_dict"):
                    ret_data[key] = val.to_dict(
                        show=list(show),
                        _hide=list(_hide),
                        #_path=("%s.%s" % (_path, key.lower()))
                        #_path=('%s.%s' % (path, key.lower())),
                        _path=(f'{_path}.{key.lower()}'),
                    )
                else:
                    try:
                        ret_data[key] = json.loads(json.dumps(val))
                    except:
                        pass

        return ret_data
    ########################################################################################
    def update_model_from_dict(self, **kwargs):
        """Update this model with a dictionary."""
        changes = {}
        _force = kwargs.pop("_force", False)
        readonly=[]
        if hasattr(self.model, "_readonly_fields"):
            readonly += self.model._readonly_fields
        if hasattr(self.model, "_hidden_fields"):
            readonly += self.model._hidden_fields
        columns = self.model.__table__.columns.keys()
        for key in kwargs:
            if key in columns:
                if not key.startswith("_"):
                    if _force or key not in readonly:
                        val_old = getattr(self.model, key)
                        val_new = kwargs[key]
                        if val_old != val_new:
                            changes[key] = {"old_value": val_old, "new_value": val_new}
                            setattr(self.model, key, val_new)
                            print(key,'=',self.model.last_usage_timestamp)
                            print(key,'=',self.current_record_obj.last_usage_timestamp)
                            setattr(self.current_record_obj, key, val_new)
                            print(key,'=',self.model.last_usage_timestamp)
                            print(key,'=',self.current_record_obj.last_usage_timestamp)
        self.last_changes = changes
    ########################################################################################
    ##############################################
    def convert_model_to_dict(self, show=None, _hide=[]):
        """Return a dictionary representation of this model."""
        # show = show or []
        # hidden=[]
        # if hasattr(self.model, "_hidden_fields"):
        #     hidden = self.model._hidden_fields
        # if hasattr(self.model, "_default_fields"):
        #     default = self.model._default_fields
        # else:
        #     default = self.model.__table__.columns.keys()
        # # default.extend(['id', 'modified_at', 'created_at'])
        # _path = self.model.__tablename__.lower()
        # def prepend_path(item):
        #         item = item.lower()
        #         if item.split(".", 1)[0] == _path:
        #             return item
        #         if len(item) == 0:
        #             return item
        #         if item[0] != ".":
        #             item = f".{item}"
        #         item = f"{_path}{item}"
        #         return item

        # _hide[:] = [prepend_path(x) for x in _hide]
        # show[:] = [prepend_path(x) for x in show]
        columns = self.model.__table__.columns.keys()
        # relationships = self.model.__mapper__.relationships.keys()
        # properties = dir(self.model)
        record_dict = {}
        for key in columns:
            record_dict[key] = getattr(self.model, key)
        # for key in relationships:
        #     if key.startswith("_"):
        #         continue
        #     check = "%s.%s" % (_path, key)
        #     if check in _hide or key in hidden:
        #         continue
        #     if check in show or key in default:
        #         _hide.append(check)
        #         is_list = self.model.__mapper__.relationships[key].uselist
        #         if is_list:
        #             items = getattr(self.model, key)
        #             if self.model.__mapper__.relationships[key].query_class is not None:
        #                 if hasattr(items, "all"):
        #                     items = items.all()
        #             record_dict[key] = []
        #             for item in items:
        #                 record_dict[key].append(
        #                     item.to_dict(
        #                         show=list(show),
        #                         _hide=list(_hide),
        #                         _path=("%s.%s" % (_path, key.lower())),
        #                     )
        #                 )
        #         else:
        #             if (
        #                 self.model.__mapper__.relationships[key].query_class is not None
        #                 or self.model.__mapper__.relationships[key].instrument_class is not None
        #             ):
        #                 item = getattr(self.model, key)
        #                 if item is not None:
        #                     record_dict[key] = item.to_dict(
        #                         show=list(show),
        #                         _hide=list(_hide),
        #                         _path=("%s.%s" % (_path, key.lower())),
        #                     )
        #                 else:
        #                     record_dict[key] = None
        #             else:
        #                 record_dict[key] = getattr(self.model, key)

        # for key in list(set(properties) - set(columns) - set(relationships)):
        #     if key.startswith("_"):
        #         continue
        #     if not hasattr(self.model.__class__, key):
        #         continue
        #     attr = getattr(self.model.__class__, key)
        #     if not (isinstance(attr, property) or isinstance(attr, QueryableAttribute)):
        #         continue
        #     check = "%s.%s" % (_path, key)
        #     if check in _hide or key in hidden:
        #         continue
        #     if check in show or key in default:
        #         val = getattr(self, key)
        #         if hasattr(val, "to_dict"):
        #             record_dict[key] = val.to_dict(
        #                 show=list(show),
        #                 _hide=list(_hide),
        #                 #_path=("%s.%s" % (_path, key.lower()))
        #                 #_path=('%s.%s' % (path, key.lower())),
        #                 _path=(f'{_path}.{key.lower()}'),
        #             )
        #         else:
        #             try:
        #                 record_dict[key] = json.loads(json.dumps(val))
        #             except:
        #                 pass

        return record_dict
    ########################################################################################
    def to_dict(self, row, method=''):
        if not row:
            return {}
        row_dict={}
        if hasattr(self.model, "_hidden_fields"):
            hidden_fields = self.model._hidden_fields
        else:
            hidden_fields=[]
        for column in row.__table__.columns:
            key=column.key
            row_dict[column.name] = str(getattr(row, column.name))
        # columns = self.model.columns.keys()
        # for key in columns:
            if not key.startswith("_"):
                if key not in hidden_fields:
                    # val_old = getattr(self, key)
                    # if str(column.type.python_type).upper().find('UUID') > 0:
                    #     #shalimar
                    #     # row_dict[column.name] = str(getattr(row, column.name))
                    #     row_dict[column.name] = getattr(row, column.name)
                    if method.upper().find('TEXT') >= 0 or method.upper().find('STRING') >= 0:
                        row_dict[column.name] = str(getattr(row, column.name))
                    else:
                        row_dict[column.name] = getattr(row, column.name)
        return row_dict
    ########################################################################################
    def rows_to_dict(self, rows, method=''):
        rows_array=[]
        for row in rows:
            rows_array.append(self.to_dict(row, method))
        return rows_array
    ########################################################################################
    def smart_locate_expression(self, kwargs):
        from_primary_key={}
        from_other_fields = {}
        partial_pk = False
        for column in self.model.__table__.columns:
            if column.unique:
                if column.key in kwargs:
                    val = kwargs[column.key]
                    if val:
                        from_unique_key = {column.key: val}
                        return from_unique_key
            elif column.primary_key:
                if column.key in kwargs:
                    val = kwargs[column.key]
                    if val:
                        from_primary_key.update({column.key: val})
                else:
                    partial_pk = True
            if 1==1 and not column.unique:
                if column.key in kwargs:
                    val = kwargs[column.key]
                    if val:
                        from_other_fields.update({column.key: val})
        if from_primary_key and not partial_pk:
            return from_primary_key
        if from_other_fields:
           return from_other_fields
        return {}
    ########################################################################################
    def locate_expression_dict(self, kwargs):
        locate_dict={}
        if type(kwargs) == type({}):
            columns = self.model.__table__.columns.keys()
            for key in kwargs: 
                if key in columns:
                    val = kwargs[key]
                    locate_dict.update({key: val})
        else:
            if type(kwargs) == type(''):
                kwargs = kwargs.split(',')
        if type(kwargs) == type([]):
            primary_keys = self.model.__mapper__.primary_key
            ix = -1
            if len(primary_keys) > 0:
                for primary_key in primary_keys:
                    ix = ix + 1
                    if ix + 1 <= len(kwargs):
                        val = kwargs[ix]
                        locate_dict.update({primary_key.key:val})
            else:
                ix = -1
                columns = self.model.__table__.columns.keys()
                for key in columns:
                    if key.startswith("_"):
                        continue
                    ix = ix + 1
                    if ix + 1 <= len(kwargs):
                        val = kwargs[ix]
                        locate_dict.update({key:val})
        self.last_query_dict = locate_dict
        return self.last_query_dict
    ########################################################################################
    # def xquery_from_dict(self,kwargs):
    #     # assuming a model class, User, with attributes, name_last, name_first
    #     # my_filters = {'name_last':'Duncan', 'name_first':'Iain'}
    #     # query = session.query(User)
    #     # for attr,value in my_filters.iteritems():
    #     #     query = query.filter( getattr(User,attr)==value )
    #     # # now we can run the query
    #     # results = query.all()

    #     rows = 0
    #     found = True
    #     query = self.session.query(self.model)
    #     #rows = query.count()
    #     columns = self.model.__table__.columns.keys()
    #     primary_key = self.model.__mapper__.primary_key
    #     primary_keys = []
    #     filter_applied = False
    #     if len(primary_key) > 0:
    #         for pk in primary_key:
    #             # print(pk)
    #             primary_keys.append(pk.key)
    #         ix = 0
    #         for key in primary_keys:
    #             val = kwargs.get(key)
    #             if val:
    #                 ix = ix + 1
    #                 # column = self.model.__table__.columns.get(key,None)
    #                 #print(column)
    #                 #if not column == None:
    #                 filter_applied = True
    #                 # filt = column.in_(val)
    #                 query = query.filter( getattr(self.model,key)==val )
    #                 # # now we can run the query
    #                 # results = query.all()
    #                 # rows = query.count()
    #                 # print(rows)
    #                 # results = query.all()
    #                 # print(results)
    #                 # print(len(results))


    #                 # if ix==1:
    #                 #     query = self.session.query(filt)
    #                 #     rows = query.count()
    #                 #     print(rows)
    #                 #     results = query.all()
    #                 #     print(results)
    #                 #     # print(len(results))
    #                 #     #                         
    #                 # else:
    #                 #     query = query.filter(filt)
    #                 #     rows = query.count()
    #                 #     print(rows)
    #     else:
    #         ix = 0
    #         for key in columns:
    #             if key.startswith("_"):
    #                 continue
    #             val = kwargs.get(key)
    #             if val:
    #                 filter_applied = True
    #                 query = query.filter( getattr(self.model,key)==val )

    #                 # ix = ix + 1
    #                 # column = self.model.__table__.columns.get(key,None)
    #                 # #print(column)
    #                 # #if not column == None:
    #                 # filter_applied = True
    #                 # filt = column.in_(val)
    #                 # if ix==1:
    #                 #     query = self.session.query(filt)
    #                 # else:
    #                 #     query = query.filter(filt)

    #     self.query = query

    #     # if not filter_applied:
    #     #     found = False
    #     #     rows=0
    #     #     #rows=query.count()
    #     # else:
    #     #     rows=query.count()
    #     #     if rows > 0:
    #     #         found = True
    #     # if not found:
    #     #     results_dict = {}
    #     # else:
    #     #     results = query.all()
    #     #     results_dict = self.to_dict()
        
    #     return query
    ########################################################################################
    # def row_exists(self,keyworded_fields_list):
    #     query = self.xquery_from_dict(keyworded_fields_list)
    #     if query:
    #         rows = query.count()
    #         # print(rows)
    #         if rows > 0:
    #             return True
    #     else:
    #         return False
    ########################################################################################
    # def locate_record(self,kwargs):
    #     if type(kwargs)==type({}):
    #         query = self.session.query(self.model)
    #         primary_keys = self.model.__mapper__.primary_key
    #         if len(primary_keys) > 0:
    #             for primary_key in primary_keys:
    #                 # if primary_key.key in kwargs.keys():
    #                 val = kwargs.get(primary_key.key)
    #                 query = query.filter( getattr(self.model,primary_key.key)==val )
    #         else:
    #             columns = self.model.__table__.columns.keys()
    #             for key in columns:
    #                 if key.startswith("_"):
    #                     continue
    #                 if key in kwargs.keys():
    #                     val = kwargs.get(key)
    #                     query = query.filter(getattr(self.model,key)==val )
    #     elif type(kwargs) == type(''):
    #         select_sql=f"select * from {self.model.__tablename__} where {kwargs}"
    #         query = self.session.query(self.model).from_statement(text(select_sql)).params().all()
    #     else:
    #         return {}
    #     self.query = query
    #     self.query_rows = query.count()
    #     if not self.query_rows == 1:
    #         self.current_record_obj = None
    #         self.current_record_dict = {}
    #         self.records_obj = []
    #         self.records_dict = []
    #         return {}
    #     self.current_record_obj = query.first()
    #     self.current_record_dict = self.to_dict(self.current_record_obj)
    #     self.records_obj = [self.current_record_obj]
    #     self.records_dict = [self.current_record_dict]
    #     return self.current_record_dict
    # ########################################################################################
    # def query_one_record(self,kwargs):
    #     if type(kwargs)==type({}):
    #         query = self.session.query(self.model)
    #         primary_keys = self.model.__mapper__.primary_key
    #         if len(primary_keys) > 0:
    #             for primary_key in primary_keys:
    #                 if primary_key.key in kwargs.keys():
    #                     val = kwargs.get(primary_key.key)
    #                     query = query.filter( getattr(self.model,primary_key.key)==val )
    #         else:
    #             columns = self.model.__table__.columns.keys()
    #             for key in columns:
    #                 if key.startswith("_"):
    #                     continue
    #                 if key in kwargs.keys():
    #                     val = kwargs.get(key)
    #                     query = query.filter(getattr(self.model,key)==val )
    #     elif type(kwargs) == type(''):
    #         select_sql=f"select * from {self.model.__tablename__} where {kwargs}"
    #         query = self.session.query(self.model).from_statement(text(select_sql)).params().all()
    #     else:
    #         return {}
    #     self.query = query
    #     self.query_rows = query.count()
    #     self.current_record_obj = query.first()
    #     self.current_record_dict = self.to_dict(self.current_record_obj)
    #     self.records_obj = [self.current_record_obj]
    #     self.records_dict = [self.current_record_dict]
    #     return self.current_record_dict
    # ########################################################################################
    # def query_just_a_record(self, kwargs):
    #     if type(kwargs)==type({}):
    #         query = self.session.query(self.model)
    #         columns = self.model.__table__.columns.keys()
    #         for key in columns:
    #             if key.startswith("_"):
    #                 continue
    #             if key in kwargs.keys():
    #                 val = kwargs.get(key)
    #                 query = query.filter(getattr(self.model, key) == val)
    #     elif type(kwargs) == type(''):
    #         select_sql=f"select * from {self.model.__tablename__} where {kwargs}"
    #         query = self.session.query(self.model).from_statement(text(select_sql)).params().all()
    #     else:
    #         return {}
    #     self.query = query
    #     self.query_rows = query.count()
    #     self.current_record_obj = query.first()
    #     self.current_record_dict = self.to_dict(self.current_record_obj)
    #     # self.records_obj = query.all()
    #     # self.records_dict = []
    #     # for row in self.records_obj:
    #     #     self.records_dict.append(self.to_dict(row, method=''))
    #     return self.current_record_dict
    # ########################################################################################
    # def query_records(self, kwargs):
    #     if type(kwargs)==type({}):
    #         query = self.session.query(self.model)
    #         columns = self.model.__table__.columns.keys()
    #         for key in columns:
    #             if key.startswith("_"):
    #                 continue
    #             if key in kwargs.keys():
    #                 val = kwargs.get(key)
    #                 query = query.filter(getattr(self.model, key) == val)
    #     elif type(kwargs) == type(''):
    #         select_sql=f"select * from {self.model.__tablename__} where {kwargs}"
    #         query = self.session.query(self.model).from_statement(text(select_sql))
    #     else:
    #         return {}
    #     self.query = query
    #     self.query_rows = query.count()
    #     self.current_record_obj = query.first()
    #     self.current_record_dict = self.to_dict(self.current_record_obj)
    #     self.records_obj = query.all()
    #     self.records_dict = []
    #     for row in self.records_obj:
    #         self.records_dict.append(self.to_dict(row, method=''))
    #     return self.records_dict
    # # ########################################################################################
    # # def query_records_from_sql(self,kwargs):
    # #     query = self.session.query(self.model).from_statement(text(kwargs)).params().all()
    # #     user = session.query(User).from_statement(
    # #         text("SELECT * FROM users where name=:name")).\
    # #         params(name='ed').all()

    # #     return user
    # ########################################################################################
    # def standard_updates(self):
    #     if self.current_record_obj:
    #         try:
    #             self.current_record_obj.last_usage_timestamp = datetime.datetime.utcnow()
    #         except:
    #             pass
    #         try:
    #             if not self.current_record_obj.times_used:
    #                 self.current_record_obj.times_used = 1
    #             else:
    #                 self.current_record_obj.times_used = self.current_record_obj.times_used + 1
    #         except:
    #             pass
    # ########################################################################################
    # def lowlevel_insert(self, kwargs):
    #     # self.query_one_record(kwargs)
    #     # if self.query_rows <=0:
    #         valid_fields_dictionary = self.valid_fields_dictionary(kwargs)
    #         new_record = self.model(**valid_fields_dictionary)
    #         self.session.add(new_record)
    #         self.standard_updates()
    #         self.session.commit()
    #         self.current_record_obj = new_record
    #         self.current_record_dict = self.to_dict(self.current_record_obj)
    #         return self.current_record_dict
    #     # else:
    #     #     return {}
    # ########################################################################################
    # def lowlevel_update(self, kwargs):
    #     self.query_one_record(kwargs)
    #     if self.query_rows > 0:
    #         valid_fields_dictionary = self.valid_fields_dictionary(kwargs)
    #         changes = self.current_record_obj.update_from_dict(**valid_fields_dictionary)
    #         self.last_changes = changes
    #         if self.session.is_modified(self.current_record_obj, include_collections=False):
    #             self.standard_updates()
    #             self.session.commit()
    #             self.current_record_dict = self.to_dict(self.current_record_obj)
    #         # if len(self.last_changes) > 0:
    #         #     self.session.commit()
    #         #     self.current_record_dict = self.to_dict(self.current_record_obj)
    #         return self.current_record_dict
    #     else:
    #         return {}
    # ########################################################################################
    # def lowlevel_insert_or_update(self, kwargs):
    #     self.query_one_record(kwargs)
    #     if not self.query_rows > 0:
    #         valid_fields_dictionary = self.valid_fields_dictionary(kwargs)
    #         new_record = self.model(**valid_fields_dictionary)
    #         self.session.add(new_record)
    #         self.standard_updates()
    #         self.session.commit()
    #         self.current_record_obj = new_record
    #         self.current_record_dict = self.to_dict(self.current_record_obj)
    #         return self.current_record_dict
    #     else:
    #         valid_fields_dictionary = self.valid_fields_dictionary(kwargs)
    #         changes = self.current_record_obj.update_from_dict(**valid_fields_dictionary)
    #         self.last_changes = changes
    #         if self.session.is_modified(self.current_record_obj, include_collections=False):
    #             self.standard_updates()
    #             self.session.commit()
    #             self.current_record_dict = self.to_dict(self.current_record_obj)
    #         return self.current_record_dict
    # ########################################################################################
    # def lowlevel_delete(self, kwargs):
    #     self.query_one_record(kwargs)
    #     if self.query_rows > 0:
    #         deleted_record = self.current_record_dict
    #         self.current_record_obj.delete()
    #         self.session.commit()
    #         return deleted_record
    #     else:
    #         return {}
#     #::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
    #shalimar
    def get_one_row_as_dict(self, access_key):
        rowObj = self.get_one_row(access_key)
        if not rowObj:
            return {}
        current_record_dict = self.to_dict(rowObj)
        return current_record_dict
    #::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
    def get_rows_as_dict(self, access_key):
        rowObjs = self.get_rows(access_key)
        if not rowObjs:
            return []
        records_dict = self.rows_to_dict(rowObjs)
        return records_dict
    #::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
    def get_one_row(self, access_key):
        msg0=f"{colors.YELLOW}{self.model.__tablename__}.get_one_row{colors.RESET} : "
        filter_dict = self.smart_locate_expression(access_key)
        msg1=f"{colors.LIGHTBLACK_EX}search filter:{colors.CYAN}{filter_dict}{colors.RESET}"
        query = self.make_query(filter_dict)
        if not query:
            msg = msg0 + f"{colors.RED}query failed{colors.RESET} " + msg1
            print(msg)
            return None
        query_rows = query.count()
        if not query_rows >= 1:
            c1=colors.RED
            msg = msg0 + f"{colors.RED}NOT FOUND{colors.RESET} " + f"{colors.LIGHTBLACK_EX}query result rows:{c1}{query_rows}{colors.RESET} " + msg1
            print(msg)
            return None
        current_record_obj = query.first()
        if query_rows > 1:
            c1 = colors.RED
        else:
            c1 = colors.GREEN
    
        msg = msg0 + f"{colors.LIGHTBLACK_EX}query result rows:{c1}{query_rows}{colors.RESET} " + msg1
        print (msg)

        return current_record_obj
    #::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
    def get_rows(self, access_key):
        filter_dict = self.smart_locate_expression(access_key)
        print(f"{colors.YELLOW}{self.model.__tablename__} : {colors.LIGHTBLACK_EX}search filter :{colors.CYAN}",filter_dict,f"{colors.WHITE}")
        query = self.make_query(filter_dict)
        if not query:
            return None
        query_rows = query.count()
        print(f"{colors.YELLOW}{self.model.__tablename__} : {colors.LIGHTBLACK_EX}query result rows :{colors.CYAN}",query_rows,f"{colors.WHITE}")
        if not query_rows >= 1:
            return None
        current_record_objects = query.all()
        return current_record_objects
    #::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
    def row_exists(self, access_key):
        filter_dict = self.smart_locate_expression(access_key)
        query = self.make_query(filter_dict)
        if not query:
            return False
        query_rows = query.count()
        if query_rows >= 1:
            return True
        else:
            return False
    #::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
    def make_query(self, kwargs):
        if type(kwargs)==type({}):
            query = self.session.query(self.model)
            for key in kwargs.keys():
                if key in self.model.__table__.columns.keys():
                    val = kwargs.get(key)
                    query = query.filter(getattr(self.model, key) == val)
        elif type(kwargs) == type(''):
            select_sql=f"select * from {self.model.__tablename__} where {kwargs}"
            query = self.session.query(self.model).from_statement(text(select_sql)).params().all()
        else:
            return None
        return query
    ########################################################################################
    def insert_or_update(self, kwargs):
        valid_fields_dictionary = self.valid_fields_dictionary(kwargs)
        record_obj= self.get_one_row(kwargs)
        if not record_obj:
            new_record = self.model(**valid_fields_dictionary)
            self.session.add(new_record)
            # self.standard_updates()
            # self.session.commit()
            # self.current_record_obj = new_record
            # self.current_record_dict = self.to_dict(self.current_record_obj)
            return new_record
        else:
            record_obj.update_from_dict(**valid_fields_dictionary)
            # if self.session.is_modified(self.current_record_obj, include_collections=False):
            #     self.standard_updates()
            #     self.session.commit()
            #     self.current_record_dict = self.to_dict(self.current_record_obj)
            return record_obj
    ########################################################################################
#     #::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
#     #::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
#     # one record functions
#     #::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
#     #::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
#     #::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
    def insert(self, json_record, user='?'):
        result = self.lowlevel_insert(json_record)
        return result
    #::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
    def refresh(self, json_record, user='?'):
        return self.lowlevel_insert_or_update(json_record)
    #::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
    def xxinsert_or_update(self, json_record, user='?'):
        return self.lowlevel_insert_or_update(json_record)
    #::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
    def update(self, json_record, access_key='', user='?'):
        if access_key:
            locate_expression = self.locate_expression_dict(access_key)
            json_record.update(locate_expression)
        result = self.lowlevel_update(json_record)
        return result
    #::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
    def delete(self, access_key, user='?'):
        locate_expression = self.locate_expression_dict(access_key)
        result = self.lowlevel_delete(locate_expression)
        return result
    #::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
    def retrieve(self, access_key, user='?'):
        locate_expression = self.locate_expression_dict(access_key)
        result = self.query_one_record(locate_expression)
        return result
    #::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
    def get(self, access_key, user='?'):
        locate_expression = self.locate_expression_dict(access_key)
        result = self.query_one_record(locate_expression)
        return result
    #::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
    # def get_one(self, access_key, user='?'):
    #     locate_expression = self.locate_expression_dict(access_key)
    #     result = self.query_just_a_record(locate_expression)
    #     return result
    #::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
    # def record_exists(self, access_key, user='?'):
    #     locate_expression = self.locate_expression_dict(access_key)
    #     result = self.query_one_record(locate_expression)
    #     if result:
    #         return True
    #     else:
    #         return False
#     #::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
#     #::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
#     #::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
#     # physical table commands
#     #::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
#     #::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
#     #::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
    def check_table(self):
        self.compare_with_physical_table(silent=True)
        query = self.session.query(self.model)
        self.table_rows = query.count()
        if self.physical_table_is_synchronized:
            msg = f"table [[{self.model.__tablename__}]] loaded with [{self.table_rows} rows]"
        else:
            msg = f"table [[{self.model.__tablename__}]] loaded with [{self.table_rows} rows]"
            if self.new_columns > 0:
                msg = msg + f", [[[{self.new_columns} new]]]"
            if self.unmapped_columns > 0:
                msg = msg + f", [[[{self.unmapped_columns} unmapped]]]"
            if self.changed_columns > 0:
                msg = msg + f", [[[{self.changed_columns} changed]]]"
            msg = msg + f" columns"
        if thisApp.DEBUG_ON or debug:
            log_message(msg, msgType='info')
#     #::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
    def display_table_ddls(self):
        engine=self.session.bind.engine
        metadata = MetaData(bind=engine)

        ddl_obj = create_table_ddl(self.model.__table__, self.session.bind.engine)
        ddl_obj = drop_table_ddl(self.model.__table__, self.session.bind.engine)
        ddl_obj = clear_table_ddl(self.model.__table__, self.session.bind.engine)
        ddl_obj = drop_table_constraints_ddl(self.model.__table__, self.session.bind.engine)
        ddl_obj = create_table_constraints_ddl(self.model.__table__, self.session.bind.engine)
        ddl_obj = drop_table_indexes_ddl(self.model.__table__, self.session.bind.engine)
        ddl_obj = create_table_indexes_ddl(self.model.__table__, self.session.bind.engine)
        #all columns ddl_obj
        for k in self.model.__table__.columns.keys():
            columnObj = self.model.__table__.columns[k]
            ddl_obj = table_column_ddl(columnObj, self.model.__table__, self.session.bind.engine)

#     #::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
    def compare_with_physical_table(self,silent=True):
        engine=self.session.bind.engine
        #check for changes
        metadata = MetaData(bind=engine)
        self.physical_table_is_synchronized = True
        self.unmapped_columns = 0
        self.new_columns = 0
        self.changed_columns = 0
        physical_table = Table(self.model.__tablename__, metadata, autoload=True)

        for c in physical_table.columns:
            if c.key not in self.model.__table__.columns.keys():
                if not silent:
                    print(f'-unmapped field in table {self.model.__tablename__} : {c.key}')
                self.physical_table_is_synchronized = False
                self.unmapped_columns = self.unmapped_columns + 1
                
        for k in self.model.__table__.columns.keys():
            if k not in physical_table.columns.keys():
                if not silent:
                    print(f'-missing field from table {self.model.__tablename__} : {c.key}')
                self.physical_table_is_synchronized=False
                self.new_columns = self.new_columns + 1

        for c in physical_table.columns:
            physical_table_column = physical_table.columns[c.key]
            if c.key in self.model.__table__.columns.keys():
                model_column = self.model.__table__.columns[c.key]
                physical_table_column_type = physical_table_column.type.compile(engine.dialect)
                model_column_type = model_column.type.compile(engine.dialect)
                if not physical_table_column_type == model_column_type:
                    if not silent:
                        print(f'-changed field in table {self.model.__tablename__} : {c.key} from {physical_table_column_type} to {model_column_type}')
                    self.physical_table_is_synchronized=False
                    self.changed_columns = self.changed_columns + 1
        #kill garbage
        del physical_table  #remove it from stack
#     #::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
    def synchronize_physical_table(self):
        self.compare_with_physical_table()
        if not self.physical_table_is_synchronized:
            if self.new_columns > 0 and self.unmapped_columns == 0 and self.changed_columns == 0:
                engine=self.session.bind.engine
                metadata = MetaData(bind=engine)
                physical_table = Table(self.model.__tablename__, metadata, autoload=True)
                for k in self.model.__table__.columns.keys():
                    if k not in physical_table.columns.keys():
                        new_column = self.model.__table__.columns[k]
                        self.add_column(new_column)
                del physical_table
            else:
                self.recreate_table()
            self.compare_with_physical_table()
        # for c in physical_table.columns:
        #     if c.key not in self.model.__table__.columns.keys():
        #         #print(self.model.__tablename__, 'o unmapped field in table :',c.key)
        #         not_mapped_column = physical_table.columns[c.key]
        #         self.drop_column(not_mapped_column)

        # for k in self.model.__table__.columns.keys():
        #     if k not in physical_table.columns.keys():
        #         #print(self.model.__tablename__, 'o missing field from table :', k)
        #         new_column = self.model.__table__.columns[k]
        #         self.add_column(new_column)

        # for c in physical_table.columns:
        #     physical_table_column = physical_table.columns[c.key]
        #     if c.key in self.model.__table__.columns.keys():
        #         model_column = self.model.__table__.columns[c.key]
        #         physical_table_column_type = physical_table_column.type.compile(engine.dialect)
        #         model_column_type = model_column.type.compile(engine.dialect)
        #         if not physical_table_column_type == model_column_type:
        #             #print(self.model.__tablename__, 'o data type different :',c.key,'from :',physical_table_column_type,' to :',model_column_type)
        #             self.alter_column(model_column)
        
        # del physical_table #remove it from stack
#     #::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
    def add_column(self, columnObj):
        engineObj = self.session.bind.engine
        tableObj = self.model.__table__
        ddl_string=add_table_column_ddl(columnObj,tableObj,engineObj)
        engineObj.execute(ddl_string)
#     #::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
    def drop_column(self, columnObj):
        engineObj = self.session.bind.engine
        tableObj = self.model.__table__
        ddl_string=drop_table_column_ddl(columnObj,tableObj,engineObj)
        #engineObj.execute(ddl_string)
#     #::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
    def alter_column(self, columnObj):
        engineObj = self.session.bind.engine
        tableObj = self.model.__table__
        ddl_string=alter_table_column_ddl(columnObj,tableObj,engineObj)
        #engineObj.execute(ddl_string)
#     #::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
    def make_column_DDL(self, column):
        engine = self.session.bind.engine
        table_name = self.model.__tablename__
        #column_name = column.compile(dialect=engine.dialect)
        column_name = column.name
        column_type = column.type.compile(engine.dialect)
        column_default = ''
        if column.default:
            sdef = column.default.arg
            #print(sdef)
            try:
                column_default = column.default.compile(dialect=engine.dialect)
            except:
                column_default = ''

        if column_default:
            print('---default---',column_default)

        DDL_command = f"TABLE {table_name} COLUMN {column_name} {column_type} {column_default}"
        print('column_DDL :',DDL_command)
        #engine.execute(DDL_command)
#     #::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
    def drop_table(self):
        # self.model.__table__.drop(self.session.bind.engine, checkfirst=True)
        # drop_table_ddl
        engineObj = self.session.bind.engine
        tableObj = self.model.__table__
        ddl_string=drop_table_ddl(tableObj,engineObj)
        engineObj.execute(ddl_string)
    #::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
    def clear_table(self):
        engineObj = self.session.bind.engine
        tableObj = self.model.__table__
        ddl_string=clear_table_ddl(tableObj,engineObj)
        engineObj.execute(ddl_string)
    #::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
    def recreate_table(self):
        #backup the table
        backup_table=self.model.__tablename__+'_backup'
        if not self.copy_table(backup_table):
            msg ='copy to backup failed'
            return

        metadata = MetaData(bind=self.session.bind.engine)
        backuptable = Table(backup_table, metadata, autoload=True)
        old_columns = backuptable.columns
        query = self.session.query(backuptable)
        old_rows = query.count()
        
        #drop and recreate with the new structure
        self.model.__table__.drop(self.session.bind.engine,checkfirst=True)
        self.model.__table__.create(self.session.bind.engine, checkfirst=True)
        columns = [c.copy() for c in self.model.__table__.columns]

        #copy data from backup
        columns_str=''
        for column in columns:
            if column.key in old_columns.keys():
                if columns_str:
                    columns_str = columns_str + ' , ' + column.name
                else:
                    columns_str = column.name
        from_table = backup_table
        to_table =self.model.__tablename__
        ddl_string = f"INSERT INTO {to_table} ({columns_str}) select {columns_str} from {from_table}"
        #print(ddl_string)
        engineObj = self.session.bind.engine
        try:
            engineObj.execute(ddl_string)
        except Exception as e:
            print(e)

        query = self.session.query(self.model)
        new_rows = query.count()
        if new_rows==old_rows:
            backuptable.drop(self.session.bind.engine,checkfirst=True)
        
        #kill garbages
        del backuptable

        msg=f"table [[{self.model.__tablename__}]] [recreated] with [[[{new_rows}/{old_rows} rows copied]]] from backup table {backup_table}"
        if thisApp.CONSOLE_ON:
            log_message(msg, msgType='info')
    #::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
    def copy_table(self,new_table_name):
        metadata = MetaData(bind=self.session.bind.engine)
        physical_table = Table(self.model.__tablename__, metadata, autoload=True)
        columns = [c.copy() for c in physical_table.columns]
        query = self.session.query(physical_table)
        query_rows1 = query.count()

        new_table = Table(new_table_name, metadata, *columns)
        new_table.drop(self.session.bind.engine, checkfirst=True)
        new_table.create(self.session.bind.engine, checkfirst=True)
        new_table = Table(new_table_name, metadata, autoload=True)
        columns = [c.copy() for c in new_table.columns]

        columns_str=''
        for column in columns:
            if columns_str:
                columns_str = columns_str + ' , ' + column.name
            else:
                columns_str = column.name
        from_table = self.model.__tablename__
        to_table = new_table.name
        ddl_string = f"INSERT INTO {to_table} ({columns_str}) select {columns_str} from {from_table}"
        #print(ddl_string)
        engineObj=self.session.bind.engine
        try:
            engineObj.execute(ddl_string)
        except Exception as e:
            print(e)
            return False

        query = self.session.query(new_table)
        query_rows2 = query.count()

        #garbage kill
        del new_table
        del physical_table

        msg=f"table [[{from_table}]] [copied to ] [[{to_table}]] with [[[{query_rows2}/{query_rows1} rows]]]."
        if thisApp.CONSOLE_ON:
            log_message(msg, msgType='info')
        if query_rows1 == query_rows2:
            return True
        else:
            return False
    #::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::

    # def clone_table_approach_1(original_table, connection, metadata):
    #     try:
    #         new_table_name = original_table.name + '_sync'
    #         columns = [c.copy() for c in original_table.columns]
    #         new_table = Table(new_table_name, metadata, quote=False, *columns)

    #         # Create table in database
    #         if not new_table.exists():
    #             new_table.create()
    #         else:
    #             raise Exception("New table already exists")

    #         # Remove constraints from new table if any
    #         for constraint in new_table.constraints:
    #             connection.execute(DropConstraint(constraint))

    #         # Return table handle for newly created table
    #         final_cloned_table = Table(new_table, metadata, quote=False)
    #         return final_cloned_table

    #     except:
    #         # Drop if we did create a new table
    #         if new_table.exists():
    #             new_table.drop()
    #         raise
    # #::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::

#device_usage = dbtable(session, dbmodel.DEVICE_USAGE, 'device_usage', 'device_usage')

#     def getid(self,json_record):
#         if not json_record:
#             return None
#         entity_record = self.get(json_record)
#         entity_id = entity_record.get(self.rowid_column)
#         return entity_id
#     #::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
#     def input_record(self, json_record={}):
#         for c in self.input_columns:
#             v = json_record.get(c, None)
#             if v == None:
#                 if self.table_structure_dictionary.get(c.upper(), {}).get('column_is_numeric',False):               
#                     json_record.update({c:0})
#                 else:
#                     json_record.update({c:''})
#         for c in self.primary_key_columns:
#             v = json_record.get(c, None)
#             if v == None:
#                 if self.table_structure_dictionary.get(c.upper(), {}).get('column_is_numeric',False):               
#                     json_record.update({c:0})
#                 else:
#                     json_record.update({c:''})
#         for c in self.mandatory_columns:
#             v = json_record.get(c, None)
#             if v == None:
#                 if self.table_structure_dictionary.get(c.upper(), {}).get('column_is_numeric',False):               
#                     json_record.update({c:0})
#                 else:
#                     json_record.update({c:''})

#         json_record = valid_json_record_to_table_structure(self.table_structure_dictionary, json_record)
#         json_record = normalized_json_record(json_record)
#         return json_record
#     #::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::

#     #::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
#     #::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
#     # exec functions
#     #::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
#     #::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
#     #::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
#     def try_insert(self, json_record, user='?'):
#         result = self.insert_validation(json_record)
#         if not result.get('api_status') == 'success':
#             return result
#         result = self.table_record_insert(json_record, user=user)
#         return result
#     #::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
#     def try_update(self, json_record, user='?'):
#         # result = self.update_validation(json_record)
#         # if not result.get('api_status') == 'success':
#         #     return result
#         result = self.table_record_update(json_record, user=user)
#         return result        
#     #::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
#     def try_refresh(self, json_record, user='?'):
#         result = self.table_record_insert_or_update(json_record, user=user)
#         return result
#     #::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
#     def validate_insert(self, json_record, user='?'):
#         return self.insert_validation(json_record)
#     #::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
#     def validate_update(self, json_record, access_key='', user='?'):
#         return self.update_validation(json_record,access_key=access_key)
#     #::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
#     #::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
#     #::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
#     # multiple records functions
#     #::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
#     #::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
#     #::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
    def sqlquery(self, where_expression, columns=None, order_by=None, rows_limit=None, exclude_null_columns=True, exclude_columns=None, user='?'):
        where_expression="1=1"
        results = self.query_records(where_expression)
        return results
        # result = self.retrieve_rows(where_expression, columns=columns, order_by=order_by, rows_limit=rows_limit, exclude_null_columns=exclude_null_columns, exclude_columns=exclude_columns, user=user)
        # self.query = query
        # self.query_rows = query.count()
        # self.current_record_obj = query.first()
        # self.current_record_dict = self.to_dict(self.current_record_obj)
        # self.records_obj = query.all()
        # self.records_dict = []
        # for row in self.records_obj:
        #     self.records_dict.append(self.to_dict(row, method=''))
        # return self.records_dict        
#     #::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
    def update_rows(self, where_expression, json_record,user='?'):
        results = self.query_records(where_expression)
        valid_fields_dictionary = self.valid_fields_dictionary(json_record)
        self.query.update(valid_fields_dictionary)
        self.session.commit()
        return results
#     #::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
    def delete_rows(self, where_expression,user='?'):
        results = self.query_records(where_expression)
        self.query.delete(synchronize_session=False)
        self.session.commit()
        # sqlCommand = f"DELETE FROM {self.table_name} WHERE {where_expression}"
        # sess.query(User).filter(User.age == 25).\
        # delete(synchronize_session=False)
        # result = self.table_records_delete(where_expression,user)
        return results
#     #::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
    def retrieve_records(self, where_expression, columns=None, order_by=None, rows_limit=None, exclude_null_columns=True, output_format='json', format_methods=None, exclude_columns=None, user='?'):
        results = self.query_records(where_expression)
        #output = self.table_records_retrieve(where_expression, columns=columns, order_by=order_by, rows_limit=rows_limit, exclude_null_columns=exclude_null_columns, output_format=output_format, format_methods=format_methods, exclude_columns=exclude_columns, user=user)
        return results
#     #::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
#     #::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
#     #::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
#     # column functions
#     #::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
#     #::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
#     #::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
    def column_value(self, column_name, where_expression, columnvalueFunction='MAX', user='?'):
        # return self.get_column_value(column_name=column_name, where_expression=where_expression, columnvalueFunction=columnvalueFunction, user=user)
        result = self.query_one_record(where_expression)
        #output = self.table_records_retrieve(where_expression, columns=columns, order_by=order_by, rows_limit=rows_limit, exclude_null_columns=exclude_null_columns, output_format=output_format, format_methods=format_methods, exclude_columns=exclude_columns, user=user)
        return result.get(column_name)
#     #::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
#     #::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
#     #::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
#     # exec sql functions
#     #::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
#     #::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
#     #::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
#     def execute_query(self, query='', command_description='', exclude_null_columns=True, user='?'):
#         return self.dbConnectionObj.exec_sql_query(query, command_description=command_description, exclude_null_columns=exclude_null_columns)
#     #::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
#     def execute_sql_command(self, query='', command_description='', user='?'):
#         return self.dbConnectionObj.exec_sql_query(query, command_description=command_description)
#     #::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
#     #::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
#     #::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
#     #@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
#     #@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
#     #@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
#     #functions flow implementation
#     #@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
#     #@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
#     #@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
#     def table_record_insert(self, json_record, user=''):
#         record_function=f'insert'

#         if self.debug_level > 0:
#             set_debug_ON()
        

#         result = standard_table_call_validation(self.table_reference,json_record=json_record, access_key='dummy', user=user)
#         if not result.get('api_status') == 'success':
#             if self.debug_level > 0:
#                 set_debug_OFF()
#             return result
        
#         if self.primary_key_columns:
#             current_record = self.locate_row(json_record,record_function)
#             if current_record:
#                 row_descriptor = self.get_row_descriptor(json_record)
#                 msg=f"{row_descriptor} already exists"
#                 log_message(msg,msgType='error')
#                 if self.debug_level > 0:
#                     set_debug_OFF()
#                 return {'api_status':'error','api_message':msg}
        
#         if self.debug_level > 0:
#             set_debug_OFF()
#         result = self.insert_row(json_record, user=user)
#         return result
#     #::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
#     def table_record_insert_or_update(self, json_record, user=''):
#         record_function=f'insert'

#         if self.debug_level > 0:
#             set_debug_ON()

#         result = standard_table_call_validation(self.table_reference,json_record=json_record, access_key='dummy', user=user)
#         if not result.get('api_status') == 'success':
#             if self.debug_level > 0:
#                 set_debug_OFF()
#             return result
    
#         if self.primary_key_columns:
#             current_record = self.locate_row(json_record,record_function)
#             if current_record:
#                 where_expression = self.rowid_where_expression(current_record)
#                 if not where_expression:
#                     row_descriptor = self.get_row_descriptor(json_record)
#                     msg=f'{row_descriptor} [[{record_function}]] canceled due to database integrity error. rowid or record_id not identified'                
#                     log_message(msg, msgType='error')
#                     msg=msg.replace('[[','[').replace(']]',']').replace('[[[','[').replace(']]]',']')
#                     result = {'api_status': 'error','api_message': msg}
#                     if self.debug_level > 0:
#                         set_debug_OFF()
#                     return result
#                 result = self.update_row(json_record, where_expression=where_expression, current_record=current_record,user=user)
#                 if self.debug_level > 0:
#                     set_debug_OFF()
#                 return result
        
#         if self.debug_level > 0:
#             set_debug_OFF()
#         result=self.insert_row(json_record, user=user)
#         return result
#     #::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
#     def table_record_update(self, json_record, access_key='dummy', user=''):
#         record_function=f'update'

#         if self.debug_level > 0:
#             set_debug_ON()

#         result = standard_table_call_validation(self.table_reference,json_record=json_record, access_key=access_key, user=user)
#         if not result.get('api_status') == 'success':
#             if self.debug_level > 0:
#                 set_debug_OFF()
#             return result

#         if access_key and not access_key=='dummy':
#             current_record = self.locate_row(access_key,record_function)
#             if not current_record:
#                 current_record = self.locate_row(json_record,record_function)
#         else:
#             current_record = self.locate_row(json_record,record_function)

#         if not current_record:
#             row_descriptor = self.get_row_descriptor(json_record)
#             msg=f'{row_descriptor} not found. {self.reference} [[[{record_function}]]] canceled.'                
#             log_message(msg,msgType='error')
#             msg=msg.replace('[[','[').replace(']]',']').replace('[[[','[').replace(']]]',']')
#             result = {'api_status': 'error','api_message': msg}
#             if self.debug_level > 0:
#                 set_debug_OFF()
#             return result
    
#         where_expression=self.rowid_where_expression(current_record)
#         if not where_expression:
#             row_descriptor = self.get_row_descriptor(json_record)
#             msg=f'{row_descriptor} [[{record_function}]] canceled due to database integrity error. rowid or record_id not identified'                
#             log_message(msg,msgType='error')
#             msg=msg.replace('[[','[').replace(']]',']').replace('[[[','[').replace(']]]',']')
#             result = {'api_status': 'error','api_message': msg}
#             if self.debug_level > 0:
#                 set_debug_OFF()
#             return result
    
#         if self.debug_level > 0:
#             set_debug_OFF()
#         result = self.update_row(json_record, where_expression=where_expression,current_record=current_record,user=user)
#         return result
#     #::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
#     def table_record_delete(self, access_key, user=''):
#         record_function=f'delete'

#         if self.debug_level > 0:
#             set_debug_ON()

#         result = standard_table_call_validation(self.table_reference,json_record={'dummy':'dummy'}, access_key=access_key, user=user)
#         if not result.get('api_status') == 'success':
#             if self.debug_level > 0:
#                 set_debug_OFF()
#             return result
    
#         current_record = self.locate_row(access_key,record_function)

#         if not current_record:
#             row_descriptor = self.get_row_descriptor(access_key)
#             msg=f'{row_descriptor} not found. {self.reference} [[[{record_function}]]] canceled.'                
#             log_message(msg,msgType='error')
#             msg=msg.replace('[[','[').replace(']]',']').replace('[[[','[').replace(']]]',']')
#             result = {'api_status': 'error', 'api_message': msg, 'access_key': access_key}
#             if self.debug_level > 0:
#                 set_debug_OFF()
#             return result

#         where_expression=self.rowid_where_expression(current_record)
#         if not where_expression:
#             row_descriptor = self.get_row_descriptor(access_key)
#             msg=f'{row_descriptor} [[{record_function}]] canceled due to database integrity error. rowid or record_id not identified'                
#             log_message(msg, msgType='error')
#             msg=msg.replace('[[','[').replace(']]',']').replace('[[[','[').replace(']]]',']')
#             result = {'api_status': 'error','api_message': msg}
#             if self.debug_level > 0:
#                 set_debug_OFF()
#             return result

#         if self.debug_level > 0:
#             set_debug_OFF()
    
#         result = self.delete_row(where_expression, current_record, user=user)
#         return result
#     #::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
#     def table_record_retrieve(self, access_key, user='', exclude_null_columns=False):
#         record_function=f'retrieve'

#         if self.debug_level > 0:
#             set_debug_ON()

#         result = standard_table_call_validation(self.table_reference,json_record={'dummy':'dummy'}, access_key=access_key, user=user)
#         if not result.get('api_status') == 'success':
#             if self.debug_level > 0:
#                 set_debug_OFF()
#             return result
    
#         current_record = self.locate_row(access_key)

#         if not current_record:
#             row_descriptor = self.get_row_descriptor(access_key)
#             msg=f'{row_descriptor} not found ({record_function})'                
#             log_message(msg,msgType='info')
#             msg=msg.replace('[[','[').replace(']]',']').replace('[[[','[').replace(']]]',']')
#             result = {'api_status': 'notfound','api_message': msg}
#             if self.debug_level > 0:
#                 set_debug_OFF()
#             return result

#         (row_descriptor, record_id, rowid, rowid_column) = self.current_record_standard_columns(current_record)
#         msg=f'{row_descriptor} record rerieved'
#         log_result_message(msg, msgType='OK')
        
#         if self.debug_level > 0:
#             set_debug_OFF()

#         result = {
#             'api_status': 'success',
#             'api_message': msg,
#             'api_data': current_record,
#             'rowid': rowid,
#              rowid_column: record_id,
#             'row_descriptor': row_descriptor,
#             }


#         return result
#     #::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
#     def table_records_update(self, where_expression, json_record, user=''):
#         record_function=f'update'

#         if self.debug_level > 0:
#             set_debug_ON()

#         result = standard_table_call_validation(self.table_reference, json_record=json_record, access_key='dummy', where_expression=where_expression, user=user)
#         if not result.get('api_status') == 'success':
#             if self.debug_level > 0:
#                 set_debug_OFF()
#             return result

#         if where_expression.upper() in ('ALL','*'):
#             where_expression = '1=1'

#         sqlCommand = self.row_update_sqlCommand(where_expression, json_record)        
#         if not sqlCommand:
#             msg='error building row_update_sqlCommand'
#             log_message(msg,msgType='error')
#             msg=msg.replace('[[','[').replace(']]',']').replace('[[[','[').replace(']]]',']')
#             result = {
#                 'api_status': 'error',
#                 'api_message': msg,
#                 'changed_records': 0,
#                 'inserted_records': 0,
#             }
#             if self.debug_level > 0:
#                 set_debug_OFF()
#             return result

#         result = self.execute_query(sqlCommand, command_description='rescords_update')
#         rowcount=result.get('rowcount')
#         if not result.get('api_status') == 'success':
#             msg=result.get('api_message',f'[{self.table_reference}] [[{record_function}]] error with where_expression:{where_expression}')
#             log_message(msg,msgType='error')
#             msg=msg.replace('[[','[').replace(']]',']').replace('[[[','[').replace(']]]',']')
#             result = {'api_status': 'error', 'api_message': msg, 'where_expression':where_expression}
#             if self.debug_level > 0:
#                 set_debug_OFF()
#             return result

#         msg=f'[{self.table_reference}]: {rowcount} row(s) updated.'

#         result = {'api_status': 'success', 'api_message': msg,'changed_records':rowcount}

#         log_result_message(msg,msgType='OK')

#         if self.debug_level > 0:
#             set_debug_OFF()

#         return result
#     #::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
#     def table_records_delete(self, where_expression, user=''):
#         record_function=f'delete'

#         if self.debug_level > 0:
#             set_debudrop_tableg_ON()

#         result = standard_table_call_validation(self.table_reference, json_record={'dummy':'dummy'}, access_key='dummy', where_expression=where_expression, user=user)
#         if not result.get('api_status') == 'success':
#             if self.debug_level > 0:
#                 set_debug_OFF()
#             return result

#         if where_expression.upper() in ('ALL','*'):
#             where_expression = '1=1'

#         sqlCommand = f"DELETE FROM {self.table_name} WHERE {where_expression}"

#         result = self.execute_query(sqlCommand, command_description='delete records')
#         rowcount=result.get('rowcount')
#         if not result.get('api_status') == 'success':
#             msg=result.get('api_message',f'[{self.table_reference}] [[{record_function}]] error with where_expression:{where_expression}')
#             log_message(msg,msgType='error')
#             msg=msg.replace('[[','[').replace(']]',']').replace('[[[','[').replace(']]]',']')
#             result = {'api_status': 'error', 'api_message': msg, 'where_expression':where_expression}
#             if self.debug_level > 0:
#                 set_debug_OFF()
#             return result

#         msg=f'[{self.table_reference}]: {rowcount} row(s) deleted.'
#         result = {'api_status': 'success', 'api_message': msg,'deleted_records':rowcount}

#         log_result_message(msg,msgType='OK')

#         if self.debug_level > 0:
#             set_debug_OFF()

#         return result
#     #::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
#     def table_records_retrieve(self, where_expression='', columns=None, order_by=None, rows_limit=None, exclude_null_columns=False, output_format='json', format_methods='', exclude_columns=None, user=''):
#         record_function=f'retrieve'

#         if self.debug_level > 0:
#             set_debug_ON()

#         result = standard_table_call_validation(self.table_reference, json_record={'dummy':'dummy'}, access_key='dummy', where_expression=where_expression, user=user)
#         if not result.get('api_status') == 'success':
#             if self.debug_level > 0:
#                 set_debug_OFF()
#             return result

#         if where_expression.upper() in ('ALL','*'):
#             where_expression = '1=1'
        
#         columns = select_columns_excluding_columns(columns, exclude_columns, self.table_model)
        
#         result = self.retrieve_rows(where_expression, columns, order_by, rows_limit, exclude_null_columns)
#         if not result.get('api_status') == 'success':
#             msg=result.get('api_message',f'[{self.table_reference}] [[{record_function}]] error with where_expression:{where_expression}')
#             log_message(msg,msgType='error')
#             msg=msg.replace('[[','[').replace(']]',']').replace('[[[','[').replace(']]]',']')
#             result = {'api_status': 'error', 'api_message': msg, 'where_expression':where_expression}
#             if self.debug_level > 0:
#                 set_debug_OFF()
#             return result

#         json_records = result.get('api_data', [])
#         rowcount=len(json_records)
#         title=''
#         output = self.format_json_records_as(format_type=output_format,json_records=json_records,columns=columns,format_methods=format_methods,title=title)

#         msg=f'{rowcount} row(s) retrieved from {self.table_reference}'
#         log_result_message(msg,msgType='OK')
#         msg=msg.replace('[[','[').replace(']]',']').replace('[[[','[').replace(']]]',']')

#         if self.debug_level > 0:
#             set_debug_OFF()

#         result = {'api_status': 'success', 'api_message': msg,'records_retrieved':rowcount}

#         return output
#     #::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
#     #@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
#     #@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
#     #@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
#     #::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
#     #::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
#     #::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
#     # functions implementation (basic functions)
#     #::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
#     #::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
#     #::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
#     def insert_row(self, json_record, user='?'):
#         json_record = self.apply_default_values(json_record,'insert')
#         json_record = valid_json_record_to_table_structure(self.table_structure_dictionary, json_record)
#         json_record = normalized_json_record(json_record)
#         if not json_record:
#             msg='nothing to insert'
#             log_message(msg,msgType='error')
#             msg=msg.replace('[[','[').replace(']]',']').replace('[[[','[').replace(']]]',']')
#             result = {
#                 'api_status': 'error',
#                 'api_message': msg,
#                 'changed_records': 0,
#                 'inserted_records': 0,
#             }
#             return result
                        
#         result = self.apply_table_validations(json_record, rowid=0,table_function='INSERT')
#         if not result.get('api_status') == 'success':
#             msg = result.get('api_message','validation errors')
#             log_message(msg,msgType='error')
#             msg=msg.replace('[[','[').replace(']]',']').replace('[[[','[').replace(']]]',']')
#             result = {
#                 'api_status': 'error',
#                 'api_message': msg,
#                 'changed_records': 0,
#                 'inserted_records': 0,
#             }
#             return result
        
#         row_descriptor = self.get_row_descriptor(json_record)
#         command_description=f'new {row_descriptor}'

#         sqlCommand = self.row_insert_sqlCommand(json_record)
#         if not sqlCommand:
#             msg='error building row_insert_sqlCommand'
#             log_message(msg,msgType='error')
#             msg=msg.replace('[[','[').replace(']]',']').replace('[[[','[').replace(']]]',']')
#             result = {
#                 'api_status': 'error',
#                 'api_message': msg,
#                 'changed_records': 0,
#                 'inserted_records': 0,
#             }
#             return result

#         query_result = self.execute_query(sqlCommand, command_description=command_description)
#         rowid = query_result.get('lastrowid',-1)
#         if rowid <= 0:
#             msg=f"{row_descriptor}: insert error by sql_command [{sqlCommand}]"
#             log_message(msg, msgType='info',level=function_level)
#             msg=f'{row_descriptor} not created.'
#             log_message(msg, msgType='error',level=function_level)
#             result = {
#                 'api_status': 'error',
#                 'api_message': msg,
#                 'changed_records': 0,
#                 'sql_command':sqlCommand
#             }
#             return result

#         where_expression=f"rowid={rowid}"
#         #inserted_record = self.retrieve_one_row(where_expression)

#         self.exec_after_insert_triggers(rowid)
        
#         inserted_record = self.retrieve_one_row(where_expression)

#         (row_descriptor, record_id, rowid, rowid_column) = self.current_record_standard_columns(inserted_record)
#         changed_columns = get_changed_columns(json_record, inserted_record)
#         changed_columns_values = get_changed_columns_values(json_record, inserted_record)

#         msg = f'{row_descriptor} inserted in {self.reference}'
#         log_result_message(msg,msgType='OK')
#         msg=msg.replace('[[','[').replace(']]',']').replace('[[[','[').replace(']]]',']')
        
#         result = {
#                 'api_status': 'success',
#                 'api_message': msg,
#                 'api_data': inserted_record,
#                 'rowid': rowid,
#                  rowid_column: record_id,
#                 'inserted_records': 1,
#                 'changed_columns': changed_columns,
#                 'changed_columns_values': changed_columns_values,
#                 'row_descriptor': row_descriptor,
#             }

#         return result
#     #::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
#     def update_row(self, json_record, where_expression, current_record=None, user='?'):
#         if not where_expression:
#             msg='where_expression not provided. internal system error'
#             log_message(msg,msgType='error')
#             msg=msg.replace('[[','[').replace(']]',']').replace('[[[','[').replace(']]]',']')
#             result = {
#                 'api_status': 'error',
#                 'api_message': msg,
#                 'changed_records': 0,
#             }
#             return result

#         json_record = valid_json_record_to_table_structure(self.table_structure_dictionary, json_record)
#         json_record = normalized_json_record(json_record)
#         if not json_record:
#             msg='nothing to update'
#             log_message(msg,msgType='error')
#             msg=msg.replace('[[','[').replace(']]',']').replace('[[[','[').replace(']]]',']')
#             result = {
#                 'api_status': 'error',
#                 'api_message': msg,
#                 'changed_records': 0,
#             }
#             return result
                
#         if not current_record:
#             current_record = self.retrieve_one_row(where_expression)
        
#         (row_descriptor, record_id, rowid, rowid_column) = self.current_record_standard_columns(current_record)
#         if not rowid or not record_id:
#             msg='invalid current_record provided'
#             log_message(msg,msgType='error')
#             msg=msg.replace('[[','[').replace(']]',']').replace('[[[','[').replace(']]]',']')
#             result = {
#                 'api_status': 'error',
#                 'api_message': msg,
#                 'changed_records': 0,
#             }
#             return result

#         optimized_record = optimize_record_based_on_current_record(json_record, current_record)
#         if not optimized_record:
#             msg=f'{row_descriptor} record is synchronized in {self.reference}. no change applied'
#             log_result_message(msg, msgType='ok', level=function_level)
#             msg=msg.replace('[[','[').replace(']]',']').replace('[[[','[').replace(']]]',']')
#             result = {
#                     'api_status': 'success',
#                     'api_message': msg,
#                     'api_data': current_record,
#                     'rowid': rowid,
#                     'rowid_column': record_id,
#                     'changed_records': 0,
#                     'changed_columns': [],
#                     'changed_columns_values': [],
#                     'row_descriptor': row_descriptor,
#                 }
#             return result

#         validation_result = self.apply_table_validations(optimized_record, rowid=rowid, table_function='UPDATE')
    
#         if not validation_result.get('api_status') == 'success':
#             msg = validation_result.get('api_message','validation errors')
#             log_result_message(msg, msgType='error',level=function_level)
#             msg=msg.replace('[[','[').replace(']]',']').replace('[[[','[').replace(']]]',']')
#             result = {
#                     'api_status': 'error',
#                     'api_message': msg,
#                     'changed_records': 0,
#                     'row_descriptor': row_descriptor,
#                 }
#             return result

#         sqlCommand = self.row_update_sqlCommand(where_expression, optimized_record)        
#         if not sqlCommand:
#             msg='error building row_update_sqlCommand'
#             log_message(msg,msgType='error')
#             msg=msg.replace('[[','[').replace(']]',']').replace('[[[','[').replace(']]]',']')
#             result = {
#                 'api_status': 'error',
#                 'api_message': msg,
#                 'changed_records': 0,
#             }
#             return result

#         command_description=f'update {row_descriptor}'
#         query_result = self.execute_query(sqlCommand, command_description=command_description)
#         if not query_result.get('api_status') == 'success':
#             errormsg=query_result.get('api_message','')
#             msg=f'{row_descriptor} update error:{errormsg}'
#             log_result_message(msg, msgType='error',level=function_level)
#             result = {
#                 'api_status': 'error',
#                 'api_message': msg,
#                 'changed_records': 0,
#                 'sql_command':sqlCommand
#             }
#             return result

#         rowcount=query_result.get('rowcount')
#         changed_records=rowcount
#         msg=f"[{self.table_reference}]: {rowcount} row(s) updated"
#         log_result_message(msg, msgType='info',level=function_level)

#         updated_record = self.retrieve_one_row( where_expression)
#         self.exec_after_update_triggers( rowid, updated_record)
#         if changed_records > 0:
#             msg = f'{row_descriptor} record updated.'
#         else:
#             msg = f'{row_descriptor} record is upToDate.'

#         log_result_message(msg,msgType='OK',level=function_level)

#         updated_record = self.retrieve_one_row( where_expression)
#         (row_descriptor, record_id, rowid, rowid_column) = self.current_record_standard_columns( updated_record)
#         changed_columns = get_changed_columns(current_record, updated_record)
#         changed_columns_values = get_changed_columns_values(current_record, updated_record)
#         if len(changed_columns) <=0:
#             changed_records = 0
#         result = {
#                 'api_status': 'success',
#                 'api_message': msg,
#                 'api_data': updated_record,
#                 'rowid': rowid,
#                  rowid_column: record_id,
#                 'row_descriptor': row_descriptor,
#                 'changed_columns': changed_columns,
#                 'changed_columns_values': changed_columns_values,
#                 'changed_records': changed_records,
#             }

#         return result
#     #::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
#     def retrieve_row(self, where_expression,user='?'):
#         command_description=f'record retrieve'
#         sqlCommand = f"select ROWID as rowid,* from {self.table_name} where {where_expression}"
#         query_result = self.execute_query(sqlCommand, command_description=command_description)
#         rows_count = query_result.get('rows_count', 0)
#         if rows_count > 1:
#             msg=f"[{command_description}]: returned {rows_count} rows. database integrity violation. query:[{where_expression}]"
#             log_message(msg, msgType='error', level=function_level)

#         json_record = get_record_from_query_result(query_result)
#         if not json_record:
#             msg=f"record not found. where={where_expression}"
#             log_message(msg,msgType='error', level=function_level)
#             result = {'api_status': 'error', 'api_message': msg,'where_expression':where_expression}

#         (row_descriptor, record_id, rowid, rowid_column) = self.current_record_standard_columns( json_record)
#         msg=f"{row_descriptor} record retrieved"
#         log_result_message(msg,msgType='OK', level=function_level)

#         result = {'api_status': 'success', 'api_message': msg,'api_data':json_record,f'{rowid_column}': record_id,'rowid':rowid}

#         return result
#     #::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
#     def delete_row(self, where_expression, current_record={},user='?'):
#         record_function=f'delete'
#         if not where_expression:
#             msg=f'where_expression not provided for {record_function}. internal system error'
#             log_message(msg,msgType='error')
#             msg=msg.replace('[[','[').replace(']]',']').replace('[[[','[').replace(']]]',']')
#             result = {
#                 'api_status': 'error',
#                 'api_message': msg,
#                 'changed_records': 0,
#             }
#             return result
    
#         if not current_record:
#             current_record = self.retrieve_one_row(where_expression)

#         if not current_record:
#             msg=f'record not found for delete. {self.reference} [[[{record_function}]]] canceled.'                
#             log_message(msg,msgType='error')
#             msg=msg.replace('[[','[').replace(']]',']').replace('[[[','[').replace(']]]',']')
#             result = {'api_status': 'error', 'api_message': msg, 'where': where_expression}
#             return result

#         sqlCommand = self.row_delete_sqlCommand(where_expression)
#         if not sqlCommand:
#             msg='error building row_delete_sqlCommand'
#             log_message(msg,msgType='error')
#             msg=msg.replace('[[','[').replace(']]',']').replace('[[[','[').replace(']]]',']')
#             result = {
#                 'api_status': 'error',
#                 'api_message': msg,
#                 'deleted_records': 0,
#             }
#             return result

#         (row_descriptor, record_id, rowid, rowid_column) = self.current_record_standard_columns(current_record)
#         if not rowid or not record_id:
#             msg='invalid current_record'
#             log_message(msg,msgType='error')
#             msg=msg.replace('[[','[').replace(']]',']').replace('[[[','[').replace(']]]',']')
#             result = {
#                 'api_status': 'error',
#                 'api_message': msg,
#                 'changed_records': 0,
#             }
#             return result

#         #command_description=f'delete {row_descriptor}'

#         result = self.execute_query(sqlCommand, command_description='delete')
#         rowcount = result.get('rowcount', 0)
#         if not result.get('api_status') == 'success':
#             msg=result.get('api_message',f'[{self.table_reference}] [[{record_function}]] error with where:{where_expression}')
#             log_message(msg,msgType='error')
#             msg=msg.replace('[[','[').replace(']]',']').replace('[[[','[').replace(']]]',']')
#             result = {'api_status': 'error', 'api_message': msg, 'where':where_expression}
#             return result
    
#         deleted_record = current_record
#         msg=f'{row_descriptor} : {rowcount} row deleted.'
#         log_result_message(msg,msgType='OK')

#         result = {
#             'api_status': 'success',
#             'api_message': msg,
#             'rowid': rowid,
#              rowid_column: record_id,
#             'api_data': deleted_record,
#             'row_descriptor': row_descriptor,
#             }


#         return result
#     #::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
#     def get_column_value(self, column_name, where_expression, columnvalueFunction='max', user='?'):
#         if not where_expression or not column_name:
#             msg=f'no where_expression'
#             log_result_message(msg,msgType='error',level=function_level)
#             return None

#         if columnvalueFunction.upper()=='MAX':
#             column_expr=f"max({column_name})"
#             sqlCommand = f"select {column_expr} from {self.table_name} where ({where_expression});"
#         elif columnvalueFunction.upper()=='MIN':
#             column_expr=f"min({column_name})"
#             sqlCommand = f"select {column_expr} from {self.table_name} where ({where_expression});"
#         elif columnvalueFunction.upper()=='AVG':
#             column_expr=f"avg({column_name})"
#             sqlCommand = f"select {column_expr} from {self.table_name} where ({where_expression});"
#         else:
#             column_expr=f"max({column_name})"
#             sqlCommand = f"select {column_expr} from {self.table_name} where ({where_expression});"

        
#         msg = sqlCommand
#         log_result_message(msg,msgType='info',level=function_level)
#         command_description=f"get_column_value from {self.table_reference} {column_name}"
#         query_result = self.execute_query(sqlCommand,command_description, exclude_null_columns=False)
#         #column_value = query_result.fetchone()[0]
#         column_value = get_column_from_query_result(query_result, column=1)
#         msg=f"table [{self.table_reference}] column [{column_expr.upper()}]={column_value} retrieved. {self.table_reference} [{where_expression}]"
#         log_result_message(msg,msgType='ok',level=function_level)
#         return column_value
#     #::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
#     def retrieve_rows(self, where_expression, columns=None, order_by=None, rows_limit=None, exclude_null_columns=True, exclude_columns=None, user='?'):
#         command_description=f'retrieve rows {self.table_reference}'
#         if not self.table_name:
#             msg = f"table [{self.table_reference}] not in database {self.dbConnectionObj.db_engine}"
#             log_result_message(msg,msgType='error', level=function_level)
#             return {'api_status': 'error', 'api_message': msg}
#         if not where_expression or where_expression.upper() in ('ALL','*',''):
#             where_expression = '1=1'
#         if not where_expression:
#             msg = f"where exression for table [{self.table_reference}] not provided"
#             log_result_message(msg,msgType='error', level=function_level)
#             return {'api_status': 'error', 'api_message': msg}

#         if where_expression.upper() in ('ALL','*'):
#             where_expression = '1=1'

#         # json_record = {'dummy': 'foo'}
#         # result = standard_record_call_validation(self.table_reference,json_record, where_expression, user)
#         # if not result.get('api_status')=='success':
#         #     log_result_message(result.get('api_message'),msgType=result.get('api_status'),level=function_level)
#         #     return result

#         columns_expression = valid_select_columns_expression(columns, self.table_model)
#         order_by_expr = valid_orderby_expression(order_by, self.table_model)
#         sqlCommand = f"SELECT {columns_expression} FROM {self.table_name} WHERE {where_expression}"
#         if order_by_expr:
#             sqlCommand=sqlCommand+f' ORDER BY {order_by_expr}'
#         if rows_limit and str(rows_limit).isnumeric():
#             sqlCommand=sqlCommand+f' LIMIT {rows_limit}'
        
#         result = self.execute_query(sqlCommand, command_description, exclude_null_columns)
#         if not result.get('api_status') == 'success':
#             msg=f"{self.table_reference} {where_expression}"
#             log_result_message(msg, msgType='info',level=function_level)
#             msg = result.get('api_message', '?')
#             log_result_message(msg, msgType='error',level=function_level)
#             return []

#         json_records = result.get('api_data', [])
#         rowcount=len(json_records)
#         msg=f'{rowcount} row(s) retrieved from {self.table_reference}'
        
#         result.update({'api_message': msg})
        
#         log_result_message(msg,msgType='OK', level=function_level)

#         return result
#     #::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
#     #::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
#     #::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
#     # support functions
#     #::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
#     #::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
#     #::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
#     def locate_row(self, json_record, for_function=''):
#         record_locate_where_expression = self.build_WHERE_expression_from_json_record(json_record,for_function)
#         msg=f"[record-locator]:[[{record_locate_where_expression}]]"
#         log_result_message(msg,msgType='info')
#         current_record = self.retrieve_one_row(record_locate_where_expression)
#         return current_record
#     #::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
#     def insert_validation(self, json_record):
#         json_record = valid_json_record_to_table_structure(self.table_structure_dictionary, json_record)
#         json_record = normalized_json_record(json_record)
            
#         current_record = self.locate_row(json_record,'insert')
#         if current_record:
#             (row_descriptor, record_id, rowid, rowid_column) = self.current_record_standard_columns(current_record)
#             msg = f'{row_descriptor} already exists.'
#             log_result_message(msg, msgType='error',level=function_level)
#             optimized_record = optimize_record_based_on_current_record(json_record, current_record)
#             if not optimized_record:
#                 msg1=f'{row_descriptor} already exists and is synchronized.'
#                 log_result_message(msg1,msgType='warning',level=function_level)
#                 result = {'api_status': 'success', 'rowid':rowid, rowid_column: record_id, 'api_message': msg}
#                 result.update({'api_data': current_record})
#                 result.update({'row_descriptor': row_descriptor})
#                 result.update({'changed_columns': []})
#                 result.update({'changed_columns_values': []})
#                 return result
#             else:
#                 fields_delta = len(optimized_record)
#                 msg1=f'{row_descriptor} already exists with {fields_delta} fields in difference.'
#                 log_result_message(msg1,msgType='warning',level=function_level)
#                 result = {'api_status': 'success', 'rowid':rowid, rowid_column: record_id, 'api_message': msg}
#                 result.update({'api_data': current_record})
#                 result.update({'row_descriptor': row_descriptor})
#                 result.update({'changed_columns': []})
#                 result.update({'changed_columns_values': []})
#                 return result

#         row_descriptor = self.get_row_descriptor(json_record)

#         result = self.apply_table_validations(json_record, rowid=0, table_function='INSERT')
        
#         if not result.get('api_status') == 'success':
#             msg = result.get('api_message','validation errors')
#             log_result_message(msg,msgType=result.get('api_status'),level=function_level)
#             return {'api_status': 'error', 'api_message': msg}
        
#         msg = f'{row_descriptor} can be inserted.'
        
#         result = {'api_status': 'success', 'api_message': msg}
#         log_result_message(msg, msgType='OK', level=function_level)
        
#         return result
#     #::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
#     def update_validation(self, json_record, access_key=''):
#         json_record = valid_json_record_to_table_structure(self.table_structure_dictionary, json_record)
#         json_record = normalized_json_record(json_record)
                        
#         row_descriptor = self.get_row_descriptor(json_record)

#         if access_key and not access_key=='dummy':
#             current_record = self.locate_row(access_key,'update')
#             if not current_record:
#                 current_record = self.locate_row(json_record,'update')
#         else:
#             current_record = self.locate_row(json_record,'update')

#         if not current_record:
#             msg = f'{row_descriptor} record does not exists'
#             result = {'api_status': 'error', 'api_message': msg}
#             log_result_message(msg,msgType='OK',level=function_level)
#             return result
    
#         (row_descriptor, record_id, rowid, rowid_column) = self.current_record_standard_columns(current_record)
#         msg = f'{row_descriptor} already exists.'
#         log_result_message(msg, msgType='ok', level=function_level)

#         optimized_record = optimize_record_based_on_current_record(json_record, current_record)
#         if not optimized_record:
#             msg1=f'{row_descriptor} record already exists and is synchronized.'
#             log_result_message(msg1,msgType='warning',level=function_level)
#             result = {'api_status': 'success', 'rowid':rowid, rowid_column: record_id, 'api_message': msg}
#             result.update({'api_data': current_record})
#             result.update({'row_descriptor': row_descriptor})
#             result.update({'changed_columns': []})
#             result.update({'changed_columns_values': []})
#             return result

#         validation_result = self.apply_table_validations(optimized_record, rowid=rowid, table_function='UPDATE')
#         if not validation_result.get('api_status') == 'success':
#             msg = validation_result.get('api_message','validation errors')
#             log_result_message(msg, msgType='error',level=function_level)
#             return {'api_status': 'error', 'api_message': msg}
        

#         fields_delta = len(optimized_record)
#         msg1=f'{row_descriptor} record ok with {fields_delta} fields in difference.'
#         log_result_message(msg1,msgType='info',level=function_level)
#         result = {'api_status': 'success', 'rowid':rowid, rowid_column: record_id, 'api_message': msg}
#         result.update({'api_data': current_record})
#         result.update({'row_descriptor': row_descriptor})
#         result.update({'changed_columns': []})
#         result.update({'changed_columns_values': []})

#         return result
#     #::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
#     def get_record_from_access_key(self, access_key_array, exclude_null_columns=True, command_description=''):
#         if len(access_key_array)<=0:
#             msg='no access_key specified'
#             log_result_message(msg,msgType='error', level=function_level)
#             return {'api_status': 'error', 'api_message': msg}
#         if len(access_key_array) == 1:
#             rowid_column = self.rowid_column
#             original_column_name = self.table_structure_dictionary.get(rowid_column.upper(), {}).get('column_name', '')                
#             column_is_numeric=self.table_structure_dictionary.get(rowid_column.upper(), {}).get('column_is_numeric',False)                
#             if original_column_name and ((column_is_numeric and str(access_key_array[0]).isnumeric()) or not column_is_numeric):
#                 res = self.get_record_from_rowid( access_key_array[0], command_description=command_description, exclude_null_columns=exclude_null_columns)
#                 if not get_api_returned_data(res):
#                     res = self.get_record_from_unique_key( access_key_array[0], command_description=command_description, exclude_null_columns=exclude_null_columns)
#             else:
#                 res = self.get_record_from_unique_key( access_key_array[0], command_description=command_description, exclude_null_columns=exclude_null_columns)
#         else:
#             res = self.get_record_from_composite_key( access_key_array, command_description=command_description, exclude_null_columns=exclude_null_columns)

#         record = get_api_returned_data(res)
#         return record
#     #::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
#     def retrieve_one_row(self, where_expression, exclude_null_columns=True, transaction_id='?'):
#         command_description=f'retrieve_one_row({self.table_reference})'
#         if not where_expression or where_expression.upper() in ('ALL','*',''):
#             where_expression = None
#         if not where_expression:
#             msg=f'no where_exression for table [{self.table_reference}]'
#             log_result_message(msg,msgType='error', level=function_level)
#             return {}
        
#         sqlCommand = f"select ROWID as rowid,* from {self.table_name} where {where_expression}"

#         query_result = self.execute_query(sqlCommand,command_description, exclude_null_columns=exclude_null_columns)
#         rows_count = query_result.get('rows_count', 0)
#         if rows_count > 1:
#             msg=f"[{command_description}]: table [{self.table_name}] queried for 1 row but {rows_count} retrieved. query:[{where_expression}]"
#             log_result_message(msg,msgType='error', level=function_level)
#             return {}

#         json_record = get_record_from_query_result(query_result)
#         if not json_record:
#             msg=f" record not found in {self.table_reference}. ({where_expression})"
#             log_result_message(msg, msgType='warning', level=function_level)
#         else:
#             rowid = json_record.get('rowid')
#             if not rowid:
#                 rowid_column = self.rowid_column
#                 record_id = json_record.get(rowid_column)
#                 if record_id:
#                     json_record.update({'rowid':record_id})
#             row_descriptor = self.get_row_descriptor(json_record)
#             msg=f"{row_descriptor} record retrieved"
#             log_result_message(msg,msgType='OK', level=function_level)

#         return json_record
#     #::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
#     def row_exists(self, where_expression):
#         if not where_expression:
#             return False
#         command_description=f'row_exists({self.table_reference},where={where_expression})'
#         sqlCommand=f"SELECT count(*) FROM {self.table_name} WHERE {where_expression}"
#         query_result = self.execute_query(sqlCommand, command_description)
#         count = get_column_from_query_result(query_result, 1)
#         return(count)
#     #::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
#     def get_record_from_rowid(self, rowid, exclude_null_columns=True, command_description=''):
#         rowid_column = self.rowid_column
#         if not rowid_column:
#             msg=f'no rowid_column defined in database model for table [{self.table_name}]'
#             return {'api_status': 'error', 'api_message': msg}
#         if rowid == None:
#             msg=f'empty key provided for record retrieve from table [{self.table_name}] with rowid_column {rowid_column}'
#             return {'api_status': 'error', 'api_message': msg}
#         original_column_name = self.table_structure_dictionary.get(rowid_column.upper(), {}).get('column_name', '')                
#         column_is_numeric=self.table_structure_dictionary.get(rowid_column.upper(), {}).get('column_is_numeric',False)                
#         if not original_column_name:
#             msg=f'rowid_column {rowid_column} not defined in table staructure of table [{self.table_name}]'
#             return {'api_status': 'error', 'api_message': msg}
#         if column_is_numeric:
#             where_expression = f"{original_column_name}=#P1#"
#         else:
#             where_expression = f"{original_column_name}='#P1#'"
#         if column_is_numeric and not str(rowid).isnumeric():
#             msg=f'rowid {rowid_column} is numeric , key {rowid} is not'
#             return {'api_status': 'error', 'api_message': msg}
        
#         evaluated_where_expression = evaluated_expression_from_param_values(where_expression, [rowid])

#         return self.retrieve_one_row( evaluated_where_expression,exclude_null_columns=exclude_null_columns)
#     #::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
#     def get_record_from_unique_key(self, uniquecolumnValue, exclude_null_columns=True, command_description=''):
#         if not self.table_name or not uniquecolumnValue:
#             msg=f'no table [{self.table_name}]'
#             return {'api_status': 'error', 'api_message': msg}
#         rowid_column = self.rowid_column
#         flds = {}
#         unique_value_columns = self.unique_value_columns
#         for fix in range(0, len(unique_value_columns)):
#             ucolumn = unique_value_columns[fix]
#             if ucolumn.find(',') <= 0:
#                 flds.update({ucolumn:'uniqueyKey'})
#         primary_key_columns = self.primary_key_columns
#         if len(primary_key_columns) == 1:
#             flds.update({primary_key_columns[0]:'primaryKey'})
#         ucolumns=[]
#         for k in flds:
#             if not k.upper() == rowid_column.upper():
#                 original_column_name = self.table_structure_dictionary.get(k.upper(), {}).get('column_name', '')                
#                 column_is_numeric=self.table_structure_dictionary.get(k.upper(), {}).get('column_is_numeric',False)                
#                 if original_column_name:
#                     if not (column_is_numeric and not str(uniquecolumnValue).isnumeric()):
#                         ucolumns.append(k)

#         unique_value_columns = ucolumns

#         if len(unique_value_columns) <= 0:
#             msg=f'no unique_columns or primary_key defined in database model for table [{self.table_name}]'
#             return {'api_status': 'error', 'api_message': msg}

#         where_expression = self.build_OR_expression_from_columns(unique_value_columns)
#         if not where_expression:
#             msg=f'where_expression build FAILED for unique_value_columns {unique_value_columns} of table [{self.table_name}]'
#             return {'api_status': 'error', 'api_message': msg}

#         evaluated_where_expression = evaluated_expression_from_param_values(where_expression, [uniquecolumnValue])
#         if not evaluated_where_expression:
#             msg=f'evaluated expression FAILED for uniqueKeys_where_expression {where_expression} of table [{self.table_name}]'
#             return {'api_status': 'error', 'api_message': msg}
        
#         json_record = self.retrieve_one_row(evaluated_where_expression, exclude_null_columns=exclude_null_columns)
#         return json_record
#     #::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
#     def get_record_from_composite_key(self, access_key_array, exclude_null_columns=True, command_description=''):
#         if len(access_key_array) <= 1:
#             msg=f'no composite_key specified for table [{self.table_name}.upper()]'
#             return {'api_status': 'error', 'api_message': msg}

#         complex_expression=""
#         unique_value_columns = self.unique_value_columns
#         for fix in range(0, len(unique_value_columns)):
#             ucolumn = unique_value_columns[fix]
#             if ucolumn.find(',') >= 0:
#                 compokeys = ucolumn.split(',')
#                 expr=''
#                 for ix in range(0, len(compokeys)):
#                     f = compokeys[ix]
#                     original_column_name = self.table_structure_dictionary.get(f.upper(), {}).get('column_name', '')                
#                     column_is_numeric=self.table_structure_dictionary.get(f.upper(), {}).get('column_is_numeric',False)                
#                     if original_column_name:
#                         if not (column_is_numeric and not str(access_key_array[ix]).isnumeric()):
#                             if column_is_numeric:
#                                 equal = f"{original_column_name}=#P{ix+1}#"
#                             else:
#                                 equal = f"{original_column_name}='#P{ix+1}#'"
#                             if not expr:
#                                 expr = equal
#                             else:
#                                 expr = expr + ' AND ' + equal
#                 if expr:
#                     if not complex_expression:
#                         complex_expression = "("+expr+")"
#                     else:
#                         complex_expression = complex_expression + ' OR (' + expr + ")"
                
#         primary_key_columns = self.primary_key_columns
#         if len(primary_key_columns) > 1:
#             expr=''
#             for ix in range(0, len(primary_key_columns)):
#                 f = primary_key_columns[ix]
#                 original_column_name = self.table_structure_dictionary.get(f.upper(), {}).get('column_name', '')                
#                 column_is_numeric=self.table_structure_dictionary.get(f.upper(), {}).get('column_is_numeric',False)                
#                 if original_column_name:
#                     if not (column_is_numeric and not str(access_key_array[ix]).isnumeric()):
#                         if column_is_numeric:
#                             equal = f"{original_column_name}=#P{ix+1}#"
#                         else:
#                             equal = f"{original_column_name}='#P{ix+1}#'"
#                         if not expr:
#                             expr = equal
#                         else:
#                             expr = expr + ' AND ' + equal
#             if expr:
#                 if not complex_expression:
#                     complex_expression = "("+expr+")"
#                 else:
#                     complex_expression = complex_expression + ' OR (' + expr + ")"
        
#         where_expression = complex_expression
#         if not where_expression:
#             msg=f'where_expression build FAILED for composite_keys of table [{self.table_name}]'
#             return {'api_status': 'error', 'api_message': msg}

#         evaluated_where_expression = evaluated_expression_from_param_values(where_expression, access_key_array)
#         if not evaluated_where_expression:
#             msg=f'evaluated expression FAILED for uniqueKeys_where_expression {where_expression} of table [{self.table_name}]'
#             return {'api_status': 'error', 'api_message': msg}
        
#         json_record = self.retrieve_one_row(evaluated_where_expression, exclude_null_columns=exclude_null_columns)
#         return json_record
#     #::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
#     def exec_after_insert_triggers(self, rowid, inserted_record={}):
#         command_description=f'exec_after_insert_triggers({self.table_reference}, rowid=[{rowid}]'
#         if not rowid:
#             msg=f'no rowid for table [{self.table_reference}]'
#             log_result_message(msg, msgType='error',level=function_level)
#             return
#         after_insert_sqlCommands = self.after_insert_sqlCommands
#         for ix in range(0, len(after_insert_sqlCommands)):
#             sqlCommand = after_insert_sqlCommands[ix]
#             log_result_message(sqlCommand, msgType='info',level=function_level)

#             sqlCommand = evaluated_expression_from_record(sqlCommand, json_record=inserted_record, rowid=rowid)
        
#             exec_result = self.execute_query(sqlCommand, command_description)
#             if not exec_result.get('api_status') == 'success':
#                 log_result_message(exec_result.get('api_message', '?'), msgType=exec_result.get('api_status'),level=function_level)
#             else:
#                 log_result_message(exec_result.get('api_message', '?'), msgType=exec_result.get('api_status'),level=function_level)
#     #::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
#     def exec_after_update_triggers(self, rowid, updated_record={}):
#         command_description=f'exec_after_update_triggers({self.table_reference}, rowid=[{rowid})'
#         if not rowid:
#             msg=f'no rowid for table [{self.table_reference}]'
#             log_result_message(msg, msgType='error',level=function_level)
#             return
#         after_update_sqlCommands = self.after_update_commands
#         for ix in range(0, len(after_update_sqlCommands)):
#             sqlCommand = after_update_sqlCommands[ix]
#             log_result_message(sqlCommand, msgType='info',level=function_level)

#             sqlCommand = evaluated_expression_from_record(sqlCommand, json_record=updated_record, rowid=rowid)
#             log_result_message(sqlCommand, msgType='info', level=function_level)
        
#             exec_result = self.execute_query(sqlCommand, command_description)
#             if not exec_result.get('api_status') == 'success':
#                 log_result_message(exec_result.get('api_message', '?'), msgType=exec_result.get('api_status'),level=function_level)
#             else:
#                 log_result_message(exec_result.get('api_message', '?'), msgType=exec_result.get('api_status'),level=function_level)
#     #::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
#     def apply_table_validations(self, json_record, rowid=0, table_function='insert'):
#         if not json_record:
#             msg = f"record for table [{self.table_reference}] not provided"
#             log_result_message(msg, msgType='error', level=function_level)
#             return {'api_status': 'error', 'api_message': msg}
#         if type(json_record) != type({}):
#             msg = f"record for table [{self.table_reference}] is not in JSON format"
#             log_result_message(msg, msgType='error', level=function_level)
#             return {'api_status': 'error', 'api_message': msg}

#         json_record = valid_json_record_to_table_structure(self.table_structure_dictionary, json_record)
#         json_record = normalized_json_record(json_record)
                
#         if table_function.upper()=='INSERT':
#             mandatory_columns = self.mandatory_columns
#             row_descriptor = self.get_row_descriptor(json_record)

#             missing_columns=get_missing_columns_from_json_record(mandatory_columns,json_record)
#             if missing_columns:
#                 msg = f"{missing_columns} not provided for {row_descriptor} {table_function}"
#                 log_result_message(msg, msgType='error', level=function_level)
#                 return {'api_status': 'error', 'api_message': msg}

#         validation_result = self.exec_uniqueness_validation_rules(json_record=json_record, rowid=rowid)
#         if not validation_result.get('api_status') == 'success':
#             msg = validation_result.get('api_message','uniqueness validation errors')
#             log_result_message(msg, msgType='error', level=function_level)
#             return {'api_status': 'error', 'api_message': msg}

#         msg=f"validations for table [{self.table_reference}] passed."
#         log_result_message(msg, msgType='OK',level=function_level)

#         return {'api_status': 'success', 'api_message': msg}
#     #::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
#     def apply_default_values(self, json_record={},table_function=''):
#         if table_function.upper()=='INSERT':
#             default_values = self.table_model.get('default_values', {})
#             ix=0
#             for k in default_values:
#                 expr=default_values.get(k,'')
#                 column_name = self.table_model.get('columns', {}).get(k.upper(), {}).get('column_name')
#                 if column_name and expr:
#                     ix=ix+1
#                     calculated_field_value_expression = evaluated_expression_from_record(expr, json_record, rowid=0).strip()
#                     if calculated_field_value_expression.upper().find('SELECT ') >= 0 and calculated_field_value_expression.upper().find(' FROM ') >= 0:
#                         calculated_field_value_expression = calculated_field_value_expression.strip()
#                         if not (calculated_field_value_expression[0] == '(' and calculated_field_value_expression[-1] == ')'):
#                             calculated_field_value_expression = f"({calculated_field_value_expression})"
#                         calculated_field_value_expression = f"#SQL:{calculated_field_value_expression}"
#                     json_record.update({column_name: calculated_field_value_expression})
#                     msg=f"{ix}. default for column [{column_name}] --> [[{calculated_field_value_expression}]]"
#                     log_result_message(msg, msgType='info')
#         return json_record
#     #::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
#     def exec_uniqueness_validation_rules(self, json_record={}, rowid=0):
#         command_description=f'exec_uniqueness_validation_rules({self.table_reference}, rowid=[{rowid})'
#         if not rowid:
#             rowid = 0
#         unique_key_validations = self.unique_key_validations
#         column_names=[]
#         for column_name in unique_key_validations:
#             val=str(json_record.get(column_name))
#             column_names.append(column_name.upper())
#             sqlCommand = unique_key_validations.get(column_name)
#             log_result_message(sqlCommand,msgType='info',level=function_level)

#             sqlCommand = sqlCommand.replace('#ROWID#', str(rowid))
#             log_result_message(sqlCommand,msgType='info',level=function_level)
#             sqlCommand = processed_string_from_json_record(sqlCommand, json_record)
#             if sqlCommand.find('#') >= 0:
#                 #sqlCommand = processed_string_from_table_structure(sqlCommand, self.table_structure_dictionary)
#                 msg = f"[{column_name}]=[[{val}]] is not in json_record for table [{self.reference}]"
#                 #log_message(msg,msgType='warning',level=function_level)
#             else:
#                 # print(sqlCommand)
#                 log_result_message(sqlCommand,msgType='info',level=function_level)
#                 exec_result = self.execute_query(sqlCommand, command_description)
#                 msg = exec_result.get('api_message', '?')
#                 if not exec_result.get('api_status') == 'success':
#                     msg=f"{column_name}={val} is NOT unique in table {self.table_name}.upper(). exists x times"
#                     log_result_message(msg,msgType='error',level=function_level)
#                     return {'api_status':'error','api_message':msg}
#                 else:
#                     count = exec_result.get('api_data', [{}])[0].get('count', 1)
#                     if count==0:
#                         msg = f"{column_name}={val} is unique in table {self.table_reference}. (count={count})"
#                         log_result_message(msg,msgType='info',level=function_level)
#                     else:
#                         msg=f"{column_name}={val} is NOT unique in table {self.table_reference}. exists {count} times"
#                         log_result_message(msg,msgType='error',level=function_level)
#                         return {'api_status':'error','api_message':msg}

#         msg=f"columns [{column_names}] are unique in table {self.table_name}.upper()"
#         log_result_message(msg,msgType='ok',level=function_level)
#         return {'api_status':'success','api_message':msg}    
#     #::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
#     #::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
#     #::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
#     # metadata functions
#     #::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
#     #::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
#     #::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
#     def model(self):
#         return self.table_model
#     #::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
#     #::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
#     #::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
#     # table system functions
#     #::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
#     #::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
#     #::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
#     def table_structure(self):
#         return get_table_structure(self.dbConnectionObj, self.table_name)
#     #::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
#     def table_exists(self):
#         return table_exists_in_database(self.dbConnectionObj, self.table_name)
#     #::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
#     def table_rows(self):
#         return get_table_rowsCount(self.dbConnectionObj, self.table_name)
#     #::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
#     def table_drop(self):
#         return drop_table(self.dbConnectionObj, self.table_name)
#     #::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
#     def copy_table_records_to(self, to_table_name):
#         return copy_table_records(self.dbConnectionObj, self.table_name, to_table_name)
#     #::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
#     def copy_table_to(self, to_table_name):
#         return make_a_table_copy(self.dbConnectionObj, self.table_name,to_table_name)
#     #::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
#     def create(self, force_recreate=False, copy_records=True):
#         create_commands = self.create_table_commands
#         if not create_commands:
#             return {'api_status':'error','api_message':f'invalid model generated for [{self.table_reference}]. no create_table_commands.'}
#         return create_table(self.dbConnectionObj,self.table_name,create_commands, force_recreate=force_recreate, copy_records=copy_records)
#     #::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
#     def recreate(self, force_recreate=False, copy_records=True):
#         create_commands = self.create_table_commands
#         if not create_commands:
#             return {'api_status':'error','api_message':f'invalid model generated for [{self.table_reference}]. no create_table_commands.'}
#         return recreate_table(self.dbConnectionObj,self.table_name,create_commands, force_recreate=force_recreate, copy_records=copy_records)
#     #::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
#     def clear_table(self, user='?'):
#         where_expression='ALL'
#         result = self.table_records_delete(where_expression,user=user)
#         return result
#     #::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
#     def display_table_structure_summary(self=''):
#         self.dbms.display_table_structure_summary(self.schema_name,self.table_name, user=self.user)        
#     #::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
    def display_summary(self, where_expression=None, order_by=None, rows_limit=None, include_columns=None, exclude_columns=[], output_method='GRID', format_methods='name,max_length=20,line_length=120', title=''):
        import plotly.graph_objects as go

        
        query = self.session.query(self.model)
        query_rows = query.count()

        header=[]
        data=[]
        for column in self.model.__table__.columns:
            header.append(column.name)
            data.append([])

        for row in query.all():
            row_values = []
            ix=-1
            for c in inspect(self.model).mapper.column_attrs:
                ix=ix+1
                val = str(getattr(row, c.key))
                data[ix].append(val)
                #row_values.append(str(getattr(row, c.key)))
            #data.append(row_values)
        
        # print(data)

        # columns = self.model.__table__.columns.keys()
        # fig = go.Figure(data=[go.Table(header=dict(values=['A Scores', 'B Scores']),
        #          cells=dict(values=[[100, 90, 80, 90], [95, 85, 75, 95]]))
        #              ])
        # fig.show()

        fig = go.Figure(data=[go.Table(header=dict(values=header),
                 cells=dict(values=data))
                     ])
        fig.show()

        # fig = go.Figure(data=[go.Table(
        #         header=dict(values=header,
        #                     line_color='darkslategray',
        #                     fill_color='lightskyblue',
        #                     align='left'),
        #         cells=dict(values=data, 
        #                 line_color='darkslategray',
        #                 fill_color='lightcyan',
        #                 align='left'))
        #     ])

        # fig.update_layout(width=500, height=300)
        # fig.show()

#     def display_summary(self, where_expression=None, order_by=None, rows_limit=None, include_columns=None, exclude_columns=[], output_method='GRID', format_methods='name,max_length=20,line_length=120', title=''):
#         if not output_method:
#             output_method = 'GRID' # 'HTML' 'JSON' 'SDF' 'XLS' 'XML'

#         if not where_expression:
#             where_expression='1=1'
#         if where_expression.upper() in ('ALL','*'):
#             where_expression = '1=1'
#         columns = self.get_important_columns()
#         if include_columns:
#             if type(include_columns) == type(''):
#                 if include_columns == '*' or include_columns.upper() == 'ALL':
#                     include_columns=[]
#                     allcolumns = self.table_model.get('columns', {})
#                     for k in allcolumns:
#                         c=allcolumns.get(k.upper(), {}).get('column_name')
#                         include_columns.append(c)
#                 else:
#                     x = include_columns
#                     include_columns = x.split(',')
#             for f in include_columns:
#                 column_name = valid_column_in_table_model(f.upper(), self.table_model)
#                 if column_name not in columns:
#                     columns.append(column_name)
        
#         columns = select_columns_excluding_columns(columns, exclude_columns, self.table_model)
#         xcolumns = columns.copy
    
#         result = self.retrieve_rows(where_expression, columns=xcolumns, order_by=order_by, rows_limit=rows_limit)
#         json_records = result.get('api_data', [])

#         line_length = get_parameter_value_from_string(format_methods, 'line_length', default=150, as_numeric=True)
#         rowsCount = get_table_rowsCount(self.dbConnectionObj, self.table_name)
#         if title == None:
#            title = ''
#         else:
#             if not title:
#                 title = f'{self.table_reference} table summary'
#         title=title.replace('#ROWCOUNT#',str(rowsCount))
#         title=title.replace('#TABLE_NAME#',self.table_name)
#         title=title.replace('#TABLE_ALIAS#',self.table_alias)
#         title=title.replace('#TABLE_ENTITY#',self.table_entity)
#         title=title.replace('#TABLE_SCHEMA#',self.schema_name)
#         title=title.replace('#TABLE_REFERENCE#',self.table_reference)

#         grid_lines_array = self.format_json_records_as(format_type=output_method,json_records=json_records,columns=columns,format_methods=format_methods,title=title)

#         # if title:
#         #     title_line = f"|{title}|"
#         #     if len(title_line) < line_length:
#         #         title_line = title_line + ' '*(line_length - len(title_line) - 1) + '|'
#         #     else:
#         #         title_line = title_line[0:line_length - 1] + '|'
#         #     if not format_methods:
#         #         format_methods = 'TITLE'
#         #     else:
#         #         format_methods = 'TITLE ' + format_methods
#         # else:        
#         #     if not format_methods:
#         #         format_methods = 'NAME, max_length=20, line_length=120'
#         #     if format_methods.upper().find('LINE_LENGTH')<=0:
#         #         format_methods = format_methods+', line_length=120'
#         #     format_methods = format_methods.upper().replace('TITLE', '')

                    
#         # top_grid_line = grid_lines_array[0]
#         # new_top_grid_line=""
#         # title_line_x=""
#         # for ix in range(1, len(title_line)-1):
#         #     if title_line[ix] == '|':
#         #         title_line_x = title_line_x + title_line[ix]
#         #     else:
#         #         title_line_x = title_line_x + '-'
#         #     if title_line[ix] == '|':
#         #         if top_grid_line[ix] == ascii_char(196):
#         #             new_top_grid_line = new_top_grid_line + ascii_char(193)
#         #         else:
#         #             new_top_grid_line = new_top_grid_line + ascii_char(197)
#         #     else:
#         #         if top_grid_line[ix] == ascii_char(196):
#         #             new_top_grid_line = new_top_grid_line + top_grid_line[ix]
#         #         else:
#         #             new_top_grid_line = new_top_grid_line + ascii_char(194)

#         # new_top_grid_line=top_grid_line[0]+new_top_grid_line+top_grid_line[-1]
#         # title_line_x=title_line[0]+title_line_x+title_line[-1]

#         # grid_lines_array[0]=new_top_grid_line

                
#         # title_line_1 = title_line_x
#         # title_line_2 = title_line
#         # title_line_3 = title_line_x         

#         # title_line_1 = format_ascii_line(title_line_1, 'TOP')
#         # title_line_2 = format_ascii_line(title_line_2, 'DETAIL')
#         # title_line_3 = format_ascii_line(title_line_3, 'MIDDLE')
        
#         # # title_line_len=len(title_line_2)
#         # # if title_line_len > grid_line_length:
#         # #     more_spaces = ' '*(grid_line_length - len(title_line) - 1)
#         # #     new_column = more_spaces + '|'

        
#         # print(title_line_1[0:line_length])
#         # print(title_line_2[0:line_length])
#         # #print(title_line_3[0:line_length])

#         # #print(where_line[0:line_length])
#         print(f"{thisApp.Fore.RESET}{thisApp.Back.RESET}{thisApp.Style.RESET_ALL}")
#         for line in grid_lines_array:
#             print(f"{thisApp.Fore.WHITE}{thisApp.Back.LIGHTBLACK_EX}",line[0:line_length],f"{thisApp.Fore.RESET}{thisApp.Back.RESET}")
#         print(f"{thisApp.Fore.RESET}{thisApp.Back.RESET}{thisApp.Style.RESET_ALL}")
#         return
#     #::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
#     def print_all_data(self, query=''):
#             query = query if query != '' else f"SELECT ROWID as rowid,* FROM '{self.table_name}';"
#             with self.db_engine.db_engine.connect() as connection:
#                 try:
#                     result = connection.execute(query)
#                 except Exception as e:
#                     print(e)
#                 else:
#                     for row in result:
#                         print(row) # print(row[0], row[1], row[2])
#                     result.close()
#             print("\n")
#     #::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
#     def reorganize(self):
#         return table_reorganization(self)
#     #::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
#     #::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
#     #::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
#     #::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
#     # sql commands utilities
#     #::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
#     #::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
#     #::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
#     def row_insert_sqlCommand(self, json_record):
#         if not json_record or not type(json_record) == type({}):
#             return ''
#         columns=''
#         values=''
#         for k in json_record:
#             column_name = self.table_structure_dictionary.get(k.upper(), {}).get('column_name', '')
#             if not column_name:
#                 msg=f"[[column]] [[[{k}]]] removed from INSERT in [{self.reference}]. not exists in table structure"
#                 log_result_message(msg, msgType='warning', level=function_level)
#                 continue
#             column_value = json_record.get(column_name)
#             if column_value == None:
#                 msg=f"[[column]] [[[{column_name}]]] removed from INSERT in [{self.reference}]. [[[[None]]]] value specified"
#                 log_result_message(msg, msgType='warning', level=function_level)
#                 continue
#             value = field_value_for_sql(self, column_name, column_value)
#             if not value:
#                 msg=f"[[column]] [[[{column_name}]]] removed from INSERT in [{self.reference}]. [[[[ivalid value specified]]]]"
#                 log_result_message(msg, msgType='warning', level=function_level)
#                 continue

#             if not columns:
#                 columns = column_name
#             else:
#                 columns = columns + ", " + column_name

#             if not values:
#                 values = value
#             else:
#                 values = values + ", " + value

#         sqlCommand = f"INSERT INTO {self.table_name} ({columns}) VALUES ({values});"

#         return sqlCommand
#     #::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
#     def row_update_sqlCommand(self, where_expression,json_record):
#         if not where_expression:
#             return ""
#         if where_expression.upper() in ('ALL','*'):
#             where_expression = '1=1'
#         if not json_record or not type(json_record) == type({}):
#             return ""
#         update_expression=''
#         for k in json_record:
#             column_name = self.table_structure_dictionary.get(k.upper(), {}).get('column_name', '')
#             if not column_name:
#                 msg=f"[[column]] [[[{k}]]] removed from UPDATE of [{self.reference}]. not exists in table structure"
#                 log_result_message(msg, msgType='warning', level=function_level)
#                 continue
#             column_value = json_record.get(column_name)
#             if column_value == None:
#                 msg=f"[[column]] [[[{column_name}]]] removed from UPDATE of  [{self.reference}]. [[[[None]]]] value specified"
#                 log_result_message(msg, msgType='warning', level=function_level)
#                 continue
#             value = field_value_for_sql(self, column_name, column_value)
#             if not value:
#                 msg=f"[[column]] [[[{column_name}]]] removed from UPDATE of  [{self.reference}]. [[[[ivalid value specified]]]]"
#                 log_result_message(msg, msgType='warning', level=function_level)
#                 continue


#             equal_expression=f"{column_name} = {value}"

#             if not update_expression:
#                 update_expression = equal_expression
#             else:
#                 update_expression = update_expression + ", " + equal_expression

#         if not update_expression:
#             return ''

#         sqlCommand = f"UPDATE {self.table_name} SET {update_expression} WHERE {where_expression};"

#         return sqlCommand
#     #::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
#     def row_delete_sqlCommand(self, where_expression=''):
#         if not where_expression:
#             return ""
#         if where_expression.upper() in ('ALL','*'):
#             where_expression = '1=1'
#         sqlCommand = f"DELETE FROM {self.table_name} WHERE {where_expression};"
#         return sqlCommand
#     #::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
#     def row_retrieve_sqlCommand(self,where_expression=''):
#         if not where_expression:
#             return ""
#         if where_expression.upper() in ('ALL','*'):
#             where_expression = '1=1'
#         sqlCommand = f"SELECT ROWID,* FROM {self.table_name} WHERE {where_expression};"
#         return sqlCommand
#     #::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
#     #::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
#     #::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
#     def AND_where_expression_from_jsonRecord(self, where_columns, json_record):
#         if not json_record or not type(json_record) == type({}):
#             return None
#         where_expression=''
#         for f in where_columns:
#             original_column_name = self.table_structure_dictionary.get(f.upper(), {}).get('column_name', '')                
#             data_type = self.table_structure_dictionary.get(f.upper(), {}).get('type', '')
#             if original_column_name:
#                 v = json_record.get(f)  #tispaolas
#                 if not data_type_is_numeric(data_type):
#                     equal_expression = f"{original_column_name} = '{v}'"
#                 else:
#                     equal_expression = f"{original_column_name} = '{v}'"
#                 if not where_expression:
#                     where_expression=equal_expression
#                 else:
#                     where_expression = where_expression + " AND " + equal_expression
#         return where_expression    
#     #::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
#     def OR_where_expression_from_jsonRecord(self, where_columns, json_record):
#         if not json_record or not type(json_record) == type({}):
#             return None
#         where_expression=''
#         for f in where_columns:
#             original_column_name = self.table_structure_dictionary.get(f.upper(), {}).get('column_name', '')                
#             #data_type = self.table_structure_dictionary.get(f.upper(), {}).get('type', '')
#             if original_column_name:
#                 v = json_record.get(f)#tispaolas
#                 equal_expression = f"{original_column_name} = '{v}'"
#                 if not where_expression:
#                     where_expression=equal_expression
#                 else:
#                     where_expression = where_expression + " OR " + equal_expression
#             else:
#                 ffs = f.split(',')
#                 w=''
#                 for ix in range(0, len(ffs)):
#                     f1 = ffs[ix].strip()
#                     if not w:
#                         w = f1
#                     else:
#                         w = w + ' AND ' + f1
#                 if w:
#                     w = f"({w})"
#                     if not where_expression:
#                         where_expression=w
#                     else:
#                         where_expression = where_expression + " OR " + w
#         return where_expression    
#     #::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
#     def build_OR_expression_from_columns(self,columns):
#         where_expression = ""
#         ix = 0
#         for f in columns:
#             ix = ix + 1
#             param = f"#P1#" #always 1 param
#             original_column_name = self.table_structure_dictionary.get(f.upper(), {}).get('column_name', '')                
#             if original_column_name:
#                 column_is_numeric=self.table_structure_dictionary.get(f.upper(), {}).get('column_is_numeric',False)                
#                 if column_is_numeric:
#                     columnequal_expression = f"{original_column_name} = {param}"
#                 else:
#                     columnequal_expression = f"{original_column_name} = '{param}'"
#                 if not where_expression:
#                     where_expression = columnequal_expression
#                 else:
#                     where_expression = where_expression + " OR " + columnequal_expression
#         return where_expression
#     #::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
#     def build_WHERE_expression_from_json_record(self, json_record,for_function=''):
#         if not json_record:
#             msg='no access_key or json_record specified'
#             log_result_message(msg,msgType='error', level=function_level)
#             return None
        
#         if type(json_record) == type({}):
#             if for_function.upper().find('INSERT') < 0:
#                 record_locate_expression = self.record_locate_expression_from_rowid
#                 if record_locate_expression:
#                     record_locate_where_expression = evaluated_expression_from_record(record_locate_expression, json_record, rowid=0)
#                     if record_locate_where_expression.find('#') < 0:
#                         return record_locate_where_expression
#                 # rowid_column=self.rowid_column
#                 # v = json_record.get(rowid_column)
#                 # if v:
#                 #     columns = self.table_model.get('columns', {})
#                 #     data_type = columns.get(rowid_column.upper(), {}).get('column_data_type')
#                 #     column_is_numeric = data_type_is_numeric(data_type)
#                 #     if column_is_numeric:
#                 #         record_locate_where_expression = f"{rowid_column}={v}"
#                 #     else:
#                 #         record_locate_where_expression = f"{rowid_column}='{v}'"
#                     # return record_locate_where_expression                  

#             if self.primary_key_columns or self.unique_value_columns:
#                 record_locate_expression = self.record_locate_expression
#                 record_locate_where_expression = evaluated_expression_from_record(record_locate_expression, json_record, rowid=0)
#                 if record_locate_where_expression.find('#') < 0:
#                     return record_locate_where_expression
#                 if self.primary_key_columns:
#                     record_locate_expression = self.record_locate_expression_from_PK
#                     record_locate_where_expression = evaluated_expression_from_record(record_locate_expression, json_record, rowid=0)
#                     if record_locate_where_expression.find('#') < 0:
#                         return record_locate_where_expression
#                 if self.unique_value_columns:
#                     record_locate_expression = self.record_locate_expression_from_UK
#                     record_locate_where_expression = evaluated_expression_from_record(record_locate_expression, json_record, rowid=0)
#                     if record_locate_where_expression.find('#') < 0:
#                         return record_locate_where_expression

#                 if for_function.upper().find('INSERT') >=0 or for_function.upper().find('UPDATE') >=0 or for_function.upper().find('DELETE') >=0:
#                     record_locate_where_expression = processed_string_from_table_structure(record_locate_where_expression, self.table_structure_dictionary)
#                     if record_locate_where_expression.find('#') < 0:
#                         return record_locate_where_expression

#             e = self.build_GENERIC_WHERE_expression_from_json_record(json_record)
#             # columns = self.table_model.get('columns', {})
#             # for k in json_record:
#             #     v = json_record.get(k)
#             #     c = columns.get(k.upper(), {}).get('column_name')
#             #     data_type = columns.get(k.upper(), {}).get('column_data_type')
#             #     column_is_numeric = data_type_is_numeric(data_type)
#             #     if c:
#             #         if column_is_numeric:
#             #             v = f"{v}"
#             #         else:
#             #             v = f"'{v}'"
#             #         if not e:
#             #             e = f"{c}={v}"
#             #         else:
#             #             e = e + ' AND ' + f"{c}={v}"
#             return e                    

#         #locate from string or array            
#         if not type(json_record) == type([]):
#             access_key_array = str(json_record).split(',')
#         else:
#             access_key_array = json_record

#         record_locate_where_expression = select_expression_from_values(access_key_array,self.table_model)
#         if not record_locate_where_expression:
#             return None
#         return record_locate_where_expression
#     #::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
#     def build_GENERIC_WHERE_expression_from_json_record(self, json_record):
#         e=''
#         for k in json_record:
#             v = json_record.get(k)
#             c = self.columns.get(k.upper(), {}).get('column_name')
#             #column_is_numeric = self.columns.get(k.upper(), {}).get('column_is_numeric',False)
#             column_is_numeric=self.table_structure_dictionary.get(k.upper(), {}).get('column_is_numeric',False)                
#             if c:
#                 if column_is_numeric:
#                     v = f"{v}"
#                 else:
#                     v = f"'{v}'"
#                 if not e:
#                     e = f"{c}={v}"
#                 else:
#                     e = e + ' AND ' + f"{c}={v}"
#         return e                    
#     #::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
#     def select_expression_from_values(self,access_key_array):
#         number_of_values=len(access_key_array)
#         e1 = ''
#         e2 = ''
#         e3 = ''
#         and_expression = ''
#         and_count = 0
#         is_invalid=False
#         for fs in self.unique_value_columns:
#             if fs:
#                 ffs = fs.split(',')
#                 equal_expression = ''
#                 if len(ffs) == number_of_values:
#                     and_count = and_count + 1
#                     for ix in range(0,len(ffs)):
#                         f = ffs[ix]
#                         #data_type=self.columns.get(f.upper()).get('column_data_type','VARCHAR')
#                         column_name = self.columns.get(f.upper()).get('column_name')
#                         val = str(access_key_array[ix])
#                         val_is_numeric = val.isnumeric()
#                         if not self.columns.get(f.upper()).get('column_is_numeric',False):
#                             fexpression = f"{column_name}='{val}'"
#                         else:
#                             if val_is_numeric:
#                                 fexpression = f"{column_name}={val}"
#                         if fexpression:
#                             if not equal_expression:
#                                 equal_expression = fexpression
#                             else:
#                                 equal_expression = equal_expression + ' AND ' + fexpression
#                         else:
#                             is_invalid = True
#                     if len(ffs) > 1:
#                         equal_expression = f'({equal_expression})'
#                     if not is_invalid:
#                         if not and_expression:
#                             and_expression=equal_expression
#                         else:
#                             and_expression = and_expression + " OR " + equal_expression
#         if and_count > 1:
#             e1 = f'({and_expression})'
#         if and_count > 0:
#             e1 = and_expression

#         if len(self.primary_key_columns) == number_of_values:
#             and_count = 0
#             equal_expression=''
#             for ix in range(0,len(self.primary_key_columns)):
#                 f = self.primary_key_columns[ix]
#                 #data_type=self.columns.get(f.upper()).get('column_data_type','VARCHAR')
#                 column_name = self.columns.get(f.upper()).get('column_name')
#                 if column_name:
#                     and_count = and_count + 1
#                     val = str(access_key_array[ix])
#                     val_is_numeric = val.isnumeric()
#                     fexpression=''
#                     if not self.columns.get(f.upper()).get('column_is_numeric',False):
#                         fexpression = f"{column_name}='{val}'"
#                     else:
#                         if val_is_numeric:
#                             fexpression = f"{column_name}={val}"
#                     if fexpression:
#                         if not equal_expression:
#                             equal_expression = fexpression
#                         else:
#                             equal_expression = equal_expression + ' AND ' + fexpression
#             if and_count > 1:
#                 equal_expression = f'({equal_expression})'
#             if and_count > 0:
#                 e2 = equal_expression

#         if number_of_values==1:
#             # data_type=self.columns.get(self.rowid_column.upper(),{}).get('column_data_type','VARCHAR')
#             column_name = self.columns.get(self.rowid_column.upper()).get('column_name')
#             val = str(access_key_array[0])
#             val_is_numeric = val.isnumeric()
#             fexpression=''
#             if column_name:
#                 if not self.columns.get(self.rowid_column.upper()).get('column_is_numeric',False):
#                     fexpression = f"{column_name}='{val}'"
#                 else:
#                     if val_is_numeric:
#                         fexpression = f"{column_name}={val}"
#                 if fexpression:
#                     e3 = fexpression

#         e_merged=[]
#         if e1:
#             e_merged.append(e1)
#         if e2:
#             e_merged.append(e2)
#         if e3:
#             e_merged.append(e3)
#         e = OR_expression(e_merged)

#         return e
#     #::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
#     def get_important_columns(self):
#         unique_value_columns = self.unique_value_columns
#         rowid_column = self.table_model.get('rowid_column', '')
#         primary_key_columns = self.primary_key_columns
#         mandatory_columns = self.mandatory_columns
#         auto_updated_columns = self.auto_updated_columns #is a {}
#         uk_columns={}
#         for f in mandatory_columns:
#             uk_columns.update({f: 'mandatory'})
#         if rowid_column:
#             uk_columns.update({rowid_column: 'rowid_column'})
#         for f in unique_value_columns:
#             uk_columns.update({f: 'uid_column'})
#         for f in primary_key_columns:
#             uk_columns.update({f: 'pk_column'})
#         for f in auto_updated_columns:
#             uk_columns.update({f: 'auto_updated_column'})

#         uk2_columns={}
#         for f in uk_columns:
#             origcolumnName = valid_column_in_table_model(f.upper(), self.table_model)
#             uk2_columns.update({origcolumnName: 'important'})

#         important_columns=[]
#         for f in uk2_columns:
#             origcolumnName = valid_column_in_table_model(f.upper(), self.table_model)
#             if origcolumnName:
#                 important_columns.append(origcolumnName)

#         return important_columns        
#     #::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
#     def get_row_descriptor(self, json_record={},rowid=0):
#         row_descriptor_expression = self.row_descriptor_expression
#         row_descriptor = evaluated_expression_from_record(row_descriptor_expression, json_record, rowid)
#         if row_descriptor.find('#') >= 0:
#             row_descriptor_expression = self.row_descriptor_expression2
#             row_descriptor = evaluated_expression_from_record(row_descriptor_expression, json_record, rowid)
#             if row_descriptor.find('#') >= 0:
#                 if type(json_record) == type(''):
#                     row_descriptor = self.table_entity + ':' + json_record
#                 elif type(json_record) == type({}):
#                     row_descriptor = self.table_entity + ':' + json.dumps(json_record)
#                 elif type(json_record) == type([]):
#                     row_descriptor = self.table_entity + ':'
#                     for k in json_record:
#                         if type(k) == type(''):
#                             row_descriptor = row_descriptor + k + '|'
#                         elif type(k) == type({}):
#                             row_descriptor = row_descriptor + json.dumps(k) + '|'
#         row_descriptor=f"[{row_descriptor}]"
#         return row_descriptor
#     #::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
#     def rowid_where_expression(self, current_record):
#         where_expression = ''
#         if not current_record:
#             return None
#         if current_record:
#             #rowid_column = self.rowid_column
#             record_id=current_record.get(self.rowid_column)
#             if record_id:
#                 column_is_numeric=self.table_structure_dictionary.get(self.rowid_column.upper(), {}).get('column_is_numeric',False)
#                 # columns = self.table_model.get('columns', {})
#                 # data_type = columns.get(rowid_column.upper(), {}).get('column_data_type')
#                 # column_is_numeric = data_type_is_numeric(data_type)
#                 if column_is_numeric:
#                     where_expression = f"{self.rowid_column}={record_id}"
#                 else:
#                     where_expression = f"{self.rowid_column}='{record_id}'"
#             else:
#                 rowid = current_record.get('rowid')
#                 if rowid:
#                     where_expression=f'ROWID={rowid}'
#                 else:
#                     msg=f'database integrity error. rowid or record_id not identified in record'                
#                     log_result_message(msg,msgType='error')
#                     return None
#         return where_expression
#     #::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
#     def current_record_standard_columns(self, current_record):
#         rowid_column = self.rowid_column
#         record_id=None
#         if rowid_column:
#             record_id=current_record.get(rowid_column)
#         rowid = current_record.get('rowid',0)
#         if record_id:
#             rowuid = record_id
#         else:
#             rowuid = rowid
#         row_descriptor = self.get_row_descriptor( current_record, rowuid)
#         return (row_descriptor, record_id, rowid, rowid_column)
#     #::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
#     def format_json_records_as(self,format_type,json_records,columns=[],format_methods='',title=''):
#         if format_type.upper().find('HTML') >= 0:
#             return self.format_json_records_as_html(json_records,columns,format_methods,title)
#         elif format_type.upper().find('GRID')>=0:
#             return self.format_json_records_as_text_grid(json_records,columns,format_methods,title)
#         elif format_type.upper().find('FIX') >= 0 and format_type.upper().find('REC') >= 0:
#             return self.format_json_records_as_fixed_length_record(json_records,columns,format_methods,title)
#         elif format_type.upper() in ('SDF','XLS'):
#             return self.format_json_records_as_sdf(json_records,columns,format_methods,title)
#         else: #json
#             return json_records
#     #::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
#     def format_json_records_as_text_grid(self, json_records, columns=[], format_methods='',title='',title_color='',bgColor='',color1='',color2='',color3=''):
#         #line_length = get_parameter_value_from_string(format_methods, 'line_length', default=150, as_numeric=True)
        
#         output=[]
#         ordered_selected_columns_list=[]
#         if columns:
#             ordered_columns_list = self.ordered_columns_list
#             for c in ordered_columns_list:
#                 if c.upper() in map(str.upper,columns):
#                     ordered_selected_columns_list.append(c)
#         else:
#             columns_in_json={}
#             for ix in range(0, len(json_records)):
#                 json_rec = json_records[ix]
#                 for f in json_rec:
#                     columns_in_json.update({f: 'in_json_rec'})
#                 if ix > 99:
#                     break
#             ordered_columns_list = self.ordered_columns_list
#             for c in ordered_columns_list:
#                 if c.upper() in map(str.upper,columns_in_json):
#                     ordered_selected_columns_list.append(c)
#         #column_values len
#         ordered_selected_columns_list_lengths = []
#         lengths={}
#         for ix in range(0, len(json_records)):
#             json_rec = json_records[ix]
#             for f in json_rec:
#                 v = json_rec.get(f)
#                 vlen = len(str(v))
#                 max_length = lengths.get(f.upper(), {}).get('max_len', 0)
#                 if vlen > max_length:
#                     lengths.update({f.upper(): {'max_len': vlen, 'name_len': len(f)}})
#             if ix > 99:
#                 break
#         for c in ordered_selected_columns_list:
#             value_len = lengths.get(c.upper(), {}).get('max_len', 0)
#             name_len = len(c)
#             if format_methods.upper().find('NAME')>=0:
#                 #method1:always name_len
#                 clen = name_len
#                 max_length = get_parameter_value_from_string(format_methods, 'max_length', default=0, as_numeric=True)
#                 if max_length > 0 and clen > max_length:
#                     clen = max_length
#             # elif format_methods.upper().find('LEN') >= 0:
#             #     #method2:defined value len
#             #     thisLength = 25
#             #     mstr = format_methods.replace('-', ' ').replace('=',' ').strip()
#             #     a = mstr.split(' ')
#             #     for w in a:
#             #         if str(w).isnumeric():
#             #             thisLength = int(w)
#             #     if value_len <= name_len:
#             #         clen = name_len
#             #     else:
#             #         if value_len>thisLength:
#             #             clen = thisLength
#             #         else:
#             #             clen = value_len
#             elif format_methods.upper().find('VALUE') >= 0:
#                 #method3:always value_len with min name_len
#                 max_length = get_parameter_value_from_string(format_methods, 'max_length', default=0, as_numeric=True)
#                 if value_len < name_len:
#                     clen = name_len
#                 else:
#                     clen = value_len
#                 if max_length > 0 and clen > max_length:
#                     clen = max_length
#             else:
#                 #method1:always name_len
#                 clen=name_len
#             ordered_selected_columns_list_lengths.append([c,clen])
#         if title:
#             title_line = f"{title}"
#         else:
#             title_line = ''
    
#         head_line_1 = ''
#         head_line_2 =''
#         head_line_3 =''
#         foot_line =''
#         for ocol in ordered_selected_columns_list_lengths:
#             column_name = ocol[0]
#             column_len = ocol[1]
#             fstr1 = column_name + ' ' * 100
#             fstr = fstr1[0:column_len]
#             if not head_line_1:
#                 head_line_1 = '|' + '-' * column_len
#             else:
#                 head_line_1 = head_line_1 + '|' + '-' * column_len
#             if not head_line_2:
#                 head_line_2 = '|' + fstr
#             else:
#                 head_line_2 = head_line_2 + '|' +fstr
#             if not head_line_3:
#                 head_line_3 = '|' + '-' * column_len
#             else:
#                 head_line_3 = head_line_3 + '|' + '-' * column_len
#             if not foot_line:
#                 foot_line = '|' +  '-' * column_len
#             else:
#                 foot_line = foot_line + '|' + '-' * column_len
#         head_line_1 = head_line_1 + '|'
#         head_line_2 = head_line_2 + '|'
#         head_line_3 = head_line_3 + '|'
#         foot_line = foot_line + '|'
#         # line_len = len(head_line_1)
#         # if line_len < line_length:
#         #     head_line_1 = head_line_1 + '-' * (line_length - line_len - 1) + '|'
#         #     head_line_2 = head_line_2 + ' ' * (line_length - line_len - 1) + '|'
#         #     head_line_3 = head_line_3 + '-' * (line_length - line_len - 1) + '|'
#         #     foot_line   = foot_line   + '-' * (line_length - line_len - 1) + '|'
#         # else:
#         #     head_line_1 = head_line_1[0:line_length-1] + '|'
#         #     head_line_2 = head_line_2[0:line_length-1] + '|'
#         #     head_line_3 = head_line_3[0:line_length-1] + '|'
#         #     foot_line   = foot_line[0:line_length-1] + '|'

#         # if format_methods.upper().find('TITLE')>=0:
#         #     head_line_1 = format_ascii_line(head_line_1, 'MIDDLE')
#         # else:
#         #     head_line_1 = format_ascii_line(head_line_1, 'TOP')
#         head_line_1 = format_ascii_line(head_line_1, 'TOP')
#         head_line_2=format_ascii_line(head_line_2,'DETAIL')
#         head_line_3=format_ascii_line(head_line_3,'MIDDLE')
#         foot_line=format_ascii_line(foot_line,'BOTTOM')
#         len1 = len(foot_line)
#         len2 = len(title_line)
#         maxlen = max(len1, len2)
        
#         if title_line:
#             output.append(title_line.ljust(maxlen))
#         output.append(head_line_1.ljust(maxlen))
#         output.append(head_line_2.ljust(maxlen))
#         output.append(head_line_3.ljust(maxlen))
        
#         #detail_lines            
#         for ix in range(0, len(json_records)):
#             json_rec = json_records[ix]
#             detail_line = ''
#             for ocol in ordered_selected_columns_list_lengths:
#                 column_name = ocol[0]
#                 column_len = ocol[1]
#                 v = str(json_rec.get(column_name))
#                 vstr1 = v + ' ' * 100
#                 vstr = vstr1[0:column_len]
#                 if not detail_line:
#                     detail_line = '|' + vstr
#                 else:
#                     detail_line = detail_line + '|' +vstr
#             detail_line = detail_line + '|'
#             detail_line=format_ascii_line(detail_line,'DETAIL')
#             output.append(detail_line.ljust(maxlen))
#         output.append(foot_line.ljust(maxlen))
#         return output
#     #::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
#     def format_json_records_as_html(self,json_records,columns=[],format_methods='',title=''):
#         output=[]

#         ordered_selected_columns_list=[]
#         if columns:
#             ordered_columns_list = self.ordered_columns_list
#             for c in ordered_columns_list:
#                 if c.upper() in map(str.upper,columns):
#                     ordered_selected_columns_list.append(c)
#         else:
#             columns_in_json={}
#             for ix in range(0, len(json_records)):
#                 json_rec = json_records[ix]
#                 for f in json_rec:
#                     columns_in_json.update({f: 'in_json_rec'})
#                 if ix > 99:
#                     break
#             ordered_columns_list = self.ordered_columns_list
#             for c in ordered_columns_list:
#                 if c.upper() in map(str.upper,columns_in_json):
#                     ordered_selected_columns_list.append(c)

#         output.append('<table style="width:100%">')
#         #header_line
#         output.append('<tr>')
#         for column_name in ordered_selected_columns_list:
#             output.append(f'<th>{column_name}</th>')
#         output.append('</tr>')
#         #detail_lines            
#         for ix in range(0, len(json_records)):
#             json_rec = json_records[ix]
#             output.append('<tr>')
#             for column_name in ordered_selected_columns_list:
#                 v = str(json_rec.get(column_name))
#                 output.append(f'<td>{v}</td>')
#             output.append('</tr>')
#         output.append('</table>')
#         html = ''
#         for lin in output:
#             html = html + lin
#         return html
#     #::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
#     def format_json_records_as_fixed_length_record(self,json_records,columns=[],format_methods='',title=''):
#         output=[]
#         ordered_selected_columns_list=[]
#         if columns:
#             ordered_columns_list = self.ordered_columns_list
#             for c in ordered_columns_list:
#                 if c.upper() in map(str.upper,columns):
#                     ordered_selected_columns_list.append(c)
#         else:
#             columns_in_json={}
#             for ix in range(0, len(json_records)):
#                 json_rec = json_records[ix]
#                 for f in json_rec:
#                     columns_in_json.update({f: 'in_json_rec'})
#                 if ix > 99:
#                     break
#             ordered_columns_list = self.ordered_columns_list
#             for c in ordered_columns_list:
#                 if c.upper() in map(str.upper,columns_in_json):
#                     ordered_selected_columns_list.append(c)
#         #column_values len
#         ordered_selected_columns_list_lengths = []
#         lengths={}
#         for ix in range(0, len(json_records)):
#             json_rec = json_records[ix]
#             for f in json_rec:
#                 v = json_rec.get(f)
#                 vlen = len(str(v))
#                 max_length = lengths.get(f.upper(), {}).get('max_len', 0)
#                 if vlen > max_length:
#                     lengths.update({f.upper(): {'max_len': vlen, 'name_len': len(f)}})
#             if ix > 99:
#                 break
#         for c in ordered_selected_columns_list:
#             value_len = lengths.get(c.upper(), {}).get('max_len', 0)
#             clen = value_len
#             ordered_selected_columns_list_lengths.append([c,clen])

#         #detail_lines            
#         for ix in range(0, len(json_records)):
#             json_rec = json_records[ix]
#             detail_line = ''
#             for ocol in ordered_selected_columns_list_lengths:
#                 column_name = ocol[0]
#                 column_len = ocol[1]
#                 v = str(json_rec.get(column_name))
#                 vstr1 = v + ' ' * 100
#                 vstr = vstr1[0:column_len]
#                 detail_line = detail_line + vstr
#             output.append(detail_line)
#         return output
#     #::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
#     def format_json_records_as_sdf(self,json_records,columns=[],format_methods='',title=''):
#         output=[]
#         ordered_selected_columns_list=[]
#         if columns:
#             ordered_columns_list = self.ordered_columns_list
#             for c in ordered_columns_list:
#                 if c.upper() in map(str.upper,columns):
#                     ordered_selected_columns_list.append(c)
#         else:
#             columns_in_json={}
#             for ix in range(0, len(json_records)):
#                 json_rec = json_records[ix]
#                 for f in json_rec:
#                     columns_in_json.update({f: 'in_json_rec'})
#                 if ix > 99:
#                     break
#             ordered_columns_list = self.ordered_columns_list
#             for c in ordered_columns_list:
#                 if c.upper() in map(str.upper,columns_in_json):
#                     ordered_selected_columns_list.append(c)

#         #header_line
#         output.append('<tr>')
#         hline=''
#         for column_name in ordered_selected_columns_list:
#             if not hline:
#                 hline = f'"{column_name}"'
#             else:
#                 hline = hline + ' , ' + f'"{column_name}"'
                
#         output.append(hline)

#         #detail_lines            
#         for ix in range(0, len(json_records)):
#             json_rec = json_records[ix]
#             dline=''
#             for column_name in ordered_selected_columns_list:
#                 v = str(json_rec.get(column_name))
#                 if not hline:
#                     hline = f'"{v}"'
#                 else:
#                     hline = hline + ' , ' + f'"{v}"'
#             output.append(dline)
#         return output
#     #::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
#     def update_cross_table_relations(self):
#         update_from_other_tables_columns = self.table_model.get('update_from_other_tables_columns', {})
#         for column_name in update_from_other_tables_columns:
#             column = update_from_other_tables_columns.get(column_name, {})
#             update_from_table = column.get('update_from_table', '')
#             update_sql_from_related_table = column.get('update_sql_from_related_table', '')
#             if update_sql_from_related_table and update_from_table:
#                 self.schema.outgoing_relations.update({update_from_table: {'to_table': self.table_name, 'to_column': column_name, 'sql': update_sql_from_related_table}})
# #::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
# #::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
# #::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
# # utilities functions
# #::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
# #::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
# #::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
# def get_missing_columns_from_json_record(mandatory_columns=[],json_record={}):
#     ix = 0
#     if not json_record:
#         return None
#     missing_columns='#'
#     for f in mandatory_columns:
#         v = json_record.get(f)
#         if not v:
#             ix = ix + 1
#             missing_columns = f'{missing_columns}, {f}'
#     missing_columns = missing_columns.replace('#,', '').strip()
#     if ix == 0:
#         missing_columns=''
#     return missing_columns    
# #::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
# def get_empty_mandatory_columns(mandatory_columns=[],columns_values_json={}):
#     ix = 0
#     missing_columns='#'
#     for k in columns_values_json:
#         v = columns_values_json.get(k)
#         if not v:
#             if k in mandatory_columns:
#                 ix = ix + 1
#                 missing_columns = f'{missing_columns}, {k}'
#     missing_columns = missing_columns.replace('#,', '').strip()
#     if ix == 0:
#         missing_columns=''
#     return missing_columns    
# #::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
# def format_query_result_as_json_records(query_result,exclude_null_columns=True):
#     rows_array=[]
#     columns = query_result.keys()
#     rows_count = 0
#     if query_result.cursor:
#         for row_values in query_result.cursor:
#             rows_count = rows_count + 1
#             row_dict={}
#             for f in range(len(row_values)):
#                 if row_values[f] != None or not exclude_null_columns:
#                     row_dict.update({columns[f]: row_values[f]})
#             rows_array.append(row_dict)
#     json_records = {'api_data': rows_array,'rows_count':rows_count}
#     return json_records
# #::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
# def access_key_as_array(access_key):
#     values=[]
#     if type(access_key) == type([]):
#         values=access_key
#     elif type(access_key) == type({}):
#         for k in access_key:
#             v = access_key.get(k)
#             values.append(v)
#     elif type(access_key) == type(''):
#         values.append(access_key)
#     elif type(access_key) == type(1):
#         values.append(access_key)
#     else:
#         values.append(access_key)
#     return values
# #::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
# def get_api_returned_data(api_result):
#     if api_result.get('api_status')== 'success':
#         api_returned_data = api_result.get('api_data', {})
#     else:
#         if api_result.get('api_status'):
#             api_returned_data = {}
#         else:
#             api_returned_data = api_result
#     return api_returned_data
# #::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
# def get_api_returned_status(api_result):
#     api_status=api_result.get('api_status')
#     if not api_status:
#         if api_result.get('api_data') == None:
#             api_status = 'failed'
#         else:
#             api_status = 'success'
#     return api_status
# #::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
# def get_record_from_query_result(query_result={}):
#     data = query_result.get('api_data', [])
#     json_record={}
#     if not data:
#         data={}
#     if type(data) == type([]):
#         if len(data) > 0:
#             json_record = data[0]
#         else:
#             json_record = {}
#     elif type(data) == type({}):
#         json_record = data
#     else:
#         json_record = {}
#     if not type(json_record) == type({}):
#         json_record = {}
#     return json_record
# #::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
# def get_records_from_query_result(query_result={}):
#     json_records = query_result.get('api_data',[])
#     return json_records
# #::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
# def get_column_from_query_result(query_result={},column=''):
#     json_record = get_record_from_query_result(query_result)
#     if not column:
#         column=1
#     if str(column).isnumeric():
#         if column == 0:
#             column = 1
#         column_ix = column
#         ix=0
#         for k in json_record:
#             ix = ix + 1
#             if ix==column_ix:
#                 column_value = json_record.get(k)
#                 break
#     else:
#         column_value = json_record.get(column)
#     return column_value
# #::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
# def standard_table_call_validation(table_reference, json_record, access_key, user, where_expression='dummy'):
#     if not access_key and not json_record:
#         msg = f"[{table_reference}]-[[{whosdaddy()}]]: access_key not provided"
#         log_message(msg, msgType='error')
#         msg=msg.replace('[[','[').replace(']]',']')
#         return {'api_status': 'error', 'api_message': msg}
#     if not json_record:
#         msg = f"[{table_reference}]-[[{whosdaddy()}]]: record not provided"
#         log_message(msg, msgType='error')
#         msg=msg.replace('[[','[').replace(']]',']')
#         return {'api_status': 'error', 'api_message': msg}
#     if type(json_record) != type({}):
#         msg = f"[{table_reference}]-[[{whosdaddy()}]]: record not in json format"
#         log_message(msg, msgType='error')
#         msg=msg.replace('[[','[').replace(']]',']')
#         return {'api_status': 'error', 'api_message': msg}
#     if not user:
#         msg = f"[{table_reference}]-[[{whosdaddy()}]]: user not provided"
#         log_message(msg, msgType='error')
#         msg=msg.replace('[[','[').replace(']]',']')
#         return {'api_status': 'error', 'api_message': msg}
#     if not where_expression:
#         msg = f"[{table_reference}]-[[{whosdaddy()}]]: where_expression not provided"
#         log_message(msg, msgType='error')
#         msg=msg.replace('[[','[').replace(']]',']')
#         return {'api_status': 'error', 'api_message': msg}

#     return {'api_status': 'success', 'api_message': f"call parameters ok."}
# #::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
# # def standard_record_call_validation(table_name, json_record, where_expression, user, transaction_id='?'):
# #     if not table_name:
# #         return {'api_status': 'error', 'api_message': f"table [{table_name}] not provided"}
# #     if not json_record:
# #         return {'api_status': 'error', 'api_message': f"table record not provided"}
# #     if type(json_record) != type({}):
# #         return {'api_status': 'error', 'api_message': f"table record not in json"}
# #     if not where_expression:
# #         return {'api_status': 'error', 'api_message': f"where_expression not provided"}
# #     if not user:
# #         return {'api_status': 'error', 'api_message': f"user not provided"}
# #     if not user:
# #         return {'api_status': 'error', 'api_message': f"transacrtion_id not provided"}
# #     return {'api_status': 'success', 'api_message': f"call parameters ok."}
# #::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
# #::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
# #::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
# # preprocess and parsing (#ROWID#,#FIELDNAME# etc)
# #::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
# #::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
# #::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
# def field_preprocess(column_name, field_value_expression='', json_record={},row_unique_key='xxxx'):
#     if not field_value_expression:
#         return ''
#     if field_value_expression.upper().find('#UID') >=0:
#         (function, params) = function_preprocess('#UID', column_name, field_value_expression, json_record)
#         if not function:
#             return ''
#         params = params.strip()
#         # s1=''
#         # for ix in range(0, len(row_unique_key)):
#         #     c = row_unique_key[ix]
#         #     cc = str(hex(ord(c)))
#         #     s1=s1+cc
#         # #s1=str(hex(row_unique_key))
#         # uid = subprocess.check_output('wmic csproduct get uuid').decode().split('\n')[1].strip()
#         uid=str(uuid.uuid5(uuid.NAMESPACE_DNS, row_unique_key))        
#         return uid
#     return 'heidi'
# #::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
# def function_preprocess(function_id,column_name='',field_value_expression='', json_record={}):
#     if not function_id:
#         return ('','')    
#     if field_value_expression.upper().find('#' + function_id.upper()) >= 0:
#         function_id = '#' + function_id.upper()
#     else:
#         if field_value_expression.upper().find(function_id.upper()) >= 0:
#             function_id = function_id.upper()
#         else:
#             return ('','')
#     pos1 = field_value_expression.upper().find(function_id.upper())
#     pos2 = field_value_expression.upper().find('#', pos1 + 1)
#     if pos2 > pos1:
#         cmd = field_value_expression[pos1:pos2]
#         pos3= cmd.find('(')
#         pos4 = cmd.find(')', pos3 + 1)
#         if pos4-11 > pos3+1:
#             params_str = cmd[pos3+1:pos4-1]
#             params = params_str.split(',')
#             function = function_id.replace('#', '')
#             return (function, params)
#     function = function_id.replace('#', '')            
#     return (function,'')
# #::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
# def processed_string_from_json_record(string, json_record):
#     if not type(json_record) == type({}):
#         return string

#     for f in json_record:
#         v = json_record.get(f, '')
#         v=string_value_preprocess(v)
#         string = string.replace(f'#{f.upper()}#', str(v))
#     return string
# #::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
# def processed_string_from_table_structure(string, table_structure_dictionary):
#     for f in table_structure_dictionary:
#         isN = table_structure_dictionary.get(f.upper(), {}).get('column_is_numeric', False)
#         if isN:
#             v = 0
#         else:
#             v=""
#         string = string.replace(f'#{f.upper()}#', str(v))
#     return string
# #::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
# def evaluated_expression_from_param_values(expression,values=[]):
#     expression = expression.replace('#p', '#P')
#     if len(values) <= 0:
#         return ""
#     for vix in range(0, len(values)):
#         v = values[vix]
#         if type(v) == type({}):
#             v = json.dumps(v)
#         else:
#             v = str(v)
#         what=f"#P{vix+1}#"
#         expression = expression.replace(what, v)
#     # vix=0
#     # while expression.find('#P')>=0 and vix < 99:
#     #     what=f"#P{vix+1}#"
#     #     expression = expression.replace(what, '?')
#     return expression
# #::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
# def evaluated_expression_from_record(string, json_record={}, rowid=0):
#     if string.find('#[UID]#')>=0:
#         p = string.find('#[UID]#')
#         while p >= 0:
#             time_start_str = "1960-09-05 01:02:03"
#             time_start = datetime.datetime.strptime(time_start_str, '%Y-%m-%d %H:%M:%S')
#             time_end = datetime.datetime.utcnow()
#             diff = time_end - time_start
#             duration = diff.days * 24 * 60 * 60 + diff.seconds
#             xrowid = str(rowid) + str(p)+str(duration)
#             uid = get_a_unique_id(str(xrowid))
#             string = string.replace('#[UID]#', uid, 1)
#             p = string.find('#[UID]#')
#         log_result_message(string, msgType='info', level=function_level)

#     if string.find('#[TOKEN]#')>=0:
#         p = string.find('#[TOKEN]#')
#         while p >= 0:
#             xrowid = str(rowid) + str(p)
#             token_param=json.dumps(json_record)+xrowid
#             token_param = token_hex(16)+xrowid+token_hex(16)+token_hex(16)+token_hex(16)
#             token = get_a_token(token_param)
#             token = get_a_urlsafe_token(128)
#             string = string.replace('#[TOKEN]#', token, 1)
#             p = string.find('#[TOKEN]#')
#         log_result_message(string, msgType='info', level=function_level)

#     if string.find('#ROWID#') >= 0:
#         if not rowid:
#             rowid = 0
#         if not str(rowid).isnumeric():
#             rowid = 0
#         string = string.replace('#ROWID#', str(rowid))
#         log_result_message(string, msgType='info', level=function_level)
#     if json_record:
#         string = processed_string_from_json_record(string, json_record)
#     return string
# #::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
# def string_value_preprocess(just_a_string):
#     if not type(just_a_string) == type(''):
#         return just_a_string
#     just_a_string = just_a_string.strip()
#     if len(just_a_string) <= 1:
#         return just_a_string       
#     while len(just_a_string) >= 2:
#         if just_a_string[0] == "'" and just_a_string[-1]=="'":
#             just_a_string = just_a_string[1:]
#             just_a_string = just_a_string[0:-1]
#         elif just_a_string[0] == '"' and just_a_string[-1]=='"':
#             just_a_string = just_a_string[1:]
#             just_a_string = just_a_string[0:-1]
#         else:
#             break
#     just_a_string = just_a_string.strip()
#     while len(just_a_string) >=4:
#         if just_a_string[0] == "(" and just_a_string[1] == "(" and just_a_string[-1]==")" and just_a_string[-2]==")":
#             just_a_string = just_a_string[1:]
#             just_a_string = just_a_string[0:-1]
#         else:
#             break
#     return just_a_string.strip()
# #::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
# def field_value_for_sql(tableObj, column_name, column_value):
#     # if tableObj.dialect == 'SQLITE':
#     #     foo = 1
        
#     value = None
#     # if column_name == 'validation_rules':
#     #     isdict = 1
        
#     # isdict = 0
#     if type(column_value) == type(True):
#         column_value = int(column_value)
#     if type(column_value) == type({}):
#         column_value = json.dumps(column_value)
#         # isdict = 1

#     original_column_name = tableObj.table_structure_dictionary.get(column_name.upper(), {}).get('column_name', '')
#     is_numeric = tableObj.table_structure_dictionary.get(column_name.upper(), {}).get('column_is_numeric', '')
#     if not original_column_name.upper():
#         msg=f"[[column]] [{column_name}] removed from UPDATE of {tableObj.reference}"
#         log_result_message(msg, msgType='info', level=function_level)
#         return None

#     if str(column_value).find('#SQL:') >= 0:
#         column_value = str(column_value)
#         column_value = string_value_preprocess(column_value)
#         column_value = column_value.replace('#SQL:', '')
#         value = f"{column_value}"
#     elif is_numeric:
#         if str(column_value).isnumeric():
#             value = f"{column_value}"
#         else:
#             value = f"NULL"
#     else:
#         column_value = str(column_value)
#         column_value=string_value_preprocess(column_value)
#         value = f"'{column_value}'"

#     # if isdict == 1:
#     #     print(value)
#     # if isdict:
#     #     print(value)

#     return value
# #::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
# # json record support
# #::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
# #::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
# #::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
# def get_changed_columns(old_record={},new_record={}):
#     changed_columns=[]
#     if new_record != old_record:
#         for k in new_record:
#             v1 = new_record.get(k)
#             v2 = old_record.get(k)
#             if not v1 == v2:
#                 changed_columns.append(k)
#     return changed_columns
# #::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
# def get_changed_columns_values(old_record={},new_record={}):
#     changed_columns=[]
#     if new_record != old_record:
#         for k in new_record:
#             v1 = new_record.get(k)
#             v2 = old_record.get(k)
#             if not v1 == v2:
#                 msg = f"[changed record:] [[{k}]]:[[[{v2}]]]-->[[[[[{v1}]]]]"
#                 log_result_message(msg,msgType='info')
#                 changed_record = {k:{'old_value': v2, 'new_value': v1}}
#                 changed_columns.append(changed_record)
#     return changed_columns
# #::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
# def optimize_record_based_on_current_record(this_record, current_record):
#     new_record={}
#     for f in this_record:
#         #print(f)
#         v1 = this_record.get(f)
#         v2 = current_record.get(f)
#         if str(v1) != str(v2):
#             #print(f,v1,v2)
#             new_record.update({f: v1})
#     # for f in current_record:
#     #     #print(f)
#     #     v1 = current_record.get(f)
#     #     v2 = this_record.get(f)
#     #     if str(v1) != str(v2):
#     #         #print(f,v1,v2)
#     #         new_record.update({f: v1})
#     return new_record
# #::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
# def normalized_json_record(json_record):
#     for k in json_record:
#         v = json_record.get(k)
#         if type(v) == type([]):
#             v = str(v)
#             json_record.update({k: v})
#         if type(v) == type({}):
#             v = json.dumps(v)
#             json_record.update({k: v})
#     return json_record
# #::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
# def valid_json_record_to_table_structure(table_structure_dictionary,json_record):
#     if not json_record or type(json_record) != type({}):
#         print('what is this ?')
#         return {}
#     # print('\njson:', json_record)
#     # print('\nstructure:', table_structure_dictionary)
    
#     valid_json_record={}
#     for k in json_record:
#         original_column_name = table_structure_dictionary.get(k.upper(), {}).get('column_name', '')
#         if not original_column_name.upper() == k.upper():
#             #print('removed column===>', k, original_column_name)
#             pass
#         else:
#             v=json_record.get(k)
#             valid_json_record.update({k: v})
#     # if not valid_json_record:
#     #     x=1
#     return valid_json_record
# #::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
# def valid_column(column_name, table_model,table_structure_dictionary):
#     original_column_name = valid_column_in_table_structure(column_name,table_structure_dictionary)
#     original_column_name2 = valid_column_in_table_model(column_name, table_model)
#     if original_column_name and original_column_name==original_column_name2:
#         return original_column_name
#     else:
#         return ''
# #::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
# def valid_column_in_table_model(column_name,table_model):
#     original_column_name = table_model['columns'].get(column_name.upper(), {}).get('column_name', '')
#     return original_column_name
# #::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
# def valid_column_in_table_structure(column_name,table_structure_dictionary):
#     original_column_name = table_structure_dictionary.get(column_name.upper(), {}).get('column_name', '')
#     return original_column_name
# #::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
# def valid_select_columns_expression(columns,table_model):
#     columns_list=[]
#     if type(columns) == type(''):
#         a = columns.split(',')
#         for f in a:
#             columns_list.append(f) 
#     elif type(columns) == type([]):
#         columns_list = columns

#     # if len(columns_list) <= 0:
#     #     columns_list.append('*')

#     expr=''
#     for ix in range(0, len(columns_list)):
#         col = columns_list[ix]
#         if col == '*':
#             ok = True
#         elif col.upper().find('ROWID') == 0:
#             ok = True
#         else:
#             f = col.split(' as ')[0]
#             if valid_column_in_table_model(f, table_model):
#                 ok = True
#             else:
#                 ok = False
#         if ok:
#             if not expr:
#                 expr = col
#             else:
#                 expr = expr + ' , ' + col
#     if not expr:
#         expr='*'
#     return expr
# #::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
# def valid_orderby_expression(order_by,table_model):
#     columns_list=[]
#     if type(order_by) == type(''):
#         a = order_by.split(',')
#         for f in a:
#             columns_list.append(f) 
#     elif type(order_by) == type([]):
#         columns_list = order_by

#     # if len(columns_list) <= 0:
#     #     columns_list.append('*')

#     expr=''
#     for ix in range(0, len(columns_list)):
#         col = columns_list[ix].strip()
#         if col.upper().find('ROWID') == 0:
#             ok = True
#         else:
#             f = col.split(' ')[0]
#             if valid_column_in_table_model(f, table_model):
#                 ok = True
#                 ads = col.split(' ')[1].upper()
#                 if ads[0:3] not in ('ASC', 'DESC'):
#                     col=f
#             else:
#                 ok = False
#         if ok:
#             if not expr:
#                 expr = col
#             else:
#                 expr = expr + ' , ' + col
#     if not expr:
#         expr=''
#     return expr
# #::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
# def select_columns_excluding_columns(columns,exclude_columns,table_model):
#     columns_list = []
#     if not exclude_columns:
#         if not columns:
#             return '*'

#     if not columns:
#         columns=[]
#         for f in table_model.get('columns', {}):
#             col = table_model.get('columns', {}).get(f.upper(), {}).get('column_name')
#             if col:
#                 columns.append(col)
#     if type(columns) == type(''):
#         a = columns.split(',')
#         for f in a:
#             columns_list.append(f) 
#     elif type(columns) == type([]):
#         columns_list = columns
        
#     exclude_columns_list=[]
#     if type(exclude_columns) == type(''):
#         a = exclude_columns.split(',')
#         for f in a:
#             exclude_columns_list.append(f.strip()) 
#     elif type(exclude_columns) == type([]):
#         exclude_columns = exclude_columns

#     for f in exclude_columns_list:
#         col = table_model.get('columns', {}).get(f.upper(), {}).get('column_name')
#         if col:
#             columns_list.remove(col)
#     return columns_list
# #::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
# #::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::##########
# def AND_fields_expression(expression_columns,columns_dictionary):
#     and_expression=''
#     for fs in expression_columns:
#         if fs:
#             ffs = fs.split(',')
#             equal_expression=''
#             for ix in range(0,len(ffs)):
#                 f = ffs[ix]
#                 data_type=columns_dictionary.get(f.upper()).get('data_type','VARCHAR')
#                 column_name = columns_dictionary.get(f.upper()).get('column_name', f)
#                 if not data_type_is_numeric(data_type):
#                     fexpression = f"{column_name}='#{column_name.upper()}#'"
#                 else:
#                     fexpression = f"{column_name}=#{column_name.upper()}#"
#                 if not equal_expression:
#                     equal_expression = fexpression
#                 else:
#                     equal_expression = equal_expression + ' AND ' + fexpression
#             if len(ffs) > 1:
#                 equal_expression = f'({equal_expression})'                
#             if not and_expression:
#                 and_expression=equal_expression
#             else:
#                 and_expression = and_expression + " AND " + equal_expression
#     if len(expression_columns) > 1:
#         and_expression=f'({and_expression})'    
#     return and_expression    
# #::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::##########
# def OR_fields_expression(expression_columns,columns_dictionary):
#     or_expression=''
#     for fs in expression_columns:
#         if fs:
#             ffs = fs.split(',')
#             equal_expression=''
#             for ix in range(0,len(ffs)):
#                 f = ffs[ix]
#                 data_type=columns_dictionary.get(f.upper()).get('data_type','VARCHAR')
#                 column_name = columns_dictionary.get(f.upper()).get('column_name', f)
#                 if not data_type_is_numeric(data_type):
#                     fexpression = f"{column_name}='#{column_name.upper()}#'"
#                 else:
#                     fexpression = f"{column_name}=#{column_name.upper()}#"
#                 if not equal_expression:
#                     equal_expression = fexpression
#                 else:
#                     equal_expression = equal_expression + ' AND ' + fexpression
#             if len(ffs) > 1:
#                 equal_expression = f'({equal_expression})'                
#             if not or_expression:
#                 or_expression=equal_expression
#             else:
#                 or_expression = or_expression + " OR " + equal_expression
#     if len(expression_columns) > 1:
#         or_expression=f'({or_expression})'    
#     return or_expression    
# #::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::##########
# def AND_expression(expression_components):
#     and_expression=''
#     for compo in expression_components:
#         if not and_expression:
#             and_expression=compo
#         else:
#             and_expression = and_expression + " AND " + compo
#     if len(expression_components) > 1:
#         and_expression=f'({and_expression})'    
#     return and_expression    
# #::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::##########
# def OR_expression(expression_components):
#     or_expression=''
#     for compo in expression_components:
#         if not or_expression:
#             or_expression=compo
#         else:
#             or_expression = or_expression + " OR " + compo
#     if len(expression_components) > 1:
#         or_expression=f'({or_expression})'    
#     return or_expression    
# #::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::##########

# #::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
# #::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
# # formatting utilities
# #::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
# #::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
# def format_ascii_line(line, line_type):
#     if line_type.upper().find('TOP') >= 0 or line_type.upper().find('HEADER') >= 0:
#         line = line.replace('-|-', '-' + ascii_char(194) + '-')
#         line = line.replace('|-' , ascii_char(218) + '-')
#         line = line.replace('-|' , '-' + ascii_char(191))
#     if line_type.upper().find('BOTTOM') >= 0 or line_type.upper().find('FOOTER') >= 0:
#         line = line.replace  ('-|-', '-' + ascii_char(193) + '-')
#         line = line.replace  ('|-' ,  ascii_char(192) + '-')
#         line = line.replace  ('-|' , '-' + ascii_char(217))
#     if line_type.upper().find('MIDDLE') >= 0 or line_type.upper().find('HEADER-1') >= 0:
#         line = line.replace('-|-', '-' + ascii_char(197) + '-')
#         line = line.replace('|-' , ascii_char(195) + '-')
#         line = line.replace('-|' , '-' + ascii_char(180))
#     elif line_type.upper().find('DETAIL') >= 0:
#         line = line.replace('-|-', '-' + ascii_char(179) + '-')
#         line = line.replace('|-' , ascii_char(195) + '-')
#         line = line.replace('-|' , '-' + ascii_char(180))
#     else:#DETAIL
#         line = line.replace('-|-', '-' + ascii_char(179) + '-')
#         line = line.replace('|-' , ascii_char(195) + '-')
#         line = line.replace('-|' , '-' + ascii_char(180))
#     line = line.replace('-'  ,   ascii_char(196))
#     line = line.replace('|'  ,   ascii_char(179))
#     return line
# #::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
# def get_a_unique_id(param1):
#     # import uuid
#     # uid1 = str(uuid.uuid1())                                        # make a UUID based on the host ID and current time
#     # uid2 = str(uuid.uuid3(uuid.NAMESPACE_DNS, 'python.org'))        # make a UUID using an MD5 hash of a namespace UUID and a name     
#     uid3 = str(uuid.uuid4())                                        # make a random UUID
#     #uid4 = str(uuid.uuid5(uuid.NAMESPACE_DNS, str(param1)))         # make a UUID using a SHA-1 hash of a namespace UUID and a name  
#     # uid5 = str(uuid.UUID('{00010203-0405-0607-0809-0a0b0c0d0e0f}')) # make a UUID from a string of hex digits (braces and hyphens ignored)     
#     return uid3
# #::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
# def get_a_token(param):
#     token = generate_token(param)
#     token =token_urlsafe(128)
#     return token
# #::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
# def get_a_urlsafe_token(nbytes):
#     token =token_urlsafe(nbytes)
#     return token
# #::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
# def get_parameter_value_from_string(string, param_name,default='',as_numeric=False,data_type=''):
#     #string='GRID value max_length=20 line_length = 120'
#     pos = string.upper().find(param_name.upper())
#     if pos < 0:
#         val = None
#     else:
#         str1 = string[pos:]
#         str1 = str1.replace(':', '=')
#         strArr = str1.split('=')
#         valStr = strArr[1]
#         str2 = valStr.split(' ')
#         val = str2[0].strip()
#     if not val:
#         val = default
#     if as_numeric:
#         if not str(val).isnumeric():
#             val = 0
#         else:
#             if data_type.upper().find('DEC')>=0:
#                 val = decimal.Decimal(val)
#             elif data_type.upper().find('FLOAT')>=0:
#                     val = float(val)
#             else:
#                 val = int(str(val).replace('.', '').replace(',', ''))
#     return val
# #::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
# def whoami():
#     return inspect.stack()[1][3]
# #::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
# def whosdaddy():
#     return inspect.stack()[3][3]
# #::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
# #::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
# #::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
# # reorganization functions
# #::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
# #::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
# #::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
def create_table_ddl(tableObj,engineObj):
    ddl_obj=ddl.CreateTable(tableObj)
    ddl_string=str(ddl_obj.compile(dialect=engineObj.dialect)).strip()
    print(ddl_string)

    # ddl_obj = CreateTable(tableObj)
    # try:
    #     ddl_string=str(ddl_obj.compile(engineObj)).strip()
    #     print(ddl_string)
    # except Exception as e:
    #     #print(e)
    #     ddl_string = ''



    return ddl_string
#################################################    
def drop_table_ddl(tableObj,engineObj):
    ddl_obj = DropTable(tableObj)
    try:
        ddl_string=str(ddl_obj.compile(dialect=engineObj.dialect)).strip()
        print(ddl_string)
    except Exception as e:
        # print(e)
        ddl_string = ''
    return ddl_string
#################################################    
def clear_table_ddl(tableObj,engineObj):
    ddl_obj = tableObj.delete()
    try:
        ddl_string=str(ddl_obj.compile(dialect=engineObj.dialect)).strip()
        print(ddl_string)
    except Exception as e:
        print(e)
        # ddl_string = ''
    return ddl_string
#################################################    
def create_table_constraints_ddl(tableObj, engineObj):
    ddl_text=''
    constraints = tableObj.constraints
    for constraint in constraints:
        ddl_obj = AddConstraint(constraint)
        try:
            ddl_string=str(ddl_obj.compile(dialect=engineObj.dialect)).strip()
            print(ddl_string)
        except Exception as e:
            # if e.message.find('it has no name')<0:
            #     print(e)
            ddl_string = ''
        if ddl_string:
            if not ddl_text:
                ddl_text = ddl_string
            else:
                ddl_text = ddl_text + '\n' + ddl_string    
    return ddl_text
#################################################    
def drop_table_constraints_ddl(tableObj, engineObj):
    ddl_text=''
    constraints = tableObj.constraints
    for constraint in constraints:
        ddl_obj = DropConstraint(constraint)
        try:
            ddl_string=str(ddl_obj.compile(dialect=engineObj.dialect)).strip()
            print(ddl_string)
        except Exception as e:
            # # if e. str(e.message).find('it has no name')<0:
            #     print(e)
            ddl_string = ''
        if ddl_string:
            if not ddl_text:
                ddl_text = ddl_string
            else:
                ddl_text = ddl_text + '\n' + ddl_string    
    return ddl_text
#################################################    
def create_table_indexes_ddl(tableObj, engineObj):
    ddl_text=''
    indexes = sorted(list(tableObj.indexes), key=lambda k: k.name,reverse=False)
    for index in indexes:
        ddl_obj = CreateIndex(index)
        try:
            ddl_string=str(ddl_obj.compile(dialect=engineObj.dialect)).strip()
            print(ddl_string)
        except Exception as e:
            # if e.message.find('it has no name')<0:
            #     print(e)
            ddl_string = ''
        if ddl_string:
            if not ddl_text:
                ddl_text = ddl_string
            else:
                ddl_text = ddl_text + '\n' + ddl_string    
    return ddl_text
#################################################    
def drop_table_indexes_ddl(tableObj, engineObj):
    ddl_text=''
    indexes = sorted(list(tableObj.indexes), key=lambda k: k.name,reverse=False)
    for index in indexes:
        ddl_obj = DropIndex(index)
        try:
            ddl_string=str(ddl_obj.compile(dialect=engineObj.dialect)).strip()
            print(ddl_string)
        except Exception as e:
            # print(e)
            ddl_string = ''
        if ddl_string:
            if not ddl_text:
                ddl_text = ddl_string
            else:
                ddl_text = ddl_text + '\n' + ddl_string    
    return ddl_text
#################################################    
#################################################    
def add_table_column_ddl(columnObj,tableObj,engineObj):
    table_name = tableObj.name
    column_name = columnObj.name

    xcolumn_name = str(columnObj.compile(dialect=engineObj.dialect)).strip()
    print(xcolumn_name)

    column_type = str(columnObj.type.compile(dialect=engineObj.dialect)).strip()
    try:
        column_default = str(columnObj.default.compile(dialect=engineObj.dialect)).strip()
    except Exception as e:
        # if e.message.find('it has no name')<0:
        #     print(e)
        column_default = ''
    if column_default:
        print('---default---',column_default)

    ddl_string = f"ALTER TABLE {table_name} ADD COLUMN {column_name} {column_type}"
    print(ddl_string)
    return ddl_string
#################################################    
def drop_table_column_ddl(columnObj,tableObj,engineObj):
    table_name = tableObj.name
    column_name = columnObj.name
    ddl_string=f"ALTER TABLE {table_name} DROP COLUMN {column_name}"
    print(ddl_string)
    return ddl_string
#################################################    
def alter_table_column_ddl(columnObj,tableObj,engineObj):
    table_name = tableObj.name
    column_name = columnObj.name

    xcolumn_name = str(columnObj.compile(dialect=engineObj.dialect)).strip()
    print(xcolumn_name)

    column_type = str(columnObj.type.compile(dialect=engineObj.dialect)).strip()
    try:
        column_default = str(columnObj.default.compile(dialect=engineObj.dialect)).strip()
    except Exception as e:
        # if e.message.find('it has no name')<0:
        #     print(e)
        column_default = ''
    if column_default:
        print('---default---',column_default)

    try:
        column_default = str(columnObj.server_default.compile(dialect=engineObj.dialect)).strip()
    except Exception as e:
        # if e.message.find('it has no name')<0:
        #     print(e)
        column_default = ''
    if column_default:
        print('---server_default---',column_default)

    ddl_string = f"ALTER TABLE {table_name} ALTER COLUMN {column_name} {column_type}"
    print(ddl_string)
    return ddl_string
#################################################    
def table_column_ddl(columnObj,tableObj,engineObj):
    table_name = tableObj.name
    column_name = columnObj.name
    # xcolumn_name = str(columnObj.compile(dialect=engineObj.dialect)).strip()
    # print(xcolumn_name)
    # cname = columnObj.key
    
    # xcolumn_name = str(tableObj.c[cname].compile(dialect=engineObj.dialect)).strip()
    # print(xcolumn_name)
    column_type = str(columnObj.type.compile(dialect=engineObj.dialect)).strip()

    try:
        column_default = str(columnObj.default.compile(dialect=engineObj.dialect)).strip()
    except Exception as e:
        # print(e)
        column_default = ''
    if column_default:
        print('---default---',column_default)

    try:
        column_default = str(columnObj.server_default.compile(dialect=engineObj.dialect)).strip()
    except Exception as e:
        # print(e)
        column_default = ''
    if column_default:
        print('---default---',column_default)

    try:
        # from sqlalchemy.engine import ddl
        ddl_obj=ddl.CreateColumn(columnObj)
        ddl_string=str(ddl_obj.compile(dialect=engineObj.dialect)).strip()
        #print(ddl_string)
    except Exception as e:
        # print(e)
        ddl_string = ''
    if not ddl_string:
        ddl_string = f"TABLE {table_name} COLUMN {column_name} {column_type} {column_default}"
    print(ddl_string)
    return ddl_string
#################################################    
# #::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
# #::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
# #::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
# #::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
# # module initialization
# #::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
# #::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
# #::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
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