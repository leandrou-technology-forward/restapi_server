from __future__ import unicode_literals
import os
from sqlalchemy import (create_engine, MetaData, Table, Column,
                        Integer, Numeric, String, Date, DateTime, text)
from sqlalchemy.ext.compiler import compiles
from sqlalchemy.schema import (CreateTable, AddConstraint, CreateIndex,
                               DropTable, DropConstraint, DropIndex,
                               ForeignKeyConstraint, CheckConstraint,
                               UniqueConstraint, PrimaryKeyConstraint)
#from dmsa import __version__
#from dmsa.utility import get_model_json, get_service_version
#from dmsa.makers import make_model
#from dmsa.makers import make_model_from_service  # noqa

serial = os.environ.get('BUILD_NUM') or '0'
sha = os.environ.get('COMMIT_SHA1') or '0'
sha = sha[0:8]

__version_info__ = {
    'major': 0,
    'minor': 6,
    'micro': 0,
    'releaselevel': 'final',
    'serial': serial,
    'sha': sha
}


def get_version(short=False):
    assert __version_info__['releaselevel'] in ('alpha', 'beta', 'final')
    vers = ['%(major)i.%(minor)i.%(micro)i' % __version_info__, ]
    if __version_info__['releaselevel'] != 'final' and not short:
        __version_info__['lvlchar'] = __version_info__['releaselevel'][0]
        vers.append('%(lvlchar)s%(serial)s+%(sha)s' % __version_info__)
    return ''.join(vers)

__version__ = get_version()


def get_model_json(model, model_version, service):
    """Retrieve model JSON for the model and version from the service."""
    r_json={'zzz':f'xxx/schemata/{model}/{model_version}?format=json'}
    # r = requests.get(''.join([service, 'schemata/', model, '/', model_version,
    #                           '?format=json']))
    return r_json

# Coerce Numeric type to produce NUMBER on Oracle backend.
@compiles(Numeric, 'oracle')
def _compile_numeric_oracle(type_, compiler, **kw):
    return 'NUMBER'


# Coerce Integer type to produce NUMBER(10) on Oracle backend.
@compiles(Integer, 'oracle')
def _compile_integer_oracle(type_, compiler, **kw):
    return 'NUMBER(10)'


# Coerce DateTime type to produce TIMESTAMP on Oracle backend.
@compiles(DateTime, 'oracle')
def _compile_datetime_oracle(type_, compiler, **kw):
    return compiler.visit_TIMESTAMP(type_, **kw)


# Coerce String type without length to produce VARCHAR2(255) on Oracle.
@compiles(String, 'oracle')
def _compile_string_oracle(type_, compiler, **kw):

    if not type_.length:
        type_.length = 255
    visit_attr = 'visit_{0}'.format(type_.__visit_name__)
    return getattr(compiler, visit_attr)(type_, **kw)


# Coerce String type without length to produce VARCHAR(255) on MySQL.
@compiles(String, 'mysql')
def _compile_string_mysql(type_, compiler, **kw):

    if not type_.length:
        type_.length = 255
    visit_attr = 'visit_{0}'.format(type_.__visit_name__)
    return getattr(compiler, visit_attr)(type_, **kw)


# Coerce DateTime type to produce DATETIME2 on MSSQL backend.
@compiles(DateTime, 'mssql')
def _compile_datetime_mssql(type_, compiler, **kw):
    return compiler.visit_DATETIME2(type_, **kw)


# Coerce Date type to produce DATETIME2 on MSSQL backend.
@compiles(Date, 'mssql')
def _compile_datetime_mssql(type_, compiler, **kw):
    return compiler.visit_DATETIME2(type_, **kw)


# Add DEFERRABLE INITIALLY DEFERRED to Oracle constraints.
@compiles(ForeignKeyConstraint, 'oracle')
@compiles(UniqueConstraint, 'oracle')
@compiles(CheckConstraint, 'oracle')
def _compile_constraint_oracle(constraint, compiler, **kw):

    constraint.deferrable = True
    constraint.initially = 'DEFERRED'
    visit_attr = 'visit_{0}'.format(constraint.__visit_name__)
    return getattr(compiler, visit_attr)(constraint, **kw)


