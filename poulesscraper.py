from selenium import webdriver
from bs4 import BeautifulSoup
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from webdriver_manager.chrome import ChromeDriverManager
import os

chrome_options = webdriver.ChromeOptions()
chrome_options.binary_location = os.environ.get("GOOGLE_CHROME_BIN")
chrome_options.add_argument('--headless')
chrome_options.add_argument('--no-sandbox')
chrome_options.add_argument('--disable-dev-shm-usage')
wd = webdriver.Chrome(executable_path=os.environ.get("CHROMEDRIVER_PATH"), chrome_options=chrome_options)

url = "https://www.flashscore.com/tennis/atp-singles/french-open-2020/results/"
wd.get(url)
table = WebDriverWait(wd, 5).until(EC.presence_of_element_located((By.ID, 'live-table')))
soup = BeautifulSoup(table.get_attribute('innerHTML'), 'lxml')

def createFormat(date, time, identifier):
  print('    {\n        "isMatch": true,\n        "start": {"day": "')
  print(date)
  print('", "time": "')
  print(time)
  print('"},\n')
  print('        "identifier": "')
  print(identifier)
  print('",\n')

def scrape(it):
  iterations = it
  for tag in soup.find_all('div', class_=lambda x: x and x.startswith('event__match event__match--static event__match--twoLine')):
    iterations += 1
    identifier = tag['id']
    start = tag.find('div', class_= 'event__time')
    start = str(start)
    start = start.replace('<div class="event__time">', '')
    start = start.replace('</div>', '')
    date = start[:6]
    time = start[7:]
    time = time.replace('<div class="event__stage"><div class="event__stage--block">WO','')
    date = date[0:2] + "-" + date [3:5]
    if (iterations == len(soup.find_all('div', class_=lambda x: x and x.startswith('event__match event__match--static event__match--twoLine')))):
      createFormat(date, time, identifier)
    else:
      createFormat(date, time, identifier)
  return iterations

its = scrape(0)