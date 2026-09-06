from jinja2 import Template

#Выгрузка логов из DB
req_log_db_sql = f"""
SELECT 
	event_time,
	command_tag,
	schema_name,
	table_name
FROM TECH_SCHEMA.DDL_LOG DL 
WHERE event_time >= (SELECT DTTM_RECORD dttm_record 
					 FROM integration.confluen_docs_log
					 WHERE LOG_PRC_STATUS = 'START'
					 ORDER BY DTTM_RECORD DESC
					 LIMIT 1 OFFSET 1
					 )
"""



#Выгрузка метаданных таблиц
req_mtd_tbl_sql = Template("""
WITH inxs_list AS (
	SELECT indexname,
	        split_part(inx, ',', 1) col_name
	FROM (SELECT indexname, 
	             regexp_split_to_table(indexs, 's+') inx
	      FROM (SELECT indexname,
	                   substring(INDEXDEF FROM POSITION('(' in INDEXDEF)+1 FOR POSITION('(' in reverse(INDEXDEF))-2) indexs
	            FROM pg_indexes
	            WHERE SCHEMANAME = '{{ schema }}' AND TABLENAME = '{{ table_name }}')) 
),
PK_list AS (
	SELECT cols.column_name, 
	        CASE WHEN tc.constraint_type = 'PRIMARY KEY' THEN 'YES' ELSE 'NO' END AS is_primary_key
	FROM information_schema.COLUMNS cols JOIN information_schema.key_column_usage kcu ON cols.table_schema = kcu.table_schema AND cols.table_name = kcu.table_name AND cols.column_name = kcu.column_name
	                                     JOIN information_schema.table_constraints tc ON kcu.table_schema = tc.table_schema AND kcu.table_name = tc.table_name AND kcu.constraint_name = tc.constraint_name AND tc.constraint_type = 'PRIMARY KEY'
	WHERE cols.table_schema = '{{ schema }}'
	      AND cols.table_name = '{{ table_name }}'
),
FK_list AS (
	SELECT cols.column_name, 
	        CASE WHEN tc.constraint_type = 'FOREIGN KEY' THEN 'YES' ELSE 'NO' END AS is_foreign_key
	FROM information_schema.COLUMNS cols JOIN information_schema.key_column_usage kcu ON cols.table_schema = kcu.table_schema AND cols.table_name = kcu.table_name AND cols.column_name = kcu.column_name
	                                     JOIN information_schema.table_constraints tc ON kcu.table_schema = tc.table_schema AND kcu.table_name = tc.table_name AND kcu.constraint_name = tc.constraint_name AND tc.constraint_type = 'FOREIGN KEY'
	WHERE cols.table_schema = '{{ schema }}'
	      AND cols.table_name = '{{ table_name }}'
)
SELECT 
    cols.column_name name,
    cols.data_type type,
    case when cols.character_maximum_length is null then '' else cols.character_maximum_length::text end COMMENT,
    CASE WHEN cols.is_nullable = 'YES' THEN 'Y' ELSE 'N' END nullable,
    COALESCE(cols.column_default, '') default,
    COALESCE(pg_catalog.col_description(c.oid, cols.ordinal_position::int), '') description,
    COALESCE((SELECT 'PK' FROM PK_list pl WHERE pl.column_name = cols.column_name), null) pk,
    COALESCE((SELECT 'FK' FROM FK_list fl WHERE fl.column_name = cols.column_name), null) fk,
    (SELECT indexname FROM inxs_list il WHERE cols.column_name = il.col_name) index_name
FROM information_schema.columns cols join pg_catalog.pg_class c ON c.relname = cols.table_name
                                     JOIN pg_catalog.pg_namespace n ON n.oid = c.relnamespace AND n.nspname = cols.table_schema                     
WHERE cols.table_schema = '{{ schema }}'
      AND cols.table_name = '{{ table_name }}'
ORDER BY ordinal_position
"""
                           )


req_max_log_id = f"""
select coalesce(max(log_hist_id), 1) from integration.confluen_docs_log
"""



#Запись лога START
ins_log_db_sql_st = Template("""
insert into integration.confluen_docs_log(log_hist_id, log_prc_status) values({{ id }}, 'START')
"""
                     )
#Запись лога END
ins_log_db_sql_ed = Template("""
insert into integration.confluen_docs_log(log_hist_id, log_prc_status) values({{ id }}, 'END')
"""
                             )
#Запись лога ошибки
ins_log_db_sql_er = Template("""
insert into integration.confluen_docs_log(log_hist_id, log_prc_status, log_prc_msg) values({{ id }}, 'ERROR', '{{ msg }}')
"""
                             )



#Запись лога DONE
ins_log_db_sql_dn = Template("""
insert into integration.confluen_docs_log_oper(log_hist_id, log_status, schema_name) values({{ log_hist_id }}, 'DONE', '{{ schema_name }}')
"""
                              )
#Запись лога ERROR
ins_log_db_sql_err = Template("""
insert into integration.confluen_docs_log_oper(log_hist_id, log_status, schema_name, tbl_name, msg_log) values({{ log_hist_id }}, 'ERROR', '{{ schema_name }}', '{{ tbl_name }}', '{{ msg_log }}')
"""
                              )