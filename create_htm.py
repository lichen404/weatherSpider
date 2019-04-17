from pyecharts import Line, Pie, WordCloud
from pymongo import MongoClient
import city_config


# 生成历年气温变化表


def create_temp_htm(city):
    client = MongoClient('localhost', 27017)
    db = client['tianqihoubao']
    data = db[city]
    max_temp_list = []
    min_temp_list = []
    day_list = []
    results = data.find({}).sort([("date", 1)])
    for d in results:
        max_temp_list.append(d['max_temp'])
        min_temp_list.append(d['min_temp'])
        day_list.append(d['date'])
    city_name = get_city_name(city)
    line = Line(city_name + "2011年至今气温变化", page_title="气温变化表")
    line.add(
        "最高温度",
        day_list,
        max_temp_list,
        mark_point=["max", "min"],
        mark_line=["average"],
    )
    line.add(
        "最低温度",
        day_list,
        min_temp_list,
        mark_point=["max", "min"],
        mark_line=["average"],
        yaxis_formatter="°C",
    )
    line.render(city_name + '气温变化表.html')

# 生成天气占比表


def create_weather_htm(city):
    attr = ["雨", "多云", "晴", "阴", "雪", "雾", "霾"]
    client = MongoClient('localhost', 27017)
    db = client['tianqihoubao']
    data = db[city]
    rain = data.count_documents({"weather": {"$regex": "雨"}})
    sun = data.count_documents({"weather": {"$regex": "晴"}})
    cloud = data.count_documents({"weather": {"$regex": "多云"}})
    overcast = data.count_documents({"weather": {"$regex": "阴"}})
    snow = data.count_documents({"weather": {"$regex": "雪"}})
    fog = data.count_documents({"weather": {"$regex": "雾"}})
    smog = data.count_documents({"weather": {"$regex": "霾"}})
    weather = [rain, cloud, sun, overcast, snow, fog, smog]
    city_name = get_city_name(city)
    pie = Pie(city_name + "历史天气占比", title_pos='left', page_title="历史天气占比表")
    pie.add(
        "",
        attr,
        weather,
        is_random=False,
        radius=[40, 75],
        center=[50, 60],
        rosetype="radius",
        label_text_color=None,
        is_label_show=True,
        legend_pos="center",
        label_color=['#313695', '#74add1', '#DC143C', '#708090', '#e0f3f8', '#ffffbf', '#fee090']
    )

    pie.render(city_name + '历史天气占比表.html')


# 生成历年晴雨天数表


def create_sun_and_rain_day_htm(city):
    client = MongoClient('localhost', 27017)
    db = client['tianqihoubao']
    data = db[city]
    year_list = [str(x + 2011) for x in range(8)]
    sun_day_list = []
    rain_day_list = []
    for num in range(8):
        sun_day_count = data.count_documents(
            {"weather": {"$regex": "晴/晴"}, "date": {"$regex": str(2011 + num)}})
        rain_day_count = data.count_documents(
            {"weather": {"$regex": "雨"}, "date": {"$regex": str(2011 + num)}})
        sun_day_list.append(sun_day_count)
        rain_day_list.append(rain_day_count)
    # print(sun_day_list)
    # print(rain_day_list)
    city_name = get_city_name(city)
    line = Line(city_name + "历年晴雨天数", page_title="历年晴雨天数表")
    line.add(
        "晴天数",
        year_list,
        sun_day_list,
        mark_point=["max", "min"],
        mark_line=["average"],


    )
    line.add(
        "雨天数",
        year_list,
        rain_day_list,
        mark_point=["max", "min"],
        mark_line=["average"],

    )
    line.render(city_name + "历年晴雨天数表.html")

# 获取城市中文名称


def get_city_name(city):
    city_url = 'http://www.tianqihoubao.com/lishi/' + city + '.html'
    city_name = city_config.city_dict[city_url]
    return city_name

# 获取城市六月份天气关键词词云


def create_city_wordcloud(city):
    city_name = get_city_name(city)
    client = MongoClient('localhost', 27017)
    db = client['tianqihoubao']
    data = db[city]
    keywords = ["小雨", "雷阵雨", "中雨", "大雨", "暴雨", "晴", "雾", "阴", "小到中雨", "多云", "中到大雨", "大到暴雨", "阵雨"]
    values = []
    for k in keywords:
        value = data.count_documents({"weather": {"$regex": k}, "date": {"$regex": "06月"}})
        values.append(value)
    wordcloud = WordCloud(city_name + "六月天气词云", width=1000, height=620, page_title="六月天气词云")
    wordcloud.add("", keywords, values, word_size_range=[20, 100])
   
    wordcloud.render(city_name + "词云图.html")


if __name__ == '__main__':
    create_weather_htm("dali")
    create_temp_htm("dali")
    create_sun_and_rain_day_htm("dali")
    create_city_wordcloud("dali")
