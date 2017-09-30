import re

url = 'https://www.meetup.com/Dallas-Japanese-Language-Meetup/members/?sort=join_date&desc=1'
newUrl = 'https://www.meetup.com/Dallas-Japanese-Language-Meetup/members/?offset=100&sort=join_date&desc=1'
test = 'https://www.meetup.com/Dallas-Japanese-Language-Meetup/members/?offset={}&sort=join_date&desc=1'
urlSet = set()


import time
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from bs4 import BeautifulSoup
import lxml
import pandas as pd

driver = webdriver.Chrome()  # Optional argument, if not specified will search path.
driver.get('https://secure.meetup.com/login/');
time.sleep(1) # Let the user actually see something!

logUser = driver.find_element_by_name('email')
logUser.send_keys('wickhcp@gmail.com') # input personal User Name for meetup.com

logPassword = driver.find_element_by_name('password')
logPassword.send_keys('1pootiet' + Keys.RETURN)

## Note above two variables, change for person

time.sleep(1) # Pause, let user see something

# groups = {
# 'japanfans':
# 	'https://www.meetup.com/japanfans/members/?sort=join_date&desc=1',
# 'The-Dallas-Japanese-English-Language-Exchange-Group':
# 	'https://www.meetup.com/The-Dallas-Japanese-English-Language-Exchange'\
# 	'-Group/members/?sort=join_date&desc=1',
# 'Dallas-Japanese-Language-Meetup':
# 	'https://www.meetup.com/Dallas-Japanese-Language-Meetup/members/?sort=join_date&desc=1'
# 	}

# Last Page ===
# https://www.meetup.com/Dallas-Japanese-Language-Meetup/members/?offset=40&sort=join_date&desc=1

lname = []
lurl = []
ldateJoined = []
llastVisit = []
lmainBio = []

url = 'https://www.meetup.com/Dallas-Japanese-Language-Meetup/members/?sort=join_date&desc=1'

driver.get(url)

# Get all pages to scrape
for lastPage in driver.find_elements_by_class_name('nav-next'):
	lastUrl = lastPage.get_attribute('href')
	# Get all pages to scrape
	lastOffset = re.findall(r'[?]offset=([0-9]+)', lastUrl)
	print(lastOffset[0])
