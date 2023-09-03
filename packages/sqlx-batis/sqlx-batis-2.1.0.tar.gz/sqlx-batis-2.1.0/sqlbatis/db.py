from sqlexec.exec import try_mapping
from . import sql_support, Engine, DBError
from .log_support import save_log, do_page_log, page_log

# Don't remove. Import for not repetitive implementation
from sqlexec import insert, save as save_select_key, batch_insert, batch_execute, do_save_sql, do_execute, do_get, do_query, do_query_one, \
    do_select, do_select_one


def save(table: str, **kwargs):
    """
    Insert data into table, return primary key.
    :param table: table
    :param kwargs:
    :return: Primary key
    """
    save_log(table, **kwargs)
    try:
        select_key = Engine.get_select_key_intf(table=table)
    except NotImplementedError:
        raise DBError(f"Expect 'select_key' but not. you may should use 'save_select_key' func with 'select_key'.")
    return save_select_key(select_key, table, **kwargs)


def save_sql(select_key: str, sql: str, *args, **kwargs):
    """
    Insert data into table, return primary key.
    :param select_key: sql for select primary key
    :param sql: SQL
    :param args:
    :return: Primary key
    """
    sql, args = _try_dynamic_sql('sqlbatis.db.save_sql', sql, *args, **kwargs)
    return do_save_sql(select_key, sql, *args)


def execute(sql: str, *args, **kwargs):
    """
    Execute SQL.
    sql: INSERT INTO user(name, age) VALUES(?, ?)  -->  args: ('张三', 20)
         INSERT INTO user(name, age) VALUES(:name,:age)  -->  kwargs: {'name': '张三', 'age': 20}
    """
    sql, args = _try_dynamic_sql('sqlbatis.db.execute', sql, *args, **kwargs)
    return do_execute(sql, *args)


# ----------------------------------------------------------Query function------------------------------------------------------------------
def get(sql: str, *args, **kwargs):
    """
    Execute select SQL and expected one int and only one int result. Automatically add 'limit ?' after sql statement if not.
    MultiColumnsError: Expect only one column.
    sql: SELECT count(1) FROM user WHERE name=? and age=? limit 1  -->  args: ('张三', 20)
         SELECT count(1) FROM user WHERE name=:name and age=:age limit 1  -->  kwargs: ('张三', 20) --> kwargs: {'name': '张三', 'age': 20}
    """
    sql, args = _try_dynamic_sql('sqlbatis.db.get', sql, *args, **kwargs)
    return do_get(sql, *args)


def query(sql: str, *args, **kwargs):
    """
    Execute select SQL and return list or empty list if no result.
    sql: SELECT * FROM user WHERE name=? and age=?  -->  args: ('张三', 20)
         SELECT * FROM user WHERE name=:name and age=:age  -->  kwargs: ('张三', 20) --> kwargs: {'name': '张三', 'age': 20}
    """
    sql, args = _try_dynamic_sql('sqlbatis.db.query', sql, *args, **kwargs)
    return do_query(sql, *args)


def query_one(sql: str, *args, **kwargs):
    """
    Execute select SQL and expected one row result(dict). Automatically add 'limit ?' after sql statement if not.
    If no result found, return None.
    If multiple results found, the first one returned.
    sql: SELECT * FROM user WHERE name=? and age=? limit 1 -->  args: ('张三', 20)
         SELECT * FROM user WHERE name=:name and age=:age limit 1  -->  kwargs: ('张三', 20) --> kwargs: {'name': '张三', 'age': 20}
    """
    sql, args = _try_dynamic_sql('sqlbatis.db.query_one', sql, *args, **kwargs)
    return do_query_one(sql, *args)


def select(sql: str, *args, **kwargs):
    """
    Execute select SQL and return list(tuple) or empty list if no result.
    sql: SELECT * FROM user WHERE name=? and age=?  -->  args: ('张三', 20)
         SELECT * FROM user WHERE name=:name and age=:age   -->  kwargs: ('张三', 20) --> kwargs: {'name': '张三', 'age': 20}
    """
    sql, args = _try_dynamic_sql('sqlbatis.db.select', sql, *args, **kwargs)
    return do_select(sql, *args)


def select_one(sql: str, *args, **kwargs):
    """
    Execute select SQL and expected one row result(tuple). Automatically add 'limit ?' after sql statement if not.
    If no result found, return None.
    If multiple results found, the first one returned.
    sql: SELECT * FROM user WHERE name=? and age=? limit 1  -->  args: ('张三', 20)
         SELECT * FROM user WHERE name=:name and age=:age limit 1  -->  kwargs: ('张三', 20) --> kwargs: {'name': '张三', 'age': 20}
    """
    sql, args = _try_dynamic_sql('sqlbatis.db.select_one', sql, *args, **kwargs)
    return do_select_one(sql, *args)


# ----------------------------------------------------------Page function------------------------------------------------------------------
def query_page(sql: str, page_num=1, page_size=10, *args, **kwargs):
    """
    Execute select SQL and return list or empty list if no result. Automatically add 'limit ?,?' after sql statement if not.
    sql: SELECT * FROM user WHERE name=? and age=?  -->  args: ('张三', 20)
         SELECT * FROM user WHERE name=:name and age=:age  -->  kwargs: ('张三', 20) --> kwargs: {'name': '张三', 'age': 20}
    """
    sql, args = _try_mapping('query_page', sql, page_num, page_size, *args, **kwargs)
    return do_query_page(sql, page_num, page_size, *args)


def select_page(sql: str, page_num=1, page_size=10, *args, **kwargs):
    """
    Execute select SQL and return list(tuple) or empty list if no result. Automatically add 'limit ?,?' after sql statement if not.
    sql: SELECT * FROM user WHERE name=? and age=?  -->  args: ('张三', 20)
         SELECT * FROM user WHERE name=:name and age=:age   -->  kwargs: ('张三', 20) --> kwargs: {'name': '张三', 'age': 20}
    """
    sql, args = _try_mapping('select_page', sql, page_num, page_size, *args, **kwargs)
    return do_select_page(sql, page_num, page_size, *args)


def do_query_page(sql: str, page_num=1, page_size=10, *args):
    """
    Execute select SQL and return list results(dict).
    sql: SELECT * FROM user WHERE name=? and age=?  -->  args: ('张三', 20)
    """
    sql, args = _do_page_sql_args('do_query_page', sql, page_num, page_size, *args)
    return do_query(sql, *args)


def do_select_page(sql: str, page_num=1, page_size=10, *args):
    """
    Execute select SQL and return list results(dict).
    sql: SELECT * FROM user WHERE name=? and age=?  -->  args: ('张三', 20)
    """
    sql, args = _do_page_sql_args('do_select_page', sql, page_num, page_size, *args)
    return do_select(sql, *args)


from .sql_exec import createSqlExec
def sql(sql: str) :
    return createSqlExec(sql)


def _try_dynamic_sql(function, sql, *args, **kwargs):
    sql = sql_support.dynamic_sql(sql, **kwargs)
    return try_mapping(function, sql, *args, **kwargs)


def _try_mapping(function, sql, page_num, page_size, *args, **kwargs):
    page_log(function, sql, page_num, page_size, *args, **kwargs)
    sql = sql_support.dynamic_sql(sql, **kwargs)
    return sql_support.get_mapping_sql_args(sql, *args, **kwargs)


def _do_page_sql_args(function, sql, page_num, page_size, *args):
    do_page_log(function, sql.strip(), page_num, page_size, *args)
    return Engine.get_page_sql_args_intf(sql, page_num, page_size, *args)


