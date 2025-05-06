import psycopg2
from psycopg2 import sql

DATABASE = "postgresql://username:password@localhost:5432/readmedatabase"

def init_db():
    try:
        conn = psycopg2.connect(DATABASE)
        cur = conn.cursor()

    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        if 'conn' in locals():
            conn.close()