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

            # if counter == 30:
            #     break
            # counter += 1
            df.loc[i, 'First_Picture_URL'] = img_src.strip()
        except:
            # if counter == 30:
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


def main():
    male_idol_csv = "data\male_idols.csv"
    output_path = "data\male_idols_with_pics.csv"
    # print(scrape_idol_image("Euijeong", "KELT9b"))
#     scrape_images_to_csv(male_idol_csv, output_path)

# main()