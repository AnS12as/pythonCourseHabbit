import time
import psycopg2
import os

DB_NAME = os.getenv("DB_NAME")
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_HOST = os.getenv("DATABASE_HOST", "db")
DB_PORT = os.getenv("DATABASE_PORT", "5432")

TIMEOUT = 30  # Время ожидания

start_time = time.time()

while True:
    try:
        conn = psycopg2.connect(
            dbname=DB_NAME,
            user=DB_USER,
            password=DB_PASSWORD,
            host=DB_HOST,
            port=DB_PORT
        )
        conn.close()
        print("Database is ready")
        break
    except psycopg2.OperationalError as e:
        if time.time() - start_time > TIMEOUT:
            print("Timeout: Database connection failed")
            exit(1)
        print("Waiting for database...")
        time.sleep(1)
