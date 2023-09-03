from . import dbx
from sqlbatis.sql_id_exec import SqlIdExec

def createSqlIdExec(sql_id: str) :
    assert sql_id, "Parameter 'sql_id' must not be none"
    return SqlIdExec(sql_id, dbx)