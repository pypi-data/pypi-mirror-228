import re
from typing import Sequence
from .support import DBError
from functools import lru_cache
from .log_support import logger
from sqlexec import get, query, select
from sqlexec.engine import Engine as SupperEngine
from .sql_support import require_limit, get_page_start
from .constant import MYSQL_COLUMN_SQL, POSTGRES_COLUMN_SQL, MYSQL_SELECT_KEY, LIMIT_1, MYSQL, POSTGRESQL, DEFAULT_KEY_FIELD, CACHE_SIZE, SQLITE, \
    SQLITE_SELECT_KEY, ORACLE


# Engin = Enum('Engin', ['MYSQL', 'POSTGRESQL', 'OTHER'])
# class Engin(Enum):
#     MYSQL = 'MySQL'
#     POSTGRESQL = 'PostgreSQL'
#     OTHER = 'Other'


class Engine(SupperEngine):

    @staticmethod
    def get_page_sql_args(sql: str, page_num: int, page_size: int, *args):
        if Engine.current_engine() == MYSQL:
            return MySqlEngine.get_page_sql_args(sql, page_num, page_size, *args)
        elif Engine.current_engine() == POSTGRESQL:
            return PostgresEngine.get_page_sql_args(sql, page_num, page_size, *args)
        elif Engine.current_engine() == SQLITE:
            return SQLiteEngine.get_page_sql_args(sql, page_num, page_size, *args)
        raise NotImplementedError(f"Not implement method 'get_page_sql_args' for {Engine.current_engine()}.")

    @staticmethod
    def get_select_key(*args, **kwargs):
        if Engine.current_engine() == MYSQL:
            return MySqlEngine.get_select_key()
        elif Engine.current_engine() == POSTGRESQL:
            return PostgresEngine.get_select_key(*args, **kwargs)
        elif Engine.current_engine() == SQLITE:
            return SQLiteEngine.get_select_key()
        raise NotImplementedError(f"Not implement method 'get_select_key' for {Engine.current_engine()}, you can use orm snowflake for primary key.")

    @staticmethod
    def get_table_columns(table: str):
        if Engine.current_engine() == MYSQL:
            return MySqlEngine.get_table_columns(table)
        elif Engine.current_engine() == POSTGRESQL:
            return PostgresEngine.get_table_columns(table)
        elif Engine.current_engine() == SQLITE:
            return SQLiteEngine.get_table_columns(table)
        raise "*"


class BaseEngine(SupperEngine):

    @staticmethod
    def get_page_sql_args(sql: str, page_num: int, page_size: int, *args):
        start = get_page_start(page_num, page_size)
        if require_limit(sql):
            sql = '{} LIMIT ? OFFSET ?'.format(sql)
        args = [*args, page_size, start]
        return sql, args

    def before_execute(self, function: str, sql: str, *args):
        if self.show_sql:
            logger.info("Exec func 'sqlexec.%s' \n\tSQL: %s \n\tARGS: %s" % (function, sql, args))
        if '%' in sql and 'like' in sql.lower():
            sql = sql.replace('%', '%%').replace('%%%%', '%%')
        return sql.replace('?', '%s')


class MySqlEngine(BaseEngine):

    @classmethod
    def init(cls, name=MYSQL):
        super().init(name)

    @staticmethod
    def create_insert_sql(table: str, cols: Sequence[str]):
        columns, placeholders = zip(*[('`{}`'.format(col), '?') for col in cols])
        return 'INSERT INTO `{}`({}) VALUES({})'.format(table, ','.join(columns), ','.join(placeholders))

    @staticmethod
    def get_page_sql_args(sql: str, page_num: int, page_size: int, *args):
        start = get_page_start(page_num, page_size)
        if require_limit(sql):
            sql = '{} LIMIT ?, ?'.format(sql)
        args = [*args, start, page_size]
        return sql, args

    @staticmethod
    def get_table_columns(table: str):
        return get(MYSQL_COLUMN_SQL, table, LIMIT_1)

    @staticmethod
    def get_select_key():
        return MYSQL_SELECT_KEY


class PostgresEngine(BaseEngine):

    @classmethod
    def init(cls, name=POSTGRESQL):
        super().init(name)
    @staticmethod
    def get_table_columns(table: str):
        return get(POSTGRES_COLUMN_SQL, table, LIMIT_1)

    @staticmethod
    def get_select_key(key_seq: str = None, table: str = None, key: str =None, sql: str = None):
        if not key_seq:
            if table:
                key_seq = PostgresEngine.build_key_seq(table, key)
            else:
                if sql:
                    key_seq = PostgresEngine._get_key_seq_from_sql(sql)
                else:
                    raise DBError("Get PostgreSQL select key fail, all of 'key_seq', 'table', 'sql' are None")
        return f"SELECT currval('{key_seq}')"

    @staticmethod
    def build_key_seq(table: str, key: str = None):
        if not key:
            key = DEFAULT_KEY_FIELD
        return f'{table}_{key}_seq'

    @staticmethod
    @lru_cache(maxsize=CACHE_SIZE)
    def _get_key_seq_from_sql(sql: str):
        table = re.search('(?<=into )\w+', sql, re.I)
        key_seq = PostgresEngine.build_key_seq(table.group())
        logger.warning("'key_seq' is None, will use default '{}' from sql.".format(key_seq))
        return key_seq


class OracleEngine(BaseEngine):

    @classmethod
    def init(cls, name=ORACLE):
        super().init(name)

    @staticmethod
    def get_page_sql_args(sql: str, page_num: int, page_size: int, *args):
        start = get_page_start(page_num, page_size)
        end = start + page_size
        sql = 'SELECT * FROM (SELECT tmp.*, rownum row_num FROM ({}) tmp WHERE rownum <= >) WHERE row_num > :startRow '.format(sql)
        args = [*args, end, start]
        return sql, args

    @staticmethod
    def get_table_columns(table: str):
        results = select('SELECT column_name FROM user_tab_columns WHERE table_name = ?')
        return ','.join([result[0] for result in results])

    @staticmethod
    def get_select_key(key_seq: str):
        # return get(f"SELECT {key_seq}.nextval FROM dual")
        raise NotImplementedError(f"Not implement method 'get_select_key' for {Engine.current_engine()}, you can use orm snowflake for primary key.")


class SQLiteEngine(BaseEngine):

    @classmethod
    def init(cls, name=SQLITE):
        super().init(name)

    @staticmethod
    def get_table_columns(table: str):
        results = query(f'PRAGMA table_info({table})')
        return ','.join([result['name'] for result in results])

    @staticmethod
    def get_select_key():
        return SQLITE_SELECT_KEY

    def before_execute(self, function: str, sql: str, *args):
        if self.show_sql:
            logger.info("Exec func 'sqlexec.%s' \n\tSQL: %s \n\tARGS: %s" % (function, sql, args))
        if '%' in sql and 'like' in sql.lower():
            sql = sql.replace('%', '%%').replace('%%%%', '%%')
        return sql
