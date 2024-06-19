import psycopg2
import psycopg2.pool
from dotenv import load_dotenv
import os
import csv

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


def upload_idols_to_db(input_file, type):
    conn = get_connection()
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

def main():
    # female_input_path = "data\\female_idol_filenames.csv"
    male_input_path = "data\male_idol_filenames.csv"
    yuh = "Male"
    # upload_idols_to_db(male_input_path, yuh)

# main()