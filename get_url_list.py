import requests
from bs4 import BeautifulSoup
import time

header = {
	'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.121 Safari/537.36',
	'Host': 'www.tianqihoubao.com',

	}

def get_province_list():
	target_url='http://www.tianqihoubao.com/weather/city.aspx'
	htm=requests.get(target_url,headers=header,timeout=60)
	htm=htm.text
	province_url_list=[]
	soup = BeautifulSoup(htm, "lxml")
	box=soup.find("div",class_="box p")
	province_list=box.find_all("a")
	for p in province_list:
		province_url_list.append('http://www.tianqihoubao.com'+p['href'])
	return province_url_list

def get_city_list(province_url_list):
	city_url_list=[]
	for url in province_url_list:
		htm=requests.get(url,headers=header,timeout=60)
		htm=htm.text
		soup=BeautifulSoup(htm,"lxml")
		try:
			citychk=soup.find("div",class_="citychk")
			city_list=citychk.find_all("a")
			for c in city_list:
				city_url_list.append('http://www.tianqihoubao.com'+c['href'])
				print('http://www.tianqihoubao.com'+c['href'])
		except AttributeError:
			pass
	
		time.sleep(1)
	print(city_url_list)


province_url_list=get_province_list()
city_url_list=get_city_list(province_url_list)


	