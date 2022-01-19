import re
import os
import csv
import requests
from bs4 import BeautifulSoup
import math

# os.system("clear")
alba_url = "http://www.alba.co.kr"
alba_request = requests.get(alba_url)
alba_soup = BeautifulSoup(alba_request.text, "html.parser")

SuperBrand = alba_soup.find('div', {"id": "MainSuperBrand"})
alba_box = SuperBrand.find("ul", {"class": "goodsBox"})
all_jobs = alba_box.find_all("li", {"class": "impact"})

company_lists = []
link_lists = []

for job in all_jobs:
    job_info = job.find("a", {"class": "goodsBox-info"})
    company = job_info.find("span", {"class": "company"}).text
    company_lists.append(company.replace("/", " "))

    link = job_info.attrs['href']
    link_lists.append(link)


def get_last_page(link):
    link_request = requests.get(link)
    link_soup = BeautifulSoup(link_request.text, "html.parser")
    how_many = link_soup.find("div", {"id": "NormalInfo"}).find(
        "p", {"class": "jobCount"})
    if how_many:
        how_many = how_many.text
    else:
        how_many = link_soup.find("div", {"id": "NormalInfo"}).find(
            "p", {"class": "listCount"})
        if how_many:
            how_many = how_many.text
        else:
            return 0
    jobs_numbers = re.sub(r'[^0-9]', '', how_many)
    jobs_numbers = int(jobs_numbers)
    last_page = jobs_numbers/50
    return math.ceil(last_page)


for company, link in zip(company_lists, link_lists):
    if get_last_page(link) != 0:
        places = []
        titles = []
        times = []
        pay_types = []
        pay_amounts = []
        dates = []
        for i in range(0, get_last_page(link)):
            link = link+f"?page={i+1}"
            link_request = requests.get(link)
            link_soup = BeautifulSoup(link_request.text, "html.parser")

            places_lists = link_soup.find("div", {"id": "NormalInfo"}).find(
                "tbody").find_all("td", {"class": "local first"})
            #places = []
            for places_list in places_lists:
                place = places_list.get_text()
                places.append(place.replace('\xa0', ''))

            title_lists = link_soup.find("div", {"id": "NormalInfo"}).find(
                "tbody").find_all("td", {"class": "title"})
            #titles = []
            for title_list in title_lists:
                title = title_list.find(
                    "span", {"class": "company"}).get_text()
                titles.append(title)

            time_lists = link_soup.find("div", {"id": "NormalInfo"}).find(
                "tbody").find_all("td", {"class": "data"})
            #times = []
            for time_list in time_lists:
                if time_list.find("span", {"class": "time"}):
                    time = time_list.find("span", {"class": "time"}).get_text()
                else:
                    time = time_list.find(
                        "span", {"class": "consult"}).get_text()
                    times.append(time)

            pay_type_lists = link_soup.find("div", {"id": "NormalInfo"}).find(
                "tbody").find_all("td", {"class": "pay"})
            #pay_types = []
            for pay_type_list in pay_type_lists:
                pay_type = pay_type_list.find(
                    "span", {"class": "payIcon"}).get_text()
                pay_types.append(pay_type)

            pay_amount_lists = link_soup.find("div", {"id": "NormalInfo"}).find(
                "tbody").find_all("td", {"class": "pay"})
            #pay_amounts = []
            for pay_amount_list in pay_amount_lists:
                pay_amount = pay_amount_list.find(
                    "span", {"class": "number"}).get_text()
                pay_amounts.append(pay_amount)

            date_lists = link_soup.find("div", {"id": "NormalInfo"}).find(
                "tbody").find_all("td", {"class": "regDate last"})
            #dates = []
            for date_list in date_lists:
                date = date_list.get_text()
                dates.append(date)

        file = open(company, mode="w")
        writer = csv.writer(file)
        writer.writerow(["place", "title", "time",
                        "pay_type", "pay_amount", "date"])
        for place, title, time, pay_type, pay_amount, date in zip(places, titles, times, pay_types, pay_amounts, dates):
            writer.writerow([place, title, time, pay_type, pay_amount, date])
    else:
        continue
