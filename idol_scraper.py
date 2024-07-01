import requests
from bs4 import BeautifulSoup
import csv
import random
from dotenv import load_dotenv
import urllib.request 
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import pandas as pd
import boto3
import os
from urllib.parse import quote
import mimetypes
load_dotenv()

# Scrapes all idols from kdb.com
def scrape(link, save_path):
    page = requests.get(link)
    soup = BeautifulSoup(page.content, "html.parser")

    table = soup.find("table", id="table_1")
    tbody = table.find("tbody")
    all_rows = tbody.find_all("tr")
    print(len(all_rows))

    for row in all_rows:
        all_td = row.find_all("td")

        stage_name = all_td[1].text
        full_name = all_td[2].text
        korean_name = all_td[3].text
        group = all_td[6].text
        country = all_td[7].text
        print(f"Stage Name: {stage_name}")
        print(f"Name: {full_name}")
        print(f"Korean Name: {korean_name}")
        print(f"Group: {group}")
        print(f"Country: {country}")
        print()

        with open(save_path, mode='a', newline='', encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow([stage_name, full_name, korean_name, group, country])

# Method to loop through input file, scrape picture, and save to new output file
def scrape_images_to_csv(input_path, output_path):
    options = webdriver.ChromeOptions()
    options.add_argument("--ignore-certificate-error")
    options.add_argument("--ignore-ssl-errors")
    options.add_argument("--headless=new")
    options.add_experimental_option("detach", True)
    driver = webdriver.Chrome(options=options)

    df = pd.read_csv(input_path)
    counter = 0
    for i in df.index:
        stage_name = df.iloc[i][0]
        group = df.iloc[i][3]
        if (not isinstance(group, str)):
            group = ""

        if group == "":
            search_term = stage_name + " K-Pop"
        else:
            search_term = stage_name + " " + group
            search_term = search_term.strip()

        try:
            # Encode the search term to URL-friendly format
            encoded_term = urllib.parse.quote_plus(search_term) 
            search_url = f"https://www.google.com/search?q={encoded_term}&tbm=isch"
            driver.get(search_url)

            thumbnails = driver.find_elements(By.CLASS_NAME, "Q4LuWd")
            img_src = ""
            for image in thumbnails:
                image.click()
                time.sleep(6)
                                                            
                needed_image = driver.find_element(By.XPATH, "/html/body/div[2]/c-wiz/div[3]/div[2]/div[3]/div[2]/div[2]/div[2]/div[2]/c-wiz/div/div/div/div/div[3]/div[1]/a/img[1]")
                # time.sleep(3)
                img_src = needed_image.get_attribute('src')
                if img_src.startswith('data:'):
                    print('Found encrypted image, skipping')
                    continue
                elif img_src.startswith('http'):
                    break

            # if counter == 3:
            # if counter == 3:
            #     break
            # counter += 1
            df.loc[i, 'First_Picture_URL'] = img_src.strip()
        except:
            # if counter == 3:
            # if counter == 3:
            #     break
            # counter += 1
            df.loc[i, 'First_Picture_URL'] = ""

    driver.close()
    df.to_csv(output_path, index=False)

# Method to scrape a picture and give it directly to the bot (temporary)
def scrape_idol_image(idol_name, group):
    try:
        options = webdriver.ChromeOptions()
        options.add_argument("--ignore-certificate-error")
        options.add_argument("--ignore-ssl-errors")
        options.add_argument("--headless=new")
        options.add_experimental_option("detach", True)
        driver = webdriver.Chrome(options=options)
        
        if group == "":
            search_term = idol_name + " K-Pop"
        else:
            search_term = idol_name + " " + group
            search_term = search_term.strip()

        # Encode the search term to URL-friendly format
        encoded_term = urllib.parse.quote_plus(search_term) 
        search_url = f"https://www.google.com/search?q={encoded_term}&tbm=isch"
        driver.get(search_url)

        thumbnails = driver.find_elements(By.CLASS_NAME, "Q4LuWd")
        img_src = ""
        # loop through all thumbnails until we get a valid photo URL
        for image in thumbnails:
            image.click()
            time.sleep(5)
                                                        
            needed_image = driver.find_element(By.XPATH, "/html/body/div[2]/c-wiz/div[3]/div[2]/div[3]/div[2]/div[2]/div[2]/div[2]/c-wiz/div/div/div/div/div[3]/div[1]/a/img[1]")
            # time.sleep(3)
            img_src = needed_image.get_attribute('src')
            if img_src.startswith('data:'):
                print('Found encrypted image, skipping')
                continue
            elif img_src.startswith('http'):
                break

        # first_image = thumbnails[0]
        # first_image.click()
        # time.sleep(3)
                                                     
        # needed_image = driver.find_element(By.XPATH, "/html/body/div[2]/c-wiz/div[3]/div[2]/div[3]/div[2]/div[2]/div[2]/div[2]/c-wiz/div/div/div/div/div[3]/div[1]/a/img[1]")
        # img_src = needed_image.get_attribute('src')

        driver.close()
        return img_src
    except Exception as error:
        return "Unable to return picture"

# Method to download idol images and upload them to S3 bucket
def upload_to_s3(input_csv, output_csv):
    aws_access_key_id = os.environ.get("IAM_ACCESS_KEY")
    aws_secret_access_key = os.environ.get("IAM_SECRET_ACCESS_KEY")
    aws_region = 'us-west-1'  

    s3 = boto3.client('s3', aws_access_key_id=aws_access_key_id, aws_secret_access_key=aws_secret_access_key, region_name=aws_region)

# --- LOOPING THRU CSV FILE ---
    df = pd.read_csv(input_csv)
    df = df.fillna('')
    for i in df.index:
        if i < 400:
            continue

        if i == 800:
            print(f"\nSTOPPED AT LINE {i + 1}")
            stage_name = df.iloc[i]['Stage_Name']
            full_name = df.iloc[i]['Full_Name']
            print(f"For next run start with: {full_name} ({stage_name})")
            break

        stage_name = df.iloc[i]['Stage_Name'] if df.iloc[i]['Stage_Name'] else ""
        full_name = df.iloc[i]['Full_Name'] if df.iloc[i]['Full_Name'] else ""
        korean_name = df.iloc[i]['Korean_Name'] if df.iloc[i]['Korean_Name'] else ""
        group = df.iloc[i]['Group'] if df.iloc[i]['Group'] else ""
        country = df.iloc[i]['Country'] if df.iloc[i]['Country'] else ""
        pic_url = df.iloc[i]['First_Picture_URL']
        print(f"Stage Name: {stage_name} | Full Name: {full_name}")
        print(f"URL: {pic_url}")

        temp_stage_name = stage_name.replace(" ", "")
        temp_full_name = full_name.replace(" ", "") if full_name else ""
        # filename = "male_idols/" + temp_stage_name + '_' + temp_full_name
        filename = "male_idolsV2/" + temp_stage_name + '_' + temp_full_name

        if ".png" in pic_url:
            filename += ".png"
        elif ".jpeg" in pic_url:
            filename += ".jpeg"
        elif ".jpg" in pic_url:
            filename += ".jpeg"
        elif ".webp" in pic_url:
            filename += ".webp"
        else:
            filename += ".jpeg"
        print(f"File save name: {filename}")

       # get correct MIME type
        content_type, _ = mimetypes.guess_type(filename)
        if not content_type:
            content_type = 'binary/octet-stream'

    # ---- USING PUT_OBJECT ----
        try: 
            headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'}
            image = requests.get(pic_url, headers=headers)
            if image.status_code == 200:
                # s3.put_object(Bucket='bias-bot-images', Key=filename, Body=image.content)
                s3.put_object(Bucket='bias-bot-images', Key=filename, Body=image.content, ContentType=content_type)     # setting content type to not binary/octet-stream
                print(f"Uploaded {filename} to S3 bucket")
                with open(output_csv, mode='a', newline='', encoding="utf-8") as f:
                    writer = csv.writer(f)
                    writer.writerow([stage_name, full_name, korean_name, group, country, filename])
            else:
                print(f"Error uploading {filename} to S3 bucket | Status code: {image.status_code}")
                with open(output_csv, mode='a', newline='', encoding="utf-8") as f:
                    writer = csv.writer(f)
                    writer.writerow([stage_name, full_name, korean_name, group, country, "ERROR"])
        except Exception as e:
            print(f"Error uploading {filename} to S3 bucket | Exception: {e}")
            with open(output_csv, mode='a', newline='', encoding="utf-8") as f:
                writer = csv.writer(f)
                writer.writerow([stage_name, full_name, korean_name, group, country, "ERROR"])
        print()

    # ---- USING PUT_OBJECT ----
    # image = requests.get("https://upload.wikimedia.org/wikipedia/commons/0/04/Kwon_Yu-ri_at_Incheon_Airport_on_August_5%2C_2023.jpg")
    # try: 
    #     s3.put_object(Bucket='bias-bot-images', Key=f'female_idols/TEST.jpg', Body=image.content)
    #     print(f"Uploaded test pic to S3 bucket")
    # except:
    #     print(f"Error uploading test pic to S3 bucket")
    # print()

# --- UPLOADING LOCAL PICTURE TO AMAZON S3 BUCKET ----
    # s3 = boto3.client('s3', aws_access_key_id=aws_access_key_id, aws_secret_access_key=aws_secret_access_key, region_name=aws_region)

    # s3.upload_file(
    #     Filename='test_kwon.jpg',
    #     Bucket='bias-bot-images',
    #     Key='female_idols/test_kwon.jpg'
    # )

def download_images(input_csv):
    df = pd.read_csv(input_csv)
    counter = 0
    for i in df.index:
        if counter == 10:
            break

        stage_name = df.iloc[i]['Stage_Name']
        full_name = df.iloc[i]['Full_Name']
        pic_url = df.iloc[i]['First_Picture_URL']

        temp = full_name.replace(" ", "")
        filename = stage_name + '_' + temp

        if ".png" in pic_url:
            filename += ".png"
        elif ".jpeg" in pic_url:
            filename += ".jpeg"
        elif ".jpg" in pic_url:
            filename += ".jpg"
        elif ".webp" in pic_url:
            filename += ".webp"
        else:
            filename += ".jpeg"
        
        try:
            headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'}

            image = requests.get(pic_url, headers=headers)
            if image.status_code == 200:
                with open(f"images/female_idols/{filename}", "wb") as f:
                    f.write(image.content)
                print(f"Downloaded {filename}")
            else:
                print(f"Failed to download {filename} | Status code: {image.status_code}")
        except Exception as e:
            print(f"ERROR: unable to download {filename}: {e}")
        counter += 1


def main():
    # male_idol_csv = "data\male_idols.csv"
    # output_path = "data\male_idols_with_pics.csv"
    # female_idol_csv = "data\\female_idols.csv"
    # output_path = "data\\female_idols_with_pics.csv"
    # scrape_images_to_csv(female_idol_csv, output_path)

# --- Saving images to s3 --- #
    input_csv = "data\male_idols_with_pics.csv"
    output_csv = "data\male_idol_filenamesV2.csv"
    upload_to_s3(input_csv, output_csv)

# --- Downloading images to local storage --- #
    # input_csv = "data\\female_idols_with_pics.csv"
    # download_images(input_csv)


# --- Check if IAM user is working --- #
    # aws_access_key_id = os.environ.get("IAM_ACCESS_KEY")
    # aws_secret_access_key = os.environ.get("IAM_SECRET_ACCESS_KEY")
    # aws_region = 'us-west-1'  
    # session = boto3.Session(
    #     aws_access_key_id=aws_access_key_id,
    #     aws_secret_access_key=aws_secret_access_key,
    #     region_name=aws_region
    # )

    # s3 = session.client('s3')
    # try:
    #     response = s3.list_buckets()
    #     print('Connected to Amazon S3 successfully!')
    #     print('List of buckets:')
    #     for bucket in response['Buckets']:
    #         print(f'  {bucket["Name"]}')
    # except Exception as e:
    #     print(f'Failed to connect to Amazon S3: {str(e)}')

# main()