import psycopg2

def get_table_metadata(conn_params):
    """
    Подключается к PostgreSQL и возвращает метаданные всех таблиц.
    """
    conn = psycopg2.connect(**conn_params)
    cursor = conn.cursor()

    # 1. Получаем список всех таблиц в схеме public
    cursor.execute("""
        SELECT table_name 
        FROM information_schema.tables 
        WHERE table_schema = 'public' 
          AND table_type = 'BASE TABLE'
        ORDER BY table_name;
    """)
    tables = cursor.fetchall()

    metadata = {}
    for (table_name,) in tables:
        # 2. Для каждой таблицы получаем информацию о колонках
        cursor.execute("""
            SELECT 
                column_name name, 
                data_type type, 
                is_nullable nullable,
                character_maximum_length comment
            FROM information_schema.columns
            WHERE table_schema = 'public' 
              AND table_name = %s
            ORDER BY ordinal_position;
        """, (table_name,))
        columns = cursor.fetchall()
        metadata[table_name] = columns

    cursor.close()
    conn.close()
    return metadata