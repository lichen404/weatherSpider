# 返回到 19年4月的郑州天气URL
# 在这里可以添加需要爬取的月份和年份
month_list = ['01', '02', '03', '04', '05', '06', '07', '08', '09', '10', '11', '12']
month_list_2019 = ['01', '02', '03', '04']
year_list = [str(2011 + x) for x in range(8)]


def get_url_list(city):
    url_temp = 'http://www.tianqihoubao.com/lishi/{0}/month/{1}.html'

    url_list = []
    for x in month_list:
        for y in year_list:
            url_list.append(url_temp.format(city, y + x))
    for x in month_list_2019:
        url_list.append(url_temp.format(city, '2019' + x))
    return url_list


if __name__ == '__main__':
    url_list = get_url_list("zhengzhou")
    print(url_list)
