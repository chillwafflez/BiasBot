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

def scrape_image(input_path, output_path):
    options = webdriver.ChromeOptions()
    options.add_argument("--ignore-certificate-error")
    options.add_argument("--ignore-ssl-errors")
    options.add_experimental_option("detach", True)
    driver = webdriver.Chrome(options=options)

    with open (input_path, 'r', encoding="utf-8") as csvfile:
       reader = csv.reader(csvfile, delimiter=',')
       next(reader)     # skip first row which are just column headers
       counter = 0
       for row in reader: # loop over the rows
            idol = row[0]
            group = row[3]
            print(f"{idol} | {group}")

            search_term = idol + " " + group
            # Encode the search term to URL-friendly format
            encoded_term = urllib.parse.quote_plus(search_term) 
            search_url = f"https://www.google.com/search?q={encoded_term}&tbm=isch"
            driver.get(search_url)

            thumbnails = driver.find_elements(By.CLASS_NAME, "Q4LuWd")
            first_image = thumbnails[0]
            first_image.click()
            time.sleep(3)

            needed_image = driver.find_element(By.XPATH, "/html/body/div[2]/c-wiz/div[3]/div[2]/div[3]/div[2]/div[2]/div[2]/div[2]/c-wiz/div/div/div/div/div[3]/div[1]/a/img[1]")
            time.sleep(3)
            # needed_image.click()
            img_src = needed_image.get_attribute('src')
            print(img_src)

            if counter == 10:
                break
            counter += 1
    
    # search_term = idol + group
    # # Encode the search term to URL-friendly format
    # encoded_term = urllib.parse.quote_plus(search_term) 
    # search_url = f"https://www.google.com/search?q={encoded_term}&tbm=isch"
    # driver.get(search_url)

    # thumbnails = driver.find_elements(By.CLASS_NAME, "Q4LuWd")
    # first_image = thumbnails[0]
    # first_image.click()
    # time.sleep(3)

    # needed_image = driver.find_element(By.XPATH, "/html/body/div[2]/c-wiz/div[3]/div[2]/div[3]/div[2]/div[2]/div[2]/div[2]/c-wiz/div/div/div/div/div[3]/div[1]/a/img[1]")
    # time.sleep(3)
    # needed_image.click()
    # img_src = needed_image.get_attribute('src')
    # print(img_src)
      


def main():
    # link = "https://dbkpop.com/db/female-k-pop-idols/"
    # path = "data\\female_idols.csv"
    # scrape(link, path)
    # scrape_image()

    male_idol_csv = "data\male_idols.csv"
    scrape_image(male_idol_csv, "penis")

main()
