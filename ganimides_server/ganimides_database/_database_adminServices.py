# -*- coding: utf-8 -*-
import os
import sys
if not (os.path.dirname(__file__) in sys.path): sys.path.append(os.path.dirname(__file__))

module_ProgramName = os.path.splitext(os.path.basename(__file__))[0]
module_id = '{}'.format(module_ProgramName)
module_version = 0.1

from _onlineApp import thisApp

from _onlineApp import log_message, get_debug_option_as_level

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
# from sqlalchemy.schema import DropTable, CreateTable
# from sqlalchemy.orm import scoped_session, sessionmaker
# #from sqlalchemy import create_engine
# from sqlalchemy.pool import SingletonThreadPool
# from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy import create_engine, MetaData, Table, Column,Integer, Numeric, String, Date, DateTime, text
from sqlalchemy.ext.compiler import compiles
from sqlalchemy.schema import (CreateTable, AddConstraint, CreateIndex,
                               DropTable, DropConstraint, DropIndex,
                               ForeignKeyConstraint, CheckConstraint,
                               UniqueConstraint, PrimaryKeyConstraint)
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import MetaData
from _database_class_table import leandroutechnologyforward_database_table_class as db_table_class
# meta = MetaData()
#::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
#::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
#::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
# globals
#::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
#::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
#::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
#::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
#::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
#::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
#::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
# services 
#::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
#::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
#::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
def check_table(tableInstance, silent=None, debug=None, auto_synchronize=True, synchronization_method='drop-create,recreate,add-columns', copy_records=True):
    debug_level = get_table_debug_level(tableInstance, debug)
    engine = tableInstance.session.bind.engine
    tableObj = tableInstance.model.__table__
    metadata = MetaData(bind=engine)
    table_name = tableInstance.model.__tablename__
    table_rows = tableInstance.rowCount()
    if table_name == 'api_subscriptions':
        x=1
    compare_with_physical_table(tableInstance, debug_level - 1)
    if tableInstance.physical_table_is_synchronized:
        msg = f"table [[{table_name}]] loaded with [{table_rows} rows]"
        if int(debug_level) > 0 and not silent:
            log_message(msg)
    else:
        msg = f"table [[{table_name}]] with [{table_rows} rows]"
        if tableInstance.new_columns > 0:
            msg = msg + f", [[[[{tableInstance.new_columns} new]]]]"
        if tableInstance.unmapped_columns > 0:
            msg = msg + f", [[[{tableInstance.unmapped_columns} unmapped]]]"
        if tableInstance.changed_columns > 0:
            msg = msg + f", [[[[[{tableInstance.changed_columns} changed]]]]]"
        if tableInstance.new_columns + tableInstance.unmapped_columns + tableInstance.changed_columns > 1:
            x = 's'
        else:
            x=''
        msg = msg + f" column{x}"
        if not auto_synchronize:
            msg = msg+" loaded [UnSynchronized]"
            if debug_level > 0 and not silent:
                log_message(msg)
        else:
            if tableInstance.new_columns == 0 and tableInstance.changed_columns == 0 and synchronization_method.upper().find('ADD') >= 0:
                msg = msg+" loaded [UnSynchronized]"
                if debug_level > 0 and not silent:
                    log_message(msg)
            else:                
                if synchronization_method.upper().find('DROP') >= 0:
                    drop_and_create_table(tableInstance, copy_records, debug_level - 1)
                elif synchronization_method.upper().find('ADD') >= 0:
                    add_columns_to_physical_table(tableInstance,debug_level - 1)
                elif synchronization_method.upper().find('RECREATE') >= 0:
                    recreate_table(tableInstance, copy_records, debug_level - 1)
                compare_with_physical_table(tableInstance,debug_level - 1)
                if tableInstance.physical_table_is_synchronized:
                    msg = msg+f" [Synchronized] (method used:[[[{synchronization_method}]]]) and loaded"
                else:
                    msg = msg+f" [Synchronized] (method used:[[[{synchronization_method}]]]) and loaded but is [still UnSynchronized]"
                if int(debug_level) > 0:
                    log_message(msg)
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 
def drop_table(tableInstance,debug=None):
    debug_level = get_table_debug_level(tableInstance, debug)
    engine = tableInstance.session.bind.engine
    tableObj = tableInstance.model.__table__
    table_name = tableInstance.model.__tablename__
    table_rows = tableInstance.rowCount()
    ddl_string = drop_table_ddl(tableObj, engine,debug_level - 1)
    engine.execute(ddl_string)
    if int(debug_level) > 0:
        msg = f"table [[{table_name}]] dropped with [{table_rows} rows]"
        log_message(msg)
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 
def clear_table(tableInstance,debug=None):
    debug_level = get_table_debug_level(tableInstance, debug)
    engine = tableInstance.session.bind.engine
    tableObj = tableInstance.model.__table__
    table_name = tableInstance.model.__tablename__
    table_rows = tableInstance.rowCount()
    ddl_string = clear_table_ddl(tableObj, engine)
    engine.execute(ddl_string)
    if int(debug_level) > 0:
        msg = f"table [[{table_name}]] cleared with [{table_rows} rows]"
        log_message(msg)
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 
def recreate_table(tableInstance,copy_records=True,debug=None):
    debug_level = get_table_debug_level(tableInstance, debug)
    engine = tableInstance.session.bind.engine
    tableObj = tableInstance.model.__table__
    metadata = MetaData(bind=engine)
    table_name = tableInstance.model.__tablename__
    table_rows = tableInstance.rowCount()
    old_rows= table_rows
    if copy_records:
        backup_table_name = tableInstance.model.__tablename__ + '_backup'
        backup_table_name = copy_table(tableInstance, backup_table_name)
        if not backup_table_name:
            msg ='#ERROR#copy to backup failed#RESET#'
            log_message(msg)
            return
        backuptable = Table(backup_table_name, metadata, autoload=True)
        old_columns = backuptable.columns
        old_rows = engine.execute(f"select count(*) from {backup_table_name}").scalar()
    
    #drop and recreate with the new structure
    tableObj.drop(engine,checkfirst=True)
    tableObj.create(engine, checkfirst=True)
    new_rows= tableInstance.rowCount()
    if not copy_records:
        msg=f"table [[{tableInstance.model.__tablename__}]] [recreated] with [[[{new_rows}/{old_rows} rows copied]]]"
    else:
        columns = [c.copy() for c in tableObj.columns]
        #copy data from backup
        columns_str=''
        for column in columns:
            if column.key in old_columns.keys():
                if columns_str:
                    columns_str = columns_str + ' , ' + column.name
                else:
                    columns_str = column.name
        from_table = backup_table_name
        to_table =tableInstance.model.__tablename__
        ddl_string = f"INSERT INTO {to_table} ({columns_str}) select {columns_str} from {from_table}"
        if int(debug_level) > 0:
            msg=f"table [[{tableInstance.model.__tablename__}]] copy records DDL: [{ddl_string}]"
            log_message(msg)
        try:
            engine.execute(ddl_string)
        except Exception as e:
            print(e)

        new_rows= tableInstance.rowCount()
        if new_rows==old_rows:
            backuptable.drop(engine,checkfirst=True)
    
        #kill garbages
        del backuptable
        # del BACKUPTABLE_TABLE

        msg=f"table [[{tableInstance.model.__tablename__}]] [recreated] with [[[{new_rows}/{old_rows} rows copied]]] from backup table {backup_table_name}"
    if int(debug_level) > 0:
        log_message(msg)
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 
def drop_and_create_table(tableInstance,copy_records=True,debug=None):
    debug_level = get_table_debug_level(tableInstance, debug)
    engine = tableInstance.session.bind.engine
    tableObj = tableInstance.model.__table__
    metadata = MetaData(bind=engine)
    table_name = tableInstance.model.__tablename__
    table_rows = tableInstance.rowCount()
    old_rows= table_rows
    table_rows = tableInstance.rowCount()
    old_rows= table_rows
    if copy_records:
        backup_table_name = tableInstance.model.__tablename__ + '_backup'
        backup_table_name = copy_table(tableInstance, backup_table_name)
        if not backup_table_name:
            msg ='#ERROR#copy to backup failed#RESET#'
            log_message(msg)
            return
        backuptable = Table(backup_table_name, metadata, autoload=True)
        old_columns = backuptable.columns
        old_rows = engine.execute(f"select count(*) from {backup_table_name}").scalar()
    
    #drop and recreate with the new structure
    tableObj.drop(engine,checkfirst=True)
    recreate_tables(tableInstance.model_base,engine)

    new_rows= tableInstance.rowCount()
    if not copy_records:
        msg=f"table [[{tableInstance.model.__tablename__}]] [recreated] with [[[{new_rows}/{old_rows} rows copied]]]"
    else:
        columns = [c.copy() for c in tableObj.columns]
        #copy data from backup
        columns_str=''
        for column in columns:
            if column.key in old_columns.keys():
                if columns_str:
                    columns_str = columns_str + ' , ' + column.name
                else:
                    columns_str = column.name
        from_table = backup_table_name
        to_table =tableInstance.model.__tablename__
        ddl_string = f"INSERT INTO {to_table} ({columns_str}) select {columns_str} from {from_table}"
        if int(debug_level) > 0:
            msg=f"table [[{tableInstance.model.__tablename__}]] copy records DDL: [{ddl_string}]"
            log_message(msg)
        try:
            engine.execute(ddl_string)
        except Exception as e:
            print(e)

        new_rows= tableInstance.rowCount()
        if new_rows==old_rows:
            backuptable.drop(engine,checkfirst=True)
    
        #kill garbages
        del backuptable

        msg=f"table [[{tableInstance.model.__tablename__}]] [recreated] with [[[{new_rows}/{old_rows} rows copied]]] from backup table {backup_table_name}"

    if int(debug_level) > 0:
        log_message(msg)
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 
def copy_table(tableInstance, new_table_name, debug=None, overwrite=False):
    debug_level = get_table_debug_level(tableInstance, debug)
    engine = tableInstance.session.bind.engine
    tableObj = tableInstance.model.__table__
    metadata = MetaData(bind=engine)
    table_name = tableInstance.model.__tablename__
    table_rows = tableInstance.rowCount()

    physical_table = Table(table_name, metadata, autoload=True)
    physical_table.__tablename__ = table_name
    
    columns = [c.copy() for c in physical_table.columns]
    #temp_schema={}
    # PHYSICAL_TABLE_TABLE = db_table_class(physical_table, temp_schema, engine, tableInstance.session, debug_level - 1)
    # query_rows1 = PHYSICAL_TABLE_TABLE.rowCount()
    query_rows1 = engine.execute(f"select count(*) from {table_name}").scalar()

    # m = MetaData()
    # m.reflect(engine)
    # for table in m.tables.values():
    #     print(table.name)
    #     # for column in table.c:
    #     #     print(column.name)

    if not overwrite:
        tables_list = get_tables_directory(engine)
        xnew_table_name = new_table_name
        ix=0
        while ix <= 99:
            ix=ix+1
            if xnew_table_name in tables_list:
                xnew_table_name = new_table_name + '_' + str(ix)
            else:
                break
        new_table_name = xnew_table_name

    new_table = Table(new_table_name, metadata, *columns)

    new_table.drop(engine, checkfirst=True)
    new_table.create(engine, checkfirst=True)
    new_table = Table(new_table_name, metadata, autoload=True)
    columns = [c.copy() for c in new_table.columns]
    # temp_schema={}
    # NEW_TABLE_TABLE = db_table_class(new_table, temp_schema, engine, tableInstance.session, debug_level - 1)

    columns_str=''
    for column in columns:
        if columns_str:
            columns_str = columns_str + ' , ' + column.name
        else:
            columns_str = column.name
    from_table = tableInstance.model.__tablename__
    to_table = new_table.name
    ddl_string = f"INSERT INTO {to_table} ({columns_str}) select {columns_str} from {from_table}"
    if int(debug_level) > 0:
        msg=f"table [[{tableInstance.model.__tablename__}]] copy records to [[{to_table}]] DDL: [[[{ddl_string}]]]"
        log_message(msg)
    try:
        engine.execute(ddl_string)
    except Exception as e:
        print(e)
        return False

    # query_rows2= NEW_TABLE_TABLE.rowCount()
    query_rows2 = engine.execute(f"select count(*) from {to_table}").scalar()

    #garbage kill
    del new_table
    del physical_table
    # del PHYSICAL_TABLE_TABLE
    # del NEW_TABLE_TABLE
    
    msg=f"table [[{from_table}]] [copied to ] [[{to_table}]] with [[[{query_rows2}/{query_rows1} rows]]]."
    if int(debug_level) > 0:
        log_message(msg)

    if query_rows1 == query_rows2:
        return to_table
    else:
        return None
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 
def clone_table_approach_1(original_table, connection, metadata):
    try:
        new_table_name = original_table.name + '_sync'
        columns = [c.copy() for c in original_table.columns]
        new_table = Table(new_table_name, metadata, quote=False, *columns)

        # Create table in database
        if not new_table.exists():
            new_table.create()
        else:
            raise Exception("New table already exists")

        # Remove constraints from new table if any
        for constraint in new_table.constraints:
            connection.execute(DropConstraint(constraint))

        # Return table handle for newly created table
        final_cloned_table = Table(new_table, metadata, quote=False)
        return final_cloned_table

    except:
        # Drop if we did create a new table
        if new_table.exists():
            new_table.drop()
        raise
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 
def display_summary(tableInstance, where_expression=None, order_by=None, rows_limit=None, include_columns=None, exclude_columns=[], output_method='GRID', format_methods='name,max_length=20,line_length=120', title=''):
    import plotly.graph_objects as go

    rowsObj = tableInstance.get_rows_as_dict(where_expression)
    header=[]
    data=[]
    for column in tableInstance.model.__table__.columns:
        header.append(column.name)
        data.append([])
    for row in rowsObj:
        row_values = []
        ix=-1
        for c in inspect(tableInstance.model).mapper.column_attrs:
            ix=ix+1
            val = str(getattr(row, c.key))
            data[ix].append(val)
            #row_values.append(str(getattr(row, c.key)))
        #data.append(row_values)
    
    # print(data)

    # columns = tableInstance.model.__table__.columns.keys()
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
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 
def display_table_ddls(tableInstance):
    engine = tableInstance.session.bind.engine
    tableObj = tableInstance.model.__table__
    metadata = MetaData(bind=engine)
    table_name = tableInstance.model.__tablename__

    ddl_obj = create_table_ddl(tableObj, engine)
    ddl_obj = drop_table_ddl(tableObj, engine)
    ddl_obj = clear_table_ddl(tableObj, engine)
    ddl_obj = drop_table_constraints_ddl(tableObj, engine)
    ddl_obj = create_table_constraints_ddl(tableObj, engine)
    ddl_obj = drop_table_indexes_ddl(tableObj, engine)
    ddl_obj = create_table_indexes_ddl(tableObj, engine)
    #all columns ddl_obj
    for k in tableObj.columns.keys():
        columnObj = tableObj.columns[k]
        ddl_obj = table_column_ddl(columnObj, tableObj, engine)
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 
def compare_with_physical_table(tableInstance,debug=None):
    debug_level = get_table_debug_level(tableInstance, debug)
    engine = tableInstance.session.bind.engine
    tableObj = tableInstance.model.__table__
    metadata = MetaData(bind=engine)
    table_name = tableInstance.model.__tablename__
    
    tableInstance.physical_table_is_synchronized = True
    tableInstance.unmapped_columns = 0
    tableInstance.new_columns = 0
    tableInstance.changed_columns = 0

    physical_table = Table(table_name, metadata, autoload=True)

    for c in physical_table.columns:
        if c.key not in tableObj.columns.keys():
            if int(debug_level) > 0:
                print(f'-unmapped field in table {tableInstance.model.__tablename__} : {c.key}')
            tableInstance.physical_table_is_synchronized = False
            tableInstance.unmapped_columns = tableInstance.unmapped_columns + 1
            
    for k in tableObj.columns.keys():
        if k not in physical_table.columns.keys():
            if int(debug_level) > 0:
                print(f'-missing field from table {tableInstance.model.__tablename__} : {c.key}')
            tableInstance.physical_table_is_synchronized=False
            tableInstance.new_columns = tableInstance.new_columns + 1

    for c in physical_table.columns:
        physical_table_column = physical_table.columns[c.key]
        if c.key in tableObj.columns.keys():
            model_column = tableObj.columns[c.key]
            physical_table_column_type = physical_table_column.type.compile(engine.dialect)
            model_column_type = model_column.type.compile(engine.dialect)
            if not physical_table_column_type == model_column_type:
                if int(debug_level) > 0:
                    print(f'-changed field in table {tableInstance.model.__tablename__} : {c.key} from {physical_table_column_type} to {model_column_type}')
                tableInstance.physical_table_is_synchronized=False
                tableInstance.changed_columns = tableInstance.changed_columns + 1
            else:
                model_column_ddl_string = table_column_ddl(model_column, tableObj, engine,debug_level - 1)
                table_column_ddl_string = table_column_ddl(physical_table_column, physical_table, engine,debug_level - 1)
                if not model_column_ddl_string == table_column_ddl_string:
                    if int(debug_level) > 0:
                        print(f'-changed field in table {tableInstance.model.__tablename__} : {c.key} from {table_column_ddl_string} to {model_column_ddl_string}')
                    tableInstance.physical_table_is_synchronized=False
                    tableInstance.changed_columns = tableInstance.changed_columns + 1
    #kill garbage
    del physical_table  #remove it from stack
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 
def synchronize_physical_table(tableInstance, copy_records=False, debug=None):
    debug_level = get_table_debug_level(tableInstance, debug)
    engine = tableInstance.session.bind.engine
    tableObj = tableInstance.model.__table__
    metadata = MetaData(bind=engine)
    table_name = tableInstance.model.__tablename__
    
    compare_with_physical_table(tableInstance, debug_level - 1)

    if not tableInstance.physical_table_is_synchronized:
        if tableInstance.new_columns > 0 and tableInstance.unmapped_columns == 0 and tableInstance.changed_columns == 0:
            engine=tableInstance.session.bind.engine
            metadata = MetaData(bind=engine)
            physical_table = Table(table_name, metadata, autoload=True)
            for k in tableObj.columns.keys():
                if k not in physical_table.columns.keys():
                    new_column = tableObj.columns[k]
                    add_column(tableInstance, new_column,debug_level-1)
            del physical_table
        else:
            recreate_table(tableInstance, copy_records, debug_level - 1)
        compare_with_physical_table(tableInstance,debug_level - 1)
    # for c in physical_table.columns:
    #     if c.key not in tableObj.columns.keys():
    #         #print(table_name, 'o unmapped field in table :',c.key)
    #         not_mapped_column = physical_table.columns[c.key]
    #         drop_column(tableInstance,not_mapped_column)

    # for k in tableObj.columns.keys():
    #     if k not in physical_table.columns.keys():
    #         #print(table_name, 'o missing field from table :', k)
    #         new_column = tableObj.columns[k]
    #         add_column(tableInstance,new_column)

    # for c in physical_table.columns:
    #     physical_table_column = physical_table.columns[c.key]
    #     if c.key in tableObj.columns.keys():
    #         model_column = tableObj.columns[c.key]
    #         physical_table_column_type = physical_table_column.type.compile(engine.dialect)
    #         model_column_type = model_column.type.compile(engine.dialect)
    #         if not physical_table_column_type == model_column_type:
    #             #print(table_name, 'o data type different :',c.key,'from :',physical_table_column_type,' to :',model_column_type)
    #             alter_column(tableInstance,model_column)
    
    # del physical_table #remove it from stack
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 
def add_columns_to_physical_table(tableInstance,debug=None):
    debug_level = get_table_debug_level(tableInstance, debug)
    engine = tableInstance.session.bind.engine
    tableObj = tableInstance.model.__table__
    metadata = MetaData(bind=engine)
    table_name = tableInstance.model.__tablename__
    
    compare_with_physical_table(tableInstance, debug_level - 1)
    if not tableInstance.physical_table_is_synchronized:
        if tableInstance.new_columns > 0:
            physical_table = Table(table_name, metadata, autoload=True)
            for k in tableObj.columns.keys():
                if k not in physical_table.columns.keys():
                    new_column = tableObj.columns[k]
                    add_column(tableInstance, new_column,debug_level - 1)
            del physical_table
    # for c in physical_table.columns:
    #     if c.key not in tableObj.columns.keys():
    #         #print(table_name, 'o unmapped field in table :',c.key)
    #         not_mapped_column = physical_table.columns[c.key]
    #         drop_column(tableInstance,not_mapped_column)

    # for k in tableObj.columns.keys():
    #     if k not in physical_table.columns.keys():
    #         #print(table_name, 'o missing field from table :', k)
    #         new_column = tableObj.columns[k]
    #         add_column(tableInstance,new_column)

    # for c in physical_table.columns:
    #     physical_table_column = physical_table.columns[c.key]
    #     if c.key in tableObj.columns.keys():
    #         model_column = tableObj.columns[c.key]
    #         physical_table_column_type = physical_table_column.type.compile(engine.dialect)
    #         model_column_type = model_column.type.compile(engine.dialect)
    #         if not physical_table_column_type == model_column_type:
    #             #print(table_name, 'o data type different :',c.key,'from :',physical_table_column_type,' to :',model_column_type)
    #             alter_column(tableInstance,model_column)
    
    # del physical_table #remove it from stack
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 
def add_column(tableInstance, columnObj,debug=None):
    debug_level = get_table_debug_level(tableInstance, debug)
    engine = tableInstance.session.bind.engine
    tableObj = tableInstance.model.__table__
    table_name = tableInstance.model.__tablename__
    ddl_string = add_table_column_ddl(columnObj, tableObj, engine,debug_level - 1)
    # if int(debug_level) > 0:
    #     msg = f"DDL:[{ddl_string}]"
    #     log_message(msg)    
    engine.execute(ddl_string)
    msg = f"table [[{table_name}]] [column {columnObj.name}] added with DDL:[{ddl_string}]"
    if int(debug_level) > 0:
        log_message(msg)        
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 
def drop_column(tableInstance, columnObj,debug=None):
    debug_level = get_table_debug_level(tableInstance, debug)
    engine = tableInstance.session.bind.engine
    tableObj = tableInstance.model.__table__
    table_name = tableInstance.model.__tablename__
    ddl_string=drop_table_column_ddl(columnObj,tableObj,engine,debug_level - 1)
    # if int(debug_level) > 0:
    #     msg = f"DDL:[{ddl_string}]"
    #     log_message(msg)    
    engine.execute(ddl_string)
    msg = f"table [[{table_name}]] [column {columnObj.name}] droped with DDL:[{ddl_string}]"
    if int(debug_level) > 0:
        log_message(msg)        
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 
def alter_column(tableInstance, columnObj,debug=None):
    debug_level = get_table_debug_level(tableInstance, debug)
    engine = tableInstance.session.bind.engine
    tableObj = tableInstance.model.__table__
    table_name = tableInstance.model.__tablename__
    ddl_string=alter_table_column_ddl(columnObj,tableObj,engine,debug_level - 1)
    # if int(debug_level) > 0:
    #     msg = f"DDL:[{ddl_string}]"
    #     log_message(msg)    
    engine.execute(ddl_string)
    msg = f"table [[{table_name}]] [column {columnObj.name}] altered with DDL:[{ddl_string}]"
    if int(debug_level) > 0:
        log_message(msg)        
