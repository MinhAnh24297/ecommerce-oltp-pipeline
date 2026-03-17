import psycopg2
from config import load_config

def connect(config):
    try:
        with psycopg2.connect(**config) as conn:
            print('Connected to the PostgreSQL server.')
            return conn
    except (psycopg2.DatabaseError, Exception) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()
            print("Connection closed.")

if __name__ == '__main__':
    config = load_config()
    connect(config)