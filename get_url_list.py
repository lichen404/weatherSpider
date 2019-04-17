#用于爬取所有城市的URL和对应名称,爬取内容已放在city_config.py
import requests
from bs4 import BeautifulSoup
import time


header = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.121 Safari/537.36',
    'Host': 'www.tianqihoubao.com',

}


def get_province_list():
    target_url = 'http://www.tianqihoubao.com/weather/city.aspx'
    htm = requests.get(target_url, headers=header, timeout=60)
    htm = htm.text
    province_url_list = []
    soup = BeautifulSoup(htm, "lxml")
    box = soup.find("div", class_="box p")
    province_list = box.find_all("a")
    for p in province_list:
        province_url_list.append('http://www.tianqihoubao.com' + p['href'])
    return province_url_list


def get_city_list(province_url_list):

    city_dict = {}
    for url in province_url_list:
        htm = requests.get(url, headers=header, timeout=60)
        htm = htm.content
        htm.decode('utf-8', "ignore")
        soup = BeautifulSoup(htm, "lxml")
        try:
            citychk = soup.find("div", class_="citychk")
            city_node_list = citychk.find_all("a")
            for c in city_node_list:

                url = 'http://www.tianqihoubao.com' + c['href']
                name = c.string
                try:
                    city_dict.update({url: name})
                except Exception as e:
                    pass

                # print('http://www.tianqihoubao.com' + c['href'])

        # 网站上云南的拼音拼成了yunan，导致无法访问...
        except AttributeError:
            htm = requests.get('http://www.tianqihoubao.com/lishi/yunnan.htm', headers=header, timeout=60)
            htm = htm.content
            htm.decode('utf-8', "ignore")
            soup = BeautifulSoup(htm, "lxml")
            citychk = soup.find("div", class_="citychk")
            city_node_list = citychk.find_all("a")
            for c in city_node_list:
                url = 'http://www.tianqihoubao.com' + c['href']
                name = c.string
                try:
                    city_dict.update({url: name})
                except Exception as e:
                    pass

        time.sleep(1)
    # print(city_list)

    return city_dict


if __name__ == '__main__':
    province_url_list = get_province_list()
    city_dict = get_city_list(province_url_list)
    print(city_dict)