# #::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
# #::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
# #::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
# # 
# #::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
# #::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
# #::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
def recreate_tables(dbmodelBase, engine,debug_level=1):
    tables_before=get_tables_directory(engine)
    # engine = tableInstance.session.bind.engine
    # tableObj = tableInstance.model.__table__
    # metadata = MetaData(bind=engine)
    # dbmodel.Base.metadata.create_all(bind=engine)
    dbmodelBase.metadata.create_all(bind=engine)
    tables_after = get_tables_directory(engine)
    ix=0
    for table_name in tables_after:
        if table_name not in tables_before:
            ix=ix+1
            if int(debug_level) > 0:
                msg = f'table [{table_name}] created'
                log_message(msg)
    if int(debug_level) > 0:
        msg = f'[{ix}] tables created in database [{engine}]'
        log_message(msg)
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 
def get_tables_directory(engine):
    m = MetaData()
    m.reflect(engine)
    tables_list=[]
    for table in m.tables.values():
        #print(table.name)
        tables_list.append(table.name)
        # for column in table.c:
        #     print(column.name)
    return tables_list
# #::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
# #::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
# #::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
# # get DDL commands from sqlalchemy
# #::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
# #::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
# #::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
def create_table_ddl(tableObj,engine,debug_level=-1):
    ddl_obj=ddl.CreateTable(tableObj)
    ddl_string=str(ddl_obj.compile(dialect=engine.dialect)).strip()
    if int(debug_level) > 0:
        msg = f"table [[{tableObj.name}]] create_table_DDL: [{ddl_string}]"
        log_message(msg)
    return ddl_string
