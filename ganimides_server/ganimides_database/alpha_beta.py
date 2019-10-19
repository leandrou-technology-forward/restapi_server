#from __future__ import (absolute_import, division, print_function,unicode_literals)
import sqlalchemy as db

from sqlalchemy import Column, MetaData, Table, create_engine
from sqlalchemy import String, Integer, Float, BigInteger, DateTime

from sqlalchemy.schema import DropTable, CreateTable
from sqlalchemy.orm import scoped_session, sessionmaker

from sqlalchemy.pool import SingletonThreadPool

from contextlib import contextmanager


@contextmanager
def Session(*args, **kwargs):
    Session = scoped_session(sessionmaker(
        bind=create_engine(*args, **kwargs)))

    try:
        session = Session()
        yield session
        session.commit()
    except:
        session.rollback()
        raise
    finally:
        session.close()


def main():
    DB = 'sqlite:///example'
    DB = 'sqlite:///C:\\Users\\User\\Documents\\my Projects\\Systems_Development\\Development_Environment\\test.db'
    # engine = create_engine(DB,poolclass=SingletonThreadPool)
    # connection = engine.connect()
    # session = scoped_session(sessionmaker(autocommit=False,autoflush=False,bind=connection))

    TABLE_SPEC = [
        ('id', BigInteger),
        ('name', String),
        ('t_modified', DateTime),
        ('whatever', String)
    ]

    TABLE_NAME = 'sample_table'

    columns = [Column(n, t) for n, t in TABLE_SPEC]

    table = Table(TABLE_NAME, MetaData(), *columns)
    # session.execute('drop table if exists {}'.format(TABLE_NAME))

    table_creation_sql = CreateTable(table)
    # session.execute(table_creation_sql)


    with Session(DB, echo=True) as s:
        # this is just here to make the script idempotent
        s.execute('drop table if exists {}'.format(TABLE_NAME))

        table_creation_sql = CreateTable(table)
        s.execute(table_creation_sql)


if __name__ == '__main__':
    main()