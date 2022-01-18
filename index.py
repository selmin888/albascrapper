import os
import csv
import requests
from bs4 import BeautifulSoup

# os.system("clear")
alba_url = "http://www.alba.co.kr"
alba_request = requests.get(alba_url)
alba_soup = BeautifulSoup(alba_request.text, "html.parser")

print(alba_soup)