#################################################    
def drop_table_ddl(tableObj,engine,debug_level=-1):
    ddl_obj = DropTable(tableObj)
    try:
        ddl_string=str(ddl_obj.compile(dialect=engine.dialect)).strip()
    except Exception as e:
        # print(e)
        ddl_string = ''
    if int(debug_level) > 0:
        msg = f"table [[{tableObj.name}]] drop_table_DDL: [{ddl_string}]"
        log_message(msg)
    return ddl_string
#################################################    
def clear_table_ddl(tableObj,engine,debug_level=-1):
    ddl_obj = tableObj.delete()
    try:
        ddl_string=str(ddl_obj.compile(dialect=engine.dialect)).strip()
    except Exception as e:
        print(e)
        # ddl_string = ''
    if int(debug_level) > 0:
        msg = f"table [[{tableObj.name}]] clear_table_DDL: [{ddl_string}]"
        log_message(msg)
    return ddl_string
#################################################    
def create_table_constraints_ddl(tableObj, engine,debug_level=-1):
    ddl_text=''
    constraints = tableObj.constraints
    for constraint in constraints:
        ddl_obj = AddConstraint(constraint)
        try:
            ddl_string=str(ddl_obj.compile(dialect=engine.dialect)).strip()
        except Exception as e:
            # if e.message.find('it has no name')<0:
            #     print(e)
            ddl_string = ''

        if ddl_string:
            if not ddl_text:
                ddl_text = ddl_string
            else:
                ddl_text = ddl_text + '\n' + ddl_string
    ddl_string=ddl_text
    if int(debug_level) > 0:
        msg = f"table [[{tableObj.name}]] create_table_constraints_DDL: [{ddl_string}]"
        log_message(msg)
    return ddl_string
