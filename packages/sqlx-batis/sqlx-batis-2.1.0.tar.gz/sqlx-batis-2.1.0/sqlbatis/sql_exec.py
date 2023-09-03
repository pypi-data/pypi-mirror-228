from . import db
from sqlexec.sql_exec import SqlExec as SupperSqlExec


def createSqlExec(sql: str) :
    assert sql, "Parameter 'sql' must not be none"
    return SqlExec(sql, db)


class SqlExec(SupperSqlExec):
    def __init__(self, sql, executor):
        super().__init__(sql, executor)

    def query_page(self, page_num=1, page_size=10, *args, **kwargs):
        """
        Execute select SQL and return list or empty list if no result. Automatically add 'limit ?,?' after sql statement if not.
        sql: SELECT * FROM user WHERE name=? and age=?  -->  args: ('张三', 20)
             SELECT * FROM user WHERE name=:name and age=:age  -->  kwargs: ('张三', 20) --> kwargs: {'name': '张三', 'age': 20}
        """
        return self.executor.query_page(self.sql, page_num, page_size, *args, **kwargs)

    def select_page(self, page_num=1, page_size=10, *args, **kwargs):
        """
        Execute select SQL and return list(tuple) or empty list if no result. Automatically add 'limit ?,?' after sql statement if not.
        sql: SELECT * FROM user WHERE name=? and age=?  -->  args: ('张三', 20)
             SELECT * FROM user WHERE name=:name and age=:age   -->  kwargs: ('张三', 20) --> kwargs: {'name': '张三', 'age': 20}
        """
        return self.executor.select_page(self.sql, page_num, page_size, *args, **kwargs)

    def do_query_page(self, page_num=1, page_size=10, *args):
        """
        Execute select SQL and return list results(dict).
        sql: SELECT * FROM user WHERE name=? and age=?  -->  args: ('张三', 20)
        """
        return self.executor.do_query_page(self.sql, page_num, page_size, *args)

    def do_select_page(self, page_num=1, page_size=10, *args):
        """
        Execute select SQL and return list results(dict).
        sql: SELECT * FROM user WHERE name=? and age=?  -->  args: ('张三', 20)
        """
        return self.executor.do_select_page(self.sql, page_num, page_size, *args)
    
    def page(self, page_num=1, page_size=10):
        return Page(self, page_num, page_size)


class Page:
    def __init__(self, sql_exec, page_num=1, page_size=10):
        self._sql_exec = sql_exec
        self._page_num = page_num
        self._page_size = page_size

    def query(self, *args, **kwargs):
        """
        Execute select SQL and return list or empty list if no result. Automatically add 'limit ?,?' after sql statement if not.
        sql: SELECT * FROM user WHERE name=? and age=?  -->  args: ('张三', 20)
             SELECT * FROM user WHERE name=:name and age=:age  -->  kwargs: ('张三', 20) --> kwargs: {'name': '张三', 'age': 20}
        """
        return self._sql_exec.query_page(self._page_num, self._page_size, *args, **kwargs)

    def select(self, *args, **kwargs):
        """
        Execute select SQL and return list(tuple) or empty list if no result. Automatically add 'limit ?,?' after sql statement if not.
        sql: SELECT * FROM user WHERE name=? and age=?  -->  args: ('张三', 20)
             SELECT * FROM user WHERE name=:name and age=:age   -->  kwargs: ('张三', 20) --> kwargs: {'name': '张三', 'age': 20}
        """
        return self._sql_exec.select_page(self._page_num, self._page_size, *args, **kwargs)

    def do_query(self, *args):
        """
        Execute select SQL and return list results(dict).
        sql: SELECT * FROM user WHERE name=? and age=?  -->  args: ('张三', 20)
        """
        return self._sql_exec.do_query_page(self._page_num, self._page_size, *args)

    def do_select(self, *args):
        """
        Execute select SQL and return list results(dict).
        sql: SELECT * FROM user WHERE name=? and age=?  -->  args: ('张三', 20)
        """
        return self._sql_exec.do_select_page(self._page_num, self._page_size, *args)
