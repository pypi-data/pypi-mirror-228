from .engine import Engine
from .sql_exec import Page
from .constant import NO_LIMIT
from .sql_support import simple_sql
from typing import Sequence, Union, List, Tuple
from .db import do_execute, do_get, do_select, do_query, do_query_page, do_select_page


class FieldExec:
    def __init__(self, cls, *fields):
        self._cls = cls
        self._fields = fields

    def where(self, where: str):
        return WhereExec(self._cls, where, *self._fields)

    def page(self, page_num=1, page_size=10):
        return OrmPage(self.where(None), page_num, page_size)

    def find(self, **kwargs):
        """
        Return list(object) or empty list if no result.
        persons = Person.fields('id', 'name', 'age').find(name='张三', age=55)
        """
        return self._cls.find(*self._fields, **kwargs)

    def find_one(self, **kwargs):
        """
        Return unique result(object) or None if no result.
        person = Person.fields('id', 'name', 'age').find_one(name='张三', age=55)
        """
        return self._cls.find_one(*self._fields, **kwargs)

    # def find_by(self, where: str, *args, **kwargs):
    #     """
    #     Return list(dict) or empty list if no result.
    #     rows = Person.fields('id', 'name', 'age').find_by('where name=?', '李四')
    #     """
    #     return [self._cls.to_obj(**d) for d in self.query_by(where, *args, **kwargs)]

    def find_by_id(self, _id: Union[int, str]):
        """
        Return one class object or None if no result.
        person = Person.fields('id', 'name', 'age').find_by_id(1)
        :param _id: key
        """
        return self._cls.find_by_id(_id, *self._fields)

    def find_by_ids(self, *ids):
        """
        Return list(class object) or empty list if no result.
        persons = Person.fields('id', 'name', 'age').find_by_ids(1,2)
        :param ids: List of key
        """
        return self._cls.find_by_ids(ids, *self._fields)

    def query(self, **kwargs):
        """
        Return list(dict) or empty list if no result.
        persons = Person.fields('id', 'name', 'age').query(name='张三', age=55)
        """
        return self._cls.query(*self._fields, **kwargs)

    def query_one(self, **kwargs):
        """
        Return unique result(dict) or None if no result.
        persons = Person.fields('id', 'name', 'age').query_one(name='张三', age=55)
        """
        return self._cls.query_one(*self._fields, **kwargs)

    # def query_by(self, where: str, *args, **kwargs):
    #     """
    #     Return list(dict) or empty list if no result.
    #     rows = Person.fields('id', 'name', 'age').query_by('where name=?', '李四')
    #     """
    #     sql, args = self._get_by_sql_args(where, *args, **kwargs)
    #     return do_query(sql, *args)

    def query_by_id(self, _id: Union[int, str]):
        """
        Return one row(dict) or None if no result.
        person = Person.fields('id', 'name', 'age').query_by_id(1)
        :param _id: key
        """
        return self._cls.query_by_id(_id, *self._fields)

    def query_by_ids(self, *ids):
        """
        Return list(dict) or empty list if no result.
        persons = Person.fields('id', 'name', 'age').query_by_ids(1,2)
        :param ids: List of key
        """
        return self._cls.query_by_ids(ids, *self._fields)

    def select(self, **kwargs):
        """
        Return list(dict) or empty list if no result.
        rows = Person.fields('id', 'name', 'age').select(name='张三', age=55)
        """
        return self._cls.select(*self._fields, **kwargs)

    def select_one(self, **kwargs):
        """
        Return unique result(tuple) or None if no result.
        row = Person.fields('id', 'name', 'age').select_one(name='张三', age=55)
        """
        return self._cls.select_one(*self._fields, **kwargs)

    # def select_by(self, where: str, *args, **kwargs):
    #     """
    #     Return list(dict) or empty list if no result.
    #     rows = Person.select_by_where('where name=?', '李四')
    #     """
    #     assert where and where.strip().lower().startswith('where'), "Parameter 'where' must startswith 'WHERE'"
    #     sql, args = self._get_by_sql_args(where, *args, **kwargs)
    #     return do_select(sql, *args)

    def select_by_id(self, _id: Union[int, str]):
        """
        Return one row(dict) or None if no result.
        row = Person.fields('id', 'name', 'age').select_by_id(1)
        :param _id: key
        """
        return self._cls.select_by_id(_id, *self._fields)

    def select_by_ids(self, *ids):
        """
        Return list(dict) or empty list if no result.
        rows = Person.select_by_ids([1,2], 'id', 'name', 'age')
        :param ids: List of key
        :param fields: Default select all fields if not set
        """
        return self._cls.select_by_ids(ids, *self._fields)

    def find_page(self, page_num=1, page_size=10, **kwargs):
        """
        Return list(object) or empty list if no result.
        persons = Person.fields('id', 'name', 'age').find_page(1, 10, name='张三', age=55)
        :param page_num: page number
        :param page_size: page size
        """
        return self._cls.find_page(page_num, page_size, *self._fields, **kwargs)

    # def find_page_by(self, page_num: int, page_size: int, where: str, *args, **kwargs):
    #     """
    #     Return list(dict) or empty list if no result. Automatically add 'limit ?,?' after where if not.
    #     rows = Person.find_by_page(1, 10, 'where name=?', '李四')
    #     """
    #     return [self._cls.to_obj(**d) for d in self.query_page_by(page_num, page_size, where, *args, **kwargs)]

    def query_page(self, page_num=1, page_size=10, **kwargs):
        """
        Return list(dict) or empty list if no result.
        persons = Person.fields('id', 'name', 'age').query_page(1, 10, name='张三', age=55)
        :param page_num: page number
        :param page_size: page size
        """
        return self._cls.query_page(page_num, page_size, *self._fields, **kwargs)

    # def query_page_by(self, page_num: int, page_size: int, where: str, *args, **kwargs):
    #     """
    #     Return list(dict) or empty list if no result. Automatically add 'limit ?,?' after where if not.
    #     rows = Person.fields('id', 'name', 'age').query_by_page(1, 10, 'where name=?', '李四')
    #     """
    #     assert where and where.strip().lower().startswith('where'), "Parameter 'where' must startswith 'WHERE'"
    #     sql, args = self._get_by_sql_args(where, *args, **kwargs)
    #     return do_query_page(sql, page_num, page_size, *args)

    def select_page(self, page_num=1, page_size=10, **kwargs):
        """
        Return list(dict) or empty list if no result.
        rows = Person.fields('id', 'name', 'age').select_page(1, 10, name='张三', age=55)
        :param page_num: page number
        :param page_size: page size
        """
        return self._cls.select_page(page_num, page_size, *self._fields, **kwargs)

    # def select_page_by(self, page_num: int, page_size: int, where: str, *args, **kwargs):
    #     """
    #     Return list(dict) or empty list if no result. Automatically add 'limit ?,?' after where if not.
    #     rows = Person.fields('id', 'name', 'age').select_by_page(1, 10, 'where name=?', '李四')
    #     """
    #     assert where and where.strip().lower().startswith('where'), "Parameter 'where' must startswith 'WHERE'"
    #     sql, args = self._get_by_sql_args(where, *args, **kwargs)
    #     return do_select_page(sql, page_num, page_size, *args)


