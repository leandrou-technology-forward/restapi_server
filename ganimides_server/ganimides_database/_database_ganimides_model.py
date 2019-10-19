# coding=utf-8
#https://www.pythoncentral.io/sqlalchemy-orm-examples/
#https://towardsdatascience.com/sqlalchemy-python-tutorial-79a577141a91
#https://wakatime.com/blog/32-flask-part-1-sqlalchemy-models-to-json
#https://auth0.com/blog/sqlalchemy-orm-tutorial-for-python-developers/
import os
# from flask import Flask
from _onlineApp import thisApp
from _onlineApp import log_message
#from colorama import Fore as colors
from _onlineApp import print_changes
from _onlineApp import get_debug_option_as_level
from _colorServices import colorized_string

from flask import json
# from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm.attributes import QueryableAttribute
from sqlalchemy.orm import column_property
#from sqlalchemy_utils import UUIDType
#from _database_class_UUID import UUIDType,GUID,AUTO_INCREMENT_COUNTER
from _database_class_UUID import GUID
# import uuid
import base64
import uuid
import datetime
# _sysrand = SystemRandom()
# randbits = _sysrand.getrandbits
# choice = _sysrand.choice
#from wakatime_website import app
from sqlalchemy import Column, MetaData, Table, ForeignKey,Sequence,UniqueConstraint
from sqlalchemy import String, Integer, Float, BigInteger, DateTime, CHAR, VARCHAR, DECIMAL, Text, Boolean
from sqlalchemy import create_engine
from sqlalchemy.sql import func,text
from sqlalchemy import sql
from sqlalchemy import inspect
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import relationship, backref
 
#for dict support Not used
#from dictalchemy import DictableModel
#from slqlachemy.ext.declarative import declarative_base
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 

# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 
import time
import random
import socket
import hashlib
#import random

# a function which counts upwards
# i = 0
# def mydefault():
#     global i
#     i += 1
#     return i

#     # Column('id', Integer, primary_key=True, default=mydefault),

# def uniqueid():
#     seed = random.getrandbits(32)
#     seed=0
#     while True:
#        yield seed
#        seed += 1

# def xguid( *args ):
#     """
#     Generates a universally unique ID.
#     Any arguments only create more randomness.
#     """
#     t = 0
#     r = 0
    
#     t = ( time.time() * 1000 )
#     r = ( random.random()*100000000000000000)
#     try:
#         a = socket.gethostbyname( socket.gethostname() )
#     except:
#         # if we can't get a network address, just imagine one
#         a = random.random()*100000000000000000
#     data = str(str(t)+' '+str(r)+' '+str(a)+' '+str(args)).encode('utf-8')
#     data = hashlib.md5(data).hexdigest()

#     return data


# unique_sequence = uniqueid()
# id1 = next(unique_sequence)
# id2 = next(unique_sequence)
# id3 = next(unique_sequence)
# print(id1)
# print(id2)
# print(id3)
# print(xguid('aaa', 'cccc'))
# # exit(0)
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 
#Base = declarative_base(cls=DictableModel)
Base = declarative_base()
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 

# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 
# define a BaseModel class for all db table classes
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 
def get_uuid(what='?',col='?'):
    #print('====',what)
    #x=str(next(unique_sequence))
    #x=what+' '+col+' '+str(mydefault())
    #x='|'+what+'|'+col+'|'+xguid(what,col)+'|'
    x=str(uuid.uuid1(uuid._random_getnode()))
    #return get_uuid()
    #print_message(f"[UUID-SET] [[[{x}]]] [{col}] [[{what}]]")
    return x
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 
def get_secret_key():
    return base64.urlsafe_b64encode(os.urandom(128)).rstrip(b'=').decode('ascii')
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 
class BaseModel(Base):
    __abstract__ = True
    ########################################################################################
    def smart_locate_expression(self, locate_dict):
        """returns a dictionary with query fields based on primary_keys, unique_fields and other valid querable fields for this model."""
        from_primary_key={}
        from_other_fields = {}
        partial_pk = False
        for column in self.__table__.columns:
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
    ########################################################################################
    def valid_model_fields_dictionary(self, record_dict):
        """returns a dictionary with valid fields for this model."""
        valid_model_record={}
        columns = self.__table__.columns.keys()
        for key in record_dict:
            if key in columns:
                valid_model_record.update({key:record_dict[key]})
        return valid_model_record
    ########################################################################################
    def to_dict(self, method=''):
        """converts this model to dictionary(json)."""
        row_dict={}
        if hasattr(self, "_hidden_fields"):
            hidden_fields = self._hidden_fields
        else:
            hidden_fields=[]
        columns = self.__table__.columns.keys()
        for key in columns:
            if not key.startswith("_"):
                if key not in hidden_fields:
                    # val_old = getattr(self, key)
                    if method.upper().find('TEXT') >= 0 or method.upper().find('STRING') >= 0:
                        row_dict[key] = str(getattr(self, key))
                    else:
                        row_dict[key] = getattr(self, key)
        return row_dict
    ########################################################################################
    def input_validation(self, input_data={}):
        """apply ADD validations for this model."""
        ok = True
        messages=[]
        # row_dict={}
        # if hasattr(self, "_hidden_fields"):
        #     hidden_fields = self._hidden_fields
        # else:
        #     hidden_fields=[]
        # columns = self.__table__.columns.keys()
        # for key in columns:
        #     if not key.startswith("_"):
        #         if key not in hidden_fields:
        #             # val_old = getattr(self, key)
        #             if method.upper().find('TEXT') >= 0 or method.upper().find('STRING') >= 0:
        #                 row_dict[key] = str(getattr(self, key))
        #             else:
        #                 row_dict[key] = getattr(self, key)
        return (ok,messages)
    ########################################################################################
    def update_validation(self, input_data={}):
        """apply UPDATE validations for this model."""
        ok = True
        messages=[]
        # row_dict={}
        # if hasattr(self, "_hidden_fields"):
        #     hidden_fields = self._hidden_fields
        # else:
        #     hidden_fields=[]
        # columns = self.__table__.columns.keys()
        # for key in columns:
        #     if not key.startswith("_"):
        #         if key not in hidden_fields:
        #             # val_old = getattr(self, key)
        #             if method.upper().find('TEXT') >= 0 or method.upper().find('STRING') >= 0:
        #                 row_dict[key] = str(getattr(self, key))
        #             else:
        #                 row_dict[key] = getattr(self, key)
        return (ok,messages)
    ########################################################################################
    def update_from_dict(self,**kwargs):
        """Update this model with a dictionary."""
        changes = {}
        readonly_columns = []
        autoset_columns=[]
        _force = kwargs.pop("_force", False)
        # readonly=[]
        # if hasattr(self, "_readonly_fields"):
        #     readonly += self._readonly_fields
        # if hasattr(self, "_hidden_fields"):
        #     readonly += self._hidden_fields
        # columns = self.__table__.columns.keys()
        # for key in kwargs:
        #     #print(key)
        #     if key in columns:
        #         if not key.startswith("_"):
        #             if _force or key not in readonly:
        #                 val_old = getattr(self, key)
        #                 val_new = kwargs[key]
        #                 #print(key,val_old,val_new)
        #                 if str(val_old) != str(val_new):
        #                     changes[key] = {"old_value": val_old, "new_value": val_new}
        #                     setattr(self, key, val_new)
        # heading = '#>#'*printLevel+f"[{self.__tablename__}] [[changes]]:"
        # if self.debug_is_on() or debug: print_changes(heading, changes)
        # return changes
        if hasattr(self, "_readonly_fields"):
            readonly_columns += self._readonly_fields
        if hasattr(self, "_hidden_fields"):
            readonly_columns += self._hidden_fields
        for c in self.__table__.columns:
            if c.key not in readonly_columns:
                if c.info:
                    if type(c.info) == type({}):
                        if c.info.get('is_readOnly'):
                            readonly_columns.append(c.key)
                        elif c.info.get('is_rowUID'):
                            val_old = getattr(self, c.key)
                            if val_old == None:
                                val_new = get_uuid(self.__table__,c.key)
                                setattr(self, c.key, val_new)
                                autoset_columns.append(c.key)
                                changes[c.key] = {"old_value": val_old, "new_value": val_new}
                        elif c.info.get('is_autoSetTimestamp'):
                            val_old = getattr(self, c.key)
                            if str(val_old).isnumeric():
                                val_new = datetime.datetime.utcnow()
                                setattr(self, c.key, val_new)
                                autoset_columns.append(c.key)
                                changes[c.key] = {"old_value": val_old, "new_value": val_new}
                        elif c.info.get('is_autoIncrementCounter'):
                            val_old = getattr(self, c.key)
                            if str(val_old).isnumeric():
                                val_new = int(val_old) + 1
                                setattr(self, c.key, val_new)
                                autoset_columns.append(c.key)
                                changes[c.key] = {"old_value": val_old, "new_value": val_new}
                        
        for key in kwargs:
            if key in self.__table__.columns.keys():
                if not key.startswith("_"):
                    if key not in autoset_columns or _force:
                        if key not in readonly_columns or _force:
                            val_old = getattr(self, key)
                            val_new = kwargs[key]
                            if str(val_old) != str(val_new):
                                changes[key] = {"old_value": val_old, "new_value": val_new}
                                setattr(self, key, val_new)
        # heading = '#>#'*printLevel+f"[{self.__tablename__}] [[changes]]:"
        # if self.debug_is_on() or debug: print_changes(heading, changes)
        return changes
    ########################################################################################
    def debug_is_on(self):
        """Return the debug mode attribute of this model."""
        if hasattr(self, "_debug"):
            return self._debug
        else:
            debug=False
            try:
                xdebug = thisApp.application_configuration.database_models_debug
                if xdebug:
                    debug=thisApp.application_configuration.database_models_debug
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
            
            return debug
    ########################################################################################
    ########################################################################################
    def debug_level(self):
        """Return the debug level attribute of this model."""
        if hasattr(self, "_debug"):
            this_debug_level = get_debug_option_as_level(self._debug)
            if this_debug_level >= 0:
                return this_debug_level
        else:
            try:
                debug_level1 = get_debug_option_as_level(thisApp.application_configuration.database_models_debug)
            except:
                debug_level1 = -1
            try:
                debug_level2 = get_debug_option_as_level(thisApp.application_configuration.database_debug)
            except:
                debug_level2 = -1
            try:
                debug_level3 = get_debug_option_as_level(thisApp.application_configuration.database_tables_debug)
            except:
                debug_level3 = -1
            return max(debug_level1,debug_level2,debug_level3)
    ########################################################################################
    def get_unique_identifier(self, locate_dict):
        """returns a string representing the current object unique identifier i.e CLIENT philippos@gmail.com"""
        id_from_primary_key1 = self.__name__
        id_from_primary_key2 = self.__name__
        id_from_other = self.__name__
        id_from_unique_field = self.__name__
        pk = 0
        for column in self.__table__.columns:
            key = column.key
            if column.unique:
                val = str(getattr(self, key))
                if val:
                    id_from_unique_field = self.__name__ + ' ' + val
                    return id_from_unique_field
            elif column.primary_key:
                pk=pk+1
                val = str(getattr(self, key))
                id_from_primary_key1 = id_from_primary_key1 + " " + val
                id_from_primary_key2 = id_from_primary_key2 + f" {key}=" + val
            else:
                val = str(getattr(self, key))
                if val:
                    id_from_other = self.__name__  + f" {key}=" + val
        if pk==1:
            return id_from_primary_key1
        elif pk > 1:
            return id_from_primary_key2
        else:
            return id_from_other
    ########################################################################################
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

        # row_dict = {}
        # for column in self.__table__.columns:
        #     row_dict[column.name] = str(getattr(self, column.name))

        ret_data = {}

        for key in columns:
            if key.startswith("_"):
                continue
            check = "%s.%s" % (_path, key)
            if check in _hide or key in hidden:
                continue
            if check in show or key in default:
                ret_data[key] = getattr(self, key)
        columns = self.__table__.columns.keys()


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
    def xfrom_dict(self, kwargs):
        """Update this model with a dictionary."""

        _force = kwargs.pop("_force", False)

        readonly = self._readonly_fields if hasattr(self, "_readonly_fields") else []
        if hasattr(self, "_hidden_fields"):
            readonly += self._hidden_fields

        readonly += ["id", "created_at", "modified_at"]

        columns = self.__table__.columns.keys()
        relationships = self.__mapper__.relationships.keys()
        properties = dir(self)

        changes = {}

        for key in columns:
            if key.startswith("_"):
                continue
            allowed = True if _force or key not in readonly else False
            exists = True if key in kwargs else False
            if allowed and exists:
                val = getattr(self, key)
                if val != kwargs[key]:
                    changes[key] = {"old": val, "new": kwargs[key]}
                    setattr(self, key, kwargs[key])

        for rel in relationships:
            if key.startswith("_"):
                continue
            allowed = True if _force or rel not in readonly else False
            exists = True if rel in kwargs else False
            if allowed and exists:
                is_list = self.__mapper__.relationships[rel].uselist
                if is_list:
                    valid_ids = []
                    query = getattr(self, rel)
                    cls = self.__mapper__.relationships[rel].argument()
                    for item in kwargs[rel]:
                        if (
                            "id" in item
                            and query.filter_by(id=item["id"]).limit(1).count() == 1
                        ):
                            obj = cls.query.filter_by(id=item["id"]).first()
                            col_changes = obj.from_dict(**item)
                            if col_changes:
                                col_changes["id"] = str(item["id"])
                                if rel in changes:
                                    changes[rel].append(col_changes)
                                else:
                                    changes.update({rel: [col_changes]})
                            valid_ids.append(str(item["id"]))
                        else:
                            col = cls()
                            col_changes = col.from_dict(**item)
                            query.append(col)
                            db.session.flush()
                            if col_changes:
                                col_changes["id"] = str(col.id)
                                if rel in changes:
                                    changes[rel].append(col_changes)
                                else:
                                    changes.update({rel: [col_changes]})
                            valid_ids.append(str(col.id))

                    # delete rows from relationship that were not in kwargs[rel]
                    for item in query.filter(not_(cls.id.in_(valid_ids))).all():
                        col_changes = {"id": str(item.id), "deleted": True}
                        if rel in changes:
                            changes[rel].append(col_changes)
                        else:
                            changes.update({rel: [col_changes]})
                        db.session.delete(item)

                else:
                    val = getattr(self, rel)
                    if self.__mapper__.relationships[rel].query_class is not None:
                        if val is not None:
                            col_changes = val.from_dict(**kwargs[rel])
                            if col_changes:
                                changes.update({rel: col_changes})
                    else:
                        if val != kwargs[rel]:
                            setattr(self, rel, kwargs[rel])
                            changes[rel] = {"old": val, "new": kwargs[rel]}

        for key in list(set(properties) - set(columns) - set(relationships)):
            if key.startswith("_"):
                continue
            allowed = True if _force or key not in readonly else False
            exists = True if key in kwargs else False
            if allowed and exists and getattr(self.__class__, key).fset is not None:
                val = getattr(self, key)
                if hasattr(val, "to_dict"):
                    val = val.to_dict()
                changes[key] = {"old": val, "new": kwargs[key]}
                setattr(self, key, kwargs[key])

        return self
    ########################################################################################
    def get_model_changes(self):
        """
        Return a dictionary containing changes made to the model since it was 
        fetched from the database.

        The dictionary is of the form {'property_name': [old_value, new_value]}

        Example:
        user = get_user_by_id(420)
        >>> '<User id=402 email="business_email@gmail.com">'
        get_model_changes(user)
        >>> {}
        user.email = 'new_email@who-dis.biz'
        get_model_changes(user)
        >>> {'email': ['business_email@gmail.com', 'new_email@who-dis.biz']}
        """
        state = inspect(self)
        changes = {}
        for attr in state.attrs:
            hist = state.get_history(attr.key, True)
            if not hist.has_changes():
                continue
            old_value = hist.deleted[0] if hist.deleted else None
            new_value = hist.added[0] if hist.added else None
            changes[attr.key] = [old_value, new_value]
        return changes
    ########################################################################################
    def has_model_changed(self):
        return bool(self.get_model_changes())    
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 
# classes from the
#  database tables
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 
# my notes:
#   o __tablename__ = 'Test_Table' is the physical table name in database
#
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 
# db1
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 
class USER(BaseModel):
    __tablename__ = 'users'
    user_id = Column(VARCHAR(50), unique=True, index=True,info={'is_rowUID':True})
    email = Column(VARCHAR(255) ,primary_key=True, nullable=False)
    name = Column(VARCHAR(255))
    mobile = Column(VARCHAR(50))
    last_name = Column(VARCHAR(255))
    first_name = Column(VARCHAR(255))
    birth_date = Column(VARCHAR(50))
    title = Column(VARCHAR(50))
    phone = Column(VARCHAR(50))
    middle_name = Column(VARCHAR(50))
    status = Column(VARCHAR(50))
    confirmed = Column(Integer ,default=0)
    password = Column(VARCHAR(50))
    confirmed_timestamp = Column(DateTime)
    last_usage_timestamp = Column(DateTime, server_default=func.now(), onupdate=func.now(), info={'is_autoSetTimestamp': True})
    row_timestamp = Column(DateTime ,server_default=func.now(),info={'is_readOnly':True})
    password = Column(String())
    user_secretKey = Column(VARCHAR(128), default=get_secret_key)
    _default_fields = [
    "username",
    "joined_recently",
    ]
    _hidden_fields = [
    "password",
    ]
    _readonly_fields = [
    "email_confirmed",
    ]
    _debug = False
    @property
    def joined_recently(self):
        return self.row_timestamp > datetime.datetime.utcnow() - datetime.timedelta(days=3)
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 
# class CUSTOMER(BaseModel):
#     __tablename__ = 'customers'
#     client_id = Column(VARCHAR(50), unique=True, index=True,info={'is_rowUID':True})
#     client_secretKey = Column(VARCHAR(128), default=get_secret_key)
#     email = Column(VARCHAR(255) ,primary_key=True, nullable=False)
#     name = Column(VARCHAR(255))
#     client_type = Column(VARCHAR(50), default='')
#     mobile = Column(VARCHAR(50))
#     last_name = Column(VARCHAR(255))
#     first_name = Column(VARCHAR(255))
#     birth_date = Column(VARCHAR(50))
#     title = Column(VARCHAR(50))
#     phone = Column(VARCHAR(50))
#     middle_name = Column(VARCHAR(50))
#     status = Column(VARCHAR(50))
#     confirmed = Column(Integer ,default=0)
#     password = Column(VARCHAR(50))
#     confirmed_timestamp = Column(DateTime)
#     last_usage_timestamp = Column(DateTime, server_default=func.now(), onupdate=func.now(), info={'is_autoSetTimestamp': True})
#     row_timestamp = Column(DateTime ,server_default=func.now(),info={'is_readOnly':True})
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 
class DEPARTMENT(Base):
    __tablename__ = 'departments'
    id = Column(Integer, autoincrement=True, primary_key=True)
    name = Column(String,unique=True)
    employees = relationship(
        'EMPLOYEE',
        secondary='department_employee_links'
    ) 
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 
class EMPLOYEE(Base):
    __tablename__ = 'employees'
    id = Column(Integer, autoincrement=True, primary_key=True)
    name = Column(String,unique=True)
    hired_on = Column(DateTime,default=func.now())
    departments = relationship(
        DEPARTMENT,
        secondary='department_employee_links'
    )
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 
class DEPARTMENT_EMPLOYEE_LINK(Base):
    __tablename__ = 'department_employee_links'
    department_id = Column(Integer, ForeignKey(DEPARTMENT.id), primary_key=True)
    employee_id = Column(Integer, ForeignKey('employees.id'), primary_key=True)
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 
# db2
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 
class SUBSCRIPTION(BaseModel):
    __tablename__ = 'api_subscriptions'
    subscription_id = Column(VARCHAR(50), unique=True, index=True,info={'is_rowUID':True})
    user_id = Column(VARCHAR(50) ,unique=True, nullable=False)
    client_id = Column(VARCHAR(50) ,unique=True, nullable=False)
    email = Column(VARCHAR(255) ,primary_key=True, nullable=False)
    name = Column(VARCHAR(255))
    mobile = Column(VARCHAR(50))
    last_name = Column(VARCHAR(255))
    first_name = Column(VARCHAR(255))
    birth_date = Column(VARCHAR(50))
    title = Column(VARCHAR(50))
    phone = Column(VARCHAR(50))
    middle_name = Column(VARCHAR(50))
    status = Column(VARCHAR(50))
    subscription_secretKey = Column(VARCHAR(128), default=get_secret_key)
    client_secretKey = Column(VARCHAR(128), default=get_secret_key)
    row_timestamp = Column(DateTime ,server_default=func.now(),info={'is_readOnly':True})
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 
class API(BaseModel):
    __tablename__ = 'api_master'
    api_id = Column(VARCHAR(50), unique=False, index=True,info={'is_rowUID':True})
    api_name = Column(VARCHAR(255) ,primary_key=True, nullable=False)
    status = Column(VARCHAR(50), default='Active')
    last_usage_timestamp = Column(DateTime, server_default=func.now(), onupdate=func.now(), info={'is_autoSetTimestamp': True})
    times_used = Column(Integer, default=0, server_default=text('0'),info={'is_autoIncrementCounter':True})
    row_timestamp = Column(DateTime ,server_default=func.now(),info={'is_readOnly':True})
    _debug = False
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 
class CLIENT(BaseModel):
    __tablename__ = 'clients'
    client_id = Column(VARCHAR(50), unique=True, index=True,info={'is_rowUID':True})
    email = Column(VARCHAR(255) ,primary_key=True, nullable=False)
    client_type = Column(VARCHAR(50) ,primary_key=True, nullable=False ,default='user')
    name = Column(VARCHAR(255))
    client_secretKey = Column(VARCHAR(128), default=get_secret_key)
    mobile = Column(VARCHAR(50))
    last_name = Column(VARCHAR(255))
    first_name = Column(VARCHAR(255))
    birth_date = Column(VARCHAR(50))
    title = Column(VARCHAR(50))
    phone = Column(VARCHAR(50))
    middle_name = Column(VARCHAR(50))
    status = Column(VARCHAR(50))
    confirmed = Column(Integer ,default=0)
    mobile_confirmed = Column(Integer ,default=0)
    email_confirmed = Column(Integer ,default=0)
    language = Column(VARCHAR(50), default='En')
    password = Column(VARCHAR(50))
    confirmed_timestamp = Column(DateTime)
    mobile_confirmed_timestamp = Column(DateTime)
    email_confirmed_timestamp = Column(DateTime)
    last_usage_timestamp = Column(DateTime, server_default=func.now(), onupdate=func.now(), info={'is_autoSetTimestamp': True})
    row_timestamp = Column(DateTime ,server_default=func.now(),info={'is_readOnly':True})
    geolocation_lat = Column(VARCHAR(50))
    geolocation_lon = Column(VARCHAR(50))
    last_usage_geolocation_lat = Column(VARCHAR(50))
    last_usage_geolocation_lon = Column(VARCHAR(50))   
    bank_subscriptions = relationship("BANK_SUBSCRIPTION")
    bank_accounts = relationship("BANK_ACCOUNT")
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 
class APPLICATION(BaseModel):
    __tablename__ = 'applications'
    application_id = Column(VARCHAR(50), unique=True, index=True,info={'is_rowUID':True})
    application_name = Column(Text ,primary_key=True, nullable=False ,unique=True, index=True)
    subscription_id = Column(VARCHAR(50) ,primary_key=True, nullable=False)
    application_email = Column(Text)
    application_redirect_uri = Column(Text)
    client_id = Column(VARCHAR(50) ,unique=False, nullable=False)
    client_secretKey = Column(VARCHAR(128), default=get_secret_key)
    subscription_secretKey = Column(VARCHAR(128), default=get_secret_key)
    status = Column(VARCHAR(50))
    language = Column(VARCHAR(50), default='En')
    row_timestamp = Column(DateTime ,server_default=func.now(),info={'is_readOnly':True})
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 
class APPLICATION_API(BaseModel):
    __tablename__ = 'application_apis'
    application_api_id = Column(VARCHAR(50), unique=True, index=True,info={'is_rowUID':True})
    api_name = Column(VARCHAR(255) ,ForeignKey(API.api_name,name='fk_apis_api_name') ,primary_key=True, nullable=False)
    application_name = Column(VARCHAR(255) ,ForeignKey(APPLICATION.application_name,name='fk_applications_application_name') ,primary_key=True, nullable=False)
    subscription_id = Column(VARCHAR(50),ForeignKey(SUBSCRIPTION.subscription_id,name='fk_subscriptions_subscription_id'))
    status = Column(VARCHAR(50) ,default='Active')
    last_usage_timestamp = Column(DateTime, server_default=func.now(), onupdate=func.now(), info={'is_autoSetTimestamp': True})
    times_used = Column(Integer, default=0, server_default=text('0'),info={'is_autoIncrementCounter':True})
    row_timestamp = Column(DateTime ,server_default=func.now(),info={'is_readOnly':True})
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 
class APPLICATION_USER(BaseModel):
    __tablename__ = 'application_users'
    application_user_id = Column(VARCHAR(50), unique=True, index=True,info={'is_rowUID':True})
    application_name = Column(VARCHAR(255) ,ForeignKey(APPLICATION.application_name,name='fk_applications_application_name') ,primary_key=True, nullable=False)
    user_role = Column(VARCHAR(50) ,primary_key=True, default='')
    client_id = Column(VARCHAR(50), ForeignKey(CLIENT.client_id, name='fk_clients_client_id', ondelete='CASCADE'),primary_key=True)
    status = Column(VARCHAR(50) ,default='Active')
    email = Column(VARCHAR(255))
    mobile = Column(VARCHAR(50))
    geolocation_lat = Column(VARCHAR(50))
    geolocation_lon = Column(VARCHAR(50))
    last_usage_geolocation_lat = Column(VARCHAR(50))
    last_usage_geolocation_lon = Column(VARCHAR(50))
    row_timestamp = Column(DateTime ,server_default=func.now(),info={'is_readOnly':True})
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 
class APPLICATION_TEMPLATE(BaseModel):
    __tablename__ = 'application_templates'
    template_id = Column(VARCHAR(50), unique=True, index=True,info={'is_rowUID':True})
    application_name = Column(VARCHAR(255) ,ForeignKey(APPLICATION.application_name,name='fk_applications_application_name') ,primary_key=True, nullable=False)
    template_name = Column(VARCHAR(255) ,primary_key=True, nullable=False)
    language = Column(VARCHAR(50), primary_key=True, nullable=False, default='En')
    subject = Column(VARCHAR(255) , default='')
    text = Column(Text , default='')
    html = Column(Text , default='')
    row_timestamp = Column(DateTime ,server_default=func.now(),info={'is_readOnly':True})
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 
class DEVICE(BaseModel):
    __tablename__ = 'devices'
    device_uid = Column(VARCHAR(255) ,primary_key=True, nullable=False)
    status = Column(VARCHAR(50))
    last_usage_geolocation_lat = Column(VARCHAR(50))
    last_usage_geolocation_lon = Column(VARCHAR(50))
    last_usage_timestamp = Column(DateTime, server_default=func.now(), onupdate=func.now(), info={'is_autoSetTimestamp': True})
    times_used = Column(Integer, default=0, server_default=text('0'),info={'is_autoIncrementCounter':True})
    row_timestamp = Column(DateTime ,server_default=func.now(),info={'is_readOnly':True})
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 
class DEVICE_USAGE(BaseModel):
    __tablename__ = 'device_usage'
    device_usage_id = Column(VARCHAR(50),  unique=True, index=True,info={'is_rowUID':True})
    device_uid = Column(VARCHAR(255) ,ForeignKey(DEVICE.device_uid, name='fk_devices_device_uid', ondelete='CASCADE') ,primary_key=True, nullable=False)
    client_id = Column(VARCHAR(50) ,primary_key=True, nullable=False)
    application_name = Column(VARCHAR(50), primary_key=True, nullable=False, default=0)
    geolocation_lon = Column(VARCHAR(50), primary_key=True, nullable=False, default=0)
    geolocation_lat = Column(VARCHAR(50), primary_key=True, nullable=False, default=0)
    last_usage_timestamp = Column(DateTime, server_default=func.now(), onupdate=func.now(), info={'is_autoSetTimestamp': True})
    times_used = Column(Integer, default=0, server_default=text('0'),info={'is_autoIncrementCounter':True})    
    row_timestamp = Column(DateTime ,server_default=func.now(),info={'is_readOnly':True})
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 
class CLIENT_DEVICE(BaseModel):
    __tablename__ = 'client_devices'
    client_device_id = Column(VARCHAR(50),  unique=True, index=True,info={'is_rowUID':True})
    device_uid = Column(VARCHAR(255) ,ForeignKey(DEVICE.device_uid, name='fk_devices_device_uid', ondelete='CASCADE') ,primary_key=True, nullable=False)
    client_id = Column(VARCHAR(50) ,ForeignKey(CLIENT.client_id, name='fk_clients_client_id', ondelete='CASCADE') ,primary_key=True, nullable=False)
    application_name = Column(VARCHAR(256) ,ForeignKey(APPLICATION.application_name, name='fk_applications_application_name', ondelete='CASCADE') ,primary_key=True, nullable=False)
    status = Column(VARCHAR(50) ,default='Active')
    last_usage_timestamp = Column(DateTime, server_default=func.now(), onupdate=func.now(), info={'is_autoSetTimestamp': True})
    times_used = Column(Integer, default='0', server_default=text('0'),info={'is_autoIncrementCounter':True})
    row_timestamp = Column(DateTime ,server_default=func.now(),info={'is_readOnly':True})
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 
class CLIENT_CONFIRMATION(BaseModel):
    __tablename__ = 'clients_confirmations'
    confirmation_id = Column(VARCHAR(50), unique=True, index=True,info={'is_rowUID':True})
    email = Column(VARCHAR(255) ,primary_key=True, nullable=False, default='')
    mobile = Column(VARCHAR(50), primary_key=True, nullable=False, default='')
    status = Column(VARCHAR(50), primary_key=False, default='Sent')
    token = Column(VARCHAR(255), primary_key=False, default='')
    token = Column(VARCHAR(255), primary_key=False, default='')
    confirmed = Column(Integer ,default=0)
    confirmed_timestamp = Column(DateTime)
    row_timestamp = Column(DateTime ,server_default=func.now(),info={'is_readOnly':True})
    send_timestamp = Column(DateTime ,server_default=func.now())
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 
class VERIFICATION(BaseModel):
    __tablename__ = 'verifications'
    verification_id = Column(VARCHAR(50), primary_key=True, unique=True, index=True,info={'is_rowUID':True})
    verification_token = Column(VARCHAR(255), default='')
    verification_code = Column(VARCHAR(50), default='')
    verification_entity = Column(VARCHAR(50), default='')
    send_method = Column(VARCHAR(50), default='')
    send_provider = Column(VARCHAR(50), default='')
    send_ticket = Column(VARCHAR(50), default='')
    send_timestamp = Column(DateTime ,server_default=func.now())
    expiry_timestamp = Column(DateTime, server_default=func.now())
    mobile = Column(VARCHAR(50), default='')
    email = Column(VARCHAR(255), default='')
    application_name = Column(VARCHAR(50), nullable=False, default='')
    client_id = Column(VARCHAR(50) ,ForeignKey(CLIENT.client_id, name='fk_clients_client_id', ondelete='CASCADE') ,primary_key=False, nullable=False)
    status = Column(VARCHAR(50), primary_key=False, default='')
    verification_timestamp = Column(DateTime)
    row_timestamp = Column(DateTime ,server_default=func.now(),info={'is_readOnly':True})
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 
class EMAIL(BaseModel):
    __tablename__ = 'emails'
    email_id = Column(VARCHAR(50), primary_key=True, unique=True, index=True,info={'is_rowUID':True})
    sender = Column(VARCHAR(255), default='')
    recipient = Column(VARCHAR(255), default='')
    cc = Column(VARCHAR(255), default='')
    bcc = Column(VARCHAR(255), default='')
    subject = Column(VARCHAR(255), default='')
    text_body = Column(Text, default='')
    html_body = Column(Text, default='')
    language = Column(VARCHAR(50), default='')
    email_template = Column(VARCHAR(255), default='')
    application_name = Column(VARCHAR(50), default='')
    attachments = Column(VARCHAR(255), default='')
    data_record = Column(Text, default='')
    send_provider = Column(VARCHAR(50), default='')
    send_ticket = Column(VARCHAR(50), default='')
    provider_reply = Column(Text, default='')
    reply_code = Column(VARCHAR(50), default='')
    reply_message = Column(VARCHAR(255), default='')
    send_timestamp = Column(DateTime ,server_default=func.now())
    row_timestamp = Column(DateTime ,server_default=func.now(),info={'is_readOnly':True})
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 
class SMS(BaseModel):
    __tablename__ = 'sms'
    sms_id = Column(VARCHAR(50), primary_key=True, unique=True, index=True,info={'is_rowUID':True})
    sender = Column(VARCHAR(255), default='')
    recipient = Column(VARCHAR(255), default='')
    cc = Column(VARCHAR(255), default='')
    bcc = Column(VARCHAR(255), default='')
    message = Column(VARCHAR(255), default='')
    language = Column(VARCHAR(50), default='')
    sms_template = Column(VARCHAR(255), default='')
    application_name = Column(VARCHAR(50), default='')
    data_record = Column(Text, default='')
    send_provider = Column(VARCHAR(50), default='')
    send_ticket = Column(VARCHAR(50), default='')
    provider_reply = Column(Text, default='')
    reply_code = Column(VARCHAR(50), default='')
    reply_message = Column(VARCHAR(255), default='')
    send_timestamp = Column(DateTime ,server_default=func.now())
    row_timestamp = Column(DateTime ,server_default=func.now(),info={'is_readOnly':True})
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 
# application_apis_association = Table('application_apis', BaseModel.metadata,
#     Column('application_id', VARCHAR(50), ForeignKey('applications.application_id')),
#     Column('api_id', VARCHAR(50), ForeignKey('api_master.api_id')))
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 
class SERVICE_PROVIDER(BaseModel):
    __tablename__ = 'service_providers'
    service_provider_id = Column(VARCHAR(50), unique=True, index=True,info={'is_rowUID':True})
    client_id = Column(VARCHAR(50), ForeignKey(CLIENT.client_id, name='fk_clients_client_id', ondelete='CASCADE'))
    email = Column(VARCHAR(255) ,primary_key=True, nullable=False)
    name = Column(VARCHAR(255))
    service_provider_secretKey = Column(VARCHAR(128), default=get_secret_key)
    mobile = Column(VARCHAR(50))
    title = Column(VARCHAR(50))
    last_name = Column(VARCHAR(255))
    middle_name = Column(VARCHAR(50))
    first_name = Column(VARCHAR(255))
    phone = Column(VARCHAR(50))
    status = Column(VARCHAR(50))
    confirmed = Column(Integer ,default=0)
    password = Column(VARCHAR(50))
    row_timestamp = Column(DateTime ,server_default=func.now(),info={'is_readOnly':True})
    confirmed_timestamp = Column(DateTime)
    last_usage_timestamp = Column(DateTime, server_default=func.now(), onupdate=func.now(), info={'is_autoSetTimestamp': True})
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 
class TOKEN(BaseModel):
    __tablename__ = 'tokens'
    token_id = Column(Integer, autoincrement=True,primary_key=True)
    token = Column(VARCHAR(128), default=get_secret_key)
    expiryDT = Column(DateTime)
    status = Column(VARCHAR(50) ,default='Active')
    duration_seconds = Column(Integer ,default=3600)
    application_name = Column(VARCHAR(255))
    application_client_id = Column(VARCHAR(255))
    application_client_secretKey = Column(VARCHAR(255))
    token_type = Column(VARCHAR(50) ,default='bearer')
    token_scope = Column(VARCHAR(50) ,default='application_service')
    grant_type = Column(VARCHAR(50) ,default='client_credentials')
    device_uid = Column(VARCHAR(255))
    client_id = Column(VARCHAR(50))
    client_secretKey = Column(VARCHAR(128), default=get_secret_key)
    row_timestamp = Column(DateTime ,server_default=func.now(),info={'is_readOnly':True})
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 
# db3
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 
class MERCHANT(BaseModel):
    __tablename__ = 'merchants'
    merchant_id = Column(VARCHAR(50), unique=True, index=True,info={'is_rowUID':True})
    name = Column(VARCHAR(255) ,primary_key=True, nullable=False)
    client_id = Column(VARCHAR(50), ForeignKey(CLIENT.client_id, name='fk_clients_client_id', ondelete='CASCADE'))
    email = Column(VARCHAR(255) ,unique=True, index=True)
    mobile = Column(VARCHAR(255))
    merchant_secretKey = Column(VARCHAR(128), default=get_secret_key)
    merchant_code = Column(VARCHAR(255))
    merchant_store = Column(VARCHAR(255))
    terminalID = Column(VARCHAR(255))
    branchID = Column(VARCHAR(255))
    transactionID = Column(VARCHAR(255))
    address = Column(VARCHAR(255))
    phone = Column(VARCHAR(50))
    shortAddress = Column(VARCHAR(255))
    payments_currency = Column(VARCHAR(3) ,default='EUR')
    merchant_logo = Column(Text)
    merchant_logo_file = Column(Text)
    bank_account_id = Column(VARCHAR(255))
    bank_subscription_id = Column(VARCHAR(255))
    bank_code = Column(VARCHAR(50))
    bank_subscriptionID = Column(VARCHAR(50))
    bank_accountID = Column(VARCHAR(50))
    status = Column(VARCHAR(50))
    row_timestamp = Column(DateTime ,server_default=func.now(),info={'is_readOnly':True})
    points_of_sale = relationship("POINT_OF_SALE")
    employees = relationship("MERCHANT_EMPLOYEE")
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 
class RETAIL_STORE(BaseModel):
    __tablename__ = 'retail_stores'
    retail_store_id = Column(VARCHAR(50), index=True,info={'is_rowUID':True})
    merchant_id = Column(VARCHAR(50), ForeignKey(MERCHANT.merchant_id, name='fk_merchants_merchant_id', ondelete='CASCADE'), primary_key=True)
    name = Column(VARCHAR(255) ,primary_key=True, nullable=False)
    geolocation_lat = Column(VARCHAR(50))
    geolocation_lon = Column(VARCHAR(50))
    email = Column(VARCHAR(255))
    mobile = Column(VARCHAR(255))
    status = Column(VARCHAR(50))
    row_timestamp = Column(DateTime ,server_default=func.now(),info={'is_readOnly':True})
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 
class POINT_OF_SALE(BaseModel):
    __tablename__ = 'points_of_sale'
    pointofsale_id = Column(VARCHAR(50), unique=True, index=True,info={'is_rowUID':True})
    merchant_id = Column(VARCHAR(50) ,ForeignKey(MERCHANT.merchant_id,name='fk_merchants_merchant_id', ondelete='CASCADE') ,primary_key=True, nullable=False)
    name = Column(VARCHAR(255) ,primary_key=True, nullable=False)
    retail_store_id = Column(VARCHAR(50), ForeignKey(RETAIL_STORE.retail_store_id,name='fk_retail_stores_retail_store_id', ondelete='CASCADE'))
    terminalID = Column(VARCHAR(255))
    pointofsale_secretKey = Column(VARCHAR(128), default=get_secret_key)
    pointofsale_code = Column(VARCHAR(50))
    merchant_code = Column(VARCHAR(255))
    merchant_store = Column(VARCHAR(255))
    merchant_name = Column(VARCHAR(255))
    branchID = Column(VARCHAR(255))
    transactionID = Column(VARCHAR(255))
    address = Column(VARCHAR(255))
    shortAddress = Column(VARCHAR(255))
    email = Column(VARCHAR(255))
    mobile = Column(VARCHAR(255))
    geolocation_lat = Column(VARCHAR(50) ,default=0)
    geolocation_lon = Column(VARCHAR(50) ,default=0)
    bank_account_id = Column(VARCHAR(255))
    bank_subscription_id = Column(VARCHAR(255))
    bank_code = Column(VARCHAR(50))
    bank_subscriptionID = Column(VARCHAR(50))
    bank_accountID = Column(VARCHAR(50))
    payments_currency = Column(VARCHAR(3) ,default='EUR')
    signed_tellerID = Column(VARCHAR(50))
    signed_tellerID_timestamp = Column(DateTime)
    signed_tellerID_expiry_timestamp = Column(DateTime)
    signed_tellerID_geolocation_lat = Column(VARCHAR(50) ,default=0)
    signed_tellerID_geolocation_lon = Column(VARCHAR(50) ,default=0)
    status = Column(VARCHAR(50))
    row_timestamp = Column(DateTime ,server_default=func.now(),info={'is_readOnly':True})
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 
class SERVICE_POINT(BaseModel):
    __tablename__ = 'service_points'
    service_point_id = Column(VARCHAR(50), unique=True, index=True,info={'is_rowUID':True})
    retail_store_id = Column(VARCHAR(50), ForeignKey(RETAIL_STORE.retail_store_id, name='fk_retail_store_retail_store_id', ondelete='CASCADE'), primary_key=True)
    name = Column(VARCHAR(255), primary_key=True)
    pointofsale_id = Column(VARCHAR(50), ForeignKey(POINT_OF_SALE.pointofsale_id, name='fk_point_of_sale_pointofsale_id', ondelete='CASCADE'))
    geolocation_lat = Column(VARCHAR(50))
    geolocation_lon = Column(VARCHAR(50))
    email = Column(VARCHAR(255))
    mobile = Column(VARCHAR(255))
    status = Column(VARCHAR(50))
    row_timestamp = Column(DateTime ,server_default=func.now(),info={'is_readOnly':True})
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 
class MERCHANT_EMPLOYEE(BaseModel):
    __tablename__ = 'merchant_employees'
    employee_id = Column(VARCHAR(50),  unique=True, index=True,info={'is_rowUID':True})
    merchant_id = Column(VARCHAR(50) ,ForeignKey(MERCHANT.merchant_id,name='fk_merchants_merchant_id', ondelete='CASCADE') ,primary_key=True, nullable=False)
    employee_code = Column(VARCHAR(50) ,primary_key=True, nullable=False)
    name = Column(VARCHAR(255))
    employee_secretKey = Column(VARCHAR(128), default=get_secret_key)
    # merchant_code = Column(VARCHAR(255))
    # merchant_store = Column(VARCHAR(255))
    # merchant_name = Column(VARCHAR(255))
    last_signon_pointofsale_id = Column(VARCHAR(50))
    last_signon_timestamp = Column(DateTime)
    last_signoff_timestamp = Column(DateTime)
    last_signon_expiry_timestamp = Column(DateTime)
    last_signon_geolocation_lat = Column(VARCHAR(50) ,default=0)
    last_signon_geolocation_lon = Column(VARCHAR(50) ,default=0)
    status = Column(VARCHAR(50))
    row_timestamp = Column(DateTime ,server_default=func.now(),info={'is_readOnly':True})
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 
class CONSUMER(BaseModel):
    __tablename__ = 'consumers'
    consumer_id = Column(VARCHAR(50),  unique=True, index=True,info={'is_rowUID':True})
    email = Column(VARCHAR(255) ,primary_key=True, nullable=False)
    client_id = Column(VARCHAR(50) ,ForeignKey(CLIENT.client_id,name='fk_clients_client_id', ondelete='CASCADE'))
    mobile = Column(VARCHAR(255))
    consumer_secretKey = Column(VARCHAR(128), default=get_secret_key)
    name = Column(VARCHAR(255))
    status = Column(VARCHAR(50))
    row_timestamp = Column(DateTime ,server_default=func.now(),info={'is_readOnly':True})
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 
class CUSTOMER_SERVICE_ASSISTANT(BaseModel):
    __tablename__ = 'customer_service_assistant'
    id = Column(VARCHAR(50),  unique=True, index=True,info={'is_rowUID':True})
    name = Column(VARCHAR(255))
    merchant_id = Column(VARCHAR(50) ,ForeignKey(MERCHANT.merchant_id,name='fk_merchants_merchant_id', ondelete='CASCADE') ,primary_key=True, nullable=False)
    employee_code = Column(VARCHAR(50) ,primary_key=True, nullable=False)
    retail_store_id = Column(VARCHAR(50), ForeignKey(RETAIL_STORE.retail_store_id, name='fk_retail_store_retail_store_id', ondelete='CASCADE'))
    pointofsale_id = Column(VARCHAR(50), ForeignKey(POINT_OF_SALE.pointofsale_id, name='fk_point_of_sale_pointofsale_id', ondelete='CASCADE'))
    employee_secretKey = Column(VARCHAR(128), default=get_secret_key)
    client_id = Column(VARCHAR(50), ForeignKey(CLIENT.client_id, name='fk_clients_client_id', ondelete='CASCADE'))
    email = Column(VARCHAR(255))
    mobile = Column(VARCHAR(255))
    last_signon_pointofsale_id = Column(VARCHAR(50))
    last_signon_timestamp = Column(DateTime)
    last_signoff_timestamp = Column(DateTime)
    last_signon_expiry_timestamp = Column(DateTime)
    last_signon_geolocation_lat = Column(VARCHAR(50) ,default=0)
    last_signon_geolocation_lon = Column(VARCHAR(50) ,default=0)
    status = Column(VARCHAR(50))
    row_timestamp = Column(DateTime ,server_default=func.now(),info={'is_readOnly':True})
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 
# db4
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 
class BANK(BaseModel):
    __tablename__ = 'banks'
    bank_id = Column(VARCHAR(50),  unique=True, index=True,info={'is_rowUID':True})
    bank_code = Column(VARCHAR(50) ,primary_key=True, nullable=False)
    bank_BIC= Column(VARCHAR(50) ,unique=True, index=True)
    bank_SWIFT = Column(VARCHAR(50))
    bank_short_code = Column(VARCHAR(50))
    bank_name = Column(VARCHAR(255))
    status = Column(VARCHAR(50))
    row_timestamp = Column(DateTime ,server_default=func.now(),info={'is_readOnly':True})
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 
class BANK_SUBSCRIPTION(BaseModel):
    __tablename__ = 'bank_subscriptions'
    bank_subscription_id = Column(VARCHAR(50),  unique=True, index=True,info={'is_rowUID':True})
    bank_code = Column(VARCHAR(50) ,ForeignKey(BANK.bank_code,name='fk_banks_bank_code', ondelete='CASCADE') ,primary_key=True, nullable=False)
    bank_subscriptionID = Column(VARCHAR(50) ,primary_key=True, nullable=False)
    client_id = Column(VARCHAR(50) ,ForeignKey(CLIENT.client_id,name='fk_clients_client_id', ondelete='CASCADE') ,primary_key=True, nullable=False)
    application_id = Column(VARCHAR(50) ,ForeignKey(APPLICATION.application_id,name='fk_applications_application_id', ondelete='CASCADE'))
    application_name = Column(VARCHAR(255))
    client_type = Column(VARCHAR(255))
    client_name = Column(VARCHAR(255))
    authorization_code = Column(VARCHAR(255))
    authorization_token = Column(VARCHAR(255))
    payments_limit = Column(Integer ,default=0)
    payments_amount = Column(Integer ,default=0)
    payments_currency = Column(VARCHAR(10))
    account_allow_transactionHistory = Column(Integer ,default=0)
    account_allow_balance = Column(Integer ,default=0)
    account_allow_details = Column(Integer ,default=0)
    account_allow_checkFundsAvailability = Column(Integer ,default=0)
    status = Column(VARCHAR(50))
    row_timestamp = Column(DateTime ,server_default=func.now(),info={'is_readOnly':True})
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 
class BANK_AUTHORIZATION(BaseModel):
    __tablename__ = 'bank_authorizations'
    bank_authorization_id = Column(VARCHAR(50),  primary_key=True, unique=True, index=True,info={'is_rowUID':True})
    status = Column(VARCHAR(50))
    bank_code = Column(VARCHAR(50) ,ForeignKey(BANK.bank_code,name='fk_banks_bank_code', ondelete='CASCADE'))
    client_id = Column(VARCHAR(50) ,ForeignKey(CLIENT.client_id,name='fk_clients_client_id', ondelete='CASCADE'))
    application_id = Column(VARCHAR(50) ,ForeignKey(APPLICATION.application_id,name='fk_applications_application_id'))
    bank_subscriptionID = Column(VARCHAR(50))
    application_name = Column(VARCHAR(255) ,ForeignKey(APPLICATION.application_id,name='fk_applications_application_name'))
    client_type = Column(VARCHAR(255))
    client_name = Column(VARCHAR(255))
    authorization_code = Column(VARCHAR(255))
    authorization_token = Column(VARCHAR(255))
    error = Column(VARCHAR(255))
    last_usage_timestamp = Column(DateTime, server_default=func.now(), onupdate=func.now(), info={'is_autoSetTimestamp': True})
    times_used = Column(Integer, default=0, server_default=text('0'),info={'is_autoIncrementCounter':True})
    row_timestamp = Column(DateTime ,server_default=func.now(),info={'is_readOnly':True})
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 
class BANK_ACCOUNT(BaseModel):
    __tablename__ = 'bank_accounts'
    bank_account_id = Column(VARCHAR(50),  unique=True, index=True,info={'is_rowUID':True})
    bank_subscription_id = Column(VARCHAR(255) ,ForeignKey(BANK_SUBSCRIPTION.bank_subscription_id,name='fk_bank_subscriptions_bank_subscription_id', ondelete='CASCADE') ,primary_key=True, nullable=False)
    bank_accountID = Column(VARCHAR(50) ,primary_key=True, nullable=False)
    client_id = Column(VARCHAR(50) ,ForeignKey(CLIENT.client_id,name='fk_clients_client_id', ondelete='CASCADE'))
    application_id = Column(VARCHAR(50))
    application_name = Column(VARCHAR(255))
    bank_code = Column(VARCHAR(50))
    bank_subscriptionID = Column(VARCHAR(50))
    client_type = Column(VARCHAR(255))
    client_name = Column(VARCHAR(255))
    payments_limit = Column(Integer ,default=0)
    payments_amount = Column(Integer ,default=0)
    payments_currency = Column(VARCHAR(10))
    account_allow_transactionHistory = Column(Integer ,default=0)
    account_allow_balance = Column(Integer ,default=0)
    account_allow_details = Column(Integer ,default=0)
    account_allow_checkFundsAvailability = Column(Integer ,default=0)
    status = Column(VARCHAR(50))
    row_timestamp = Column(DateTime ,server_default=func.now(),info={'is_readOnly':True})
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 
# db5
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 
class INTERACTION(BaseModel):
    __tablename__ = 'interactions'
    interaction_id = Column(VARCHAR(50),  primary_key=True, index=True,info={'is_rowUID':True})
    status = Column(VARCHAR(50) ,default='Active')
    originator = Column(VARCHAR(50))
    corresponder = Column(VARCHAR(50))
    originator_id = Column(VARCHAR(50))
    corresponder_id = Column(VARCHAR(50))
    originator_name = Column(VARCHAR(255))
    corresponder_name = Column(VARCHAR(255))
    completed_timestamp = Column(DateTime)
    duration = Column(Integer ,default=0)
    application_name = Column(VARCHAR(50))
    geolocation_lat = Column(VARCHAR(50))
    geolocation_lon = Column(VARCHAR(50))
    accept_geolocation_lat = Column(VARCHAR(50))
    accept_geolocation_lon = Column(VARCHAR(50))
    last_usage_timestamp = Column(DateTime, server_default=func.now(), onupdate=func.now(), info={'is_autoSetTimestamp': True})
    times_used = Column(Integer, default='0', server_default=text('0'),info={'is_autoIncrementCounter':True})
    row_timestamp = Column(DateTime ,server_default=func.now(),info={'is_readOnly':True})
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 
class INTERACTION_MESSAGE(BaseModel):
    __tablename__ = 'interaction_messages'
    interaction_message_id = Column(Integer, autoincrement=True, primary_key=True)
    interaction_id = Column(VARCHAR(50) ,ForeignKey(INTERACTION.interaction_id,name='fk_interactions_interaction_id', ondelete='CASCADE'))
    originator = Column(VARCHAR(50))
    originator_name = Column(VARCHAR(255))
    originator_id = Column(VARCHAR(50))
    message_type = Column(VARCHAR(50),default='')
    message_record = Column(VARCHAR(1024))
    content_type = Column(VARCHAR(50),default='')
    message_format = Column(VARCHAR(50),default='')
    application_name = Column(VARCHAR(50))
    geolocation_lat = Column(VARCHAR(50))
    geolocation_lon = Column(VARCHAR(50))
    row_timestamp = Column(DateTime ,server_default=func.now(),info={'is_readOnly':True})
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 
class TEST(BaseModel):
    __tablename__ = 'Test_Table'
    row_id = Column(VARCHAR(50), primary_key=True,info={'is_rowUID':True})
    #device_uid = Column(VARCHAR(255) ,ForeignKey(DEVICE.device_uid, name='fk_devices_device_uid', ondelete='CASCADE') ,primary_key=True, nullable=False)
    client_id = Column(VARCHAR(50) , nullable=False)
    geolocation_lat = Column(Integer ,default=0)
    geolocation_lon = Column(Integer ,default=0)
    name = Column(VARCHAR(50))
    #shalimar = Column(VARCHAR(50),server_default='shalimar')
    #rocco = Column(VARCHAR(50),server_default='rocco')
    #natasha = Column(VARCHAR(50),server_default='natasha')
    # brandi=Column(Integer,server_default='13')
    #rain = Column(VARCHAR(150),server_default='rain')
    status = Column(VARCHAR(150) ,default='Active')
    last_usage_timestamp = Column(DateTime, server_default=func.now(), onupdate=func.now(), info={'is_autoSetTimestamp': True})
    times_used = Column(Integer ,server_default=text('0'))
    row_timestamp = Column(DateTime ,server_default=func.now(),info={'is_readOnly':True})
