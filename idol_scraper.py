import requests
from bs4 import BeautifulSoup
from time import sleep
import csv
import random
from dotenv import load_dotenv


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

def main():
    link = "https://dbkpop.com/db/female-k-pop-idols/"
    path = "data\\female_idols.csv"
    scrape(link, path)

main()