class WhereExec:
    def __init__(self, cls, where, *fields):
        self._cls = cls
        self._where = where
        self._fields = fields

    def fields(self, *fields):
        self._fields = fields
        return self

    def page(self, page_num=1, page_size=10):
        return OrmPage(self, page_num, page_size)

    def delete(self, *args, **kwargs):
        """
        Physical delete
        rowcount = Person.delete_by('where name=? and age=?', '张三', 55)
        return: Effect rowcount
        """
        table = self._cls.get_table()
        sql = 'DELETE FROM %s %s' % (table, self._where)
        sql, args = simple_sql(sql, *args, **kwargs)
        return do_execute(sql, *args)

    def count(self, *args, **kwargs):
        """
        Automatically add 'limit ?' where if not.
        count = Person.count_by('where name=?', '李四')
        """
        table = self._cls.get_table()
        sql = "SELECT count(1) FROM {} {}".format(table, self._where)
        sql, args = simple_sql(sql, *args, **kwargs)
        return do_get(sql, *args)

    def exists(self, *args, **kwargs):
        table = self._cls.get_table()
        sql = "SELECT 1 FROM {} {}".format(table, self._where)
        sql, args = simple_sql(sql, *args, **kwargs)
        return do_get(sql, *args) == 1

    def select(self, *args, **kwargs):
        """
        Return list(dict) or empty list if no result.
        rows = Person.where('where name=?').select('李四')
        """
        sql, args = self._get_by_sql_args(self._where, *args, **kwargs)
        return do_select(sql, *args)

    def query(self, *args, **kwargs):
        """
        Return list(dict) or empty list if no result.
        rows = Person.where('where name=?').query('李四')
        """
        sql, args = self._get_by_sql_args(self._where, *args, **kwargs)
        return do_query(sql, *args)

    def find(self, *args, **kwargs):
        """
        Return list(dict) or empty list if no result.
        rows = Person.where('where name=?').find('李四')
        """
        return [self._cls.to_obj(**d) for d in self.query(*args, **kwargs)]

    def select_page(self, page_num=1, page_size=10, *args, **kwargs):
        """
        Return list(dict) or empty list if no result.
        rows = Person.where('where name=?').select('李四')
        """
        sql, args = self._get_by_sql_args(self._where, *args, **kwargs)
        return do_select_page(sql, page_num, page_size, *args)

    def query_page(self, page_num=1, page_size=10, *args, **kwargs):
        """
        Return list(dict) or empty list if no result.
        rows = Person.where('where name=?').query('李四')
        """
        sql, args = self._get_by_sql_args(self._where, *args, **kwargs)
        return do_query_page(sql, page_num, page_size, *args)

    def find_page(self, page_num=1, page_size=10, *args, **kwargs):
        """
        Return list(dict) or empty list if no result.
        rows = Person.where('where name=?').find('李四')
        """
        return [self._cls.to_obj(**d) for d in self.query_page(page_num, page_size, *args, **kwargs)]

    def _get_by_sql_args(self, where: str, *args, **kwargs):
        if where and not where.strip().lower().startswith('where'):
            raise ValueError("Must startswith 'WHERE'")

        table = self._cls.get_table()
        sql = get_select_sql(table, where, NO_LIMIT, *self._fields)
        return simple_sql(sql, *args, **kwargs)


