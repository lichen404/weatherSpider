import threading,time,os,queue
import fetch_data
import get_url
import create_htm
import city_url_list
import argparse

class ThreadPool(object):
	def __init__(self,maxsieze):
		self.maxsieze=maxsieze
		self._q=queue.Queue(self.maxsieze)
		for i in range(self.maxsieze):
			self._q.put(threading.Thread)
	def getThread(self):
		return self._q.get()

	def addThread(self):
		self._q.put(threading.Thread)

def task(url,p):
	fetch_data.fetch_data(url)
	time.sleep(1)
	p.addThread()
def main(city):
	pool=ThreadPool(4)
	for url in get_url.get_url_list(city):
		t=pool.getThread()
		a=t(target=task,args=(url,pool))
		a.start()
	create_htm.create_weather_htm(city)
	create_htm.create_temp_htm(city)
	create_htm.create_sun_and_rain_day_htm(city)
	print("finish downloading data and creating html page")
if __name__ == '__main__':
	parser=argparse .ArgumentParser(description='query weather info use this spider')
	parser.add_argument('-c','--city',type=str,help='city name')
	args = parser.parse_args()
	city=args.city
	if 'http://www.tianqihoubao.com/lishi/'+city+'.html' in city_url_list.city_url_set:
		main(city)
	else:
		print('city' +city+ 'not found,please check your input')
		            
	
	