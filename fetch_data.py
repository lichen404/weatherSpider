import requests
from bs4 import BeautifulSoup
import re
from pymongo import MongoClient


target_url = 'http://www.tianqihoubao.com/lishi/zhengzhou/month/201901.html'


def fetch_data(url):
    header = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.121 Safari/537.36',
        'Host': 'www.tianqihoubao.com',
        'Referer': 'http://www.tianqihoubao.com/lishi/zhengzhou.html'
    }
    htm = requests.get(url, headers=header, timeout=60)
    htm = htm.text
    city = url.split('/')[4]

    data_list = []
    soup = BeautifulSoup(htm, "lxml")
    tr = soup.select('tr')
    for td in tr:
        tds = td.select('td')
        date = re.sub('\r|\n', '', str(tds[0].get_text())).replace(' ', '')
        weather = re.sub('\r|\n', '', tds[1].get_text()).replace(' ', '')
        temp = re.sub('\r|\n', '', tds[2].get_text()).replace(' ', '')
        wind = re.sub('\r|\n', '', tds[3].get_text()).replace(' ', '')
        data_list.append({
            'date': date,
            'weather': weather,
            'temp': temp,
            'wind': wind,
        })
    # print('downloading data from ' + url)
    return (format_data(data_list[1:], city))  # 剔除表格头部


def format_data(data_list, city):
    format_data_list = []
    for d in data_list:
        '''d['weather'] = d['weather'].split('/')[0]
        d['wind'] = d['wind'].split('/')[0]'''
        try:

            max_temp = int(d['temp'].split('/')[0].replace('℃', ''))  # 温度值可能为空字符串
            d.update({'max_temp': max_temp})
        except ValueError:
            d.update({'max_temp': None})
        try:
            min_temp = int(d['temp'].split('/')[1].replace('℃', ''))
            d.update({'min_temp': min_temp})
        except ValueError:
            d.update({'min_temp': None})
        d.pop('temp')
        store_data(d, city)
        format_data_list.append(d)
    return format_data_list


def store_data(data, city):
    client = MongoClient('localhost', 27017)
    db = client['tianqihoubao']
    posts = db[city]
    posts.insert_one(data)


if __name__ == '__main__':
    results = fetch_data(target_url)

    print(results)
