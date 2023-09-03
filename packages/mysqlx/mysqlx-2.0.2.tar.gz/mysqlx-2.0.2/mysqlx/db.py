from . import MySqlEngine
from .log_support import save_log

# Don't remove. Import for not repetitive implementation
from sqlbatis.db import insert, save_select_key, execute, batch_insert, batch_execute, get, query, query_one, select, select_one, do_execute,\
    do_get, do_query, do_query_one, do_select, do_select_one, do_query_page, do_select_page, query_page, select_page, sql


def save(table: str, **kwargs):
    """
    Insert data into table, return primary key.
    :param table: table
    :param kwargs:
    :return: Primary key
    """
    save_log(table, **kwargs)
    return save_select_key(MySqlEngine.get_select_key(), table, **kwargs)
