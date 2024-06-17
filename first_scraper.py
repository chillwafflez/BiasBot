import requests
from idol_scraper import BeautifulSoup
from time import sleep
import csv
import random
from dotenv import load_dotenv


def scrape_group(link, save_path, group):
    page = requests.get(link)
    soup = BeautifulSoup(page.content, "html.parser")

    main_column = soup.find("div", class_="col-lg-10 col-md-10 col-sm-10")
    p_tags = main_column.find_all("p")
    
    current_member_count = 0
    for p in p_tags:
        if (p.find("strong")):      # narrow down to all <strong> tags which have relevant informaton
            if ("Members Profile:" in p.find("strong").text):
                # Get the member in this current <p> tag
                strong_tags_after_profile_one = p.find_all("strong")
                second_strong_tag = ""
                if len(strong_tags_after_profile_one) > 1:
                    second_strong_tag = strong_tags_after_profile_one[1]
                else:
                    second_strong_tag = strong_tags_after_profile_one[0].split(":")[1].strip()
                first_member_name = second_strong_tag.text.strip()
                first_member_picture = p.find("img")['src'].strip()
                print(f"---- Member {current_member_count + 1} ----")
                print(f"Name: {first_member_name}")
                print(f"Picture URL: {first_member_picture}")
                current_member_count += 1
                print()

                # If there is a chance the name isnt in the first strong tag
                if ':' in first_member_name:
                    first_member_name = first_member_name.split(":")[1].strip()             # In case we get a "Good Hands:" situation
                    if first_member_name == "":                                             # if still naw, just get the name from 'Stage Name' span tag
                        all_spans = p.find_all("span")
                        for span in all_spans:
                            if "Stage" in span.text:
                                first_member_name = span.next_sibling.strip()
                                
                with open(save_path, mode='a', newline='', encoding="utf-8") as f:
                    writer = csv.writer(f)
                    writer.writerow([first_member_name, first_member_picture, group])
                continue
            elif ("Members Profile" in p.find("strong").text):
                continue
            elif p.find("img"):
                member_name = p.find("strong").text.strip()
                member_picture = p.find("img")['src'].strip()
                print(f"---- Member {current_member_count + 1} ----")
                print(f"Name: {member_name}")
                print(f"Picture URL: {member_picture}")
                current_member_count += 1
                print()

                # If there is a chance the name isnt in the first strong tag
                if ':' in member_name:
                    member_name = member_name.split(":")[1].strip()                 # In case we get a "Good Hands:" situation
                    if member_name == "":                                           # if still naw, just get the name from 'Stage Name' span tag
                        all_spans = p.find_all("span")
                        for span in all_spans:
                            if "Stage" in span.text:
                                member_name = span.next_sibling.strip()

                # If no picture
                if member_name == None:
                    member_name = "None"

                with open(save_path, mode='a', newline='', encoding="utf-8") as f:
                    writer = csv.writer(f)
                    writer.writerow([member_name, member_picture, group])
    
            
def scrape_group_types(link):
    page = requests.get(link)
    soup = BeautifulSoup(page.content, "html.parser")

    main_column = soup.find("div", class_="entry-content herald-entry-content")
    p_tags = main_column.find_all("p")

    for p in p_tags:
        if p.get('style'):
            continue
        else:
            all_links = p.find_all("a")
            for link in all_links:
                group_name = link.text.strip()
                group_link = link['href'].strip()
                print(f"Group: {group_name} | {group_link}")
                with open("./data/girl_groups.csv", mode='a', newline='', encoding='utf-8') as f:
                    writer = csv.writer(f)
                    writer.writerow([group_name, group_link])

def main():
    male_idols_path = "./data/male_idols.csv"
    boy_group_path = './data/boy_groups.csv'
    # link = "https://kprofiles.com/1-n-members-profile/"
    # link = "https://kprofiles.com/inphase-members-profile/" #no pics
    # scrape_group(link, male_idols_path, 'penis')


    with open (boy_group_path, 'r', encoding='utf-8') as csvfile:
        reader = csv.reader (csvfile, delimiter=',')
        next(reader)     # skip first row which are just column headers

        # counter = 0
        line_tracker = 2
        for row in reader:
            if line_tracker < 21:       #tracks where error took place
                line_tracker += 1
                continue


            print(f"Line: {line_tracker} | Group Name: {row[0]} | Link: {row[1]}")
            scrape_group(row[1], male_idols_path, row[0])
            # counter += 1
            line_tracker += 1
            sleep(random.randint(5,10))

# main()