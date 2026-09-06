from db_connect import db_connect_session
from sql_request import (ins_log_db_sql_st, #Шаблон лога старта процесса документирования
                         ins_log_db_sql_ed, #Шаблон лога окончания процесса документирования
                         req_max_log_id, #Запрос максимального id лога документирования
                         ins_log_db_sql_er, #Шаблон лога ошибки процесса документирования
                         ins_log_db_sql_dn, #Шаблон лога успешного документирования объекта
                         ins_log_db_sql_err, #Шаблон лога не успешного документирования объекта
                         req_log_db_sql, #Скрипт запроса логов изменения DDL
                         req_mtd_tbl_sql #Шаблон запроса метаданных объектов БД
                         )


#Лог процесса документирования
def log_docs_prc(log_type: str, log_id: int|None = None, err_msg: str|None = None):
    conn = db_connect_session()
    cursor = conn.cursor()
    if log_type == 'S':
        cursor.execute(req_max_log_id)
        log_hist_id = cursor.fetchone()[0] + 1
        cursor.execute(ins_log_db_sql_st.render(id=log_hist_id))
        conn.commit()
        cursor.close()
        return log_hist_id
    elif log_type == 'E':
        cursor.execute(ins_log_db_sql_ed.render(id=log_id))
        conn.commit()
        cursor.close()
        return None
    else:
        cursor.execute(ins_log_db_sql_er.render(id=log_id, msg=err_msg))
        conn.commit()
        cursor.close()
        return None

#Лог обработки объектов при документировании
def log_success_err(log_type: str, log_hist_id: int, schema_name: str, tbl_name: str|None = None, msg_log: str|None = None):
    conn = db_connect_session()
    cursor = conn.cursor()
    if log_type == 'S':
        cursor.execute(ins_log_db_sql_dn.render(log_hist_id=log_hist_id, schema_name=schema_name))
        conn.commit()
        cursor.close()
    else:
        cursor.execute(ins_log_db_sql_err.render(log_hist_id=log_hist_id, schema_name=schema_name, tbl_name=tbl_name, msg_log=msg_log))
        conn.commit()
        cursor.close()

#Выгрузка логов из DB
def req_log_ddl_db():
    conn = db_connect_session()
    cursor = conn.cursor()
    cursor.execute(req_log_db_sql)
    logs = cursor.fetchall()
    return logs


#Выгрузка метаданных таблиц из DB
def req_mtd_ddl_db(schema_name: str, tbl_name: str):
    conn = db_connect_session()
    cursor = conn.cursor()
    cursor.execute(req_mtd_tbl_sql.render(schema= schema_name, table_name=tbl_name))
    meta_date = cursor.fetchall()
    return meta_date