#################################################    
def drop_table_constraints_ddl(tableObj, engine,debug_level=-1):
    ddl_text=''
    constraints = tableObj.constraints
    for constraint in constraints:
        ddl_obj = DropConstraint(constraint)
        try:
            ddl_string=str(ddl_obj.compile(dialect=engine.dialect)).strip()
        except Exception as e:
            # # if e. str(e.message).find('it has no name')<0:
            #     print(e)
            ddl_string = ''
        if ddl_string:
            if not ddl_text:
                ddl_text = ddl_string
            else:
                ddl_text = ddl_text + '\n' + ddl_string
    ddl_string=ddl_text
    if int(debug_level) > 0:
        msg = f"table [[{tableObj.name}]] drop_table_constraints_DDL: [{ddl_string}]"
        log_message(msg)
    return ddl_string
#################################################    
def create_table_indexes_ddl(tableObj, engine,debug_level=-1):
    ddl_text=''
    indexes = sorted(list(tableObj.indexes), key=lambda k: k.name,reverse=False)
    for index in indexes:
        ddl_obj = CreateIndex(index)
        try:
            ddl_string=str(ddl_obj.compile(dialect=engine.dialect)).strip()
        except Exception as e:
            # if e.message.find('it has no name')<0:
            #     print(e)
            ddl_string = ''
        if ddl_string:
            if not ddl_text:
                ddl_text = ddl_string
            else:
                ddl_text = ddl_text + '\n' + ddl_string    
    ddl_string=ddl_text
    if int(debug_level) > 0:
        msg = f"table [[{tableObj.name}]] create_table_indexes_DDL: [{ddl_string}]"
        log_message(msg)
    return ddl_string
