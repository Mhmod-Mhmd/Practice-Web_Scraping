import requests
from bs4 import BeautifulSoup
import csv
import pandas as pd
from datetime import datetime


date = input("Enter specific date in the following format mm/dd/yyyy: ")
try:
    if str(date).format == format("mm/dd/yyyy"):
        pass
except:
    print('enter the detemined date')

page = requests.get(f"https://www.yallakora.com/match-center/%D9%85%D8%B1%D9%83%D8%B2-%D8%A7%D9%84%D9%85%D8%A8%D8%A7%D8%B1%D9%8A%D8%A7%D8%AA?date={date}#")


def main(page):

    src = page.content
    soup = BeautifulSoup(src, "lxml")
    matches_details = []
    compitations = soup.find_all("div", {'class' : 'matchCard'})
    
    def get_match_info(compitations):
        comp_title = compitations.contents[1].find("h2").text.strip()
        match_info = compitations.contents[3].find_all("li")

        for i in range(len(match_info)):
            # extract teams details
            teamA = match_info[i].find("div", {'class':'teamA'}).text.strip()
            teamB = match_info[i].find("div", {'class':'teamB'}).text.strip()

            # extract match results
            result = match_info[i].find("div", {'class':'MResult'})
            score1 = result.find('span', {'class':'score'}).text.strip() 
            score2 = result.find('span', {'class':'score'}).text.strip()

            M_time = result.find('span', {'class': 'time'}).text.strip()


            matches_details.append({"نوع البطوله": comp_title, "الفريق الاول": teamA, "الفريق الثاني":teamB,
                                     "النتيجة" : f"{score1} - {score2}", "الوقت": M_time})

    for i in range(len(compitations)):
        get_match_info(compitations[i])



    # load data to excel file
    file_path = "C:\\Users\\mahmo\\Desktop\\Web Scraping\\Excel_data.xlsx"
    df = pd.DataFrame(matches_details)
    df.to_excel(file_path, index=False)
    print("done!")

    # load data to csv file
    
    keys_values = matches_details[0].keys()
    
    with open('C:\\Users\\mahmo\\Desktop\\Web Scraping\\CSV_data.csv', 'w', newline='',encoding='utf-8') as file:
        match_write = csv.DictWriter(file,  fieldnames=keys_values)
        match_write.writeheader()
        match_write.writerows(matches_details)
        print("done!")
    
main(page)