from . import dbx
from .sql_exec import SqlExec

def createSqlIdExec(sql_id: str) :
    assert sql_id, "Parameter 'sql' must not be none"
    return SqlIdExec(sql_id, dbx)


class SqlIdExec(SqlExec):

    def save(self, *args, **kwargs):
        return self.executor.save(self.sql, *args, **kwargs)