# Add DEFERRABLE INITIALLY DEFERRED to PostgreSQL constraints.
@compiles(ForeignKeyConstraint, 'postgresql')
@compiles(UniqueConstraint, 'postgresql')
@compiles(CheckConstraint, 'postgresql')
def _compile_constraint_postgresql(constraint, compiler, **kw):

    constraint.deferrable = True
    constraint.initially = 'DEFERRED'
    visit_attr = 'visit_{0}'.format(constraint.__visit_name__)
    return getattr(compiler, visit_attr)(constraint, **kw)


def generate(model, model_version, dialect, tables=True, constraints=True,
             indexes=True, drop=False, delete_data=False, nologging=False,
             logging=False,
             service='https://data-models-service.research.chop.edu/'):
    """Generate data definition language for the data model specified in the
    given DBMS dialect.
    Arguments:
      model          Model to generate DDL for.
      model_version  Model version to generate DDL for.
      dialect        DBMS dialect to generate DDL in.
      tables         Include tables when generating DDL.
      constraints    Include constraints when generating DDL.
      indexes        Include indexes when generating DDL.
      drop           Generate DDL to drop, instead of create, objects.
      delete_data    Generate DML to delete data from the model.
      nologging      Generate Oracle DDL to make objects "nologging".
      logging        Generate Oracle DDL to make objects "logging".
      service        Base URL of the data models service to use.
    """  # noqa

    metadata = MetaData()
    model_json = get_model_json(model, model_version, service)
    make_model(model_json, metadata)

    service_version = get_service_version(service)

    engine = create_engine(dialect + '://')

    output = []

    INSERT = ("INSERT INTO version_history (operation, model, model_version, "
              "dms_version, dmsa_version) VALUES ('{operation}', '" +
              model + "', '" + model_version + "', '" +
              service_version + "', '" + __version__ + "');\n\n")

    if dialect.startswith('oracle'):
        INSERT = INSERT + "COMMIT;\n\n"

    version_history = Table(
        'version_history', MetaData(),
        Column('datetime', DateTime(), primary_key=True,
               server_default=text('CURRENT_TIMESTAMP')),
        Column('operation', String(100)),
        Column('model', String(16)),
        Column('model_version', String(50)),
        Column('dms_version', String(50)),
        Column('dmsa_version', String(50))
    )

    version_tbl_ddl = str(CreateTable(version_history).
                          compile(dialect=engine.dialect)).strip()

    if dialect.startswith('mssql'):
        version_tbl_ddl = ("IF OBJECT_ID ('version_history', 'U') IS NULL " +
                           version_tbl_ddl + ";")
    elif dialect.startswith('oracle'):
        version_tbl_ddl = ("BEGIN\n" +
                           "EXECUTE IMMEDIATE '" + version_tbl_ddl + "';\n" +
                           "EXCEPTION\n" +
                           "WHEN OTHERS THEN\n" +
                           "IF SQLCODE = -955 THEN NULL;\n" +
                           "ELSE RAISE;\n" +
                           "END IF;\nEND;\n/")
    else:
        version_tbl_ddl = version_tbl_ddl.replace('CREATE TABLE',
                                                  'CREATE TABLE IF NOT EXISTS')
        version_tbl_ddl = version_tbl_ddl + ";"

    if delete_data:

        output.append(INSERT.format(operation='delete data'))

        tables = reversed(metadata.sorted_tables)
        output.extend(delete_ddl(tables, engine))

        output.insert(0, version_tbl_ddl + '\n\n')

        output = ''.join(output)

        return output

    LOGGING = 'ALTER {type} {name} LOGGING;\n'
    NOLOGGING = 'ALTER {type} {name} NOLOGGING;\n'

    if tables:

        if drop:

            tables = reversed(metadata.sorted_tables)
            output.extend(table_ddl(tables, engine, True))
            output.insert(0, INSERT.format(operation='drop tables'))

        elif logging and dialect.startswith('oracle'):

            output.append(INSERT.format(operation='table logging'))
            for table in metadata.sorted_tables:
                output.append(LOGGING.format(type='TABLE', name=table.name))
            output.append('\n')

        elif nologging and dialect.startswith('oracle'):

            output.append(INSERT.format(operation='table nologging'))
            for table in metadata.sorted_tables:
                output.append(NOLOGGING.format(type='TABLE', name=table.name))
            output.append('\n')

        else:

            output.append(INSERT.format(operation='create tables'))
            tables = metadata.sorted_tables
            output.extend(table_ddl(tables, engine, False))

    if constraints:

        if drop and not dialect.startswith('sqlite'):

            tables = reversed(metadata.sorted_tables)
            output.insert(0, '\n')
            output[0:0] = constraint_ddl(tables, engine, True)
            output.insert(0, INSERT.format(operation='drop constraints'))

        elif logging:
            pass
        elif nologging:
            pass

        elif not dialect.startswith('sqlite'):

            output.append('\n')
            output.append(INSERT.format(operation='create constraints'))
            tables = metadata.sorted_tables
            output.extend(constraint_ddl(tables, engine, False))

    if indexes:

        if drop:

            tables = reversed(metadata.sorted_tables)
            output.insert(0, '\n')
            output[0:0] = index_ddl(tables, engine, True)
            output.insert(0, INSERT.format(operation='drop indexes'))

        elif logging and dialect.startswith('oracle'):

            output.append(INSERT.format(operation='index logging'))
            for table in metadata.sorted_tables:
                output.append(LOGGING.format(type='INDEX', name=table.name))
            output.append('\n')

        elif nologging and dialect.startswith('oracle'):

            output.append(INSERT.format(operation='index nologging'))
            for table in metadata.sorted_tables:
                output.append(NOLOGGING.format(type='INDEX', name=table.name))
            output.append('\n')

        else:

            output.append('\n')
            output.append(INSERT.format(operation='create indexes'))
            tables = metadata.sorted_tables
            output.extend(index_ddl(tables, engine, False))

    output.insert(0, version_tbl_ddl + '\n\n')

    output = ''.join(output)

    return output