#::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
#::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
#::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
# session = Session()
#::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
#::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
#::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 
# #https: // docs.sqlalchemy.org / en / 13 / orm / query.html
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 
# shalimar = CLIENT()
# what = {
#     "email": "abc@gmail.com",
#     # "name": "shalimar",
#     # "client_type":"client",
# }
# # assuming a model class, User, with attributes, name_last, name_first
# # my_filters = {'name_last':'Duncan', 'name_first':'Iain'}
# query = session.query(CLIENT)
# print(session.query(CLIENT).count())
# for key in what:
#     value=what.get(key)    
#     query = query.filter( getattr(CLIENT,key)==value )
# # now we can run the query
# print(query.count())
# results = query.all()
# print(len(results))

# print(results)


# # query = session.query(CLIENT)
# # xquery = shalimar.locate_from_dict(query,**what)

# # exist = session.query(CLIENT).filter(shalimar).first

# x = shalimar.locate_from_dict(**what)
# # print(x)
# # print(shalimar)
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 

# # 1 - new record
# #1.create
# shalimar = CLIENT(email="rocki@shalimar.com", client_type="client", name="letticia", mobile="01201201212")
# exist = session.query(CLIENT).filter_by(email=shalimar.email).first
# if not exist:
#     #2.persist
#     session.add(shalimar)
#     #3.commit
#     session.commit()
#     # #4.close
#     # session.close()
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 
# updates = {
#     "email": "shalimar@rocki.com",
#     "name": "shalimar",
# }
# x = shalimar.from_dict(**updates)
# print(x)
# session.commit()

# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 
# # 3 - queries
# clients = session.query(CLIENT).all()
# for client in clients:
#     print(f'{client.email} --- {client.client_id}')
#     print(client.bank_accounts)
#     print(client.bank_subscriptions)
#     print('------------------------')
# #more functions
# # count(): Returns the total number of rows of a query.
# # filter(): Filters the query by applying a criteria.
# # delete(): Removes from the database the rows matched by a query.
# # distinct(): Applies a distinct statement to a query.
# # exists(): Adds an exists operator to a subquery.
# # first(): Returns the first row in a query.
# # get(): Returns the row referenced by the primary key parameter passed as argument.
# # join(): Creates a SQL join in a query.
# # limit(): Limits the number of rows returned by a query.
# # order_by(): Sets an order in the rows returned by a query.

# # # 5 - get movies after 15-01-01
# # movies = session.query(Movie) \
# #     .filter(Movie.release_date > date(2015, 1, 1)) \
# #     .all()

# # print('### Recent movies:')
# # for movie in movies:
# #     print(f'{movie.title} was released after 2015')
# # print('')

# # # 6 - movies that Dwayne Johnson participated
# # the_rock_movies = session.query(Movie) \
# #     .join(Actor, Movie.actors) \
# #     .filter(Actor.name == 'Dwayne Johnson') \
# #     .all()

