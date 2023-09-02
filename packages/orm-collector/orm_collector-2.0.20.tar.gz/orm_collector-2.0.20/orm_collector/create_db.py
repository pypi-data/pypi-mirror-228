from sqlalchemy import create_engine
from sqlalchemy.schema import CreateSchema
from sqlalchemy import event
from sqlalchemy.sql import exists, select

from networktools.environment import get_env_variable
from orm_collector import Base
import os
from sqlalchemy import text

"""
Create Schema Collector
"""


# def get_schemas(engine, conn=None):
#     query = text("SELECT schema_name FROM information_schema.schemata;")

#     if conn:
#         result = [n[0] for n in conn.execute(query).all()]
#         return result

#     with engine.connect() as conn:
#         result = [n[0] for n in conn.execute(query).all()]
#         return result
#     return []


def create_collector(engine):

    try:
        with engine.connect() as conn:
            if not engine.dialect.has_schema(conn, "collector"):
                print("Crear schema...")
                result = conn.execute(CreateSchema('collector'))
                conn.commit()
                print("Resultado", result)
                return True
            return False
        return False
    except Exception as e:
        raise e


"""
Create Schema DataWork
"""


def create_datawork(engine):
    try:
        with engine.connect() as conn:
            conn.execute(CreateSchema('datawork'))
            return True
        return False
    except:
        raise


if __name__ == '__main__':
    user = os.environ.get('COLLECTOR_DBUSER')
    passw = os.environ.get('COLLECTOR_DBPASS')
    dbname = os.environ.get('COLLECTOR_DBNAME')
    hostname = os.environ.get('COLLECTOR_DBHOST')
    db_engine = 'postgresql://%s:%s@%s/%s' % (user, passw, hostname, dbname)
    # create engine
    engine = create_engine(db_engine, echo=True)
    print(db_engine)
    # load schema on engine
    try:
        create_collector(engine)
        Base.metadata.create_all(engine, checkfirst=True)
    except Exception as e:
        print("Falla al crear esquema de tablas")
        raise e
