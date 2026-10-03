import psycopg2.pool
import os
import contextlib

from dotenv import load_dotenv
load_dotenv()

try:
    connect_pul = psycopg2.pool.SimpleConnectionPool(
            minconn=1,
            maxconn=10,
            host=os.getenv("DB_HOST"),
            database=os.getenv("DB_NAME"),
            user=os.getenv("DB_USER"),
            password=os.getenv("DB_PASSWORD"),
            port="5432"
        )
except psycopg2.DatabaseError as e:
    print(f"Ошибка при создании пула соединений: {e}")
    connect_pul = None

@contextlib.contextmanager
def db_connect_session():
    if connect_pul is None:
        raise RuntimeError("Пул соединений не инициализирован")

    conn = connect_pul.getconn()
    try:
        yield conn
        conn.commit()
    except Exception as e:
        conn.rollback()
        print(f"Транзакция откачена из-за ошибки: {e}")
        raise e
    finally:
        connect_pul.putconn(conn)