# # print('### Dwayne Johnson movies:')
# # for movie in the_rock_movies:
# #     print(f'The Rock starred in {movie.title}')
# # print('')

# # # 7 - get actors that have house in Glendale
# # glendale_stars = session.query(Actor) \
# #     .join(ContactDetails) \
# #     .filter(ContactDetails.address.ilike('%glendale%')) \
# #     .all()

# # print('### Actors that live in Glendale:')
# # for actor in glendale_stars:
# #     print(f'{actor.name} has a house in Glendale')
# # print('')
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 
# for client in session.query(CLIENT).all():
#     d = client.to_dict()
#     print('xxx:', json.dumps(d))
    

# #CLIENT.query.all()


# #CLIENT.query.all()])


# #json.dumps([client.to_dict() for client in session.query(CLIENT).all()])


# # user = User(username="zzzeek")
# # session.add(user)
# # session.commit()

# # print(user.to_dict())

# # # Which prints:

# # # {
# # #     'id': UUID('488345de-88a1-4c87-9304-46a1a31c9414'),
# # #     'username': 'zzzeek',
# # #     'joined_recently': True,
# # #     'modified_at': None,
# # #     'created_at': datetime.datetime(2018, 7, 11, 6, 28, 56, 905379),
# # # }
# # # And is easily jsonified with:

