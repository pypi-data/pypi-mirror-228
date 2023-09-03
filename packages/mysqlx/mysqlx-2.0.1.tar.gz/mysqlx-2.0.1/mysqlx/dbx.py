from . import MySqlEngine
from .log_support import sql_id_log
from sqlbatis import sql_holder as holder
from sqlbatis.dbx import insert, save_select_key, batch_insert, batch_execute, execute, get, query, query_one, select, select_one, sql


def save(sql_id: str, *args, **kwargs):
    """
    Execute insert SQL, return primary key.
    :return: Primary key
    """
    sql_id_log('save', sql_id, *args, **kwargs)

    select_key = MySqlEngine.get_select_key()
    return save_select_key(select_key, sql_id, *args, **kwargs)
