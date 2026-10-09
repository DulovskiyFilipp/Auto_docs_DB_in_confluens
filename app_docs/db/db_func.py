from app_docs.db.db_connect import db_connect_session
from app_docs.db.sql_request import (req_max_log_id, #Запрос максимального id лога документирования
                         req_log_db_sql, #Скрипт запроса логов изменения DDL
                         req_mtd_tbl_sql, #Шаблон запроса метаданных объектов БД
                         ins_log_db_sql, #Шаблон лога процесса документирования
                         ins_log_db_sql_oper #Шаблон лога документирования объекта
                         )

def log_docs_prc(status: str, log_id: int|None = None, err_msg: str = 'NULL'):
    """Лог процесса документирования"""

    with db_connect_session() as conn:
        with conn.cursor() as cursor:
            if status == 'START':
                cursor.execute(req_max_log_id)
                log_id = cursor.fetchone()[0] + 1
            cursor.execute(ins_log_db_sql.render(id=log_id, status=status, msg=err_msg))
            conn.commit()
            cursor.close()
            return log_id


def log_oper(status: str, log_hist_id: int, schema_name: str, tbl_name: str = 'NULL', msg_log: str = 'NULL'):
    """Лог обработки объектов при документировании"""

    with db_connect_session() as conn:
        with conn.cursor() as cursor:
            cursor.execute(ins_log_db_sql_oper.render(log_hist_id=log_hist_id, status=status, schema_name=schema_name, tbl_name=tbl_name, msg_log=msg_log))
            conn.commit()
            cursor.close()


def req_log_ddl_db():
    """Выгрузка логов из DB"""

    with db_connect_session() as conn:
        with conn.cursor() as cursor:
            cursor.execute(req_log_db_sql)
            logs = cursor.fetchall()
            return logs


def req_mtd_ddl_db(schema_name: str, tbl_name: str):
    """Выгрузка метаданных таблиц из DB"""

    with db_connect_session() as conn:
        with conn.cursor() as cursor:
            cursor.execute(req_mtd_tbl_sql.render(schema= schema_name, table_name=tbl_name))
            meta_date = cursor.fetchall()
            return meta_date