# # json.dumps(user.to_dict())

# # # customize which columns from User are included in the returned dictionary. For example, if you want to include email_confirmed in your serialized user you would do:

# # print(user.to_dict(show=['email_confirmed', 'password']))
# # # Which prints:

# # # {
# # #     'id': UUID('488345de-88a1-4c87-9304-46a1a31c9414'),
# # #     'username': 'zzzeek',
# # #     'email_confirmed': None,
# # #     'joined_recently': True,
# # #     'modified_at': None,
# # #     'created_at': datetime.datetime(2018, 7, 11, 6, 28, 56, 905379),
# # # }
# # # Also notice that password was not included, since it’s listed as hidden on User.

#|||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||
#|||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||
#|||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||
#https://sqlalchemy-utils.readthedocs.io/en/latest/data_types.html
#|||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||
#|||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||
#  SQLAlchemy-Utils
# latest
# Search docs
# Installation
# Listeners
# Data types
# ArrowType
# ChoiceType
# ColorType
# CompositeType
# CountryType
# CurrencyType
# EmailType
# EncryptedType
# JSONType
# LocaleType
# LtreeType
# IPAddressType
# PasswordType
# PhoneNumberType
# ScalarListType
# TimezoneType
# TSVectorType
# URLType
# UUIDType
# WeekDaysType
# Range data types
# Aggregated attributes
# Observers
# Internationalization
# Generic relationships
# Database helpers
# Foreign key helpers
# ORM helpers
# Utility classes
# Model mixins
# Testing
# License

# Private repos and priority support
# Try Read the Docs for Business Today!
# Sponsored · Ads served ethically
# Docs » Data types Edit on GitHub
# Data types
# SQLAlchemy-Utils provides various new data types for SQLAlchemy. In order to gain full advantage of these datatypes you should use automatic data coercion. See force_auto_coercion() for how to set up this feature.

# ArrowType
# classsqlalchemy_utils.types.arrow.ArrowType(*args, **kwargs)[source]
# ArrowType provides way of saving Arrow objects into database. It automatically changes Arrow objects to datetime objects on the way in and datetime objects back to Arrow objects on the way out (when querying database). ArrowType needs Arrow library installed.

# from datetime import datetime
# from sqlalchemy_utils import ArrowType
# import arrow


# class Article(Base):
#     __tablename__ = 'article'
#     id = sa.Column(sa.Integer, primary_key=True)
#     name = sa.Column(sa.Unicode(255))
#     created_at = sa.Column(ArrowType)



# article = Article(created_at=arrow.utcnow())
# As you may expect all the arrow goodies come available:

# article.created_at = article.created_at.replace(hours=-1)

# article.created_at.humanize()
# # 'an hour ago'
# ChoiceType
# classsqlalchemy_utils.types.choice.ChoiceType(choices, impl=None)[source]
# ChoiceType offers way of having fixed set of choices for given column. It could work with a list of tuple (a collection of key-value pairs), or integrate with enum in the standard library of Python 3.4+ (the enum34 backported package on PyPI is compatible too for < 3.4).

# Columns with ChoiceTypes are automatically coerced to Choice objects while a list of tuple been passed to the constructor. If a subclass of enum.Enum is passed, columns will be coerced to enum.Enum objects instead.

# class User(Base):
#     TYPES = [
#         (u'admin', u'Admin'),
#         (u'regular-user', u'Regular user')
#     ]

#     __tablename__ = 'user'
#     id = sa.Column(sa.Integer, primary_key=True)
#     name = sa.Column(sa.Unicode(255))
#     type = sa.Column(ChoiceType(TYPES))


# user = User(type=u'admin')
# user.type  # Choice(type='admin', value=u'Admin')
# Or:

# import enum


# class UserType(enum.Enum):
#     admin = 1
#     regular = 2


# class User(Base):
#     __tablename__ = 'user'
#     id = sa.Column(sa.Integer, primary_key=True)
#     name = sa.Column(sa.Unicode(255))
#     type = sa.Column(ChoiceType(UserType, impl=sa.Integer()))


# user = User(type=1)
# user.type  # <UserType.admin: 1>
# ChoiceType is very useful when the rendered values change based on user’s locale:

# from babel import lazy_gettext as _


# class User(Base):
#     TYPES = [
#         (u'admin', _(u'Admin')),
#         (u'regular-user', _(u'Regular user'))
#     ]

#     __tablename__ = 'user'
#     id = sa.Column(sa.Integer, primary_key=True)
#     name = sa.Column(sa.Unicode(255))
#     type = sa.Column(ChoiceType(TYPES))


# user = User(type=u'admin')
# user.type  # Choice(type='admin', value=u'Admin')

# print user.type  # u'Admin'
# Or:

# from enum import Enum
# from babel import lazy_gettext as _


# class UserType(Enum):
#     admin = 1
#     regular = 2


# UserType.admin.label = _(u'Admin')
# UserType.regular.label = _(u'Regular user')


# class User(Base):
#     __tablename__ = 'user'
#     id = sa.Column(sa.Integer, primary_key=True)
#     name = sa.Column(sa.Unicode(255))
#     type = sa.Column(ChoiceType(UserType, impl=sa.Integer()))


# user = User(type=UserType.admin)
# user.type  # <UserType.admin: 1>

# print user.type.label  # u'Admin'
# ColorType
# classsqlalchemy_utils.types.color.ColorType(max_length=20, *args, **kwargs)[source]
# ColorType provides a way for saving Color (from colour package) objects into database. ColorType saves Color objects as strings on the way in and converts them back to objects when querying the database.

# from colour import Color
# from sqlalchemy_utils import ColorType


# class Document(Base):
#     __tablename__ = 'document'
#     id = sa.Column(sa.Integer, autoincrement=True)
#     name = sa.Column(sa.Unicode(50))
#     background_color = sa.Column(ColorType)


# document = Document()
# document.background_color = Color('#F5F5F5')
# session.commit()
# Querying the database returns Color objects:

# document = session.query(Document).first()

# document.background_color.hex
# # '#f5f5f5'
# CompositeType
# CompositeType provides means to interact with PostgreSQL composite types. Currently this type features:

# Easy attribute access to composite type fields
# Supports SQLAlchemy TypeDecorator types
# Ability to include composite types as part of PostgreSQL arrays
# Type creation and dropping
# Installation
# CompositeType automatically attaches before_create and after_drop DDL listeners. These listeners create and drop the composite type in the database. This means it works out of the box in your test environment where you create the tables on each test run.

# When you already have your database set up you should call register_composites() after you’ve set up all models.

# register_composites(conn)
# Usage
# from collections import OrderedDict

# import sqlalchemy as sa
# from sqlalchemy_utils import CompositeType, CurrencyType


# class Account(Base):
#     __tablename__ = 'account'
#     id = sa.Column(sa.Integer, primary_key=True)
#     balance = sa.Column(
#         CompositeType(
#             'money_type',
#             [
#                 sa.Column('currency', CurrencyType),
#                 sa.Column('amount', sa.Integer)
#             ]
#         )
#     )
# Accessing fields
# CompositeType provides attribute access to underlying fields. In the following example we find all accounts with balance amount more than 5000.

# session.query(Account).filter(Account.balance.amount > 5000)
# Arrays of composites
# from sqlalchemy_utils import CompositeArray


