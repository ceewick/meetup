import time
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from bs4 import BeautifulSoup
import lxml
import pandas as pd

username = <str(YOUR USERNAME)>
password = <str(YOUR PASSWORD)>

driver = webdriver.Chrome()  # Optional argument, if not specified will search path.
driver.get('https://secure.meetup.com/login/');
time.sleep(1) # Let the user actually see something!

logUser = driver.find_element_by_name(username)
logUser.send_keys(username) # input personal User Name for meetup.com

logPassword = driver.find_element_by_name('password')
logPassword.send_keys(password + Keys.RETURN)

## Note above two variables, change for person

time.sleep(1) # Pause, let user see something

# groups = {
# 'japanfans':
# 'The-Dallas-Japanese-English-Language-Exchange-Group':
# 	'https://www.meetup.com/The-Dallas-Japanese-English-Language-Exchange'\
# 	'-Group/members/?sort=join_date&desc=1',
# 'Dallas-Japanese-Language-Meetup':
# 	'https://www.meetup.com/Dallas-Japanese-Language-Meetup/members/?sort=join_date&desc=1'
# 	}

lname = []
lurl = []
ldateJoin = []
llastVisit = []
lmainBio = []

offset = 0

while offset <= 1420: #This should be the offset # in url from last page of member list...
# 	'https://www.meetup.com/japanfans/members/?sort=join_date&desc=1',
# last page = 'https://www.meetup.com/japanfans/members/?offset=1420&sort=join_date&desc=1'
	url = 'https://www.meetup.com/japanfans/members/?offset='+str(offset)\
	+'&sort=join_date&desc=1'
	driver.get(url)
	memberPage = driver.page_source
	#~ memberList = driver.find_element_by_xpath('//*[@id="member_list"]')
	bs = BeautifulSoup(memberPage)#, 'lxml')
	membersList = bs.find('ul',{'id':'memberList'})
	membersList = membersList.findAll('div',{'class':'margin-bottom unit lastUnit gutter-right member-details wrapNice '})

	for x in membersList:
		name = x.h4.text.strip()
		lname.append(name)

		url = x.a.attrs['href'].strip()
		lurl.append(url)

		dateJoin = x.span.text.strip()
		ldateJoin.append(dateJoin)

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
df['dateJoined']=ldateJoin
df['mainBio']=lmainBio

csvName = input('What do you want to call the csv?')
df.to_csv('{}.csv'.format(csvName), sep=',')

print(df)