class OrmPage(Page):

    def where(self, where: str):
        self._sql_exec._where = where
        return self

    def fields(self, *fields):
        self._sql_exec.fields(*fields)
        return self

    def find(self, *args, **kwargs):
        """
        Execute select SQL and return list or empty list if no result. Automatically add 'limit ?,?' after sql statement if not.
        sql: SELECT * FROM user WHERE name=? and age=?  -->  args: ('张三', 20)
             SELECT * FROM user WHERE name=:name and age=:age  -->  kwargs: ('张三', 20) --> kwargs: {'name': '张三', 'age': 20}
        """
        return self._sql_exec.find_page(self._page_num, self._page_size, *args, **kwargs)

    def do_find(self, *args):
        """
        Execute select SQL and return list or empty list if no result. Automatically add 'limit ?,?' after sql statement if not.
        sql: SELECT * FROM user WHERE name=? and age=?  -->  args: ('张三', 20)
        """
        return self.find(*args)


def get_select_sql(table: str, where: str, limit: Union[int, Tuple[int], List[int]], *fields):
    if fields:
        fields = ','.join([col if '(' in col else '{}'.format(col) for col in fields])
    else:
        fields = Engine.get_table_columns_intf(table)

    if limit:
        if isinstance(limit, int):
            return 'SELECT {} FROM {} {} LIMIT ?'.format(fields, table, where)
        elif (isinstance(limit, Tuple) or isinstance(limit, List)) and len(limit) == 2:
            return 'SELECT {} FROM {} {} LIMIT ? OFFSET ?'.format(fields, table, where)
        else:
            raise ValueError("The type of the parameter 'limit' must be 'int' or tuple, list, and it length is 2.")
    else:
        return 'SELECT {} FROM {} {}'.format(fields, table, where)


