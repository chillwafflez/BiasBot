import psycopg2
import psycopg2.pool
from dotenv import load_dotenv
import os
import csv
from sqlalchemy_utils import database_exists
from sqlalchemy import create_engine
from sqlalchemy import MetaData
from sqlalchemy.orm import Session

def get_connection_psycop():
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


def upload_idols_to_db(input_file, type):
    conn = get_connection_psycop()
    with open(input_file, 'r', encoding="utf-8") as f:
        headers = next(f) # skip column names
        counter = 0
        rows = csv.reader(f)
        for row in rows:
            if counter == 3:
                break
            stage_name = row[0].strip().replace("'", "''")
            full_name = row[1].strip().replace("'", "''")
            korean_name = row[2].strip().replace("'", "''")
            group = row[3].strip().replace("'", "''")
            country = row[4].strip().replace("'", "''")
            url = row[5].strip().replace("'", "''")
            # print(f"Stage Name: {stage_name} | Full Name: {full_name} | Korean Name: {korean_name} | Gender: {type}")
            # print(f"Group: {group} | Country: {country} | URL: {url}\n")
            try:
                sql = f"INSERT INTO idol(stage_name, full_name, korean_name, idol_group, country, gender) VALUES ('{stage_name}', '{full_name}', '{korean_name}', '{group}', '{country}', '{type}') RETURNING id;"
                cursor = conn.cursor()
                cursor.execute(sql)
                conn.commit()

                idol_id = cursor.fetchone()[0]
                sql = f"INSERT INTO idol_picture(idol_id, url) VALUES ('{idol_id}', '{url}')"
                cursor.execute(sql)
                conn.commit()
            except Exception as e: 
                print(f"ERROR: couldn't upload idol info or picture for {stage_name} ({full_name})")
                print(e)

                counter += 1
    conn.close()
    cursor.close()

def get_engine():
    host = os.environ.get("DB_HOST")
    db_name = os.environ.get("DB_NAME")
    user = os.environ.get("DB_USER")
    password = os.environ.get("DB_PASSWORD")
    url = f'postgresql+psycopg2://{user}:{password}@{host}:5432/{db_name}'
    if database_exists(url):
        print("connected to db!")
    else:
        print("couldn't connect")

    engine = create_engine(url)
    return engine

def main():
    # female_input_path = "data\\female_idol_filenames.csv"
    male_input_path = "data\male_idol_filenames.csv"
    yuh = "Male"
    engine = get_engine()
    engine.dispose()
# main()

engine = get_engine()
metadata = MetaData()
metadata.reflect(engine)
session = Session(bind=engine)