#################################################    
def drop_table_indexes_ddl(tableObj, engine,debug_level=-1):
    ddl_text=''
    indexes = sorted(list(tableObj.indexes), key=lambda k: k.name,reverse=False)
    for index in indexes:
        ddl_obj = DropIndex(index)
        try:
            ddl_string=str(ddl_obj.compile(dialect=engine.dialect)).strip()
        except Exception as e:
            # print(e)
            ddl_string = ''
        if ddl_string:
            if not ddl_text:
                ddl_text = ddl_string
            else:
                ddl_text = ddl_text + '\n' + ddl_string    
    ddl_string=ddl_text
    if int(debug_level) > 0:
        msg = f"table [[{tableObj.name}]] drop_table_indexes_DDL: [{ddl_string}]"
        log_message(msg)
    return ddl_string
#################################################    
def add_table_column_ddl(columnObj,tableObj,engine,debug_level=-1):
    table_name = tableObj.name
    # column_name = columnObj.name
    # xcolumn_name = str(columnObj.compile(dialect=engine.dialect)).strip()
    # column_type = str(columnObj.type.compile(dialect=engine.dialect)).strip()
    # try:
    #     column_default = str(columnObj.default.compile(dialect=engine.dialect)).strip()
    # except Exception as e:
    #     # if e.message.find('it has no name')<0:
    #     #     print(e)
    #     column_default = ''
    column_ddl_string = table_column_ddl(columnObj, tableObj, engine,debug_level - 1)
    #ddl_string = f"ALTER TABLE {table_name} ADD COLUMN {column_name} {column_type}"    
    ddl_string = f"ALTER TABLE {table_name} ADD COLUMN {column_ddl_string}"
    if int(debug_level) > 0:
        msg = f"table [[{tableObj.name}]] add_table_column_DLL: [{ddl_string}]"
        log_message(msg)
    return ddl_string