def get_condition_arg(k: str, v: object):
    if k.endswith("__eq"):
        return "{} = ?".format(k[:-4]), v
    if k.endswith("__ne"):
        return "{} != ?".format(k[:-4]), v
    if k.endswith("__gt"):
        return "{} > ?".format(k[:-4]), v
    if k.endswith("__lt"):
        return "{} < ?".format(k[:-4]), v
    if k.endswith("__ge"):
        return "{} >= ?".format(k[:-4]), v
    if k.endswith("__gte"):
        return "{} >= ?".format(k[:-5]), v
    if k.endswith("__le"):
        return "{} <= ?".format(k[:-4]), v
    if k.endswith("__lte"):
        return "{} <= ?".format(k[:-5]), v
    if k.endswith("__isnull"):
        return "{} is {}".format(k[:-8], 'null' if v else 'not null'), None
    if k.endswith("__in") and isinstance(v, Sequence) and not isinstance(v, str):
        return "{} in({})".format(k[:-4], ','.join(['?' for _ in v])), v
    if k.endswith("__in"):
        return "{} in({})".format(k[:-4], '?'), v
    if k.endswith("__not_in") and isinstance(v, Sequence) and not isinstance(v, str):
        return "{} not in({})".format(k[:-8], ','.join(['?' for _ in v])), v
    if k.endswith("__not_in"):
        return "{} not in({})".format(k[:-8], '?'), v
    if k.endswith("__like"):
        return "{} like ?".format(k[:-6], '?'), v
    if k.endswith("__startswith"):
        return "{} like ?".format(k[:-12]), '{}%'.format(v)
    if k.endswith("__endswith"):
        return "{} like ?".format(k[:-10]), '%{}'.format(v)
    if k.endswith("__contains"):
        return "{} like ?".format(k[:-10]), '%{}%'.format(v)
    if k.endswith("__range") and isinstance(v, Sequence) and 2 == len(v) and not isinstance(v, str):
        col = k[:-7]
        return "{} >= ? and {} <= ?".format(col, col), v
    if k.endswith("__between") and isinstance(v, Sequence) and 2 == len(v) and not isinstance(v, str):
        return "{} between ? and ?".format(k[:-9]), v
    if k.endswith("__range") or k.endswith("__between"):
        return ValueError("Must is instance of Sequence with length 2 when use range or between statement")

    return "{} = ?".format(k), v


def get_where_arg_limit(**kwargs):
    where, args, limit = '', [], 0
    if 'limit' in kwargs:
        limit = kwargs.pop('limit')

    if kwargs:
        conditions, tmp_args = zip(*[get_condition_arg(k, v) for k, v in kwargs.items()])
        tmp_args = [arg for arg in tmp_args if arg is not None]

        for arg in tmp_args:
            if arg:
                if isinstance(arg, Sequence) and not isinstance(arg, str):
                    args.extend(arg)
                else:
                    args.append(arg)
        where = 'WHERE {}'.format(' and '.join(conditions))

    return where, args, limit


def split_ids(ids: Sequence[int], batch_size):
    return [ids[i:i + batch_size] for i in range(0, len(ids), batch_size)]


def get_table_name(class_name):
    for i in range(1, len(class_name) - 1)[::-1]:
        if class_name[i].isupper():
            class_name = class_name[:i] + '_' + class_name[i:]
    return class_name.lower()
