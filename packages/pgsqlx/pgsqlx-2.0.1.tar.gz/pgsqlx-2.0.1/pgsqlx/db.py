from . import PostgresEngine
from .log_support import save_log, save_key_seq_log

# Don't remove. Import for not repetitive implementation
from sqlbatis.db import insert, save_select_key, execute, batch_insert, batch_execute, get, query, query_one, select, select_one,\
    do_execute, do_get, do_query, do_query_one, do_select, do_select_one, do_select_page, do_query_page, select_page, query_page, sql


def save(table: str, **kwargs):
    """
    Insert data into table, return primary key.
    :param table: table
    :param kwargs:
    :return: Primary key
    """
    save_log(table, **kwargs)
    return save_key_seq(PostgresEngine.build_key_seq(table), table, **kwargs)


def save_key_seq(key_seq: str, table: str, **kwargs):
    """
    Insert data into table, return primary key.
    :param key_seq: primary key sequnece
    :param table: table
    :param kwargs:
    :return: Primary key
    """
    save_key_seq_log(key_seq, table, **kwargs)
    return save_select_key(PostgresEngine.get_select_key(key_seq=key_seq, table=table), table, **kwargs)