def delete_ddl(tables, engine):

    output = []

    for table in tables:
        output.append(str(table.delete().compile(dialect=engine.dialect)).
                      strip())
        output.append(';\n\n')

    return output


def table_ddl(tables, engine, drop=False):

    output = []

    for table in tables:

        if not drop:
            ddl = CreateTable(table)
        else:
            ddl = DropTable(table)

        output.append(str(ddl.compile(dialect=engine.dialect)).strip())
        output.append(';\n\n')

    return output


def constraint_ddl(tables, engine, drop=False):

    output = []

    for table in tables:
        constraints = sorted(list(table.constraints), key=lambda k: k.name,
                             reverse=drop)
        for constraint in constraints:

            # Avoid duplicating primary key constraint definitions (they are
            # included in CREATE TABLE statements).
            if not isinstance(constraint, PrimaryKeyConstraint):

                if not drop:
                    ddl = AddConstraint(constraint)
                else:
                    ddl = DropConstraint(constraint)

                output.append(str(ddl.compile(dialect=engine.dialect)).strip())
                output.append(';\n\n')

    return output


def index_ddl(tables, engine, drop=False):

    output = []

    for table in tables:
        indexes = sorted(list(table.indexes), key=lambda k: k.name,
                         reverse=drop)
        for index in indexes:

            if not drop:
                ddl = CreateIndex(index)
            else:
                ddl = DropIndex(index)

            output.append(str(ddl.compile(dialect=engine.dialect)).strip())
            output.append(';\n\n')

    return output

#######################################################

def get_datatype_map():
    from sqlalchemy import (Integer, Numeric, Float, String, Date,
                            DateTime, Time, Text, Boolean, LargeBinary)

    return {
        'integer': Integer,
        'number': Numeric,
        'decimal': Numeric,
        'float': Float,
        'string': String,
        'date': Date,
        'datetime': DateTime,
        'timestamp': DateTime,
        'time': Time,
        'text': Text,
        'clob': Text,
        'boolean': Boolean,
        'blob': LargeBinary
    }


def make_index(index_json):
    """Returns a dynamically constructed SQLAlchemy model Index class.
    `index_json` is a declarative style dictionary index object, as defined by
    the chop-dbhi/data-models package.
    """

    from sqlalchemy.schema import Index

    # Transform empty string to None in order to trigger auto-generation.

    idx_name = index_json.get('name')

    return Index(idx_name, *index_json['fields'])


