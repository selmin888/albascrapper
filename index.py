import os
import csv
import requests
from bs4 import BeautifulSoup

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
    company_lists.append(company)

    link = job_info.attrs['href']
    link_lists.append(link)

# print(company_lists)
# print(link_lists)
'''
site = all_jobs[0].find("a", {"class": "goodsBox-info"})
link = site.attrs['href']
print(link)
'''

for link in link_lists:
    link_request = requests.get(link)
    link_soup = BeautifulSoup(link_request.text, "html.parser")
