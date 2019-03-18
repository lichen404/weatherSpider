from pyecharts import Line,Pie
from pymongo import MongoClient

#生成历年气温变化表
def create_temp_htm(city):
	client = MongoClient('localhost', 27017)
	db = client['tianqihoubao']
	data = db[city]
	max_temp_list = []
	min_temp_list = []
	day_list = []
	results = data.find({}).sort([("date",1)])
	for d in results:
	    max_temp_list.append(d['max_temp'])
	    min_temp_list.append(d['min_temp'])
	    day_list.append(d['date'])
	    line = Line("2011年至今气温变化")
	line.add(
	    "最高温度",
	    day_list,
	    max_temp_list,
	    mark_point=["max","min"],
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
	line.render(city+'气温变化表.html')

#生成天气占比表
def create_weather_htm(city):
	attr = ["雨", "多云", "晴", "阴", "雪", "雾","霾"]
	client = MongoClient('localhost', 27017)
	db = client['tianqihoubao']
	data = db[city]
	rain=data.find({"weather":{"$regex":"雨"}}).count()
	sun=data.find({"weather":"晴"}).count()
	cloud=data.find({"weather":"多云"}).count()
	overcast=data.find({"weather":"阴"}).count()
	snow=data.find({"weather":{"$regex":"雪"}}).count()
	fog=data.find({"weather":"雾"}).count()
	smog=data.find({"weather":"霾"}).count()
	weather=[rain,cloud,sun,overcast,snow,fog,smog]
	pie = Pie("历史天气占比", title_pos='left')
	pie.add(
	    "",
	    attr,
	    weather,
	    is_random=True,
	    radius=[40, 75],
	    center=[50,60],
	    rosetype="radius",
	    label_text_color=None,
	    is_label_show=True,
	    legend_pos="center",
	)

	pie.render(city+'历史天气占比表.html')


#生成历年晴雨天数表
def create_sun_and_rain_day_htm(city):
	client = MongoClient('localhost', 27017)
	db = client['tianqihoubao']
	data = db[city]
	year_list=[str(x+2011) for x in range(8)]
	sun_day_list=[]
	rain_day_list = []
	for num in range(8):
	    sun_day_count=data.find({"weather":"晴","date":{"$regex":str(2011+num)}}).count()
	    rain_day_count=data.find({"weather":{"$regex":"雨"},"date":{"$regex":str(2011+num)}}).count()
	    sun_day_list.append(sun_day_count)
	    rain_day_list.append(rain_day_count)
	#print(sun_day_list)
	#print(rain_day_list)


	line = Line("历年晴雨天数")
	line.add(
	    "晴天数",
	    year_list,
	    sun_day_list,
	    mark_point=["max","min"],
	    mark_line=["average"],
	  

	)
	line.add(
	    "雨天数",
	    year_list,
	    rain_day_list,
	    mark_point=["max", "min"],
	    mark_line=["average"],
	   
	)
	line.render(city+"历年晴雨天数表.html")

if __name__ == '__main__':
	create_weather_htm("sheqi")
	create_temp_htm("sheqi")
	create_sun_and_rain_day_htm("sheqi")