import requests
from idol_scraper import BeautifulSoup
from time import sleep
import csv
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from dotenv import load_dotenv

def scrape(url):
    options = webdriver.ChromeOptions()
    options.add_argument("--ignore-certificate-error")
    options.add_argument("--ignore-ssl-errors")
    options.add_experimental_option("detach", True)

    driver = webdriver.Chrome(options=options)
    driver.get(url)

    for i in range(3):
        dropdown_button = WebDriverWait(driver, 30).until(EC.element_to_be_clickable((By.XPATH, '/html/body/div[1]/div[1]/div/div[1]/main/article/div[2]/div[2]/div/div[7]/a[3]')))
        dropdown_button.click()
        print("clicked button")

        driver.implicitly_wait(20)


def main():
    url = "https://dbkpop.com/db/male-k-pop-idols/"
    scrape(url)
    
main()