# class Account(Base):
#     __tablename__ = 'account'
#     id = sa.Column(sa.Integer, primary_key=True)
#     balances = sa.Column(
#         CompositeArray(
#             CompositeType(
#                 'money_type',
#                 [
#                     sa.Column('currency', CurrencyType),
#                     sa.Column('amount', sa.Integer)
#                 ]
#             )
#         )
#     )
# Related links:

# http://schinckel.net/2014/09/24/using-postgres-composite-types-in-django/

# classsqlalchemy_utils.types.pg_composite.CompositeType(name, columns)[source]
# Represents a PostgreSQL composite type.

# Parameters:	
# name – Name of the composite type.
# columns – List of columns that this composite type consists of
# CountryType
# classsqlalchemy_utils.types.country.CountryType(*args, **kwargs)[source]
# Changes Country objects to a string representation on the way in and changes them back to :class:`.Country objects on the way out.

# In order to use CountryType you need to install Babel first.

# from sqlalchemy_utils import CountryType, Country


# class User(Base):
#     __tablename__ = 'user'
#     id = sa.Column(sa.Integer, autoincrement=True)
#     name = sa.Column(sa.Unicode(255))
#     country = sa.Column(CountryType)


# user = User()
# user.country = Country('FI')
# session.add(user)
# session.commit()

# user.country  # Country('FI')
# user.country.name  # Finland

# print user.country  # Finland
# CountryType is scalar coercible:

# user.country = 'US'
# user.country  # Country('US')
# classsqlalchemy_utils.primitives.country.Country(code_or_country)[source]
# Country class wraps a 2 to 3 letter country code. It provides various convenience properties and methods.

# from babel import Locale
# from sqlalchemy_utils import Country, i18n


# # First lets add a locale getter for testing purposes
# i18n.get_locale = lambda: Locale('en')


# Country('FI').name  # Finland
# Country('FI').code  # FI

# Country(Country('FI')).code  # 'FI'
# Country always validates the given code.

# Country(None)  # raises TypeError

# Country('UnknownCode')  # raises ValueError
# Country supports equality operators.

# Country('FI') == Country('FI')
# Country('FI') != Country('US')
# Country objects are hashable.

# assert hash(Country('FI')) == hash('FI')
# CurrencyType
# classsqlalchemy_utils.types.currency.CurrencyType(*args, **kwargs)[source]
# Changes Currency objects to a string representation on the way in and changes them back to Currency objects on the way out.

# In order to use CurrencyType you need to install Babel first.

# from sqlalchemy_utils import CurrencyType, Currency


# class User(Base):
#     __tablename__ = 'user'
#     id = sa.Column(sa.Integer, autoincrement=True)
#     name = sa.Column(sa.Unicode(255))
#     currency = sa.Column(CurrencyType)


# user = User()
# user.currency = Currency('USD')
# session.add(user)
# session.commit()

# user.currency  # Currency('USD')
# user.currency.name  # US Dollar

# str(user.currency)  # US Dollar
# user.currency.symbol  # $
# CurrencyType is scalar coercible:

# user.currency = 'US'
# user.currency  # Currency('US')
# classsqlalchemy_utils.primitives.currency.Currency(code)[source]
# Currency class wraps a 3-letter currency code. It provides various convenience properties and methods.

# from babel import Locale
# from sqlalchemy_utils import Currency, i18n


# # First lets add a locale getter for testing purposes
# i18n.get_locale = lambda: Locale('en')


# Currency('USD').name  # US Dollar
# Currency('USD').symbol  # $

# Currency(Currency('USD')).code  # 'USD'
# Currency always validates the given code.

# Currency(None)  # raises TypeError

# Currency('UnknownCode')  # raises ValueError
# Currency supports equality operators.

# Currency('USD') == Currency('USD')
# Currency('USD') != Currency('EUR')
# Currencies are hashable.

# len(set([Currency('USD'), Currency('USD')]))  # 1
# EmailType
# classsqlalchemy_utils.types.email.EmailType(length=255, *args, **kwargs)[source]
# Provides a way for storing emails in a lower case.

# Example:

# from sqlalchemy_utils import EmailType


# class User(Base):
#     __tablename__ = 'user'
#     id = sa.Column(sa.Integer, primary_key=True)
#     name = sa.Column(sa.Unicode(255))
#     email = sa.Column(EmailType)


# user = User()
# user.email = 'John.Smith@foo.com'
# user.name = 'John Smith'
# session.add(user)
# session.commit()
# # Notice - email in filter() is lowercase.
# user = (session.query(User)
#                .filter(User.email == 'john.smith@foo.com')
#                .one())
# assert user.name == 'John Smith'
# EncryptedType
# classsqlalchemy_utils.types.encrypted.encrypted_type.EncryptedType(type_in=None, key=None, engine=None, padding=None, **kwargs)[source]
# EncryptedType provides a way to encrypt and decrypt values, to and from databases, that their type is a basic SQLAlchemy type. For example Unicode, String or even Boolean. On the way in, the value is encrypted and on the way out the stored value is decrypted.

# EncryptedType needs Cryptography library in order to work.

# When declaring a column which will be of type EncryptedType it is better to be as precise as possible and follow the pattern below.

# a_column = sa.Column(EncryptedType(sa.Unicode,
#                                    secret_key,
#                                    FernetEngine))

# another_column = sa.Column(EncryptedType(sa.Unicode,
#                                    secret_key,
#                                    AesEngine,
#                                    'pkcs5'))
# A more complete example is given below.

# import sqlalchemy as sa
# from sqlalchemy import create_engine
# from sqlalchemy.ext.declarative import declarative_base
# from sqlalchemy.orm import sessionmaker

# from sqlalchemy_utils import EncryptedType
# from sqlalchemy_utils.types.encrypted.encrypted_type import AesEngine

# secret_key = 'secretkey1234'
# # setup
# engine = create_engine('sqlite:///:memory:')
# connection = engine.connect()
# Base = declarative_base()


# class User(Base):
#     __tablename__ = "user"
#     id = sa.Column(sa.Integer, primary_key=True)
#     username = sa.Column(EncryptedType(sa.Unicode,
#                                        secret_key,
#                                        AesEngine,
#                                        'pkcs5'))
#     access_token = sa.Column(EncryptedType(sa.String,
#                                            secret_key,
#                                            AesEngine,
#                                            'pkcs5'))
#     is_active = sa.Column(EncryptedType(sa.Boolean,
#                                         secret_key,
#                                         AesEngine,
#                                         'zeroes'))
#     number_of_accounts = sa.Column(EncryptedType(sa.Integer,
#                                                  secret_key,
#                                                  AesEngine,
#                                                  'oneandzeroes'))


# sa.orm.configure_mappers()
# Base.metadata.create_all(connection)

# # create a configured "Session" class
# Session = sessionmaker(bind=connection)

# # create a Session
# session = Session()

# # example
# user_name = u'secret_user'
# test_token = 'atesttoken'
# active = True
# num_of_accounts = 2

# user = User(username=user_name, access_token=test_token,
#             is_active=active, number_of_accounts=num_of_accounts)
# session.add(user)
# session.commit()

# user_id = user.id

# session.expunge_all()

# user_instance = session.query(User).get(user_id)

# print('id: {}'.format(user_instance.id))
# print('username: {}'.format(user_instance.username))
# print('token: {}'.format(user_instance.access_token))
# print('active: {}'.format(user_instance.is_active))
# print('accounts: {}'.format(user_instance.number_of_accounts))

# # teardown
# session.close_all()
# Base.metadata.drop_all(connection)
# connection.close()
# engine.dispose()
# The key parameter accepts a callable to allow for the key to change per-row instead of being fixed for the whole table.

# def get_key():
#     return 'dynamic-key'

# class User(Base):
#     __tablename__ = 'user'
#     id = sa.Column(sa.Integer, primary_key=True)
#     username = sa.Column(EncryptedType(
#         sa.Unicode, get_key))
# JSONType
# classsqlalchemy_utils.types.json.JSONType(*args, **kwargs)[source]
# JSONType offers way of saving JSON data structures to database. On PostgreSQL the underlying implementation of this data type is ‘json’ while on other databases its simply ‘text’.

# from sqlalchemy_utils import JSONType


# class Product(Base):
#     __tablename__ = 'product'
#     id = sa.Column(sa.Integer, autoincrement=True)
#     name = sa.Column(sa.Unicode(50))
#     details = sa.Column(JSONType)


# product = Product()
# product.details = {
#     'color': 'red',
#     'type': 'car',
#     'max-speed': '400 mph'
# }
# session.commit()
# LocaleType
# classsqlalchemy_utils.types.locale.LocaleType[source]
# LocaleType saves Babel Locale objects into database. The Locale objects are converted to string on the way in and back to object on the way out.

# In order to use LocaleType you need to install Babel first.

# from sqlalchemy_utils import LocaleType
# from babel import Locale


# class User(Base):
#     __tablename__ = 'user'
#     id = sa.Column(sa.Integer, autoincrement=True)
#     name = sa.Column(sa.Unicode(50))
#     locale = sa.Column(LocaleType)


# user = User()
# user.locale = Locale('en_US')
# session.add(user)
# session.commit()
# Like many other types this type also supports scalar coercion:

# user.locale = 'de_DE'
# user.locale  # Locale('de', territory='DE')
# LtreeType
# classsqlalchemy_utils.types.ltree.LtreeType[source]
# Postgresql LtreeType type.

# The LtreeType datatype can be used for representing labels of data stored in hierarchial tree-like structure. For more detailed information please refer to http://www.postgresql.org/docs/current/static/ltree.html

# from sqlalchemy_utils import LtreeType


# class DocumentSection(Base):
#     __tablename__ = 'document_section'
#     id = sa.Column(sa.Integer, autoincrement=True)
#     path = sa.Column(LtreeType)


# section = DocumentSection(name='Countries.Finland')
# session.add(section)
# session.commit()

# section.path  # Ltree('Countries.Finland')
# Note

# Using LtreeType, LQUERY and LTXTQUERY types may require installation of Postgresql ltree extension on the server side. Please visit http://www.postgres.org for details.

# classsqlalchemy_utils.primitives.ltree.Ltree(path_or_ltree)[source]
# Ltree class wraps a valid string label path. It provides various convenience properties and methods.

# from sqlalchemy_utils import Ltree

# Ltree('1.2.3').path  # '1.2.3'
# Ltree always validates the given path.

# Ltree(None)  # raises TypeError

# Ltree('..')  # raises ValueError
# Validator is also available as class method.

# Ltree.validate('1.2.3')
# Ltree.validate(None)  # raises ValueError
# Ltree supports equality operators.

# Ltree('Countries.Finland') == Ltree('Countries.Finland')
# Ltree('Countries.Germany') != Ltree('Countries.Finland')
# Ltree objects are hashable.

# assert hash(Ltree('Finland')) == hash('Finland')
# Ltree objects have length.

# assert len(Ltree('1.2'))  2
# assert len(Ltree('some.one.some.where'))  # 4
# You can easily find subpath indexes.