#################################################    
def drop_table_column_ddl(columnObj,tableObj,engine,debug_level=-1):
    table_name = tableObj.name
    column_name = columnObj.name
    ddl_string=f"ALTER TABLE {table_name} DROP COLUMN {column_name}"
    if int(debug_level) > 0:
        msg = f"table [[{tableObj.name}]] drop_table_column_DDL: [{ddl_string}]"
        log_message(msg)
    return ddl_string
#################################################    
def alter_table_column_ddl(columnObj,tableObj,engine,debug_level=-1):
    table_name = tableObj.name
    # column_name = columnObj.name

    # xcolumn_name = str(columnObj.compile(dialect=engine.dialect)).strip()
    # column_type = str(columnObj.type.compile(dialect=engine.dialect)).strip()
    # try:
    #     column_default = str(columnObj.default.compile(dialect=engine.dialect)).strip()
    # except Exception as e:
    #     # if e.message.find('it has no name')<0:
    #     #     print(e)
    #     column_default = ''
    # try:
    #     column_default = str(columnObj.server_default.compile(dialect=engine.dialect)).strip()
    # except Exception as e:
    #     # if e.message.find('it has no name')<0:
    #     #     print(e)
    #     column_default = ''
    # ddl_string = f"ALTER TABLE {table_name} ALTER COLUMN {column_name} {column_type}"

    column_ddl_string = table_column_ddl(columnObj, tableObj, engine)
    #ddl_string = f"ALTER TABLE {table_name} ADD COLUMN {column_name} {column_type}"    
    ddl_string = f"ALTER TABLE {table_name} ALTER COLUMN {column_ddl_string}"
    if int(debug_level) > 0:
        msg = f"table [[{tableObj.name}]] alter_table_column_DDL: [{ddl_string}]"
        log_message(msg)
    return ddl_string
