import psycopg2
import psycopg2.pool
from dotenv import load_dotenv
import os
from sqlalchemy_utils import database_exists
from sqlalchemy import create_engine

def get_connection():
    try:
        load_dotenv() 
        print("Connecting to PostgreSQL database...")

        conn = psycopg2.connect(host = os.environ.get("DB_HOST"),
                                database = os.environ.get("DB_NAME"),
                                user = os.environ.get("DB_USER"),
                                password = os.environ.get("DB_PASSWORD"))
        print(f"Successfully connected")
        return conn
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)

def get_engine():
    user = os.environ.get("DB_USER")
    password = os.environ.get("DB_PASSWORD")
    host = os.environ.get("DB_HOST")
    database = os.environ.get("DB_NAME")
    url = f'postgresql+psycopg2://{user}:{password}@{host}:5432/{database}'
    if not database_exists(url):
        print("bruh")
    else:
        print("yippee")
    engine = create_engine(url)
    return engine

def main():
    conn = get_connection()
    conn.close()

main()