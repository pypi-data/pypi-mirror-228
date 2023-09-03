from .engine import Engine
from typing import Sequence, Union, List, Tuple

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
