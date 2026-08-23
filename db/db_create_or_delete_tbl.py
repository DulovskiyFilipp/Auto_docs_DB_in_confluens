import psycopg2
import random
import string


pg_params = {
    'host': 'localhost',
    'database': 'postgres',
    'user': 'postgres',
    'password': '12345'
}

#----------------------------------Создание нужного числа таблиц в БД
def create_tbl(num: int, shema: str):
    for _ in range(num):
        conn = psycopg2.connect(**pg_params)
        cursor = conn.cursor()
        length = 10
        letters_and_digits = string.ascii_letters
        random_string = "".join(random.choices(letters_and_digits, k=length))

        cursor.execute(f"""
                create table {shema}.{random_string} (
                id SERIAL PRIMARY KEY,
                name VARCHAR(255) NOT NULL,
                age INTEGER NOT NULL,
                gender VARCHAR(255) NOT NULL,
                email VARCHAR(255) NOT NULL
                );
            """)
        cursor.connection.commit()



#-----------------------------------Удаление таблиц из БД
def drop_tbl(shema: str):
    conn = psycopg2.connect(**pg_params)
    cursor = conn.cursor()
    cursor.execute(f"""
            SELECT table_name
            FROM information_schema.tables
            WHERE table_schema = '{shema}'
              AND table_type = 'BASE TABLE'
            ORDER BY table_name;
        """)
    tables = cursor.fetchall()
    for i in tables:
        cursor.execute(f"""
        drop table if exists {i[0]};
        """)
    cursor.connection.commit()

#----------------------------------- Вызовы
def one_or_null(one_or_null: int, shema: str, cnt: int):
    if one_or_null == 0:
        create_tbl(cnt, shema)
    else:
        drop_tbl(shema)

one_or_null(0, 'public', 20)