#################################################    
def table_column_ddl(columnObj,tableObj,engine,debug_level=-1):
    table_name = tableObj.name
    column_name = columnObj.name
    # xcolumn_name = str(columnObj.compile(dialect=engine.dialect)).strip()
    # print(xcolumn_name)
    # cname = columnObj.key
    
    # xcolumn_name = str(tableObj.c[cname].compile(dialect=engine.dialect)).strip()
    # print(xcolumn_name)
    column_type = str(columnObj.type.compile(dialect=engine.dialect)).strip()
    try:
        column_default = str(columnObj.default.compile(dialect=engine.dialect)).strip()
    except Exception as e:
        # print(e)
        column_default = ''
    try:
        column_default = str(columnObj.server_default.compile(dialect=engine.dialect)).strip()
    except Exception as e:
        # print(e)
        column_default = ''
    try:
        ddl_obj=ddl.CreateColumn(columnObj)
        ddl_string=str(ddl_obj.compile(dialect=engine.dialect)).strip()
    except Exception as e:
        # print(e)
        ddl_string = ''
    if not ddl_string:
        ddl_string = f"TABLE {table_name} COLUMN {column_name} {column_type} {column_default}"
    if int(debug_level) > 0:
        msg = f"table [[{tableObj.name}]] table_column_DDL: [{ddl_string}]"
        log_message(msg)
    return ddl_string
