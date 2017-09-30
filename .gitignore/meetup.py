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


# lastPage = 'https://www.meetup.com/Dallas-Japanese-Language-Meetup/members/?offset=40&sort=join_date&desc=1'
# Last offset == 40
offset = 0
url = 'https://www.meetup.com/Dallas-Japanese-Language-Meetup/members/?offset='\
+str(offset)\
+'&sort=join_date&desc=1'

while offset <= 100:
	driver.get(url)
	memberPage = driver.page_source
	bs = BeautifulSoup(memberPage, 'lxml')
	#~ memberList = driver.find_element_by_xpath('//*[@id="member_list"]')
#	bs = BeautifulSoup(memberPage, 'lxml')
	membersList = bs.find('ul',{'id':'memberList'})
	members = membersList.findAll('div',{'class':'margin-bottom unit lastUnit gutter-right member-details wrapNice '})
	for x in members:
		name = x.h4.text.strip()
		lname.append(name)

		url = x.a.attrs['href'].strip()
		lurl.append(url)

		dateJoined = x.span.text.strip()
		ldateJoined.append(dateJoined)

		try:
			lastVisit = x.find('li',{'class':'last'}).text.strip()
			llastVisit.append(lastVisit)
		except:
			llastVisit.append('None')

		try:
			mainBio = x.find('li',{'class':'last bioText'}).text.strip()
			lmainBio.append(mainBio)
		except:
			lmainBio.append('None')
	#driver.find_element_by_xpath('//*[@id="member_list"]/ul[2]/li[4]/a').click()
	offset += 20

df=pd.DataFrame()
df['name']=lname
df['url']=lurl
df['dateJoined']=ldateJoined
df['mainBio']=lmainBio

csvName = input('What do you want to call the csv?')
df.to_csv('{}.csv'.format(csvName), sep=',')

print(df)
