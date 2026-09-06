import psycopg2
import os

from dotenv import load_dotenv
load_dotenv()

def db_connect_session():
    pg_coon = {
    'host': os.getenv("DB_HOST"),
    'database': os.getenv("DB_NAME"),
    'user': os.getenv("DB_USER"),
    'password': os.getenv("DB_PASSWORD")
    }
    conn = psycopg2.connect(**pg_coon)
    return conn