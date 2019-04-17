import threading
import time
import queue
import fetch_data
import url_config
import city_config
import argparse
from progress.bar import Bar


class ThreadPool(object):
    def __init__(self, maxsieze):
        self.maxsieze = maxsieze
        self._q = queue.Queue(self.maxsieze)
        for i in range(self.maxsieze):
            self._q.put(threading.Thread)

    def getThread(self):
        return self._q.get()

    def addThread(self):
        self._q.put(threading.Thread)


def task(url, p):
    fetch_data.fetch_data(url)
    time.sleep(1)
    p.addThread()


def main(city):
    pool = ThreadPool(4)
    url_list = url_config.get_url_list(city)
    num = len(url_list)
    bar = Bar('Downloading', max=num, fill='#', suffix='%(percent)d%%')
    for url in url_list:
        t = pool.getThread()
        a = t(target=task, args=(url, pool))
        a.start()
        bar.next()
    bar.finish()
    # print("finish downloading data and creating html page")


if __name__ == '__main__':
    start = time.time()
    parser = argparse .ArgumentParser(description='query weather info use this spider')
    parser.add_argument('-c', '--city', type=str, help='city name')
    args = parser.parse_args()
    city = args.city
    if 'http://www.tianqihoubao.com/lishi/' + city + '.html' in city_config.city_dict:
        main(city)
    else:
        print('city' + city + 'not found,please check your input')
    end = time.time()
    print("Finshed in", int(end - start), "s")
