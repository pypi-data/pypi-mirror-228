from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from sqlalchemy.sql import text
from networktools.environment import get_env_variable

data = dict(dbuser=get_env_variable('COLLECTOR_DBUSER'),
            dbpass=get_env_variable('COLLECTOR_DBPASS'),
            dbname=get_env_variable('COLLECTOR_DBNAME'),
            dbhost=get_env_variable('COLLECTOR_DBHOST'),
            dbport=get_env_variable('COLLECTOR_DBPORT'))


class CollectorSession:
    def __init__(self, *args, **kwargs):
        self.db_engine = 'postgresql://{dbuser}:{dbpass}@{dbhost}:{dbport}/{dbname}'.format(
            **kwargs)
        self.engine = create_engine(self.db_engine)
        self.connection = self.engine.connect()
        self.session = sessionmaker(bind=self.engine)()
        self.data = kwargs

    def get_session(self):
        return self.session

    def run_sql(self, sql):
        if isinstance(sql, str):
            sql = text(sql)
        self.connection.execute(sql)


if __name__ == '__main__':
    csession = CollectorSession(**data)
    session = csession.get_session()
    engine = csession.engine
    connection = csession.connection
