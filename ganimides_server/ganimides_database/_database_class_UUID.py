from __future__ import absolute_import
from sqlalchemy import types
from sqlalchemy.dialects import mssql, postgresql, sqlite
from sqlalchemy.types import TypeDecorator, CHAR,VARCHAR,INTEGER
from sqlalchemy.dialects.postgresql import UUID
import uuid
from _colorServices import colorized_string
# from colorama import Fore
# colorama.init(convert=True)
#from .scalar_coercible import ScalarCoercible
import uuid
###############################################
shalimar = 0

def get_uuid(n):
    # x=str(uuid.uuid1())
    x=str(uuid.uuid1(uuid.getnode()+n))
    print(n,'o o o o ',x)
    return x
    #return str(uuid.uuid1(uuid.getnode()+n))
###############################################
#Base = declarative_base()
class GUID(TypeDecorator):
    """Platform-independent GUID type.
    Uses PostgreSQL's UUID type, otherwise uses
    CHAR(36), storing as stringified hex values.
    """
    impl = VARCHAR
    shalimar = 0
    bobbi = 0
    
    def load_dialect_impl(self, dialect):
        if dialect.name == 'sqlite':
            return dialect.type_descriptor(VARCHAR(255))
        elif dialect.name == 'mysql':
            return dialect.type_descriptor(UUID())
        elif dialect.name == 'postgresql':
            return dialect.type_descriptor(UUID())
        else:
            return dialect.type_descriptor(UUID())

    def process_bind_param(self, value, dialect):
        if value is None:
            return value
        elif dialect.name == 'sqlite':
            self.shalimar = self.shalimar + 1
            print(self.shalimar,colorized_string(f"[UUID-SET] [[{str(value)}]]"))
            return str(value)
        elif dialect.name == 'postgresql':
            print('SSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSS')
            return str(value)
        elif dialect.name == 'mysql':
            print('SSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSS')
            return str(value)
        else:
            print('SSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSS')
            if not isinstance(value, uuid.UUID):
                return "%.32x" % uuid.UUID(value).int
            else:
                # hexstring
                return "%.32x" % value.int

    def process_result_value(self, value, dialect):
        if value is None:
            return value
        else:
            if dialect.name == 'sqlite':
                self.bobbi = self.bobbi + 1
                print(self.bobbi,colorized_string(f"[UUID-GET] #RED#{str(value)}#RESET#"))
                return str(value)
            else:
                if not isinstance(value, uuid.UUID):
                    value = uuid.UUID(value)
                return value

class xGUID(TypeDecorator):
    """Platform-independent GUID type.

    Uses Postgresql's UUID type, otherwise uses
    CHAR(32), storing as stringified hex values.

    """
    impl = CHAR

    def process_bind_param(self, value, dialect):
        if value is None:
            return value
        elif dialect.name == 'postgresql':
            return str(value)
        else:
            return(str(value))
            if not isinstance(value, uuid.UUID):
                #x = "%.32x" % uuid.UUID(value).int
                x=value
                print('STORE','is-not-uid',value,'<--',x)
                return str(value)
            else:
                # hexstring
                x = "%.32x" % value.int
                x=value
                print('STORE','isuid',value,'<==',x)
                return str(value)

    def process_result_value(self, value, dialect):
        if value is None:
            return value
        else:
            return(str(value))
            if not isinstance(value, uuid.UUID):
                #shalimar
                #value = uuid.UUID(value)
                x=value
                value = str(value)
                print('RETRIEVE','is-not-uid', x, '-->',value)
            else:
                x=value
                value = str(value)
                print('RETRIEVE','is-uid', x, '-->',value)
            return value



##########################################################  

class UUIDType(types.TypeDecorator): #, ScalarCoercible):
    """
    Stores a UUID in the database natively when it can and falls back to
    a BINARY(16) or a CHAR(32) when it can't.

    ::

        from sqlalchemy_utils import UUIDType
        import uuid

        class User(Base):
            __tablename__ = 'user'

            # Pass `binary=False` to fallback to CHAR instead of BINARY
            id = sa.Column(UUIDType(binary=False), primary_key=True)
    """
    impl = types.BINARY(16)

    python_type = uuid.UUID

    def __init__(self, binary=True, native=True):
        """
        :param binary: Whether to use a BINARY(16) or CHAR(32) fallback.
        """
        self.binary = binary
        self.native = native

    def load_dialect_impl(self, dialect):
        if dialect.name == 'postgresql' and self.native:
            # Use the native UUID type.
            return dialect.type_descriptor(postgresql.UUID())

        if dialect.name == 'mssql' and self.native:
            # Use the native UNIQUEIDENTIFIER type.
            return dialect.type_descriptor(mssql.UNIQUEIDENTIFIER())

        else:
            # Fallback to either a BINARY or a CHAR.
            kind = self.impl if self.binary else types.CHAR(32)
            return dialect.type_descriptor(kind)

    @staticmethod
    def _coerce(value):
        if value and not isinstance(value, uuid.UUID):
            try:
                value = uuid.UUID(value)

            except (TypeError, ValueError):
                value = uuid.UUID(bytes=value)

        return value

    def process_bind_param(self, value, dialect):
        if value is None:
            return value

        if not isinstance(value, uuid.UUID):
            value = self._coerce(value)

        if self.native and dialect.name in ('postgresql', 'mssql'):
            return str(value)

        return value.bytes if self.binary else value.hex

    def process_result_value(self, value, dialect):
        if value is None:
            return value

        if self.native and dialect.name in ('postgresql', 'mssql'):
            if isinstance(value, uuid.UUID):
                # Some drivers convert PostgreSQL's uuid values to
                # Python's uuid.UUID objects by themselves
                return value
            return uuid.UUID(value)

        return uuid.UUID(bytes=value) if self.binary else uuid.UUID(value)
##########################################################################
class NOT_WORKING_AUTO_INCREMENT_COUNTER(TypeDecorator):
    """Platform-independent GUID type.
    Uses PostgreSQL's UUID type, otherwise uses
    CHAR(36), storing as stringified hex values.
    """
    impl = INTEGER

    def load_dialect_impl(self, dialect):
        return dialect.type_descriptor(INTEGER)
    def process_bind_param(self, value, dialect):
        if value is None:
            print(colorized_string(f"[[COUNTER-SET]] #RED#{str(value)}#RESET#"))
            return 0
        else:
            print(colorized_string(f"[[COUNTER-SET]] #RED#{str(value+1)}#RESET#"))
            return value + 1
    def process_result_value(self, value, dialect):
        if value is None:
            print(colorized_string(f"[[COUNTER-GET]] #YELLOW#{str(value)}#RESET#"))
            return 0
        else:
            print(colorized_string(f"[[COUNTER-GET]] #YELLOW#{str(value+1)}#RESET#"))
            return value + 1