def make_constraint(constraint_type, constraint_json):
    """Returns a dynamically constructed SQLAlchemy model Constraint class.
    `constraint_type` is a string that maps to the type of constraint to be
    constructed.
    `constraint_json` is a declarative style dictionary constraint object, as
    defined by the chop-dbhi/data-models package.
    """

    from sqlalchemy.schema import (PrimaryKeyConstraint, ForeignKeyConstraint,
                                   UniqueConstraint)

    # Transform empty string to None in order to trigger auto-generation.

    constraint_name = constraint_json.get('name')

    # Create the appropriate constraint class.

    if constraint_type == 'primary_keys':

        return PrimaryKeyConstraint(*constraint_json['fields'],
                                    name=constraint_name)

    elif constraint_type == 'foreign_keys':

        source_column_list = [constraint_json['source_field']]
        target_column_list = ['.'.join([constraint_json['target_table'],
                                        constraint_json['target_field']])]

        return ForeignKeyConstraint(source_column_list, target_column_list,
                                    constraint_name, use_alter=True)

    elif constraint_type == 'uniques':

        return UniqueConstraint(*constraint_json['fields'],
                                name=constraint_name)


def make_column(field, not_null_flag=False):
    """Returns a dynamically constructed SQLAlchemy model Column class.
    `field` is a declarative style dictionary field object retrieved from the
    chop-dbhi/data-models service or at least matching the format specified
    there.
    `not_null_flag` signifies that a not null constraint should be included.
    """

    from sqlalchemy import (Column, String, Numeric)

    column_kwargs = {}
    column_kwargs['name'] = field['name']

    type_string = field['type']
    DATATYPE_MAP = get_datatype_map()
    type_class = DATATYPE_MAP[type_string]
    type_kwargs = {}

    if field.get('description'):
        # This only exists in the ORM, will not generate a DB "comment".
        column_kwargs['doc'] = field['description']

    if field.get('default'):
        # The first is for the ORM, the second for the DB.
        column_kwargs['default'] = field['default']
        column_kwargs['server_default'] = field['default']

    if not_null_flag:
        column_kwargs['nullable'] = False

    if type_class == String:
        type_kwargs['length'] = field.get('length') or 256

    if type_class == Numeric:
        type_kwargs['precision'] = field.get('precision') or 20
        type_kwargs['scale'] = field.get('scale') or 5

    column_kwargs['type_'] = type_class(**type_kwargs)
    return Column(**column_kwargs)


def make_table(table_json, metadata, not_nulls):
    """Makes and attaches a SQLAlchemy Table class to the metadata object.
    `table_json` is a declarative style nested table object retrieved from the
    chop-dbhi/data-models service or at least matching the format specified
    there.
    `metadata` is the metadata instance the produced model should attach to.
    This could simply be sqlalchemy.MetaData().
    `not_nulls` is a list of table-relevant not null constraints matching the
    chop-dbhi/data-models specified format.
    """

    from sqlalchemy import Table

    table = Table(table_json['name'], metadata)

    fields = table_json.get('fields', []) or []

    for field in fields:

        not_null_flag = False

        for not_null in not_nulls:
            if not_null['field'] == field['name']:
                not_null_flag = True
                break

        table.append_column(make_column(field, not_null_flag))

    return table


def make_model(data_model, metadata):
    """Makes and attaches a collection of SQLAlchemy classes that describe a
    data model to the metadata object.
    `data_model` is a declarative style nested data model object retrieved from
    the chop-dbhi/data-models service or at least matching the format specified
    there.
    `metadata` is the metadata instance the produced models should attach to.
    This could simply be sqlalchemy.MetaData().
    """

    for table_json in data_model['tables']:

        # Construct table-relevant not-null constraint list.

        table_not_nulls = []

        for not_null in data_model['schema']['constraints']['not_null'] or []:

            if not_null['table'] == table_json['name']:

                table_not_nulls.append(not_null)

        # Construct and attach table to metadata.

        make_table(table_json, metadata, table_not_nulls)

    # Construct and add constraints to the relevant tables.

    for con_type, con_list in \
            data_model['schema']['constraints'].iteritems():

        if con_type != 'not_null':

            for con in con_list or []:

                table_name = con.get('table') or con.get('source_table')
                metadata.tables[table_name].\
                    append_constraint(make_constraint(con_type, con))

    # Construct and add indexes to the relevant tables.

    for index in data_model['schema']['indexes']:

        table_name = index['table']
        metadata.tables[table_name].append_constraint(make_index(index))

    return metadata


def make_model_from_service(model, model_version, service, metadata):
    from dmsa.utility import get_model_json
    return make_model(get_model_json(model, model_version, service), metadata)