# assert Ltree('1.2.3').index('2.3') == 1
# assert Ltree('1.2.3.4.5').index('3.4') == 2
# Ltree objects can be sliced.

# assert Ltree('1.2.3')[0:2] == Ltree('1.2')
# assert Ltree('1.2.3')[1:] == Ltree('2.3')
# Finding longest common ancestor.

# assert Ltree('1.2.3.4.5').lca('1.2.3', '1.2.3.4', '1.2.3') == '1.2'
# assert Ltree('1.2.3.4.5').lca('1.2', '1.2.3') == '1'
# Ltree objects can be concatenated.

# assert Ltree('1.2') + Ltree('1.2') == Ltree('1.2.1.2')
# IPAddressType
# classsqlalchemy_utils.types.ip_address.IPAddressType(max_length=50, *args, **kwargs)[source]
# Changes IPAddress objects to a string representation on the way in and changes them back to IPAddress objects on the way out.

# IPAddressType uses ipaddress package on Python >= 3 and ipaddr package on Python 2. In order to use IPAddressType with python you need to install ipaddr first.

# from sqlalchemy_utils import IPAddressType


# class User(Base):
#     __tablename__ = 'user'
#     id = sa.Column(sa.Integer, autoincrement=True)
#     name = sa.Column(sa.Unicode(255))
#     ip_address = sa.Column(IPAddressType)


# user = User()
# user.ip_address = '123.123.123.123'
# session.add(user)
# session.commit()

# user.ip_address  # IPAddress object
# PasswordType
# classsqlalchemy_utils.types.password.PasswordType(max_length=None, **kwargs)[source]
# PasswordType hashes passwords as they come into the database and allows verifying them using a Pythonic interface. This Pythonic interface relies on setting up automatic data type coercion using the force_auto_coercion() function.

# All keyword arguments (aside from max_length) are forwarded to the construction of a passlib.context.LazyCryptContext object, which also supports deferred configuration via the onload callback.

# The following usage will create a password column that will automatically hash new passwords as pbkdf2_sha512 but still compare passwords against pre-existing md5_crypt hashes. As passwords are compared; the password hash in the database will be updated to be pbkdf2_sha512.

# class Model(Base):
#     password = sa.Column(PasswordType(
#         schemes=[
#             'pbkdf2_sha512',
#             'md5_crypt'
#         ],

#         deprecated=['md5_crypt']
#     ))
# Verifying password is as easy as:

# target = Model()
# target.password = 'b'
# # '$5$rounds=80000$H.............'

# target.password == 'b'
# # True
# Lazy configuration of the type with Flask config:

# import flask
# from sqlalchemy_utils import PasswordType, force_auto_coercion

# force_auto_coercion()

# class User(db.Model):
#     __tablename__ = 'user'

#     password = db.Column(
#         PasswordType(
#             # The returned dictionary is forwarded to the CryptContext
#             onload=lambda **kwargs: dict(
#                 schemes=flask.current_app.config['PASSWORD_SCHEMES'],
#                 **kwargs
#             ),
#         ),
#         unique=False,
#         nullable=False,
#     )
# PhoneNumberType
# classsqlalchemy_utils.types.phone_number.PhoneNumber(raw_number, region=None, check_region=True)[source]
# Extends a PhoneNumber class from Python phonenumbers library. Adds different phone number formats to attributes, so they can be easily used in templates. Phone number validation method is also implemented.

# Takes the raw phone number and country code as params and parses them into a PhoneNumber object.

# from sqlalchemy_utils import PhoneNumber


# class User(self.Base):
#     __tablename__ = 'user'
#     id = sa.Column(sa.Integer, autoincrement=True, primary_key=True)
#     name = sa.Column(sa.Unicode(255))
#     _phone_number = sa.Column(sa.Unicode(20))
#     country_code = sa.Column(sa.Unicode(8))

#     phonenumber = sa.orm.composite(
#         PhoneNumber,
#         _phone_number,
#         country_code
#     )


# user = User(phone_number=PhoneNumber('0401234567', 'FI'))

# user.phone_number.e164  # u'+358401234567'
# user.phone_number.international  # u'+358 40 1234567'
# user.phone_number.national  # u'040 1234567'
# user.country_code  # 'FI'
# Parameters:	
# raw_number – String representation of the phone number.
# region – Region of the phone number.
# check_region – Whether to check the supplied region parameter; should always be True for external callers. Can be useful for short codes or toll free
# classsqlalchemy_utils.types.phone_number.PhoneNumberType(region='US', max_length=20, *args, **kwargs)[source]
# Changes PhoneNumber objects to a string representation on the way in and changes them back to PhoneNumber objects on the way out. If E164 is used as storing format, no country code is needed for parsing the database value to PhoneNumber object.

# class User(self.Base):
#     __tablename__ = 'user'
#     id = sa.Column(sa.Integer, autoincrement=True, primary_key=True)
#     name = sa.Column(sa.Unicode(255))
#     phone_number = sa.Column(PhoneNumberType())


# user = User(phone_number='+358401234567')

# user.phone_number.e164  # u'+358401234567'
# user.phone_number.international  # u'+358 40 1234567'
# user.phone_number.national  # u'040 1234567'
# ScalarListType
# classsqlalchemy_utils.types.scalar_list.ScalarListType(coerce_func=<type 'unicode'>, separator=u', ')[source]
# ScalarListType type provides convenient way for saving multiple scalar values in one column. ScalarListType works like list on python side and saves the result as comma-separated list in the database (custom separators can also be used).

# Example

# from sqlalchemy_utils import ScalarListType


# class User(Base):
#     __tablename__ = 'user'
#     id = sa.Column(sa.Integer, autoincrement=True)
#     hobbies = sa.Column(ScalarListType())


# user = User()
# user.hobbies = [u'football', u'ice_hockey']
# session.commit()
# You can easily set up integer lists too:

# from sqlalchemy_utils import ScalarListType


# class Player(Base):
#     __tablename__ = 'player'
#     id = sa.Column(sa.Integer, autoincrement=True)
#     points = sa.Column(ScalarListType(int))


# player = Player()
# player.points = [11, 12, 8, 80]
# session.commit()
# TimezoneType
# classsqlalchemy_utils.types.timezone.TimezoneType(backend='dateutil')[source]
# TimezoneType provides a way for saving timezones (from either the pytz or the dateutil package) objects into database. TimezoneType saves timezone objects as strings on the way in and converts them back to objects when querying the database.

# from sqlalchemy_utils import TimezoneType

# class User(Base):
#     __tablename__ = 'user'

#     # Pass backend='pytz' to change it to use pytz (dateutil by
#     # default)
#     timezone = sa.Column(TimezoneType(backend='pytz'))
# TSVectorType
# classsqlalchemy_utils.types.ts_vector.TSVectorType(*args, **kwargs)[source]
# Note

# This type is PostgreSQL specific and is not supported by other dialects.

# Provides additional functionality for SQLAlchemy PostgreSQL dialect’s TSVECTOR type. This additional functionality includes:

# Vector concatenation
# regconfig constructor parameter which is applied to match function if no postgresql_regconfig parameter is given
# Provides extensible base for extensions such as SQLAlchemy-Searchable
# from sqlalchemy_utils import TSVectorType


# class Article(Base):
#     __tablename__ = 'user'
#     id = sa.Column(sa.Integer, primary_key=True)
#     name = sa.Column(sa.String(100))
#     search_vector = sa.Column(TSVectorType)


# # Find all articles whose name matches 'finland'
# session.query(Article).filter(Article.search_vector.match('finland'))
# TSVectorType also supports vector concatenation.

# class Article(Base):
#     __tablename__ = 'user'
#     id = sa.Column(sa.Integer, primary_key=True)
#     name = sa.Column(sa.String(100))
#     name_vector = sa.Column(TSVectorType)
#     content = sa.Column(sa.String)
#     content_vector = sa.Column(TSVectorType)

# # Find all articles whose name or content matches 'finland'
# session.query(Article).filter(
#     (Article.name_vector | Article.content_vector).match('finland')
# )
# You can configure TSVectorType to use a specific regconfig.

# class Article(Base):
#     __tablename__ = 'user'
#     id = sa.Column(sa.Integer, primary_key=True)
#     name = sa.Column(sa.String(100))
#     search_vector = sa.Column(
#         TSVectorType(regconfig='pg_catalog.simple')
#     )
# Now expression such as:

# Article.search_vector.match('finland')
# Would be equivalent to SQL:

# search_vector @@ to_tsquery('pg_catalog.simgle', 'finland')
# URLType
# classsqlalchemy_utils.types.url.URLType(*args, **kwargs)[source]
# URLType stores furl objects into database.

# from sqlalchemy_utils import URLType
# from furl import furl


# class User(Base):
#     __tablename__ = 'user'

#     id = sa.Column(sa.Integer, primary_key=True)
#     website = sa.Column(URLType)


# user = User(website=u'www.example.com')

# # website is coerced to furl object, hence all nice furl operations
# # come available
# user.website.args['some_argument'] = '12'

# print user.website
# # www.example.com?some_argument=12
# UUIDType
# classsqlalchemy_utils.types.uuid.UUIDType(binary=True, native=True)[source]
# Stores a UUID in the database natively when it can and falls back to a BINARY(16) or a CHAR(32) when it can’t.

# from sqlalchemy_utils import UUIDType
# import uuid

# class User(Base):
#     __tablename__ = 'user'

#     # Pass `binary=False` to fallback to CHAR instead of BINARY
#     id = sa.Column(VARCHAR(50), primary_key=True)
# WeekDaysType
# classsqlalchemy_utils.types.weekdays.WeekDaysType(*args, **kwargs)[source]
# WeekDaysType offers way of saving WeekDays objects into database. The WeekDays objects are converted to bit strings on the way in and back to WeekDays objects on the way out.

# In order to use WeekDaysType you need to install Babel first.

# from sqlalchemy_utils import WeekDaysType, WeekDays
# from babel import Locale


# class Schedule(Base):
#     __tablename__ = 'schedule'
#     id = sa.Column(sa.Integer, autoincrement=True)
#     working_days = sa.Column(WeekDaysType)


# schedule = Schedule()
# schedule.working_days = WeekDays('0001111')
# session.add(schedule)
# session.commit()

# print schedule.working_days  # Thursday, Friday, Saturday, Sunday
# WeekDaysType also supports scalar coercion:

# schedule.working_days = '1110000'
# schedule.working_days  # WeekDays object
# © Copyright 2013, Konsta Vesterinen Revision 717432b0.

# Built with Sphinx using a theme provided by Read the Docs.
#  Read the Docsv: latest 
#print(Base)
#print(BaseModel)
#print(BaseModel.metadata.sorted_tables)

tables_modeled = BaseModel.metadata.tables
classes_modelled = BaseModel._decl_class_registry.data
t = len(tables_modeled)
c = len(classes_modelled) - 1  #exclude class: _sa_module_registry
msg = f"database [ganimides] [[[[models loaded]]]] with [[{c} models]] on [[{t} tables]]"
if thisApp.CONSOLE_ON:
    log_message(msg)
else:
    log_message(msg)
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 