#################################################    
#::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
#::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
def get_table_debug_level(tableInstance, this_debug=None):
    this_debug_level = get_debug_option_as_level(this_debug)
    if this_debug_level >= 0:
        return this_debug_level
    try:
        debug_level1 = get_debug_option_as_level(thisApp.application_configuration.get('database_models_debug'))
    except:
        debug_level1 = -1
    try:
        debug_level2 = get_debug_option_as_level(thisApp.application_configuration.get('database_debug'))
    except:
        debug_level2 = -1
    try:
        debug_level3 = get_debug_option_as_level(thisApp.application_configuration.get('database_tables_debug'))
    except:
        debug_level3 = -1
    try:
        debug_level4 = get_debug_option_as_level(thisApp.application_configuration.get('database_admin_debug'))
    except:
        debug_level4 = -1

    table_model = tableInstance.model
    if hasattr(table_model, "_debug"):
        debug_level5 = get_debug_option_as_level(table_model._debug)
    else:
        debug_level5 = -1

    return max(debug_level1,debug_level2,debug_level3,debug_level4,debug_level5)
#::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::

#::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
#::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
msg = f'module [{module_id}] [[version {module_version}]] loaded.'
if thisApp.CONSOLE_ON:
    log_message(msg)
else:
    log_message(msg)
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 
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